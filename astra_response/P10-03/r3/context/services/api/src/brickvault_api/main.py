import json
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from brickvault_api.api.auth import require_auth
from brickvault_api.api.auth import router as auth_router
from brickvault_api.api.errors import ERRORS, ErrorResponse, http_error, validation_error
from brickvault_api.api.forecasts import router as forecasts_router
from brickvault_api.api.health import router
from brickvault_api.api.hunt import router as hunt_router
from brickvault_api.api.lineage_metadata import router as lineage_metadata_router
from brickvault_api.api.profiles import router as profiles_router
from brickvault_api.api.refresh import router as refresh_router
from brickvault_api.api.sets import router as sets_router
from brickvault_api.api.static import load_build
from brickvault_api.api.static import router as static_router
from brickvault_api.api.watchlist import router as watchlist_router
from brickvault_api.auth import AuthService
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.observability import RequestBoundary, logging_config
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.settings import RuntimeSettings


def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        configured = settings if settings is not None else RuntimeSettings.from_environment()
        configured.target()
        application.state.build = (
            load_build(configured.web_build_dir) if configured.static_enabled else None
        )
        engine = create_database_engine(
            configured.database_url.get_secret_value(), configured.purpose
        )
        application.state.settings = configured
        application.state.auth = (
            AuthService(
                CatalogDatabase(
                    configured.database_url.get_secret_value(),
                    configured.purpose,
                    configured.database_ownership_marker.get_secret_value(),
                    role="runtime",
                )
            )
            if configured.database_ownership_marker
            else None
        )
        application.state.refresh_signing_key = secrets.token_bytes(32)
        application.state.engine = engine
        try:
            yield
        finally:
            engine.dispose()

    application = FastAPI(
        title="BrickVault Appraisal App API",
        version="0.0.0",
        lifespan=lifespan,
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
        dependencies=[Depends(require_auth)],
        responses={
            code: {"model": ErrorResponse, "description": message}
            for code, (_, message) in ERRORS.items()
        },
    )
    application.add_middleware(RequestBoundary)
    application.add_exception_handler(HTTPException, http_error)
    application.add_exception_handler(RequestValidationError, validation_error)
    application.include_router(router)
    application.include_router(auth_router)
    application.include_router(sets_router)
    application.include_router(forecasts_router)
    application.include_router(hunt_router)
    application.include_router(lineage_metadata_router)
    application.include_router(watchlist_router)
    application.include_router(profiles_router)
    application.include_router(refresh_router)
    application.include_router(static_router)

    @application.get(
        "/api/openapi.json",
        operation_id="openapi_document",
        response_class=Response,
        responses={
            200: {
                "content": {
                    "application/json": {"schema": {"type": "object", "additionalProperties": True}}
                }
            }
        },
    )
    def openapi_document() -> Response:
        return Response(schema_bytes(application), media_type="application/json")

    return application


def schema_bytes(application: FastAPI) -> bytes:
    return (
        json.dumps(application.openapi(), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


app = create_app()


def serve() -> None:
    configured = RuntimeSettings.from_environment()
    uvicorn.run(
        create_app(configured),
        host="127.0.0.1",
        port=configured.port,
        access_log=False,
        proxy_headers=False,
        log_config=logging_config(configured.log_level),
    )


if __name__ == "__main__":
    serve()
