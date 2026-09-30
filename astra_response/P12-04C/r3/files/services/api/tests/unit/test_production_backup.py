"""Backup transport behavior without production PostgreSQL or remote services."""

import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from brickvault_api import production_admin as admin
from brickvault_api import production_backup as backup


def _source(size: int) -> list[str]:
    return [
        sys.executable,
        "-c",
        "import sys;sys.stdout.buffer.write(bytes(range(256))*" + str(size // 256) + ")",
    ]


def _sink(path: Path) -> list[str]:
    return [
        sys.executable,
        "-c",
        "import pathlib,sys;pathlib.Path(sys.argv[1]).write_bytes(sys.stdin.buffer.read())",
        str(path),
    ]


def test_dual_stream_has_identical_bytes_and_digest(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    size, digest = backup.stream_to_two(
        _source(1024 * 1024),
        [_sink(first), _sink(second)],
        [os.environ, os.environ],
        deadline_seconds=30,
    )
    expected = bytes(range(256)) * 4096
    assert first.read_bytes() == second.read_bytes() == expected
    assert size == len(expected)
    assert digest == hashlib.sha256(expected).hexdigest()


def test_one_failed_destination_fails_entire_run(tmp_path: Path) -> None:
    first = tmp_path / "first"
    failed = [sys.executable, "-c", "import sys;sys.stdin.buffer.read();sys.exit(4)"]
    with pytest.raises(backup.BackupError):
        backup.stream_to_two(
            _source(1024 * 1024),
            [_sink(first), failed],
            [os.environ, os.environ],
            deadline_seconds=30,
        )


def test_source_failure_is_not_reported_as_success(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    source = [sys.executable, "-c", "import sys;sys.stdout.buffer.write(b'x');sys.exit(2)"]
    with pytest.raises(backup.BackupError):
        backup.stream_to_two(
            source,
            [_sink(first), _sink(second)],
            [os.environ, os.environ],
            deadline_seconds=30,
        )


def test_cli_redacts_underlying_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refused() -> str:
        raise RuntimeError("sensitive credential material")

    monkeypatch.setattr(backup, "backup", refused)
    assert backup.main(["backup"]) == 1
    output = capsys.readouterr()
    assert "sensitive" not in output.out + output.err
    assert "refused" in output.err


def test_preflight_refuses_without_root(monkeypatch: pytest.MonkeyPatch) -> None:
    def refused() -> None:
        raise backup.BackupError("root required")

    monkeypatch.setattr(backup.admin, "_require_root", refused)
    with pytest.raises(backup.BackupError, match="root required"):
        backup._preflight()


def test_producer_does_not_use_plaintext_output_path() -> None:
    for artifact in backup.ARTIFACTS:
        command = backup._producer(artifact, ("etc/brickvault/production-admin.json",))
        assert command[0].startswith("/")
        assert "-f" not in command or artifact == "configuration.tar"
        if artifact == "configuration.tar":
            assert command[command.index("-cf") + 1] == "-"


@pytest.mark.parametrize(
    ("artifact", "executable", "options"),
    [
        ("database.dump", "/usr/lib/postgresql/18/bin/pg_dump", ["--format=custom"]),
        ("globals.sql", "/usr/lib/postgresql/18/bin/pg_dumpall", ["--globals-only"]),
    ],
)
def test_database_producers_use_direct_local_peer_without_privilege_transition(
    artifact: str, executable: str, options: list[str]
) -> None:
    expected = [
        executable,
        *options,
        "--no-password",
        "--host=/var/run/postgresql",
        "--username=postgres",
    ]
    if artifact == "database.dump":
        expected.append("--dbname=brickvault_appraisal_prod")
    assert backup._producer(artifact, ()) == expected


def test_source_cannot_inherit_credentials_or_request_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PGPASSWORD", "synthetic-password")
    monkeypatch.setenv("PGSERVICE", "synthetic-service")
    first, second = tmp_path / "first", tmp_path / "second"
    source = [
        sys.executable,
        "-c",
        "import json,os,sys; print(json.dumps({'stdin':sys.stdin.read(),"
        "'home':os.getenv('HOME'),'passfile':os.getenv('PGPASSFILE'),"
        "'password':os.getenv('PGPASSWORD'),'service':os.getenv('PGSERVICE')}))",
    ]
    backup.stream_to_two(
        source, [_sink(first), _sink(second)], [os.environ, os.environ], deadline_seconds=30
    )
    assert first.read_bytes() == second.read_bytes()
    assert json.loads(first.read_bytes()) == {
        "stdin": "",
        "home": "/nonexistent",
        "passfile": "/dev/null",
        "password": None,
        "service": None,
    }


def test_rclone_unlock_is_limited_to_drive_child(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "rclone-config.pass").write_text("synthetic-config-key\n", encoding="ascii")
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path)
    proxmox, drive = backup.DESTINATIONS
    assert "RCLONE_CONFIG_PASS" not in proxmox.environment()
    assert drive.environment()["RCLONE_CONFIG_PASS"] == "synthetic-config-key"


def _identity() -> dict[str, object]:
    return {
        "schema": 1,
        "purpose": "brickvault-production-backup",
        "repositories": {
            destination.name: {
                "uri": destination.repository,
                "id": ("a" if destination.name == "proxmox" else "b") * 64,
            }
            for destination in backup.DESTINATIONS
        },
        "rclone_client_sha256": hashlib.sha256(b"synthetic-client").hexdigest(),
    }


def test_repository_identity_rejects_wrong_uri() -> None:
    identity = _identity()
    ids, client_hash = backup._validated_identity(identity)
    assert set(ids) == {"proxmox", "drive"}
    assert client_hash == hashlib.sha256(b"synthetic-client").hexdigest()
    identity["repositories"]["drive"]["uri"] = "rclone:unreviewed:other"  # type: ignore[index]
    with pytest.raises(backup.BackupError, match="repository identity"):
        backup._validated_identity(identity)


def test_destination_identity_rejects_broader_drive_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "rclone-config.pass").write_text("synthetic-config-key\n", encoding="ascii")
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path)
    monkeypatch.setattr(
        backup.admin, "_protected_file", lambda _: json.dumps(_identity()).encode("utf-8")
    )
    remote = {
        "bva-drive": {
            "type": "drive",
            "scope": "drive",
            "client_id": "synthetic-client",
            "client_secret": "synthetic",
            "token": "synthetic",
        }
    }
    monkeypatch.setattr(
        backup.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, json.dumps(remote).encode("utf-8"), b""
        ),
    )
    with pytest.raises(backup.BackupError, match="scope differs"):
        backup._verify_destination_identity()


RUN = "1" * 32
MARKER = "brickvault-appraisal:" + "2" * 32 + ":" + "3" * 32


def _complete_receipt() -> dict[str, object]:
    snapshots = iter("456789")
    return {
        "schema": 2,
        "purpose": "production",
        "database": backup.DATABASE,
        "ownership_marker": MARKER,
        "run_id": RUN,
        "revisions_at_backup": [],
        "verified_at_utc": datetime.now(UTC).isoformat(),
        "repositories": {
            d.name: {"uri": d.repository, "id": ("a" if d.name == "proxmox" else "b") * 64}
            for d in backup.DESTINATIONS
        },
        "artifacts": {
            name: {
                "bytes": 7,
                "sha256": "c" * 64,
                "snapshots": {d.name: next(snapshots) * 64 for d in backup.DESTINATIONS},
            }
            for name in backup.ARTIFACTS
        },
    }


def _mock_receipt_context(
    monkeypatch: pytest.MonkeyPatch, receipt: dict[str, object]
) -> list[tuple[str, str]]:
    config = admin.AdminConfig("synthetic-owner-url", "synthetic-runtime-url", MARKER)
    monkeypatch.setattr(backup, "_preflight", lambda: config)
    raw = json.dumps(receipt, sort_keys=True).encode()
    identity = json.dumps(_identity()).encode()
    monkeypatch.setattr(
        backup.admin,
        "_protected_file",
        lambda path: identity if path.name == "repositories.json" else raw,
    )
    observed: list[tuple[str, str]] = []
    monkeypatch.setattr(
        backup,
        "_readback",
        lambda dest, _snap, artifact, *_: observed.append((dest.name, artifact)),
    )
    monkeypatch.setattr(backup, "_restic", lambda dest, *_: observed.append((dest.name, "check")))
    return observed


def test_complete_receipt_requires_six_readbacks_and_two_checks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = _complete_receipt()
    observed = _mock_receipt_context(monkeypatch, receipt)
    verified, raw = backup.verified_receipt(RUN)
    assert verified == receipt
    assert (
        hashlib.sha256(raw).hexdigest()
        == hashlib.sha256(json.dumps(receipt, sort_keys=True).encode()).hexdigest()
    )
    assert observed == [
        (destination.name, artifact)
        for artifact in backup.ARTIFACTS
        for destination in backup.DESTINATIONS
    ] + [(destination.name, "check") for destination in backup.DESTINATIONS]


def test_missing_destination_or_tampered_receipt_refuses_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = _complete_receipt()
    receipt["artifacts"]["database.dump"]["snapshots"].pop("drive")  # type: ignore[index]
    observed = _mock_receipt_context(monkeypatch, receipt)
    with pytest.raises(backup.BackupError, match="artifact"):
        backup.verified_receipt(RUN)
    assert not observed


def test_failed_encrypted_readback_never_finishes_receipt_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = _complete_receipt()
    observed = _mock_receipt_context(monkeypatch, receipt)

    def readback(
        destination: backup.Destination, _snapshot: str, artifact: str, *_: object
    ) -> None:
        observed.append((destination.name, artifact))
        if destination.name == "drive":
            raise backup.BackupError("Encrypted readback digest differs.")

    monkeypatch.setattr(backup, "_readback", readback)
    with pytest.raises(backup.BackupError, match="readback"):
        backup.verified_receipt(RUN)
    assert observed == [("proxmox", "database.dump"), ("drive", "database.dump")]


def test_receipt_change_during_readback_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    receipt = _complete_receipt()
    observed = _mock_receipt_context(monkeypatch, receipt)
    raw = json.dumps(receipt, sort_keys=True).encode()
    reads = 0

    def protected(path: Path) -> bytes:
        nonlocal reads
        if path.name == "repositories.json":
            return json.dumps(_identity()).encode()
        reads += 1
        return raw if reads == 1 else raw + b" "

    monkeypatch.setattr(backup.admin, "_protected_file", protected)
    with pytest.raises(backup.BackupError, match="changed"):
        backup.verified_receipt(RUN)
    assert len(observed) == 8
    receipt = _complete_receipt()
    receipt["ownership_marker"] = "brickvault-appraisal:" + "f" * 32 + ":" + "e" * 32
    observed = _mock_receipt_context(monkeypatch, receipt)
    with pytest.raises(backup.BackupError, match="identity"):
        backup.verified_receipt(RUN)
    assert not observed


def test_finalize_proof_derives_only_verified_snapshots_and_receipt_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    receipt = _complete_receipt()
    raw = json.dumps(receipt, sort_keys=True).encode()
    config = admin.AdminConfig("synthetic-owner-url", "synthetic-runtime-url", MARKER)
    monkeypatch.setattr(backup, "verified_receipt", lambda _: (receipt, raw))
    monkeypatch.setattr(backup.admin, "_load_config", lambda _: config)
    monkeypatch.setattr(backup, "_current_revisions", lambda _: ())
    stored: list[dict[str, object]] = []
    monkeypatch.setattr(
        backup,
        "_write_proof",
        lambda _run, proof: (stored.append(proof), tmp_path / "proof.json")[1],
    )
    assert backup.finalize_proof(RUN) == tmp_path / "proof.json"
    assert len(stored) == 1
    proof = stored[0]
    assert proof["backup_receipt_sha256"] == hashlib.sha256(raw).hexdigest()
    assert (
        proof["proxmox_snapshot"] == receipt["artifacts"]["database.dump"]["snapshots"]["proxmox"]
    )  # type: ignore[index]
    assert proof["drive_snapshot"] == receipt["artifacts"]["database.dump"]["snapshots"]["drive"]  # type: ignore[index]
    assert proof["revisions_at_backup"] == []

    receipt["verified_at_utc"] = (datetime.now(UTC) - timedelta(days=2)).isoformat()
    with pytest.raises(backup.BackupError, match="too old"):
        backup.finalize_proof(RUN)
    assert len(stored) == 1


def test_finalize_cli_rejects_operator_snapshot_argument(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(backup, "finalize_proof", lambda _: pytest.fail("Finalization reached"))
    assert backup.main(["finalize-proof", RUN, "--proxmox-snapshot", "f" * 64]) == 1
    output = capsys.readouterr()
    assert "refused" in output.err
    assert "f" * 64 not in output.out + output.err
