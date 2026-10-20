"""Private actual-outcome routes on existing saved forecasts."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from starlette.responses import JSONResponse

from brickvault_api.auth import AuthError
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.outcome_models import (
    OutcomeAppend,
    OutcomeEntry,
    OutcomeErrorCode,
    OutcomeProblem,
    OutcomeProblemDetail,
    OutcomeResponse,
)
from brickvault_api.outcomes import OutcomeError, OutcomeService

from .auth import SESSION_COOKIE, cookie

router = APIRouter(prefix="/api/deal-forecasts")
RESPONSES: dict[int | str, dict[str, Any]] = {
    code: {"model": OutcomeProblem} for code in (404, 409, 422, 503)
}


def service(request: Request) -> OutcomeService:
    settings = request.app.state.settings
    if settings.database_ownership_marker is None:
        raise HTTPException(503)
    return OutcomeService(
        CatalogDatabase(
            settings.database_url.get_secret_value(),
            settings.purpose,
            settings.database_ownership_marker.get_secret_value(),
            role="runtime",
        )
    )


Service = Annotated[OutcomeService, Depends(service)]


def problem(request: Request, error: OutcomeError) -> JSONResponse:
    details: dict[str, tuple[int, OutcomeErrorCode, str]] = {
        "OUTCOME_NOT_FOUND": (404, "OUTCOME_NOT_FOUND", "Saved deal or outcome entry not found."),
        "OUTCOME_CONFLICT": (409, "OUTCOME_CONFLICT", "Outcome changed. Reload before correcting."),
        "OUTCOME_ID_REUSED": (409, "OUTCOME_ID_REUSED", "Submission identity was already used."),
        "OUTCOME_INVALID_CHRONOLOGY": (
            422,
            "OUTCOME_INVALID_CHRONOLOGY",
            "The original forecast date is after the stated acquisition date; it cannot precede purchase.",
        ),
    }
    status, code, message = details.get(
        error.code,
        (
            503,
            "OUTCOME_UNAVAILABLE",
            "Actual outcome is temporarily unavailable.",
        ),
    )
    return JSONResponse(
        OutcomeProblem(
            error=OutcomeProblemDetail(
                code=code,
                message=message,
                request_id=UUID(request.state.request_id),
            )
        ).model_dump(mode="json"),
        status_code=status,
        headers={"Cache-Control": "no-store"},
    )


@router.get(
    "/{identifier}/outcome",
    operation_id="get_deal_outcome",
    response_model=OutcomeResponse,
    responses=RESPONSES,
)
def get_outcome(
    identifier: UUID,
    request: Request,
    response: Response,
    service: Service,
    before_revision: Annotated[int | None, Query(ge=1, le=2_147_483_647)] = None,
) -> OutcomeResponse | JSONResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return service.get(
            cookie(request, SESSION_COOKIE), identifier, before_revision=before_revision
        )
    except OutcomeError as error:
        return problem(request, error)
    except AuthError as error:
        raise HTTPException(error.status) from None


@router.post(
    "/{identifier}/outcome",
    operation_id="append_deal_outcome",
    response_model=OutcomeEntry,
    responses=RESPONSES,
)
def append_outcome(
    identifier: UUID,
    body: OutcomeAppend,
    request: Request,
    response: Response,
    service: Service,
) -> OutcomeEntry | JSONResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return service.append(
            cookie(request, SESSION_COOKIE),
            request.headers.get("x-csrf-token"),
            identifier,
            body,
        )
    except OutcomeError as error:
        return problem(request, error)
    except AuthError as error:
        raise HTTPException(error.status) from None


@router.get(
    "/{identifier}/outcome/entries/{entry_id}",
    operation_id="get_deal_outcome_entry",
    response_model=OutcomeEntry,
    responses=RESPONSES,
)
def get_entry(
    identifier: UUID,
    entry_id: UUID,
    request: Request,
    response: Response,
    service: Service,
) -> OutcomeEntry | JSONResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return service.entry(cookie(request, SESSION_COOKIE), identifier, entry_id)
    except OutcomeError as error:
        return problem(request, error)
    except AuthError as error:
        raise HTTPException(error.status) from None
