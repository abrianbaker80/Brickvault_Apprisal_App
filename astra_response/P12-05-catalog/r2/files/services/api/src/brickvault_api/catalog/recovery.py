"""Exact failed-first-import retirement, retaining truthful attempt provenance."""

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from psycopg import sql
from psycopg.types.json import Jsonb

from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.catalog.fingerprint import fingerprint
from brickvault_api.catalog.models import CATALOG_TABLES
from brickvault_api.catalog.ownership import import_lock
from brickvault_api.providers.rebrickable.records import PROFILES, SourceError
from brickvault_api.providers.rebrickable.source import Manifest, digest

RECOVERY_VERSION = "catalog-failed-retirement-v1"
RECOVERY_STRATEGY = "retire-and-fresh-retry"
BASE_COUNTS = {
    "catalog_provider": 1,
    "catalog_source_version": 1,
    "catalog_source_file": 12,
    "catalog_import_run": 1,
    "catalog_active_snapshot": 1,
}


def counts(connection: CatalogConnection) -> dict[str, int]:
    result = {}
    for name in CATALOG_TABLES:
        row = connection.execute(
            sql.SQL("SELECT count(*) AS n FROM public.{}").format(sql.Identifier(name))
        ).fetchone()
        if row is None:
            raise SourceError("recovery_counts_unavailable")
        result[name] = row["n"]
    return result


def validate_counts(value: object) -> dict[str, int]:
    if (
        not isinstance(value, dict)
        or set(value) != set(PROFILES)
        or any(type(n) is not int or n < 0 for n in value.values())
    ):
        raise SourceError("recovery_source_counts_invalid")
    return dict(value)


def expected_state(actual: dict[str, int], datasets: dict[str, int], *, candidate: bool) -> None:
    expected = dict(BASE_COUNTS)
    if candidate:
        expected["catalog_snapshot"] = 1
        expected.update({"catalog_stage_" + name: n for name, n in datasets.items()})
    if set(actual) != set(CATALOG_TABLES) or any(
        n != expected.get(name, 0) for name, n in actual.items()
    ):
        raise SourceError("recovery_state_not_exact")


def source_guard(connection: CatalogConnection, manifest: Manifest) -> UUID:
    if (
        manifest.synthetic
        or manifest.provider != "rebrickable"
        or manifest.scope != "full-catalog"
        or not manifest.source_version.startswith("official-")
    ):
        raise SourceError("recovery_official_source_required")
    source = connection.execute(
        """SELECT v.*,p.code FROM catalog_source_version v
        JOIN catalog_provider p ON p.id=v.provider_id"""
    ).fetchall()
    if len(source) != 1:
        raise SourceError("recovery_source_not_exact")
    row = source[0]
    if (
        row["code"] != "rebrickable"
        or row["synthetic"] is not False
        or row["scope"] != manifest.scope
        or row["manifest_digest"] != digest(manifest.provenance())
        or row["source_metadata"] != manifest.provenance()
    ):
        raise SourceError("recovery_source_not_exact")
    files = connection.execute(
        "SELECT * FROM catalog_source_file WHERE source_version_id=%s", (row["id"],)
    ).fetchall()
    wanted = {item.dataset: item for item in manifest.files}
    if len(files) != 12 or {item["dataset_name"] for item in files} != set(wanted):
        raise SourceError("recovery_files_not_exact")
    for item in files:
        source_file = wanted[item["dataset_name"]]
        if any(
            item[field] != getattr(source_file, field)
            for field in (
                "compressed_sha256",
                "decompressed_sha256",
                "compressed_bytes",
                "decompressed_bytes",
                "encoding",
                "source_url",
            )
        ) or item["headers"] != list(source_file.headers):
            raise SourceError("recovery_files_not_exact")
    pointer = connection.execute("SELECT * FROM catalog_active_snapshot").fetchall()
    if (
        len(pointer) != 1
        or pointer[0]["provider_id"] != row["provider_id"]
        or pointer[0]["scope"] != manifest.scope
        or pointer[0]["snapshot_id"] is not None
        or pointer[0]["generation"] != 0
        or pointer[0]["activation_id"] is not None
    ):
        raise SourceError("recovery_pointer_not_empty")
    return UUID(str(row["id"]))


def failed_run(
    connection: CatalogConnection, source_id: UUID, run_id: UUID, manifest: Manifest
) -> dict[str, Any]:
    run = connection.execute(
        "SELECT * FROM catalog_import_run WHERE id=%s FOR UPDATE", (run_id,)
    ).fetchone()
    if (
        run is None
        or run["source_version_id"] != source_id
        or run["predecessor_id"] is not None
        or run["status"] != "failed"
        or run["stage"] != "failed"
        or run["failure_category"] != "database_failure"
        or run["finished_at"] is None
        or run["parser_version"] != manifest.profile_version
        or run["importer_version"] != "offline-catalog-2d.2"
        or run["application_version"] != "phase-2b"
        or not isinstance(run["counts"], dict)
        or "datasets" not in run["counts"]
    ):
        raise SourceError("recovery_failed_run_not_exact")
    validate_counts(run["counts"]["datasets"])
    return run


def metadata_guard(run: dict[str, Any], manifest: Manifest) -> dict[str, Any]:
    recovery = run["counts"].get("recovery")
    fields = {
        "version",
        "strategy",
        "candidate",
        "source_manifest_digest",
        "source_version",
        "staging_counts",
        "recovered_at",
    }
    if (
        set(run["counts"]) != {"datasets", "recovery"}
        or not isinstance(recovery, dict)
        or set(recovery) != fields
        or recovery["version"] != RECOVERY_VERSION
        or recovery["strategy"] != RECOVERY_STRATEGY
        or recovery["source_manifest_digest"] != digest(manifest.provenance())
        or recovery["source_version"] != manifest.source_version
        or validate_counts(recovery["staging_counts"]) != validate_counts(run["counts"]["datasets"])
    ):
        raise SourceError("recovery_metadata_not_exact")
    candidate = recovery["candidate"]
    if (
        not isinstance(candidate, dict)
        or set(candidate)
        != {
            "id",
            "semantic_fingerprint",
            "source_version_id",
            "scope",
            "created_at",
        }
        or candidate["scope"] != manifest.scope
        or candidate["source_version_id"] != str(run["source_version_id"])
    ):
        raise SourceError("recovery_metadata_not_exact")
    try:
        UUID(candidate["id"])
        fingerprint = candidate["semantic_fingerprint"]
        if (
            not isinstance(fingerprint, str)
            or len(fingerprint) != 64
            or any(char not in "0123456789abcdef" for char in fingerprint)
        ):
            raise ValueError
        for value in (candidate["created_at"], recovery["recovered_at"]):
            if type(value) is not str:
                raise ValueError
            parsed = datetime.fromisoformat(value)
            if parsed.utcoffset() != timedelta(0):
                raise ValueError
        for value in (run["started_at"], run["finished_at"]):
            if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
                raise ValueError
        created = datetime.fromisoformat(candidate["created_at"])
        if not run["started_at"] <= created <= run["finished_at"]:
            raise ValueError
        if datetime.fromisoformat(recovery["recovered_at"]) < run["finished_at"]:
            raise ValueError
    except (KeyError, TypeError, ValueError, AttributeError):
        raise SourceError("recovery_metadata_not_exact") from None
    return recovery


def admit_retry(connection: CatalogConnection, manifest: Manifest, predecessor_id: UUID) -> None:
    """Caller holds the exclusive provider import lock; admission writes nothing."""
    source_id = source_guard(connection, manifest)
    run = failed_run(connection, source_id, predecessor_id, manifest)
    metadata_guard(run, manifest)
    expected_state(counts(connection), validate_counts(run["counts"]["datasets"]), candidate=False)


def require_retry_fingerprint(
    connection: CatalogConnection,
    manifest: Manifest,
    predecessor_id: UUID,
    semantic_fingerprint: str,
) -> None:
    """After staging, a linked retry must retain the retired candidate semantics."""
    source_id = source_guard(connection, manifest)
    run = failed_run(connection, source_id, predecessor_id, manifest)
    prior = metadata_guard(run, manifest)
    if semantic_fingerprint != prior["candidate"]["semantic_fingerprint"]:
        raise SourceError("recovery_retry_fingerprint_not_exact")


def recover_failed(
    database: CatalogDatabase,
    manifest: Manifest,
    verified_counts: dict[str, int],
    run_id: UUID,
    candidate_id: UUID,
) -> dict[str, Any]:
    """Retire one empty candidate/staging atomically; never rewrite failure truth."""
    if database.role != "owner" or database.purpose not in ("production", "test"):
        raise SourceError("recovery_owner_context_required")
    datasets = validate_counts(verified_counts)
    with (
        database.connect() as connection,
        import_lock(connection, "rebrickable"),
        connection.transaction(),
    ):
        source_id = source_guard(connection, manifest)
        run = failed_run(connection, source_id, run_id, manifest)
        if (
            set(run["counts"]) != {"datasets"}
            or validate_counts(run["counts"]["datasets"]) != datasets
        ):
            raise SourceError("recovery_failed_run_not_exact")
        expected_state(counts(connection), datasets, candidate=True)
        candidate = connection.execute(
            "SELECT * FROM catalog_snapshot WHERE id=%s FOR UPDATE", (candidate_id,)
        ).fetchone()
        if (
            candidate is None
            or candidate["import_run_id"] != run_id
            or candidate["source_version_id"] != source_id
            or candidate["state"] != "candidate"
            or candidate["validation_digest"] is not None
            or candidate["scope"] != manifest.scope
        ):
            raise SourceError("recovery_candidate_not_exact")
        for dataset, expected in datasets.items():
            row = connection.execute(
                sql.SQL(
                    "SELECT count(*) AS n FROM public.{} WHERE run_id=%s AND source_version_id=%s AND source_file_id=(SELECT id FROM catalog_source_file WHERE source_version_id=%s AND dataset_name=%s)"
                ).format(sql.Identifier("catalog_stage_" + dataset)),
                (run_id, source_id, source_id, dataset),
            ).fetchone()
            if row is None or row["n"] != expected:
                raise SourceError("recovery_staging_not_exact")
        if candidate["semantic_fingerprint"] != fingerprint(
            connection, run_id, manifest, run["importer_version"]
        ):
            raise SourceError("recovery_fingerprint_not_exact")
        recovery = {
            "version": RECOVERY_VERSION,
            "strategy": RECOVERY_STRATEGY,
            "candidate": {
                "id": str(candidate_id),
                "semantic_fingerprint": candidate["semantic_fingerprint"],
                "source_version_id": str(source_id),
                "scope": candidate["scope"],
                "created_at": candidate["created_at"].astimezone(UTC).isoformat(),
            },
            "source_manifest_digest": digest(manifest.provenance()),
            "source_version": manifest.source_version,
            "staging_counts": datasets,
            "recovered_at": datetime.now(UTC).isoformat(),
        }
        updated = connection.execute(
            "UPDATE catalog_import_run SET counts=%s WHERE id=%s AND status='failed' AND stage='failed' AND failure_category='database_failure'",
            (Jsonb({**run["counts"], "recovery": recovery}), run_id),
        )
        if updated.rowcount != 1:
            raise SourceError("recovery_failed_run_not_exact")
        for dataset, expected in datasets.items():
            removed = connection.execute(
                sql.SQL("DELETE FROM public.{} WHERE run_id=%s").format(
                    sql.Identifier("catalog_stage_" + dataset)
                ),
                (run_id,),
            )
            if removed.rowcount != expected:
                raise SourceError("recovery_staging_not_exact")
        removed_candidate = connection.execute(
            "DELETE FROM catalog_snapshot WHERE id=%s AND import_run_id=%s AND state='candidate' AND validation_digest IS NULL",
            (candidate_id, run_id),
        )
        if removed_candidate.rowcount != 1:
            raise SourceError("recovery_candidate_not_exact")
        admit_retry(connection, manifest, run_id)
        return {
            "state": "recovered_for_fresh_retry",
            "predecessor_id": str(run_id),
            "retired_staging_counts": datasets,
            "failed_status_preserved": True,
        }
