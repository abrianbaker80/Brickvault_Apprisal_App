"""Internal snapshot-scoped contracts. No ORM rows, prices or HTTP surface."""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import JsonValue

from brickvault_api.catalog.types import Owner, Quantity, Target


class QueryState(StrEnum):
    OK = "ok"
    EMPTY = "verified_empty"
    UNKNOWN = "unknown"
    AMBIGUOUS = "ambiguous"
    UNAVAILABLE = "unavailable"
    INCOMPLETE = "incomplete"


class CatalogError(ValueError):
    """Only fixed diagnostic codes, never SQL, paths, credentials or raw input."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class ExtrasMode(StrEnum):
    EXCLUDE = "EXCLUDE_EXTRAS"
    INCLUDE = "INCLUDE_EXTRAS"


class FigureMode(StrEnum):
    KEEP = "KEEP_INTACT"
    EXPAND = "EXPAND_COMPONENTS"


class NestedMode(StrEnum):
    KEEP = "KEEP_INTACT"
    EXPAND = "EXPAND"


class Representation(StrEnum):
    COMPLETE_SET = "COMPLETE_SET"
    FIGURES_PLUS_REMAINING_BUILD = "FIGURES_PLUS_REMAINING_BUILD"
    PART_OUT_WITH_INTACT_FIGURES = "PART_OUT_WITH_INTACT_FIGURES"
    FULL_COMPONENT_PART_OUT = "FULL_COMPONENT_PART_OUT"
    # Existing low-level policy: expand figures while keeping subsets intact.
    COMPONENT_FIGURES_INTACT_SUBSETS = "COMPONENT_FIGURES_INTACT_SUBSETS"


class PhysicalState(StrEnum):
    """Completion is scoped to the selected revision, representation and policy.

    VERIFIED_COMPLETE proves exhaustive atomic components in that scope;
    COMPLETE_FOR_REPRESENTATION proves the selected saleable units, allowing
    intact assemblies whose internal piece count remains unknown. PARTIAL means
    known missing coverage, AMBIGUOUS conflicting evidence or unresolved choice,
    UNKNOWN absent proof, and BLOCKED invalid evidence or a violated hard guard.
    Neither complete state certifies a seller's actual box or condition.
    """

    VERIFIED_COMPLETE = "VERIFIED_COMPLETE"
    COMPLETE_FOR_REPRESENTATION = "COMPLETE_FOR_REPRESENTATION"
    PARTIAL = "PARTIAL"
    AMBIGUOUS = "AMBIGUOUS"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class ProofState(StrEnum):
    VERIFIED = "verified"
    UNKNOWN = "unknown"
    PARTIAL = "partial"
    AMBIGUOUS = "ambiguous"
    INVALID = "invalid"


@dataclass(frozen=True)
class SnapshotRef:
    id: UUID
    provider_id: UUID
    source_version_id: UUID
    scope: str
    synthetic: bool
    generation: int | None = None


@dataclass(frozen=True)
class Provenance:
    snapshot_id: UUID
    source_version_id: UUID
    evidence_id: UUID


@dataclass(frozen=True)
class IngestionEvidence:
    """Faithful ingestion only; never a physical source contract."""

    snapshot: SnapshotRef
    state: ProofState = ProofState.UNKNOWN
    manifest_digest: str | None = None
    validation_digest: str | None = None
    import_run_id: UUID | None = None
    parser_version: str | None = None
    importer_version: str | None = None
    files: tuple[tuple[str, str, str], ...] = ()


@dataclass(frozen=True)
class SourceContract:
    """Explicit reviewed assertions bound to exact contents; no inferred defaults.

    Synthetic proofs are accepted only on synthetic snapshots. Production callers
    must provide separately reviewed source evidence; bulk import supplies none.
    parts/figures/subsets assert exhaustive regular membership (including empty).
    partition covers disjoint direct occurrences, including intact composites.
    components asserts exact exhaustive replacement of the bound parent occurrence.
    choices asserts exhaustive candidate coverage and authoritative group semantics.
    extras asserts exhaustive optional spare membership, independently of regulars.
    child_extras additionally asserts inherited spares do not duplicate parent rows.
    """

    revision_id: UUID
    content_digest: str
    version: str
    synthetic: bool
    references: tuple[Provenance, ...]
    parts: ProofState = ProofState.UNKNOWN
    figures: ProofState = ProofState.UNKNOWN
    subsets: ProofState = ProofState.UNKNOWN
    partition: ProofState = ProofState.UNKNOWN
    components: ProofState = ProofState.UNKNOWN
    choices: ProofState = ProofState.UNKNOWN
    extras: ProofState = ProofState.UNKNOWN
    child_extras: ProofState = ProofState.UNKNOWN


@dataclass(frozen=True)
class EvidenceDimension:
    revision_id: UUID
    name: str
    state: ProofState
    references: tuple[Provenance, ...] = ()


@dataclass(frozen=True)
class RecordedInventory:
    revision_id: UUID
    provenance: Provenance
    content_digest: str
    semantic_profile: str
    figure_membership: str
    components: str
    # Direct recorded rows/quantities, never a physical denominator.
    rows: tuple[tuple[str, int, int, int], ...] | None


@dataclass(frozen=True)
class Completeness:
    source_coverage: str = "unknown"
    structural: str = "unknown"
    minifigure_membership: str = "unknown"
    component_availability: str = "unknown"
    matching_resolution: str = "unknown"
    physical_partition: str = "unknown"
    nested_availability: str = "unknown"


@dataclass(frozen=True)
class QueryResult[T]:
    snapshot: SnapshotRef
    state: QueryState
    data: T
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class Identity:
    id: UUID
    kind: str
    namespace: str
    identifier: str


@dataclass(frozen=True)
class ProviderIdentity:
    id: UUID
    provider_id: UUID
    provider: str
    native_type: str
    identifier: str


@dataclass(frozen=True)
class MappingStatus:
    id: UUID
    provider: ProviderIdentity
    target_id: UUID | None
    target_kind: str
    state: str
    method: str
    provenance: Provenance
    part_id: UUID | None = None
    color_id: UUID | None = None


@dataclass(frozen=True)
class SetMatch:
    identity: Identity
    source_identifier: str
    name: str
    provenance: Provenance
    rank: int | None = None


@dataclass(frozen=True)
class FigureMatch:
    identity: Identity
    name: str
    source_type: str | None
    classification: str | None
    provenance: Provenance


@dataclass(frozen=True)
class DefaultInventory:
    owner: Owner
    revision_id: UUID | None
    state: str
    rule_version: str | None
    reason: str
    provenance: Provenance | None = None


@dataclass(frozen=True)
class SetMetadata:
    match: SetMatch
    year: int | None
    theme: Identity | None
    theme_name: str | None
    source_piece_count: int | None
    source_status: str | None
    mappings: tuple[MappingStatus, ...]
    default: DefaultInventory
    completeness: Completeness
    image_url: str | None = None


@dataclass(frozen=True)
class InventoryVersion:
    id: UUID
    inventory_id: UUID
    owner: Owner
    provider: ProviderIdentity
    native_version: str
    numeric_version: int | None
    content_digest: str
    semantic_profile: str
    source_current: bool | None
    application_default: bool
    default: DefaultInventory
    completeness: Completeness
    provenance: Provenance


@dataclass(frozen=True)
class ChoiceMembership:
    group_id: UUID
    option_key: str
    native_role: str | None
    source_flags: dict[str, JsonValue]
    provenance: Provenance


@dataclass(frozen=True)
class BoundInventory:
    id: UUID
    child_revision_id: UUID
    review_state: str
    partition_state: str
    coverage_state: str
    provenance: Provenance


@dataclass(frozen=True)
class SourceLine:
    id: UUID
    revision_id: UUID
    locator: str
    native_type: str
    target: Target
    quantity: Quantity
    provenance: Provenance
    source_flags: dict[str, JsonValue]
    part_id: UUID | None = None
    color_id: UUID | None = None
    choice: ChoiceMembership | None = None
    binding: BoundInventory | None = None
    target_state: str = "known"
    color_semantic_state: str | None = None


@dataclass(frozen=True)
class ChoiceBundle:
    key: str
    line_ids: tuple[UUID, ...]


@dataclass(frozen=True)
class ChoiceGroup:
    id: UUID
    revision_id: UUID
    native_key: str
    state: str
    minimum: int | None
    maximum: int | None
    bundles: tuple[ChoiceBundle, ...]
    provenance: Provenance


@dataclass(frozen=True)
class Inventory:
    version: InventoryVersion
    lines: tuple[SourceLine, ...]
    groups: tuple[ChoiceGroup, ...]
    extras_mode: ExtrasMode = ExtrasMode.INCLUDE
    contract: SourceContract | None = None
    relations_observed: bool = True


@dataclass(frozen=True)
class FigureMembership:
    identity: Identity
    source_type: str | None
    classification: str | None
    mappings: tuple[MappingStatus, ...]
    line: SourceLine
    component_state: str


@dataclass(frozen=True)
class PartRelationship:
    id: UUID
    parent: Identity
    child: Identity
    relation_code: str
    meaning: str | None
    direction: Literal["outgoing", "incoming"]
    provenance: Provenance


@dataclass(frozen=True)
class ExpansionPolicy:
    figures: FigureMode = FigureMode.KEEP
    nested: NestedMode = NestedMode.KEEP
    extras: ExtrasMode = ExtrasMode.EXCLUDE
    selections: dict[UUID, frozenset[str]] = field(default_factory=dict)
    max_depth: int = 32
    max_nodes: int = 10000


@dataclass(frozen=True)
class LineageStep:
    revision_id: UUID
    line_id: UUID
    provenance: Provenance
    choice: ChoiceMembership | None
    binding: BoundInventory | None
    color_semantic_state: str | None = None


@dataclass(frozen=True)
class PhysicalLine:
    target: Target
    quantity: Quantity
    part_id: UUID | None
    color_id: UUID | None
    lineage: tuple[LineageStep, ...]
    allocation: Literal["inventory", "removed_figure", "remaining_build"] = "inventory"


@dataclass(frozen=True)
class ExpansionIssue:
    code: str
    revision_id: UUID
    path: tuple[UUID, ...]
    group_id: UUID | None = None
    state: PhysicalState = PhysicalState.UNKNOWN


@dataclass(frozen=True)
class GatedResult[T]:
    status: Literal["supported", "blocked"]
    value: T | None
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class PhysicalAssessment:
    representation: Representation
    rule_version: str
    snapshot: SnapshotRef
    root_revision_id: UUID
    state: PhysicalState
    dimensions: tuple[EvidenceDimension, ...]
    reasons: tuple[str, ...]
    recorded: tuple[RecordedInventory, ...]
    ingestion: IngestionEvidence | None
    policy: ExpansionPolicy
    contract_versions: tuple[tuple[UUID, str], ...]
    whole_set_id: UUID | None = None
    saleable_quantity: int | None = None
    physical_piece_count: int | None = None

    @property
    def admitted(self) -> bool:
        return self.state in (
            PhysicalState.VERIFIED_COMPLETE,
            PhysicalState.COMPLETE_FOR_REPRESENTATION,
        )

    def evaluate[T](self, calculate: Callable[[], T]) -> GatedResult[T]:
        """Physical gate only. Callers must separately gate economic evidence."""
        if not self.admitted:
            return GatedResult("blocked", None, self.reasons)
        return GatedResult("supported", calculate(), ())


@dataclass(frozen=True)
class Expansion:
    root_revision_id: UUID
    policy: ExpansionPolicy
    lines: tuple[PhysicalLine, ...]
    issues: tuple[ExpansionIssue, ...]
    completeness: Completeness
    nodes: int
    assessment: PhysicalAssessment

    def __post_init__(self) -> None:
        if self.lines and not self.assessment.admitted:
            raise ValueError("unadmitted_physical_contents")


@dataclass(frozen=True)
class ContainmentScope:
    inventories: Literal["application_default", "all_versions"] = "application_default"
    traversal: Literal["direct", "expanded"] = "direct"
    extras: ExtrasMode = ExtrasMode.EXCLUDE
    include_possible: bool = False
    selections: dict[UUID, frozenset[str]] = field(default_factory=dict)
    max_sets: int = 2000
    max_nodes: int = 10000


@dataclass(frozen=True)
class ContainingSet:
    identity: Identity
    presence: Literal["proven", "possible"]
    revision_ids: tuple[UUID, ...]
    evidence_ids: tuple[UUID, ...]


@dataclass(frozen=True)
class Containment:
    scope: ContainmentScope
    sets: tuple[ContainingSet, ...]
    proven_count: int
    possible_count: int
    unassessed_set_ids: tuple[UUID, ...]
    # Exact SQL count; IDs are a bounded diagnostic sample when coverage is large.
    unassessed_set_count: int | None = None
