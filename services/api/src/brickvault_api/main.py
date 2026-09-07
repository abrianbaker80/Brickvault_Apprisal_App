import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from brickvault_api.api.errors import ERRORS, ErrorResponse, http_error, validation_error
from brickvault_api.api.health import router
from brickvault_api.observability import RequestBoundary, logging_config
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.settings import RuntimeSettings


def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        configured = settings if settings is not None else RuntimeSettings.from_environment()
        configured.target()
        engine = create_database_engine(
            configured.database_url.get_secret_value(), configured.purpose
        )
        application.state.settings = configured
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
        responses={
            code: {"model": ErrorResponse, "description": message}
            for code, (_, message) in ERRORS.items()
        },
    )
    application.add_middleware(RequestBoundary)
    application.add_exception_handler(HTTPException, http_error)
    application.add_exception_handler(RequestValidationError, validation_error)
    application.include_router(router)

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
