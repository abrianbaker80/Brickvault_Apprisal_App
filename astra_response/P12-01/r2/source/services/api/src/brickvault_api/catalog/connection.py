"""Import-specific connections retain the accepted target and ownership guards."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

import psycopg
from psycopg.rows import dict_row

from brickvault_api.persistence.database import expected_revisions
from brickvault_api.providers.rebrickable.records import SourceError
from brickvault_api.settings import Purpose, Role, reject_pg_environment, validate_target

CatalogConnection = psycopg.Connection[dict[str, Any]]


@contextmanager
def read_transaction(
    database: "CatalogDatabase",
    connection: CatalogConnection | None = None,
    *,
    repeatable: bool = False,
) -> Iterator[CatalogConnection]:
    """Borrow an admission transaction, or own the original read-only boundary."""
    if connection is not None:
        if connection.info.transaction_status != psycopg.pq.TransactionStatus.INTRANS:
            raise ValueError("active_transaction_required")
        yield connection
    else:
        with database.connect() as current, current.transaction():
            current.execute(
                "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY"
                if repeatable
                else "SET TRANSACTION READ ONLY"
            )
            yield current


@dataclass(frozen=True)
class CatalogDatabase:
    url: str = field(repr=False)
    purpose: Purpose
    ownership_marker: str = field(repr=False)
    role: Role = "owner"

    def connect(self) -> CatalogConnection:
        reject_pg_environment()
        target = validate_target(self.url, self.purpose, self.role)
        connection = psycopg.connect(
            host=target.host,
            port=target.port,
            dbname=target.database,
            user=target.username,
            password=target.password,
            row_factory=dict_row,
            autocommit=True,
            connect_timeout=2,
            options=(
                "-c statement_timeout=2000 -c lock_timeout=2000 -c idle_in_transaction_session_timeout=60000"
                if self.role == "runtime"
                else "-c statement_timeout=300000 -c lock_timeout=10000 -c idle_in_transaction_session_timeout=60000"
            ),
            sslmode="disable",
            gssencmode="disable",
            application_name="brickvault-catalog",
        )
        try:
            if self.purpose == "production":
                if target.username is None:
                    raise SourceError("database_ownership")
                owner = (
                    target.username.replace("_runtime", "_owner")
                    if self.role == "runtime"
                    else target.username
                )
            else:
                owner = (
                    "brickvault_dev_owner"
                    if self.purpose == "development"
                    else "brickvault_test_owner"
                )
            record = connection.execute(
                "SELECT shobj_description(oid,'pg_database') AS marker,pg_get_userbyid(datdba) AS owner FROM pg_database WHERE datname=current_database()"
            ).fetchone()
            if not record or record != {"marker": self.ownership_marker, "owner": owner}:
                raise SourceError("database_ownership")
            revision = connection.execute(
                "SELECT version_num FROM public.alembic_version"
            ).fetchall()
            if sorted(row["version_num"] for row in revision) != list(expected_revisions()):
                raise SourceError("migration_required")
            return connection
        except BaseException:
            connection.close()
            raise
