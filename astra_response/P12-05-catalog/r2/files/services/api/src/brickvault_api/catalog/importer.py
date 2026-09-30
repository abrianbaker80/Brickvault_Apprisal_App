"""Explicit offline import. Successful validation never implicitly activates."""

import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb

from brickvault_api.catalog.build_steps import BuildInspector, BuildSteps
from brickvault_api.catalog.builder import build_candidate
from brickvault_api.catalog.candidate_validation import validate_candidate
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.catalog.fingerprint import IMPORTER_VERSION, VALIDATION_VERSION, fingerprint
from brickvault_api.catalog.ownership import import_lock, reconcile_runs
from brickvault_api.catalog.staged_validation import bundle_checks
from brickvault_api.providers.rebrickable.parser import DEFAULT_LIMITS, Limits, Parser
from brickvault_api.providers.rebrickable.records import PROFILE_STATUS, PROFILES, SourceError
from brickvault_api.providers.rebrickable.source import Manifest, SourceArea, digest, load_manifest
from brickvault_api.publication import auxiliary_progress

Progress = Callable[[dict[str, Any]], None]
Checkpoint = Callable[[str], None]


def quiet_progress(event: dict[str, Any]) -> None:
    pass


def no_checkpoint(stage: str) -> None:
    pass


def provider_code(manifest: Manifest) -> str:
    return "synthetic-rebrickable" if manifest.synthetic else manifest.provider


def create_source(
    connection: CatalogConnection, manifest: Manifest
) -> tuple[UUID, UUID, dict[str, UUID]]:
    code = provider_code(manifest)
    provider = connection.execute(
        "SELECT id FROM catalog_provider WHERE code=%s", (code,)
    ).fetchone()
    provider_id = provider["id"] if provider else uuid4()
    if not provider:
        connection.execute(
            "INSERT INTO catalog_provider(id,code,name,documentation_url,use_policy_reference) VALUES(%s,%s,%s,%s,%s)",
            (
                provider_id,
                code,
                code,
                "https://rebrickable.com/downloads/",
                "ExecPlan 020; fixture-only 2B evidence"
                if manifest.synthetic
                else "docs/PHASE_2D_PROVIDER_GATE.md; 2026-09-09 official metadata policy; Rebrickable attribution; no AI training",
            ),
        )
    # Acquisition identity is distinct from the catalog's semantic fingerprint.
    provenance = manifest.provenance()
    manifest_digest = digest(provenance)
    conflict = connection.execute(
        """SELECT manifest_digest FROM catalog_source_version
        WHERE provider_id=%s AND scope=%s AND source_metadata->>'source_version'=%s
        AND (source_metadata->'files' IS DISTINCT FROM %s OR source_metadata->>'profile_version'<>%s) LIMIT 1""",
        (
            provider_id,
            manifest.scope,
            manifest.source_version,
            Jsonb(provenance["files"]),
            manifest.profile_version,
        ),
    ).fetchone()
    if conflict:
        raise SourceError("source_version_conflict")
    existing = connection.execute(
        "SELECT id FROM catalog_source_version WHERE provider_id=%s AND manifest_digest=%s",
        (provider_id, manifest_digest),
    ).fetchone()
    source_id = existing["id"] if existing else uuid4()
    if not existing:
        connection.execute(
            """INSERT INTO catalog_source_version(id,provider_id,manifest_digest,acquired_start,acquired_end,released_at,scope,source_metadata,synthetic)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                source_id,
                provider_id,
                manifest_digest,
                manifest.acquired_start,
                manifest.acquired_end,
                manifest.released_at,
                manifest.scope,
                Jsonb(provenance),
                manifest.synthetic,
            ),
        )
        for source in manifest.files:
            connection.execute(
                """INSERT INTO catalog_source_file(id,source_version_id,dataset_name,resource_identity,source_url,compressed_sha256,decompressed_sha256,compressed_bytes,decompressed_bytes,headers,encoding,schema_metadata,http_metadata,downloaded_at)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    uuid4(),
                    source_id,
                    source.dataset,
                    source.dataset + ".csv",
                    source.source_url or "",
                    source.compressed_sha256,
                    source.decompressed_sha256,
                    source.compressed_bytes,
                    source.decompressed_bytes,
                    Jsonb(source.headers),
                    source.encoding,
                    Jsonb(
                        {
                            "profile_version": manifest.profile_version,
                            "status": PROFILE_STATUS
                            if manifest.synthetic
                            else "OFFICIAL SOURCE PROFILE VERIFIED; CATALOG ACCEPTANCE PENDING",
                            "format": source.format,
                        }
                    ),
                    Jsonb(
                        {
                            "acquisition_method": manifest.acquisition_method,
                            **(source.http_metadata or {}),
                        }
                    ),
                    source.downloaded_at or manifest.acquired_end,
                ),
            )
    files = connection.execute(
        "SELECT id,dataset_name FROM catalog_source_file WHERE source_version_id=%s", (source_id,)
    ).fetchall()
    connection.execute(
        """INSERT INTO catalog_active_snapshot(provider_id,scope,snapshot_id,generation,activation_id)
        VALUES(%s,%s,NULL,0,NULL) ON CONFLICT DO NOTHING""",
        (provider_id, manifest.scope),
    )
    return provider_id, source_id, {row["dataset_name"]: row["id"] for row in files}


def stage_dataset(
    connection: CatalogConnection,
    parser: Parser,
    run_id: UUID,
    source_id: UUID,
    file_id: UUID,
    progress: Progress,
    checkpoint: Checkpoint,
    *,
    batch_size: int = 10000,
) -> int:
    profile = PROFILES[parser.source.dataset]
    names = (
        "run_id",
        "source_file_id",
        "source_version_id",
        "row_number",
        "evidence_id",
        "reserved_id",
        "reserved_provider_id",
        "native_key",
        "native_values",
        "semantic_values",
        "diagnostics",
        "row_sha256",
        *profile.names,
    )
    statement = sql.SQL("COPY {} ({}) FROM STDIN").format(
        sql.Identifier("catalog_stage_" + profile.dataset),
        sql.SQL(",").join(map(sql.Identifier, names)),
    )
    iterator = iter(parser.rows())
    exhausted = False
    try:
        while not exhausted:
            with connection.transaction(), connection.cursor().copy(statement) as copy:
                for _ in range(batch_size):
                    row = next(iterator, None)
                    if row is None:
                        exhausted = True
                        break
                    copy.write_row(
                        (
                            run_id,
                            file_id,
                            source_id,
                            row.row_number,
                            uuid4(),
                            uuid4(),
                            uuid4(),
                            Jsonb(row.native_key),
                            Jsonb(row.raw),
                            Jsonb(row.values),
                            Jsonb(list(row.ignored)),
                            digest(row.raw),
                            *(row.values[name] for name in profile.names),
                        )
                    )
                    if parser.count == 1:
                        checkpoint("copy_first_row")
            if not exhausted:
                progress(
                    {
                        "stage": "rows_staged",
                        "dataset": profile.dataset,
                        "rows": parser.count,
                        "run_id": str(run_id),
                    }
                )
                checkpoint("staging_batch_committed")
    finally:
        iterator.close()
    if not parser.complete:
        raise SourceError("incomplete_parser", profile.dataset)
    return parser.count


def import_source(
    database: CatalogDatabase,
    area: SourceArea,
    location: str,
    *,
    progress: Progress = quiet_progress,
    checkpoint: Checkpoint = no_checkpoint,
    importer_version: str = IMPORTER_VERSION,
    limits: Limits = DEFAULT_LIMITS,
    build_inspector: BuildInspector | None = None,
    predecessor_id: UUID | None = None,
) -> dict[str, Any]:
    manifest, paths = load_manifest(area, location)
    return import_manifest(
        database,
        area,
        manifest,
        paths,
        progress=progress,
        checkpoint=checkpoint,
        importer_version=importer_version,
        limits=limits,
        build_inspector=build_inspector,
        predecessor_id=predecessor_id,
    )


def import_manifest(
    database: CatalogDatabase,
    area: SourceArea,
    manifest: Manifest,
    paths: dict[str, Path],
    *,
    progress: Progress,
    checkpoint: Checkpoint,
    importer_version: str,
    limits: Limits,
    build_inspector: BuildInspector | None = None,
    predecessor_id: UUID | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    progress = auxiliary_progress(progress)
    run_id = uuid4()
    counts: dict[str, int] = {}
    candidate: UUID | None = None
    created = False
    if database.role != "owner":
        raise SourceError("owner_context_required")
    with database.connect() as connection, import_lock(connection, provider_code(manifest)):
        if predecessor_id is None:
            reconcile_runs(connection, provider_code(manifest))

        def event(stage: str, **extra: Any) -> None:
            progress(
                {
                    "run_id": str(run_id),
                    "stage": stage,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    **extra,
                }
            )

        def state(expected: str, stage: str) -> None:
            changed = connection.execute(
                "UPDATE catalog_import_run SET stage=%s,counts=%s WHERE id=%s AND stage=%s AND status='running'",
                (stage, Jsonb(counts), run_id, expected),
            )
            if changed.rowcount != 1:
                raise SourceError("invalid_import_transition")

        def finish(stage: str, result_counts: dict[str, Any]) -> None:
            expected, status, failure = {
                "no_op": ("validating", "no_op", None),
                "validated": ("validating_candidate", "succeeded", None),
                "failed": ("validating_candidate", "failed", "candidate_validation"),
            }[stage]
            changed = connection.execute(
                """UPDATE catalog_import_run SET stage=%s,status=%s,failure_category=%s,
                finished_at=clock_timestamp(),counts=%s WHERE id=%s AND stage=%s AND status='running'""",
                (stage, status, failure, Jsonb(result_counts), run_id, expected),
            )
            if changed.rowcount != 1:
                raise SourceError("invalid_import_transition")

        try:
            with connection.transaction():
                if predecessor_id is not None:
                    # Admission and new-run provenance share the exclusive provider
                    # lock and transaction; a wrapper-only check can become stale.
                    from brickvault_api.catalog.recovery import admit_retry

                    admit_retry(connection, manifest, predecessor_id)
                provider, source, files = create_source(connection, manifest)
                connection.execute(
                    """INSERT INTO catalog_import_run(id,source_version_id,parser_version,importer_version,application_version,stage,status,started_at,counts,predecessor_id)
                    VALUES(%s,%s,%s,%s,'phase-2b','created','running',%s,'{}',%s)""",
                    (
                        run_id,
                        source,
                        manifest.profile_version,
                        importer_version,
                        datetime.now(UTC),
                        predecessor_id,
                    ),
                )
            created = True
            event("source_validated")
            state("created", "staging")
            for source_file in manifest.files:
                event("dataset_staging_started", dataset=source_file.dataset)
                parser = Parser(
                    area,
                    source_file,
                    paths[source_file.dataset],
                    synthetic=manifest.synthetic,
                    limits=limits,
                )
                counts[source_file.dataset] = stage_dataset(
                    connection,
                    parser,
                    run_id,
                    source,
                    files[source_file.dataset],
                    progress,
                    checkpoint,
                )
                # Each run adds a new, initially unseen run_id distribution.
                # Reference validation must not plan against the prior run's
                # statistics or depend on asynchronous autovacuum timing.
                connection.execute(
                    sql.SQL("ANALYZE {}").format(
                        sql.Identifier("catalog_stage_" + source_file.dataset)
                    )
                )
                state("staging", "staging")
                event("dataset_staging_completed", dataset=source_file.dataset, rows=parser.count)
                checkpoint("dataset_staged:" + source_file.dataset)
            state("staging", "validating")
            event("bundle_validation_started")
            with connection.transaction():
                bundle = bundle_checks(connection, run_id, counts)
                semantic = fingerprint(connection, run_id, manifest, importer_version)
                if predecessor_id is not None:
                    from .recovery import require_retry_fingerprint

                    require_retry_fingerprint(connection, manifest, predecessor_id, semantic)
            event("bundle_validation_completed")
            existing = connection.execute(
                "SELECT id,state FROM catalog_snapshot WHERE semantic_fingerprint=%s AND state IN ('validated','accepted')",
                (semantic,),
            ).fetchone()
            if existing:
                finish("no_op", {"datasets": counts, "reused_snapshot": str(existing["id"])})
                return {
                    "run_id": str(run_id),
                    "stage": "no_op",
                    "candidate_snapshot": str(existing["id"]),
                    "dataset_counts": counts,
                }
            candidate = uuid4()
            with connection.transaction():
                connection.execute(
                    """INSERT INTO catalog_snapshot(id,import_run_id,source_version_id,semantic_fingerprint,state,scope,created_at)
                    VALUES(%s,%s,%s,%s,'candidate',%s,clock_timestamp())""",
                    (candidate, run_id, source, semantic, manifest.scope),
                )
                state("validating", "building")
            event("candidate_build_started", candidate_snapshot=str(candidate))
            prior = connection.execute(
                "SELECT snapshot_id FROM catalog_active_snapshot WHERE provider_id=%s AND scope=%s",
                (provider, manifest.scope),
            ).fetchone()
            with connection.transaction():
                identities = build_candidate(
                    connection,
                    run_id,
                    source,
                    candidate,
                    provider,
                    provider_code(manifest),
                    prior["snapshot_id"] if prior else None,
                    checkpoint,
                    progress=progress,
                    inspector=build_inspector,
                )
            # This shared fact table has just received the committed candidate.
            # Missing snapshot/evidence statistics made ownership validation
            # materialize and repeatedly scan the entire official inventory.
            # Refresh this measured relation before validation can cache a plan;
            # historical facts and all planner/timeout settings stay unchanged.
            with connection.transaction():
                BuildSteps(
                    connection,
                    run_id,
                    candidate,
                    progress,
                    build_inspector,
                    phase="candidate_statistics",
                ).execute("inventory_line_statistics", "ANALYZE catalog_inventory_line")
            state("building", "validating_candidate")
            event("candidate_build_completed")
            checkpoint("before_candidate_validation")
            with connection.transaction():
                # Exclude concurrent candidate writers until validation/freeze commits.
                connection.execute(
                    "SELECT id FROM catalog_snapshot WHERE id=%s FOR UPDATE", (candidate,)
                )
                report = validate_candidate(
                    connection,
                    run_id,
                    candidate,
                    manifest,
                    counts,
                    identities,
                    bundle,
                    progress=progress,
                    inspector=build_inspector,
                )
                connection.execute(
                    """INSERT INTO catalog_snapshot_validation(snapshot_id,rules_version,digest,state,report,created_at)
                    VALUES(%s,%s,%s,%s,%s,clock_timestamp())""",
                    (
                        candidate,
                        VALIDATION_VERSION,
                        report["digest"],
                        report["state"],
                        Jsonb(report),
                    ),
                )
                if report["state"] == "passed":
                    connection.execute(
                        "UPDATE catalog_snapshot SET state='validated',validation_digest=%s WHERE id=%s",
                        (report["digest"], candidate),
                    )
                    finish("validated", {"datasets": counts, "canonical_identities": identities})
                else:
                    finish("failed", {"datasets": counts})
            event("validation_completed", state=report["state"], candidate_snapshot=str(candidate))
            if report["state"] == "passed":
                event("snapshot_validated", candidate_snapshot=str(candidate))
            return report
        except BaseException as error:
            category = (
                error.category
                if isinstance(error, SourceError)
                else "interrupted"
                if isinstance(error, (KeyboardInterrupt, SystemExit))
                else "database_failure"
                if isinstance(error, psycopg.Error)
                else "import_failure"
            )
            if created and not connection.closed:
                # A committed terminal result is authoritative even if its acknowledgement was lost.
                try:
                    connection.execute(
                        "UPDATE catalog_import_run SET stage=%s,status=%s,failure_category=%s,finished_at=clock_timestamp(),counts=%s WHERE id=%s AND status='running'",
                        (
                            "interrupted" if category == "interrupted" else "failed",
                            "interrupted" if category == "interrupted" else "failed",
                            category,
                            Jsonb({"datasets": counts}),
                            run_id,
                        ),
                    )
                except psycopg.Error:
                    # The next exclusive owner reconciles the durable database state.
                    connection.close()
            if isinstance(error, (KeyboardInterrupt, SystemExit)):
                raise
            if isinstance(error, SourceError):
                raise
            raise SourceError(category) from None


def cleanup_staging(database: CatalogDatabase, run_id: UUID) -> dict[str, int]:
    """Library maintenance primitive; exact terminal run only, no broad cleanup CLI."""
    if database.role != "owner":
        raise SourceError("owner_context_required")
    with database.connect() as connection:
        owner = connection.execute(
            """SELECT p.code FROM catalog_import_run r JOIN catalog_source_version s ON s.id=r.source_version_id JOIN catalog_provider p ON p.id=s.provider_id WHERE r.id=%s""",
            (run_id,),
        ).fetchone()
        if not owner:
            raise SourceError("unknown_run")
        with import_lock(connection, owner["code"]), connection.transaction():
            run = connection.execute(
                "SELECT status FROM catalog_import_run WHERE id=%s FOR UPDATE", (run_id,)
            ).fetchone()
            if not run or run["status"] not in ("failed", "interrupted", "no_op", "succeeded"):
                raise SourceError("run_not_terminal")
            return {
                dataset: connection.execute(
                    sql.SQL("DELETE FROM {} WHERE run_id=%s").format(
                        sql.Identifier("catalog_stage_" + dataset)
                    ),
                    (run_id,),
                ).rowcount
                for dataset in PROFILES
            }
