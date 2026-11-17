-- Evidence only: executed through guarded read-only transactions on schema 0019.
-- No 0020 function calls. Statement timeout 10-30 seconds, lock timeout 2 seconds.

-- inspect.py / transaction
SELECT current_setting('transaction_read_only') AS read_only, current_setting('transaction_isolation') AS isolation;

-- inspect.py / schema
SELECT version_num FROM alembic_version LIMIT 5;

-- inspect.py / active_catalog
SELECT p.code AS provider, a.scope, a.generation, s.id AS snapshot_id,
      s.state, s.source_version_id, v.synthetic, v.acquired_end, v.manifest_digest
      FROM catalog_active_snapshot a JOIN catalog_provider p ON p.id=a.provider_id
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id LIMIT 10;

-- inspect.py / mapping_rows
SELECT provider,item_type,review_state,closed_at IS NOT NULL AS closed,count(*) AS rows,
      count(DISTINCT COALESCE(minifigure_id,part_color_id,set_id)) AS distinct_targets
      FROM market_mapping_revision GROUP BY 1,2,3,4 ORDER BY 1,2,3,4 LIMIT 40;

-- inspect.py / scope_metadata
SELECT s.provider,s.suspended,p.version,p.fresh_seconds,p.mapping_seconds,
      p.interactive_limit,p.global_limit,p.retries,p.effective_at
      FROM provider_scope_state s JOIN market_policy p ON p.id=s.policy_id LIMIT 10;

-- inspect.py / retained_access
SELECT k.provider,k.item_type,r.outcome,r.failure,count(*) AS rows,
      min(r.started_at) AS first_started,max(r.finished_at) AS last_finished
      FROM provider_fetch_run r JOIN provider_cache_entry k ON k.id=r.cache_id
      GROUP BY 1,2,3,4 ORDER BY 1,2,3,4 LIMIT 30;

-- eligibility.py / catalog_denominators
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT
      (SELECT count(*) FROM catalog_set_fact f JOIN active a ON a.snapshot_id=f.snapshot_id) AS set_facts,
      (SELECT count(*) FROM catalog_default_inventory d JOIN active a ON a.snapshot_id=d.snapshot_id WHERE d.set_id IS NOT NULL AND d.selection_state='selected') AS selected_set_inventories,
      (SELECT count(*) FROM catalog_minifigure_fact f JOIN active a ON a.snapshot_id=f.snapshot_id) AS figure_facts;

-- eligibility.py / direct_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) , direct AS MATERIALIZED (
      SELECT l.*,r.set_id,COALESCE(l.minifigure_id,l.part_color_id) AS target_id,
      CASE WHEN l.minifigure_id IS NOT NULL THEN 'MINIFIG' ELSE 'PART' END AS item_type,
      NOT EXISTS(SELECT 1 FROM inventory_matching_candidate x WHERE x.line_id=l.id) AS no_choice,
      (l.minifigure_id IS NOT NULL OR cf.semantic_state='known') AS known
      FROM active a JOIN catalog_default_inventory d ON d.snapshot_id=a.snapshot_id
      JOIN catalog_inventory_revision r ON r.id=d.revision_id AND r.set_id=d.set_id
        AND r.snapshot_id=a.snapshot_id AND r.source_version_id=a.source_version_id
      JOIN catalog_inventory_line l ON l.revision_id=r.id AND l.snapshot_id=a.snapshot_id AND l.source_version_id=a.source_version_id
      LEFT JOIN catalog_color_fact cf ON cf.snapshot_id=a.snapshot_id AND cf.color_id=l.color_id
      WHERE d.selection_state='selected' AND d.set_id IS NOT NULL AND COALESCE(l.minifigure_id,l.part_color_id) IS NOT NULL
    ), checked AS (
      SELECT d.*,m.id AS eligible_mapping FROM direct d LEFT JOIN market_mapping_revision m
      ON m.provider='bricklink' AND m.closed_at IS NULL AND m.review_state='verified'
      AND COALESCE(m.minifigure_id,m.part_color_id)=d.target_id AND m.snapshot_id=d.snapshot_id AND m.source_version_id=d.source_version_id
      AND ((d.minifigure_id=m.minifigure_id AND m.item_type='MINIFIG' AND m.color_id IS NULL)
      OR (d.part_color_id=m.part_color_id AND m.item_type='PART' AND m.part_id=d.part_id AND m.canonical_color_id=d.color_id AND m.color_id IS NOT NULL))
      AND (SELECT count(*) FROM market_mapping_revision x WHERE x.provider='bricklink' AND x.closed_at IS NULL
        AND x.review_state='verified' AND COALESCE(x.minifigure_id,x.part_color_id)=d.target_id)=1
    ) SELECT item_type,count(*) AS direct_occurrences,count(DISTINCT target_id) AS direct_distinct_targets,
      count(*) FILTER(WHERE no_choice AND known) AS supported_occurrences_including_extras,
      count(DISTINCT target_id) FILTER(WHERE no_choice AND known) AS supported_distinct_targets_including_extras,
      count(*) FILTER(WHERE no_choice AND known AND regular_quantity>0) AS supported_regular_occurrences,
      count(DISTINCT target_id) FILTER(WHERE no_choice AND known AND regular_quantity>0) AS supported_regular_distinct_targets,
      count(*) FILTER(WHERE NOT no_choice) AS choice_occurrences,
      count(*) FILTER(WHERE NOT known) AS unknown_color_occurrences,
      count(DISTINCT eligible_mapping) FILTER(WHERE no_choice AND known) AS eligible_mapping_rows,
      count(DISTINCT target_id) FILTER(WHERE no_choice AND known AND eligible_mapping IS NOT NULL) AS eligible_distinct_targets,
      count(*) FILTER(WHERE no_choice AND known AND eligible_mapping IS NOT NULL) AS eligible_occurrences
      FROM checked GROUP BY item_type ORDER BY item_type;

-- eligibility.py / preferred_set_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) , direct AS MATERIALIZED (
      SELECT l.*,r.set_id,COALESCE(l.minifigure_id,l.part_color_id) AS target_id,
      CASE WHEN l.minifigure_id IS NOT NULL THEN 'MINIFIG' ELSE 'PART' END AS item_type,
      NOT EXISTS(SELECT 1 FROM inventory_matching_candidate x WHERE x.line_id=l.id) AS no_choice,
      (l.minifigure_id IS NOT NULL OR cf.semantic_state='known') AS known
      FROM active a JOIN catalog_default_inventory d ON d.snapshot_id=a.snapshot_id
      JOIN catalog_inventory_revision r ON r.id=d.revision_id AND r.set_id=d.set_id
        AND r.snapshot_id=a.snapshot_id AND r.source_version_id=a.source_version_id
      JOIN catalog_inventory_line l ON l.revision_id=r.id AND l.snapshot_id=a.snapshot_id AND l.source_version_id=a.source_version_id
      LEFT JOIN catalog_color_fact cf ON cf.snapshot_id=a.snapshot_id AND cf.color_id=l.color_id
      WHERE d.selection_state='selected' AND d.set_id IS NOT NULL AND COALESCE(l.minifigure_id,l.part_color_id) IS NOT NULL
    ), checked AS (
      SELECT d.*,m.id AS eligible_mapping FROM direct d LEFT JOIN market_mapping_revision m
      ON m.provider='bricklink' AND m.closed_at IS NULL AND m.review_state='verified'
      AND COALESCE(m.minifigure_id,m.part_color_id)=d.target_id AND m.snapshot_id=d.snapshot_id AND m.source_version_id=d.source_version_id
      AND ((d.minifigure_id=m.minifigure_id AND m.item_type='MINIFIG' AND m.color_id IS NULL)
      OR (d.part_color_id=m.part_color_id AND m.item_type='PART' AND m.part_id=d.part_id AND m.canonical_color_id=d.color_id AND m.color_id IS NOT NULL))
      AND (SELECT count(*) FROM market_mapping_revision x WHERE x.provider='bricklink' AND x.closed_at IS NULL
        AND x.review_state='verified' AND COALESCE(x.minifigure_id,x.part_color_id)=d.target_id)=1
    ) SELECT s.identifier,c.item_type,count(*) AS direct_occurrences,
      count(DISTINCT c.target_id) AS distinct_targets,
      count(*) FILTER(WHERE c.no_choice AND c.known AND c.eligible_mapping IS NOT NULL) AS eligible_occurrences
      FROM checked c JOIN catalog_set s ON s.id=c.set_id WHERE s.identifier='10350-1'
      GROUP BY 1,2 ORDER BY 1,2;

-- eligibility.py / onboarding_candidates
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) , direct AS MATERIALIZED (
      SELECT l.*,r.set_id,COALESCE(l.minifigure_id,l.part_color_id) AS target_id,
      CASE WHEN l.minifigure_id IS NOT NULL THEN 'MINIFIG' ELSE 'PART' END AS item_type,
      NOT EXISTS(SELECT 1 FROM inventory_matching_candidate x WHERE x.line_id=l.id) AS no_choice,
      (l.minifigure_id IS NOT NULL OR cf.semantic_state='known') AS known
      FROM active a JOIN catalog_default_inventory d ON d.snapshot_id=a.snapshot_id
      JOIN catalog_inventory_revision r ON r.id=d.revision_id AND r.set_id=d.set_id
        AND r.snapshot_id=a.snapshot_id AND r.source_version_id=a.source_version_id
      JOIN catalog_inventory_line l ON l.revision_id=r.id AND l.snapshot_id=a.snapshot_id AND l.source_version_id=a.source_version_id
      LEFT JOIN catalog_color_fact cf ON cf.snapshot_id=a.snapshot_id AND cf.color_id=l.color_id
      WHERE d.selection_state='selected' AND d.set_id IS NOT NULL AND COALESCE(l.minifigure_id,l.part_color_id) IS NOT NULL
    ), checked AS (
      SELECT d.*,m.id AS eligible_mapping FROM direct d LEFT JOIN market_mapping_revision m
      ON m.provider='bricklink' AND m.closed_at IS NULL AND m.review_state='verified'
      AND COALESCE(m.minifigure_id,m.part_color_id)=d.target_id AND m.snapshot_id=d.snapshot_id AND m.source_version_id=d.source_version_id
      AND ((d.minifigure_id=m.minifigure_id AND m.item_type='MINIFIG' AND m.color_id IS NULL)
      OR (d.part_color_id=m.part_color_id AND m.item_type='PART' AND m.part_id=d.part_id AND m.canonical_color_id=d.color_id AND m.color_id IS NOT NULL))
      AND (SELECT count(*) FROM market_mapping_revision x WHERE x.provider='bricklink' AND x.closed_at IS NULL
        AND x.review_state='verified' AND COALESCE(x.minifigure_id,x.part_color_id)=d.target_id)=1
    ) , candidates AS (
      SELECT c.*,s.namespace AS set_namespace,s.identifier AS set_number,
        COALESCE(f.namespace,p.namespace) AS target_namespace,COALESCE(f.identifier,p.identifier) AS target_identifier,
        col.namespace AS color_namespace,col.identifier AS color_identifier,cf.display_name AS color_name,
        ROW_NUMBER() OVER(PARTITION BY c.item_type ORDER BY (s.identifier='10350-1') DESC,(s.identifier='21333-1') DESC,s.identifier,c.id) AS rank
      FROM checked c JOIN catalog_set s ON s.id=c.set_id
      LEFT JOIN catalog_minifigure f ON f.id=c.minifigure_id LEFT JOIN catalog_part p ON p.id=c.part_id
      LEFT JOIN catalog_color col ON col.id=c.color_id LEFT JOIN catalog_color_fact cf ON cf.color_id=c.color_id AND cf.snapshot_id=c.snapshot_id
      WHERE c.no_choice AND c.known AND c.regular_quantity>0
      AND (f.identifier='fig-012609' OR (p.identifier='3001' AND col.identifier='15'))
    ) SELECT item_type,set_namespace,set_number,set_id,snapshot_id,source_version_id,revision_id,id AS occurrence_id,
      target_id,target_namespace,target_identifier,part_id,color_id,color_namespace,color_identifier,color_name,
      regular_quantity,extra_quantity,evidence_id,eligible_mapping
      FROM candidates WHERE rank=1 ORDER BY item_type LIMIT 2;

-- eligibility.py / candidate_element
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT i.exact_identifier AS element_identifier,p.namespace AS part_namespace,p.identifier AS part_identifier,
      col.namespace AS color_namespace,col.identifier AS color_identifier,m.part_color_id,m.review_state,m.evidence_id,
      e.row_sha256,f.dataset_name,f.decompressed_sha256
      FROM element_mapping m JOIN active a ON a.snapshot_id=m.snapshot_id
      JOIN catalog_provider_identity i ON i.id=m.provider_identity_id JOIN catalog_provider pr ON pr.id=i.provider_id
      JOIN catalog_part p ON p.id=m.part_id JOIN catalog_color col ON col.id=m.color_id
      JOIN catalog_evidence e ON e.id=m.evidence_id JOIN catalog_source_file f ON f.id=e.source_file_id
      WHERE pr.code='rebrickable' AND i.exact_identifier='300101' LIMIT 5;

-- eligibility.py / candidate_source_files
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT f.dataset_name,f.decompressed_sha256 FROM catalog_source_file f JOIN active a ON a.source_version_id=f.source_version_id
      WHERE f.dataset_name IN ('minifigs','inventory_minifigs','parts','colors','elements') ORDER BY 1 LIMIT 10;

-- eligibility.py / mapping_rows_recheck
SELECT item_type,review_state,closed_at IS NOT NULL AS closed,count(*) AS rows FROM market_mapping_revision WHERE provider='bricklink' GROUP BY 1,2,3 ORDER BY 1,2,3 LIMIT 20;

-- eligibility.py / minifigure_provider_mapping_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT p.code AS provider,m.review_state,count(*) AS association_rows
          FROM minifigure_provider_mapping m JOIN active a ON a.snapshot_id=m.snapshot_id
          JOIN catalog_provider_identity i ON i.id=m.provider_identity_id JOIN catalog_provider p ON p.id=i.provider_id
          GROUP BY 1,2 ORDER BY 1,2 LIMIT 12;

-- eligibility.py / part_provider_mapping_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT p.code AS provider,m.review_state,count(*) AS association_rows
          FROM part_provider_mapping m JOIN active a ON a.snapshot_id=m.snapshot_id
          JOIN catalog_provider_identity i ON i.id=m.provider_identity_id JOIN catalog_provider p ON p.id=i.provider_id
          GROUP BY 1,2 ORDER BY 1,2 LIMIT 12;

-- eligibility.py / color_provider_mapping_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT p.code AS provider,m.review_state,count(*) AS association_rows
          FROM color_provider_mapping m JOIN active a ON a.snapshot_id=m.snapshot_id
          JOIN catalog_provider_identity i ON i.id=m.provider_identity_id JOIN catalog_provider p ON p.id=i.provider_id
          GROUP BY 1,2 ORDER BY 1,2 LIMIT 12;

-- eligibility.py / element_mapping_counts
WITH active AS (
      SELECT s.id AS snapshot_id,s.source_version_id FROM catalog_active_snapshot a
      JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id
      WHERE p.code='rebrickable' AND a.scope='full-catalog' AND s.state='accepted' AND NOT v.synthetic
    ) SELECT p.code AS provider,m.review_state,count(*) AS association_rows
          FROM element_mapping m JOIN active a ON a.snapshot_id=m.snapshot_id
          JOIN catalog_provider_identity i ON i.id=m.provider_identity_id JOIN catalog_provider p ON p.id=i.provider_id
          GROUP BY 1,2 ORDER BY 1,2 LIMIT 12;

-- bindings.py / figure_parent_membership
SELECT i.identifier,f.display_name,l.id AS occurrence_id,l.minifigure_id,l.regular_quantity,l.extra_quantity,
      l.evidence_id,e.row_sha256,sf.dataset_name,sf.decompressed_sha256,
      (SELECT count(*) FROM inventory_matching_candidate x WHERE x.line_id=l.id) AS alternatives
      FROM catalog_inventory_line l JOIN catalog_minifigure i ON i.id=l.minifigure_id
      JOIN catalog_minifigure_fact f ON f.snapshot_id=l.snapshot_id AND f.minifigure_id=i.id
      JOIN catalog_evidence e ON e.id=l.evidence_id JOIN catalog_source_file sf ON sf.id=e.source_file_id
      WHERE l.revision_id='66f77536-fd04-4394-b7b0-6beec7c008c5' LIMIT 10;

-- bindings.py / candidate_fact_evidence
SELECT 'MINIFIG' AS item_type,i.namespace,i.identifier,f.display_name,f.evidence_id,e.row_sha256,s.dataset_name,s.decompressed_sha256
      FROM catalog_minifigure_fact f JOIN catalog_minifigure i ON i.id=f.minifigure_id
      JOIN catalog_evidence e ON e.id=f.evidence_id JOIN catalog_source_file s ON s.id=e.source_file_id
      WHERE f.snapshot_id='9ba3056b-690d-4686-bd96-109981f696ea' AND i.id='f8fb4ab6-1464-4c91-9202-659df5788d7a'
      UNION ALL SELECT 'PART',i.namespace,i.identifier,f.display_name,f.evidence_id,e.row_sha256,s.dataset_name,s.decompressed_sha256
      FROM catalog_part_fact f JOIN catalog_part i ON i.id=f.part_id JOIN catalog_evidence e ON e.id=f.evidence_id
      JOIN catalog_source_file s ON s.id=e.source_file_id
      WHERE f.snapshot_id='9ba3056b-690d-4686-bd96-109981f696ea' AND i.id='c2ddbb86-f38b-4aa7-9247-d16f9014b3c2' LIMIT 2;

-- bindings.py / final_baseline
SELECT a.snapshot_id,a.generation,s.source_version_id,s.state,v.manifest_digest
      FROM catalog_active_snapshot a JOIN catalog_snapshot s ON s.id=a.snapshot_id JOIN catalog_source_version v ON v.id=s.source_version_id
      JOIN catalog_provider p ON p.id=a.provider_id WHERE p.code='rebrickable' AND a.scope='full-catalog' LIMIT 1;

-- bindings.py / schema
SELECT version_num FROM alembic_version LIMIT 5;
