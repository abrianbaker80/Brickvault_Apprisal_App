"""Description-assisted local retrieval; no model, prediction or mapping writes."""

import json
import re
import unicodedata
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brickvault_api.catalog.query_types import FigureMatch, SetMatch
from brickvault_api.catalog.repository import PinnedCatalog
from brickvault_api.recognition.local import digest, read_bytes, write_bytes

WORD = re.compile(r"[^\W_]+", re.UNICODE)
IDENTIFIER = re.compile(
    r"\b(?:sw\d+|fig[-_]\d+|\d{4,}(?:-\d+)?)\b|[\\/]|\.(?:png|jpe?g|webp)\b",
    re.IGNORECASE,
)
STOP = frozenset("a an the with and or of on in is are has have figure minifigure lego".split())


class RetrievalError(ValueError):
    """Fixed error categories only; private data never belongs in diagnostics."""


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, hide_input_in_errors=True)


class Key(Record):
    kind: Literal["set", "minifigure"]
    namespace: str = Field(min_length=1, max_length=64)
    identifier: str = Field(min_length=1, max_length=256)

    @property
    def token(self) -> str:
        return f"{self.kind}:{self.namespace}:{self.identifier}"


class Reference(Record):
    key: Key
    name: str
    features: str
    name_basis: str
    association_basis: str
    identity_status: Literal["provenance_supported"]
    source_urls: list[str]
    image_path: str
    image_sha256: str
    views: list[str]
    missing_views: list[str]
    attribution: dict[str, str]
    permission: str
    license_evidence: dict[str, str]


class Registry(Record):
    version: Literal["14b-reference-index-v1"] = "14b-reference-index-v1"
    source_sha256: str
    references: list[Reference]

    @model_validator(mode="after")
    def unique(self) -> "Registry":
        if len({r.key.token for r in self.references}) != len(self.references):
            raise RetrievalError("duplicate_reference_identity")
        return self


class Candidate(Record):
    key: Key
    name: str
    features: str = ""
    provenance: dict[str, str]
    canonical: dict[str, str] | None = None
    resolution: Literal["verified", "unresolved", "ambiguous", "not_checked"]
    reference: Reference | None = None


class Query(Record):
    text: str
    terms: list[str]
    excluded_fields: list[str]


class Match(Record):
    candidate: Candidate
    score: int
    matched_terms: dict[str, list[str]]
    ranking_basis: str = "name=3, source features=2; exact name phrase=6; identity keys excluded"


class KindBucket(Record):
    kind: Literal["set", "minifigure"]
    matches: list[Match]
    pool_count: int
    state: Literal["shortlist", "no_match"]

    @model_validator(mode="after")
    def consistent(self) -> "KindBucket":
        if (
            any(m.candidate.key.kind != self.kind for m in self.matches)
            or (self.state == "no_match") != (not self.matches)
            or self.pool_count < len(self.matches)
        ):
            raise RetrievalError("invalid_kind_bucket")
        return self


class Retrieval(Record):
    version: Literal["14b-description-v1", "14d-kind-partitioned-v1"] = "14b-description-v1"
    query: Query
    # Legacy records have a combined list. New records flatten both independent buckets
    # for note-key validation; this is not a shared rank or shared capacity.
    matches: list[Match]
    sets: KindBucket | None = None
    minifigures: KindBucket | None = None
    pool_count: int
    reference_count: int
    catalog_status: str
    catalog_truncated: bool
    state: Literal["shortlist", "no_match"]
    claim: str = "Description-assisted retrieval; scores are not confidence or identity proof."

    @model_validator(mode="after")
    def partition(self) -> "Retrieval":
        if self.version == "14d-kind-partitioned-v1" and (
            self.sets is None
            or self.minifigures is None
            or self.sets.kind != "set"
            or self.minifigures.kind != "minifigure"
            or self.matches != [*self.sets.matches, *self.minifigures.matches]
            or self.pool_count != self.sets.pool_count + self.minifigures.pool_count
        ):
            raise RetrievalError("invalid_kind_partition")
        return self


class SelectedImage(Record):
    path: str
    sha256: str


class Comparison(Record):
    version: Literal["14b-comparison-v1"] = "14b-comparison-v1"
    run: str = Field(pattern=r"^[a-f0-9]{32}$")
    retrieval: Retrieval
    images: list[SelectedImage]


class ReviewNote(Record):
    version: Literal["14b-operator-note-v1"] = "14b-operator-note-v1"
    run: str = Field(pattern=r"^[a-f0-9]{32}$")
    comparison_sha256: str
    decision: Literal[
        "provisional", "compatible", "none", "insufficient_evidence", "known_identity"
    ]
    candidates: list[Key] = Field(default_factory=list)
    needed_view: str = Field(default="", max_length=1000)
    comment: str = Field(default="", max_length=2000)
    operator_identity: Key | None = None
    assertion: str = "Operator review only; no production confirmation, mapping or valuation."

    @model_validator(mode="after")
    def disposition(self) -> "ReviewNote":
        n = len(self.candidates)
        if (
            (self.decision == "provisional" and n != 1)
            or (self.decision == "compatible" and n < 2)
            or (self.decision in ("none", "insufficient_evidence", "known_identity") and n != 0)
            or (self.decision == "insufficient_evidence" and not self.needed_view.strip())
            or ((self.decision == "known_identity") != (self.operator_identity is not None))
            or len({k.token for k in self.candidates}) != n
        ):
            raise RetrievalError("invalid_review_disposition")
        return self


def terms(value: str) -> list[str]:
    return sorted(set(WORD.findall(unicodedata.normalize("NFKC", value).casefold())) - STOP)


def query_from(payload: Mapping[str, Any]) -> Query:
    """Positive field selection: never ingest IDs, labels, filenames or prior answers."""
    if not isinstance(payload, Mapping):
        raise RetrievalError("invalid_visible_description")
    description = payload.get("description", "")
    clues = payload.get("visual_clues", [])
    if not isinstance(description, str) or not isinstance(clues, list):
        raise RetrievalError("invalid_visible_description")
    if not all(isinstance(c, str) for c in clues):
        raise RetrievalError("invalid_visible_description")
    text = " ".join([description, *clues]).strip()
    if (
        not text
        or len(text) > 256
        or IDENTIFIER.search(text)
        or any(unicodedata.category(c).startswith("C") for c in text)
    ):
        raise RetrievalError("description_requires_visible_text_without_identifiers_or_filenames")
    tokens = terms(text)
    if not 1 <= len(tokens) <= 12:
        raise RetrievalError("description_term_limit")
    return Query(
        text=text,
        terms=tokens,
        excluded_fields=sorted(set(payload) - {"description", "visual_clues"}),
    )


def retained_clues(
    payload: Mapping[str, Any],
    index: int,
    *,
    field: str = "visual_clues",
    indices: list[int] | None = None,
    candidate_index: int = 0,
) -> Query:
    """One selected prior candidate clue field; all other answer fields are excluded."""
    try:
        objects = payload["recognition"]["objects"]
        if index < 0 or index >= len(objects):
            raise RetrievalError("clue_object_unavailable")
        if field not in ("visual_clues", "text_clues"):
            raise RetrievalError("invalid_clue_field")
        candidates = objects[index]["candidates"]
        if candidate_index < 0 or candidate_index >= len(candidates):
            raise RetrievalError("clue_object_unavailable")
        clues = candidates[candidate_index]["supporting_" + field]
        if indices is not None:
            if any(i < 0 or i >= len(clues) for i in indices):
                raise RetrievalError("clue_object_unavailable")
            clues = [clues[i] for i in indices]
        query = query_from({"visual_clues": clues})
    except (KeyError, TypeError, IndexError):
        raise RetrievalError("clue_object_unavailable") from None
    return query.model_copy(
        update={"excluded_fields": [f"all prior fields except selected {field}"]}
    )


def prepare_registry(
    source: Path, names: Mapping[str, tuple[str, str]], destination: Path
) -> Registry:
    """Derive a reference-only index from accepted corrected evidence and supported names."""
    raw = read_bytes(source)
    evidence = json.loads(raw)
    refs = []
    for row in evidence["candidates"]:
        code = row["code"]
        name, basis = names[code]
        image = Path(row["source_image_path"])
        if digest(read_bytes(image, 25 * 1024 * 1024)) != row["source_image_sha256"]:
            raise RetrievalError("reference_image_changed")
        license_record = row["license_evidence"]
        license_path = Path(license_record.get("html_path", license_record.get("screenshot", "")))
        license_hash = license_record.get("html_sha256", license_record.get("screenshot_sha256"))
        if digest(read_bytes(license_path, 2 * 1024 * 1024)) != license_hash:
            raise RetrievalError("license_evidence_changed")
        if row["license"] != "CC BY 2.0" or row["identity_status"] != "provenance_supported":
            raise RetrievalError("reference_permission_or_identity_unavailable")
        credit = dict(row["required_attribution"])
        credit["changes"] = (
            "Original retained photo bytes embedded unchanged; CSS scales display only."
        )
        refs.append(
            Reference(
                key=Key.model_validate(row["whole_minifigure_identity"]),
                name=name,
                features=row["visible_features"],
                name_basis=basis,
                association_basis=row["association_basis"],
                identity_status=row["identity_status"],
                source_urls=[row["catalog_identity_source_url"], *row["provenance_urls"]],
                image_path=str(image),
                image_sha256=row["source_image_sha256"],
                views=["front, helmet on"],
                missing_views=row["unavailable_views"],
                attribution=credit,
                permission=row["permission_status"],
                license_evidence={"path": str(license_path), "sha256": str(license_hash)},
            )
        )
    registry = Registry(source_sha256=digest(raw), references=refs)
    write_bytes(destination, registry.model_dump_json(indent=2).encode())
    return registry


def catalog_candidates(catalog: PinnedCatalog, query: Query) -> tuple[list[Candidate], bool]:
    """Bounded union of existing set text search and the added figure text helper."""
    by_key: dict[str, Candidate] = {}
    truncated = False
    for term in query.terms:
        sets = catalog.search_sets(term, limit=100).data
        figures = catalog.search_minifigures(term, limit=100).data
        truncated |= len(sets) == 100 or len(figures) == 100
        rows: list[SetMatch | FigureMatch] = [*sets, *figures]
        for row in rows:
            key = Key(
                kind="set" if row.identity.kind == "set" else "minifigure",
                namespace=row.identity.namespace,
                identifier=row.identity.identifier,
            )
            facts = (
                " ".join(x for x in (row.source_type, row.classification) if x)
                if isinstance(row, FigureMatch)
                else ""
            )
            provenance = {
                "snapshot_id": str(row.provenance.snapshot_id),
                "source_version_id": str(row.provenance.source_version_id),
                "evidence_id": str(row.provenance.evidence_id),
            }
            by_key[key.token] = Candidate(
                key=key,
                name=row.name,
                features=facts,
                provenance=provenance,
                canonical={"id": str(row.identity.id), **key.model_dump()},
                resolution="verified",
            )
    return list(by_key.values()), truncated


def reference_candidate(reference: Reference, catalog: PinnedCatalog | None) -> Candidate:
    """Existing exact namespace/identifier resolution; no new provider crosswalk."""
    canonical = None
    resolution: Literal["verified", "unresolved", "ambiguous", "not_checked"] = (
        "unresolved" if catalog else "not_checked"
    )
    if catalog:
        identities = [
            x
            for x in catalog.resolve_identity(reference.key.kind, reference.key.identifier).data
            if x.namespace == reference.key.namespace
        ]
        # Native external mappings are intentionally not guessed from catalog names.
        if len(identities) == 1:
            canonical = {"id": str(identities[0].id), **reference.key.model_dump()}
            resolution = "verified"
        elif identities:
            resolution = "ambiguous"
    return Candidate(
        key=reference.key,
        name=reference.name,
        features=reference.features,
        provenance={
            "name_basis": reference.name_basis,
            "identity_basis": reference.association_basis,
        },
        canonical=canonical,
        resolution=resolution,
        reference=reference,
    )


def retrieve(
    query: Query, registry: Registry, catalog: PinnedCatalog | None, *, limit: int = 8
) -> Retrieval:
    if not 1 <= limit <= 12:
        raise RetrievalError("shortlist_limit")
    pool, truncated = catalog_candidates(catalog, query) if catalog else ([], False)
    candidates = {c.key.token: c for c in pool}
    for ref in registry.references:
        candidate = reference_candidate(ref, catalog)
        existing = candidates.get(candidate.key.token)
        if existing:
            candidate = candidate.model_copy(
                update={
                    "canonical": existing.canonical,
                    "resolution": existing.resolution,
                    "provenance": {**existing.provenance, **candidate.provenance},
                }
            )
        candidates[candidate.key.token] = candidate
    matches = []
    for candidate in candidates.values():
        hits = {
            "name": sorted(set(query.terms) & set(terms(candidate.name))),
            "source_features": sorted(set(query.terms) & set(terms(candidate.features))),
        }
        score = 3 * len(hits["name"]) + 2 * len(hits["source_features"])
        if WORD.findall(query.text.casefold()) == WORD.findall(candidate.name.casefold()):
            score += 6
        if score:
            matches.append(Match(candidate=candidate, score=score, matched_terms=hits))
    matches.sort(key=lambda m: (-m.score, m.candidate.key.token))
    sets = KindBucket(
        kind="set",
        matches=[m for m in matches if m.candidate.key.kind == "set"][:limit],
        pool_count=sum(c.key.kind == "set" for c in candidates.values()),
        state="shortlist" if any(m.candidate.key.kind == "set" for m in matches) else "no_match",
    )
    figures = KindBucket(
        kind="minifigure",
        matches=[m for m in matches if m.candidate.key.kind == "minifigure"][:limit],
        pool_count=sum(c.key.kind == "minifigure" for c in candidates.values()),
        state="shortlist"
        if any(m.candidate.key.kind == "minifigure" for m in matches)
        else "no_match",
    )
    return Retrieval(
        version="14d-kind-partitioned-v1",
        query=query,
        matches=[*sets.matches, *figures.matches],
        sets=sets,
        minifigures=figures,
        pool_count=len(candidates),
        reference_count=len(registry.references),
        catalog_status=f"accepted snapshot {catalog.snapshot.id}"
        if catalog
        else "not queried: reference-only",
        catalog_truncated=truncated,
        state="shortlist" if matches else "no_match",
    )


def save_note(root: Path, comparison: Comparison, note: ReviewNote) -> Path:
    path = root / comparison.run / "comparison.json"
    if (
        note.run != comparison.run
        or note.comparison_sha256 != digest(read_bytes(path, 4 * 1024 * 1024))
        or any(
            k.token not in {m.candidate.key.token for m in comparison.retrieval.matches}
            for k in note.candidates
        )
    ):
        raise RetrievalError("note_comparison_mismatch")
    target = path.parent / f"note-{uuid4().hex}.json"
    write_bytes(target, note.model_dump_json(indent=2).encode())
    return target
