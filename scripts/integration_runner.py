"""Exclusive runner, durable resource ledger, real tests and best-effort owned cleanup."""

import json
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from pathlib import Path
from types import FrameType
from typing import Any
from uuid import uuid4

import httpx
import pytest
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.settings import RuntimeSettings
from database import (
    LOCAL,
    ROOT,
    DatabaseError,
    Instance,
    cleanup_database,
    migrate,
    provision,
    require_free_port,
    write_record,
)
from pydantic import SecretStr
from sqlalchemy import Engine


class IntegrationFixtures:
    def __init__(self, instance: Instance, database: str, run_id: str) -> None:
        self.instance = instance
        self.database = database
        self.run_id = run_id

    @pytest.fixture
    def owned_instance(self) -> Instance:
        return self.instance

    @pytest.fixture
    def disposable_database(self) -> str:
        return self.database

    @pytest.fixture
    def integration_run_id(self) -> str:
        return self.run_id

    @pytest.fixture
    def test_settings(self) -> RuntimeSettings:
        return RuntimeSettings(
            purpose="test",
            database_url=SecretStr(self.instance.target(self.database, "runtime")),
            port=18000,
        )

    @pytest.fixture
    def owner_engine(self) -> Iterator[Engine]:
        engine = create_database_engine(
            self.instance.target(self.database, "owner"), "test", "owner"
        )
        try:
            yield engine
        finally:
            engine.dispose()

    @pytest.fixture
    def runtime_engine(self) -> Iterator[Engine]:
        engine = create_database_engine(
            self.instance.target(self.database, "runtime"), "test"
        )
        try:
            yield engine
        finally:
            engine.dispose()


def smoke_api(
    instance: Instance, database: str, record: dict[str, Any], journal: Path
) -> None:
    require_free_port(18000)
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("BVA_")
    }
    environment.update(
        {
            "BVA_MODE": "test",
            "BVA_API_PORT": "18000",
            "BVA_BIND_HOST": "127.0.0.1",
            "BVA_RUNTIME_DATABASE_URL": instance.target(database, "runtime"),
        }
    )
    log = journal.with_suffix(".api.log")
    with log.open("x", encoding="utf-8") as output:
        process = subprocess.Popen(
            [sys.executable, "-m", "brickvault_api.main"],
            cwd=ROOT,
            env=environment,
            stdout=output,
            stderr=output,
        )
        try:
            record["api_pid"] = process.pid
            record["api_stopped"] = False
            write_record(journal, record)
            deadline = time.monotonic() + 15
            with httpx.Client(
                base_url="http://127.0.0.1:18000", timeout=3, trust_env=False
            ) as client:
                # Startup coordination only; application readiness has no retries.
                while True:
                    if process.poll() is not None:
                        raise DatabaseError(
                            "Owned API process exited during startup; safe log retained."
                        )
                    try:
                        health = client.get("/api/health")
                        break
                    except httpx.ConnectError:
                        if time.monotonic() >= deadline:
                            raise DatabaseError(
                                "Owned API process startup timed out."
                            ) from None
                        threading.Event().wait(0.1)
                assert health.status_code == 200
                assert health.json() == {"service": "brickvault-api", "status": "ok"}
                assert client.get("/api/ready").json() == {
                    "status": "ready",
                    "database": "ok",
                    "migrations": "current",
                }
                assert client.get("/api/openapi.json").json() == json.loads(
                    (ROOT / "packages/contracts/openapi.json").read_text()
                )
                assert (
                    client.get(
                        "/api/health", headers={"Origin": "https://invalid.example"}
                    ).status_code
                    == 403
                )
                assert client.get("/api/missing").status_code == 404
            record["api_smoke"] = "passed"
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            record["api_stopped"] = process.poll() is not None
            write_record(journal, record)
    require_free_port(18000)


def integration(instance: Instance) -> None:
    run_id = uuid4().hex
    database = "brickvault_test_" + uuid4().hex
    journal = LOCAL / "runs" / f"{run_id}.json"
    before = instance.verify(required=False)
    before_resources = instance.inventory()
    running_before = bool(before and before["State"]["Running"])
    record: dict[str, Any] = {
        "run_id": run_id,
        "project": instance.project,
        "instance_owner": instance.owner,
        "running_before": running_before,
        "resources_before": before_resources,
        "recorded_databases": [database],
        "status": "starting",
        "leftovers": [],
    }
    write_record(journal, record)
    previous_handler = signal.getsignal(signal.SIGTERM)

    def interrupted(signum: int, frame: FrameType | None) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    cleanup_failures: list[str] = []
    try:
        instance.up()
        record["resources"] = instance.inventory()
        record["created_resources"] = [
            sorted(set(after) - set(prior))
            for after, prior in zip(record["resources"], before_resources, strict=True)
        ]
        record["status"] = "provisioning"
        write_record(journal, record)
        provision(instance, database, run_id)
        record["created_databases"] = [database]
        write_record(journal, record)
        migrate(instance, database, run_id=run_id)
        provision(instance, database, run_id)
        migrate(instance, database, run_id=run_id)
        record["status"] = "testing"
        write_record(journal, record)
        exit_code = pytest.main(
            [
                "-c",
                str(ROOT / "services/api/pyproject.toml"),
                "--basetemp",
                str(LOCAL / "runs" / f"{run_id}-pytest"),
                str(ROOT / "services/api/tests/integration"),
            ],
            plugins=[IntegrationFixtures(instance, database, run_id)],
        )
        record["pytest_exit"] = int(exit_code)
        if exit_code:
            raise DatabaseError(
                "Real PostgreSQL integration tests failed; see test results and run ledger."
            )
        smoke_api(instance, database, record, journal)
        record["status"] = "passed"
    except BaseException:
        record["status"] = "failed_or_interrupted"
        raise
    finally:
        # Even after an outage or interruption, restore this owned service long enough to clean up.
        try:
            instance.up()
            removed = cleanup_database(instance, database, run_id, [database])
            record["removed_databases"] = [database] if removed else []
        except Exception:
            cleanup_failures.append(database)
        try:
            if not running_before:
                instance.stop()
            record["running_after"] = bool(
                (instance.verify(required=False) or {})
                .get("State", {})
                .get("Running", False)
            )
        except Exception:
            cleanup_failures.append(instance.project)
        record["leftovers"] = cleanup_failures
        write_record(journal, record)
        signal.signal(signal.SIGTERM, previous_handler)
        print(
            json.dumps(
                {
                    "integration_status": record["status"],
                    "ledger": str(journal.relative_to(ROOT)),
                    "leftovers": cleanup_failures,
                    "volumes": "preserved",
                }
            )
        )
    if cleanup_failures:
        raise DatabaseError(
            "Owned cleanup incomplete; consult the run ledger before retrying."
        )
