"""Offline production-admin guards; no test opens a real database connection."""

import getpass
import hashlib
import json
import re
import secrets
import sys
from contextlib import nullcontext
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import psycopg
import pytest
from alembic import command

from brickvault_api import production_admin as admin
from brickvault_api import production_backup as backup
from brickvault_api.persistence.database import expected_revisions

MARKER = "brickvault-appraisal:" + "1" * 32 + ":" + "2" * 32
OWNER_URL = (
    "postgresql+psycopg://brickvault_appraisal_prod_owner:"
    + "a" * 64
    + "@127.0.0.1:5432/brickvault_appraisal_prod"
)
RUNTIME_URL = (
    "postgresql+psycopg://brickvault_appraisal_prod_runtime:"
    + "b" * 64
    + "@127.0.0.1:5432/brickvault_appraisal_prod"
)


def descriptor(**changes: object) -> bytes:
    return json.dumps(
        {
            "purpose": "production",
            "database": admin.DATABASE,
            "owner_url": OWNER_URL,
            "runtime_url": RUNTIME_URL,
            "ownership_marker": MARKER,
            **changes,
        }
    ).encode()


def test_exact_production_descriptor_and_redacted_representation() -> None:
    config = admin.parse_config(descriptor())
    assert config.marker == MARKER
    assert config.owner_url == OWNER_URL
    assert OWNER_URL not in repr(config)
    assert MARKER not in repr(config)


@pytest.mark.parametrize(
    "change",
    [
        {"purpose": "test"},
        {"database": "brickvault_dev"},
        {"owner_url": OWNER_URL.replace("_owner:", "_runtime:")},
        {"owner_url": OWNER_URL.replace("127.0.0.1", "192.0.2.10")},
        {"runtime_url": RUNTIME_URL.replace(":5432/", ":55433/")},
        {"runtime_url": OWNER_URL},
        {"ownership_marker": "wrong"},
        {"owner_url": 4},
        {"extra": "value"},
    ],
)
def test_descriptor_refuses_nonapproved_targets(change: dict[str, object]) -> None:
    with pytest.raises((admin.AdminError, ValueError)) as caught:
        admin.parse_config(descriptor(**change))
    assert "a" * 64 not in str(caught.value)
    assert "b" * 64 not in str(caught.value)


def test_duplicate_and_nonobject_json_refused() -> None:
    with pytest.raises(admin.AdminError):
        admin.parse_config(descriptor().replace(b'"purpose":', b'"purpose":"test","purpose":'))
    with pytest.raises(admin.AdminError):
        admin.parse_config(b"[]")


def test_maintenance_session_requires_peer_socket_and_loopback_pg18() -> None:
    expected = {
        "role": "postgres",
        "login": "postgres",
        "database": "postgres",
        "socket": True,
        "listen": "127.0.0.1",
        "port": 5432,
        "recovery": False,
        "version": 180006,
    }
    admin.validate_maintenance_session(expected)
    for change in (
        {"role": "other"},
        {"socket": False},
        {"listen": "*"},
        {"port": 55433},
        {"recovery": True},
        {"version": 170006},
    ):
        with pytest.raises(admin.AdminError):
            admin.validate_maintenance_session({**expected, **change})


def test_invalid_invocation_redacts_secret_and_stops_before_config(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def forbidden(*args: Any, **kwargs: Any) -> None:
        pytest.fail("Invalid invocation read production configuration")

    monkeypatch.setattr(admin, "_load_config", forbidden)
    sentinel = "synthetic-secret-sentinel"
    assert admin.main(["provision-db", "--password", sentinel]) == 1
    assert admin.main(["migrate", "--recovery-proof", sentinel, "--owner-password", sentinel]) == 1
    result = capsys.readouterr()
    assert sentinel not in result.out + result.err


def test_cli_redacts_underlying_credential_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    config = admin.parse_config(descriptor())
    sentinel = "synthetic-secret-sentinel"
    monkeypatch.setattr(admin, "_load_config", lambda *_: config)

    def fail(*_: Any) -> None:
        raise RuntimeError("driver detail included " + sentinel)

    monkeypatch.setattr(admin, "provision_db", fail)
    assert admin.main(["provision-db"]) == 1
    output = capsys.readouterr()
    assert sentinel not in output.out + output.err
    assert "refused" in output.err


def test_preflight_recognizes_only_fully_absent_or_verified_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = admin.parse_config(descriptor())
    connection = object()
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(connection))
    monkeypatch.setattr(admin, "_snapshot", lambda *_: ([], None))
    assert "unused" in admin.preflight(config)
    monkeypatch.setattr(admin, "_snapshot", lambda *_: ([{"rolname": admin.OWNER}], None))
    with pytest.raises(admin.AdminError):
        admin.preflight(config)


def test_provisioned_state_checks_role_flags_marker_membership_and_acl(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = admin.parse_config(descriptor())
    roles = [
        {
            "rolname": name,
            "rolcanlogin": True,
            "rolsuper": False,
            "rolcreatedb": False,
            "rolcreaterole": False,
            "rolreplication": False,
            "rolbypassrls": False,
            "marker": MARKER + ":role",
        }
        for name in (admin.OWNER, admin.RUNTIME)
    ]
    database = {"owner": admin.OWNER, "marker": MARKER}
    grants = {
        "connect": True,
        "create": False,
        "temporary": False,
        "public_access": False,
    }

    class Result:
        def __init__(self, row: dict[str, Any]) -> None:
            self.row = row

        def fetchone(self) -> dict[str, Any]:
            return self.row

    class Maintenance:
        def execute(self, query: str, *_: Any) -> Result:
            return Result({"exists": False} if "pg_auth_members" in query else grants)

    monkeypatch.setattr(admin, "_snapshot", lambda *_: (roles, database))
    connection = Maintenance()
    admin._require_provisioned(connection, config)  # type: ignore[arg-type]
    database["owner"] = "postgres"
    with pytest.raises(admin.AdminError, match="owner or marker"):
        admin._require_provisioned(connection, config)  # type: ignore[arg-type]
    database["owner"] = admin.OWNER
    roles[1]["rolsuper"] = True
    with pytest.raises(admin.AdminError, match="role ownership"):
        admin._require_provisioned(connection, config)  # type: ignore[arg-type]
    roles[1]["rolsuper"] = False
    grants["public_access"] = True
    with pytest.raises(admin.AdminError, match="grants"):
        admin._require_provisioned(connection, config)  # type: ignore[arg-type]


def test_provision_refuses_existing_role_before_any_sql(monkeypatch: pytest.MonkeyPatch) -> None:
    config = admin.parse_config(descriptor())

    class NoMutation:
        def execute(self, *_: Any, **__: Any) -> None:
            pytest.fail("Existing role reached provisioning SQL")

    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(NoMutation()))
    monkeypatch.setattr(admin, "_snapshot", lambda *_: ([{"rolname": admin.OWNER}], None))
    with pytest.raises(admin.AdminError, match="existing or partial"):
        admin.provision_db(config)


def test_scram_verifier_matches_postgresql_format_without_plaintext() -> None:
    verifier = admin._scram_verifier("a" * 64, 4096, bytes(range(16)))
    assert verifier == (
        "SCRAM-SHA-256$4096:AAECAwQFBgcICQoLDA0ODw==$"
        "HdrLQKlGCF6BYVPVDo1W42SrzG2w7U3LkMEWU/Rhlxs=:"
        "hKfY4QZft7Vi1wQiz9MvToq8CBi2+Wb1+1VTNTnG3w8="
    )
    assert "a" * 64 not in verifier
    with pytest.raises(admin.AdminError):
        admin._scram_verifier("synthetic-secret-sentinel", 4096, bytes(range(16)))


def test_provision_sends_only_verifiers_after_effective_logging_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner_sentinel = "deadbeef" * 8
    runtime_sentinel = "cafebabe" * 8
    config = admin.parse_config(
        descriptor(
            owner_url=OWNER_URL.replace("a" * 64, owner_sentinel),
            runtime_url=RUNTIME_URL.replace("b" * 64, runtime_sentinel),
        )
    )
    events: list[str] = []
    role_sql: list[str] = []

    class Result:
        def __init__(
            self, row: dict[str, Any] | None = None, rows: list[dict[str, Any]] | None = None
        ):
            self.row, self.rows = row, rows or []

        def fetchone(self) -> dict[str, Any] | None:
            return self.row

        def fetchall(self) -> list[dict[str, Any]]:
            return self.rows

    class Maintenance:
        def __init__(self) -> None:
            self.settings: dict[str, str] = {}

        def transaction(self) -> Any:
            return nullcontext()

        def execute(self, query: Any, params: Any = None) -> Result:
            statement = query.as_string(None) if hasattr(query, "as_string") else query
            if "shared_preload_libraries" in statement:
                return Result({"shared": "", "session": "", "local": ""})
            if statement.startswith("SET "):
                match = re.fullmatch(r'SET "([a-z_]+)" = \'([^\']+)\'', statement)
                assert match is not None
                self.settings[match[1]] = match[2]
                events.append("setting")
                return Result()
            if "FROM pg_settings" in statement:
                events.append("logging_readback")
                return Result(
                    rows=[{"name": key, "setting": value} for key, value in self.settings.items()]
                )
            if "scram_iterations" in statement:
                return Result({"encryption": "scram-sha-256", "iterations": 4096})
            if statement.startswith("CREATE ROLE "):
                assert "logging_readback" in events
                role_sql.append(statement)
                events.append("create_role")
            return Result()

    maintenance = Maintenance()
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(maintenance))
    monkeypatch.setattr(admin, "_snapshot", lambda *_: ([], None))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: None)
    monkeypatch.setattr(
        admin,
        "_owner_connection",
        lambda *_: nullcontext(SimpleNamespace(execute=lambda *_: None)),
    )
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: None)
    monkeypatch.setattr(admin, "_runtime_identity", lambda *_: None)
    salts = iter((bytes(range(16)), bytes(range(16, 32))))
    monkeypatch.setattr(secrets, "token_bytes", lambda size: next(salts))
    admin.provision_db(config)
    assert len(role_sql) == 2
    assert all("SCRAM-SHA-256$4096:" in statement for statement in role_sql)
    assert all(
        owner_sentinel not in statement and runtime_sentinel not in statement
        for statement in role_sql
    )
    assert events.index("logging_readback") < events.index("create_role")


def test_provision_refuses_when_logging_readback_differs_before_verifier_sql(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner_sentinel = "deadbeef" * 8
    runtime_sentinel = "cafebabe" * 8
    config = admin.parse_config(
        descriptor(
            owner_url=OWNER_URL.replace("a" * 64, owner_sentinel),
            runtime_url=RUNTIME_URL.replace("b" * 64, runtime_sentinel),
        )
    )
    statements: list[str] = []

    class Result:
        def __init__(self, row: dict[str, Any] | None = None):
            self.row = row

        def fetchone(self) -> dict[str, Any] | None:
            return self.row

        def fetchall(self) -> list[dict[str, Any]]:
            return []  # Effective settings could not be confirmed.

    class Maintenance:
        def execute(self, query: Any, params: Any = None) -> Result:
            statement = query.as_string(None) if hasattr(query, "as_string") else query
            statements.append(statement)
            if "shared_preload_libraries" in statement:
                return Result({"shared": "", "session": "", "local": ""})
            return Result()

    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(Maintenance()))
    monkeypatch.setattr(admin, "_snapshot", lambda *_: ([], None))
    with pytest.raises(admin.AdminError, match="logging controls"):
        admin.provision_db(config)
    assert not any(
        "CREATE ROLE" in statement or "SCRAM-SHA-256$" in statement for statement in statements
    )
    assert all(
        owner_sentinel not in statement and runtime_sentinel not in statement
        for statement in statements
    )


def test_unreviewed_preload_refuses_before_any_secret_session_sql() -> None:
    statements: list[str] = []

    class Connection:
        def execute(self, statement: str) -> Any:
            statements.append(statement)
            return SimpleNamespace(
                fetchone=lambda: {"shared": "pgaudit", "session": "", "local": ""}
            )

    with pytest.raises(admin.AdminError, match="preload"):
        admin._credential_session_guard(Connection())  # type: ignore[arg-type]
    assert len(statements) == 1
    assert "shared_preload_libraries" in statements[0]


def test_runtime_descriptor_connects_only_to_exact_loopback_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = admin.parse_config(descriptor())
    observed: list[dict[str, Any]] = []
    row = {
        "role": admin.RUNTIME,
        "database": admin.DATABASE,
        "marker": MARKER,
        "owner": admin.OWNER,
    }

    class Connection:
        def __enter__(self) -> "Connection":
            return self

        def __exit__(self, *_: Any) -> None:
            return None

        def execute(self, _: str) -> Any:
            return SimpleNamespace(fetchone=lambda: row)

    def connect(**kwargs: Any) -> Connection:
        observed.append(kwargs)
        return Connection()

    monkeypatch.setattr(psycopg, "connect", connect)
    admin._runtime_identity(config)
    assert observed[0]["host"] == "127.0.0.1"
    assert observed[0]["port"] == 5432
    assert observed[0]["dbname"] == admin.DATABASE
    row["owner"] = "postgres"
    with pytest.raises(admin.AdminError):
        admin._runtime_identity(config)


def test_migration_requires_receipt_before_alembic(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    owner = object()
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: None)
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: None)
    monkeypatch.setattr(admin, "_runtime_identity", lambda *_: None)
    monkeypatch.setattr(admin, "_revisions", lambda *_: ())

    def no_receipt(*_: Any) -> None:
        raise admin.AdminError("No verified backup receipt")

    monkeypatch.setattr(admin, "_recovery_proof", no_receipt)
    monkeypatch.setattr(command, "upgrade", lambda *_: pytest.fail("Migration ran"))
    with pytest.raises(admin.AdminError, match="receipt"):
        admin.migrate(config, tmp_path / "absent.json")


def test_grant_command_uses_shared_enumerated_policy_after_guards(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    owner = object()
    events: list[str] = []
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: events.append("ownership"))
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: events.append("schema"))
    monkeypatch.setattr(admin, "_revisions", lambda *_: expected_revisions())
    monkeypatch.setattr(admin, "_recovery_proof", lambda *_: events.append("recovery"))
    monkeypatch.setattr(admin, "grant_runtime", lambda *_: events.append("enumerated_grants"))
    admin.grant_runtime_role(config, tmp_path / "receipt.json")
    assert events == ["ownership", "schema", "recovery", "enumerated_grants"]


def test_generated_recovery_proof_binds_verified_receipt_copies_and_revision(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    run_id = "3" * 32
    receipt: dict[str, Any] = {
        "schema": 2,
        "purpose": "production",
        "database": admin.DATABASE,
        "ownership_marker": MARKER,
        "run_id": run_id,
        "revisions_at_backup": ["0016_hunt_cached_runs"],
        "verified_at_utc": datetime.now(UTC).isoformat(),
        "repositories": {
            "proxmox": {"uri": backup.PROXMOX_REPO, "id": "a" * 64},
            "drive": {"uri": backup.DRIVE_REPO, "id": "b" * 64},
        },
        "artifacts": {
            name: {
                "bytes": 5,
                "sha256": "c" * 64,
                "snapshots": {"proxmox": str(index) * 64, "drive": str(index + 3) * 64},
            }
            for index, name in enumerate(backup.ARTIFACTS, start=4)
        },
    }
    raw = json.dumps(receipt, sort_keys=True).encode()
    proof = backup._proof_from_receipt(
        run_id, receipt, raw, ("0016_hunt_cached_runs",), datetime.now(UTC)
    )
    monkeypatch.setattr(backup, "PROOF_DIR", tmp_path)
    monkeypatch.setattr(admin, "_protected_file", lambda _: json.dumps(proof).encode())
    monkeypatch.setattr(backup, "verified_receipt", lambda _: (receipt, raw))
    path = tmp_path / f"{run_id}.json"
    admin._recovery_proof(path, config, ("0016_hunt_cached_runs",))
    with pytest.raises(admin.AdminError):
        admin._recovery_proof(path, config, ())
    proof["backup_receipt_sha256"] = "f" * 64
    with pytest.raises(admin.AdminError):
        admin._recovery_proof(path, config, None)
    proof["backup_receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    proof["artifact_snapshots"]["database.dump"].pop("drive")
    with pytest.raises(admin.AdminError):
        admin._recovery_proof(path, config, None)
    proof["artifact_snapshots"] = {
        name: row["snapshots"] for name, row in receipt["artifacts"].items()
    }
    proof["verified_at_utc"] = (datetime.now(UTC) - timedelta(days=2)).isoformat()
    with pytest.raises(admin.AdminError, match="stale"):
        admin._recovery_proof(path, config, None)
    proof["verified_at_utc"] = datetime.now(UTC).isoformat()
    receipt["verified_at_utc"] = (datetime.now(UTC) - timedelta(days=2)).isoformat()
    raw = json.dumps(receipt, sort_keys=True).encode()
    proof["backup_receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(admin.AdminError, match="Verified backup is stale"):
        admin._recovery_proof(path, config, None)


def test_grant_and_bootstrap_require_generated_dual_backup_proof(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    run_id = "8" * 32
    receipt = {
        "purpose": "production",
        "database": admin.DATABASE,
        "ownership_marker": MARKER,
        "run_id": run_id,
        "revisions_at_backup": [],
        "verified_at_utc": datetime.now(UTC).isoformat(),
        "repositories": {
            "proxmox": {"uri": backup.PROXMOX_REPO, "id": "a" * 64},
            "drive": {"uri": backup.DRIVE_REPO, "id": "b" * 64},
        },
        "artifacts": {
            name: {
                "bytes": 5,
                "sha256": "c" * 64,
                "snapshots": {"proxmox": str(index) * 64, "drive": str(index + 3) * 64},
            }
            for index, name in enumerate(backup.ARTIFACTS, start=4)
        },
    }
    raw = json.dumps(receipt, sort_keys=True).encode()
    proof = backup._proof_from_receipt(run_id, receipt, raw, (), datetime.now(UTC))
    path = tmp_path / f"{run_id}.json"
    owner = SimpleNamespace(scalar=lambda *_: 0)
    grants: list[str] = []
    monkeypatch.setattr(backup, "PROOF_DIR", tmp_path)
    monkeypatch.setattr(backup, "verified_receipt", lambda _: (receipt, raw))
    monkeypatch.setattr(admin, "_protected_file", lambda _: json.dumps(proof).encode())
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: None)
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: None)
    monkeypatch.setattr(admin, "_revisions", lambda *_: expected_revisions())
    monkeypatch.setattr(admin, "grant_runtime", lambda *_: grants.append("applied"))
    monkeypatch.setattr(admin, "_runtime_guard", lambda *_: None)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(
        getpass, "getpass", lambda *_: (_ for _ in ()).throw(RuntimeError("hidden input reached"))
    )

    proof["backup_receipt_sha256"] = "f" * 64
    with pytest.raises(admin.AdminError):
        admin.grant_runtime_role(config, path)
    with pytest.raises(admin.AdminError):
        admin.bootstrap_owner(config, path)
    assert grants == []

    proof["backup_receipt_sha256"] = hashlib.sha256(raw).hexdigest()
    admin.grant_runtime_role(config, path)
    assert grants == ["applied"]
    with pytest.raises(RuntimeError, match="hidden input reached"):
        admin.bootstrap_owner(config, path)


def test_bootstrap_refuses_existing_account_before_hidden_input(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    owner = SimpleNamespace(scalar=lambda *_: 1)
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: None)
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: None)
    monkeypatch.setattr(admin, "_revisions", lambda *_: expected_revisions())
    monkeypatch.setattr(admin, "_recovery_proof", lambda *_: None)
    monkeypatch.setattr(getpass, "getpass", lambda *_: pytest.fail("Hidden input reached"))
    with pytest.raises(admin.AdminError, match="already exists"):
        admin.bootstrap_owner(config, tmp_path / "proof.json")


def test_bootstrap_routes_hash_write_through_guarded_peer_owner(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config = admin.parse_config(descriptor())
    owner = SimpleNamespace(scalar=lambda *_: 0)
    sentinel = "synthetic-hidden-input"
    observed: list[str] = []
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: None)
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: None)
    monkeypatch.setattr(admin, "_revisions", lambda *_: expected_revisions())
    monkeypatch.setattr(admin, "_recovery_proof", lambda *_: None)
    monkeypatch.setattr(admin, "_runtime_guard", lambda *_: None)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(getpass, "getpass", lambda *_: sentinel)

    class SpyAuthService:
        def __init__(self, database: Any) -> None:
            assert isinstance(database, admin._GuardedOwnerDatabase)

        def provision(self, password: str) -> None:
            assert password == sentinel
            observed.append("guarded_owner_auth")

    monkeypatch.setattr(admin, "AuthService", SpyAuthService)
    admin.bootstrap_owner(config, tmp_path / "receipt.json")
    assert observed == ["guarded_owner_auth"]


def test_guarded_owner_session_switches_role_only_after_logging_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = admin.parse_config(descriptor())
    events: list[str] = []

    class Result:
        def __init__(
            self, row: dict[str, Any] | None = None, rows: list[dict[str, Any]] | None = None
        ):
            self.row, self.rows = row, rows or []

        def fetchone(self) -> dict[str, Any] | None:
            return self.row

        def fetchall(self) -> list[dict[str, Any]]:
            return self.rows

    class Connection:
        closed = False

        def close(self) -> None:
            self.closed = True

        def execute(self, query: Any, params: Any = None) -> Result:
            statement = query.as_string(None) if hasattr(query, "as_string") else query
            if "server_version_num" in statement:
                return Result(
                    {
                        "role": "postgres",
                        "login": "postgres",
                        "database": admin.DATABASE,
                        "socket": True,
                        "version": 180006,
                        "listen": "127.0.0.1",
                        "port": 5432,
                        "recovery": False,
                        "marker": MARKER,
                        "owner": admin.OWNER,
                    }
                )
            if statement.startswith("SET ROLE "):
                assert events == ["guard"]
                events.append("set_role")
                return Result()
            if "session_user" in statement:
                return Result(
                    {"role": admin.OWNER, "login": "postgres", "database": admin.DATABASE}
                )
            if "alembic_version" in statement:
                return Result(rows=[{"version_num": "0016_hunt_cached_runs"}])
            pytest.fail("Unexpected guarded owner SQL")

    connection = Connection()
    monkeypatch.setattr(admin, "_require_root", lambda: None)
    monkeypatch.setattr(psycopg, "connect", lambda **_: connection)
    monkeypatch.setattr(admin, "_credential_session_guard", lambda *_: events.append("guard"))
    monkeypatch.setattr(admin, "_verify_credential_logging", lambda *_: events.append("verify"))
    database = admin._GuardedOwnerDatabase(config.owner_url, "production", MARKER, "owner")
    assert id(database.connect()) == id(connection)
    assert events == ["guard", "set_role", "verify"]
    assert connection.closed is False


def test_guarded_owner_failure_closes_session_before_account_sql(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = admin.parse_config(descriptor())
    statements: list[str] = []

    class Connection:
        closed = False

        def close(self) -> None:
            self.closed = True

        def execute(self, query: Any, params: Any = None) -> Any:
            statement = query.as_string(None) if hasattr(query, "as_string") else query
            statements.append(statement)
            return SimpleNamespace(
                fetchone=lambda: {
                    "role": "postgres",
                    "login": "postgres",
                    "database": admin.DATABASE,
                    "socket": True,
                    "version": 180006,
                    "listen": "127.0.0.1",
                    "port": 5432,
                    "recovery": False,
                    "marker": MARKER,
                    "owner": admin.OWNER,
                }
            )

    connection = Connection()
    monkeypatch.setattr(admin, "_require_root", lambda: None)
    monkeypatch.setattr(psycopg, "connect", lambda **_: connection)
    monkeypatch.setattr(
        admin,
        "_credential_session_guard",
        lambda *_: (_ for _ in ()).throw(admin.AdminError("logging guard failed")),
    )
    database = admin._GuardedOwnerDatabase(config.owner_url, "production", MARKER, "owner")
    with pytest.raises(admin.AdminError, match="logging guard failed"):
        database.connect()
    assert connection.closed is True
    assert not any(
        "SET ROLE" in statement or "auth_principal" in statement for statement in statements
    )


def test_verify_is_read_only_and_checks_single_account(monkeypatch: pytest.MonkeyPatch) -> None:
    config = admin.parse_config(descriptor())
    owner = SimpleNamespace(scalar=lambda *_: 1)
    seen: list[str] = []
    monkeypatch.setattr(admin, "_maintenance", lambda: nullcontext(object()))
    monkeypatch.setattr(admin, "_require_provisioned", lambda *_: seen.append("ownership"))
    monkeypatch.setattr(admin, "_owner_connection", lambda *_: nullcontext(owner))
    monkeypatch.setattr(admin, "_schema_guard", lambda *_: seen.append("schema"))
    monkeypatch.setattr(admin, "_revisions", lambda *_: expected_revisions())
    monkeypatch.setattr(admin, "_runtime_guard", lambda *_: seen.append("runtime"))
    admin.verify(config)
    admin.verify(config)
    assert seen == ["ownership", "schema", "runtime"] * 2
