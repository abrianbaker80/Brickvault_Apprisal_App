"""Actual-outcome append/history on owned TEST PostgreSQL, never live providers."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from typing import Any
from uuid import uuid4

import psycopg
import pytest
from alembic import command
from sqlalchemy.exc import IntegrityError

from brickvault_api.auth import AuthError
from brickvault_api.outcome_models import OutcomeActuals, OutcomeAppend
from brickvault_api.outcomes import OutcomeError, OutcomeService
from brickvault_api.persistence.database import create_database_engine, migration_config
from brickvault_api.persistence.runtime_grants import grant_runtime

from ..unit.test_outcomes import actual
from .test_forecast_api import assert_problem, endpoint, logged_in
from .test_forecasts import ForecastHarness
from .test_forecasts import forecasts as forecasts
from .test_forecasts import market as market
from .test_forecasts import no_provider_network as no_provider_network
from .test_forecasts import owner_engine as owner_engine
from .test_forecasts import synthetic as synthetic
from .test_product import forbid_market_actions


def request(revision: int = 0, **changes: Any) -> OutcomeAppend:
    return OutcomeAppend(
        id=uuid4(),
        expected_revision=revision,
        actuals=actual(**changes),
        correction_reason="Corrected recorded facts" if revision else None,
    )


def test_history_lineage_exact_retry_and_unchanged_forecasts(
    forecasts: ForecastHarness,
    no_provider_network: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = forecasts
    h.market.lookup()
    h.market.fetch()
    root = h.save(h.preview().status.id)
    child = h.save(h.service.preview_revision(h.token, h.csrf, root.id, h.request()).status.id)
    rows = [h.row(x) for x in (root.id, child.id)]
    frozen = [h.service.load(h.token, x).calculation for x in (root.id, child.id)]
    forbid_market_actions(monkeypatch)
    service = OutcomeService(h.market.app.database)
    assert service.get(h.token, child.id).state == "NOT_RECORDED"
    first_request = request()
    first = service.append(h.token, h.csrf, child.id, first_request)
    second = service.append(h.token, h.csrf, root.id, request(1, purchase_price="81"))
    assert (first.revision, second.revision) == (1, 2)
    assert service.append(h.token, h.csrf, root.id, first_request) == first
    assert service.entry(h.token, child.id, first.id) == first
    result = service.get(h.token, root.id)
    assert result.latest == second
    assert [entry.revision for entry in result.history] == [2, 1]
    with pytest.raises(OutcomeError, match="OUTCOME_ID_REUSED"):
        service.append(
            h.token,
            h.csrf,
            root.id,
            first_request.model_copy(update={"actuals": actual(purchase_price="82")}),
        )
    with pytest.raises(OutcomeError, match="OUTCOME_CONFLICT"):
        service.append(h.token, h.csrf, root.id, request())
    assert [h.row(x) for x in (root.id, child.id)] == rows
    assert [h.service.load(h.token, x).calculation for x in (root.id, child.id)] == frozen


def test_concurrent_expected_revision_allows_one_append(forecasts: ForecastHarness) -> None:
    h = forecasts
    root = h.save(h.preview().status.id)
    service = OutcomeService(h.market.app.database)
    barrier = Barrier(2)

    def append() -> str:
        barrier.wait(timeout=10)
        try:
            service.append(h.token, h.csrf, root.id, request())
            return "saved"
        except OutcomeError as error:
            return error.code

    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = pool.submit(append), pool.submit(append)
        assert sorted([a.result(timeout=20), b.result(timeout=20)]) == ["OUTCOME_CONFLICT", "saved"]
    assert len(service.get(h.token, root.id).history) == 1


def test_auth_final_write_guards_root_isolation_and_populated_downgrade(
    forecasts: ForecastHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = forecasts
    root = h.save(h.preview().status.id)
    other = h.save(h.preview().status.id)
    service = OutcomeService(h.market.app.database)
    for csrf in (None, "invalid"):
        with pytest.raises(AuthError):
            service.append(h.token, csrf, root.id, request())
    entry = service.append(h.token, h.csrf, root.id, request())
    with pytest.raises(OutcomeError, match="OUTCOME_NOT_FOUND"):
        service.entry(h.token, other.id, entry.id)
    pending = h.preview().status.id
    with pytest.raises(OutcomeError, match="OUTCOME_NOT_FOUND"):
        service.append(h.token, h.csrf, pending, request())
    with h.market.app.database.connect() as c:
        for statement in (
            "UPDATE deal_outcome_revision SET revision=revision",
            "DELETE FROM deal_outcome_revision",
            "TRUNCATE deal_outcome_revision",
        ):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                c.execute(statement)
        with pytest.raises(psycopg.errors.CheckViolation, match="OUTCOME_UNAUTHORIZED"):
            c.execute(
                "INSERT INTO deal_outcome_revision(id,owner_id,root_forecast_id,revision,actuals,results) "
                "VALUES(gen_random_uuid(),%s,%s,1,'{}','{}')",
                (h.owner, other.id),
            )
    with h.market.owner.database.connect() as c:
        for statement in (
            "UPDATE deal_outcome_revision SET revision=revision",
            "DELETE FROM deal_outcome_revision",
        ):
            with pytest.raises(psycopg.errors.CheckViolation, match="OUTCOME_IMMUTABLE"):
                c.execute(statement)
    engine = create_database_engine(h.market.owner.database.url, "test", "owner")
    try:
        with (
            pytest.raises(IntegrityError, match="outcome_history_prevents_downgrade"),
            engine.begin() as c,
        ):
            config = migration_config()
            config.attributes["connection"] = c
            command.downgrade(config, "0017_listing_images")
    finally:
        engine.dispose()
    original = service._authorize
    count = 0

    def expire(c: Any, token: Any, csrf: Any) -> Any:
        nonlocal count
        count += 1
        if count == 2:
            h.advance(1801)
        return original(c, token, csrf)

    monkeypatch.setattr(service, "_authorize", expire)
    with pytest.raises(AuthError):
        service.append(h.token, h.csrf, root.id, request(1))
    h.login()
    assert service.get(h.token, root.id).latest == entry


def test_empty_migration_roundtrip_retains_saved_forecast_and_grants(
    forecasts: ForecastHarness,
) -> None:
    h = forecasts
    root = h.save(h.preview().status.id)
    before = h.row(root.id)
    with h.market.app.database.connect() as c:
        role = c.execute("SELECT current_user AS role").fetchone()["role"]
    engine = create_database_engine(h.market.owner.database.url, "test", "owner")
    try:
        with engine.begin() as c:
            config = migration_config()
            config.attributes["connection"] = c
            command.downgrade(config, "0017_listing_images")
            command.upgrade(config, "0018_deal_outcome_revisions")
            grant_runtime(c, role)
    finally:
        engine.dispose()
    assert h.row(root.id) == before
    assert OutcomeService(h.market.app.database).get(h.token, root.id).state == "NOT_RECORDED"


def test_http_contracts_history_recovery_and_broken_original(
    forecasts: ForecastHarness,
    no_provider_network: None,
) -> None:
    h = forecasts
    root = h.save(h.preview().status.id)
    root_before = h.row(root.id)
    with logged_in(h) as client:
        path = endpoint(str(root.id)) + "/outcome"
        empty = client.get(path)
        assert empty.status_code == 200 and empty.headers["cache-control"] == "no-store"
        assert empty.json()["state"] == "NOT_RECORDED"
        body = request().model_dump(mode="json")
        saved = client.post(path, json=body)
        assert saved.status_code == 200, saved.text
        assert saved.headers["cache-control"] == "no-store"
        assert client.get(path + "/entries/" + body["id"]).json() == saved.json()
        assert client.post(path, json=body).json() == saved.json()
        assert_problem(
            client.post(path, json=request().model_dump(mode="json")), 409, "OUTCOME_CONFLICT"
        )
        assert client.post(path, json={**body, "results": {}}).status_code == 422
        assert client.get(path + "?before_revision=0").status_code == 422
        assert client.get(path + "?before_revision=1").json()["history"] == []
        assert client.get(path + "?before_revision=1").json()["latest"]["revision"] == 1
        assert h.row(root.id) == root_before
        # A damaged stored snapshot is represented honestly; recording actuals remains possible.
        with h.market.owner.database.connect() as c, c.transaction():
            c.execute("ALTER TABLE deal_forecast DISABLE TRIGGER USER")
            c.execute("UPDATE deal_forecast SET canonical_payload=%s WHERE id=%s", (b"{", root.id))
            c.execute("ALTER TABLE deal_forecast ENABLE TRIGGER USER")
        corrected = client.post(path, json=request(1).model_dump(mode="json"))
        assert corrected.status_code == 200, corrected.text
        assert corrected.json()["results"]["profit"]["amount"] == "82.05"
        assert corrected.json()["results"]["comparison"]["profit"]["state"] == "UNAVAILABLE"
        assert bytes(h.row(root.id)["canonical_payload"]) == b"{"


def test_foreign_saved_root_and_pagination_are_not_leaked(forecasts: ForecastHarness) -> None:
    h = forecasts
    foreign = h.save(h.preview().status.id)
    with h.market.owner.database.connect() as c, c.transaction():
        c.execute("ALTER TABLE deal_forecast DROP CONSTRAINT deal_forecast_owner_id_fkey")
        c.execute("ALTER TABLE deal_forecast DISABLE TRIGGER USER")
        c.execute("UPDATE deal_forecast SET owner_id=%s WHERE id=%s", (uuid4(), foreign.id))
        c.execute("ALTER TABLE deal_forecast ENABLE TRIGGER USER")
    service = OutcomeService(h.market.app.database)
    for identifier in (foreign.id, uuid4()):
        with pytest.raises(OutcomeError, match="OUTCOME_NOT_FOUND"):
            service.get(h.token, identifier)
        with pytest.raises(OutcomeError, match="OUTCOME_NOT_FOUND"):
            service.append(h.token, h.csrf, identifier, request())
    root = h.save(h.preview().status.id)
    for revision in range(21):
        service.append(
            h.token,
            h.csrf,
            root.id,
            OutcomeAppend(
                id=uuid4(),
                expected_revision=revision,
                actuals=OutcomeActuals(purchase_decision="NOT_BOUGHT"),
                correction_reason="Synthetic correction" if revision else None,
            ),
        )
    first = service.get(h.token, root.id)
    assert len(first.history) == 20 and first.next_before_revision == 2
    last = service.get(h.token, root.id, before_revision=first.next_before_revision)
    assert [row.revision for row in last.history] == [1]
    assert last.next_before_revision is None and last.latest.revision == 21
