"""Only allowlisted metadata reaches structured logs, including server diagnostics."""

import json
import logging
import time
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from brickvault_api.api.errors import error_response

logger = logging.getLogger("brickvault.requests")
METHODS = {"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"}


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
                headers.extend(
                    [(b"x-request-id", request_id.encode()), (b"cache-control", b"no-store")]
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
            f"http://{host}:{port_number}".encode()
            for host in ("127.0.0.1", "localhost")
            for port_number in (8000, 5173, 18000)
        }
        try:
            if len(hosts) != 1 or hosts[0] not in allowed_hosts:
                category = "host_rejected"
                await error_response(400, request_id)(scope, receive, safe_send)
            elif len(origins) > 1 or (origins and origins[0] not in allowed_origins):
                category = "origin_rejected"
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
