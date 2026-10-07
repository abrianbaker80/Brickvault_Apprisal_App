"""One frozen description-retrieval evaluation; absent corpus keys are unscoreable."""

from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from brickvault_api.catalog.repository import PinnedCatalog
from brickvault_api.recognition.local import digest, read_bytes
from brickvault_api.recognition.retrieval import (
    Key,
    Query,
    Record,
    Registry,
    Retrieval,
    RetrievalError,
    query_from,
    retrieve,
)


class VisibleQuery(Record):
    group: str
    description: str


class QueryFile(Record):
    version: Literal["14c-queries-v1"]
    queries: dict[str, VisibleQuery]
    basis: str


class LabelCase(Record):
    code: str
    group: str
    query_code: str | None
    expected: Key
    labels_exhaustive: bool


class Labels(Record):
    version: Literal["14c-labels-v1"]
    prepared_sha256: str
    cases: list[LabelCase]
    excluded_groups: dict[str, str]


class CaseScore(Record):
    code: str
    group: str
    kind: str
    namespace: str
    status: Literal["scoreable", "not_scoreable"]
    reason: str | None = None
    corpus_identity: Literal["catalog_native", "external_unresolved", "unavailable"]
    curated_reference: bool
    rank: int | None = None
    top1: bool | None = None
    top3: bool | None = None
    top8: bool | None = None
    reciprocal_rank_at8: float | None = None
    no_match: bool | None = None
    pool_count: int | None = None
    overall_pool_count: int | None = None
    shortlist_count: int | None = None
    rank_scope: Literal["combined_top8", "correct_kind_bucket"] = "combined_top8"
    truncated: bool | None = None
    reference_images_in_shortlist: int | None = None
    target_returned_reference: bool | None = None


def frozen_bytes(path: Path, expected_hash: str) -> bytes:
    raw = read_bytes(path, 4 * 1024 * 1024)
    if digest(raw) != expected_hash:
        raise RetrievalError("frozen_evaluation_input_changed")
    return raw


def score_case(
    case: LabelCase,
    result: Retrieval | None,
    *,
    available: bool,
    curated_reference: bool,
) -> CaseScore:
    fields = {
        "code": case.code,
        "group": case.group,
        "kind": case.expected.kind,
        "namespace": case.expected.namespace,
        "curated_reference": curated_reference,
    }
    if not available:
        return CaseScore.model_validate(
            {
                **fields,
                "status": "not_scoreable",
                "reason": "not scoreable: corpus/mapping unavailable",
                "corpus_identity": "unavailable",
            }
        )
    if result is None:
        raise RetrievalError("scoreable_case_requires_frozen_retrieval")
    # Both kinds were retrieved independently before the scorer consults the label.
    bucket = result.sets if case.expected.kind == "set" else result.minifigures
    matches = bucket.matches if bucket is not None else result.matches
    rank = next(
        (i for i, match in enumerate(matches, 1) if match.candidate.key == case.expected),
        None,
    )
    return CaseScore.model_validate(
        {
            **fields,
            "status": "scoreable",
            "corpus_identity": "external_unresolved" if curated_reference else "catalog_native",
            "rank": rank,
            "top1": rank == 1,
            "top3": rank is not None and rank <= 3,
            "top8": rank is not None and rank <= 8,
            "reciprocal_rank_at8": 1 / rank if rank is not None else 0,
            "no_match": (bucket.state if bucket is not None else result.state) == "no_match",
            "pool_count": bucket.pool_count if bucket is not None else result.pool_count,
            "overall_pool_count": result.pool_count,
            "shortlist_count": len(matches),
            "rank_scope": "correct_kind_bucket" if bucket is not None else "combined_top8",
            "truncated": result.catalog_truncated,
            "reference_images_in_shortlist": sum(
                m.candidate.reference is not None for m in matches
            ),
            "target_returned_reference": matches[rank - 1].candidate.reference is not None
            if rank is not None
            else None,
        }
    )


def aggregate(scores: list[CaseScore]) -> dict[str, int | float]:
    scored = [row for row in scores if row.status == "scoreable"]
    n = len(scored)
    if not n:
        raise RetrievalError("no_scoreable_evaluation_cases")
    return {
        "scoreable": n,
        "not_scoreable_corpus_mapping_unavailable": len(scores) - n,
        "top1_hits": sum(row.top1 is True for row in scored),
        "top3_hits": sum(row.top3 is True for row in scored),
        "top8_hits": sum(row.top8 is True for row in scored),
        "mean_reciprocal_rank_at8": sum(row.reciprocal_rank_at8 or 0 for row in scored) / n,
        "no_match_cases": sum(row.no_match is True for row in scored),
        "average_candidate_pool": sum(row.pool_count or 0 for row in scored) / n,
        "average_overall_pool": sum(
            row.overall_pool_count if row.overall_pool_count is not None else row.pool_count or 0
            for row in scored
        )
        / n,
        "truncated_cases": sum(row.truncated is True for row in scored),
        "truncated_fraction": sum(row.truncated is True for row in scored) / n,
        "shortlist_entries_with_reference": sum(
            row.reference_images_in_shortlist or 0 for row in scored
        ),
        "target_hits_with_reference": sum(row.target_returned_reference is True for row in scored),
    }


def evaluate(
    queries: QueryFile, labels: Labels, registry: Registry, catalog: PinnedCatalog
) -> tuple[list[CaseScore], Mapping[str, Retrieval]]:
    if len({c.code for c in labels.cases}) != len(labels.cases):
        raise RetrievalError("duplicate_evaluation_case")
    # Corpus membership is independent of query results; no label is a retrieval input.
    refs = {ref.key.token for ref in registry.references}
    available: dict[str, bool] = {}
    validated: dict[str, Query] = {}
    for case in labels.cases:
        native = any(
            identity.namespace == case.expected.namespace
            for identity in catalog.resolve_identity(
                case.expected.kind, case.expected.identifier
            ).data
        )
        available[case.code] = native or case.expected.token in refs
        if available[case.code]:
            if case.query_code not in queries.queries:
                raise RetrievalError("scoreable_case_requires_frozen_query")
            assert case.query_code is not None
            visible = queries.queries[case.query_code]
            if visible.group != case.group:
                raise RetrievalError("query_group_mismatch")
            validated[case.query_code] = query_from({"description": visible.description})
    results = {
        code: retrieve(query, registry, catalog, limit=8) for code, query in validated.items()
    }
    scores = [
        score_case(
            case,
            results.get(case.query_code or ""),
            available=available[case.code],
            curated_reference=case.expected.token in refs,
        )
        for case in labels.cases
    ]
    return scores, results
