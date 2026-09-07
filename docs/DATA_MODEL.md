# Data Model

## Scope, stages, and conventions

This is a conceptual contract, not a migration or permission to implement. Phase 1 creates only an empty Alembic baseline and its revision metadata; no listing, image, catalog, or valuation entity is required then. Add the entities below in their named phases under reviewed migrations. See [architecture](ARCHITECTURE.md), [valuation rules](VALUATION_RULES.md), and [traceability](REQUIREMENTS_TRACEABILITY.md).

Use UUID primary keys, timezone-aware UTC timestamps, explicit foreign keys, positive inventory quantities, and nonnegative adjustment/cost inputs where required. Money is exact NUMERIC/Decimal with currency; JSON uses decimal strings. Null/unavailable monetary evidence is not zero. Deletion of catalog rows referenced by history is restricted; use version/status changes and retain reproducible references subject to source rights.

## Phase 2 — Explicit catalog identities and relationships

### catalog_set

Internal UUID; canonical base number and variant suffix; canonical full set number; name; theme reference; piece count and release/retirement metadata when known; provenance and active status. Unique canonical full identifier, preserving examples such as 75331-1. Canonical namespace rules are explicit; an unsuffixed number is a search input, not permission to pick a variant.

### catalog_theme

Internal UUID, canonical/source name and parent relationship if verified, provenance/version. Unknown theme remains unknown.

### minifigure

Internal UUID; canonical figure identifier and namespace; name; source/version provenance; active status. A minifigure is an explicit entity, not an untyped catalog-set placeholder.

### set_inventory_version and set_minifigure

set_inventory_version identifies one set's inventory revision, source/import run, completeness/review state, and validity/observed times. Distinguish verified empty inventory from missing/incomplete inventory.

set_minifigure links inventory-version ID to minifigure ID with integer quantity > 0, source-line provenance, and review state; unique (inventory_version_id, minifigure_id). Repeated figures use quantity, not duplicate relationship rows. An inventory version belongs to exactly one set. A current-version pointer must reference that set's version; snapshots retain the exact version they used.

These foreign keys and constraints preserve explicit set/figure identity and quantities; generic catalog_item is not a substitute.

### catalog_import_run and catalog_source_version

Record provider/source, source version or content digest, retrieval/import time, importer version, permitted-use reference, status, counts, and quarantine/error summaries without secrets. Imports are resumable/idempotent for a source version. Reject/quarantine malformed rows and uncertain relationships; never silently omit them while marking inventory complete.

### set_provider_mapping and minifigure_provider_mapping

Separate tables link the appropriate canonical entity to provider namespace, provider item type, exact provider identifier, source/import version, mapping method, evidence, reviewer/time, and review state (proposed, verified, rejected, unresolved).

A provider item key has at most one active verified canonical target within its item type/namespace. Conflicting proposed mappings remain reviewable and block dependent price attribution. A provider mapping can have multiple historical revisions; snapshots identify the exact accepted mapping revision. Suffix stripping, name similarity, and arbitrary first matches cannot create a verified mapping.

### catalog_image_reference

Explicit nullable set ID or minifigure ID with an exactly-one-target constraint; provider/reference URL or permitted local asset reference; source/import provenance; permission basis; review/availability status. Images are optional display metadata with a placeholder when unavailable. Do not borrow unrelated variants' images or assume catalog-image storage rights. Phase 2 does not create the later listing-image BlobStore.

### Part/color catalog and physical allocation — D-025, R-13/R-32

Add explicit part, catalog_color and part_color_identity records: canonical namespace/identifier, exact printed/decorated variant, color identity, active/review state and source/version provenance. A part_color_identity identifies a verified part/color combination, not a guessed compatible color. Add provider_color_mapping and part_provider_mapping revisions with provider namespace/type/item/color IDs, canonical targets, method/evidence/reviewer and proposed/verified/rejected/unresolved states. Enforce one active verified target for each provider key and retain historical mapping references. Non-applicable color for an intact non-part item is explicit and differs from unknown part color.

Extend set_inventory_version through set_component_inventory and set_inventory_line, preserving source-line identity and exactly one applicable part/color, minifigure, nested subset or supported instruction/booklet/packaging target. Store regular_quantity and extra_quantity separately as nonnegative integers with at least one positive quantity for a present line, source/inventory version, membership, provenance and completeness/review state. Known zero optional extras do not mean missing data. Instruction/booklet content is supported only where sourced; box/packaging inclusion remains later and rights-gated. Keep the default exclusions from the part-out plan explicit in selection policy, not by deleting source relationships.

inventory_choice_group and inventory_choice_member describe alternate/matching cardinality and source semantics. A selection/allocation snapshot records the chosen members and unresolved required groups; alternatives cannot all count by default. minifigure_component and subset_membership reference versioned exact constituent quantities/lineage. Expansion must be acyclic and complete for its claimed scope; unresolved nested contents cannot silently disappear. An intact sale line and its expanded components are mutually exclusive allocations.

Catalog presence/rarity is reproducible from part_set_presence relationships or a derived view over verified inventory choices: distinct canonical set IDs per exact part/color, inventory/catalog version, scope/completeness, alternate-resolution basis, first/last known appearances where supplied. Multiple inventory versions do not inflate set counts. Global exclusivity needs complete demonstrated coverage; incomplete catalogs expose known set count only. Preserve unresolved possible presence separately from proven presence.

Extend catalog_image_reference with an explicit part/color target in its exactly-one-target constraint, including mapping/version and permission basis. Optional part images never substitute another color/print or require listing-image ingestion.

## Phase 3 — Market observations and provenance

### market_observation

Immutable observation identity; exactly one set-mapping, minifigure-mapping or part-mapping revision, with verified color-mapping revision for a part; provider/item/color key; raw source condition plus normalized new/used and supported packaging/completeness qualifiers; market side (sold or current_listing, displayed as CURRENT); statistic type; exact amount/currency or explicit unavailable state; region; source observed-at, fetched-at, observation-window start/end, and stale-after times; sample listing/sale count and item quantity when supplied; source request parameters/version; provenance/use-policy reference.

Foreign keys tie each observation to its verified mapping and correct canonical item type. Do not silently attach an unmapped provider result to a set/figure. Unresolved mappings produce provider_fetch_run/quarantine outcomes, not observations attributed to unverified identities; the API derives mapping-unresolved status from that outcome. Observation state/reason fields represent unavailable, stale, thin, and provider error. Unknown sample information remains null/unknown. Availability and freshness are distinct dimensions.

For parts, preserve normalized activity alongside its observation or in an explicitly linked market_activity_observation: sold_quantity, sale_occurrence_count and its source meaning; observation-window start/end and supplied duration; average/quantity-weighted/minimum/maximum sold price where exposed; current_quantity, active_inventory_count, active_lot_count and seller/store_count where separately supplied; current average/quantity-weighted price; source-observed, fetched, stale-after and price/activity confidence states. Counts/quantities are nonnegative or unknown, not default zero. Price statistics retain their distinct identities. Do not infer sellers from lots, transactions from occurrences, or historical inventory from current supply.

A liquidity input group references compatible SOLD interval and CURRENT snapshot observations for exact part/color/condition/provider/region/currency scope, including their timestamp skew and policy checks. Pairing does not rewrite either observation. Store any month-normalization rule/version, raw window and metric-specific availability. Shared part observations belong to the item/query, not one set; all sets using that exact key can reuse them.

New/used, sold/current listing, currency, region, statistic, and observation period participate in query/cache identity. They cannot overwrite or masquerade as each other. Provider refresh creates an observation rather than rewriting one used in a saved calculation, where permitted.

### provider_fetch_run and provider_cache_entry

Record bounded request purpose, provider adapter version, canonical query key or unresolved attempted provider identifier, mapping review/quarantine outcome, status/timing/quota metadata, permitted cache expiry, and attributable observation references. Exclude keys, auth headers, URLs containing secrets, and excessive raw payloads. Cache/retention rules are source-specific and must pass Phase 3/4 rights gates.

### provider_refresh_job — Phase 3 design, R-35

Plan durable deduplicated jobs in the existing PostgreSQL/backend: canonical request key, mapping and adapter version, requested reason/priority, provider interval/quota eligibility, scheduled time, lease/attempt state, bounded retry/backoff, terminal failure and output observation/fetch references. Exact key includes provider/type/item/color, condition, market side, region, currency, statistic/window and source-affecting parameters; mapping changes invalidate incompatible reuse. A job can serve multiple set/watchlist/Hunt consumers without duplicate provider calls. Preserve source timestamp separately from refresh time and make older late responses unable to replace newer valid cache pointers. Rights determine permitted retention of jobs, observations and historical references. No queue, worker or table is created in Phase 1.

### currency_conversion_observation

Source/target currencies, exact rate/direction, provider, source time, fetched time, and validity policy. Valuations reference the applied conversion; no implicit currency mixing.

## Phase 4 — Feasibility evidence

### feasibility_run and feasibility_case

Versioned sample definition, catalog/mapping/import versions, observation references, sample category, expected/actual relationship quantities, whole-set/figure condition/side coverage, freshness/sample adequacy, gaps, rights/access status, and supported/partial/blocked conclusion. The first gate may use a reproducible Markdown/report artifact instead of new database tables if that preserves all evidence.

Include modern/retired; zero/one/many/repeated figures; dominant valuable figure; suffixed/variant identifiers; unresolved mappings; missing/stale/thin prices. Fixture evidence and live evidence have distinct status; a fixture cannot certify live entitlement.

D-025 extends cases with exact part/color inventories, four POV views, activity/price coverage, optional direct-provider/website comparison settings and numerical differences/reasons, cache/call-volume/stale behavior, and candidate recovery/liquidity/Gem/burden/Hunt policy versions. Retain representative small/very-large/current/retired, few-lot/high-value, many-lot/low-value, repeated/alternate/extra, figure-heavy/valuable-nonfigure, velocity extremes, missing-price/zero-sale/high-supply/thin-sample cases. Keep calibration and validation case identities/results visible; no adopted threshold is implied by a proposed candidate.

## Phase 5 — Valuation domain and snapshot contract

The engine is independently testable before browser work. Phase 5 defines immutable snapshot schemas and fixture serialization; Phase 7 persists user deal snapshots through migrations.

### valuation_snapshot

Set ID and inventory version; optional deal ID (no required listing/analysis-run ID); chosen sale strategy; formula/calculation version; evidence/confidence policy version; currency; enabled target ROI/minimum-profit constraints; exact assumptions; calculation time; complete/partial/blocked status/reasons; input hash; source/manual distinctions and permitted observation references.

### valuation_input_line

Snapshot ID, stable line ID, physical allocation group/figure identity or residual-build reference, catalog quantity, actual/absent/selected quantities, condition, source or manual value basis, adjusted unit value/currency, source freshness, conversion reference, and adjustment reason. Quantities must reconcile to the inventory/deal; no physical unit belongs to multiple sale lines in one strategy.

Cost input lines identify purchase price, purchase-dependent tax/premium function and bases, fixed acquisition expenses, fee bases/rates, order counts, shipping, packaging, labor/replacements, promotions, risk reserve, and other costs exactly once.

### valuation_output_line

Snapshot ID, named calculation/line type, exact amount/currency or dimensionless ratio, quantity/coverage where applicable, input dependencies, rounding rule, and available/undefined/partial/blocked state. Outputs include minifigure new/used/deal totals, priced/total/unavailable quantity, concentration, gross/selling/net proceeds, acquisition cost, profit, ROI, each raw maximum-buy cap, recommended rounded/clamped cap, and explanation.

Keep whole-set and split-sale snapshots separate; never add their totals. Preserve signed raw bounds and a no-feasible-purchase status when a zero clamp cannot meet targets. ROI is explicitly undefined for zero acquisition cost. Snapshot retention must comply with verified source rules; access alone does not grant perpetual provider-content storage.

### Part-out snapshot family — R-11–R-37, Phase 5 contracts

Reuse valuation_input_line/output_line and permitted observation references. The following are named logical snapshot structures, not a requirement for one physical table per metric. Derive inexpensive values from versioned inputs; persist derived snapshots only for justified performance/history with reviewed migrations. Phase 5 defines deterministic contracts/fixtures; Phase 7 persists user scenarios, while shared server caches can materialize permitted results in their owning phase.

| Structure | Required reproducible content |
|---|---|
| part_liquidity_snapshot | Exact part/color/condition and compatible SOLD/CURRENT observation IDs; S/C/O/window, month convention, velocity/proxy/supply-months, each metric state/reason, calculation version and freshness/confidence. Set-specific absorption references this shared velocity plus selected set quantity; it is not stored as universal part liquidity. |
| part_opportunity_snapshot | Lot/inventory allocation and price/liquidity/rarity references, unit/contributed value and POV share, value/demand/supply/absorption/confidence dimensions, classification, Gem flag/reasons, threshold/profile/calculation versions; no opaque score as the only output. |
| theoretical_pov_snapshot | Set/inventory version, selection/allocation, condition, SOLD/CURRENT, statistic/currency/region, full theoretical total or null and distinct priced subtotal; regular quantity, included extra quantity, unique total/priced/missing lots, total/priced/unpriced sellable quantities, physical piece count or unavailable, missing lines, alternate resolution, figure/extra modes, inclusion/source observations and observed/fetched/stale-after times, quantity/lot/value/activity coverage and denominator/reference-weight basis, calculation version and complete/partial/blocked reasons. |
| recoverable_pov_snapshot | Parent POV/allocation/evidence references, horizon/profile/model version, explicit sold-fraction/realized-price or grouped-line assumptions with support and exclusions, expected recoverable gross/state, confidence; selling cost lines remain separate from gross. |
| liquid_pov_snapshot / fast_cash_value_snapshot / dead_stock_exposure_snapshot | Parent POV, qualifying/excluded lot identities and reasons, gross basis/adjustments, values, compatible POV shares, lot/sellable/physical counts, unknown/unpriced exclusions, threshold/configuration version, confidence and freshness. Preserve fast-within-liquid and dead/unknown distinctions. |
| concentration_snapshot | Stable lot rank/ties, highest/top-5/top-10 values/shares, qualified high-value/high-liquidity concentrations, distinct figure concentration and partial/zero denominator states. |
| break_even_lot_analysis | Acquisition target/currency and cost basis, theoretical and liquidity-ranked views, ranking policy/ties, selected prefix identities/counts/quantities, gross/recoverable/net contributions where supported, lot/unit/piece coverage, target-reached state, subset-cost assumptions and confidence. |
| operational_burden_snapshot | Unique lots, selected physical pieces, expected listings/orders with evidence, low/high-value-lot proportions/thresholds, fragmentation, value per lot/piece and optional LOW/MEDIUM/HIGH classification/version; unknown labor remains unknown. |
| set_part_out_snapshot | References to four independent POV views and compatible derived components; selected basis, high-value-part/Gem counts, recovery/Liquid/Fast Cash/dead/coverage/concentration/density/burden/POV-premium outputs, supply/absorption distributions including unknown/infinite buckets, overall confidence and price/activity freshness. |

Snapshot identity includes exact inventory/mapping/observation and policy versions, selection/figure/extra/alternate modes, currency/region/statistic/window, recovery horizon/profile, formula/rounding versions and input hash. State-bearing metric values use decimal strings or null plus units/reasons; infinite/undefined values are explicit states, never nonfinite JSON numbers. Include independent reference weights only when needed to support a labeled value-coverage estimate. Unknown full POV cannot yield an invented coverage denominator.

Physical allocation groups extend valuation_input_line to exact part/color and optional instruction/packaging targets as well as figures/residual builds. Store catalog regular/extra, actual/absent, selected sellable units and physical-component counts separately. Enforce nonoverlapping allocation within one active strategy, resolved group cardinality, and no intact-plus-components or removed-part-plus-residual duplication. Alternative snapshots may model the same inventory, but their proceeds are never combined.

## Phase 7 — Private saved work and adjustments

### user_settings and selling_profile

Single Brian user/principal reference; revision; currency preference; enabled targets; target ROI/minimum profit; acquisition-cost rules; profile-specific fees, shipping, packaging, order-count, labor, reserve, and freshness policies; schema/version/time. Defaults are visible and editable, not hidden financial facts. Preserve configurable local-sale, shipped-resale, BrickLink-like, and personal-collection scenarios from earlier planning; fee schedules are dated settings, never eternal provider constants. No public registration/team model.

### saved_set and watchlist_item

Canonical set reference and Brian owner; saved timestamp; active/status; target purchase price/currency; notes; selected strategy/profile; revision and notification-independent watch status. Use uniqueness for the same owner/set/strategy where appropriate; a watchlist is not an automated purchase or seller-contact permission.

### saved_deal

Brian owner; canonical set and inventory version; asking price/currency; source URL/type, notes, target price, deal state, creation/update/revision; references to immutable valuation snapshots and selected profile version. URLs remain metadata and are not fetched. A later listing-session link is nullable. A deal can exist without any image or prediction.

### deal_minifigure_adjustment

Deal/figure and stable unit-group references; catalog quantity, present quantity, absent quantity, selected-for-separate-sale quantity; intact/damaged/incomplete condition; adjusted value/replacement basis, notes, and provenance. Split mixed conditions into nonoverlapping quantity groups. Enforce totals and no more physical units than a declared inventory/explicit additional-item amendment permits.

### deal_build_adjustment

Deal and residual-build allocation; completeness estimate/evidence, missing build items, instructions/box status, retained figures, estimated proceeds basis, condition adjustment or replacement costs, confidence and notes. Prevent removed figures or their components from remaining in valued residual quantities.

### authentication and revisions

Private principal/session records store only approved credential verifiers/tokens, expiry/revocation, and minimal audit data; exact mechanism is a Phase 7 security-plan decision. Saved-work writes carry a server revision; conflicting updates are explicit, not silently overwritten. Phase 1 creates none of these tables.

### Part-out saved strategies and adjustments — R-27/R-33

Extend saved_deal with separate complete, figures-plus-build and full-part-out valuation references and exactly one active strategy; selective harvest remains later/unsupported until its evidence gate passes. deal_part_adjustment uses exact part/color/physical groups, actual condition, absent/extra/selected quantities and provenance. Removing parts updates residual allocation/evidence as well as any intact-figure selection. Save calculation/threshold/profile versions, recovery assumptions, acquisition/selling-cost bases, break-even views, evidence freshness and permitted source references so reopening never silently recalculates from refreshed prices.

## Phase 8 — Hunting

### hunt_run and hunt_score_snapshot

Sample/universe and catalog/market/profile versions; scoring version; deterministic sort/tie policy; timestamp; eligible/blocked status; component scores and explanations; referenced valuation snapshot; profit/ROI/max-buy, minifigure coverage, market activity/freshness, confidence, top-figure concentration, residual-estimate dependence, estimated listing/order count, and operational burden.

A score is reproducible from its inputs. Unknown required evidence blocks or excludes with a reason; no fabricated precise score. Catalog opportunities without a known asking price expose maximum buy and the explicit hypothetical acquisition assumption, not an invented available deal.

### hunt_score_component_snapshot — R-36

Add components for purchase economics, POV premium/recoverable/Liquid/Fast Cash/Dead-Stock values, proxy/velocity/supply/absorption distributions, figure/part/top-5/top-10/Gem/high-liquidity concentration, break-even lots, value per lot/piece, fragmentation/listings/orders/burden, competition, rarity and price/activity/mapping/sample/freshness confidence. Each component references its set/part-out/valuation inputs, normalized value/state, denominator, policy and explanation. Record any eventual weighting/calibration version, overlapping-metric rationale, universe and deterministic ties; Phase 4 evaluates candidates and Phase 8 implements only the reviewed policy. Unknown critical components cannot disappear through silent weight redistribution.

## Phase 9 — Synchronization and caches

PostgreSQL remains authoritative. Server revision/sync metadata identifies cached versions; device/browser caches hold only allowed dated views of set details, saved work, and watchlists. Initial offline behavior is read-only; fresh searches, recalculation, and writes require connectivity. Provider cache rights still apply on client caches; do not replicate prohibited content. Account logout/expiry clears or locks sensitive local data under the reviewed policy.

## Later listing, image, recognition, and dataset module — Phases 13–16

These entities are optional additions, not prerequisites for any core table or Phase 1.

- Phase 13 listing: optional source URL/title/description/asking price with private metadata; nullable association to saved_deal.
- Phase 13 blob: physical immutable SHA-256 key/byte count; image_asset: semantic original/thumbnail with dimensions/kind/privacy; image_relation: parent/child/versioned transformation lineage.
- Phase 13 listing_image: UUID exposed as listing_image_id, listing ID, canonical original asset, persisted display_order; unique original and position per listing.
- Phase 13 upload_receipt: listing, client UUID, immutable bytes hash/requested position, private filename, stored result, listing_image_id; unique UUID and claimed position per listing, same-listing foreign key. Every successful duplicate has a new/reused receipt; replay is recoverable.
- Persist minimum successful receipt position per unique image; maintain receipt high-water mark and explicit UUID/position conflicts. Full constraints, race examples, privacy, and recovery are preserved in [IMAGE_INGESTION.md](IMAGE_INGESTION.md).
- Phases 14–15 analysis_run, provider_call_log, candidate_match, identity_confirmation, capture_session, and object_region reference shared canonical sets/minifigures and optional image lineage, never duplicate core catalogs/mappings/valuation.
- Later reference representations point to shared catalog_image_reference records and record embedding provider/model/version/dimension, view type, and update status; they are a derived index, not new catalog identities. Add vector persistence only when the measured Phase 14/16 use case needs it.
- Phase 16 label_state, dataset_release, and dataset_item preserve reviewed labels, source grouping, manifests, split seed, hard negatives, and privacy provenance.
- Phase 16 deal_outcome appends purchase price/date, verified sets/figures/missing items, replacements/labor, channel/date/gross/fees/shipping/net, time to sell, and forecast-versus-actual error to the core saved deal. It does not rewrite the original valuation snapshot.

Originals cannot be overwritten. Implement retention/deletion only under the approved later policy; references, shared blobs, dataset releases, and backups must be handled deliberately. AI predictions never become confirmed training labels automatically.
