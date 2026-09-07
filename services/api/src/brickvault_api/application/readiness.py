from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from brickvault_api.persistence.database import expected_revisions


class Ready(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["ready"] = "ready"
    database: Literal["ok"] = "ok"
    migrations: Literal["current"] = "current"


class DatabaseUnavailable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["not_ready"] = "not_ready"
    database: Literal["unavailable"] = "unavailable"
    migrations: Literal["not_checked"] = "not_checked"


class MigrationUnavailable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["not_ready"] = "not_ready"
    database: Literal["ok"] = "ok"
    migrations: Literal["missing", "mismatch"]


NotReady = DatabaseUnavailable | MigrationUnavailable


def check_readiness(engine: Engine) -> Ready | NotReady:
    expected = expected_revisions()
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            present = connection.scalar(text("SELECT to_regclass('public.alembic_version')"))
            if present is None:
                return MigrationUnavailable(migrations="missing")
            revisions = tuple(
                sorted(connection.scalars(text("SELECT version_num FROM public.alembic_version")))
            )
            if not revisions:
                return MigrationUnavailable(migrations="missing")
            if not expected or revisions != expected:
                return MigrationUnavailable(migrations="mismatch")
    except SQLAlchemyError:
        return DatabaseUnavailable()
    return Ready()
