"""Bounded line inserts preserve every source row and candidate transaction."""

import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
from typing import Any

import pytest

from brickvault_api.catalog import builder
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.catalog.importer import import_source
from brickvault_api.providers.rebrickable.records import SourceError
from brickvault_api.providers.rebrickable.source import SourceArea


def test_part_line_batches_cover_source_rows_once(
    catalog_db: CatalogDatabase, catalog_bundle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(builder, "INVENTORY_LINE_BATCH_SPAN", 2)
    observed: list[tuple[int, int]] = []

    def inspect(
        connection: CatalogConnection,
        event: dict[str, Any],
        statement: str,
        params: Any,
    ) -> None:
        if event["operation"].startswith("inventory_lines:parts"):
            observed.append((params["row_after"], params["row_through"]))

    report = import_source(
        catalog_db,
        SourceArea(catalog_bundle),
        str(catalog_bundle / "initial/manifest.json"),
        build_inspector=inspect,
    )
    assert report["state"] == "passed"
    assert observed == [(0, 2), (2, 4), (4, 6), (6, 8)]
    with catalog_db.connect() as connection:
        quantities = connection.execute(
            """SELECT sum(regular_quantity) AS regular,sum(extra_quantity) AS spare,
            count(*) AS lines,count(DISTINCT source_locator) AS locators
            FROM catalog_inventory_line WHERE native_type='part'"""
        ).fetchone()
        assert quantities == {"regular": 9, "spare": 1, "lines": 6, "locators": 6}
        coverage = connection.execute(
            """SELECT count(*) AS n FROM catalog_stage_inventory_parts s
            FULL JOIN (SELECT id,evidence_id FROM catalog_inventory_line
                WHERE native_type='part') l ON l.evidence_id=s.evidence_id
            WHERE s.run_id IS NULL OR l.id IS NULL"""
        ).fetchone()
        assert coverage == {"n": 0}


def test_multiline_gzip_records_preserve_sparse_row_locators_and_empty_batches(
    catalog_db: CatalogDatabase, catalog_bundle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path = catalog_bundle / "initial/manifest.json"
    manifest = json.loads(manifest_path.read_bytes())
    source = next(item for item in manifest["files"] if item["dataset"] == "inventory_parts")
    with (manifest_path.parent / source["location"]).open(encoding="utf-8", newline="") as stream:
        records = list(csv.DictReader(stream))
    assert len(records) == 6
    headers = [*source["headers"], "fixture_note"]
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    for index, record in enumerate(records):
        # The ignored field is legal synthetic evidence. Its four physical lines
        # make the next record start at 6, leaving the (2,4] range empty.
        writer.writerow(
            {**record, "fixture_note": "one\ntwo\nthree\nfour" if index == 0 else "single"}
        )
    raw = text.getvalue().encode("utf-8")
    compressed = gzip.compress(raw, mtime=0)
    source.update(
        location="inventory_parts.csv.gz",
        format="gzip",
        headers=headers,
        compressed_sha256=hashlib.sha256(compressed).hexdigest(),
        decompressed_sha256=hashlib.sha256(raw).hexdigest(),
        compressed_bytes=len(compressed),
        decompressed_bytes=len(raw),
    )
    (manifest_path.parent / source["location"]).write_bytes(compressed)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(builder, "INVENTORY_LINE_BATCH_SPAN", 2)
    ranges: list[tuple[int, int]] = []
    affected: list[int] = []

    def inspect(
        connection: CatalogConnection,
        event: dict[str, Any],
        statement: str,
        params: Any,
    ) -> None:
        if event["operation"].startswith("inventory_lines:parts"):
            ranges.append((params["row_after"], params["row_through"]))

    def progress(event: dict[str, Any]) -> None:
        if event.get("stage") == "build_step_completed" and event["operation"].startswith(
            "inventory_lines:parts"
        ):
            affected.append(event["affected_rows"])

    report = import_source(
        catalog_db,
        SourceArea(catalog_bundle),
        str(manifest_path),
        build_inspector=inspect,
        progress=progress,
    )
    assert report["state"] == "passed" and report["dataset_counts"]["inventory_parts"] == 6
    assert ranges == [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
    assert affected == [1, 0, 1, 2, 2]
    with catalog_db.connect() as connection:
        actual = connection.execute(
            """SELECT source_locator,regular_quantity,extra_quantity
            FROM catalog_inventory_line WHERE native_type='part'
            ORDER BY split_part(source_locator,':',2)::bigint"""
        ).fetchall()
        assert actual == [
            {"source_locator": "inventory_parts:2", "regular_quantity": 1, "extra_quantity": 0},
            {"source_locator": "inventory_parts:6", "regular_quantity": 4, "extra_quantity": 0},
            {"source_locator": "inventory_parts:7", "regular_quantity": 0, "extra_quantity": 1},
            {"source_locator": "inventory_parts:8", "regular_quantity": 1, "extra_quantity": 0},
            {"source_locator": "inventory_parts:9", "regular_quantity": 2, "extra_quantity": 0},
            {"source_locator": "inventory_parts:10", "regular_quantity": 1, "extra_quantity": 0},
        ]


def test_failure_after_first_part_batch_rolls_back_whole_candidate(
    catalog_db: CatalogDatabase, catalog_bundle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(builder, "INVENTORY_LINE_BATCH_SPAN", 2)
    seen: list[int] = []

    def inspect(
        connection: CatalogConnection,
        event: dict[str, Any],
        statement: str,
        params: Any,
    ) -> None:
        if not event["operation"].startswith("inventory_lines:parts"):
            return
        row = connection.execute("SELECT count(*) AS n FROM catalog_inventory_line").fetchone()
        assert row
        seen.append(row["n"])
        if len(seen) == 2:
            assert row["n"] == 1
            raise SourceError("batch_failure_fixture", "inventory_parts")

    with pytest.raises(SourceError, match="batch_failure_fixture"):
        import_source(
            catalog_db,
            SourceArea(catalog_bundle),
            str(catalog_bundle / "initial/manifest.json"),
            build_inspector=inspect,
        )
    assert seen == [0, 1]
    with catalog_db.connect() as connection:
        for table in ("catalog_inventory_line", "catalog_inventory_revision", "catalog_evidence"):
            assert connection.execute(f"SELECT count(*) AS n FROM {table}").fetchone() == {"n": 0}
        assert connection.execute("SELECT status,stage FROM catalog_import_run").fetchall() == [
            {"status": "failed", "stage": "failed"}
        ]
        assert connection.execute("SELECT state FROM catalog_snapshot").fetchall() == [
            {"state": "candidate"}
        ]
        assert connection.execute(
            "SELECT count(*) AS n FROM catalog_stage_inventory_parts"
        ).fetchone() == {"n": 6}
