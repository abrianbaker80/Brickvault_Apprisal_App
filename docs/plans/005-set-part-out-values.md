# Set part-out values — Phases 2–6

**Status:** Brian requested this planning addition on 2026-09-06. Planned, not implemented; no provider access or Phase 1 scope expansion is authorized.

## 1. Goal and user-visible outcome

On set detail, show separate **New part-out value** and **Used part-out value**, with currency, pricing basis, included inventory, coverage and freshness. Brian can compare them with whole-set and minifigure values when assessing a purchase.

These are theoretical component market totals. Realizable proceeds, selling costs, profit and maximum buy remain separate calculations requiring supported selling assumptions.

## 2. Why this belongs here

This extends deterministic sourcing and uses the existing catalog, market and valuation core. Add the necessary inventory contracts in Phase 2, pricing evidence in Phase 3, feasibility in Phase 4, aggregation in Phase 5 and set-detail display in Phase 6. It needs no images or recognition and creates no Phase 1 product tables.

## 3. In scope

Versioned set-component quantities; exact provider item/color mappings; new/used component evidence; deterministic decimal totals; a reproducible inclusion policy; coverage and missing-data explanations; set-detail comparison using generated API contracts.

## 4. Explicit non-goals

Actual individual-piece listing/fulfillment, inventory management, guaranteed sell-through, scraping BrickLink's website, paid/provider calls under this planning request, or automatically treating a theoretical total as cash, profit or a maximum offer. The existing initial-engine exclusion for operational full piece-by-piece sales remains.

## 5. Current repository and provider evidence

Slice 1B implements foundation infrastructure only. There is no component catalog, pricing adapter, valuation engine or product UI.

The [official BrickLink API manual](https://static.bricklink.com/alpha/default/api_wiki.html) was read on 2026-09-06. It documents `GET /items/{type}/{no}/subsets` for inventory and `GET /items/{type}/{no}/price` for per-item guides, with condition, color, currency and market-side parameters. The reviewed catalog-method list does not document an aggregate set part-out-price endpoint. The planned integration therefore derives totals from inventory and component price guides; this is an inference about feasibility, not verified account capability or parity with the website calculator.

No authenticated requests, credentials, account rights, quota tests or live coverage checks were performed. See [provider gates](../PROVIDER_GATES.md).

## 6. Decisions and assumptions

- Default view: distinct new and used totals based on the same inventory/inclusion policy. Prefer the provider's quantity-weighted six-month sold unit statistic when permitted and sufficiently supported. Label any current-listing view separately; never silently substitute it for sold evidence.
- Initial inclusion policy: required regular set contents, minifigures kept assembled, nested sets expanded only with verified source semantics; exclude extra/spare pieces, alternate choices, box and instructions by default and disclose those choices. An unresolved required matching group blocks a complete total; do not add all alternatives together.
- Assembled figures may contribute once to the part-out total. Their component pieces cannot also contribute. A future broken-down-figure option must be a separate mutually exclusive policy with proven expansion; changing it changes the snapshot identity.
- Preserve exact printed/decorated variants and color IDs. No name-based or first-match substitution. A known empty inventory differs from an unknown inventory.
- Website equality is a Phase 4 comparison, requiring equivalent inclusion flags, region, currency, condition, price basis and observation time. Differences must be explained, not hidden with correction factors.

## 7. Data model and API changes — future migrations only

Extend the Phase 2 model with canonical part/color identities, reviewed provider mappings and a versioned `set_component_inventory` with quantity-bearing lines. Each line records source item type/ID, canonical mapping, color, quantity, regular/extra/alternate status, matching group and component/figure allocation. Preserve raw source versions only within verified retention rights.

Phase 3 adds component market observations to the same server-owned evidence model, retaining condition, market side, unit statistic, currency, sample information and timestamps. Do not overload set/minifigure mappings or invent a second provider cache.

Phase 5 produces versioned part-out snapshots: canonical set and inventory version, policy version/flags, geography/currency, price basis, component input references, new/used totals or explicit unavailable states, priced/total distinct lots and units, missing quantities, freshness range and calculation time. Missing items contribute to an explicitly partial subtotal only; a complete total remains unavailable. No arithmetic in TypeScript.

Phase 6 exposes those server results through the existing set-detail response or a bounded related `/api/catalog/sets/{id}/part-out` resource. Final Pydantic/OpenAPI contracts and migrations are reviewed in the responsible phase.

## 8. Implementation sequence

| Phase | Reviewable slice |
|---|---|
| 2 — Catalog | Import/version required parts, colors, quantities and choices using permitted fixtures; preserve exact set/minifigure relationships |
| 3 — Market | Verify account/rights and component guides; bounded deduplicated requests and permitted cache keyed by item type/ID, color, condition, side, geography and currency |
| 4 — Feasibility | Measure coverage, calls/latency, matching-group/flag semantics and comparable website results on a representative sample; block unsupported cases |
| 5 — Valuation | Pure decimal aggregation and reproducible snapshots for separate new/used totals and partial states |
| 6 — Set detail | Display both values, inclusion policy and evidence beside whole-set/minifigure values; expanded component breakdown and explicit unavailable states |

Each phase still requires its separate authorization. This plan does not start those phases or change Slice 1B/1C acceptance.

## 9. Validation and acceptance

Test repeated quantities/colors, zero/one/many figures, nested sets, decorated variants, extras/alternates, ambiguous mappings, missing/stale/thin prices, unsupported currencies and independently missing new/used coverage. Exact-decimal fixture totals must reproduce from inputs; changing inclusion flags must prevent mixing snapshots.

Prove that assembled figures and their parts never both contribute, and whole-set/residual-build proceeds are not added to this total. Show distinct priced-lot and priced-unit coverage. No-quote or zero-sample provider records are unavailable unless a legitimate zero-price observation is explicitly supported.

Use bounded request budgeting: one inventory retrieval plus up to two condition-specific guides per distinct priced item/color for the initial sold-only pair, plus any needed nested resolution. Deduplicate repeated parts, use only permitted cache retention, record partial failures and honor quotas. Do not assume a bulk price endpoint or unlimited parallel calls.

Phase 4 must verify source flags and reconcile a small representative sample, recording actual website/API settings and timing when comparison is authorized. Published API examples contain ambiguities, so parameter descriptions alone do not prove nested or minifigure expansion behavior. Unit fixtures cannot establish live coverage or website parity.

## 10. Security, privacy and data integrity

Server-side credentials/adapters only; current source-use, display/cache/history rights and account access are prerequisites. No website scraping, seller actions or new infrastructure authorization. Generated contracts contain public response shapes, never credentials.

## 11. Failure, rollback and recovery

Missing rights, mapping, inventory or price coverage produces a visible blocked/partial feature state. The direct whole-set/minifigure workflow remains usable. Do not replace API evidence with scraped HTML or a guessed total. Schema changes require forward reviewed migrations; retain reproducibility only within permitted history rights.

## 12. Progress log

- [x] 2026-09-06 — Record Brian's new/used part-out request and review the official public manual.
- [x] Place dependencies in Phases 2–6 and preserve the distinction between component value and realizable proceeds.
- [ ] Phase-specific authorization, source rights/access, live feasibility, implementation and acceptance.

## 13. Open verification gates

Current API/account rights, quotas and retention; exact subset matching-group/extra/alternate behavior; supported item/color coverage and minifigure expansion; parity with the website's chosen settings. These are provider feasibility gates, not reasons to add product work to Phase 1.

## 14. Outcome and follow-up

Planning accepted; implementation pending in the named phases. [D-024](../DECISIONS.md#d-024--new-and-used-set-part-out-values--2026-09-06), [R-11](../PRODUCT_SPEC.md#r-11--new-and-used-set-part-out-values) and roadmap/traceability link this feature to the shared deterministic core.
