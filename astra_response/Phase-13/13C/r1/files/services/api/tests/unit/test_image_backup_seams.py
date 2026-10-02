"""Bounded new recovery-format, real filesystem and service failure seams."""

import copy
import hashlib
import io
import json
import os
import sys
import tarfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from brickvault_api import backup_format as fmt
from brickvault_api import image_backup as images
from brickvault_api import production_admin as admin
from brickvault_api import production_backup as backup
from brickvault_api.images.storage import FilesystemBlobStore, ImageError

NOW = datetime.now(UTC)
REPOS = {
    d: {"uri": "synthetic:" + d, "id": hashlib.sha256(d.encode()).hexdigest()}
    for d in ("proxmox", "drive")
}
MARKER = "brickvault-appraisal:" + "1" * 32 + ":" + "2" * 32


def receipt(schema: int = 3) -> dict[str, Any]:
    revisions = [fmt.IMAGE_REVISION if schema == 3 else fmt.LEGACY_REVISION]
    names = fmt.required_artifacts(schema, revisions)
    return {
        "schema": schema,
        "purpose": "production",
        "database": admin.DATABASE,
        "ownership_marker": MARKER,
        "run_id": "a" * 32,
        "revisions_at_backup": revisions,
        "verified_at_utc": (NOW - timedelta(seconds=5)).isoformat(),
        "repositories": REPOS,
        "artifacts": {
            n: {
                "bytes": 10,
                "sha256": "b" * 64,
                "snapshots": {d: hashlib.sha256((n + d).encode()).hexdigest() for d in REPOS},
            }
            for n in names
        },
    }


def proof_check(monkeypatch: pytest.MonkeyPatch, schema: int) -> None:
    r = receipt(schema)
    raw = json.dumps(r).encode()
    proof = backup._proof_from_receipt(r["run_id"], r, raw, tuple(r["revisions_at_backup"]), NOW)
    monkeypatch.setattr(admin, "_protected_file", lambda _p: json.dumps(proof).encode())
    monkeypatch.setattr(backup, "verified_receipt", lambda _r: (r, raw))
    cfg = admin.AdminConfig("unused-owner", "unused-runtime", MARKER)
    admin._recovery_proof(backup._proof_path(r["run_id"]), cfg, tuple(r["revisions_at_backup"]))
    admin._recovery_proof(backup._proof_path(r["run_id"]), cfg, None)
    with pytest.raises(admin.AdminError):
        admin._recovery_proof(backup._proof_path(r["run_id"]), cfg, ("unexpected",))


def test_legacy_proof_remains_exact_during_approved_transition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    r = receipt(2)
    assert fmt.validate_receipt(r["run_id"], r, REPOS, MARKER, NOW) == fmt.LEGACY_ARTIFACTS
    proof_check(monkeypatch, 2)
    r["revisions_at_backup"] = [fmt.IMAGE_REVISION]
    with pytest.raises(ValueError):
        fmt.validate_receipt(r["run_id"], r, REPOS, MARKER, NOW)


def test_combined_proof_requires_all_four_artifacts(monkeypatch: pytest.MonkeyPatch) -> None:
    r = receipt()
    assert fmt.validate_receipt(r["run_id"], r, REPOS, MARKER, NOW) == fmt.IMAGE_ARTIFACTS
    proof_check(monkeypatch, 3)
    r["artifacts"].pop("image-blobs.tar")
    with pytest.raises(ValueError):
        fmt.validate_receipt(r["run_id"], r, REPOS, MARKER, NOW)


def test_malformed_unknown_or_incomplete_copies_fail_closed() -> None:
    bad = []
    r = receipt()
    r["schema"] = 4
    bad.append(r)
    r = receipt()
    r["artifacts"]["image-blobs.tar"]["snapshots"].pop("drive")
    bad.append(r)
    r = receipt()
    r["artifacts"]["image-blobs.tar"]["sha256"] = "broken"
    bad.append(r)
    r = receipt()
    r["artifacts"]["image-blobs.tar"]["snapshots"] = r["artifacts"]["database.dump"]["snapshots"]
    bad.append(r)
    r = receipt()
    r["optional_images"] = True
    bad.append(r)
    for r in bad:
        with pytest.raises(ValueError):
            fmt.validate_receipt(r["run_id"], r, REPOS, MARKER, NOW)


def fixture_archive(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, dict[str, Any]]:
    root = tmp_path / "source"
    store = FilesystemBlobStore(root)
    blobs = [store.publish(b"original fixture"), store.publish(b"thumbnail fixture")]
    value = {
        "schema": 1,
        "revisions": [fmt.IMAGE_REVISION],
        "database": {
            "counts": {"blob": 2},
            "security": {},
            "context": {},
            "objects": [],
            "image_tables": {},
            "blobs": [
                {"sha256": b.sha256, "storage_key": b.key, "byte_count": b.byte_count}
                for b in blobs
            ],
        },
    }
    inventory = tmp_path / "inventory.json"
    inventory.write_bytes(images.canonical(value))
    out = io.BytesIO()
    monkeypatch.setattr(images.sys, "stdout", SimpleNamespace(buffer=out))
    images.write_archive(inventory, root)
    archive = tmp_path / "images.tar"
    archive.write_bytes(out.getvalue())
    return archive, root, value


def test_real_blob_archive_roundtrip_and_missing_corrupt_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, root, value = fixture_archive(tmp_path, monkeypatch)
    destination = tmp_path / "recovered"
    assert images.extract_archive(archive, destination) == value
    for row in value["database"]["blobs"]:
        assert (destination / row["storage_key"]).read_bytes() == (
            root / row["storage_key"]
        ).read_bytes()
    blob = root / value["database"]["blobs"][0]["storage_key"]
    blob.write_bytes(b"corrupt")
    with pytest.raises(ImageError):
        images.write_archive(tmp_path / "inventory.json", root)
    blob.unlink()
    with pytest.raises(ImageError):
        images.write_archive(tmp_path / "inventory.json", root)


def test_archive_rejects_path_escape_links_missing_and_duplicate_members(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, _root, value = fixture_archive(tmp_path, monkeypatch)
    with tarfile.open(archive) as source:
        members = [(m, source.extractfile(m).read()) for m in source.getmembers()]
    for n, mode in enumerate(("escape", "link", "missing", "duplicate", "corrupt")):
        altered = tmp_path / f"bad-{n}.tar"
        with tarfile.open(altered, "w") as target:
            for member, data in members:
                if mode == "missing" and member.name != "inventory.json":
                    continue
                member = copy.copy(member)
                if member.name != "inventory.json" and mode == "escape":
                    member.name = "../escaped"
                if member.name != "inventory.json" and mode == "link":
                    member.type = tarfile.SYMTYPE
                    member.linkname = "../escaped"
                if member.name != "inventory.json" and mode == "corrupt":
                    data = b"x" * len(data)
                target.addfile(member, io.BytesIO(data) if member.isfile() else None)
            if mode == "duplicate":
                target.addfile(members[0][0], io.BytesIO(members[0][1]))
        with pytest.raises(ValueError):
            images.extract_archive(altered, tmp_path / f"target-{n}")
    assert not (tmp_path / "escaped").exists()
    assert len(value["database"]["blobs"]) == 2


def test_mixed_receipts_retention_keeps_complete_artifact_set_and_pins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scripts = Path(__file__).resolve().parents[5] / "scripts"
    monkeypatch.syspath_prepend(str(scripts))
    import complete_run_retention as retention

    legacy = receipt(2)
    new = receipt(3)
    retention.validate_receipt(legacy["run_id"], legacy, REPOS, MARKER, NOW)
    retention.validate_receipt(new["run_id"], new, REPOS, MARKER, NOW)
    # Planner binds every actual artifact and protects two historical permanent pins.
    new["run_id"] = "c" * 32
    extra = copy.deepcopy(legacy)
    extra["run_id"] = "d" * 32
    for n, r in enumerate((legacy, extra, new)):
        r["verified_at_utc"] = (NOW - timedelta(days=400 + n)).isoformat()
        for a, row in r["artifacts"].items():
            row["snapshots"] = {
                d: hashlib.sha256((r["run_id"] + a + d).encode()).hexdigest() for d in REPOS
            }
    receipts = {r["run_id"]: r for r in (legacy, extra, new)}
    snapshots = {
        d: [
            {"id": row["snapshots"][d], "paths": [f"/{run}/{a}"], "tags": [run]}
            for run, r in receipts.items()
            for a, row in r["artifacts"].items()
        ]
        for d in REPOS
    }
    canaries = {}
    for d in REPOS:
        row = {
            "id": hashlib.sha256((d + "canary").encode()).hexdigest(),
            "paths": ["/canary"],
            "tags": ["canary"],
        }
        snapshots[d].append(row)
        canaries[d] = {row["id"]: retention.digest(row)}
    pins = {
        "schema": 1,
        "repositories": REPOS,
        "runs": {r["run_id"]: retention.digest(r) for r in (legacy, extra)},
        "canaries": canaries,
    }
    ledger = {"schema": 1, "status": "READY", "deleted": {}, "last_transaction": None}
    before = images.canonical(pins)
    plan = retention.make_plan(receipts, REPOS, MARKER, snapshots, pins, ledger, NOW)
    assert set(pins["runs"]) <= set(plan["keep"])
    assert images.canonical(pins) == before
    snapshots["drive"] = [
        r
        for r in snapshots["drive"]
        if r["id"] != new["artifacts"]["image-blobs.tar"]["snapshots"]["drive"]
    ]
    with pytest.raises(retention.RetentionError):
        retention.make_plan(receipts, REPOS, MARKER, snapshots, pins, ledger, NOW)


def test_pause_restores_prior_state_after_capture_or_stop_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(os, "O_NOFOLLOW", getattr(os, "O_NOFOLLOW", 0), raising=False)
    monkeypatch.setattr(admin, "_require_root", lambda: None)
    monkeypatch.setattr(images, "STATE", tmp_path / "pause")
    monkeypatch.setattr(images, "JOURNAL", tmp_path / "pause/pause.json")
    monkeypatch.setattr(admin, "_protected_file", lambda p: p.read_bytes())
    # Windows lacks POSIX owner/mode checks; preserve all remaining real journal/finally behavior.
    real_lstat = Path.lstat

    def info(p: Path) -> Any:
        r = real_lstat(p)
        if p == images.STATE:
            return SimpleNamespace(st_mode=0o40700, st_uid=0)
        return r

    monkeypatch.setattr(Path, "lstat", info)
    for stop_fails in (False, True):
        calls = []

        def control(
            *args: str, calls: list[tuple[str, ...]] = calls, stop_fails: bool = stop_fails
        ) -> str:
            calls.append(args)
            if args[0] == "show":
                if "--property=MainPID" in args:
                    return "0"
                return "active" if args[1] in images.UNITS else "inactive"
            if stop_fails and args[:2] == ("stop", "brickvault-api.service"):
                raise RuntimeError("synthetic stop failure")
            return ""

        monkeypatch.setattr(images, "systemctl", control)
        with pytest.raises(RuntimeError):
            with images.maintenance_pause():
                raise RuntimeError("synthetic capture failure")
        assert [a[1] for a in calls if a[0] == "start"] == list(reversed(images.UNITS))
        assert not images.JOURNAL.exists()


def test_new_artifact_stream_requires_both_destinations(tmp_path: Path) -> None:
    source = [sys.executable, "-c", "import sys;sys.stdout.buffer.write(b'image artifact')"]
    sink = [
        sys.executable,
        "-c",
        "import sys;from pathlib import Path;Path(sys.argv[1]).write_bytes(sys.stdin.buffer.read())",
        str(tmp_path / "copy"),
    ]
    failed = [sys.executable, "-c", "import sys;sys.stdin.buffer.read();sys.exit(2)"]
    with pytest.raises(backup.BackupError):
        backup.stream_to_two(source, [sink, failed], [dict(), dict()], deadline_seconds=20)
