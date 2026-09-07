"""Strict local configuration. No credential loading or connections at import time."""

import os
import re
from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, ConfigDict, SecretStr
from sqlalchemy.engine import URL, make_url

Purpose = Literal["development", "test"]
Role = Literal["owner", "runtime"]
TEST_DATABASE = re.compile(r"brickvault_test_[0-9a-f]{32}\Z")


class ConfigurationError(ValueError):
    """Messages contain only safe categories, never configuration values."""


def reject_pg_environment(environment: Mapping[str, str] | None = None) -> None:
    if any(
        key.upper().startswith("PG") for key in (os.environ if environment is None else environment)
    ):
        raise ConfigurationError("Inherited PostgreSQL settings are not supported.")


def validate_target(
    value: str, purpose: Purpose, role: Role, *, config_template: bool = False
) -> URL:
    """Require canonical bytes before URL parsing, which can silently normalize input."""
    reject_pg_environment()
    if purpose not in ("development", "test") or role not in ("owner", "runtime"):
        raise ConfigurationError("Unsupported database purpose or role.")
    prefix, port = ("dev", 55432) if purpose == "development" else ("test", 55433)
    database = "brickvault_dev" if purpose == "development" else r"brickvault_test_[0-9a-f]{32}"
    if purpose == "test" and config_template:
        database = "brickvault_test"
    pattern = (
        rf"postgresql\+psycopg://brickvault_{prefix}_{role}:[a-f0-9]{{64}}"
        rf"@127\.0\.0\.1:{port}/{database}"
    )
    if re.fullmatch(pattern, value) is None:
        raise ConfigurationError(
            "Invalid database target: expected the approved local purpose and role."
        )
    return make_url(value)


class RuntimeSettings(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid", hide_input_in_errors=True)

    purpose: Purpose
    database_url: SecretStr
    port: Literal[8000, 18000] = 8000
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    def target(self) -> URL:
        if (self.purpose == "development" and self.port != 8000) or (
            self.purpose == "test" and self.port != 18000
        ):
            raise ConfigurationError("API port does not match the local purpose.")
        return validate_target(self.database_url.get_secret_value(), self.purpose, "runtime")

    @classmethod
    def from_environment(cls) -> "RuntimeSettings":
        allowed = {
            "BVA_MODE",
            "BVA_RUNTIME_DATABASE_URL",
            "BVA_API_PORT",
            "BVA_LOG_LEVEL",
            "BVA_BIND_HOST",
        }
        try:
            if any(key.startswith("BVA_") and key not in allowed for key in os.environ):
                raise ConfigurationError("Unexpected runtime setting.")
            if os.environ.get("BVA_BIND_HOST", "127.0.0.1") != "127.0.0.1":
                raise ConfigurationError("API must bind to loopback.")
            port = os.environ.get("BVA_API_PORT", "8000")
            if port not in ("8000", "18000"):
                raise ConfigurationError("Unsupported API port.")
            result = cls.model_validate(
                {
                    "purpose": os.environ.get("BVA_MODE", "development"),
                    "database_url": SecretStr(os.environ.get("BVA_RUNTIME_DATABASE_URL", "")),
                    "port": int(port),
                    "log_level": os.environ.get("BVA_LOG_LEVEL", "INFO"),
                }
            )
            result.target()
            return result
        except (ValueError, TypeError):
            raise ConfigurationError(
                "Invalid local runtime configuration; values redacted."
            ) from None
