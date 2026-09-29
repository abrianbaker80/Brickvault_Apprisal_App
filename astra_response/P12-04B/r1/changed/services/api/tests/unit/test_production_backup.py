"""Backup transport behavior without production PostgreSQL or remote services."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

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
