"""Set-based candidate construction; no ORM objects or per-row SQL inserts."""

from collections.abc import Callable
from typing import Any
from uuid import UUID

from brickvault_api.catalog.build_steps import BuildInspector, BuildSteps
from brickvault_api.catalog.connection import CatalogConnection
from brickvault_api.providers.rebrickable.colors import COLOR_STATE_SQL
from brickvault_api.providers.rebrickable.records import PROFILES, RELATIONS, SourceError

IDENTITIES = (
    ("theme", "themes", "id"),
    ("color", "colors", "id"),
    ("part_category", "part_categories", "id"),
    ("part", "parts", "part_num"),
    ("set", "sets", "set_num"),
    ("minifigure", "minifigs", "fig_num"),
)

# Bound the full INSERT (including indexes and per-row constraint triggers),
# while every batch remains inside the caller's one candidate transaction.
INVENTORY_LINE_BATCH_SPAN = 100_000


def build_candidate(
    connection: CatalogConnection,
    run: UUID,
    source: UUID,
    snapshot: UUID,
    provider: UUID,
    namespace: str,
    prior: UUID | None,
    checkpoint: Callable[[str], None],
    progress: Callable[[dict[str, Any]], None] = lambda event: None,
    inspector: BuildInspector | None = None,
) -> dict[str, dict[str, int]]:
    params = {
        "run": run,
        "source": source,
        "snapshot": snapshot,
        "provider": provider,
        "namespace": namespace,
        "prior": prior,
    }

    steps = BuildSteps(connection, run, snapshot, progress, inspector)

    def execute(operation: str, statement: str) -> int:
        return steps.execute(operation, statement, params).rowcount

    for dataset in PROFILES:
        # Existing evidence can be reused when a new importer version processes frozen bytes.
        conflict = steps.execute(
            f"evidence_conflict:{dataset}",
            f"""SELECT 1 FROM catalog_stage_{dataset} s
            JOIN catalog_evidence e ON e.source_file_id=s.source_file_id AND e.locator=s.row_number::text
            WHERE s.run_id=%(run)s AND (e.row_sha256<>s.row_sha256 OR e.native_values<>s.native_values) LIMIT 1""",
            params,
        ).fetchone()
        if conflict:
            raise SourceError("source_evidence_conflict", dataset)
        # Only preexisting evidence needs reconciliation. New evidence is inserted
        # with its staging-reserved UUID already correct. Reconciling after INSERT
        # rewrites every fresh row and can join a whole newly populated file group
        # against itself using statistics from tiny retained source history.
        execute(
            f"evidence_reconcile:{dataset}",
            f"""UPDATE catalog_stage_{dataset} s SET evidence_id=e.id FROM catalog_evidence e
            WHERE s.run_id=%(run)s AND e.source_file_id=s.source_file_id AND e.locator=s.row_number::text""",
        )
        inserted = execute(
            f"evidence_insert:{dataset}",
            f"""INSERT INTO catalog_evidence(id,source_file_id,source_version_id,locator,native_key,native_values,row_sha256)
            SELECT evidence_id,source_file_id,source_version_id,row_number::text,native_key,native_values,row_sha256
            FROM catalog_stage_{dataset} s WHERE run_id=%(run)s
            AND NOT EXISTS (SELECT 1 FROM catalog_evidence e WHERE e.source_file_id=s.source_file_id AND e.locator=s.row_number::text)""",
        )
        if inserted > 0:
            # Failed builds can leave a large reusable heap with tiny historical
            # estimates. Later datasets read this growing evidence population in
            # the same transaction, where autovacuum cannot see the new rows.
            # Refresh at each changed dataset boundary, including the final one
            # consumed by identity construction and validation. Reuse adds none.
            execute(f"evidence_statistics:{dataset}", "ANALYZE catalog_evidence")

    reuse: dict[str, dict[str, int]] = {}
    for kind, dataset, key in (
        *IDENTITIES,
        ("inventory", "inventories", "id"),
        ("element", "elements", "element_id"),
    ):
        conflict = steps.execute(
            f"provider_identity_conflict:{kind}",
            f"""SELECT 1 FROM catalog_stage_{dataset} s JOIN catalog_provider_identity p
            ON p.provider_id=%(provider)s AND p.native_entity_type='{kind}' AND p.exact_identifier=s.{key}::text
            WHERE s.run_id=%(run)s AND p.canonical_kind<>'{kind}' LIMIT 1""",
            params,
        ).fetchone()
        if conflict:
            raise SourceError("provider_identity_conflict", dataset)
        execute(
            f"provider_identity_reconcile:{kind}",
            f"""UPDATE catalog_stage_{dataset} s SET reserved_provider_id=p.id FROM catalog_provider_identity p
            WHERE s.run_id=%(run)s AND p.provider_id=%(provider)s AND p.native_entity_type='{kind}' AND p.exact_identifier=s.{key}::text""",
        )
        execute(
            f"provider_identity_insert:{kind}",
            f"""INSERT INTO catalog_provider_identity(id,provider_id,native_entity_type,exact_identifier,canonical_kind,first_evidence_id,source_version_id)
            SELECT reserved_provider_id,%(provider)s,'{kind}',{key}::text,'{kind}',evidence_id,%(source)s
            FROM catalog_stage_{dataset} WHERE run_id=%(run)s ON CONFLICT DO NOTHING""",
        )
        if kind in ("inventory", "element"):
            continue
        # No fuzzy matching, and competing historical mappings cannot silently choose a target.
        conflict = steps.execute(
            f"mapping_conflict:{kind}",
            f"""SELECT 1 FROM {kind}_provider_mapping m
            JOIN catalog_snapshot v ON v.id=m.snapshot_id
            JOIN catalog_stage_{dataset} s ON s.reserved_provider_id=m.provider_identity_id AND s.run_id=%(run)s
            WHERE v.state IN ('validated','accepted') AND m.review_state='verified'
            GROUP BY m.provider_identity_id HAVING count(DISTINCT m.{kind}_id)>1 LIMIT 1""",
            params,
        ).fetchone()
        if conflict:
            raise SourceError("canonical_mapping_conflict", dataset)
        execute(
            f"canonical_reconcile:{kind}",
            f"""UPDATE catalog_stage_{dataset} s SET reserved_id=c.id FROM catalog_{kind} c
            WHERE s.run_id=%(run)s AND c.namespace=%(namespace)s AND c.identifier=s.{key}::text""",
        )
        conflict = steps.execute(
            f"canonical_conflict:{kind}",
            f"""SELECT 1 FROM catalog_stage_{dataset} s
            JOIN {kind}_provider_mapping m ON m.provider_identity_id=s.reserved_provider_id AND m.review_state='verified'
            JOIN catalog_snapshot v ON v.id=m.snapshot_id AND v.state IN ('validated','accepted')
            JOIN catalog_{kind} c ON c.namespace=%(namespace)s AND c.identifier=s.{key}::text
            WHERE s.run_id=%(run)s AND c.id<>m.{kind}_id LIMIT 1""",
            params,
        ).fetchone()
        if conflict:
            raise SourceError("canonical_mapping_conflict", dataset)
        execute(
            f"mapping_reconcile:{kind}",
            f"""UPDATE catalog_stage_{dataset} s SET reserved_id=m.{kind}_id FROM {kind}_provider_mapping m
            JOIN catalog_snapshot v ON v.id=m.snapshot_id AND v.state IN ('validated','accepted')
            WHERE s.run_id=%(run)s AND m.provider_identity_id=s.reserved_provider_id AND m.review_state='verified'""",
        )
        new = execute(
            f"canonical_insert:{kind}",
            f"""INSERT INTO catalog_{kind}(id,namespace,identifier,creation_evidence_id)
            SELECT reserved_id,%(namespace)s,{key}::text,evidence_id FROM catalog_stage_{dataset} s
            WHERE run_id=%(run)s AND NOT EXISTS(SELECT 1 FROM catalog_{kind} c WHERE c.id=s.reserved_id)""",
        )
        total = steps.execute(
            f"identity_total:{kind}",
            f"SELECT count(*) AS n FROM catalog_stage_{dataset} WHERE run_id=%(run)s",
            params,
        ).fetchone()
        absent = steps.execute(
            f"identity_not_observed:{kind}",
            f"""SELECT count(*) AS n FROM catalog_{kind}_fact f
            WHERE f.snapshot_id=%(prior)s AND NOT EXISTS(SELECT 1 FROM catalog_stage_{dataset} s WHERE s.run_id=%(run)s AND s.reserved_id=f.{kind}_id)""",
            params,
        ).fetchone()
        previous_values = (
            "jsonb_build_object("
            + ",".join(f"'{name}',e.native_values->'{name}'" for name in PROFILES[dataset].names)
            + ")"
        )
        current_values = (
            "jsonb_build_object("
            + ",".join(f"'{name}',s.native_values->'{name}'" for name in PROFILES[dataset].names)
            + ")"
        )
        changed = steps.execute(
            f"identity_changed:{kind}",
            f"""SELECT count(*) AS n FROM catalog_stage_{dataset} s
            JOIN catalog_{kind}_fact f ON f.snapshot_id=%(prior)s AND f.{kind}_id=s.reserved_id
            JOIN catalog_evidence e ON e.id=f.evidence_id WHERE s.run_id=%(run)s
            AND {previous_values} IS DISTINCT FROM {current_values}""",
            params,
        ).fetchone()
        reuse[kind] = {
            "new": new,
            "reused": int(total["n"]) - new if total else 0,
            "not_observed": int(absent["n"]) if absent else 0,
            "changed": int(changed["n"]) if changed else 0,
        }
    checkpoint("identities_reconciled")

    for kind, dataset, key in IDENTITIES:
        columns, values, joins = "", "", ""
        if kind == "theme":
            columns, values = ",parent_theme_id", ",p.reserved_id"
            joins = " LEFT JOIN catalog_stage_themes p ON p.run_id=s.run_id AND p.id=s.parent_id"
        elif kind == "color":
            columns, values = (
                ",rgb,is_transparent,semantic_state",
                ",s.rgb,s.is_trans," + COLOR_STATE_SQL.format(alias="s"),
            )
        elif kind == "part":
            columns, values = ",part_category_id,source_attributes", ",p.reserved_id,'{}'::jsonb"
            joins = (
                " JOIN catalog_stage_part_categories p ON p.run_id=s.run_id AND p.id=s.part_cat_id"
            )
        elif kind == "set":
            columns = ",theme_id,year,source_piece_count,base_number,suffix"
            values = ",p.reserved_id,s.year,s.num_parts,substring(s.set_num from '^([0-9]+)-[0-9]+$'),substring(s.set_num from '^[0-9]+-([0-9]+)$')"
            joins = " JOIN catalog_stage_themes p ON p.run_id=s.run_id AND p.id=s.theme_id"
        elif kind == "minifigure":
            columns, values = ",source_type,source_piece_count", ",'minifigure',s.num_parts"
        execute(
            f"facts:{kind}",
            f"""INSERT INTO catalog_{kind}_fact(snapshot_id,source_version_id,evidence_id,{kind}_id,source_identifier,source_name,display_name{columns})
            SELECT %(snapshot)s,%(source)s,s.evidence_id,s.reserved_id,s.{key}::text,s.name,s.name{values}
            FROM catalog_stage_{dataset} s {joins} WHERE s.run_id=%(run)s""",
        )
        if kind == "color":
            # Observation joins must see this candidate's color distribution.
            # Retained tiny-table statistics estimated one color, causing repeated
            # current-run inventory scans after a large part/color intermediate.
            # Analyze in the constructing transaction: autovacuum cannot see these
            # uncommitted facts. This changes no historical rows or query semantics.
            execute("color_fact_statistics", "ANALYZE catalog_color_fact")
        mapped = execute(
            f"mappings:{kind}",
            f"""INSERT INTO {kind}_provider_mapping(id,snapshot_id,source_version_id,evidence_id,provider_identity_id,canonical_kind,{kind}_id,method,review_state,first_observed_at,last_observed_at)
            SELECT gen_random_uuid(),%(snapshot)s,%(source)s,s.evidence_id,s.reserved_provider_id,'{kind}',s.reserved_id,'direct','verified',v.acquired_start,v.acquired_end
            FROM catalog_stage_{dataset} s JOIN catalog_source_version v ON v.id=%(source)s WHERE s.run_id=%(run)s""",
        )
        if mapped > 0:
            # The generated metadata checks join each candidate's mapping group.
            # Tiny historical snapshot estimates can materialize that whole group
            # for every staged entity. Publish the new distribution explicitly.
            execute(f"mapping_statistics:{kind}", f"ANALYZE {kind}_provider_mapping")
    execute(
        "set_aliases",
        """INSERT INTO catalog_set_alias(id,snapshot_id,source_version_id,evidence_id,set_id,namespace,normalized_key,alias_kind)
        SELECT gen_random_uuid(),snapshot_id,source_version_id,evidence_id,set_id,%(namespace)s,source_identifier,'exact' FROM catalog_set_fact WHERE snapshot_id=%(snapshot)s
        UNION ALL SELECT gen_random_uuid(),snapshot_id,source_version_id,evidence_id,set_id,%(namespace)s,base_number,'base' FROM catalog_set_fact WHERE snapshot_id=%(snapshot)s AND base_number IS NOT NULL""",
    )
    for dataset in ("inventory_parts", "elements"):
        execute(
            f"part_color_identity:{dataset}",
            f"""INSERT INTO part_color_identity(id,part_id,color_id,creation_evidence_id)
            SELECT DISTINCT ON (p.reserved_id,c.reserved_id) s.reserved_id,p.reserved_id,c.reserved_id,s.evidence_id
            FROM catalog_stage_{dataset} s JOIN catalog_stage_parts p ON p.run_id=s.run_id AND p.part_num=s.part_num
            JOIN catalog_stage_colors c ON c.run_id=s.run_id AND c.id=s.color_id
            WHERE s.run_id=%(run)s ORDER BY p.reserved_id,c.reserved_id,s.row_number ON CONFLICT(part_id,color_id) DO NOTHING""",
        )
        execute(
            f"part_color_observations:{dataset}",
            f"""INSERT INTO part_color_observation(snapshot_id,source_version_id,evidence_id,part_color_id,part_id,color_id,semantic_state)
            SELECT %(snapshot)s,%(source)s,s.evidence_id,pc.id,p.reserved_id,c.reserved_id,CASE WHEN cf.semantic_state='known' THEN 'known' ELSE 'unresolved' END
            FROM catalog_stage_{dataset} s JOIN catalog_stage_parts p ON p.run_id=s.run_id AND p.part_num=s.part_num
            JOIN catalog_stage_colors c ON c.run_id=s.run_id AND c.id=s.color_id
            JOIN catalog_color_fact cf ON cf.snapshot_id=%(snapshot)s AND cf.color_id=c.reserved_id
            JOIN part_color_identity pc ON pc.part_id=p.reserved_id AND pc.color_id=c.reserved_id WHERE s.run_id=%(run)s""",
        )
    execute(
        "inventories",
        """INSERT INTO catalog_inventory(id,provider_identity_id,canonical_kind)
        SELECT reserved_id,reserved_provider_id,'inventory' FROM catalog_stage_inventories WHERE run_id=%(run)s ON CONFLICT(provider_identity_id) DO NOTHING""",
    )
    execute(
        "inventory_revisions",
        """INSERT INTO catalog_inventory_revision(id,snapshot_id,source_version_id,evidence_id,inventory_id,set_id,minifigure_id,native_version,numeric_version,content_digest,semantic_profile,structural_state,figure_membership_state,component_state)
        SELECT gen_random_uuid(),%(snapshot)s,%(source)s,i.evidence_id,c.id,s.reserved_id,f.reserved_id,i.version::text,i.version,i.row_sha256,
            'rebrickable-bulk-live-unverified-v1','valid',
            CASE WHEN EXISTS(SELECT 1 FROM catalog_stage_inventory_minifigs l WHERE l.run_id=i.run_id AND l.inventory_id=i.id) THEN 'complete' ELSE 'unknown' END,'unknown'
        FROM catalog_stage_inventories i JOIN catalog_inventory c ON c.provider_identity_id=i.reserved_provider_id
        LEFT JOIN catalog_stage_sets s ON s.run_id=i.run_id AND s.set_num=i.set_num
        LEFT JOIN catalog_stage_minifigs f ON f.run_id=i.run_id AND f.fig_num=i.set_num WHERE i.run_id=%(run)s""",
    )
    revision_join = """JOIN catalog_stage_inventories i ON i.run_id=l.run_id AND i.id=l.inventory_id
        JOIN catalog_inventory c ON c.provider_identity_id=i.reserved_provider_id
        JOIN catalog_inventory_revision r ON r.snapshot_id=%(snapshot)s AND r.inventory_id=c.id"""
    extent = steps.execute(
        "inventory_part_line_extent",
        "SELECT max(row_number) AS last FROM catalog_stage_inventory_parts WHERE run_id=%(run)s",
        params,
    ).fetchone()
    last = extent["last"] if extent else None
    for batch, row_after in enumerate(range(0, last or 0, INVENTORY_LINE_BATCH_SPAN), start=1):
        steps.execute(
            "inventory_lines:parts" if batch == 1 else f"inventory_lines:parts:batch:{batch}",
            f"""INSERT INTO catalog_inventory_line(id,snapshot_id,source_version_id,evidence_id,revision_id,source_locator,native_type,part_color_id,part_id,color_id,regular_quantity,extra_quantity,source_flags)
        SELECT gen_random_uuid(),%(snapshot)s,%(source)s,l.evidence_id,r.id,'inventory_parts:'||l.row_number,'part',pc.id,p.reserved_id,col.reserved_id,
        CASE WHEN l.is_spare THEN 0 ELSE l.quantity END,CASE WHEN l.is_spare THEN l.quantity ELSE 0 END,jsonb_build_object('is_spare',l.is_spare,'quantity',l.quantity)
        FROM catalog_stage_inventory_parts l {revision_join}
        JOIN catalog_stage_parts p ON p.run_id=l.run_id AND p.part_num=l.part_num
        JOIN catalog_stage_colors col ON col.run_id=l.run_id AND col.id=l.color_id
        JOIN part_color_identity pc ON pc.part_id=p.reserved_id AND pc.color_id=col.reserved_id WHERE l.run_id=%(run)s
        AND l.row_number>%(row_after)s AND l.row_number<=%(row_through)s""",
            {
                **params,
                "row_after": row_after,
                "row_through": row_after + INVENTORY_LINE_BATCH_SPAN,
            },
        )
    for dataset, target, target_key, column, native_type in (
        ("inventory_minifigs", "minifigs", "fig_num", "minifigure_id", "minifigure"),
        ("inventory_sets", "sets", "set_num", "nested_set_id", "set"),
    ):
        execute(
            f"inventory_lines:{dataset}",
            f"""INSERT INTO catalog_inventory_line(id,snapshot_id,source_version_id,evidence_id,revision_id,source_locator,native_type,{column},regular_quantity,extra_quantity,source_flags)
            SELECT gen_random_uuid(),%(snapshot)s,%(source)s,l.evidence_id,r.id,'{dataset}:'||l.row_number,'{native_type}',t.reserved_id,l.quantity,0,jsonb_build_object('quantity',l.quantity)
            FROM catalog_stage_{dataset} l {revision_join} JOIN catalog_stage_{target} t ON t.run_id=l.run_id AND t.{target_key}=l.{target_key} WHERE l.run_id=%(run)s""",
        )
    # Expansion bindings consume these lines before the construction transaction
    # commits. The existing committed refresh still protects later validation;
    # it is too late to plan this earlier join against the candidate distribution.
    execute("inventory_line_build_statistics", "ANALYZE catalog_inventory_line")
    # Content digest uses source-native semantic rows, streamed in stable source order below.
    from brickvault_api.catalog.fingerprint import inventory_digests

    inventory_digests(connection, run, snapshot, steps)
    # Defaults and later containment consume the finished revision population.
    # Missing snapshot statistics made the containment coverage query repeatedly
    # probe inventory lines until the normal read timeout. Do not depend on an
    # automatic analyze racing the first candidate/active read after commit.
    execute("inventory_revision_statistics", "ANALYZE catalog_inventory_revision")
    for kind in ("set", "minifigure"):
        execute(
            f"default_inventory:{kind}",
            f"""INSERT INTO catalog_default_inventory(id,snapshot_id,source_version_id,evidence_id,{kind}_id,revision_id,selection_state,rule_version,reason)
            SELECT gen_random_uuid(),%(snapshot)s,%(source)s,f.evidence_id,f.{kind}_id,
            CASE WHEN choice.n=1 THEN choice.id ELSE NULL END,
            CASE WHEN choice.n=1 THEN 'selected' WHEN choice.n>1 THEN 'ambiguous' ELSE 'unknown' END,
            'highest-numeric-v1',CASE WHEN choice.n=1 THEN 'application_selected_not_provider_certified' WHEN choice.n>1 THEN 'highest_version_tie' ELSE 'no_inventory_observed' END
            FROM catalog_{kind}_fact f LEFT JOIN LATERAL (
                SELECT count(*) AS n,(array_agg(r.id ORDER BY r.id))[1] AS id FROM catalog_inventory_revision r
                WHERE r.snapshot_id=f.snapshot_id AND r.{kind}_id=f.{kind}_id AND r.numeric_version=(
                    SELECT max(v.numeric_version) FROM catalog_inventory_revision v WHERE v.snapshot_id=f.snapshot_id AND v.{kind}_id=f.{kind}_id)
            ) choice ON true WHERE f.snapshot_id=%(snapshot)s""",
        )
    execute(
        "expansion_bindings",
        """INSERT INTO inventory_expansion_binding(id,snapshot_id,source_version_id,evidence_id,parent_line_id,child_revision_id,minifigure_id,nested_set_id,review_state,partition_state,coverage_state)
        SELECT gen_random_uuid(),l.snapshot_id,l.source_version_id,l.evidence_id,l.id,d.revision_id,l.minifigure_id,l.nested_set_id,'unresolved','unknown','unknown'
        FROM catalog_inventory_line l JOIN catalog_default_inventory d ON d.snapshot_id=l.snapshot_id
        AND (d.set_id=l.nested_set_id OR d.minifigure_id=l.minifigure_id)
        WHERE l.snapshot_id=%(snapshot)s AND d.selection_state='selected'""",
    )
    execute(
        "element_mappings",
        """INSERT INTO element_mapping(id,snapshot_id,source_version_id,evidence_id,provider_identity_id,canonical_kind,part_color_id,part_id,color_id,method,review_state,first_observed_at,last_observed_at)
        SELECT gen_random_uuid(),%(snapshot)s,%(source)s,l.evidence_id,l.reserved_provider_id,'element',pc.id,p.reserved_id,c.reserved_id,'direct',CASE WHEN cf.semantic_state='known' THEN 'verified' ELSE 'unresolved' END,v.acquired_start,v.acquired_end
        FROM catalog_stage_elements l JOIN catalog_stage_parts p ON p.run_id=l.run_id AND p.part_num=l.part_num
        JOIN catalog_color_fact cf ON cf.snapshot_id=%(snapshot)s AND cf.source_identifier=l.color_id::text
        JOIN catalog_stage_colors c ON c.run_id=l.run_id AND c.id=l.color_id
        JOIN part_color_identity pc ON pc.part_id=p.reserved_id AND pc.color_id=c.reserved_id
        JOIN catalog_source_version v ON v.id=%(source)s WHERE l.run_id=%(run)s""",
    )
    for code, meaning in RELATIONS.items():
        steps.execute(
            f"part_relationships:{code}",
            """INSERT INTO part_relationship(id,snapshot_id,source_version_id,evidence_id,parent_part_id,child_part_id,source_relation_code,normalized_meaning)
            SELECT gen_random_uuid(),%s,%s,l.evidence_id,p.reserved_id,c.reserved_id,l.rel_type,%s
            FROM catalog_stage_part_relationships l JOIN catalog_stage_parts p ON p.run_id=l.run_id AND p.part_num=l.parent_part_num
            JOIN catalog_stage_parts c ON c.run_id=l.run_id AND c.part_num=l.child_part_num WHERE l.run_id=%s AND l.rel_type=%s""",
            (snapshot, source, meaning, run, code),
        )
    checkpoint("candidate_built")
    return reuse
