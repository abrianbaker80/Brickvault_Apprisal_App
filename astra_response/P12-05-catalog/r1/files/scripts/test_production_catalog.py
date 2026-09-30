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
    counts[field] += 1
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
        catalog, "operations_guard", lambda: events.append("operations")
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
    monkeypatch.setattr(
        Path,
        "resolve",
        lambda path, **kwargs: (
            catalog.RELEASE if path.name == "current" else catalog.RELEASE / "api/venv"
        ),
    )
    monkeypatch.setattr(Path, "read_bytes", lambda path: b"changed release manifest")
    monkeypatch.setattr(
        catalog, "expected_revisions", lambda: ("0016_hunt_cached_runs",)
    )

    def no_job(*args: object, **kwargs: object) -> None:
        pytest.fail("Changed release must stop before job inspection or import.")

    monkeypatch.setattr(subprocess, "run", no_job)
    with pytest.raises(admin.AdminError, match="release or migration"):
        catalog.operations_guard()
