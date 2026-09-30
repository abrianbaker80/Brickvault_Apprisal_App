"""Exact-state recovery admission without database or provider access."""

import copy
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from uuid import UUID

import pytest

from brickvault_api.catalog import recovery
from brickvault_api.catalog.connection import CatalogConnection
from brickvault_api.catalog.models import CATALOG_TABLES
from brickvault_api.catalog.recovery import (
    BASE_COUNTS,
    RECOVERY_STRATEGY,
    RECOVERY_VERSION,
    expected_state,
    metadata_guard,
    require_retry_fingerprint,
    validate_counts,
)
from brickvault_api.providers.rebrickable.records import PROFILES, SourceError
from brickvault_api.providers.rebrickable.source import Manifest, digest


def example_manifest(catalog_bundle: Path) -> Manifest:
    value = json.loads((catalog_bundle / "initial/manifest.json").read_bytes())
    value.update(
        synthetic=False,
        source_version="official-recovery-fixture",
        scope="full-catalog",
        acquisition_method="offline-approved-acquisition",
        profile_version="rebrickable-bulk-v3-2d.1",
    )
    for item in value["files"]:
        item.update(format="gzip")
    return Manifest.model_validate(value)


@pytest.mark.parametrize("table", CATALOG_TABLES)
def test_any_unexpected_catalog_row_refuses_retirement(table: str) -> None:
    datasets = {name: 2 for name in PROFILES}
    actual = {name: BASE_COUNTS.get(name, 0) for name in CATALOG_TABLES}
    actual["catalog_snapshot"] = 1
    actual.update({"catalog_stage_" + name: n for name, n in datasets.items()})
    expected_state(actual, datasets, candidate=True)
    actual[table] += 1
    with pytest.raises(SourceError, match="recovery_state_not_exact"):
        expected_state(actual, datasets, candidate=True)


@pytest.mark.parametrize(
    "changed",
    [
        "catalog_snapshot",
        "catalog_stage_sets",
        "catalog_import_run",
        "catalog_activation",
        "catalog_snapshot_validation",
        "catalog_set",
    ],
)
def test_recovered_retry_state_rejects_candidate_staging_or_extra_attempt(changed: str) -> None:
    actual = {name: BASE_COUNTS.get(name, 0) for name in CATALOG_TABLES}
    datasets = {name: 2 for name in PROFILES}
    expected_state(actual, datasets, candidate=False)
    actual[changed] += 1
    with pytest.raises(SourceError, match="recovery_state_not_exact"):
        expected_state(actual, datasets, candidate=False)


@pytest.mark.parametrize(
    "value",
    [
        {},
        {"sets": 1},
        {name: True for name in PROFILES},
        {name: -1 for name in PROFILES},
        {name: "1" for name in PROFILES},
    ],
)
def test_source_counts_reject_missing_coerced_and_negative_values(value: object) -> None:
    with pytest.raises(SourceError, match="recovery_source_counts_invalid"):
        validate_counts(value)


def audit_example(manifest: Manifest) -> dict[str, Any]:
    finished = datetime(2026, 9, 30, tzinfo=UTC)
    source_id = UUID(int=2)
    datasets = {name: 2 for name in PROFILES}
    return {
        "source_version_id": source_id,
        "started_at": finished - timedelta(minutes=2),
        "finished_at": finished,
        "counts": {
            "datasets": datasets,
            "recovery": {
                "version": RECOVERY_VERSION,
                "strategy": RECOVERY_STRATEGY,
                "candidate": {
                    "id": str(UUID(int=3)),
                    "semantic_fingerprint": "a" * 64,
                    "source_version_id": str(source_id),
                    "scope": manifest.scope,
                    "created_at": (finished - timedelta(minutes=1)).isoformat(),
                },
                "source_manifest_digest": digest(manifest.provenance()),
                "source_version": manifest.source_version,
                "staging_counts": datasets,
                "recovered_at": (finished + timedelta(seconds=1)).isoformat(),
            },
        },
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("version", "unknown"),
        ("strategy", "resume"),
        ("source_manifest_digest", "0" * 64),
        ("source_version", "other"),
        ("recovered_at", "2026-09-29T00:00:00+00:00"),
        ("recovered_at", "2026-09-30T00:00:00"),
        ("staging_counts", {name: 3 for name in PROFILES}),
    ],
)
def test_retirement_receipt_binds_source_counts_strategy_and_time(
    catalog_bundle: Path,
    field: str,
    value: object,
) -> None:
    manifest = example_manifest(catalog_bundle)
    audit = audit_example(manifest)
    metadata_guard(audit, manifest)
    changed = copy.deepcopy(audit)
    changed["counts"]["recovery"][field] = value
    with pytest.raises(SourceError):
        metadata_guard(changed, manifest)


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", "invalid"),
        ("semantic_fingerprint", "A" * 64),
        ("source_version_id", str(UUID(int=5))),
        ("scope", "other"),
        ("created_at", "2026-09-29T00:00:00+00:00"),
        ("created_at", "2026-09-30T00:00:01+00:00"),
        ("created_at", "2026-09-29T23:59:00"),
        ("created_at", "2026-09-29T23:59:00+01:00"),
    ],
)
def test_retired_candidate_receipt_refuses_changed_identity_fingerprint_or_time(
    catalog_bundle: Path, field: str, value: object
) -> None:
    manifest = example_manifest(catalog_bundle)
    audit = audit_example(manifest)
    audit["counts"]["recovery"]["candidate"][field] = value
    with pytest.raises(SourceError):
        metadata_guard(audit, manifest)


def test_retry_fingerprint_matches_retired_audit_before_build(
    catalog_bundle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = example_manifest(catalog_bundle)
    audit = audit_example(manifest)
    monkeypatch.setattr(recovery, "source_guard", lambda *args: UUID(int=2))
    monkeypatch.setattr(recovery, "failed_run", lambda *args: audit)
    connection = cast(CatalogConnection, object())
    require_retry_fingerprint(connection, manifest, UUID(int=1), "a" * 64)
    with pytest.raises(SourceError, match="recovery_retry_fingerprint_not_exact"):
        require_retry_fingerprint(connection, manifest, UUID(int=1), "b" * 64)
