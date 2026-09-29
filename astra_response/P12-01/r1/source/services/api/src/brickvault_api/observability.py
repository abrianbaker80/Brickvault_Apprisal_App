"""Only allowlisted metadata reaches structured logs, including server diagnostics."""

import json
import logging
import secrets
import time
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from brickvault_api.api.errors import error_response

logger = logging.getLogger("brickvault.requests")
METHODS = {"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"}
NATIVE_ORIGIN = b"https://localhost"
CORS_METHODS = b"GET, POST, PUT, PATCH, DELETE"
CORS_HEADERS = b"Content-Type, X-BrickVault-Login, X-CSRF-Token, X-BrickVault-Passive"
CORS_EXPOSE = b"X-Session-Idle-Expires, X-Session-Absolute-Expires"


class SafeFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        event: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "severity": record.levelname,
            "category": "server",
        }
        metadata = getattr(record, "safe_metadata", None)
        if isinstance(metadata, dict):
            event.update(metadata)
        # Never format message, args, exception or stack info from third-party loggers.
        return json.dumps(event, sort_keys=True, separators=(",", ":"))


def logging_config(level: str) -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"safe": {"()": SafeFormatter}},
        "handlers": {"safe": {"class": "logging.StreamHandler", "formatter": "safe"}},
        "root": {"level": level, "handlers": ["safe"]},
        "loggers": {
            name: {"level": level, "handlers": ["safe"], "propagate": False}
            for name in (
                "uvicorn",
                "uvicorn.error",
                "uvicorn.access",
                "brickvault.requests",
                "sqlalchemy.engine",
            )
        },
    }


class RequestBoundary:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_id = str(uuid4())
        scope.setdefault("state", {})["request_id"] = request_id
        started = time.monotonic()
        status = 500
        sent = False
        category = "request"
        native_cors = False
        cors_origin = NATIVE_ORIGIN

        async def safe_send(message: Message) -> None:
            nonlocal sent, status
            if message["type"] == "http.response.start":
                sent = True
                status = message["status"]
                headers = [
                    (key, value)
                    for key, value in message.get("headers", [])
                    if key.lower() not in (b"x-request-id", b"cache-control")
                ]
                policy = b"no-store"
                public_policy = scope.get("state", {}).get("public_static_cache")
                if status == 200 and not scope.get("path", "").startswith("/api") and public_policy:
                    policy = public_policy.encode()
                headers.extend([(b"x-request-id", request_id.encode()), (b"cache-control", policy)])
                if native_cors:
                    headers.extend(
                        [
                            (b"access-control-allow-origin", cors_origin),
                            (b"access-control-allow-credentials", b"true"),
                            (b"access-control-expose-headers", CORS_EXPOSE),
                            (b"vary", b"Origin"),
                        ]
                    )
                message = {**message, "headers": headers}
            await send(message)

        headers = scope.get("headers", [])
        hosts = [value for key, value in headers if key.lower() == b"host"]
        origins = [value for key, value in headers if key.lower() == b"origin"]
        application_state = getattr(scope.get("app"), "state", None)
        runtime = getattr(application_state, "settings", None)
        port = runtime.port if runtime is not None else 8000
        allowed_hosts = {f"{host}:{port}".encode() for host in ("127.0.0.1", "localhost")}
        allowed_origins = {
            f"{scope.get('scheme', 'http')}://{host}:{port_number}".encode()
            for host in ("127.0.0.1", "localhost")
            for port_number in (8000, 5173, 18000, port)
        }
        qualification = bool(runtime is not None and runtime.android_qualification)
        production = bool(runtime is not None and runtime.purpose == "production")
        if qualification:
            # Narrower than browser defaults: never approve a different loopback
            # alias, port or scheme, including preflight and error responses.
            allowed_hosts = {b"localhost:18443"} if scope.get("scheme") == "https" else set()
            allowed_origins = {NATIVE_ORIGIN, b"https://localhost:18443"}
        if production:
            assert runtime is not None and runtime.production_origin is not None
            host = runtime.production_origin.removeprefix("https://")
            allowed_hosts = {host.encode("ascii")}
            cors_origin = f"https://android.{host}".encode("ascii")
            allowed_origins = {runtime.production_origin.encode("ascii"), cors_origin}
        proxy_identity = [value for key, value in headers if key.lower() == b"x-brickvault-proxy"]
        proxy_valid = not production
        if production:
            assert runtime is not None and runtime.proxy_shared_secret is not None
            proxy_valid = len(proxy_identity) == 1 and secrets.compare_digest(
                proxy_identity[0], runtime.proxy_shared_secret.get_secret_value().encode("ascii")
            )
        try:
            if len(hosts) != 1 or hosts[0] not in allowed_hosts:
                category = "host_rejected"
                await error_response(400, request_id)(scope, receive, safe_send)
            elif not proxy_valid:
                category = "proxy_rejected"
                await error_response(403, request_id)(scope, receive, safe_send)
            elif (
                len(origins) > 1
                or (origins and origins[0] not in allowed_origins)
                or (
                    production
                    and scope["method"] in {"POST", "PUT", "PATCH", "DELETE"}
                    and not origins
                )
            ):
                category = "origin_rejected"
                await error_response(403, request_id)(scope, receive, safe_send)
            else:
                if production:
                    scope["state"]["production_proxy_verified"] = True
                native_cors = (qualification and origins == [NATIVE_ORIGIN]) or (
                    production and origins == [cors_origin]
                )
                if native_cors and scope["method"] == "OPTIONS":
                    requested_methods = [
                        v for k, v in headers if k.lower() == b"access-control-request-method"
                    ]
                    requested_headers = [
                        v for k, v in headers if k.lower() == b"access-control-request-headers"
                    ]
                    valid = (
                        scope.get("path", "").startswith("/api/")
                        and len(requested_methods) == 1
                        and requested_methods[0] in CORS_METHODS.split(b", ")
                        and len(requested_headers) <= 1
                        and all(
                            h.strip().lower() in CORS_HEADERS.lower().split(b", ")
                            for value in requested_headers
                            for h in value.split(b",")
                        )
                    )
                    if valid:
                        await Response(
                            status_code=204,
                            headers={
                                "Access-Control-Allow-Methods": CORS_METHODS.decode(),
                                "Access-Control-Allow-Headers": CORS_HEADERS.decode(),
                                "Access-Control-Max-Age": "0",
                            },
                        )(scope, receive, safe_send)
                    else:
                        await error_response(403, request_id)(scope, receive, safe_send)
                else:
                    await self.app(scope, receive, safe_send)
        except Exception:
            category = "internal_error"
            if not sent:
                await error_response(500, request_id)(scope, receive, safe_send)
            else:
                raise RuntimeError("Response interrupted; details redacted.") from None
        finally:
            route = getattr(scope.get("route"), "path", "unmatched")
            logger.info(
                "request",
                extra={
                    "safe_metadata": {
                        "request_id": request_id,
                        "method": scope["method"] if scope["method"] in METHODS else "OTHER",
                        "route": route,
                        "status": status,
                        "duration_ms": round((time.monotonic() - started) * 1000, 3),
                        "category": category,
                    }
                },
            )
