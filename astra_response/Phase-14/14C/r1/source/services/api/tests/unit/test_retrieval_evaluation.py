"""Three scoring/integrity fixtures; no 14B test rerun or catalog startup."""

from pathlib import Path

import pytest
from brickvault_api.recognition.evaluation import LabelCase, aggregate, frozen_bytes, score_case
from brickvault_api.recognition.local import digest
from brickvault_api.recognition.retrieval import (
    Candidate,
    Key,
    Match,
    Retrieval,
    RetrievalError,
    query_from,
)


def result(keys: list[Key], *, truncated: bool = False, pool: int = 10) -> Retrieval:
    return Retrieval(
        query=query_from({"description": "gray robot"}),
        matches=[
            Match(
                candidate=Candidate(
                    key=key, name="Gray robot", provenance={}, resolution="verified"
                ),
                score=3,
                matched_terms={"name": ["robot"]},
            )
            for key in keys
        ],
        pool_count=pool,
        reference_count=0,
        catalog_status="synthetic fixture",
        catalog_truncated=truncated,
        state="shortlist" if keys else "no_match",
    )


def label(code: str = "fixture") -> LabelCase:
    return LabelCase(
        code=code,
        group="synthetic",
        query_code="query",
        expected=Key(kind="set", namespace="native", identifier="target"),
        labels_exhaustive=True,
    )


def test_exact_key_rank_and_top8_boundary() -> None:
    case = label()
    wrong_namespace = Key(kind="set", namespace="other", identifier="target")
    wrong_kind = Key(kind="minifigure", namespace="native", identifier="target")
    ranked = result([wrong_namespace, wrong_kind, case.expected])
    score = score_case(case, ranked, available=True, curated_reference=False)
    assert score.rank == 3 and not score.top1 and score.top3 and score.top8
    assert score.reciprocal_rank_at8 == pytest.approx(1 / 3)
    eight = result(
        [Key(kind="set", namespace="native", identifier=str(i)) for i in range(7)] + [case.expected]
    )
    boundary = score_case(case, eight, available=True, curated_reference=False)
    assert boundary.rank == 8 and not boundary.top3 and boundary.top8
    assert boundary.reciprocal_rank_at8 == 0.125


def test_unavailable_excluded_and_no_match_counted_as_scoreable_miss() -> None:
    hit = score_case(
        label("hit"),
        result([label().expected], truncated=True, pool=4),
        available=True,
        curated_reference=False,
    )
    miss = score_case(label("miss"), result([], pool=2), available=True, curated_reference=False)
    absent = score_case(label("absent"), None, available=False, curated_reference=False)
    assert absent.top8 is None and absent.no_match is None and absent.rank is None
    totals = aggregate([hit, miss, absent])
    assert totals["scoreable"] == 2 and totals["not_scoreable_corpus_mapping_unavailable"] == 1
    assert totals["top8_hits"] == 1 and totals["no_match_cases"] == 1
    assert totals["mean_reciprocal_rank_at8"] == 0.5
    assert totals["average_candidate_pool"] == 3 and totals["truncated_fraction"] == 0.5


def test_query_and_truth_hashes_refuse_changes_independently(tmp_path: Path) -> None:
    query = tmp_path / "query.json"
    truth = tmp_path / "truth.json"
    query.write_bytes(b'{"description":"gray robot"}')
    truth.write_bytes(b'{"identity":"synthetic"}')
    qhash, thash = digest(query.read_bytes()), digest(truth.read_bytes())
    assert frozen_bytes(query, qhash) == query.read_bytes()
    assert frozen_bytes(truth, thash) == truth.read_bytes()
    query.write_bytes(b'{"description":"changed after ranking"}')
    with pytest.raises(RetrievalError, match="frozen_evaluation_input_changed"):
        frozen_bytes(query, qhash)
    assert frozen_bytes(truth, thash) == truth.read_bytes()
    truth.write_bytes(b'{"identity":"changed label"}')
    with pytest.raises(RetrievalError, match="frozen_evaluation_input_changed"):
        frozen_bytes(truth, thash)
