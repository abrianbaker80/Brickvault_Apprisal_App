"""Strict runtime configuration. No credential loading or connections at import time."""

import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, SecretStr
from sqlalchemy.engine import URL, make_url

Purpose = Literal["development", "test", "production"]
Role = Literal["owner", "runtime"]
TEST_DATABASE = re.compile(r"brickvault_test_[0-9a-f]{32}\Z")
PRODUCTION_TARGET = re.compile(
    r"postgresql\+psycopg://brickvault_(?P<stem>[a-z][a-z0-9_]{0,30})_"
    r"(?P<role>owner|runtime):[a-f0-9]{64}@127\.0\.0\.1:"
    r"(?P<port>[1-9][0-9]{0,4})/(?P<database>brickvault_[a-z][a-z0-9_]{0,50})\Z"
)
PRODUCTION_ORIGIN = re.compile(
    r"https://(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"[a-z](?:[a-z0-9-]*[a-z0-9])?\Z"
)


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
    if purpose not in ("development", "test", "production") or role not in (
        "owner",
        "runtime",
    ):
        raise ConfigurationError("Unsupported database purpose or role.")
    if purpose == "production":
        match = PRODUCTION_TARGET.fullmatch(value)
        if (
            config_template
            or match is None
            or match.group("role") != role
            or match.group("stem").startswith(("dev", "test"))
            or match.group("database").startswith(("brickvault_dev", "brickvault_test"))
            or int(match.group("port")) > 65535
        ):
            raise ConfigurationError("Invalid dedicated loopback production database target.")
        return make_url(value)
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


def validate_production_origin(value: str) -> str:
    """Require one canonical DNS HTTPS origin, without path, port or normalization."""
    if PRODUCTION_ORIGIN.fullmatch(value) is None or value.endswith(".localhost"):
        raise ConfigurationError("Invalid production HTTPS application origin.")
    return value.removeprefix("https://")


def production_credentials_root_is_safe(value: str) -> bool:
    """Keep provider credential files outside Git checkouts."""
    root = Path(value)
    return root.is_absolute() and not any(
        (directory / ".git").exists() for directory in (root, *root.parents)
    )


class RuntimeSettings(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid", hide_input_in_errors=True)

    purpose: Purpose
    database_url: SecretStr
    database_ownership_marker: SecretStr | None = None
    # Owned TEST helpers may inject a reserved OS-assigned port. Environment-based
    # startup below retains the existing fixed-port configuration contract.
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    static_enabled: bool = False
    web_build_dir: str | None = None
    market_account_scope: UUID | None = None
    market_credentials_root: str | None = None
    auth_allow_loopback_http: bool = False
    android_qualification: bool = False
    production_origin: str | None = None
    proxy_shared_secret: SecretStr | None = None

    def target(self) -> URL:
        if self.purpose == "production":
            if (
                "port" not in self.model_fields_set
                or self.production_origin is None
                or self.proxy_shared_secret is None
                or re.fullmatch(r"[a-f0-9]{64}", self.proxy_shared_secret.get_secret_value())
                is None
                or self.database_ownership_marker is None
                or re.fullmatch(
                    r"brickvault-appraisal:[a-f0-9]{32}:[a-f0-9]{32}",
                    self.database_ownership_marker.get_secret_value(),
                )
                is None
                or not self.static_enabled
                or self.web_build_dir is None
                or not Path(self.web_build_dir).is_absolute()
                or self.auth_allow_loopback_http
                or self.android_qualification
                or (self.market_account_scope is None) != (self.market_credentials_root is None)
                or (
                    self.market_credentials_root is not None
                    and not production_credentials_root_is_safe(self.market_credentials_root)
                )
            ):
                raise ConfigurationError("Incomplete or unsafe production runtime settings.")
            validate_production_origin(self.production_origin)
            return validate_target(self.database_url.get_secret_value(), self.purpose, "runtime")
        if self.production_origin is not None or self.proxy_shared_secret is not None:
            raise ConfigurationError("Production settings are forbidden in local modes.")
        if self.android_qualification and (
            self.purpose != "test"
            or self.port != 18443
            or self.auth_allow_loopback_http
            or self.market_account_scope is not None
            or self.market_credentials_root is not None
            or self.database_ownership_marker is None
        ):
            raise ConfigurationError("Android qualification requires owned HTTPS TEST settings.")
        if self.purpose == "development" and self.port != 8000:
            raise ConfigurationError("API port does not match the local purpose.")
        return validate_target(self.database_url.get_secret_value(), self.purpose, "runtime")

    @classmethod
    def from_environment(cls) -> "RuntimeSettings":
        allowed = {
            "BVA_MODE",
            "BVA_RUNTIME_DATABASE_URL",
            "BVA_DATABASE_OWNERSHIP_MARKER",
            "BVA_API_PORT",
            "BVA_LOG_LEVEL",
            "BVA_BIND_HOST",
            "BVA_STATIC_ENABLED",
            "BVA_WEB_BUILD_DIR",
            "BVA_MARKET_ACCOUNT_SCOPE",
            "BVA_MARKET_CREDENTIALS_ROOT",
            "BVA_AUTH_ALLOW_LOOPBACK_HTTP",
            "BVA_PRODUCTION_ORIGIN",
            "BVA_PROXY_SHARED_SECRET",
        }
        try:
            if any(key.startswith("BVA_") and key not in allowed for key in os.environ):
                raise ConfigurationError("Unexpected runtime setting.")
            production = os.environ.get("BVA_MODE") == "production"
            if production and any(
                key not in os.environ
                for key in (
                    "BVA_BIND_HOST",
                    "BVA_API_PORT",
                    "BVA_RUNTIME_DATABASE_URL",
                    "BVA_DATABASE_OWNERSHIP_MARKER",
                    "BVA_PRODUCTION_ORIGIN",
                    "BVA_PROXY_SHARED_SECRET",
                    "BVA_STATIC_ENABLED",
                    "BVA_WEB_BUILD_DIR",
                )
            ):
                raise ConfigurationError("Missing required production runtime setting.")
            if os.environ.get("BVA_BIND_HOST", "127.0.0.1") != "127.0.0.1":
                raise ConfigurationError("API must bind to loopback.")
            port = os.environ.get("BVA_API_PORT", "8000")
            if (
                re.fullmatch(r"[1-9][0-9]{0,4}", port) is None
                or int(port) > 65535
                or (not production and port not in ("8000", "18000"))
            ):
                raise ConfigurationError("Unsupported API port.")
            enabled = os.environ.get("BVA_STATIC_ENABLED", "false")
            auth_http = os.environ.get("BVA_AUTH_ALLOW_LOOPBACK_HTTP", "false")
            if auth_http not in ("true", "false"):
                raise ConfigurationError("Invalid authentication transport setting.")
            if enabled not in ("true", "false"):
                raise ConfigurationError("Invalid static-serving flag.")
            result = cls.model_validate(
                {
                    "purpose": os.environ.get("BVA_MODE", "development"),
                    "database_url": SecretStr(os.environ.get("BVA_RUNTIME_DATABASE_URL", "")),
                    "database_ownership_marker": SecretStr(
                        os.environ["BVA_DATABASE_OWNERSHIP_MARKER"]
                    )
                    if "BVA_DATABASE_OWNERSHIP_MARKER" in os.environ
                    else None,
                    "port": int(port),
                    "log_level": os.environ.get("BVA_LOG_LEVEL", "INFO"),
                    "static_enabled": enabled == "true",
                    "web_build_dir": os.environ.get("BVA_WEB_BUILD_DIR"),
                    "market_account_scope": UUID(os.environ["BVA_MARKET_ACCOUNT_SCOPE"])
                    if os.environ.get("BVA_MARKET_ACCOUNT_SCOPE")
                    else None,
                    "market_credentials_root": os.environ.get("BVA_MARKET_CREDENTIALS_ROOT"),
                    "auth_allow_loopback_http": auth_http == "true",
                    "production_origin": os.environ.get("BVA_PRODUCTION_ORIGIN"),
                    "proxy_shared_secret": SecretStr(os.environ["BVA_PROXY_SHARED_SECRET"])
                    if "BVA_PROXY_SHARED_SECRET" in os.environ
                    else None,
                }
            )
            if result.purpose == "test" and result.port != 18000:
                raise ConfigurationError("API port does not match the local purpose.")
            result.target()
            return result
        except (ValueError, TypeError):
            raise ConfigurationError(
                "Invalid local runtime configuration; values redacted."
            ) from None
