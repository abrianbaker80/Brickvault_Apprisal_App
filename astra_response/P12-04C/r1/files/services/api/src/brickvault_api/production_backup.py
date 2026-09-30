"""Guarded dual-destination production backups and encrypted readback.

The command is deliberately unavailable until the production descriptor,
database, and both repository credentials have been provisioned. No plaintext
database artifact is written to a persistent file.
"""

import argparse
import hashlib
import json
import os
import queue
import re
import stat
import subprocess
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, NoReturn

from brickvault_api import production_admin as admin

DATABASE = admin.DATABASE
BACKUP_DIR = Path("/etc/brickvault/backup")
RECEIPT_DIR = Path("/etc/brickvault/backup/receipts")
PROOF_DIR = Path("/etc/brickvault/backup/proofs")
PROXMOX_REPO = "sftp:bva-proxmox-repository:/repository"
DRIVE_REPO = "rclone:bva-drive:Brickvault_Apprisal_App_Backup/restic-production"
RESTIC = "/usr/local/bin/restic"
RCLONE = "/usr/local/bin/rclone"
PG_DUMP = "/usr/lib/postgresql/18/bin/pg_dump"
PG_DUMPALL = "/usr/lib/postgresql/18/bin/pg_dumpall"
RUNUSER = "/usr/sbin/runuser"
TAR = "/usr/bin/tar"
TIMEOUT = "/usr/bin/timeout"
SSH_COMMAND = "ssh -F /etc/brickvault/backup/proxmox-ssh-config bva-proxmox-repository -s sftp"
ARTIFACTS = ("database.dump", "globals.sql", "configuration.tar")
RUN_ID = re.compile(r"[a-f0-9]{32}\Z")
SNAPSHOT_ID = re.compile(r"[a-f0-9]{64}\Z")
CHUNK = 256 * 1024
STREAM_DEADLINE_SECONDS = 4 * 60 * 60


class BackupError(RuntimeError):
    """Generic, credential-free operator failure."""


@dataclass(frozen=True)
class Destination:
    name: str
    repository: str
    password_file: Path
    options: tuple[str, ...]

    def environment(self) -> dict[str, str]:
        environment = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": "/var/lib/brickvault-backup-runner",
            "RESTIC_PASSWORD_FILE": str(self.password_file),
            "RESTIC_CACHE_DIR": "/var/cache/brickvault-backup/restic",
            "RCLONE_CONFIG": str(BACKUP_DIR / "rclone.conf"),
            "RCLONE_CACHE_DIR": "/var/cache/brickvault-backup/rclone",
        }
        if self.name == "drive":
            environment["RCLONE_CONFIG_PASS"] = (
                (BACKUP_DIR / "rclone-config.pass").read_text(encoding="ascii").strip()
            )
        return environment

    def command(self, *arguments: str) -> list[str]:
        return [RESTIC, *self.options, "-r", self.repository, *arguments]


DESTINATIONS = (
    Destination(
        "proxmox",
        PROXMOX_REPO,
        BACKUP_DIR / "proxmox-restic.pass",
        ("-o", f"sftp.command={SSH_COMMAND}"),
    ),
    Destination("drive", DRIVE_REPO, BACKUP_DIR / "drive-restic.pass", ()),
)


def _validated_identity(value: Any) -> tuple[dict[str, str], str]:
    if (
        not isinstance(value, dict)
        or set(value) != {"schema", "purpose", "repositories", "rclone_client_sha256"}
        or type(value["schema"]) is not int
        or value["schema"] != 1
        or value["purpose"] != "brickvault-production-backup"
        or not isinstance(value["repositories"], dict)
        or set(value["repositories"]) != {destination.name for destination in DESTINATIONS}
        or not isinstance(value["rclone_client_sha256"], str)
        or SNAPSHOT_ID.fullmatch(value["rclone_client_sha256"]) is None
    ):
        raise BackupError("Backup destination identity record is invalid.")
    identities: dict[str, str] = {}
    for destination in DESTINATIONS:
        record = value["repositories"][destination.name]
        if (
            not isinstance(record, dict)
            or set(record) != {"uri", "id"}
            or record["uri"] != destination.repository
            or not isinstance(record["id"], str)
            or SNAPSHOT_ID.fullmatch(record["id"]) is None
        ):
            raise BackupError("Backup repository identity differs.")
        identities[destination.name] = record["id"]
    return identities, value["rclone_client_sha256"]


def _verify_destination_identity() -> None:
    identities, client_hash = _validated_identity(
        json.loads(admin._protected_file(BACKUP_DIR / "repositories.json"))
    )
    environment = DESTINATIONS[1].environment()
    result = subprocess.run(
        [RCLONE, "config", "dump"],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise BackupError("Drive configuration cannot be opened.")
    remotes = json.loads(result.stdout)
    if not isinstance(remotes, dict) or set(remotes) != {"bva-drive"}:
        raise BackupError("Drive remote identity differs.")
    remote = remotes["bva-drive"]
    if not isinstance(remote, dict):
        raise BackupError("Drive remote identity differs.")
    client_id = remote.get("client_id")
    if (
        remote.get("type") != "drive"
        or remote.get("scope") != "drive.file"
        or not remote.get("client_secret")
        or not remote.get("token")
        or not isinstance(client_id, str)
        or not client_id.isascii()
        or hashlib.sha256(client_id.encode("ascii")).hexdigest() != client_hash
    ):
        raise BackupError("Drive client or scope differs.")
    for destination in DESTINATIONS:
        repository = json.loads(_restic(destination, "cat", "config", capture=True))
        if not isinstance(repository, dict) or repository.get("id") != identities[destination.name]:
            raise BackupError("Encrypted repository identity differs.")


def _regular_root_file(path: Path, modes: tuple[int, ...] = (0o400, 0o600)) -> None:
    if not path.is_absolute():
        raise BackupError("Backup input path is not absolute.")
    for parent in (path.parent, *path.parent.parents):
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise BackupError("Backup input directory is unsafe.")
    info = path.lstat()
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != 0
        or stat.S_IMODE(info.st_mode) not in modes
    ):
        raise BackupError("Backup input file is unsafe.")


def _tool(path: str) -> None:
    info = Path(path).lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o755:
        raise BackupError("Backup tool identity is unsafe.")


def _preflight() -> admin.AdminConfig:
    admin._require_root()
    config = admin._load_config(admin.CONFIG_PATH)
    for executable in (RESTIC, RCLONE, PG_DUMP, PG_DUMPALL, RUNUSER, TAR, TIMEOUT):
        _tool(executable)
    for destination in DESTINATIONS:
        _regular_root_file(destination.password_file)
    _regular_root_file(BACKUP_DIR / "rclone.conf")
    _regular_root_file(BACKUP_DIR / "rclone-config.pass")
    _regular_root_file(BACKUP_DIR / "repositories.json")
    _regular_root_file(BACKUP_DIR / "proxmox-ssh-config")
    _regular_root_file(BACKUP_DIR / "proxmox-known-hosts")
    _regular_root_file(BACKUP_DIR / "proxmox-transport_ed25519")
    if (BACKUP_DIR / "proxmox-restic.pass").read_bytes() == (
        BACKUP_DIR / "drive-restic.pass"
    ).read_bytes():
        raise BackupError("Repository credentials are not distinct.")
    _verify_destination_identity()
    with admin._maintenance() as maintenance:
        admin._require_provisioned(maintenance, config)
        directory = maintenance.execute("SHOW data_directory").fetchone()
        if directory is None or directory["data_directory"] != "/var/lib/postgresql/18/main":
            raise BackupError("Production PostgreSQL data location differs.")
    return config


def _run_id() -> str:
    import secrets

    return secrets.token_hex(16)


def _producer(artifact: str, configuration: Sequence[str]) -> list[str]:
    if artifact == "database.dump":
        return [
            RUNUSER,
            "-u",
            "postgres",
            "--",
            PG_DUMP,
            "--format=custom",
            "--host=/var/run/postgresql",
            "--username=postgres",
            f"--dbname={DATABASE}",
        ]
    if artifact == "globals.sql":
        return [
            RUNUSER,
            "-u",
            "postgres",
            "--",
            PG_DUMPALL,
            "--globals-only",
            "--host=/var/run/postgresql",
            "--username=postgres",
        ]
    if artifact == "configuration.tar":
        return [TAR, "-C", "/", "-cf", "-", "--", *configuration]
    raise BackupError("Unknown backup artifact.")


def _configuration_files() -> tuple[str, ...]:
    required = [
        Path("/etc/brickvault/production-admin.json"),
        Path("/opt/brickvault/current/manifest.json"),
    ]
    optional = [Path("/etc/brickvault/api.env"), Path("/etc/brickvault/caddy.env")]
    if any(not path.is_file() for path in required):
        raise BackupError("Required production recovery configuration is absent.")
    for path in (*required, *optional):
        if path.exists() and path != Path("/opt/brickvault/current/manifest.json"):
            _regular_root_file(path, (0o400, 0o600, 0o640))
    return tuple(
        str(path).lstrip("/") for path in (*required, *(p for p in optional if p.exists()))
    )


def stream_to_two(
    source_command: Sequence[str],
    sink_commands: Sequence[Sequence[str]],
    sink_environments: Sequence[Mapping[str, str]],
    *,
    deadline_seconds: float = STREAM_DEADLINE_SECONDS,
) -> tuple[int, str]:
    """Copy identical bounded chunks to both children; fail closed on any ambiguity."""
    if len(sink_commands) != 2 or len(sink_environments) != 2:
        raise BackupError("Exactly two backup destinations are required.")
    deadline = time.monotonic() + deadline_seconds
    source = subprocess.Popen(
        source_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env={"PATH": "/usr/bin:/bin", "HOME": "/root"},
    )
    sinks: list[subprocess.Popen[bytes]] = []
    errors: queue.Queue[BaseException] = queue.Queue()
    source_chunks: queue.Queue[bytes | None] = queue.Queue(maxsize=4)
    sink_chunks: list[queue.Queue[bytes | None]] = [queue.Queue(maxsize=4), queue.Queue(maxsize=4)]
    cancelled = threading.Event()

    def send(channel: queue.Queue[bytes | None], value: bytes | None) -> None:
        while not cancelled.is_set():
            try:
                channel.put(value, timeout=0.2)
                return
            except queue.Full:
                if time.monotonic() >= deadline:
                    raise BackupError("Backup stream timed out.") from None
        raise BackupError("Backup stream was cancelled.")

    def read_source() -> None:
        try:
            assert source.stdout is not None
            while not cancelled.is_set():
                chunk = source.stdout.read(CHUNK)
                if not chunk:
                    break
                send(source_chunks, chunk)
            if not cancelled.is_set():
                send(source_chunks, None)
        except BaseException as exc:
            errors.put(exc)
            cancelled.set()

    def write_sink(process: subprocess.Popen[bytes], channel: queue.Queue[bytes | None]) -> None:
        try:
            assert process.stdin is not None
            while not cancelled.is_set():
                try:
                    chunk = channel.get(timeout=0.2)
                except queue.Empty:
                    if time.monotonic() >= deadline:
                        raise BackupError("Backup stream timed out.") from None
                    continue
                if chunk is None:
                    break
                process.stdin.write(chunk)
                process.stdin.flush()
            process.stdin.close()
        except BaseException as exc:
            errors.put(exc)
            cancelled.set()

    threads: list[threading.Thread] = []
    try:
        for command, environment in zip(sink_commands, sink_environments, strict=True):
            sinks.append(
                subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=dict(environment),
                )
            )
        threads = [
            threading.Thread(target=read_source, daemon=True),
            *(
                threading.Thread(target=write_sink, args=(sink, channel), daemon=True)
                for sink, channel in zip(sinks, sink_chunks, strict=True)
            ),
        ]
        for thread in threads:
            thread.start()
        digest = hashlib.sha256()
        total = 0
        while True:
            if (
                not errors.empty()
                or time.monotonic() >= deadline
                or any(sink.poll() not in (None, 0) for sink in sinks)
            ):
                raise BackupError("Backup stream failed or timed out.")
            try:
                chunk = source_chunks.get(timeout=0.2)
            except queue.Empty:
                continue
            if chunk is None:
                break
            digest.update(chunk)
            total += len(chunk)
            for channel in sink_chunks:
                send(channel, chunk)
        for channel in sink_chunks:
            send(channel, None)
        for thread in threads:
            thread.join(timeout=max(0.1, min(30.0, deadline - time.monotonic())))
        if any(thread.is_alive() for thread in threads) or not errors.empty():
            raise BackupError("Backup stream workers did not finish.")
        if (
            source.wait(timeout=30) != 0
            or any(sink.wait(timeout=30) != 0 for sink in sinks)
            or total == 0
        ):
            raise BackupError("Backup source or destination failed.")
        return total, digest.hexdigest()
    except BaseException:
        cancelled.set()
        for process in (source, *sinks):
            if process.poll() is None:
                process.terminate()
        for process in (source, *sinks):
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        raise BackupError("Dual-destination backup did not complete.") from None
    finally:
        for thread in threads:
            thread.join(timeout=1)


def _restic(destination: Destination, *arguments: str, capture: bool = False) -> bytes:
    result = subprocess.run(
        destination.command(*arguments),
        env=destination.environment(),
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=STREAM_DEADLINE_SECONDS,
        check=False,
    )
    if result.returncode:
        raise BackupError("Encrypted repository operation failed.")
    return result.stdout if capture and isinstance(result.stdout, bytes) else b""


def _snapshot(destination: Destination, run_id: str, artifact: str) -> str:
    rows = json.loads(_restic(destination, "snapshots", "--json", "--tag", run_id, capture=True))
    matches = [
        row["id"]
        for row in rows
        if row.get("paths") == [f"/{run_id}/{artifact}"]
        or row.get("paths") == [f"{run_id}/{artifact}"]
    ]
    if len(matches) != 1 or SNAPSHOT_ID.fullmatch(matches[0]) is None:
        raise BackupError("Backup snapshot identity is ambiguous.")
    return matches[0]


def _readback(
    destination: Destination,
    snapshot: str,
    artifact: str,
    expected_size: int,
    expected_sha: str,
    run_id: str,
) -> None:
    if (
        SNAPSHOT_ID.fullmatch(snapshot) is None
        or RUN_ID.fullmatch(run_id) is None
        or artifact not in ARTIFACTS
    ):
        raise BackupError("Backup receipt identity is invalid.")
    process = subprocess.Popen(
        [
            TIMEOUT,
            "--signal=TERM",
            "--kill-after=10s",
            "4h",
            *destination.command("dump", snapshot, f"/{run_id}/{artifact}"),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        env=destination.environment(),
    )
    digest = hashlib.sha256()
    count = 0
    try:
        assert process.stdout is not None
        while chunk := process.stdout.read(CHUNK):
            digest.update(chunk)
            count += len(chunk)
        if (
            process.wait(timeout=120) != 0
            or count != expected_size
            or digest.hexdigest() != expected_sha
        ):
            raise BackupError("Encrypted readback digest differs.")
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)


def _receipt_path(run_id: str) -> Path:
    if RUN_ID.fullmatch(run_id) is None:
        raise BackupError("Backup run ID is invalid.")
    return RECEIPT_DIR / f"{run_id}.json"


def _proof_path(run_id: str) -> Path:
    if RUN_ID.fullmatch(run_id) is None:
        raise BackupError("Backup run ID is invalid.")
    return PROOF_DIR / f"{run_id}.json"


def _protected_output_dir(path: Path) -> None:
    path.mkdir(mode=0o700, exist_ok=True)
    for directory in (path, *path.parents):
        info = directory.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise BackupError("Protected backup output directory is unsafe.")
    if path.stat().st_mode & 0o077:
        raise BackupError("Protected backup output directory is too permissive.")


def _current_revisions(config: admin.AdminConfig) -> tuple[str, ...]:
    with admin._owner_connection(config) as owner:
        admin._schema_guard(owner)
        return admin._revisions(owner)


def backup() -> str:
    config = _preflight()
    revisions = _current_revisions(config)
    files = _configuration_files()
    run_id = _run_id()
    artifacts: dict[str, Any] = {}
    for artifact in ARTIFACTS:
        stream_name = f"{run_id}/{artifact}"
        commands = [
            destination.command(
                "backup", "--stdin", "--stdin-filename", stream_name, "--tag", run_id
            )
            for destination in DESTINATIONS
        ]
        size, sha = stream_to_two(
            _producer(artifact, files), commands, [d.environment() for d in DESTINATIONS]
        )
        snapshots = {
            destination.name: _snapshot(destination, run_id, artifact)
            for destination in DESTINATIONS
        }
        for destination in DESTINATIONS:
            _readback(destination, snapshots[destination.name], artifact, size, sha, run_id)
        artifacts[artifact] = {"bytes": size, "sha256": sha, "snapshots": snapshots}
    for destination in DESTINATIONS:
        _restic(destination, "check")
    if _current_revisions(config) != revisions:
        raise BackupError("Migration state changed during backup.")
    identities, _ = _validated_identity(
        admin._parse_json(admin._protected_file(BACKUP_DIR / "repositories.json"))
    )
    receipt: dict[str, Any] = {
        "schema": 2,
        "purpose": "production",
        "database": DATABASE,
        "ownership_marker": config.marker,
        "run_id": run_id,
        "revisions_at_backup": list(revisions),
        "verified_at_utc": datetime.now(UTC).isoformat(),
        "repositories": {
            d.name: {"uri": d.repository, "id": identities[d.name]} for d in DESTINATIONS
        },
        "artifacts": artifacts,
    }
    _protected_output_dir(RECEIPT_DIR)
    path = _receipt_path(run_id)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if not isinstance(nofollow, int):
        raise BackupError("Safe receipt creation is unavailable.")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        json.dump(receipt, output, sort_keys=True)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    return run_id


def verified_receipt(run_id: str) -> tuple[dict[str, Any], bytes]:
    """Read and verify one complete protected receipt against both repositories."""
    config = _preflight()
    raw = admin._protected_file(_receipt_path(run_id))
    receipt = dict(admin._parse_json(raw))
    identities, _ = _validated_identity(
        admin._parse_json(admin._protected_file(BACKUP_DIR / "repositories.json"))
    )
    repositories = {d.name: {"uri": d.repository, "id": identities[d.name]} for d in DESTINATIONS}
    if (
        set(receipt)
        != {
            "schema",
            "purpose",
            "database",
            "ownership_marker",
            "run_id",
            "revisions_at_backup",
            "verified_at_utc",
            "repositories",
            "artifacts",
        }
        or type(receipt["schema"]) is not int
        or receipt["schema"] != 2
        or receipt.get("purpose") != "production"
        or receipt.get("database") != DATABASE
        or receipt.get("ownership_marker") != config.marker
        or receipt.get("run_id") != run_id
        or type(receipt["revisions_at_backup"]) is not list
        or any(type(value) is not str for value in receipt["revisions_at_backup"])
        or tuple(receipt["revisions_at_backup"]) not in ((), admin.expected_revisions())
        or type(receipt["verified_at_utc"]) is not str
        or receipt.get("repositories") != repositories
        or type(receipt["artifacts"]) is not dict
        or set(receipt.get("artifacts", {})) != set(ARTIFACTS)
    ):
        raise BackupError("Backup receipt identity differs.")
    try:
        stamp = datetime.fromisoformat(receipt["verified_at_utc"])
    except ValueError as exc:
        raise BackupError("Backup receipt time is invalid.") from exc
    if stamp.tzinfo is None or stamp.utcoffset() != timedelta(0) or stamp > datetime.now(UTC):
        raise BackupError("Backup receipt time is invalid.")
    snapshot_ids: list[str] = []
    for artifact in ARTIFACTS:
        row = receipt["artifacts"][artifact]
        if (
            type(row) is not dict
            or set(row) != {"bytes", "sha256", "snapshots"}
            or type(row.get("bytes")) is not int
            or row["bytes"] <= 0
            or type(row["sha256"]) is not str
            or SNAPSHOT_ID.fullmatch(row["sha256"]) is None
            or type(row["snapshots"]) is not dict
            or set(row["snapshots"]) != {d.name for d in DESTINATIONS}
            or any(
                type(row["snapshots"][d.name]) is not str
                or SNAPSHOT_ID.fullmatch(row["snapshots"][d.name]) is None
                for d in DESTINATIONS
            )
        ):
            raise BackupError("Backup receipt artifact is invalid.")
        snapshot_ids.extend(row["snapshots"][d.name] for d in DESTINATIONS)
        for destination in DESTINATIONS:
            _readback(
                destination,
                row["snapshots"][destination.name],
                artifact,
                row["bytes"],
                row["sha256"],
                run_id,
            )
    if len(set(snapshot_ids)) != len(ARTIFACTS) * len(DESTINATIONS):
        raise BackupError("Backup snapshots are not independent.")
    for destination in DESTINATIONS:
        _restic(destination, "check")
    if admin._protected_file(_receipt_path(run_id)) != raw:
        raise BackupError("Backup receipt changed during verification.")
    return receipt, raw


def verify(run_id: str) -> None:
    verified_receipt(run_id)


def _proof_from_receipt(
    run_id: str, receipt: dict[str, Any], raw: bytes, revisions: tuple[str, ...], now: datetime
) -> dict[str, Any]:
    artifact_snapshots = {
        name: {
            destination.name: receipt["artifacts"][name]["snapshots"][destination.name]
            for destination in DESTINATIONS
        }
        for name in ARTIFACTS
    }
    return {
        "schema": 2,
        "purpose": "production",
        "database": DATABASE,
        "ownership_marker": receipt["ownership_marker"],
        "run_id": run_id,
        "backup_receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "revisions_at_backup": list(revisions),
        "repositories": receipt["repositories"],
        "artifact_snapshots": artifact_snapshots,
        "proxmox_snapshot": artifact_snapshots["database.dump"]["proxmox"],
        "drive_snapshot": artifact_snapshots["database.dump"]["drive"],
        "verified_at_utc": now.isoformat(),
    }


def _write_proof(run_id: str, proof: dict[str, Any]) -> Path:
    _protected_output_dir(PROOF_DIR)
    path = _proof_path(run_id)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if not isinstance(nofollow, int):
        raise BackupError("Safe recovery proof creation is unavailable.")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        json.dump(proof, output, sort_keys=True)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    return path


def finalize_proof(run_id: str) -> Path:
    """Create a protected admin proof only from fresh, fully verified copies."""
    receipt, raw = verified_receipt(run_id)
    config = admin._load_config(admin.CONFIG_PATH)
    now = datetime.now(UTC)
    backup_time = datetime.fromisoformat(receipt["verified_at_utc"])
    if not now - timedelta(hours=24) <= backup_time <= now:
        raise BackupError("Backup is too old for migration proof.")
    revisions = _current_revisions(config)
    if (
        receipt["ownership_marker"] != config.marker
        or tuple(receipt["revisions_at_backup"]) != revisions
    ):
        raise BackupError("Backup does not match current production revisions.")
    return _write_proof(run_id, _proof_from_receipt(run_id, receipt, raw, revisions, now))


def retention_plan(run_id: str) -> None:
    """Recheck a full run before any future retention policy is considered.

    Snapshot filenames contain the run ID, so restic's simple per-path forget
    grouping would keep every run. Deletion needs an explicit complete-run
    algorithm and remains outside the inactive P12-04B foundation.
    """
    verify(run_id)


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise BackupError("Invalid production backup command.")


def main(argv: list[str] | None = None) -> int:
    parser = _Parser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("backup")
    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("run_id")
    retain_parser = commands.add_parser("retention-plan")
    retain_parser.add_argument("run_id")
    proof_parser = commands.add_parser("finalize-proof")
    proof_parser.add_argument("run_id")
    try:
        args = parser.parse_args(argv)
        if args.command == "backup":
            print("Verified dual backup run: " + backup())
        elif args.command == "verify":
            verify(args.run_id)
            print("Both encrypted copies passed readback.")
        elif args.command == "retention-plan":
            retention_plan(args.run_id)
            print(
                "Verified run; proposed retention is 30 daily, 8 weekly, 12 monthly. No snapshots deleted."
            )
        elif args.command == "finalize-proof":
            print("Protected recovery proof created: " + str(finalize_proof(args.run_id)))
        return 0
    except Exception:  # noqa: BLE001 - no credentials, paths or driver errors in logs.
        print("Production backup refused; inspect protected local state.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
