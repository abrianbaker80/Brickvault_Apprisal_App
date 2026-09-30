"""Real PostgreSQL failure retirement and source-bound fresh retry qualification."""

import gzip
import hashlib
import json
from pathlib import Path
from uuid import UUID

import psycopg
import pytest
from psycopg import sql
from psycopg.types.json import Jsonb

from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.catalog.fingerprint import IMPORTER_VERSION
from brickvault_api.catalog.importer import import_source
from brickvault_api.catalog.models import CATALOG_TABLES
from brickvault_api.catalog.ownership import import_lock
from brickvault_api.catalog.promotion import activate
from brickvault_api.catalog.recovery import admit_retry, counts, recover_failed
from brickvault_api.providers.rebrickable.parser import Parser
from brickvault_api.providers.rebrickable.records import SourceError
from brickvault_api.providers.rebrickable.source import Manifest, SourceArea, load_manifest


def durable_state(connection: CatalogConnection) -> dict[str, list[str]]:
    """Compare every catalog row/value; fixture bytes stay inside TEST assertions."""
    return {
        name: sorted(
            json.dumps(row["value"], sort_keys=True)
            for row in connection.execute(
                sql.SQL("SELECT to_jsonb(t) AS value FROM public.{} t").format(sql.Identifier(name))
            ).fetchall()
        )
        for name in CATALOG_TABLES
    }


def recovery_fixture(
    database: CatalogDatabase,
    root: Path,
) -> tuple[SourceArea, Manifest, dict[str, int], UUID, UUID]:
    """Fixture bytes model official manifest shape only in an owned TEST target."""
    path = root / "initial/manifest.json"
    value = json.loads(path.read_bytes())
    value.update(
        synthetic=False,
        source_version="official-recovery-fixture",
        scope="full-catalog",
        profile_version="rebrickable-bulk-v3-2d.1",
        acquisition_method="offline-approved-acquisition",
    )
    for item in value["files"]:
        raw = (path.parent / item["location"]).read_bytes()
        compressed = gzip.compress(raw, mtime=0)
        item.update(
            location=item["dataset"] + ".csv.gz",
            format="gzip",
            compressed_bytes=len(compressed),
            decompressed_bytes=len(raw),
            compressed_sha256=hashlib.sha256(compressed).hexdigest(),
            decompressed_sha256=hashlib.sha256(raw).hexdigest(),
            source_url="https://cdn.rebrickable.com/media/downloads/" + item["dataset"] + ".csv.gz",
            downloaded_at=value["acquired_end"],
        )
        (path.parent / item["location"]).write_bytes(compressed)
    path.write_text(json.dumps(value), encoding="utf-8")
    area = SourceArea(root)
    manifest, paths = load_manifest(area, str(path))
    datasets = {}
    for item in manifest.files:
        parser = Parser(area, item, paths[item.dataset], synthetic=False)
        list(parser.rows())
        assert parser.complete
        datasets[item.dataset] = parser.count

    def fail(stage: str) -> None:
        if stage == "identities_reconciled":
            raise psycopg.OperationalError("Disposable candidate construction failure")

    with pytest.raises(SourceError, match="database_failure"):
        import_source(database, area, str(path), checkpoint=fail)
    with database.connect() as connection:
        run = connection.execute("SELECT id FROM catalog_import_run").fetchone()
        candidate = connection.execute("SELECT id,state FROM catalog_snapshot").fetchone()
        assert run and candidate and candidate["state"] == "candidate"
    return area, manifest, datasets, run["id"], candidate["id"]


def test_retirement_preserves_failure_audit_and_exact_fresh_retry(
    catalog_db: CatalogDatabase,
    catalog_bundle: Path,
) -> None:
    area, manifest, datasets, run_id, candidate_id = recovery_fixture(catalog_db, catalog_bundle)
    with catalog_db.connect() as connection:
        original = connection.execute(
            "SELECT * FROM catalog_import_run WHERE id=%s", (run_id,)
        ).fetchone()
        old_candidate = connection.execute("SELECT * FROM catalog_snapshot").fetchone()
        assert original and old_candidate
        with import_lock(connection, "rebrickable"), connection.transaction():
            with pytest.raises(SourceError, match="recovery_metadata_not_exact"):
                admit_retry(connection, manifest, run_id)
    result = recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
    assert result["state"] == "recovered_for_fresh_retry"
    with catalog_db.connect() as connection:
        retired = connection.execute(
            "SELECT * FROM catalog_import_run WHERE id=%s", (run_id,)
        ).fetchone()
        assert retired
        assert {k: v for k, v in retired.items() if k != "counts"} == {
            k: v for k, v in original.items() if k != "counts"
        }
        assert retired["counts"]["datasets"] == original["counts"]["datasets"]
        assert retired["counts"]["recovery"]["candidate"]["id"] == str(candidate_id)
        assert (
            retired["counts"]["recovery"]["candidate"]["semantic_fingerprint"]
            == old_candidate["semantic_fingerprint"]
        )
        current = counts(connection)
        assert current["catalog_snapshot"] == 0
        assert all(n == 0 for name, n in current.items() if name.startswith("catalog_stage_"))
    with pytest.raises(SourceError):
        recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
    report = import_source(
        catalog_db, area, str(catalog_bundle / "initial/manifest.json"), predecessor_id=run_id
    )
    assert report["state"] == "passed" and report["dataset_counts"] == datasets
    with catalog_db.connect() as connection:
        fresh_candidate = connection.execute(
            "SELECT semantic_fingerprint FROM catalog_snapshot"
        ).fetchone()
        assert (
            fresh_candidate
            and fresh_candidate["semantic_fingerprint"] == old_candidate["semantic_fingerprint"]
        )
        rows = connection.execute(
            "SELECT id,status,stage,predecessor_id FROM catalog_import_run ORDER BY started_at"
        ).fetchall()
        assert len(rows) == 2
        assert rows[0] == {
            "id": run_id,
            "status": "failed",
            "stage": "failed",
            "predecessor_id": None,
        }
        assert rows[1]["predecessor_id"] == run_id and rows[1]["status"] == "succeeded"
        assert connection.execute("SELECT state FROM catalog_snapshot").fetchone() == {
            "state": "validated"
        }
        assert connection.execute("SELECT count(*) AS n FROM catalog_activation").fetchone() == {
            "n": 0
        }
        with import_lock(connection, "rebrickable"), connection.transaction():
            with pytest.raises(SourceError):
                admit_retry(connection, manifest, run_id)
    receipt_id = UUID(int=123)
    assert (
        activate(catalog_db, UUID(report["candidate_snapshot"]), None, 0, receipt_id)["state"]
        == "committed"
    )
    with catalog_db.connect() as connection:
        pointer = connection.execute("SELECT * FROM catalog_active_snapshot").fetchone()
        assert pointer and pointer["generation"] == 1
        assert pointer["snapshot_id"] == UUID(report["candidate_snapshot"])
        assert pointer["activation_id"] == receipt_id
        assert counts(connection)["catalog_activation"] == 1
        before = durable_state(connection)
    # The schema requires activation receipt and active pointer to commit together.
    with pytest.raises(SourceError, match="recovery_pointer_not_empty"):
        recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
    with catalog_db.connect() as connection:
        assert durable_state(connection) == before


@pytest.mark.parametrize(
    "mutation",
    [
        "wrong_source",
        "wrong_counts",
        "wrong_candidate",
        "validated",
        "accepted",
        "competing_attempt",
        "extra_provider",
        "extra_evidence",
        "extra_identity",
        "changed_stage",
        "changed_staging_counts",
        "wrong_staging_file",
    ],
)
def test_changed_failed_state_refuses_without_audit_mutation(
    catalog_db: CatalogDatabase,
    catalog_bundle: Path,
    mutation: str,
) -> None:
    _, manifest, datasets, run_id, candidate_id = recovery_fixture(catalog_db, catalog_bundle)
    supplied_manifest, supplied_counts, supplied_candidate = manifest, datasets, candidate_id
    with catalog_db.connect() as connection:
        if mutation == "wrong_source":
            supplied_manifest = manifest.model_copy(update={"source_version": "official-other"})
        elif mutation == "wrong_counts":
            supplied_counts = {**datasets, "sets": datasets["sets"] + 1}
        elif mutation == "wrong_candidate":
            supplied_candidate = UUID(int=1)
        elif mutation in ("validated", "accepted"):
            connection.execute(
                "UPDATE catalog_snapshot SET state='validated',validation_digest=%s", ("0" * 64,)
            )
            if mutation == "accepted":
                connection.execute("UPDATE catalog_snapshot SET state='accepted'")
        elif mutation == "competing_attempt":
            connection.execute(
                """INSERT INTO catalog_import_run(id,source_version_id,parser_version,importer_version,
                application_version,stage,status,started_at,counts)
                SELECT gen_random_uuid(),source_version_id,parser_version,importer_version,application_version,
                'created','running',clock_timestamp(),'{}' FROM catalog_import_run WHERE id=%s""",
                (run_id,),
            )
        elif mutation == "extra_provider":
            connection.execute("""INSERT INTO catalog_provider(id,code,name,documentation_url,use_policy_reference)
                VALUES(gen_random_uuid(),'unexpected-fixture','unexpected fixture','https://example.invalid/','TEST only')""")
        elif mutation in ("extra_evidence", "extra_identity"):
            evidence = connection.execute(
                """INSERT INTO catalog_evidence(id,source_file_id,source_version_id,locator,native_key,native_values,row_sha256)
                SELECT gen_random_uuid(),id,source_version_id,'extra-test-evidence','{}','{}',%s
                FROM catalog_source_file ORDER BY dataset_name LIMIT 1 RETURNING id""",
                ("0" * 64,),
            ).fetchone()
            if mutation == "extra_identity":
                assert evidence
                connection.execute(
                    """INSERT INTO catalog_set(id,namespace,identifier,creation_evidence_id)
                    VALUES(gen_random_uuid(),'rebrickable','unexpected-test-set',%s)""",
                    (evidence["id"],),
                )
        elif mutation == "changed_staging_counts":
            connection.execute(
                "DELETE FROM catalog_stage_sets WHERE row_number=(SELECT min(row_number) FROM catalog_stage_sets)"
            )
        elif mutation == "wrong_staging_file":
            connection.execute(
                """UPDATE catalog_stage_sets SET source_file_id=(SELECT id FROM catalog_source_file
                WHERE dataset_name='colors') WHERE row_number=(SELECT min(row_number) FROM catalog_stage_sets)"""
            )
        else:
            connection.execute(
                "UPDATE catalog_import_run SET stage='unexpected' WHERE id=%s", (run_id,)
            )
        before = durable_state(connection)
    with pytest.raises(SourceError):
        recover_failed(catalog_db, supplied_manifest, supplied_counts, run_id, supplied_candidate)
    with catalog_db.connect() as connection:
        assert durable_state(connection) == before


def test_recovery_refuses_concurrent_import_lock(
    catalog_db: CatalogDatabase, catalog_bundle: Path
) -> None:
    _, manifest, datasets, run_id, candidate_id = recovery_fixture(catalog_db, catalog_bundle)
    with catalog_db.connect() as connection, import_lock(connection, "rebrickable"):
        before = durable_state(connection)
        with pytest.raises(SourceError, match="import_busy"):
            recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
        assert durable_state(connection) == before
        run = connection.execute(
            "SELECT counts FROM catalog_import_run WHERE id=%s", (run_id,)
        ).fetchone()
        assert run and "recovery" not in run["counts"]


@pytest.mark.parametrize("mutation", ["running_child", "malformed_metadata"])
def test_explicit_retry_refuses_without_reconciling_or_new_attempt(
    catalog_db: CatalogDatabase,
    catalog_bundle: Path,
    mutation: str,
) -> None:
    area, manifest, datasets, run_id, candidate_id = recovery_fixture(catalog_db, catalog_bundle)
    recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
    with catalog_db.connect() as connection:
        if mutation == "running_child":
            connection.execute(
                """INSERT INTO catalog_import_run(id,source_version_id,parser_version,importer_version,
                application_version,stage,status,started_at,counts)
                SELECT gen_random_uuid(),source_version_id,parser_version,importer_version,application_version,
                'created','running',clock_timestamp(),'{}' FROM catalog_import_run WHERE id=%s""",
                (run_id,),
            )
        else:
            record = connection.execute(
                "SELECT counts FROM catalog_import_run WHERE id=%s", (run_id,)
            ).fetchone()
            assert record
            record["counts"]["recovery"]["version"] = "unreviewed"
            connection.execute(
                "UPDATE catalog_import_run SET counts=%s WHERE id=%s",
                (Jsonb(record["counts"]), run_id),
            )
        before = durable_state(connection)
    with pytest.raises(SourceError):
        import_source(
            catalog_db, area, str(catalog_bundle / "initial/manifest.json"), predecessor_id=run_id
        )
    with catalog_db.connect() as connection:
        assert durable_state(connection) == before


def test_linked_retry_with_changed_importer_version_refuses_before_candidate_build(
    catalog_db: CatalogDatabase, catalog_bundle: Path
) -> None:
    area, manifest, datasets, run_id, candidate_id = recovery_fixture(catalog_db, catalog_bundle)
    recover_failed(catalog_db, manifest, datasets, run_id, candidate_id)
    with catalog_db.connect() as connection:
        failed_audit = connection.execute(
            "SELECT * FROM catalog_import_run WHERE id=%s", (run_id,)
        ).fetchone()
    with pytest.raises(SourceError, match="recovery_retry_fingerprint_not_exact"):
        import_source(
            catalog_db,
            area,
            str(catalog_bundle / "initial/manifest.json"),
            importer_version=IMPORTER_VERSION + "-changed-test-version",
            predecessor_id=run_id,
        )
    with catalog_db.connect() as connection:
        assert (
            connection.execute("SELECT * FROM catalog_import_run WHERE id=%s", (run_id,)).fetchone()
            == failed_audit
        )
        attempts = connection.execute(
            "SELECT status,stage,failure_category,predecessor_id FROM catalog_import_run WHERE id<>%s",
            (run_id,),
        ).fetchall()
        assert attempts == [
            {
                "status": "failed",
                "stage": "failed",
                "failure_category": "recovery_retry_fingerprint_not_exact",
                "predecessor_id": run_id,
            }
        ]
        current = counts(connection)
        assert current["catalog_snapshot"] == current["catalog_set"] == 0
        assert current["catalog_set_fact"] == current["catalog_inventory_line"] == 0
        assert current["catalog_evidence"] == current["catalog_snapshot_validation"] == 0
        assert current["catalog_activation"] == 0
        assert all(current["catalog_stage_" + name] == n for name, n in datasets.items())
