"""A real TEST pg_dump/pg_restore preserves private service state."""

from typing import Any
from uuid import UUID

import pytest
from database import Instance, database_marker
from recovery_runner import RecoveryFixtures

from brickvault_api.application.readiness import Ready, check_readiness
from brickvault_api.auth import AuthService
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.economics_snapshot import encode
from brickvault_api.forecasts import ForecastService
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.watchlist import WatchlistService

from .test_catalog_queries import owner_engine as owner_engine
from .test_catalog_schema import key
from .test_catalog_schema import synthetic as synthetic
from .test_forecasts import ForecastHarness
from .test_forecasts import forecasts as forecasts
from .test_market import market as market
from .test_market import no_provider_network as no_provider_network


@pytest.fixture
def catalog_db(
    owned_instance: Instance, disposable_database: str, integration_run_id: str
) -> CatalogDatabase:
    # Use the already recorded source; the standard catalog fixture creates a third DB.
    return CatalogDatabase(
        owned_instance.target(disposable_database, "owner"),
        "test",
        database_marker(owned_instance, integration_run_id),
    )


def selected_rows(
    database: CatalogDatabase, principal: UUID, item: UUID, forecast: UUID
) -> tuple[Any, ...]:
    with database.connect() as connection:
        return (
            connection.execute("SELECT * FROM auth_principal WHERE id=%s", (principal,)).fetchone(),
            connection.execute("SELECT * FROM watchlist_item WHERE id=%s", (item,)).fetchone(),
            connection.execute("SELECT * FROM deal_forecast WHERE id=%s", (forecast,)).fetchone(),
        )


def test_backup_restore_private_records(
    forecasts: ForecastHarness, recovery_fixture: RecoveryFixtures, no_provider_network: None
) -> None:
    source = forecasts.market.owner.database
    watchlist = WatchlistService(forecasts.market.app.database, snapshot_id=key("snapshot"))
    item = watchlist.add(forecasts.token, forecasts.csrf, "80000-1")
    identifier = UUID(str(item["id"]))
    note = "Check the instructions."
    watchlist.update_note(forecasts.token, forecasts.csrf, identifier, 1, note)
    expected_item = watchlist.update_target(forecasts.token, forecasts.csrf, identifier, 2, "25.00")
    preview = forecasts.preview()
    saved = forecasts.save(preview.status.id)
    original = forecasts.service.load(forecasts.token, saved.id)
    source_rows = selected_rows(source, forecasts.owner, identifier, saved.id)
    if any(row is None for row in source_rows):
        pytest.fail("Source fixture is incomplete")
    expected_payload = encode(original.snapshot)
    if expected_payload != bytes(source_rows[2]["canonical_payload"]):
        pytest.fail("Saved source forecast does not match its immutable payload")

    recovery_fixture.backup_restore()

    selected = recovery_fixture.instance
    destination = recovery_fixture.destination
    restored = CatalogDatabase(
        selected.target(destination, "runtime"),
        "test",
        database_marker(selected, recovery_fixture.run_id),
        "runtime",
    )
    engine = create_database_engine(selected.target(destination, "runtime"), "test")
    try:
        if not isinstance(check_readiness(engine), Ready):
            pytest.fail("Restored migration readiness failed")
    finally:
        engine.dispose()
    with restored.connect() as connection:
        grants = connection.execute(
            "SELECT has_table_privilege(current_user,'public.auth_principal','SELECT') AS auth, "
            "has_table_privilege(current_user,'public.watchlist_item','SELECT') AS watchlist, "
            "has_table_privilege(current_user,'public.deal_forecast','SELECT') AS forecast"
        ).fetchone()
    if grants is None or not all(grants.values()):
        pytest.fail("Restored runtime read privileges are incomplete")

    token, csrf, session = AuthService(restored, clock=forecasts.market.clock).login(
        forecasts.password, None
    )
    if session.principal_id != forecasts.owner:
        pytest.fail("Restored principal identity changed")
    restored_watchlist = WatchlistService(restored, snapshot_id=key("snapshot"))
    items, cursor = restored_watchlist.list(token)
    if cursor is not None or len(items) != 1 or items[0] != expected_item:
        pytest.fail("Restored Watchlist item, target, note, or revision changed")
    if restored_watchlist.get(token, identifier) != expected_item:
        pytest.fail("Restored Watchlist direct read changed")

    restored_forecasts = ForecastService(restored)
    historical = restored_forecasts.load(token, saved.id)
    if (
        historical.status != original.status
        or encode(historical.snapshot) != expected_payload
        or historical.calculation != original.calculation
        or restored_forecasts.status(token, saved.id) != saved
        or restored_forecasts.save(token, csrf, saved.id) != saved
    ):
        pytest.fail("Restored saved forecast content or idempotent replay changed")

    if selected_rows(source, forecasts.owner, identifier, saved.id) != source_rows:
        pytest.fail("Source private records changed during restore")
