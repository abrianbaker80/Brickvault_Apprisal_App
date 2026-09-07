import json

import pytest
from brickvault_api.main import create_app
from brickvault_api.settings import RuntimeSettings
from database import LOCAL, DatabaseError, Instance, cleanup_database, migrate
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text


def test_disposable_downgrade_upgrade(
    owned_instance: Instance,
    disposable_database: str,
    integration_run_id: str,
    test_settings: RuntimeSettings,
) -> None:
    try:
        migrate(owned_instance, disposable_database, downgrade=True, run_id=integration_run_id)
        with TestClient(create_app(test_settings), base_url="http://127.0.0.1:18000") as client:
            response = client.get("/api/ready")
            assert response.status_code == 503
            assert response.json() == {
                "status": "not_ready",
                "database": "ok",
                "migrations": "missing",
            }
    finally:
        migrate(owned_instance, disposable_database, run_id=integration_run_id)


@pytest.mark.parametrize(
    "revisions",
    [[], ["0000_outdated"], ["unknown_revision"], ["0001_foundation", "additional_revision"]],
)
def test_exact_revision_readiness(
    revisions: list[str], owner_engine: Engine, test_settings: RuntimeSettings
) -> None:
    try:
        with owner_engine.begin() as connection:
            connection.execute(text("DELETE FROM public.alembic_version"))
            for revision in revisions:
                connection.execute(
                    text("INSERT INTO public.alembic_version (version_num) VALUES (:revision)"),
                    {"revision": revision},
                )
        with TestClient(create_app(test_settings), base_url="http://127.0.0.1:18000") as client:
            response = client.get("/api/ready")
            assert response.status_code == 503
            assert response.json() == {
                "status": "not_ready",
                "database": "ok",
                "migrations": "missing" if not revisions else "mismatch",
            }
            assert response.headers["cache-control"] == "no-store"
    finally:
        with owner_engine.begin() as connection:
            connection.execute(text("DELETE FROM public.alembic_version"))
            connection.execute(
                text("INSERT INTO public.alembic_version VALUES ('0001_foundation')")
            )


def test_absent_revision_table(owner_engine: Engine, test_settings: RuntimeSettings) -> None:
    try:
        with owner_engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE public.alembic_version RENAME TO revision_test_saved")
            )
        with TestClient(create_app(test_settings), base_url="http://127.0.0.1:18000") as client:
            response = client.get("/api/ready")
            assert response.status_code == 503
            assert response.json()["migrations"] == "missing"
    finally:
        with owner_engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE public.revision_test_saved RENAME TO alembic_version")
            )


def test_real_owned_service_outage_and_recovery(
    owned_instance: Instance, test_settings: RuntimeSettings
) -> None:
    with TestClient(create_app(test_settings), base_url="http://127.0.0.1:18000") as client:
        assert client.get("/api/ready").status_code == 200
        try:
            owned_instance.stop()
            response = client.get("/api/ready")
            assert response.status_code == 503
            assert response.json() == {
                "status": "not_ready",
                "database": "unavailable",
                "migrations": "not_checked",
            }
            assert client.get("/api/health").status_code == 200
        finally:
            owned_instance.up()
        assert client.get("/api/ready").status_code == 200


def test_cleanup_cannot_remove_database_owned_by_another_run(
    owned_instance: Instance, disposable_database: str, owner_engine: Engine
) -> None:
    with pytest.raises(DatabaseError, match="ownership"):
        cleanup_database(owned_instance, disposable_database, "another-run", [disposable_database])
    with owner_engine.connect() as connection:
        assert (
            connection.scalar(text("SELECT version_num FROM public.alembic_version"))
            == "0001_foundation"
        )


@pytest.mark.parametrize("interrupt", [False, True])
def test_runner_cleans_actual_database_after_failed_or_interrupted_tests(
    owned_instance: Instance, monkeypatch: pytest.MonkeyPatch, interrupt: bool
) -> None:
    from integration_runner import integration

    before = set((LOCAL / "runs").glob("*.json"))

    def failed(*args: object, **kwargs: object) -> int:
        if interrupt:
            raise KeyboardInterrupt
        return 1

    monkeypatch.setattr(pytest, "main", failed)
    with pytest.raises(KeyboardInterrupt if interrupt else DatabaseError):
        integration(owned_instance)
    added = set((LOCAL / "runs").glob("*.json")) - before
    assert len(added) == 1
    ledger = json.loads(added.pop().read_text())
    assert ledger["status"] == "failed_or_interrupted"
    assert ledger["created_databases"] == ledger["removed_databases"]
    assert ledger["leftovers"] == []
    assert ledger["running_before"] is ledger["running_after"] is True
    with owned_instance.bootstrap() as maintenance:
        assert (
            maintenance.execute(
                "SELECT 1 FROM pg_database WHERE datname=%s", (ledger["created_databases"][0],)
            ).fetchone()
            is None
        )
