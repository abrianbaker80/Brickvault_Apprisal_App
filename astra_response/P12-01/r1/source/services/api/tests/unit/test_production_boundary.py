from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from brickvault_api.main import create_app
from brickvault_api.settings import RuntimeSettings

ORIGIN = "https://app.example.test"
NATIVE = "https://android.app.example.test"
PROXY = "b" * 64
MARKER = "brickvault-appraisal:" + "1" * 32 + ":" + "2" * 32


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    settings = RuntimeSettings(
        purpose="production",
        port=8600,
        database_url=SecretStr(
            "postgresql+psycopg://brickvault_app_runtime:"
            + "a" * 64
            + "@127.0.0.1:55433/brickvault_appraisal"
        ),
        database_ownership_marker=SecretStr(MARKER),
        production_origin=ORIGIN,
        proxy_shared_secret=SecretStr(PROXY),
        static_enabled=True,
        web_build_dir=str(tmp_path),
    )
    settings.target()
    app = create_app(settings)
    app.state.settings = settings
    return TestClient(app, base_url=ORIGIN)


def test_exact_host_origin_and_proxy_identity(client: TestClient) -> None:
    approved = {"X-BrickVault-Proxy": PROXY}
    assert client.get("/api/health", headers=approved).status_code == 200
    assert client.get("/api/health").status_code == 403
    assert (
        client.get("/api/health", headers={**approved, "Host": "evil.example.test"}).status_code
        == 400
    )
    assert (
        client.get(
            "/api/health", headers={**approved, "Origin": "https://evil.example.test"}
        ).status_code
        == 403
    )
    assert client.get("/api/health", headers={**approved, "Origin": ORIGIN}).status_code == 200
    assert client.post("/api/missing", headers=approved).status_code == 403
    assert client.post("/api/missing", headers={**approved, "Origin": ORIGIN}).status_code == 404
    for header in ("X-Forwarded-Host", "X-Forwarded-Proto", "Forwarded"):
        assert client.get("/api/health", headers={header: ORIGIN}).status_code == 403
    assert (
        client.get(
            "/api/health", headers=[("X-BrickVault-Proxy", PROXY), ("X-BrickVault-Proxy", PROXY)]
        ).status_code
        == 403
    )


def test_exact_native_cors_only_after_proxy_identity(client: TestClient) -> None:
    headers = {
        "Host": "app.example.test",
        "Origin": NATIVE,
        "X-BrickVault-Proxy": PROXY,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,x-csrf-token",
    }
    response = client.options("/api/auth/login", headers=headers)
    assert response.status_code == 204
    assert response.headers["access-control-allow-origin"] == NATIVE
    assert response.headers["access-control-allow-credentials"] == "true"
    assert response.headers["cache-control"] == "no-store"
    for changed in (
        {"Origin": "https://localhost"},
        {"Host": "android.app.example.test"},
        {"X-BrickVault-Proxy": "invalid"},
    ):
        response = client.options("/api/auth/login", headers={**headers, **changed})
        assert response.status_code in (400, 403)
        assert "access-control-allow-origin" not in response.headers
