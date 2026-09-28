"""One guarded TEST-only PostgreSQL backup and restore rehearsal."""

import json
import re
import signal
import subprocess
import sys
from pathlib import Path
from types import FrameType
from typing import Any
from uuid import uuid4

import pytest
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.settings import TEST_DATABASE, ConfigurationError
from database import (
    LOCAL,
    ROOT,
    DatabaseError,
    Instance,
    cleanup_database,
    database_marker,
    instance,
    migrate,
    private_path,
    provision,
    runner_lock,
    write_record,
)
from integration_runner import IntegrationFixtures
from sqlalchemy import text


def validate_selection(
    selected: Instance,
    run_id: str,
    source: str,
    destination: str,
    record: dict[str, Any],
) -> None:
    """Refuse any database or run other than the two recorded TEST resources."""
    if (
        selected.purpose != "test"
        or re.fullmatch(r"[a-f0-9]{32}", run_id) is None
        or TEST_DATABASE.fullmatch(source) is None
        or TEST_DATABASE.fullmatch(destination) is None
        or source == destination
        or record.get("run_id") != run_id
        or record.get("project") != selected.project
        or record.get("instance_owner") != selected.owner
        or record.get("recorded_databases") != [source, destination]
    ):
        raise DatabaseError(
            "Recovery requires two distinct, exact run-recorded TEST databases."
        )


def verify_databases(
    selected: Instance,
    run_id: str,
    source: str,
    destination: str,
    record: dict[str, Any],
) -> str:
    validate_selection(selected, run_id, source, destination, record)
    container = selected.verify()
    assert container is not None
    with selected.bootstrap() as connection:
        rows = connection.execute(
            "SELECT datname, shobj_description(oid, 'pg_database'), pg_get_userbyid(datdba) "
            "FROM pg_database WHERE datname IN (%s,%s)",
            (source, destination),
        ).fetchall()
    expected = {
        (name, database_marker(selected, run_id), "brickvault_test_owner")
        for name in (source, destination)
    }
    if set(rows) != expected:
        raise DatabaseError("Recovery database ownership or identity check failed.")
    return str(container["Id"])


def require_empty_destination(selected: Instance, destination: str) -> None:
    engine = create_database_engine(
        selected.target(destination, "owner"), "test", "owner"
    )
    try:
        with engine.connect() as connection:
            # A freshly provisioned target has no application relations. Never overlay a populated DB.
            count = connection.scalar(
                text(
                    "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                    "WHERE n.nspname='public' AND c.relkind IN ('r','p','v','m','S','f')"
                )
            )
    finally:
        engine.dispose()
    if count != 0:
        raise DatabaseError("Restore destination is not an empty owned database.")


def dump_path(run_id: str) -> Path:
    if re.fullmatch(r"[a-f0-9]{32}", run_id) is None:
        raise DatabaseError("Invalid recovery run identity.")
    path = LOCAL / "backups" / f"{run_id}.dump"
    private_path(path)
    return path


def _run_tool(args: list[str], payload: bytes, *, stdout: Any) -> int | None:
    try:
        result = subprocess.run(
            args,
            cwd=ROOT,
            input=payload,
            stdout=stdout,
            stderr=subprocess.DEVNULL,
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.returncode


def _pg_tool(selected: Instance, container: str, utility: str, *args: str) -> list[str]:
    # Supply the bootstrap password over stdin inside the verified local container.
    # The fixed shell reads one line, then execs the utility with remaining stdin intact.
    return [
        "docker",
        "--context",
        selected.context,
        "exec",
        "-i",
        container,
        "sh",
        "-c",
        'IFS= read -r PGPASSWORD; export PGPASSWORD; exec "$@"',
        "brickvault-recovery",
        utility,
        *args,
    ]


def backup_restore(
    selected: Instance,
    run_id: str,
    source: str,
    destination: str,
    record: dict[str, Any],
) -> None:
    container = verify_databases(selected, run_id, source, destination, record)
    require_empty_destination(selected, destination)
    path = dump_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    # The only output path is a new, ignored, run-owned file. No shell or provider network.
    password_line = (
        selected.config["BVA_TEST_BOOTSTRAP_PASSWORD"].encode("ascii") + b"\n"
    )
    with path.open("xb") as stream:
        result = _run_tool(
            _pg_tool(
                selected,
                container,
                "pg_dump",
                "--format=custom",
                "--username=brickvault_bootstrap",
                f"--dbname={source}",
            ),
            password_line,
            stdout=stream,
        )
    if result != 0:
        raise DatabaseError("Local pg_dump failed or timed out; output redacted.")
    if not 0 < path.stat().st_size <= 32 * 1024 * 1024:
        raise DatabaseError("TEST backup is empty or exceeds the bounded fixture size.")
    record["dump_created"] = True
    record["status"] = "backed_up"
    write_record(LOCAL / "runs" / f"{run_id}.json", record)
    container = verify_databases(selected, run_id, source, destination, record)
    require_empty_destination(selected, destination)
    result = _run_tool(
        _pg_tool(
            selected,
            container,
            "pg_restore",
            "--exit-on-error",
            "--single-transaction",
            "--no-owner",
            "--no-privileges",
            "--role=brickvault_test_owner",
            "--username=brickvault_bootstrap",
            f"--dbname={destination}",
        ),
        password_line + path.read_bytes(),
        stdout=subprocess.DEVNULL,
    )
    if result != 0:
        raise DatabaseError("Local pg_restore failed or timed out; output redacted.")
    record["status"] = "restored"
    write_record(LOCAL / "runs" / f"{run_id}.json", record)
    # Reapply the existing, enumerated runtime grants and check the migration head.
    migrate(selected, destination, run_id=run_id)


class RecoveryFixtures(IntegrationFixtures):
    def __init__(
        self,
        selected: Instance,
        source: str,
        destination: str,
        run_id: str,
        record: dict[str, Any],
    ) -> None:
        super().__init__(selected, source, run_id)
        self.destination = destination
        self.record = record

    @pytest.fixture
    def recovery_fixture(self) -> "RecoveryFixtures":
        return self

    def backup_restore(self) -> None:
        backup_restore(
            self.instance, self.run_id, self.database, self.destination, self.record
        )


def rehearsal(selected: Instance) -> None:
    if selected.purpose != "test":
        raise DatabaseError("Recovery rehearsal requires the owned TEST instance.")
    run_id = uuid4().hex
    source, destination = ("brickvault_test_" + uuid4().hex for _ in range(2))
    journal = LOCAL / "runs" / f"{run_id}.json"
    before = selected.verify(required=False)
    before_resources = selected.inventory()
    if before is None:
        raise DatabaseError(
            "Existing owned TEST container required; preserve initial infrastructure."
        )
    running_before = bool(before["State"]["Running"])
    record: dict[str, Any] = {
        "run_id": run_id,
        "kind": "P10-02-backup-restore",
        "project": selected.project,
        "instance_owner": selected.owner,
        "recorded_databases": [source, destination],
        "running_before": running_before,
        "resources_before": before_resources,
        "status": "starting",
        "removed_databases": [],
        "leftovers": [],
    }
    validate_selection(selected, run_id, source, destination, record)
    write_record(journal, record)
    previous_handler = signal.getsignal(signal.SIGTERM)

    def interrupted(signum: int, frame: FrameType | None) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    cleanup_failures: list[str] = []
    try:
        selected.up()
        if selected.inventory() != before_resources:
            raise DatabaseError("Owned TEST resource inventory changed unexpectedly.")
        with selected.bootstrap() as connection:
            existing = connection.execute(
                "SELECT datname FROM pg_database WHERE datname IN (%s,%s)",
                (source, destination),
            ).fetchall()
        if existing:
            raise DatabaseError("Recovery target name already exists; preserving it.")
        record["status"] = "provisioning"
        write_record(journal, record)
        provision(selected, source, run_id)
        migrate(selected, source, run_id=run_id)
        provision(selected, destination, run_id)
        verify_databases(selected, run_id, source, destination, record)
        require_empty_destination(selected, destination)
        record["status"] = "testing"
        write_record(journal, record)
        exit_code = pytest.main(
            [
                "-c",
                str(ROOT / "services/api/pyproject.toml"),
                "--basetemp",
                str(LOCAL / "runs" / f"{run_id}-pytest"),
                "--tb=line",
                str(ROOT / "services/api/tests/integration/recovery_proof.py"),
            ],
            plugins=[RecoveryFixtures(selected, source, destination, run_id, record)],
        )
        record["pytest_exit"] = int(exit_code)
        if exit_code:
            raise DatabaseError(
                "Recovery proof failed; see focused test result and run ledger."
            )
        record["status"] = "passed"
    except BaseException:
        record["status"] = "failed_or_interrupted"
        raise
    finally:
        path = dump_path(run_id)
        try:
            if path.exists():
                path.unlink()
            record["dump_removed"] = not path.exists()
        except OSError:
            cleanup_failures.append("dump")
        try:
            selected.up()
            for name in (source, destination):
                try:
                    if cleanup_database(
                        selected, name, run_id, record["recorded_databases"]
                    ):
                        record["removed_databases"].append(name)
                except Exception:  # noqa: BLE001 -- continue with the other exact owned DB
                    cleanup_failures.append(name)
        except Exception:  # noqa: BLE001 -- attempt remaining owned cleanup
            cleanup_failures.append("databases")
        try:
            if not running_before:
                selected.stop()
            final_container = selected.verify()
            if final_container is None:
                raise DatabaseError("Owned TEST container disappeared during cleanup.")
            record["running_after"] = bool(final_container["State"]["Running"])
            if selected.inventory() != before_resources:
                cleanup_failures.append("resources")
        except Exception:  # noqa: BLE001 -- preserve ledger after cleanup failure
            cleanup_failures.append("service")
        record["leftovers"] = cleanup_failures
        if cleanup_failures:
            record["status"] = "cleanup_incomplete"
        write_record(journal, record)
        signal.signal(signal.SIGTERM, previous_handler)
        print(
            json.dumps(
                {
                    "recovery_status": record["status"],
                    "ledger": str(journal.relative_to(ROOT)),
                    "dump_removed": record.get("dump_removed", False),
                    "databases_removed": len(record["removed_databases"]),
                    "leftovers": cleanup_failures,
                    "test_service_restored": record.get("running_after")
                    == running_before,
                }
            )
        )
    if cleanup_failures:
        raise DatabaseError(
            "Owned recovery cleanup incomplete; consult exact run ledger."
        )


if __name__ == "__main__":
    try:
        with runner_lock():
            rehearsal(instance("test"))
    except (DatabaseError, ConfigurationError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except (Exception, KeyboardInterrupt):  # noqa: BLE001 -- redact private driver errors
        print(
            "Recovery rehearsal failed or was interrupted; private output redacted.",
            file=sys.stderr,
        )
        sys.exit(1)
