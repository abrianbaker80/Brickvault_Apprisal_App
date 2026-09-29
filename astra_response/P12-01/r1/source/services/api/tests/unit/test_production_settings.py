import os
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import SecretStr

from brickvault_api.settings import (
    ConfigurationError,
    RuntimeSettings,
    validate_production_origin,
    validate_target,
)

OWNER = "brickvault_app_owner"
RUNTIME = "brickvault_app_runtime"
DATABASE = "brickvault_appraisal"
PASSWORD = "a" * 64
URL = f"postgresql+psycopg://{RUNTIME}:{PASSWORD}@127.0.0.1:55433/{DATABASE}"
PROXY = "b" * 64
ORIGIN = "https://app.example.test"
MARKER = "brickvault-appraisal:" + "1" * 32 + ":" + "2" * 32


def configured(tmp_path: Path, **changes: object) -> RuntimeSettings:
    return RuntimeSettings.model_validate(
        {
            "purpose": "production",
            "port": 8600,
            "database_url": SecretStr(URL),
            "database_ownership_marker": SecretStr(MARKER),
            "static_enabled": True,
            "web_build_dir": str(tmp_path),
            "production_origin": ORIGIN,
            "proxy_shared_secret": SecretStr(PROXY),
            **changes,
        }
    )


def test_explicit_production_settings_and_database_roles(tmp_path: Path) -> None:
    settings = configured(tmp_path)
    assert settings.target().username == RUNTIME
    assert validate_target(URL.replace(RUNTIME, OWNER), "production", "owner").database == DATABASE
    assert validate_production_origin(ORIGIN) == "app.example.test"
    assert "a" * 64 not in repr(settings)
    assert PROXY not in repr(settings)


@pytest.mark.parametrize(
    "change",
    [
        {"production_origin": None},
        {"production_origin": "http://app.example.test"},
        {"production_origin": "https://localhost"},
        {"production_origin": "https://app.example.test:443"},
        {"production_origin": "https://*.example.test"},
        {"proxy_shared_secret": None},
        {"proxy_shared_secret": SecretStr("short")},
        {"database_ownership_marker": None},
        {"database_url": SecretStr(URL.replace(RUNTIME, OWNER))},
        {"database_url": SecretStr(URL.replace("brickvault_appraisal", "brickvault_dev"))},
        {"database_url": SecretStr(URL.replace("brickvault_appraisal", "brickvault_test_shadow"))},
        {"database_url": SecretStr(URL.replace("127.0.0.1", "192.0.2.10"))},
        {"database_url": SecretStr(URL + "?host=remote.invalid")},
        {"static_enabled": False},
        {"web_build_dir": "relative"},
        {"auth_allow_loopback_http": True},
        {"android_qualification": True},
    ],
)
def test_production_refuses_unsafe_values(tmp_path: Path, change: dict[str, object]) -> None:
    with pytest.raises(ConfigurationError) as caught:
        configured(tmp_path, **change).target()
    assert PASSWORD not in str(caught.value) and PROXY not in str(caught.value)


def test_production_requires_explicit_api_port(tmp_path: Path) -> None:
    settings = configured(tmp_path).model_copy(update={"port": 8000})
    assert settings.target().database == DATABASE
    fields = configured(tmp_path).model_dump(exclude={"port"})
    with pytest.raises(ConfigurationError):
        RuntimeSettings.model_validate(fields).target()


def test_environment_requires_each_production_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for key in list(os.environ):
        if key.startswith(("BVA_", "PG")):
            monkeypatch.delenv(key)
    values = {
        "BVA_MODE": "production",
        "BVA_BIND_HOST": "127.0.0.1",
        "BVA_API_PORT": "8600",
        "BVA_RUNTIME_DATABASE_URL": URL,
        "BVA_DATABASE_OWNERSHIP_MARKER": MARKER,
        "BVA_PRODUCTION_ORIGIN": ORIGIN,
        "BVA_PROXY_SHARED_SECRET": PROXY,
        "BVA_STATIC_ENABLED": "true",
        "BVA_WEB_BUILD_DIR": str(tmp_path),
    }
    for key, value in values.items():
        monkeypatch.setenv(key, value)
    assert RuntimeSettings.from_environment().target().database == DATABASE
    for key in values:
        monkeypatch.delenv(key)
        with pytest.raises(ConfigurationError) as caught:
            RuntimeSettings.from_environment()
        assert PASSWORD not in str(caught.value) and PROXY not in str(caught.value)
        monkeypatch.setenv(key, values[key])


def test_local_modes_reject_production_inputs(tmp_path: Path) -> None:
    settings = configured(tmp_path, purpose="test")
    with pytest.raises(ConfigurationError):
        settings.target()


def test_production_provider_credentials_cannot_be_under_git(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    with pytest.raises(ConfigurationError):
        configured(
            tmp_path,
            market_account_scope=UUID("00000000-0000-4000-8000-000000000001"),
            market_credentials_root=str(tmp_path / "secrets"),
        ).target()
