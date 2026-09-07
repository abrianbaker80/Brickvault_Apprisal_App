from typing import Literal

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, ConfigDict
from starlette.responses import JSONResponse

from brickvault_api.application.readiness import NotReady, Ready, check_readiness

router = APIRouter(prefix="/api")


class Health(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service: Literal["brickvault-api"] = "brickvault-api"
    status: Literal["ok"] = "ok"


@router.get("/health", response_model=Health, operation_id="health")
def health() -> Health:
    return Health()


@router.get(
    "/ready", response_model=Ready, responses={503: {"model": NotReady}}, operation_id="ready"
)
def ready(request: Request, response: Response) -> Ready | JSONResponse:
    result = check_readiness(request.app.state.engine)
    if not isinstance(result, Ready):
        return JSONResponse(result.model_dump(), status_code=503)
    return result
