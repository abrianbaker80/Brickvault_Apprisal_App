"""Strict, private pilot contracts. Predictions never become confirmations."""

from decimal import Decimal
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from brickvault_api.catalog.query_types import Identity, SnapshotRef

MODEL: Literal["gpt-6-luna"] = "gpt-6-luna"
SOL_MODEL: Literal["gpt-6.1-sol"] = "gpt-6.1-sol"
SOL_PRICING_DATE = "2026-10-03"
SOL_INPUT_RATE = Decimal("2.00")
SOL_CACHED_RATE = Decimal("0.10")
SOL_WRITE_RATE = Decimal("2.50")
SOL_OUTPUT_RATE = Decimal("10.00")
SOL_CONTEXT_BOUND = 1050000
PROMPT_VERSION = "recognition-14a-v1"
SCHEMA_VERSION = "recognition-14a-v2"
PRICING_DATE = "2026-10-02"
INPUT_RATE = Decimal("0.10")
CACHED_RATE = Decimal("0.01")
WRITE_RATE = Decimal("0.125")
OUTPUT_RATE = Decimal("0.50")
MAX_ATTEMPTS = 10
MAX_OUTPUT = 2048
AMENDED_OUTPUT: Literal[16384] = 16384
TEXT_BYTES = 16000
TIMEOUT = 60
AMENDED_TIMEOUT: Literal[180] = 180
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
    objects: Annotated[list[ObjectResult], Field(min_length=1, max_length=12)]


class SelectedGroup(StrictModel):
    group: Annotated[str, Field(pattern=r"^G0[1-8]$")]
    files: Annotated[list[str], Field(min_length=1, max_length=2)]
    listing_text: Annotated[str, Field(max_length=1000)]
    independently_confirmed: bool
    labels_exhaustive: bool
    expected: Annotated[list[Proposal], Field(max_length=12)]
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
    expected: Annotated[list[Proposal], Field(max_length=12)]
    expected_outcome: Outcome | None


class Prepared(StrictModel):
    recipe: Literal["recognition-rgb-1024-jpeg85-v1"]
    groups: Annotated[list[PreparedGroup], Field(min_length=6, max_length=8)]


class CatalogRequest(StrictModel):
    snapshot_id: str
    identities: Annotated[list[Proposal], Field(min_length=1, max_length=30)]


class ReferenceSubset(StrictModel):
    snapshot: SnapshotRef
    identities: Annotated[list[Identity], Field(min_length=1, max_length=30)]

    @model_validator(mode="after")
    def distinct(self) -> Self:
        if len({i.id for i in self.identities}) != len(self.identities):
            raise ValueError("duplicate_reference")
        return self


class Approval(StrictModel):
    approved: bool
    approved_by: Literal["Brian"]
    provider: Literal["openai"]
    model: Literal["gpt-6-luna"]
    project_id: Annotated[str, Field(pattern=r"^proj_[A-Za-z0-9]+$")]
    prepared_sha256: Digest
    subset_sha256: Digest
    protocol_sha256: Digest
    dollar_cap: Annotated[Decimal, Field(gt=0, le=Decimal("10.00"))]
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
    reserved_usd: Annotated[Decimal, Field(gt=0, le=Decimal("10.00"))]
    input_token_bound: Annotated[int, Field(gt=0, le=1050000)]
    model: Literal["gpt-6-luna", "gpt-6.1-sol"] = MODEL
    prices_verified_on: Literal["2026-10-02", "2026-10-03"] = "2026-10-02"
    result_sha256: Digest | None = None
    reuse_count: Annotated[int, Field(ge=0)] = 0
    latency_seconds: float | None = None
    input_tokens: int | None = None
    cached_input_tokens: int | None = None
    cache_write_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    estimated_usd: Decimal | None = None
    cost_basis: Literal["token_details", "upper_bound_missing_details"] | None = None
    reported_billing_usd: None = None
    response_received: bool = False
    failure_code: str | None = None
    amendment_sha256: Digest | None = None
    protocol_sha256: Digest | None = None
    max_output_tokens: Literal[16384] | None = None
    request_deadline_seconds: Literal[180] | None = None
    result_filename: (
        Literal[
            "G07-amendment-v1-result.json", "G06-amendment-v1-result.json", "G06-sol-v1-result.json"
        ]
        | None
    ) = None
    predecessor_input_sha256: Digest | None = None

    @model_validator(mode="after")
    def model_limits(self) -> Self:
        if self.model == MODEL:
            if self.reserved_usd > Decimal("0.25") or self.input_token_bound > 922000:
                raise ValueError("original_model_limits")
            if (
                self.prices_verified_on != PRICING_DATE
                or self.result_filename == "G06-sol-v1-result.json"
            ):
                raise ValueError("original_model_metadata")
        elif (
            self.group != "G06"
            or self.prices_verified_on != SOL_PRICING_DATE
            or self.input_token_bound != SOL_CONTEXT_BOUND
            or self.max_output_tokens != AMENDED_OUTPUT
            or self.request_deadline_seconds != AMENDED_TIMEOUT
            or self.result_filename != "G06-sol-v1-result.json"
            or self.amendment_sha256 is None
            or self.protocol_sha256 is None
            or self.predecessor_input_sha256 is None
        ):
            raise ValueError("comparison_model_limits")
        return self


class Amendment(StrictModel):
    version: Literal["recognition-14a-limits-v1"]
    approved: bool
    approved_by: Literal["Brian"]
    accepted_review_commit: Literal["108f7f6d65a38ebead7701d3c0f7f2d62ed3b5ab"]
    parent_approval_sha256: Digest
    parent_ledger_sha256: Digest
    original_attempts_sha256: Digest
    prepared_sha256: Digest
    subset_sha256: Digest
    prior_protocol_sha256: Digest
    protocol_sha256: Digest
    order: Literal["G07_then_G06"]
    additional_attempts: Literal[2]
    g06_predecessor_input_sha256: Digest
    dollar_cap: Literal["10.00"]
    expires_on: str


class Ledger(StrictModel):
    approval_sha256: Digest
    attempts: Annotated[list[Attempt], Field(max_length=10)]
    stopped: bool = False


class ModelComparisonAmendment(StrictModel):
    version: Literal["recognition-14a-sol-v1"]
    approved: bool
    approved_by: Literal["Brian"]
    accepted_review_commit: Literal["c89583e40eb1c62620c1162bd1ac0c23bbf51c56"]
    parent_approval_sha256: Digest
    parent_ledger_sha256: Digest
    prior_attempts_sha256: Digest
    prepared_sha256: Digest
    subset_sha256: Digest
    prior_protocol_sha256: Digest
    protocol_sha256: Digest
    g06_request_sha256: Digest
    g06_predecessor_input_sha256: Digest
    g06_predecessor_result_sha256: Digest
    model: Literal["gpt-6.1-sol"]
    group: Literal["G06"]
    lifetime_attempt_number: Literal[9]
    additional_attempts: Literal[1]
    dollar_cap: Literal["10.00"]
    expires_on: str
