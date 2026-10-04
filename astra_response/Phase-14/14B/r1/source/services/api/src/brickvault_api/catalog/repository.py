"""Read-only, bounded catalog queries pinned to one accepted immutable snapshot."""

import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import replace
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID

from psycopg.errors import QueryCanceled

from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase, read_transaction
from brickvault_api.catalog.normalization import normalize_set_number
from brickvault_api.catalog.physical import ingestion_from_record
from brickvault_api.catalog.query_types import (
    BoundInventory,
    CatalogError,
    ChoiceBundle,
    ChoiceGroup,
    ChoiceMembership,
    Completeness,
    DefaultInventory,
    ExtrasMode,
    FigureMatch,
    FigureMembership,
    FigureMode,
    Identity,
    IngestionEvidence,
    Inventory,
    InventoryVersion,
    MappingStatus,
    NestedMode,
    PartRelationship,
    Provenance,
    ProviderIdentity,
    QueryResult,
    QueryState,
    SetMatch,
    SetMetadata,
    SnapshotRef,
    SourceContract,
    SourceLine,
)
from brickvault_api.catalog.search import FIGURE_SEARCH_SQL, MATCH_COLUMNS, SEARCH_SQL, search_input
from brickvault_api.catalog.types import (
    FigureTarget,
    Owner,
    PartTarget,
    Quantity,
    SetTarget,
    UnresolvedTarget,
)

MAX_ROWS = 10000
MAPPING_TABLES = {
    kind: kind + "_provider_mapping"
    for kind in ("set", "theme", "part_category", "part", "color", "minifigure")
}


def retained_set_image(row: dict[str, Any]) -> str | None:
    """Validate an exact source reference; never rewrite it or infer an image identity."""
    url = row.get("image_url")
    if (
        not isinstance(row.get("source_identifier"), str)
        or row.get("image_provider") != "rebrickable"
        or row.get("image_synthetic") is not False
        or row.get("image_set_number") != row.get("source_identifier")
        or row.get("image_dataset") != "sets"
        or not isinstance(url, str)
    ):
        return None
    # Reject whitespace, encoded path traversal, credentials, queries and all other paths.
    if not re.fullmatch(
        r"https://cdn\.rebrickable\.com/media/sets/[A-Za-z0-9_.-]+\.(?:jpg|png|webp)", url
    ):
        return None
    parsed = urlsplit(url)
    return (
        url
        if parsed.netloc == "cdn.rebrickable.com"
        and parsed.path.rsplit("/", 1)[-1].rsplit(".", 1)[0] == row["source_identifier"]
        else None
    )


def provenance(row: dict[str, Any]) -> Provenance:
    return Provenance(row["snapshot_id"], row["source_version_id"], row["evidence_id"])


def provider_identity(row: dict[str, Any]) -> ProviderIdentity:
    return ProviderIdentity(
        row["provider_identity_id"],
        row["provider_id"],
        row["provider_code"],
        row["native_entity_type"],
        row["exact_identifier"],
    )


def set_match(row: dict[str, Any]) -> SetMatch:
    return SetMatch(
        Identity(row["set_id"], "set", row["namespace"], row["identifier"]),
        row["source_identifier"],
        row["display_name"],
        provenance(row),
        row.get("rank"),
    )


def owner_of(row: dict[str, Any]) -> Owner:
    return (
        Owner(kind="set", id=row["set_id"])
        if row["set_id"] is not None
        else Owner(kind="minifigure", id=row["minifigure_id"])
    )


def default_of(row: dict[str, Any], owner: Owner) -> DefaultInventory:
    if row.get("selection_state") is None:
        return DefaultInventory(owner, None, "unknown", None, "inventory_unavailable")
    return DefaultInventory(
        owner,
        row["default_revision_id"],
        row["selection_state"],
        row["rule_version"],
        row["reason"],
        Provenance(row["snapshot_id"], row["source_version_id"], row["default_evidence_id"]),
    )


def version_of(row: dict[str, Any]) -> InventoryVersion:
    owner = owner_of(row)
    default = default_of(row, owner)
    return InventoryVersion(
        row["id"],
        row["inventory_id"],
        owner,
        provider_identity(row),
        row["native_version"],
        row["numeric_version"],
        row["content_digest"],
        row["semantic_profile"],
        row["source_current"],
        default.revision_id == row["id"],
        default,
        Completeness(
            structural=row["structural_state"],
            minifigure_membership=row["figure_membership_state"],
            component_availability=row["component_state"],
        ),
        provenance(row),
    )


VERSION_SQL = """SELECT r.*,p.id AS provider_identity_id,p.provider_id,p.native_entity_type,p.exact_identifier,v.code AS provider_code,
    d.revision_id AS default_revision_id,d.selection_state,d.rule_version,d.reason,d.evidence_id AS default_evidence_id
    FROM catalog_inventory_revision r JOIN catalog_inventory i ON i.id=r.inventory_id
    JOIN catalog_provider_identity p ON p.id=i.provider_identity_id JOIN catalog_provider v ON v.id=p.provider_id
    LEFT JOIN catalog_default_inventory d ON d.snapshot_id=r.snapshot_id AND (d.set_id=r.set_id OR d.minifigure_id=r.minifigure_id)
    WHERE r.snapshot_id=%(snapshot)s"""
VERSION_ORDER = ' ORDER BY r.numeric_version DESC NULLS LAST,p.exact_identifier COLLATE "C",r.id'


class PinnedCatalog:
    """Create through open_catalog; every SELECT uses the captured snapshot ID.

    Rows are converted here, never returned as SQL/ORM domain objects. A counter
    measures repository statements only, independently of connection guards.
    """

    def __init__(
        self,
        connection: CatalogConnection,
        snapshot: SnapshotRef,
        contracts: Mapping[UUID, SourceContract] | None = None,
    ) -> None:
        self._connection = connection
        self._snapshot = snapshot
        self.query_count = 0
        self._contracts = dict(contracts or {})
        self._ingestion: IngestionEvidence | None = None

    def ingestion_evidence(self) -> IngestionEvidence:
        """One read per pinned catalog, with no staging dependency or side effects."""
        if self._ingestion is None:
            rows = self._rows(
                """SELECT s.id AS snapshot_id,s.source_version_id,s.state AS snapshot_state,
                s.import_run_id,s.validation_digest,v.manifest_digest,v.source_metadata,
                r.source_version_id AS run_source_version_id,r.status,r.stage,r.counts,
                r.parser_version,r.importer_version,q.rules_version,q.state AS validation_state,
                q.digest AS report_digest,q.report,
                (SELECT coalesce(jsonb_agg(jsonb_build_object('dataset_name',f.dataset_name,
                    'compressed_sha256',f.compressed_sha256,'decompressed_sha256',f.decompressed_sha256)), '[]'::jsonb)
                 FROM catalog_source_file f WHERE f.source_version_id=s.source_version_id) AS files
                FROM catalog_snapshot s JOIN catalog_source_version v ON v.id=s.source_version_id
                JOIN catalog_import_run r ON r.id=s.import_run_id
                LEFT JOIN catalog_snapshot_validation q ON q.snapshot_id=s.id
                WHERE s.id=%(snapshot)s""",
                bound=1,
            )
            self._ingestion = ingestion_from_record(self.snapshot, rows[0] if rows else None)
        return self._ingestion

    def get_inventory_reference(self, revision_id: UUID) -> Inventory | None:
        """Set market references need identity/revision, never a contents scan."""
        rows = self._rows(
            VERSION_SQL + " AND r.id=%(revision)s", {"revision": revision_id}, bound=1
        )
        return Inventory(version_of(rows[0]), (), (), relations_observed=False) if rows else None

    @property
    def snapshot(self) -> SnapshotRef:
        return self._snapshot

    def _rows(
        self, statement: str, parameters: dict[str, Any] | None = None, *, bound: int = MAX_ROWS
    ) -> list[dict[str, Any]]:
        self.query_count += 1
        params = {**(parameters or {}), "snapshot": self.snapshot.id}
        # Each fixed SELECT contains a LIMIT or an exact unique predicate. Never
        # accept SQL, sort options or table identifiers from a caller.
        try:
            rows = self._connection.execute(statement, params).fetchmany(bound + 1)
        except QueryCanceled:
            raise CatalogError("query_time_limit") from None
        if len(rows) > bound:
            raise CatalogError("query_row_limit")
        return rows

    def resolve_set_number(self, value: str) -> QueryResult[tuple[SetMatch, ...]]:
        if not isinstance(value, str) or (key := normalize_set_number(value)) is None:
            raise CatalogError("invalid_input")
        numeric = re.fullmatch(r"[0-9]+", key) is not None
        rows = self._rows(
            f"""SELECT {MATCH_COLUMNS} FROM catalog_set_fact f JOIN catalog_set c ON c.id=f.set_id
            WHERE f.snapshot_id=%(snapshot)s AND (
                c.identifier=%(key)s OR f.source_identifier=%(key)s
                OR EXISTS(SELECT 1 FROM catalog_set_alias a WHERE a.snapshot_id=f.snapshot_id AND a.set_id=f.set_id AND a.normalized_key=%(key)s)
                OR (%(numeric)s AND (c.identifier ~ %(pattern)s)))
            ORDER BY c.identifier COLLATE "C",c.id LIMIT 1001""",
            {"key": key, "numeric": numeric, "pattern": "^" + re.escape(key) + "-[0-9]+$"},
            bound=1000,
        )
        matches = tuple(set_match(row) for row in rows)
        state = (
            QueryState.OK
            if len(matches) == 1
            else QueryState.AMBIGUOUS
            if matches
            else QueryState.UNKNOWN
        )
        return QueryResult(self.snapshot, state, matches)

    def search_sets(self, value: str, *, limit: int = 20) -> QueryResult[tuple[SetMatch, ...]]:
        query = search_input(value, limit)
        rows = self._rows(SEARCH_SQL, {"query": query, "limit": limit}, bound=limit)
        return QueryResult(
            self.snapshot,
            QueryState.OK if rows else QueryState.EMPTY,
            tuple(set_match(row) for row in rows),
        )

    def search_minifigures(
        self, value: str, *, limit: int = 20
    ) -> QueryResult[tuple[FigureMatch, ...]]:
        query = search_input(value, limit)
        rows = self._rows(FIGURE_SEARCH_SQL, {"query": query, "limit": limit}, bound=limit)
        return QueryResult(
            self.snapshot,
            QueryState.OK if rows else QueryState.EMPTY,
            tuple(
                FigureMatch(
                    Identity(row["id"], "minifigure", row["namespace"], row["identifier"]),
                    row["display_name"],
                    row["source_type"],
                    row["classification"],
                    provenance(row),
                )
                for row in rows
            ),
        )

    def resolve_identity(self, kind: str, identifier: str) -> QueryResult[tuple[Identity, ...]]:
        if (
            kind not in MAPPING_TABLES
            or not isinstance(identifier, str)
            or normalize_set_number(identifier) is None
        ):
            raise CatalogError("invalid_input")
        rows = self._rows(
            f"""SELECT c.id,c.namespace,c.identifier FROM catalog_{kind} c
            JOIN catalog_{kind}_fact f ON f.{kind}_id=c.id WHERE f.snapshot_id=%(snapshot)s AND c.identifier=%(identifier)s
            ORDER BY c.namespace COLLATE "C",c.identifier COLLATE "C",c.id LIMIT 1001""",
            {"identifier": identifier},
            bound=1000,
        )
        state = (
            QueryState.OK
            if len(rows) == 1
            else QueryState.AMBIGUOUS
            if rows
            else QueryState.UNKNOWN
        )
        return QueryResult(
            self.snapshot,
            state,
            tuple(Identity(row["id"], kind, row["namespace"], row["identifier"]) for row in rows),
        )

    def get_default_inventory(self, owner: Owner) -> QueryResult[DefaultInventory]:
        rows = self._rows(
            """SELECT *,revision_id AS default_revision_id,evidence_id AS default_evidence_id
            FROM catalog_default_inventory WHERE snapshot_id=%(snapshot)s AND
            ((%(kind)s='set' AND set_id=%(owner)s) OR (%(kind)s='minifigure' AND minifigure_id=%(owner)s))""",
            {"kind": owner.kind, "owner": owner.id},
            bound=1,
        )
        default = (
            default_of(rows[0], owner)
            if rows
            else DefaultInventory(owner, None, "unknown", None, "inventory_unavailable")
        )
        state = (
            QueryState.OK
            if default.state == "selected"
            else QueryState.AMBIGUOUS
            if default.state == "ambiguous"
            else QueryState.UNAVAILABLE
        )
        return QueryResult(
            self.snapshot,
            state,
            default,
            ()
            if state == QueryState.OK
            else (
                "default_inventory_ambiguous"
                if state == QueryState.AMBIGUOUS
                else "inventory_unavailable",
            ),
        )

    def list_inventory_versions(self, owner: Owner) -> QueryResult[tuple[InventoryVersion, ...]]:
        rows = self._rows(
            VERSION_SQL
            + " AND ((%(kind)s='set' AND r.set_id=%(owner)s) OR (%(kind)s='minifigure' AND r.minifigure_id=%(owner)s))"
            + VERSION_ORDER
            + " LIMIT 1001",
            {"kind": owner.kind, "owner": owner.id},
            bound=1000,
        )
        return QueryResult(
            self.snapshot,
            QueryState.OK if rows else QueryState.UNAVAILABLE,
            tuple(version_of(row) for row in rows),
        )

    def get_set(self, set_id: UUID) -> QueryResult[SetMetadata | None]:
        rows = self._rows(
            f"""SELECT {MATCH_COLUMNS},f.year,f.source_piece_count,f.source_status,
            t.theme_id,t.display_name AS theme_name,c2.namespace AS theme_namespace,c2.identifier AS theme_identifier,
            e.native_values->>'img_url' AS image_url,e.native_key->>'set_num' AS image_set_number,
            ip.code AS image_provider,sv.synthetic AS image_synthetic,sf.dataset_name AS image_dataset
            FROM catalog_set_fact f JOIN catalog_set c ON c.id=f.set_id
            LEFT JOIN catalog_evidence e ON e.id=f.evidence_id AND e.source_version_id=f.source_version_id
            LEFT JOIN catalog_source_file sf ON sf.id=e.source_file_id AND sf.source_version_id=e.source_version_id
            LEFT JOIN catalog_source_version sv ON sv.id=sf.source_version_id
            LEFT JOIN catalog_provider ip ON ip.id=sv.provider_id
            LEFT JOIN catalog_theme_fact t ON t.snapshot_id=f.snapshot_id AND t.theme_id=f.theme_id
            LEFT JOIN catalog_theme c2 ON c2.id=t.theme_id
            WHERE f.snapshot_id=%(snapshot)s AND f.set_id=%(id)s""",
            {"id": set_id},
            bound=1,
        )
        if not rows:
            return QueryResult(self.snapshot, QueryState.UNKNOWN, None, ("set_unknown",))
        row = rows[0]
        versions = self.list_inventory_versions(Owner(kind="set", id=set_id)).data
        default = self.get_default_inventory(Owner(kind="set", id=set_id)).data
        completeness = next(
            (version.completeness for version in versions if version.id == default.revision_id),
            Completeness(),
        )
        theme = (
            Identity(row["theme_id"], "theme", row["theme_namespace"], row["theme_identifier"])
            if row["theme_id"]
            else None
        )
        mappings = self._mappings("set", [set_id])
        return QueryResult(
            self.snapshot,
            QueryState.OK,
            SetMetadata(
                set_match(row),
                row["year"],
                theme,
                row["theme_name"],
                row["source_piece_count"],
                row["source_status"],
                mappings,
                default,
                completeness,
                retained_set_image(row),
            ),
        )

    def _mappings(
        self,
        kind: str,
        targets: list[UUID] | None = None,
        *,
        provider_id: UUID | None = None,
        identifier: str | None = None,
        native_type: str | None = None,
        part_id: UUID | None = None,
        color_id: UUID | None = None,
    ) -> tuple[MappingStatus, ...]:
        if kind not in MAPPING_TABLES and kind != "element":
            raise CatalogError("invalid_input")
        table = "element_mapping" if kind == "element" else MAPPING_TABLES[kind]
        target = "part_color_id" if kind == "element" else kind + "_id"
        extra = "m.part_id,m.color_id" if kind == "element" else "NULL AS part_id,NULL AS color_id"
        predicates = ""
        params: dict[str, Any] = {}
        if targets is not None:
            predicates += f" AND m.{target}=ANY(%(targets)s::uuid[])"
            params["targets"] = targets
        if provider_id is not None:
            predicates += " AND p.provider_id=%(provider)s AND p.exact_identifier=%(identifier)s"
            params.update(provider=provider_id, identifier=identifier)
        if native_type is not None:
            predicates += " AND p.native_entity_type=%(native)s"
            params["native"] = native_type
        if part_id is not None:
            predicates += " AND m.part_id=%(part)s AND m.color_id=%(color)s"
            params.update(part=part_id, color=color_id)
        rows = self._rows(
            f"""SELECT m.id,m.snapshot_id,m.source_version_id,m.evidence_id,m.method,m.review_state,m.{target} AS target_id,{extra},
            p.id AS provider_identity_id,p.provider_id,p.native_entity_type,p.exact_identifier,v.code AS provider_code
            FROM {table} m JOIN catalog_provider_identity p ON p.id=m.provider_identity_id JOIN catalog_provider v ON v.id=p.provider_id
            WHERE m.snapshot_id=%(snapshot)s {predicates}
            ORDER BY v.code COLLATE "C",p.native_entity_type COLLATE "C",p.exact_identifier COLLATE "C",m.review_state COLLATE "C",m.{target},m.id LIMIT 10001""",
            params,
        )
        return tuple(
            MappingStatus(
                row["id"],
                provider_identity(row),
                row["target_id"],
                "part_color" if kind == "element" else kind,
                row["review_state"],
                row["method"],
                provenance(row),
                row["part_id"],
                row["color_id"],
            )
            for row in rows
        )

    def get_provider_mapping_status(
        self, kind: str, provider_id: UUID, native_type: str, identifier: str
    ) -> QueryResult[tuple[MappingStatus, ...]]:
        if normalize_set_number(identifier) is None or not 1 <= len(native_type) <= 64:
            raise CatalogError("invalid_input")
        rows = self._mappings(
            kind, provider_id=provider_id, identifier=identifier, native_type=native_type
        )
        targets = {
            row.target_id for row in rows if row.state != "rejected" and row.target_id is not None
        }
        state = (
            QueryState.AMBIGUOUS
            if len(targets) > 1
            else QueryState.OK
            if any(row.state == "verified" for row in rows)
            else QueryState.UNKNOWN
            if rows
            else QueryState.UNAVAILABLE
        )
        return QueryResult(
            self.snapshot,
            state,
            rows,
            () if state == QueryState.OK else ("unresolved_provider_mapping",),
        )

    def get_element_mappings(
        self,
        *,
        provider_id: UUID | None = None,
        element_id: str | None = None,
        part_id: UUID | None = None,
        color_id: UUID | None = None,
    ) -> QueryResult[tuple[MappingStatus, ...]]:
        by_element = (
            provider_id is not None and element_id is not None and part_id is color_id is None
        )
        by_part = (
            part_id is not None
            and color_id is not None
            and provider_id is None
            and element_id is None
        )
        if not (by_element or by_part) or (
            element_id is not None and normalize_set_number(element_id) is None
        ):
            raise CatalogError("invalid_input")
        rows = self._mappings(
            "element",
            provider_id=provider_id,
            identifier=element_id,
            part_id=part_id,
            color_id=color_id,
        )
        targets: dict[UUID, set[UUID]] = {}
        for row in rows:
            if row.target_id is not None and row.state != "rejected":
                targets.setdefault(row.provider.id, set()).add(row.target_id)
        state = (
            QueryState.AMBIGUOUS
            if any(len(ids) > 1 for ids in targets.values())
            else QueryState.OK
            if rows
            else QueryState.UNAVAILABLE
        )
        return QueryResult(self.snapshot, state, rows)

    def get_part_relationships(self, part_id: UUID) -> QueryResult[tuple[PartRelationship, ...]]:
        rows = self._rows(
            """SELECT r.*,p.namespace AS parent_namespace,p.identifier AS parent_identifier,c.namespace AS child_namespace,c.identifier AS child_identifier
            FROM part_relationship r JOIN catalog_part p ON p.id=r.parent_part_id JOIN catalog_part c ON c.id=r.child_part_id
            WHERE r.snapshot_id=%(snapshot)s AND (r.parent_part_id=%(part)s OR r.child_part_id=%(part)s)
            ORDER BY p.identifier COLLATE "C",c.identifier COLLATE "C",r.source_relation_code COLLATE "C",r.id LIMIT 10001""",
            {"part": part_id},
        )
        result = tuple(
            PartRelationship(
                row["id"],
                Identity(
                    row["parent_part_id"], "part", row["parent_namespace"], row["parent_identifier"]
                ),
                Identity(
                    row["child_part_id"], "part", row["child_namespace"], row["child_identifier"]
                ),
                row["source_relation_code"],
                row["normalized_meaning"],
                "outgoing" if row["parent_part_id"] == part_id else "incoming",
                provenance(row),
            )
            for row in rows
        )
        return QueryResult(self.snapshot, QueryState.OK if result else QueryState.UNKNOWN, result)

    def _inventories(
        self, revision_ids: list[UUID], *, max_lines: int = MAX_ROWS
    ) -> dict[UUID, Inventory]:
        if not revision_ids:
            return {}
        if len(revision_ids) > MAX_ROWS or not 1 <= max_lines <= MAX_ROWS:
            raise CatalogError("query_row_limit")
        params = {"ids": revision_ids, "limit": max_lines + 1}
        versions = self._rows(
            VERSION_SQL + " AND r.id=ANY(%(ids)s::uuid[])" + VERSION_ORDER + " LIMIT 10001", params
        )
        lines = self._rows(
            'SELECT l.*,c.semantic_state AS color_semantic_state FROM catalog_inventory_line l LEFT JOIN catalog_color_fact c ON c.snapshot_id=l.snapshot_id AND c.color_id=l.color_id WHERE l.snapshot_id=%(snapshot)s AND l.revision_id=ANY(%(ids)s::uuid[]) ORDER BY l.revision_id,l.source_locator COLLATE "C",l.id LIMIT %(limit)s',
            params,
            bound=max_lines,
        )
        bindings = self._rows(
            """SELECT b.* FROM inventory_expansion_binding b JOIN catalog_inventory_line l ON l.snapshot_id=b.snapshot_id AND l.id=b.parent_line_id
            WHERE b.snapshot_id=%(snapshot)s AND l.revision_id=ANY(%(ids)s::uuid[]) ORDER BY b.parent_line_id LIMIT %(limit)s""",
            params,
            bound=max_lines,
        )
        candidates = self._rows(
            'SELECT * FROM inventory_matching_candidate WHERE snapshot_id=%(snapshot)s AND revision_id=ANY(%(ids)s::uuid[]) ORDER BY group_id,option_key COLLATE "C",line_id LIMIT %(limit)s',
            params,
            bound=max_lines,
        )
        groups = self._rows(
            'SELECT * FROM inventory_matching_group WHERE snapshot_id=%(snapshot)s AND revision_id=ANY(%(ids)s::uuid[]) ORDER BY revision_id,native_group_key COLLATE "C",id LIMIT 10001',
            params,
        )
        binding_by_line = {
            r["parent_line_id"]: BoundInventory(
                r["id"],
                r["child_revision_id"],
                r["review_state"],
                r["partition_state"],
                r["coverage_state"],
                provenance(r),
            )
            for r in bindings
        }
        choice_by_line = {
            r["line_id"]: ChoiceMembership(
                r["group_id"], r["option_key"], r["native_role"], r["source_flags"], provenance(r)
            )
            for r in candidates
        }
        line_groups: dict[UUID, list[SourceLine]] = {}
        for row in lines:
            target = (
                PartTarget(id=row["part_color_id"])
                if row["part_color_id"]
                else FigureTarget(id=row["minifigure_id"])
                if row["minifigure_id"]
                else SetTarget(id=row["nested_set_id"])
                if row["nested_set_id"]
                else UnresolvedTarget(id=row["unresolved_identity_id"])
            )
            line = SourceLine(
                row["id"],
                row["revision_id"],
                row["source_locator"],
                row["native_type"],
                target,
                Quantity(regular=row["regular_quantity"], extra=row["extra_quantity"]),
                provenance(row),
                row["source_flags"],
                row["part_id"],
                row["color_id"],
                choice_by_line.get(row["id"]),
                binding_by_line.get(row["id"]),
                "unresolved"
                if target.kind == "unresolved"
                or (target.kind == "part_color" and row["color_semantic_state"] != "known")
                else "known",
                row["color_semantic_state"],
            )
            line_groups.setdefault(row["revision_id"], []).append(line)
        bundles: dict[UUID, dict[str, list[UUID]]] = {}
        for candidate in candidates:
            bundles.setdefault(candidate["group_id"], {}).setdefault(
                candidate["option_key"], []
            ).append(candidate["line_id"])
        group_by_revision: dict[UUID, list[ChoiceGroup]] = {}
        for group in groups:
            item = ChoiceGroup(
                group["id"],
                group["revision_id"],
                group["native_group_key"],
                group["semantics_state"],
                group["min_options"],
                group["max_options"],
                tuple(
                    ChoiceBundle(key, tuple(ids))
                    for key, ids in bundles.get(group["id"], {}).items()
                ),
                provenance(group),
            )
            group_by_revision.setdefault(group["revision_id"], []).append(item)
        return {
            row["id"]: Inventory(
                version_of(row),
                tuple(line_groups.get(row["id"], ())),
                tuple(group_by_revision.get(row["id"], ())),
                contract=self._contracts.get(row["id"]),
            )
            for row in versions
        }

    def get_inventory(
        self, revision_id: UUID, *, extras: ExtrasMode = ExtrasMode.INCLUDE
    ) -> QueryResult[Inventory | None]:
        if not isinstance(extras, ExtrasMode):
            raise CatalogError("invalid_input")
        inventory = self._inventories([revision_id]).get(revision_id)
        if inventory is None:
            return QueryResult(
                self.snapshot, QueryState.UNAVAILABLE, None, ("inventory_unavailable",)
            )
        # Raw defaults to include: both source quantities remain visible. Excluding
        # extras filters spare-only lines but never rewrites their source quantities.
        if extras == ExtrasMode.EXCLUDE:
            inventory = replace(
                inventory,
                lines=tuple(line for line in inventory.lines if line.quantity.regular > 0),
                extras_mode=extras,
            )
        return QueryResult(self.snapshot, QueryState.OK, inventory)

    def load_graph(
        self,
        revision_ids: list[UUID],
        *,
        figures: FigureMode,
        nested: NestedMode,
        max_nodes: int = MAX_ROWS,
    ) -> dict[UUID, Inventory]:
        if not 1 <= max_nodes <= MAX_ROWS or len(revision_ids) > MAX_ROWS:
            raise CatalogError("invalid_input")
        rows = self._rows(
            """WITH RECURSIVE reachable(id) AS (
            SELECT id FROM catalog_inventory_revision WHERE snapshot_id=%(snapshot)s AND id=ANY(%(ids)s::uuid[])
            UNION
            SELECT b.child_revision_id FROM reachable r
            JOIN catalog_inventory_line l ON l.snapshot_id=%(snapshot)s AND l.revision_id=r.id
            JOIN inventory_expansion_binding b ON b.snapshot_id=%(snapshot)s AND b.parent_line_id=l.id
            WHERE (%(figures)s AND l.minifigure_id IS NOT NULL) OR (%(nested)s AND l.nested_set_id IS NOT NULL)
        ) SELECT id FROM reachable ORDER BY id LIMIT %(limit)s""",
            {
                "ids": revision_ids,
                "figures": figures == FigureMode.EXPAND,
                "nested": nested == NestedMode.EXPAND,
                "limit": max_nodes + 1,
            },
            bound=max_nodes,
        )
        return self._inventories([r["id"] for r in rows], max_lines=max_nodes)

    def get_inventory_minifigures(
        self, revision_id: UUID, *, extras: ExtrasMode = ExtrasMode.EXCLUDE
    ) -> QueryResult[tuple[FigureMembership, ...]]:
        result = self.get_inventory(revision_id, extras=extras)
        if result.data is None:
            return QueryResult(self.snapshot, result.state, (), result.issues)
        lines = [line for line in result.data.lines if line.target.kind == "minifigure"]
        ids = list({line.target.id for line in lines})
        facts = (
            self._rows(
                """SELECT f.*,c.namespace,c.identifier FROM catalog_minifigure_fact f JOIN catalog_minifigure c ON c.id=f.minifigure_id
            WHERE f.snapshot_id=%(snapshot)s AND f.minifigure_id=ANY(%(ids)s::uuid[]) ORDER BY c.identifier COLLATE "C",c.id LIMIT 10001""",
                {"ids": ids},
            )
            if ids
            else []
        )
        fact_by_id = {row["minifigure_id"]: row for row in facts}
        mappings = self._mappings("minifigure", ids) if ids else ()
        mappings_by_target: dict[UUID, list[MappingStatus]] = {}
        for mapping in mappings:
            if mapping.target_id is not None:
                mappings_by_target.setdefault(mapping.target_id, []).append(mapping)
        children = [line.binding.child_revision_id for line in lines if line.binding]
        versions = (
            self._rows(
                VERSION_SQL + " AND r.id=ANY(%(ids)s::uuid[])" + VERSION_ORDER + " LIMIT 10001",
                {"ids": children},
            )
            if children
            else []
        )
        components = {r["id"]: r["component_state"] for r in versions}
        members = []
        for line in lines:
            fact = fact_by_id[line.target.id]
            component = (
                components.get(line.binding.child_revision_id, "unavailable")
                if line.binding and line.binding.review_state == "verified"
                else "unavailable"
            )
            members.append(
                FigureMembership(
                    Identity(line.target.id, "minifigure", fact["namespace"], fact["identifier"]),
                    fact["source_type"],
                    fact["classification"],
                    tuple(mappings_by_target.get(line.target.id, ())),
                    line,
                    component,
                )
            )
        membership = result.data.version.completeness.minifigure_membership
        state = (
            QueryState.OK
            if lines and membership == "complete"
            else QueryState.EMPTY
            if not lines and membership in ("complete", "verified_empty")
            else QueryState.INCOMPLETE
        )
        return QueryResult(
            self.snapshot,
            state,
            tuple(members),
            ("minifigure_membership_unknown",) if state == QueryState.INCOMPLETE else (),
        )

    def get_minifigure_components(self, parent_line_id: UUID) -> QueryResult[Inventory | None]:
        rows = self._rows(
            """SELECT b.child_revision_id,b.review_state,b.coverage_state,b.partition_state
            FROM catalog_inventory_line l LEFT JOIN inventory_expansion_binding b ON b.snapshot_id=l.snapshot_id AND b.parent_line_id=l.id
            WHERE l.snapshot_id=%(snapshot)s AND l.id=%(line)s AND l.minifigure_id IS NOT NULL""",
            {"line": parent_line_id},
            bound=1,
        )
        if (
            not rows
            or rows[0]["child_revision_id"] is None
            or rows[0]["review_state"] != "verified"
        ):
            return QueryResult(
                self.snapshot, QueryState.UNAVAILABLE, None, ("component_inventory_unavailable",)
            )
        result = self.get_inventory(rows[0]["child_revision_id"])
        if result.data and (
            result.data.version.completeness.component_availability != "complete"
            or rows[0]["coverage_state"] != "complete"
        ):
            return replace(
                result, state=QueryState.INCOMPLETE, issues=("component_inventory_incomplete",)
            )
        return result


@contextmanager
def open_catalog(
    database: CatalogDatabase,
    *,
    snapshot_id: UUID | None = None,
    provider_id: UUID | None = None,
    scope: str | None = None,
    contracts: Mapping[UUID, SourceContract] | None = None,
    connection: CatalogConnection | None = None,
) -> Iterator[PinnedCatalog]:
    """One active-pointer read, then immutable snapshot keys even at READ COMMITTED."""
    if (
        snapshot_id is None and (provider_id is None or scope is None or not 1 <= len(scope) <= 128)
    ) or (snapshot_id is not None and (provider_id is not None or scope is not None)):
        raise CatalogError("invalid_input")
    with read_transaction(database, connection) as connection:
        connection.execute("SELECT set_config('statement_timeout','2000',true)")
        generation = None
        if snapshot_id is None:
            pointer = connection.execute(
                "SELECT snapshot_id,generation FROM catalog_active_snapshot WHERE provider_id=%s AND scope=%s",
                (provider_id, scope),
            ).fetchone()
            if not pointer or pointer["snapshot_id"] is None:
                raise CatalogError("catalog_unavailable")
            snapshot_id, generation = pointer["snapshot_id"], pointer["generation"]
        row = connection.execute(
            """SELECT s.id,s.source_version_id,s.scope,s.state,v.provider_id,v.synthetic
            FROM catalog_snapshot s JOIN catalog_source_version v ON v.id=s.source_version_id WHERE s.id=%s""",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            raise CatalogError("snapshot_unknown")
        if row["state"] != "accepted":
            raise CatalogError("snapshot_not_accepted")
        ref = SnapshotRef(
            row["id"],
            row["provider_id"],
            row["source_version_id"],
            row["scope"],
            row["synthetic"],
            generation,
        )
        yield PinnedCatalog(connection, ref, contracts)
