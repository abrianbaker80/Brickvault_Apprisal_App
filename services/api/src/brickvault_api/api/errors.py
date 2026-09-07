from uuid import UUID

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

ERRORS = {
    400: ("BAD_REQUEST", "Invalid request"),
    403: ("FORBIDDEN", "Request forbidden"),
    404: ("NOT_FOUND", "Resource not found"),
    405: ("METHOD_NOT_ALLOWED", "Method not allowed"),
    422: ("VALIDATION_ERROR", "Invalid request data"),
    500: ("INTERNAL_ERROR", "Internal server error"),
}


class ErrorDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str
    message: str
    request_id: UUID


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    error: ErrorDetail


def error_response(status: int, request_id: str) -> JSONResponse:
    code, message = ERRORS.get(status, ERRORS[500])
    return JSONResponse(
        ErrorResponse(
            error=ErrorDetail(code=code, message=message, request_id=UUID(request_id))
        ).model_dump(mode="json"),
        status_code=status if status in ERRORS else 500,
    )


async def http_error(request: Request, exception: Exception) -> JSONResponse:
    assert isinstance(exception, HTTPException)
    response = error_response(exception.status_code, request.state.request_id)
    if exception.status_code == 405 and exception.headers and "Allow" in exception.headers:
        response.headers["Allow"] = exception.headers["Allow"]
    return response


async def validation_error(request: Request, exception: Exception) -> JSONResponse:
    assert isinstance(exception, RequestValidationError)
    return error_response(422, request.state.request_id)
