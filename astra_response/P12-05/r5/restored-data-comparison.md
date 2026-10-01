# Restored data and production contract — PASS

Immediately before comparison, the source was captured in one bounded PostgreSQL
REPEATABLE READ / READ ONLY transaction with a 180-second per-statement limit.
Only counts and the required catalog/application/ownership/role state were read.
Private IDs and credentials were not published. All 76 table counts,
normalized effective object ACLs, schema/column/function/default grants, database
owner/marker contract, role attributes and memberships matched restored state.
Effective ACLs expand acldefault and sort grant entries, retaining the accepted
normalization for equivalent explicit versus default ACL representations.

- Revision 0016_hunt_cached_runs and exactly one owner principal.
- Exact database ownership contract and role markers; PUBLIC database access absent.
- Recovered owner and runtime credentials authenticated with SCRAM on the isolated
  socket. Runtime cannot create schema/database/temp objects, write revision or
  create principals, and retains required reads. No credential bypass.
- 28,278 sets, exactly one accepted active nonsynthetic Rebrickable snapshot,
  generation 1 and exactly one activation receipt.
- Exact private active/activation/import-audit state matched, preserving the failed
  predecessor and its successful predecessor-linked retry. No running import.
- Zero market observations; Watchlist empty; Settings equal accepted defaults;
  zero valid owner sessions and zero saved forecast/deal.
- The one ordinary unsaved forecast remains preserved, with saved count zero;
  its table count matches the backup. No manual forecast deletion occurred.
- 75331-1 / The Razor Crest exists, with one inventory and four directly recorded
  minifigure lots. Exact private lot data matched as well as the counts.

| Production application/catalog table | Source | Restored | Result |
|---|---:|---:|---|
| `public.alembic_version` | 1 | 1 | PASS |
| `public.application_settings` | 1 | 1 | PASS |
| `public.auth_control` | 1 | 1 | PASS |
| `public.auth_principal` | 1 | 1 | PASS |
| `public.auth_session` | 2 | 2 | PASS |
| `public.catalog_activation` | 1 | 1 | PASS |
| `public.catalog_active_snapshot` | 1 | 1 | PASS |
| `public.catalog_color` | 275 | 275 | PASS |
| `public.catalog_color_fact` | 275 | 275 | PASS |
| `public.catalog_default_inventory` | 45,503 | 45,503 | PASS |
| `public.catalog_evidence` | 1,898,466 | 1,898,466 | PASS |
| `public.catalog_evidence_link` | 0 | 0 | PASS |
| `public.catalog_import_run` | 2 | 2 | PASS |
| `public.catalog_inventory` | 47,452 | 47,452 | PASS |
| `public.catalog_inventory_line` | 1,588,405 | 1,588,405 | PASS |
| `public.catalog_inventory_revision` | 47,452 | 47,452 | PASS |
| `public.catalog_minifigure` | 17,225 | 17,225 | PASS |
| `public.catalog_minifigure_fact` | 17,225 | 17,225 | PASS |
| `public.catalog_part` | 64,620 | 64,620 | PASS |
| `public.catalog_part_category` | 76 | 76 | PASS |
| `public.catalog_part_category_fact` | 76 | 76 | PASS |
| `public.catalog_part_fact` | 64,620 | 64,620 | PASS |
| `public.catalog_provider` | 1 | 1 | PASS |
| `public.catalog_provider_identity` | 272,667 | 272,667 | PASS |
| `public.catalog_set` | 28,278 | 28,278 | PASS |
| `public.catalog_set_alias` | 53,877 | 53,877 | PASS |
| `public.catalog_set_fact` | 28,278 | 28,278 | PASS |
| `public.catalog_snapshot` | 1 | 1 | PASS |
| `public.catalog_snapshot_validation` | 1 | 1 | PASS |
| `public.catalog_source_file` | 12 | 12 | PASS |
| `public.catalog_source_version` | 1 | 1 | PASS |
| `public.catalog_stage_colors` | 275 | 275 | PASS |
| `public.catalog_stage_elements` | 114,245 | 114,245 | PASS |
| `public.catalog_stage_inventories` | 47,452 | 47,452 | PASS |
| `public.catalog_stage_inventory_minifigs` | 25,820 | 25,820 | PASS |
| `public.catalog_stage_inventory_parts` | 1,557,375 | 1,557,375 | PASS |
| `public.catalog_stage_inventory_sets` | 5,210 | 5,210 | PASS |
| `public.catalog_stage_minifigs` | 17,225 | 17,225 | PASS |
| `public.catalog_stage_part_categories` | 76 | 76 | PASS |
| `public.catalog_stage_part_relationships` | 37,394 | 37,394 | PASS |
| `public.catalog_stage_parts` | 64,620 | 64,620 | PASS |
| `public.catalog_stage_sets` | 28,278 | 28,278 | PASS |
| `public.catalog_stage_themes` | 496 | 496 | PASS |
| `public.catalog_theme` | 496 | 496 | PASS |
| `public.catalog_theme_fact` | 496 | 496 | PASS |
| `public.color_provider_mapping` | 275 | 275 | PASS |
| `public.deal_forecast` | 1 | 1 | PASS |
| `public.deal_lineage_metadata` | 0 | 0 | PASS |
| `public.element_mapping` | 114,245 | 114,245 | PASS |
| `public.hunt_candidate` | 0 | 0 | PASS |
| `public.hunt_run` | 0 | 0 | PASS |
| `public.inventory_expansion_binding` | 31,030 | 31,030 | PASS |
| `public.inventory_matching_candidate` | 0 | 0 | PASS |
| `public.inventory_matching_group` | 0 | 0 | PASS |
| `public.market_mapping_revision` | 0 | 0 | PASS |
| `public.market_observation` | 0 | 0 | PASS |
| `public.market_policy` | 0 | 0 | PASS |
| `public.market_purge_receipt` | 0 | 0 | PASS |
| `public.minifigure_provider_mapping` | 17,225 | 17,225 | PASS |
| `public.part_category_provider_mapping` | 76 | 76 | PASS |
| `public.part_color_identity` | 109,475 | 109,475 | PASS |
| `public.part_color_observation` | 1,671,620 | 1,671,620 | PASS |
| `public.part_provider_mapping` | 64,620 | 64,620 | PASS |
| `public.part_relationship` | 37,394 | 37,394 | PASS |
| `public.product_refresh_operation` | 0 | 0 | PASS |
| `public.product_refresh_view` | 0 | 0 | PASS |
| `public.provider_budget_group` | 0 | 0 | PASS |
| `public.provider_cache_entry` | 0 | 0 | PASS |
| `public.provider_discovery_evidence` | 0 | 0 | PASS |
| `public.provider_fetch_run` | 0 | 0 | PASS |
| `public.provider_refresh_job` | 0 | 0 | PASS |
| `public.provider_scope_state` | 0 | 0 | PASS |
| `public.selling_profile` | 0 | 0 | PASS |
| `public.set_provider_mapping` | 28,278 | 28,278 | PASS |
| `public.theme_provider_mapping` | 496 | 496 | PASS |
| `public.watchlist_item` | 0 | 0 | PASS |
