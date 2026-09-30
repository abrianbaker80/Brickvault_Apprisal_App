"""HTTP authentication boundary shared by every registered API route."""

from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, SecretStr

from brickvault_api.auth import ABSOLUTE_SECONDS, AuthError, AuthService, Session

SESSION_COOKIE = "bva_session"
CSRF_COOKIE = "bva_csrf"
router = APIRouter(prefix="/api/auth")


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)
    password: SecretStr


class SessionState(BaseModel):
    principal_id: UUID
    idle_expires_at: datetime
    absolute_expires_at: datetime
    csrf_token: str


def service(request: Request) -> AuthService:
    auth: AuthService | None = getattr(request.app.state, "auth", None)
    if auth is None:
        raise HTTPException(503)
    return auth


def transport(request: Request) -> bool:
    settings = getattr(request.app.state, "settings", None)
    if settings is not None and settings.purpose == "production":
        if not getattr(request.state, "production_proxy_verified", False):
            raise HTTPException(503)
        return True
    if request.url.scheme == "https":
        return True
    if (
        settings is None
        or not settings.auth_allow_loopback_http
        or settings.purpose not in ("development", "test")
        or request.url.hostname not in ("localhost", "127.0.0.1")
    ):
        raise HTTPException(503)
    return False


def cookie(request: Request, name: str) -> str | None:
    occurrences = sum(
        part.strip().split("=", 1)[0] == name
        for header in request.headers.getlist("cookie")
        for part in header.split(";")
    )
    if occurrences > 1:
        raise HTTPException(401)
    return request.cookies.get(name)


def require_auth(request: Request, response: Response) -> None:
    path = request.url.path
    if not path.startswith("/api/") or path in ("/api/health", "/api/auth/login"):
        return
    token = cookie(request, SESSION_COOKIE)
    if token is None:
        raise HTTPException(401)
    transport(request)
    mutate = request.method not in ("GET", "HEAD", "OPTIONS")
    csrf = request.headers.get("x-csrf-token") if mutate else None
    if mutate and (
        not csrf
        or len(request.headers.getlist("x-csrf-token")) != 1
        or not request.headers.get("origin")
    ):
        raise HTTPException(403)
    activity = (
        path.startswith("/api/sets/")
        and (
            path.endswith(("/search", "/appraisal", "/deal-economics", "/plan"))
            or request.method == "POST"
        )
        or (
            request.method == "POST"
            and path.startswith("/api/deal-forecasts/")
            and path.endswith("/revision-preview")
        )
        or (
            request.method == "POST"
            and path.startswith("/api/market-refresh/")
            and path.endswith("/resume")
        )
        or (
            path.startswith(("/api/settings", "/api/selling-profiles"))
            and request.method in ("POST", "PUT", "DELETE")
        )
        or (path.startswith("/api/hunt/runs") and request.method == "POST")
        or (path.startswith("/api/watchlist") and request.method in ("POST", "PATCH", "DELETE"))
    )
    # Automatic reconnect reads cannot extend inactivity. This marker only
    # reduces activity; authentication, CSRF and expiry checks remain authoritative.
    if request.method == "GET" and request.headers.get("x-brickvault-passive") == "1":
        activity = False
    try:
        request.state.principal = service(request).check(token, csrf, activity=activity)
        response.headers["X-Session-Idle-Expires"] = (
            request.state.principal.idle_expires_at.isoformat()
        )
        response.headers["X-Session-Absolute-Expires"] = (
            request.state.principal.absolute_expires_at.isoformat()
        )
    except AuthError as error:
        raise HTTPException(error.status) from None
    except Exception:
        raise HTTPException(503) from None


def state(session: Session, csrf: str) -> SessionState:
    return SessionState(**asdict(session), csrf_token=csrf)


@router.post("/login", response_model=SessionState, operation_id="login")
def login(body: LoginRequest, request: Request, response: Response) -> SessionState:
    secure = transport(request)
    # RequestBoundary validates exact allowed origins. Absence is not browser consent.
    if not request.headers.get("origin") or request.headers.get("x-brickvault-login") != "1":
        raise HTTPException(403)
    try:
        token, csrf, session = service(request).login(
            body.password.get_secret_value(), cookie(request, SESSION_COOKIE)
        )
    except AuthError as error:
        raise HTTPException(error.status) from None
    except Exception:
        raise HTTPException(503) from None
    for name, value in ((SESSION_COOKIE, token), (CSRF_COOKIE, csrf)):
        response.set_cookie(
            name,
            value,
            max_age=ABSOLUTE_SECONDS,
            httponly=True,
            secure=secure,
            samesite="strict",
            path="/",
        )
    return state(session, csrf)


@router.get("/session", response_model=SessionState, operation_id="session_state")
def session_state(request: Request) -> SessionState:
    csrf = cookie(request, CSRF_COOKIE)
    if csrf is None:
        raise HTTPException(401)
    try:
        session = service(request).check(cookie(request, SESSION_COOKIE), csrf)
    except AuthError as error:
        raise HTTPException(error.status) from None
    except Exception:
        raise HTTPException(503) from None
    return state(session, csrf)


@router.post("/logout", status_code=204, operation_id="logout")
def logout(request: Request, response: Response) -> None:
    try:
        service(request).check(
            cookie(request, SESSION_COOKIE), request.headers.get("x-csrf-token"), logout=True
        )
    except AuthError as error:
        raise HTTPException(error.status) from None
    except Exception:
        raise HTTPException(503) from None
    for name in (SESSION_COOKIE, CSRF_COOKIE):
        response.delete_cookie(
            name, path="/", httponly=True, secure=transport(request), samesite="strict"
        )
