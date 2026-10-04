"""Six synthetic Phase 14B correctness cases; no network or database startup."""

from pathlib import Path
from typing import Any, cast
from uuid import UUID

import pytest
from PIL import Image
from pydantic import ValidationError

from brickvault_api.catalog.connection import CatalogConnection
from brickvault_api.catalog.query_types import (
    FigureMatch,
    Identity,
    Provenance,
    QueryResult,
    QueryState,
    SnapshotRef,
)
from brickvault_api.catalog.repository import PinnedCatalog
from brickvault_api.recognition.comparison import create_comparison, render_note
from brickvault_api.recognition.local import digest, read_bytes
from brickvault_api.recognition.retrieval import (
    Key,
    Reference,
    Registry,
    RetrievalError,
    ReviewNote,
    catalog_candidates,
    query_from,
    retained_clues,
    retrieve,
    save_note,
)

UID = UUID(int=1)
SNAPSHOT = SnapshotRef(UID, UID, UID, "synthetic", True)
PROVENANCE = Provenance(UID, UID, UID)


def reference(tmp_path: Path, identifier: str = "external-fixture") -> Reference:
    path = tmp_path / "reference.png"
    if not path.exists():
        Image.new("RGB", (40, 60), "green").save(path)
    return Reference(
        key=Key(kind="minifigure", namespace="external-fixture", identifier=identifier),
        name="Green helmet figure",
        features="green helmet gray hands",
        name_basis="synthetic source",
        association_basis="synthetic identity provenance; head unverified",
        identity_status="provenance_supported",
        source_urls=["https://example.invalid/catalog"],
        image_path=str(path),
        image_sha256=digest(path.read_bytes()),
        views=["front, helmet on"],
        missing_views=["head with helmet removed"],
        attribution={"creator": "Synthetic fixture", "license": "fixture"},
        permission="synthetic fixture only",
        license_evidence={"path": "synthetic", "sha256": "0" * 64},
    )


class FakeCatalog:
    snapshot = SNAPSHOT

    def __init__(self) -> None:
        self.queries: list[str] = []

    def search_sets(self, value: str, *, limit: int) -> QueryResult[tuple[Any, ...]]:
        self.queries.append(value)
        return QueryResult(SNAPSHOT, QueryState.EMPTY, ())

    def search_minifigures(self, value: str, *, limit: int) -> QueryResult[tuple[FigureMatch, ...]]:
        self.queries.append(value)
        rows = (
            (
                FigureMatch(
                    Identity(UID, "minifigure", "native-fixture", "native-fixture"),
                    "Green helmet figure",
                    None,
                    None,
                    PROVENANCE,
                ),
            )
            if value in ("green", "helmet")
            else ()
        )
        return QueryResult(SNAPSHOT, QueryState.OK if rows else QueryState.EMPTY, rows)

    def resolve_identity(self, kind: str, identifier: str) -> QueryResult[tuple[Identity, ...]]:
        # A same identifier in another namespace must never become a crosswalk.
        return QueryResult(
            SNAPSHOT, QueryState.OK, (Identity(UID, kind, "native-fixture", identifier),)
        )


def test_deterministic_rank_ties_and_no_match(tmp_path: Path) -> None:
    refs = [reference(tmp_path, "z-fixture"), reference(tmp_path, "a-fixture")]
    query = query_from({"description": "green helmet"})
    first = retrieve(query, Registry(source_sha256="fixture", references=refs), None)
    second = retrieve(query, Registry(source_sha256="fixture", references=refs[::-1]), None)
    assert first.matches == second.matches
    assert [m.candidate.key.identifier for m in first.matches] == ["a-fixture", "z-fixture"]
    assert first.matches[0].matched_terms["name"] == ["green", "helmet"]
    assert first.matches[0].score == 10
    assert (
        retrieve(
            query_from({"description": "purple spaceship"}),
            Registry(source_sha256="fixture", references=refs),
            None,
        ).state
        == "no_match"
    )


def test_catalog_candidate_without_image_and_namespace_gap(tmp_path: Path) -> None:
    catalog = cast(PinnedCatalog, FakeCatalog())
    registry = Registry(source_sha256="fixture", references=[reference(tmp_path)])
    result = retrieve(query_from({"description": "green helmet"}), registry, catalog)
    assert result.pool_count == 2
    external = next(m.candidate for m in result.matches if m.candidate.reference)
    native = next(m.candidate for m in result.matches if not m.candidate.reference)
    assert external.resolution == "unresolved" and external.canonical is None
    assert native.resolution == "verified" and native.reference is None
    assert native.key.namespace != external.key.namespace


def test_labels_answers_filenames_and_ids_never_reach_query() -> None:
    payload = {
        "description": "green helmet",
        "expected": ["sw1234"],
        "previous_answer": {"identifier": "sw5678"},
        "filename": "answer-sw1234.jpg",
        "correct_answer": "B",
        "reviewer_conclusion": "B is correct",
    }
    query = query_from(payload)
    catalog = FakeCatalog()
    catalog_candidates(cast(PinnedCatalog, catalog), query)
    assert catalog.queries == ["green", "green", "helmet", "helmet"]
    assert query.excluded_fields == sorted(set(payload) - {"description"})
    for text in ("green helmet sw1234", "answer-sw1234.jpg", "green fig-012345"):
        with pytest.raises(RetrievalError):
            query_from({"description": text})
    prior = {
        "recognition": {
            "objects": [
                {
                    "candidates": [
                        {
                            "identifier": "sw1234",
                            "supporting_visual_clues": ["green helmet"],
                            "supporting_text_clues": ["green armor"],
                        }
                    ]
                }
            ]
        },
        "expected": ["sw5678"],
    }
    assert retained_clues(prior, 0).terms == ["green", "helmet"]
    with pytest.raises(RetrievalError):
        retained_clues(prior, -1)


def test_ambiguity_notes_are_separate_append_only_operator_assertions(tmp_path: Path) -> None:
    registry = Registry(
        source_sha256="fixture",
        references=[reference(tmp_path, "a-fixture"), reference(tmp_path, "b-fixture")],
    )
    result = retrieve(query_from({"description": "green helmet"}), registry, None)
    comparison, report = create_comparison(tmp_path, result, [tmp_path / "reference.png"])
    original = read_bytes(report)
    source_hash = digest(read_bytes(report.parent / "comparison.json"))
    note = ReviewNote(
        run=comparison.run,
        comparison_sha256=source_hash,
        decision="compatible",
        candidates=[m.candidate.key for m in result.matches],
    )
    path = save_note(tmp_path, comparison, note)
    second = save_note(tmp_path, comparison, note)
    assert path != second and ReviewNote.model_validate_json(path.read_bytes()) == note
    assert report.read_bytes() == original
    assert "unique identity: not established" in original.decode()
    with pytest.raises(ValidationError):
        ReviewNote(
            run=comparison.run, comparison_sha256=source_hash, decision="insufficient_evidence"
        )
    with pytest.raises(RetrievalError):
        save_note(
            tmp_path,
            comparison,
            note.model_copy(
                update={"candidates": [Key(kind="set", namespace="other", identifier="missing")]}
            ),
        )
    known = ReviewNote(
        run=comparison.run,
        comparison_sha256=source_hash,
        decision="known_identity",
        operator_identity=Key(
            kind="minifigure", namespace="operator-fixture", identifier="known-fixture"
        ),
    )
    assert "operator-supplied assertion" in render_note(known).decode()


def test_private_html_escapes_text_and_preserves_selected_bytes(tmp_path: Path) -> None:
    ref = reference(tmp_path)
    before = Path(ref.image_path).read_bytes()
    result = retrieve(
        query_from({"description": "<green helmet>"}),
        Registry(source_sha256="fixture", references=[ref]),
        None,
    )
    # Slashes are forbidden in retrieval text, so exercise escaping through an untrusted source name.
    candidate = result.matches[0].candidate.model_copy(
        update={"name": "<img src=https://example.invalid onerror=alert(1)>"}
    )
    result = result.model_copy(
        update={"matches": [result.matches[0].model_copy(update={"candidate": candidate})]}
    )
    comparison, report = create_comparison(tmp_path, result, [Path(ref.image_path)])
    text = report.read_text()
    assert "&lt;img src=https:" in text and "<img src=https:" not in text
    assert "script-src &apos;none&apos;" in text and "connect-src &apos;none&apos;" in text
    assert 'src="data:image/png;base64,' in text and "https://example.invalid" in text
    assert before == Path(ref.image_path).read_bytes()
    Path(ref.image_path).write_bytes(b"changed")
    from brickvault_api.recognition.comparison import render

    with pytest.raises(RetrievalError):
        render(comparison)


def test_minifigure_query_is_bounded_and_snapshot_scoped() -> None:
    calls: list[tuple[str, dict[str, Any]]] = []

    class Rows:
        def fetchmany(self, count: int) -> list[dict[str, Any]]:
            assert count == 4
            return [
                {
                    "id": UID,
                    "namespace": "fixture",
                    "identifier": "whole-figure",
                    "display_name": "Helmet figure",
                    "source_type": None,
                    "classification": None,
                    "snapshot_id": UID,
                    "source_version_id": UID,
                    "evidence_id": UID,
                }
            ]

    class Connection:
        def execute(self, sql: str, params: dict[str, Any]) -> Rows:
            calls.append((sql, params))
            return Rows()

    catalog = PinnedCatalog(cast(CatalogConnection, Connection()), SNAPSHOT)
    result = catalog.search_minifigures("helmet", limit=3)
    assert result.data[0].identity.kind == "minifigure"
    assert calls[0][1] == {"query": "helmet", "limit": 3, "snapshot": UID}
    assert "f.snapshot_id=%(snapshot)s" in calls[0][0] and "LIMIT %(limit)s" in calls[0][0]
    assert catalog.query_count == 1
