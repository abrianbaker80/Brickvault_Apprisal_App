"""Strict, private pilot contracts. Predictions never become confirmations."""

from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brickvault_api.catalog.query_types import Identity, SnapshotRef

MODEL: Literal["gpt-4.1-mini-2025-04-14"] = "gpt-4.1-mini-2025-04-14"
PROMPT_VERSION = "recognition-14a-v1"
SCHEMA_VERSION = "recognition-14a-v1"
RESERVATION = Decimal("0.02")
MAX_ATTEMPTS = 10
MAX_OUTPUT = 2048
TEXT_BYTES = 16000
TIMEOUT = 60
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Short = Annotated[str, Field(min_length=1, max_length=240)]
Identifier = Annotated[str, Field(min_length=1, max_length=80)]
Outcome = Literal[
    "candidates", "unknown", "insufficient_evidence", "mixed_sets", "custom_build", "non_lego"
]


class PilotError(ValueError):
    """Fixed codes only. Never include native exception text or private input."""


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)


class Proposal(StrictModel):
    kind: Literal["set", "minifigure"]
    namespace: Identifier
    identifier: Identifier


class Candidate(Proposal):
    rank: Annotated[int, Field(ge=1, le=3)]
    confidence_uncalibrated: Annotated[float, Field(ge=0, le=1)]
    supporting_visual_clues: Annotated[list[Short], Field(max_length=5)]
    supporting_text_clues: Annotated[list[Short], Field(max_length=5)]
    contradictions: Annotated[list[Short], Field(max_length=5)]


class ObjectResult(StrictModel):
    object_description: Short
    outcome: Outcome
    candidates: Annotated[list[Candidate], Field(max_length=3)]
    additional_view_requested: Short | None

    @model_validator(mode="after")
    def consistency(self) -> Self:
        if [c.rank for c in self.candidates] != list(range(1, len(self.candidates) + 1)):
            raise ValueError("non_contiguous_ranks")
        keys = [(c.kind, c.namespace, c.identifier) for c in self.candidates]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate_candidate")
        if self.outcome == "candidates" and not self.candidates:
            raise ValueError("missing_candidates")
        if self.outcome not in ("candidates", "mixed_sets") and self.candidates:
            raise ValueError("abstention_with_candidates")
        return self


class Recognition(StrictModel):
    objects: Annotated[list[ObjectResult], Field(min_length=1, max_length=6)]


class SelectedGroup(StrictModel):
    group: Annotated[str, Field(pattern=r"^G0[1-8]$")]
    files: Annotated[list[str], Field(min_length=1, max_length=2)]
    listing_text: Annotated[str, Field(max_length=1000)]
    independently_confirmed: bool
    labels_exhaustive: bool
    expected: Annotated[list[Proposal], Field(max_length=6)]
    expected_outcome: Outcome | None
    submission_rights_confirmed: bool
    personal_content_removed: bool


class Selection(StrictModel):
    groups: Annotated[list[SelectedGroup], Field(min_length=6, max_length=8)]

    @model_validator(mode="after")
    def unique_groups(self) -> Self:
        if len({g.group for g in self.groups}) != len(self.groups):
            raise ValueError("duplicate_group")
        return self


class PreparedImage(StrictModel):
    original_sha256: Digest
    transmitted_sha256: Digest


class PreparedGroup(StrictModel):
    group: Annotated[str, Field(pattern=r"^G0[1-8]$")]
    images: Annotated[list[PreparedImage], Field(min_length=1, max_length=2)]
    listing_text: Annotated[str, Field(max_length=1000)]
    independently_confirmed: bool
    labels_exhaustive: bool
    expected: Annotated[list[Proposal], Field(max_length=6)]
    expected_outcome: Outcome | None


class Prepared(StrictModel):
    recipe: Literal["recognition-rgb-1024-jpeg85-v1"]
    groups: Annotated[list[PreparedGroup], Field(min_length=6, max_length=8)]


class CatalogRequest(StrictModel):
    snapshot_id: str
    identities: Annotated[list[Proposal], Field(min_length=20, max_length=30)]


class ReferenceSubset(StrictModel):
    snapshot: SnapshotRef
    identities: Annotated[list[Identity], Field(min_length=20, max_length=30)]

    @model_validator(mode="after")
    def distinct(self) -> Self:
        if len({i.id for i in self.identities}) != len(self.identities):
            raise ValueError("duplicate_reference")
        return self


class Approval(StrictModel):
    approved: bool
    approved_by: Literal["Brian"]
    provider: Literal["openai"]
    model: Literal["gpt-4.1-mini-2025-04-14"]
    prepared_sha256: Digest
    subset_sha256: Digest
    protocol_sha256: Digest
    dollar_cap: Annotated[Decimal, Field(gt=0, le=Decimal("0.25"))]
    max_attempts: Annotated[int, Field(ge=1, le=10)]
    standard_api_retention_accepted: bool
    account_data_sharing_disabled_confirmed: bool
    selected_photos_and_text_approved: bool
    prices_verified_on: Literal["2026-10-02"]
    expires_on: str


class Attempt(StrictModel):
    group: str
    input_sha256: Digest
    state: Literal["reserved", "complete", "failed"]
    reserved_usd: Decimal
    latency_seconds: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_usd: Decimal | None = None

    @model_validator(mode="after")
    def reservation_fixed(self) -> Self:
        if self.reserved_usd != RESERVATION:
            raise ValueError("invalid_reservation")
        return self


class Ledger(StrictModel):
    approval_sha256: Digest
    attempts: Annotated[list[Attempt], Field(max_length=10)]
    stopped: bool = False
