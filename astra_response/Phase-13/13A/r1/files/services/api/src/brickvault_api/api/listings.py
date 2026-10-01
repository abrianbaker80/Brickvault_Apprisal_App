"""Private listing endpoints and bounded, independently committed multipart uploads."""

import re
from collections.abc import Iterator
from typing import Annotated, Any
from uuid import UUID

import psycopg
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile
from starlette.responses import JSONResponse, StreamingResponse

from brickvault_api.api.auth import SESSION_COOKIE, cookie
from brickvault_api.api.errors import ErrorResponse
from brickvault_api.auth import AuthError
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.images.processing import MAX_FILE_BYTES, MAX_REQUEST_BYTES
from brickvault_api.images.storage import BlobStore, ImageError
from brickvault_api.listings.models import (
    ListingCreate,
    ListingDetail,
    ListingPage,
    ListingProblem,
    ListingResponse,
    UploadArguments,
    UploadBody,
    UploadProblem,
    UploadResult,
)
from brickvault_api.listings.service import ListingService

router = APIRouter(prefix="/api")
IMAGE_ERRORS: dict[int | str, dict[str, Any]] = {
    code: {"model": UploadResult | ListingProblem | ErrorResponse}
    for code in (400, 404, 409, 413, 422, 503)
}


def service(request: Request) -> ListingService:
    settings = request.app.state.settings
    if settings.database_ownership_marker is None:
        raise HTTPException(503)
    return ListingService(
        CatalogDatabase(
            settings.database_url.get_secret_value(),
            settings.purpose,
            settings.database_ownership_marker.get_secret_value(),
            role="runtime",
        ),
        request.app.state.image_store,
    )


def problem(
    error: ImageError, arguments: UploadArguments | None = None, filename: str = "image"
) -> JSONResponse:
    if arguments is not None:
        return JSONResponse(
            UploadResult(
                client_upload_id=arguments.client_upload_id,
                filename=filename,
                status="failed",
                listing_image_id=None,
                error=UploadProblem(
                    code=error.code, message="Image upload could not be completed."
                ),
            ).model_dump(mode="json"),
            status_code=error.status,
        )
    return JSONResponse(
        {"error": {"code": error.code, "message": "Image/listing request could not be completed."}},
        status_code=error.status,
    )


@router.post(
    "/listings", status_code=201, response_model=ListingResponse, operation_id="create_listing"
)
def create_listing(request: Request, body: ListingCreate) -> object:
    try:
        return service(request).create(
            cookie(request, SESSION_COOKIE), request.headers["x-csrf-token"], body
        )
    except AuthError as error:
        raise HTTPException(error.status) from None


@router.get("/listings", response_model=ListingPage, operation_id="list_listings")
def list_listings(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0, le=1000000)] = 0,
) -> object:
    try:
        return service(request).list(cookie(request, SESSION_COOKIE), limit, offset)
    except AuthError as error:
        raise HTTPException(error.status) from None


@router.get(
    "/listings/{listing_id}",
    response_model=ListingDetail,
    operation_id="get_listing",
    responses=IMAGE_ERRORS,
)
def get_listing(request: Request, listing_id: UUID) -> object:
    try:
        return service(request).detail(cookie(request, SESSION_COOKIE), listing_id)
    except ImageError as error:
        return problem(error)
    except AuthError as error:
        raise HTTPException(error.status) from None


@router.post(
    "/listings/{listing_id}/images",
    response_model=UploadResult,
    status_code=201,
    operation_id="upload_listing_image",
    responses={**IMAGE_ERRORS, 200: {"model": UploadResult}},
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {"multipart/form-data": {"schema": UploadBody.model_json_schema()}},
        }
    },
)
async def upload_image(request: Request, listing_id: UUID) -> object:
    # Auth/Origin/CSRF dependencies run before this manually parsed body. Bound
    # chunked bodies before multipart spooling, then close every parsed upload.
    arguments: UploadArguments | None = None
    filename = "image"
    try:
        declared = request.headers.get("content-length")
        if declared is not None and (not declared.isdecimal() or int(declared) > MAX_REQUEST_BYTES):
            raise ImageError("IMAGE_REQUEST_TOO_LARGE", 413)
        body = bytearray()
        async for chunk in request.stream():
            if len(body) + len(chunk) > MAX_REQUEST_BYTES:
                raise ImageError("IMAGE_REQUEST_TOO_LARGE", 413)
            body.extend(chunk)
        delivered = False

        async def receive() -> dict[str, object]:
            nonlocal delivered
            if delivered:
                return {"type": "http.disconnect"}
            delivered = True
            return {"type": "http.request", "body": bytes(body), "more_body": False}

        parsed_request = Request(request.scope, receive=receive)  # type: ignore[arg-type]
        async with parsed_request.form(
            max_files=1, max_fields=2, max_part_size=MAX_REQUEST_BYTES
        ) as form:
            if len(form.multi_items()) != 3 or set(form) != {
                "file",
                "client_upload_id",
                "display_order",
            }:
                raise ImageError("INVALID_MULTIPART")
            file = form["file"]
            if (
                not isinstance(file, UploadFile)
                or not isinstance(form["client_upload_id"], str)
                or not isinstance(form["display_order"], str)
            ):
                raise ImageError("INVALID_MULTIPART")
            raw_order = str(form["display_order"])
            if re.fullmatch(r"0|[1-9][0-9]{0,9}", raw_order) is None:
                raise ImageError("INVALID_DISPLAY_ORDER")
            arguments = UploadArguments(
                client_upload_id=UUID(str(form["client_upload_id"])), display_order=int(raw_order)
            )
            data = await file.read(MAX_FILE_BYTES + 1)
            filename = (file.filename or "image").replace("\\", "/").split("/")[-1]
            filename = (
                "".join(c for c in filename if ord(c) >= 32 and ord(c) != 127)[:255] or "image"
            )
            code, result = await run_in_threadpool(
                service(request).upload,
                cookie(request, SESSION_COOKIE),
                request.headers["x-csrf-token"],
                listing_id,
                arguments,
                filename,
                data,
            )
            return JSONResponse(result, status_code=code)
    except ImageError as error:
        return problem(error, arguments, filename)
    except AuthError as error:
        error_code = {401: "UNAUTHENTICATED", 403: "FORBIDDEN"}.get(
            error.status, "SERVICE_UNAVAILABLE"
        )
        return problem(ImageError(error_code, error.status), arguments, filename)
    except psycopg.Error:
        return problem(ImageError("IMAGE_DATABASE_UNAVAILABLE", 503), arguments, filename)
    except (ValueError, ValidationError):
        return problem(ImageError("INVALID_UPLOAD_ARGUMENTS"))
    except HTTPException:
        return problem(ImageError("INVALID_MULTIPART", 400))


def content_chunks(store: BlobStore, digest: str) -> Iterator[bytes]:
    with store.read(digest) as source:
        while chunk := source.read(1024 * 1024):
            yield chunk


@router.get(
    "/images/{asset_id}/content",
    response_class=StreamingResponse,
    operation_id="image_content",
    responses={
        **IMAGE_ERRORS,
        200: {
            "content": {
                t: {"schema": {"type": "string", "format": "binary"}}
                for t in ("image/jpeg", "image/png", "image/webp")
            }
        },
    },
)
def image_content(request: Request, asset_id: UUID) -> object:
    try:
        current = service(request)
        if current.store is None:
            raise ImageError("IMAGE_STORAGE_NOT_CONFIGURED", 503)
        digest, media_type = current.content(cookie(request, SESSION_COOKIE), asset_id)
        # Verify before sending response headers; fail closed on missing/corrupt bytes.
        current.store.stat(digest)
        return StreamingResponse(
            content_chunks(current.store, digest),
            media_type=media_type,
            headers={"Content-Disposition": "inline", "X-Content-Type-Options": "nosniff"},
        )
    except ImageError as error:
        return problem(error)
    except AuthError as error:
        raise HTTPException(error.status) from None
