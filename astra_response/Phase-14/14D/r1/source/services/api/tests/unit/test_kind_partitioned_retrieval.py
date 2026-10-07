"""Three structural fixtures; no older suites, provider or database calls."""

from typing import Literal, cast
from uuid import UUID

import pytest
from brickvault_api.catalog.query_types import Identity, QueryResult, QueryState, SnapshotRef
from brickvault_api.catalog.repository import PinnedCatalog
from brickvault_api.recognition import retrieval
from brickvault_api.recognition.comparison import render
from brickvault_api.recognition.evaluation import LabelCase, score_case
from brickvault_api.recognition.retrieval import (
    Candidate,
    Comparison,
    Key,
    Query,
    Reference,
    Registry,
    Retrieval,
    query_from,
    retrieve,
)

UID = UUID(int=1)
SNAPSHOT = SnapshotRef(UID, UID, UID, "fixture", True)


class Catalog:
    snapshot = SNAPSHOT

    def resolve_identity(self, kind: str, identifier: str) -> QueryResult[tuple[Identity, ...]]:
        return QueryResult(
            SNAPSHOT, QueryState.OK, (Identity(UID, kind, "native-fixture", identifier),)
        )


def candidate(kind: Literal["set", "minifigure"], identifier: str, name: str) -> Candidate:
    key = Key(kind=kind, namespace="native-fixture", identifier=identifier)
    return Candidate(
        key=key, name=name, provenance={}, canonical=key.model_dump(), resolution="verified"
    )


def pool_fixture(
    monkeypatch: pytest.MonkeyPatch, pool: list[Candidate], *, truncated: bool = False
) -> None:
    def pool_for(catalog: PinnedCatalog, query: Query) -> tuple[list[Candidate], bool]:
        return pool, truncated

    monkeypatch.setattr(retrieval, "catalog_candidates", pool_for)


def test_buckets_cannot_starve_and_report_has_both_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = [candidate("set", str(i), "Fighter") for i in range(3)] + [
        candidate("minifigure", str(i), "Gray fighter") for i in range(10)
    ]
    pool_fixture(monkeypatch, pool, truncated=True)
    registry = Registry(source_sha256="fixture", references=[])
    result = retrieve(
        query_from({"description": "gray fighter"}), registry, cast(PinnedCatalog, Catalog())
    )
    assert result.sets is not None and result.minifigures is not None
    assert len(result.sets.matches) == 3 and len(result.minifigures.matches) == 8
    assert result.sets.pool_count == 3 and result.minifigures.pool_count == 10
    assert result.pool_count == 13 and result.catalog_truncated
    assert all(m.score == 3 for m in result.sets.matches)
    assert all(m.score == 12 for m in result.minifigures.matches)  # Includes unchanged exact-name bonus.
    text = render(Comparison(run="0" * 32, retrieval=result, images=[])).decode()
    assert "<h2>Set candidates</h2>" in text and "<h2>Minifigure candidates</h2>" in text
    assert "connect-src &apos;none&apos;" in text
    empty = retrieve(
        query_from({"description": "purple castle"}), registry, cast(PinnedCatalog, Catalog())
    )
    assert empty.sets is not None and empty.minifigures is not None
    assert empty.sets.state == empty.minifigures.state == "no_match"


def test_within_kind_ranking_ties_and_legacy_reading_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    kinds: tuple[Literal["set", "minifigure"], ...] = ("set", "minifigure")
    pool = [
        candidate(kind, key, name)
        for kind in kinds
        for key, name in [("z", "Gray fighter"), ("a", "Gray fighter"), ("bonus", "Fighter")]
    ]
    registry = Registry(source_sha256="fixture", references=[])
    query = query_from({"description": "fighter"})
    pool_fixture(monkeypatch, pool)
    first = retrieve(query, registry, cast(PinnedCatalog, Catalog()))
    pool_fixture(monkeypatch, pool[::-1])
    second = retrieve(query, registry, cast(PinnedCatalog, Catalog()))
    assert first.sets == second.sets and first.minifigures == second.minifigures
    assert first.sets is not None and first.minifigures is not None
    for bucket in (first.sets, first.minifigures):
        assert [m.candidate.key.identifier for m in bucket.matches] == ["bonus", "a", "z"]
        assert [m.score for m in bucket.matches] == [9, 3, 3]
        assert bucket.matches[0].matched_terms == {"name": ["fighter"], "source_features": []}
    legacy = first.model_dump(exclude={"sets", "minifigures"})
    legacy["version"] = "14b-description-v1"
    loaded = Retrieval.model_validate(legacy)
    assert loaded.sets is None and loaded.matches == first.matches


def test_query_leakage_and_exact_namespace_canonical_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    query = query_from(
        {
            "description": "gray fighter",
            "expected": ["secret-fixture"],
            "filename": "answer-fixture.png",
            "previous_answer": "secret-fixture",
        }
    )
    assert query.terms == ["fighter", "gray"]
    assert query.excluded_fields == ["expected", "filename", "previous_answer"]
    native = candidate("minifigure", "same-fixture", "Gray fighter")
    pool_fixture(monkeypatch, [native])
    key = Key(kind="minifigure", namespace="external-fixture", identifier="same-fixture")
    ref = Reference(
        key=key,
        name="Gray fighter",
        features="gray armor",
        name_basis="fixture",
        association_basis="fixture, concealed head unverified",
        identity_status="provenance_supported",
        source_urls=[],
        image_path="synthetic",
        image_sha256="0" * 64,
        views=["front"],
        missing_views=["uncovered head"],
        attribution={},
        permission="fixture",
        license_evidence={},
    )
    result = retrieve(
        query, Registry(source_sha256="fixture", references=[ref]), cast(PinnedCatalog, Catalog())
    )
    assert result.sets is not None and result.sets.state == "no_match"
    assert result.minifigures is not None
    external = next(m.candidate for m in result.minifigures.matches if m.candidate.reference)
    assert (
        external.key == key and external.resolution == "unresolved" and external.canonical is None
    )
    assert native.key != key and len(result.minifigures.matches) == 2
    label = LabelCase(
        code="fixture",
        group="synthetic",
        query_code="fixture",
        expected=key,
        labels_exhaustive=True,
    )
    score = score_case(label, result, available=True, curated_reference=True)
    assert score.rank == 1 and score.rank_scope == "correct_kind_bucket"
    absent = score_case(label, None, available=False, curated_reference=False)
    assert absent.status == "not_scoreable" and absent.top8 is None
