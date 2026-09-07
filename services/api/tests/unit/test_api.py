import json
import logging
from uuid import UUID

import pytest
from brickvault_api.main import create_app, schema_bytes
from brickvault_api.observability import SafeFormatter
from brickvault_api.settings import RuntimeSettings
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import Engine


def test_health_and_schema_never_connect(
    runtime_settings: RuntimeSettings, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("Liveness or schema queried PostgreSQL")

    monkeypatch.setattr(Engine, "connect", forbidden)
    app = create_app(runtime_settings)
    with TestClient(app, base_url="http://127.0.0.1:8000") as client:
        response = client.get("/api/health")
        assert response.json() == {"service": "brickvault-api", "status": "ok"}
        assert response.headers["cache-control"] == "no-store"
        assert UUID(response.headers["x-request-id"]).version == 4
        schema = client.get("/api/openapi.json")
        assert schema.status_code == 200
        assert schema.content == schema_bytes(app)
        assert set(schema.json()["paths"]) == {"/api/health", "/api/ready", "/api/openapi.json"}
        for route in ("/docs", "/redoc", "/openapi.json", "/api/missing", "/"):
            error = client.get(route)
            assert error.status_code == 404
            assert error.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.parametrize(
    "host,origin,status",
    [
        ("127.0.0.1:8000", None, 200),
        ("localhost:8000", "http://localhost:5173", 200),
        ("127.0.0.1:8000", "http://127.0.0.1:8000", 200),
        ("evil.invalid:8000", None, 400),
        ("127.0.0.1:5432", None, 400),
        ("127.0.0.1:8000.evil.invalid", None, 400),
        ("127.0.0.1:8000", "null", 403),
        ("127.0.0.1:8000", "https://evil.invalid", 403),
        ("127.0.0.1:8000", "http://localhost:9999", 403),
        ("127.0.0.1:8000", "http://127.0.0.1:5173/", 403),
    ],
)
def test_local_request_boundary(
    host: str, origin: str | None, status: int, runtime_settings: RuntimeSettings
) -> None:
    headers = {"host": host}
    if origin is not None:
        headers["origin"] = origin
    with TestClient(create_app(runtime_settings), base_url="http://127.0.0.1:8000") as client:
        response = client.get("/api/health", headers=headers)
        assert response.status_code == status
        assert "access-control-allow-origin" not in response.headers
        assert response.headers["x-request-id"]


def test_duplicate_headers_fail_closed(runtime_settings: RuntimeSettings) -> None:
    with TestClient(create_app(runtime_settings), base_url="http://127.0.0.1:8000") as client:
        assert (
            client.get(
                "/api/health", headers=[("host", "127.0.0.1:8000"), ("host", "evil.invalid")]
            ).status_code
            == 400
        )
        assert (
            client.get(
                "/api/health",
                headers=[("origin", "http://localhost:5173"), ("origin", "http://localhost:8000")],
            ).status_code
            == 403
        )


def test_json_errors_ids_and_safe_logging(
    runtime_settings: RuntimeSettings, caplog: pytest.LogCaptureFixture
) -> None:
    app = create_app(runtime_settings)

    @app.get("/api/test-only/error/{code}")
    def error(code: int) -> None:
        if code == 500:
            raise RuntimeError("secret-sentinel postgresql://private")
        raise HTTPException(code, detail="secret-sentinel")

    caplog.set_level(logging.INFO, logger="brickvault.requests")
    with TestClient(app, base_url="http://127.0.0.1:8000") as client:
        ids = set()
        for code in (400, 403, 404, 405, 422, 500):
            response = client.get(
                f"/api/test-only/error/{code}?secret-sentinel=value",
                headers={"X-Request-ID": "secret-sentinel", "Authorization": "secret-sentinel"},
            )
            assert response.status_code == code
            request_id = response.headers["x-request-id"]
            assert response.json()["error"]["request_id"] == request_id
            ids.add(request_id)
            assert "secret-sentinel" not in response.text
        assert len(ids) == 6
        assert client.get("/api/test-only/error/secret-sentinel").status_code == 422
        assert client.post("/api/health", content="secret-sentinel").status_code == 405
        client.get("/api/secret-sentinel?secret-sentinel=value")
    records = [record for record in caplog.records if record.name == "brickvault.requests"]
    serialized = "\n".join(SafeFormatter().format(record) for record in records)
    assert "secret-sentinel" not in serialized
    assert "postgresql" not in serialized
    assert ids.issubset(
        {json.loads(SafeFormatter().format(record))["request_id"] for record in records}
    )
    assert json.loads(SafeFormatter().format(records[-1]))["route"] == "unmatched"
    third_party = logging.LogRecord(
        "uvicorn.error", logging.ERROR, "", 0, "secret-sentinel", (), None
    )
    assert "secret-sentinel" not in SafeFormatter().format(third_party)


def test_engine_disposed_at_lifecycle_end(
    runtime_settings: RuntimeSettings, monkeypatch: pytest.MonkeyPatch
) -> None:
    disposed = []
    original = Engine.dispose

    def dispose(engine: Engine, close: bool = True) -> None:
        disposed.append(engine)
        original(engine, close=close)

    monkeypatch.setattr(Engine, "dispose", dispose)
    with TestClient(create_app(runtime_settings), base_url="http://127.0.0.1:8000"):
        assert not disposed
    assert len(disposed) == 1
