"""Focused production catalog authority and exact source binding regressions."""

import hashlib
import json
import stat
import subprocess
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from uuid import UUID

import production_catalog as catalog
import pytest
from brickvault_api import production_admin as admin
from brickvault_api.catalog.connection import CatalogConnection
from brickvault_api.catalog.fingerprint import IMPORTER_VERSION
from brickvault_api.providers.rebrickable.source import Manifest, digest


def source_and_approval() -> tuple[Manifest, bytes, bytes]:
    path = (
        Path(__file__).resolve().parents[1]
        / "services/api/tests/fixtures/catalog/synthetic/initial/manifest.json"
    )
    data = json.loads(path.read_bytes())
    data.update(
        synthetic=False,
        source_version="official-reviewed-source",
        scope="full-catalog",
        profile_version="rebrickable-bulk-v3-2d.1",
        acquisition_method="offline-approved-acquisition",
    )
    for source in data["files"]:
        source.update(
            format="gzip",
            location=source["dataset"] + ".csv.gz",
            downloaded_at=data["acquired_end"],
            source_url="https://cdn.rebrickable.com/media/downloads/"
            + source["dataset"]
            + ".csv.gz",
        )
    manifest_raw = json.dumps(data).encode()
    manifest = Manifest.model_validate(data)
    approval = {
        "purpose": "production",
        "database": admin.DATABASE,
        "provider": "rebrickable",
        "synthetic": False,
        "scope": "full-catalog",
        "source_version": manifest.source_version,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "provenance_sha256": digest(manifest.provenance()),
        "importer_version": IMPORTER_VERSION,
        "permitted_use_reference": "https://rebrickable.com/downloads/",
        "rights_limitations": [
            "Private retained catalog with attribution; no AI training."
        ],
        "classification": "official-nonsynthetic",
        "known_set": catalog.KNOWN_SET,
    }
    return manifest, manifest_raw, json.dumps(approval).encode()


@pytest.mark.parametrize(
    "changes",
    [
        {"purpose": "development"},
        {"database": "brickvault_dev"},
        {"provider": "bricklink"},
        {"synthetic": True},
        {"synthetic": 0},
        {"classification": "fixture"},
        {"source_version": "other"},
        {"manifest_sha256": "0" * 64},
        {"provenance_sha256": "0" * 64},
        {"importer_version": "unknown"},
        {"scope": "subset"},
        {"known_set": "75331"},
        {"permitted_use_reference": "https://example.invalid/terms/"},
        {
            "permitted_use_reference": "https://rebrickable.com/downloads/?secret=sentinel"
        },
        {"rights_limitations": []},
        {"rights_limitations": ["bad\nrecord"]},
        {"extra": "field"},
    ],
)
def test_source_approval_rejects_changed_authority_or_digest(
    changes: dict[str, object],
) -> None:
    manifest, raw, approval_raw = source_and_approval()
    catalog.approve(approval_raw, manifest, raw)
    approval = json.loads(approval_raw)
    approval.update(changes)
    with pytest.raises(admin.AdminError):
        catalog.approve(json.dumps(approval).encode(), manifest, raw)


def test_first_import_refuses_partial_history() -> None:
    catalog.require_empty({"catalog_provider": 0, "catalog_set": 0})
    for count in (
        {"catalog_provider": 1, "catalog_set": 0},
        {"catalog_import_run": 1},
        {"catalog_stage_sets": 1},
    ):
        with pytest.raises(admin.AdminError):
            catalog.require_empty(count)


@pytest.mark.parametrize(
    "field",
    [
        "catalog_provider",
        "catalog_source_version",
        "catalog_source_file",
        "catalog_import_run",
        "catalog_snapshot",
        "catalog_snapshot_validation",
        "catalog_active_snapshot",
    ],
)
def test_activation_refuses_partial_or_competing_history_before_lookup(
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    counts = {
        "catalog_provider": 1,
        "catalog_source_version": 1,
        "catalog_source_file": 12,
        "catalog_import_run": 1,
        "catalog_snapshot": 1,
        "catalog_snapshot_validation": 1,
        "catalog_active_snapshot": 1,
        "catalog_set_fact": 1,
    }
    counts[field] += 2 if field == "catalog_import_run" else 1
    monkeypatch.setattr(catalog, "table_counts", lambda connection: counts)

    class Connection:
        def execute(self, *args: object) -> None:
            pytest.fail("Competing state must fail before candidate lookup.")

    manifest, _, _ = source_and_approval()
    with pytest.raises(admin.AdminError):
        catalog.candidate_guard(
            cast(CatalogConnection, Connection()),
            cast(catalog.ApprovedSource, SimpleNamespace(manifest=manifest)),
            UUID(int=1),
        )


@pytest.mark.parametrize(
    "args",
    [
        ["import", "--source", "private-path-secret"],
        ["activate", "--snapshot", "credential-sentinel"],
        [
            "recover-failed",
            "--run",
            "credential-sentinel",
            "--candidate",
            str(UUID(int=1)),
        ],
        ["retry-import", "--predecessor", "private-path-secret"],
        ["unknown"],
    ],
)
def test_bad_arguments_refuse_before_protected_input_and_redact(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: list[str],
) -> None:
    def fail(*args: object) -> None:
        pytest.fail("Invalid arguments reached protected configuration.")

    monkeypatch.setattr(catalog, "execute", fail)
    assert catalog.main(args) == 1
    output = capsys.readouterr()
    assert "private-path-secret" not in output.out + output.err
    assert "credential-sentinel" not in output.out + output.err


def test_import_uses_existing_importer_then_requires_validated_readback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events = []
    source = SimpleNamespace(area=object(), manifest=object())
    report = {
        "state": "passed",
        "candidate_snapshot": str(UUID(int=1)),
        "dataset_counts": {"sets": 1},
    }

    class Database:
        def __init__(self, *args: object) -> None:
            pass

        def connect(self) -> Any:
            return nullcontext(object())

    monkeypatch.setattr(
        admin,
        "_load_config",
        lambda path: SimpleNamespace(owner_url="private", marker="private"),
    )
    monkeypatch.setattr(catalog, "load_source", lambda: source)
    monkeypatch.setattr(catalog, "operations_lock", lambda: nullcontext())
    monkeypatch.setattr(
        catalog, "operations_guard", lambda *args: events.append("operations")
    )
    monkeypatch.setattr(admin, "verify", lambda config: events.append("verify"))
    monkeypatch.setattr(catalog, "CatalogDatabase", Database)
    monkeypatch.setattr(catalog, "table_counts", lambda connection: {"catalog_set": 0})

    def parse(current: object) -> dict[str, int]:
        events.append("parse")
        return {"sets": 1}

    def importer(*args: object) -> dict[str, Any]:
        events.append("import")
        return report

    monkeypatch.setattr(catalog, "parse_source", parse)
    monkeypatch.setattr(catalog, "import_source", importer)
    monkeypatch.setattr(
        catalog, "candidate_guard", lambda *args: events.append("readback")
    )
    assert catalog.execute("import") == report
    assert events == ["operations", "verify", "parse", "import", "readback"]


@pytest.mark.parametrize("command", ["recover-failed", "retry-import"])
def test_recovery_commands_bind_exact_attempt_after_source_and_admin_guards(
    monkeypatch: pytest.MonkeyPatch, command: str
) -> None:
    events: list[str] = []
    run, candidate = UUID(int=1), UUID(int=2)
    manifest, _, _ = source_and_approval()
    source = SimpleNamespace(area=object(), manifest=manifest)
    report = {
        "state": "passed",
        "candidate_snapshot": str(candidate),
        "dataset_counts": {"sets": 1},
    }

    class Connection:
        def transaction(self) -> Any:
            return nullcontext()

    class Database:
        def __init__(self, *args: object) -> None:
            assert args == ("private", "production", "private", "owner")

        def connect(self) -> Any:
            return nullcontext(Connection())

    monkeypatch.setattr(
        admin,
        "_load_config",
        lambda path: SimpleNamespace(owner_url="private", marker="private"),
    )
    monkeypatch.setattr(catalog, "load_source", lambda: source)
    monkeypatch.setattr(catalog, "operations_lock", lambda: nullcontext())
    monkeypatch.setattr(
        catalog, "operations_guard", lambda *args: events.append("operations")
    )
    monkeypatch.setattr(admin, "verify", lambda config: events.append("verify"))
    monkeypatch.setattr(catalog, "CatalogDatabase", Database)

    def parse(current: object) -> dict[str, int]:
        events.append("parse")
        assert current is source
        return {"sets": 1}

    def recover(*args: object) -> dict[str, Any]:
        events.append("recover")
        assert args[1:] == (manifest, {"sets": 1}, run, candidate)
        return {"state": "recovered_for_fresh_retry"}

    def admission(connection: object, current: Manifest, predecessor: UUID) -> None:
        events.append("admission")
        assert current is manifest and predecessor == run

    def importer(*args: object, **kwargs: object) -> dict[str, Any]:
        events.append("retry")
        assert args[1:] == (source.area, str(catalog.MANIFEST))
        assert kwargs == {"predecessor_id": run}
        return report

    monkeypatch.setattr(catalog, "parse_source", parse)
    monkeypatch.setattr(catalog, "recover_failed", recover)
    monkeypatch.setattr(catalog, "import_lock", lambda *args: nullcontext())
    monkeypatch.setattr(catalog, "admit_retry", admission)
    monkeypatch.setattr(catalog, "import_source", importer)
    monkeypatch.setattr(
        catalog, "candidate_guard", lambda *args: events.append("readback")
    )
    if command == "recover-failed":
        assert catalog.execute(command, run=run, candidate=candidate) == {
            "state": "recovered_for_fresh_retry"
        }
        assert events == ["operations", "verify", "parse", "recover"]
    else:
        assert catalog.execute(command, predecessor=run) == report
        assert events == [
            "operations",
            "verify",
            "admission",
            "parse",
            "retry",
            "readback",
        ]


def test_retry_refusal_precedes_source_parse_and_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Connection:
        def transaction(self) -> Any:
            return nullcontext()

    class Database:
        def __init__(self, *args: object) -> None:
            pass

        def connect(self) -> Any:
            return nullcontext(Connection())

    def refuse(*args: object) -> None:
        raise admin.AdminError("Recovered history is not exact.")

    def no_parse(*args: object) -> None:
        pytest.fail("Unrecovered retry reached parsing or importer.")

    monkeypatch.setattr(
        admin,
        "_load_config",
        lambda path: SimpleNamespace(owner_url="private", marker="private"),
    )
    monkeypatch.setattr(
        catalog, "load_source", lambda: SimpleNamespace(manifest=object())
    )
    monkeypatch.setattr(catalog, "operations_lock", lambda: nullcontext())
    monkeypatch.setattr(catalog, "operations_guard", lambda *args: None)
    monkeypatch.setattr(admin, "verify", lambda config: None)
    monkeypatch.setattr(catalog, "CatalogDatabase", Database)
    monkeypatch.setattr(catalog, "import_lock", lambda *args: nullcontext())
    monkeypatch.setattr(catalog, "admit_retry", refuse)
    monkeypatch.setattr(catalog, "parse_source", no_parse)
    monkeypatch.setattr(catalog, "import_source", no_parse)
    with pytest.raises(admin.AdminError):
        catalog.execute("retry-import", predecessor=UUID(int=1))


def test_operational_failure_never_prints_private_driver_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(*args: object) -> None:
        raise RuntimeError("private-path-secret credential-sentinel")

    monkeypatch.setattr(catalog, "execute", refuse)
    assert catalog.main(["retry-import", "--predecessor", str(UUID(int=1))]) == 1
    output = capsys.readouterr()
    assert "private-path-secret" not in output.out + output.err
    assert "credential-sentinel" not in output.out + output.err


def test_invalid_preparse_never_reaches_importer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = SimpleNamespace(
        manifest=SimpleNamespace(files=[SimpleNamespace(dataset="sets")]),
        area=object(),
        paths={"sets": Path("private")},
    )

    class IncompleteParser:
        complete = False

        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

        def rows(self) -> Any:
            return iter(())

    monkeypatch.setattr(catalog, "Parser", IncompleteParser)
    with pytest.raises(admin.AdminError, match="verified EOF"):
        catalog.parse_source(source)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        {"code": "synthetic-rebrickable"},
        {"synthetic": True},
        {"scope": "other"},
        {"manifest_digest": "0" * 64},
        {"source_version": "official-unreviewed"},
        {"status": "running"},
        {"state": "candidate"},
        {"generation": 1},
    ],
)
def test_candidate_identity_and_durable_state_must_match(
    monkeypatch: pytest.MonkeyPatch,
    changes: dict[str, object],
) -> None:
    manifest, _, _ = source_and_approval()
    counts = {
        "catalog_provider": 1,
        "catalog_source_version": 1,
        "catalog_source_file": 12,
        "catalog_import_run": 1,
        "catalog_snapshot": 1,
        "catalog_snapshot_validation": 1,
        "catalog_active_snapshot": 1,
        "catalog_set_fact": 1,
        "catalog_activation": 0,
    }
    row = {
        "code": "rebrickable",
        "synthetic": False,
        "scope": manifest.scope,
        "manifest_digest": digest(manifest.provenance()),
        "source_version": manifest.source_version,
        "status": "succeeded",
        "state": "validated",
        "stage": "validated",
        "snapshot_id": None,
        "generation": 0,
        "activation_id": None,
    }

    class Connection:
        def execute(self, *args: object) -> Any:
            return SimpleNamespace(fetchone=lambda: row)

    connection = Connection()
    source = SimpleNamespace(manifest=manifest)
    monkeypatch.setattr(catalog, "table_counts", lambda connection: counts)
    catalog.candidate_guard(connection, source, UUID(int=1))  # type: ignore[arg-type]
    row.update(changes)
    with pytest.raises(admin.AdminError):
        catalog.candidate_guard(connection, source, UUID(int=1))  # type: ignore[arg-type]


@pytest.mark.parametrize("changed", ["unbound", "fingerprint", "staging"])
def test_retry_candidate_requires_retired_predecessor_and_identical_semantics(
    monkeypatch: pytest.MonkeyPatch, changed: str
) -> None:
    manifest, _, _ = source_and_approval()
    table_counts = {
        "catalog_provider": 1,
        "catalog_source_version": 1,
        "catalog_source_file": 12,
        "catalog_import_run": 2,
        "catalog_snapshot": 1,
        "catalog_snapshot_validation": 1,
        "catalog_active_snapshot": 1,
        "catalog_set_fact": 1,
        "catalog_activation": 0,
    }
    row = {
        "code": "rebrickable",
        "synthetic": False,
        "scope": manifest.scope,
        "manifest_digest": digest(manifest.provenance()),
        "source_version": manifest.source_version,
        "source_version_id": UUID(int=2),
        "status": "succeeded",
        "state": "validated",
        "stage": "validated",
        "snapshot_id": None,
        "generation": 0,
        "activation_id": None,
        "predecessor_id": UUID(int=3),
        "semantic_fingerprint": "a" * 64,
    }
    staging = 0

    class Connection:
        def execute(self, query: object, *args: object) -> Any:
            result = {"n": staging} if "catalog_stage_" in str(query) else row
            return SimpleNamespace(fetchone=lambda: result)

    def prior(*args: object) -> dict[str, Any]:
        assert args[1:3] == (UUID(int=2), UUID(int=3))
        return {}

    monkeypatch.setattr(catalog, "table_counts", lambda connection: table_counts)
    monkeypatch.setattr(catalog, "failed_run", prior)
    monkeypatch.setattr(
        catalog,
        "metadata_guard",
        lambda *args: {"candidate": {"semantic_fingerprint": "a" * 64}},
    )
    connection = cast(CatalogConnection, Connection())
    source = cast(
        catalog.ApprovedSource,
        SimpleNamespace(manifest=manifest, paths={"sets": object()}),
    )
    catalog.candidate_guard(connection, source, UUID(int=1))
    if changed == "unbound":
        row["predecessor_id"] = None
    elif changed == "fingerprint":
        row["semantic_fingerprint"] = "b" * 64
    else:
        staging = 1
    with pytest.raises(admin.AdminError):
        catalog.candidate_guard(connection, source, UUID(int=1))


def test_committed_activation_recovery_requires_exact_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest, _, _ = source_and_approval()
    snapshot, receipt = UUID(int=1), UUID(int=2)
    counts = {
        "catalog_provider": 1,
        "catalog_source_version": 1,
        "catalog_source_file": 12,
        "catalog_import_run": 1,
        "catalog_snapshot": 1,
        "catalog_snapshot_validation": 1,
        "catalog_active_snapshot": 1,
        "catalog_set_fact": 1,
        "catalog_activation": 1,
    }
    row = {
        "code": "rebrickable",
        "synthetic": False,
        "scope": manifest.scope,
        "manifest_digest": digest(manifest.provenance()),
        "source_version": manifest.source_version,
        "status": "succeeded",
        "state": "accepted",
        "stage": "accepted",
        "snapshot_id": snapshot,
        "generation": 1,
        "activation_id": receipt,
    }

    class Connection:
        def execute(self, *args: object) -> Any:
            return SimpleNamespace(fetchone=lambda: row)

    monkeypatch.setattr(catalog, "table_counts", lambda connection: counts)
    connection, source = Connection(), SimpleNamespace(manifest=manifest)
    catalog.candidate_guard(connection, source, snapshot, receipt)  # type: ignore[arg-type]
    for supplied in (None, UUID(int=3)):
        with pytest.raises(admin.AdminError):
            catalog.candidate_guard(connection, source, snapshot, supplied)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "changes",
    [
        {"st_nlink": 2},
        {"st_uid": 1},
        {"st_mode": stat.S_IFREG | 0o644},
        {"st_mode": stat.S_IFLNK | 0o600},
    ],
)
def test_protected_source_rejects_links_other_owner_and_public_read(
    monkeypatch: pytest.MonkeyPatch,
    changes: dict[str, int],
) -> None:
    path = Path("/protected/source.json")
    file_info = {"st_mode": stat.S_IFREG | 0o600, "st_uid": 0, "st_nlink": 1}
    file_info.update(changes)

    def info(current: Path) -> Any:
        return (
            SimpleNamespace(**file_info)
            if current == path
            else SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o755,
                st_uid=0,
            )
        )

    monkeypatch.setattr(Path, "lstat", info)
    with pytest.raises(admin.AdminError):
        catalog.protected_source_file(path)


def test_changed_installed_manifest_refuses_before_job_checks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest, _, _ = source_and_approval()
    monkeypatch.setattr(
        Path,
        "resolve",
        lambda path, **kwargs: (
            catalog.RELEASE if path.name == "current" else catalog.RELEASE / "api/venv"
        ),
    )
    monkeypatch.setattr(Path, "read_bytes", lambda path: b"changed release manifest")
    monkeypatch.setattr(catalog, "protected_source_file", lambda *args: None)
    monkeypatch.setattr(admin, "_protected_file", lambda *args: b"protected")
    monkeypatch.setattr(catalog, "approve_repair_release", lambda *args: "a" * 64)
    monkeypatch.setattr(
        catalog, "expected_revisions", lambda: ("0016_hunt_cached_runs",)
    )

    def no_job(*args: object, **kwargs: object) -> None:
        pytest.fail("Changed release must stop before job inspection or import.")

    monkeypatch.setattr(subprocess, "run", no_job)
    with pytest.raises(admin.AdminError, match="release or migration"):
        catalog.operations_guard(
            "retry-import",
            cast(catalog.ApprovedSource, SimpleNamespace(manifest=manifest)),
        )


@pytest.mark.parametrize("command", ["recover-failed", "retry-import", "activate"])
def test_release_bridge_refuses_wrong_current_before_job_checks(
    monkeypatch: pytest.MonkeyPatch, command: str
) -> None:
    manifest, _, _ = source_and_approval()
    expected = (
        catalog.PREDECESSOR_RELEASE if command == "recover-failed" else catalog.RELEASE
    )
    wrong = (
        catalog.RELEASE if command == "recover-failed" else catalog.PREDECESSOR_RELEASE
    )
    current = expected
    monkeypatch.setattr(catalog, "protected_source_file", lambda *args: None)
    monkeypatch.setattr(admin, "_protected_file", lambda *args: b"protected")
    reviewed = hashlib.sha256(b"repaired manifest").hexdigest()
    monkeypatch.setattr(catalog, "approve_repair_release", lambda *args: reviewed)
    monkeypatch.setattr(
        Path,
        "resolve",
        lambda path, **kwargs: (
            current if path.name == "current" else catalog.RELEASE / "api/venv"
        ),
    )
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda path: (
            b"predecessor manifest"
            if path.parent == catalog.PREDECESSOR_RELEASE
            else b"repaired manifest"
        ),
    )
    monkeypatch.setattr(
        catalog,
        "PREDECESSOR_MANIFEST_SHA256",
        hashlib.sha256(b"predecessor manifest").hexdigest(),
    )
    monkeypatch.setattr(
        catalog, "expected_revisions", lambda: ("0016_hunt_cached_runs",)
    )
    jobs: list[object] = []

    def inactive(*args: object, **kwargs: object) -> Any:
        jobs.append(args)
        return SimpleNamespace(returncode=0, stdout=b"inactive\n")

    monkeypatch.setattr(subprocess, "run", inactive)
    source = cast(catalog.ApprovedSource, SimpleNamespace(manifest=manifest))
    catalog.operations_guard(command, source)
    assert len(jobs) == len(catalog.CONFLICT_UNITS)
    jobs.clear()
    current = wrong
    with pytest.raises(admin.AdminError, match="release or migration"):
        catalog.operations_guard(command, source)
    assert not jobs


@pytest.mark.parametrize(
    "field",
    [
        "purpose",
        "database",
        "release_id",
        "predecessor_release_id",
        "predecessor_release_manifest_sha256",
        "source_version",
        "source_manifest_sha256",
        "source_provenance_sha256",
        "migration_head",
        "release_manifest_sha256",
        "extra",
    ],
)
def test_detached_repair_release_approval_binds_exact_authority_and_source(
    monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    manifest, raw, _ = source_and_approval()
    monkeypatch.setattr(catalog, "SOURCE_VERSION", manifest.source_version)
    monkeypatch.setattr(
        catalog, "SOURCE_MANIFEST_SHA256", hashlib.sha256(raw).hexdigest()
    )
    monkeypatch.setattr(
        catalog, "SOURCE_PROVENANCE_SHA256", digest(manifest.provenance())
    )
    descriptor = {
        "purpose": "production",
        "database": admin.DATABASE,
        "release_id": catalog.RELEASE.name,
        "predecessor_release_id": catalog.PREDECESSOR_RELEASE.name,
        "predecessor_release_manifest_sha256": catalog.PREDECESSOR_MANIFEST_SHA256,
        "source_version": catalog.SOURCE_VERSION,
        "source_manifest_sha256": catalog.SOURCE_MANIFEST_SHA256,
        "source_provenance_sha256": catalog.SOURCE_PROVENANCE_SHA256,
        "migration_head": "0016_hunt_cached_runs",
        "release_manifest_sha256": "a" * 64,
    }
    assert (
        catalog.approve_repair_release(json.dumps(descriptor).encode(), manifest, raw)
        == "a" * 64
    )
    descriptor[field] = "changed"
    with pytest.raises(admin.AdminError):
        catalog.approve_repair_release(json.dumps(descriptor).encode(), manifest, raw)
