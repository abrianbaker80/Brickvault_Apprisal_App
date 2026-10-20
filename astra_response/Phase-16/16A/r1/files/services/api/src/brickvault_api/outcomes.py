"""Owner-scoped append-only actuals; frozen forecasts are never mutated."""

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import Any, cast
from uuid import UUID

import psycopg
from psycopg.types.json import Jsonb

from brickvault_api.auth import AuthError, AuthService, Session, digest
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.economics_snapshot import (
    MalformedSnapshot,
    ReplayMismatch,
    SnapshotIntegrityFailure,
    UnsupportedVersion,
)
from brickvault_api.forecasts import ForecastService
from brickvault_api.outcome_calculation import (
    OutcomeBaseline,
    OutcomeChronologyError,
    calculate_outcome,
)
from brickvault_api.outcome_models import (
    OutcomeAppend,
    OutcomeEntry,
    OutcomeHistoryItem,
    OutcomeResponse,
)


class OutcomeError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class OutcomeService:
    def __init__(self, database: CatalogDatabase) -> None:
        self.database = database

    @staticmethod
    def _clock(c: CatalogConnection) -> datetime:
        row = c.execute("SELECT public.forecast_clock() AS now").fetchone()
        assert row is not None
        return cast(datetime, row["now"])

    def _authorize(self, c: CatalogConnection, token: str | None, csrf: str | None) -> Session:
        session = AuthService(self.database, clock=lambda: self._clock(c)).check_in_transaction(
            c, token, csrf
        )
        if csrf is not None:
            assert token is not None
            c.execute(
                "SELECT set_config('brickvault.outcome_session',%s,true),"
                "set_config('brickvault.outcome_auth_until',%s,true)",
                (
                    digest(token),
                    min(session.idle_expires_at, session.absolute_expires_at).isoformat(),
                ),
            )
        return session

    @contextmanager
    def _transaction(
        self, token: str | None, csrf: str | None = None, *, write: bool = False
    ) -> Iterator[tuple[CatalogConnection, Session]]:
        if write and csrf is None:
            raise AuthError(403)
        try:
            with self.database.connect() as c, c.transaction():
                session = self._authorize(c, token, csrf)
                if write:
                    c.execute(
                        "SELECT pg_advisory_xact_lock(hashtextextended(%s,16))",
                        (str(session.principal_id),),
                    )
                yield c, session
                self._authorize(c, token, csrf)
        except psycopg.errors.CheckViolation as error:
            code = error.diag.message_primary
            if code == "OUTCOME_UNAUTHORIZED":
                raise AuthError() from None
            if code == "OUTCOME_ROOT_INVALID":
                raise OutcomeError("OUTCOME_NOT_FOUND") from None
            if code == "OUTCOME_CONFLICT":
                raise OutcomeError(code) from None
            raise
        except psycopg.errors.UniqueViolation:
            raise OutcomeError("OUTCOME_ID_REUSED") from None
        except (
            psycopg.errors.LockNotAvailable,
            psycopg.errors.DeadlockDetected,
            psycopg.errors.SerializationFailure,
            psycopg.errors.QueryCanceled,
        ):
            raise OutcomeError("OUTCOME_UNAVAILABLE") from None

    @staticmethod
    def _root(c: CatalogConnection, owner: UUID, identifier: UUID) -> dict[str, Any]:
        row = c.execute(
            """SELECT root.* FROM public.deal_forecast f
            JOIN public.deal_forecast root ON root.id=COALESCE(f.root_id,f.id)
              AND root.owner_id=f.owner_id
            WHERE f.id=%s AND f.owner_id=%s AND f.saved_at IS NOT NULL
              AND root.saved_at IS NOT NULL AND root.root_id IS NULL AND root.parent_id IS NULL""",
            (identifier, owner),
        ).fetchone()
        if row is None:
            raise OutcomeError("OUTCOME_NOT_FOUND")
        return row

    @staticmethod
    def _entry(row: dict[str, Any]) -> OutcomeEntry:
        return OutcomeEntry.model_validate({name: row[name] for name in OutcomeEntry.model_fields})

    @staticmethod
    def _baseline(root: dict[str, Any]) -> OutcomeBaseline:
        try:
            snapshot, calculation = ForecastService._verify(root)
        except (
            MalformedSnapshot,
            UnsupportedVersion,
            SnapshotIntegrityFailure,
            ReplayMismatch,
        ) as error:
            reason = {
                MalformedSnapshot: "SNAPSHOT_MALFORMED",
                UnsupportedVersion: "SNAPSHOT_UNSUPPORTED_VERSION",
                SnapshotIntegrityFailure: "SNAPSHOT_INTEGRITY_FAILURE",
                ReplayMismatch: "SNAPSHOT_REPLAY_MISMATCH",
            }[type(error)]
            return OutcomeBaseline(root["id"], root["created_at"], unavailable_reason=reason)
        return OutcomeBaseline(root["id"], root["created_at"], snapshot, calculation)

    def get(
        self, token: str | None, identifier: UUID, *, before_revision: int | None = None
    ) -> OutcomeResponse:
        if before_revision is not None and not 1 <= before_revision <= 2_147_483_647:
            raise ValueError("invalid_before_revision")
        with self._transaction(token) as (c, session):
            owner = session.principal_id
            root = self._root(c, owner, identifier)["id"]
            latest_row = c.execute(
                """SELECT * FROM public.deal_outcome_revision WHERE owner_id=%s AND root_forecast_id=%s
                ORDER BY revision DESC LIMIT 1""",
                (owner, root),
            ).fetchone()
            rows = c.execute(
                """SELECT id,revision,recorded_at,correction_reason,
                actuals->>'purchase_decision' AS purchase_decision,
                actuals->>'sale_status' AS sale_status
                FROM public.deal_outcome_revision WHERE owner_id=%s AND root_forecast_id=%s
                  AND (%s::integer IS NULL OR revision<%s)
                ORDER BY revision DESC LIMIT 21""",
                (owner, root, before_revision, before_revision),
            ).fetchall()
            return OutcomeResponse(
                root_forecast_id=root,
                state="RECORDED" if latest_row else "NOT_RECORDED",
                latest=self._entry(latest_row) if latest_row else None,
                history=tuple(OutcomeHistoryItem.model_validate(row) for row in rows[:20]),
                next_before_revision=rows[19]["revision"] if len(rows) > 20 else None,
            )

    def entry(self, token: str | None, identifier: UUID, entry_id: UUID) -> OutcomeEntry:
        with self._transaction(token) as (c, session):
            root = self._root(c, session.principal_id, identifier)["id"]
            row = c.execute(
                """SELECT * FROM public.deal_outcome_revision
                WHERE id=%s AND owner_id=%s AND root_forecast_id=%s""",
                (entry_id, session.principal_id, root),
            ).fetchone()
            if row is None:
                raise OutcomeError("OUTCOME_NOT_FOUND")
            return self._entry(row)

    def append(
        self, token: str | None, csrf: str | None, identifier: UUID, body: OutcomeAppend
    ) -> OutcomeEntry:
        with self._transaction(token, csrf, write=True) as (c, session):
            owner = session.principal_id
            root = self._root(c, owner, identifier)
            existing = c.execute(
                """SELECT * FROM public.deal_outcome_revision
                WHERE id=%s AND owner_id=%s AND root_forecast_id=%s""",
                (body.id, owner, root["id"]),
            ).fetchone()
            if existing is not None:
                if (
                    existing["revision"] != body.expected_revision + 1
                    or existing["actuals"] != body.actuals.model_dump(mode="json")
                    or existing["correction_reason"] != body.correction_reason
                ):
                    raise OutcomeError("OUTCOME_ID_REUSED")
                return self._entry(existing)
            latest = c.execute(
                """SELECT COALESCE(max(revision),0) AS revision FROM public.deal_outcome_revision
                WHERE owner_id=%s AND root_forecast_id=%s""",
                (owner, root["id"]),
            ).fetchone()
            assert latest is not None
            if latest["revision"] != body.expected_revision:
                raise OutcomeError("OUTCOME_CONFLICT")
            try:
                results = calculate_outcome(body.actuals, self._baseline(root))
            except OutcomeChronologyError:
                raise OutcomeError("OUTCOME_INVALID_CHRONOLOGY") from None
            self._authorize(c, token, csrf)
            row = c.execute(
                """INSERT INTO public.deal_outcome_revision
                (id,owner_id,root_forecast_id,revision,correction_reason,actuals,results)
                VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
                (
                    body.id,
                    owner,
                    root["id"],
                    body.expected_revision + 1,
                    body.correction_reason,
                    Jsonb(body.actuals.model_dump(mode="json")),
                    Jsonb(results.model_dump(mode="json")),
                ),
            ).fetchone()
            assert row is not None
            return self._entry(row)
