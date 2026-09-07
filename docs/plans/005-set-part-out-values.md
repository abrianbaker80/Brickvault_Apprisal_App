# Set part-out values and liquidity intelligence — Phases 2–8

**Status:** D-024's 2026-09-06 planning addition is expanded by D-025 on 2026-09-06. Authoritative core product plan, documentation only; implementation and provider/threshold feasibility are not started. The separate acceptance request authorizes one reviewed local documentation checkpoint. No Phase 1 scope expansion, service startup, dependency change, provider contact, push or automatic implementation is authorized.

## 1. Goal and user-visible outcome

On Set Detail, show separate **New part-out value** and **Used part-out value**, each with independent SOLD and CURRENT-for-sale views, currency/statistic, included inventory, coverage and freshness. Add part-level value, demand, supply, absorption, confidence, competition and rarity evidence so Brian can distinguish expensive inventory from attractive liquid lots and slow/unknown inventory.

The four POV views are theoretical component totals. Expected recoverable gross, Liquid POV, Fast Cash Value, Dead-Stock Exposure, Part-Out Gems, concentration, break-even lots, value per lot/piece and burden explain possible strategy economics. Whole-set, figures plus remaining build and full part-out comparisons stay separate; selective harvest is later until supported. Feed these same results into saved deals and decomposable Sets-to-Hunt components. Recoverable gross, selling costs, net proceeds, acquisition cost, profit and maximum buy retain their distinct meanings.

## 2. Why this belongs here

This extends deterministic sourcing through the existing catalog, market and valuation core. Add inventory contracts in Phase 2, prices/activity/cache/refresh design in Phase 3, provider and policy feasibility in Phase 4, calculations in Phase 5, Set Detail in Phase 6, saved strategy economics in Phase 7 and Hunt components in Phase 8. It needs no images or recognition, creates no standalone phase and adds no Phase 1 product tables, queue or worker.

## 3. In scope

Versioned set-component quantities and selection; exact provider item/color mappings; four price views and part activity; deterministic decimal totals and liquidity/opportunity metrics; reproducible inclusion/recovery/threshold policies; explicit evidence coverage and missing-data states; shared provider caching/priority refresh; generated API contracts and planned Set Detail/deal/Hunt behavior. [PRODUCT_SPEC R-11–R-37](../PRODUCT_SPEC.md#r-11--new-and-used-set-part-out-values) and [VALUATION_RULES](../VALUATION_RULES.md) define the complete capabilities and formulas; [traceability](../REQUIREMENTS_TRACEABILITY.md#part-out-and-liquidity-requirements--d-025) maps each capability independently.

## 4. Explicit non-goals

Actual individual-piece listing/fulfillment, inventory management, guaranteed sell-through, scraping BrickLink's website, paid/provider calls under this planning request, or automatically treating theoretical value as cash, profit or a maximum offer. D-025 includes full part-out economic analysis while preserving the exclusion for selling operations. Do not implement selective harvest before its residual/allocation/recovery evidence, lock thresholds/weights now, or start Slice 1C/Phase 2 implementation.

## 5. Current repository and provider evidence

Slice 1B implements foundation infrastructure only. There is no component catalog, pricing adapter, valuation engine or product UI.

This amendment started from d79395223b5d6fedf78e01dabd3202b5526211eb with an empty index and no tracked changes. The unrelated NVIDIA installer was untracked at entry; after it disappeared during editing, Brian confirmed he removed it. Codex performed no content inspection or operation on it and added no ignore rule. Phase 1 plans/prompts remain unchanged. All new contracts below are proposed future structures, not implemented schema/API evidence.

Historical D-024 evidence: the [official BrickLink API manual](https://static.bricklink.com/alpha/default/api_wiki.html) was read on 2026-09-06 before this amendment. It documents `GET /items/{type}/{no}/subsets` for inventory and `GET /items/{type}/{no}/price` for per-item guides, with condition, color, currency and market-side parameters. That reviewed method list did not document an aggregate set part-out-price endpoint. Initially plan inventory-plus-item-observation aggregation; Phase 3 must explicitly verify current authorized aggregate or equivalent capabilities and permitted additional-source/benchmark use. This amendment performs no new provider research and claims no account capability or website parity.

No authenticated requests, credentials, account rights, quota tests or live coverage checks were performed. See [provider gates](../PROVIDER_GATES.md).

## 6. Decisions and assumptions

- Views: four independent NEW/USED × SOLD/CURRENT results based on a disclosed inventory/inclusion policy. Prefer a supported quantity-weighted sold statistic for SOLD; preserve the actual provider interval rather than assuming six months. CURRENT is an equally explicit required comparison view, not a fallback for missing sold evidence.
- Initial inclusion policy: required regular set contents, minifigures kept assembled, nested sets expanded only with verified semantics; exclude optional extra/spare pieces, unselected alternate possibilities, box and instructions by default and disclose these choices. Preserve separate regular/extra quantities and sourced instruction/booklet inventory for optional inclusion. Packaging is later/rights-gated. Resolve required matching groups explicitly; never include every alternative or omit unresolved required contents while claiming completeness.
- Assembled figures may contribute once to the part-out total. Their component pieces cannot also contribute. A future broken-down-figure option must be a separate mutually exclusive policy with proven expansion; changing it changes the snapshot identity.
- Preserve exact printed/decorated variants and color IDs. No name-based or first-match substitution. A known empty inventory differs from an unknown inventory.
- Website equality is a Phase 4 comparison, requiring equivalent inclusion flags, region, currency, condition, price basis and observation time. Differences must be explained, not hidden with correction factors.

- Expected recoverable POV means gross, before itemized selling costs. Recovery fractions, price adjustments, horizons, labor/order assumptions, classification cutoffs and Hunt weights require Phase 4 evidence; no numerical defaults are adopted here. A versioned deterministic calculation does not by itself prove predictive accuracy.
- Current supply is point-in-time; sold activity is interval-based. Derived sell-through is a proxy, market absorption is demand-equivalent time and rarity is catalog context. None establishes a guaranteed sale or Brian's share of market demand.
- Use “BrickLink Part Out Value” only after equivalence and permitted naming/display are established. Direct aggregate observations, if permitted, do not replace reproducible lot-level evidence.

## 7. Data model and API changes — future migrations only

Extend the Phase 2 model with canonical part/color identities, reviewed mappings and versioned `set_component_inventory` lines, separate regular/extra quantities, source item type/ID, exact color/variant, group resolution, nested/figure membership and physical allocation. Support sourced instruction/booklet inventory and later permitted packaging. Preserve raw source versions only within verified retention rights. Exact part/color set-presence relationships carry catalog scope/version/completeness; missing catalog coverage cannot prove global exclusivity.

Phase 3 adds part prices/activity to the same server-owned observation model: condition, SOLD/CURRENT, currency/statistics, sold units, source-defined occurrences, actual window, current units and separately exposed inventories/lots/stores, source-observed/fetched/stale-after times and confidence. Do not overload set/minifigure mappings or invent a second cache. Shared exact item/color query keys reuse evidence across sets; PostgreSQL-backed priority refresh in the same backend avoids synchronous detail fan-out, bounded by rights, quotas, concurrency, retry/backoff, freshness and failure isolation.

Phase 5 produces reusable part-liquidity, opportunity, theoretical/recoverable POV, Liquid/Fast Cash/dead-stock, concentration, break-even, burden and set-level snapshot contracts. Derive inexpensive outputs from versioned inputs; persist only when history/performance justifies it and rights permit. Phase 7 saves scenario/strategy snapshots; Phase 8 adds Hunt component snapshots. No arithmetic in TypeScript or separate recognition engine.

### Minimum POV result contract

| Group | Required fields and semantics |
|---|---|
| Identity and basis | Canonical set ID, inventory version, exact mapping/selection references, condition, SOLD/CURRENT, currency/region, exact price statistic, source request scope and calculation version |
| Inventory | Regular quantity; included extra quantity separately; total unique sellable lots; priced lot count; total represented sellable quantity; priced and unpriced quantities; physical piece count or unavailable; missing/unpriced lot identities and reasons |
| Inclusion | Required alternate/matching resolutions, unresolved group IDs, minifigure intact/component mode, extra inclusion mode, nested expansion, optional instruction/packaging policy and physical allocation lineage |
| Value and coverage | Complete theoretical total or null; distinct priced partial subtotal; lot/quantity/value coverage with numerator/denominator/state; independent metric-specific activity coverage. Value coverage is undefined if the full-value denominator is unknown, except separately labeled, provenance-backed complete reference weighting under VALUATION_RULES. |
| Evidence and status | Provider/source observation IDs and permitted metadata, observed-at/window/fetched/stale-after timestamps, independent price/activity freshness, confidence/coverage, calculation/policy/profile versions, as-of time, complete/partial/blocked status and reasons |

Sellable units and physical pieces differ when figures/subsets remain intact; count verified constituent pieces once without adding their component prices. Zero/unknown denominators and infinite supply/absorption use explicit states and null numeric values. Missing prices remain UNKNOWN, not zero; refreshing a cache does not change source observation time.

### Part-level and set-level intelligence contracts

Each part opportunity shows value (unit, set quantity, contribution/share), demand (sold units, velocity, occurrences), supply (current units, lots/sellers, supply-months), set-quantity absorption, sample/price/activity/freshness confidence and scoped rarity/appearances. Preserve raw source meanings and derived formula/version. Gem callouts include permitted image/reference and all available fields plus reasons; expensive-only, rare-only and unknown evidence do not qualify.

Each set-level snapshot exposes all four POV views; supported recoverable gross; Liquid POV/share and exclusions; Fast Cash Value/share/lots/pieces/confidence; Dead-Stock Exposure/share/lots/pieces with unknown evidence separate; unique lots and selected pieces; price/activity coverage; high-value-part/Gem counts; highest/top-5/top-10 and high-liquidity concentration; value per lot/piece; operational burden; price/activity freshness and confidence. Supply/absorption distributions preserve unknown/infinite buckets and weighting. Compare compatible whole-set value through POV premium, never mixed condition/side totals.

Break-even analysis takes a candidate acquisition target and returns theoretical-value and liquidity-aware ranked lot prefixes, quantities/identities, inventory percentages, theoretical/recoverable contributions, confidence and target-not-reached states. Gross target coverage is not economic break-even: the latter requires supported subset costs and net proceeds. Each supported complete/split/full-part-out strategy includes gross, selling/acquisition costs, net/profit/ROI/max-buy, burden/liquidity/confidence; selective harvest is deferred and removed inventory cannot remain valued in the residual build.

Phase 6 exposes catalog-level server results through set detail or a bounded related `/api/catalog/sets/{set_id}/part-out` resource, with paginated evidence drill-down and pending/stale/partial/blocked refresh states. Use the [Part-Out Analysis UX](../PRODUCT_SPEC.md#part-out-analysis-ux-concept--planned-phase-6): four-view matrix, recovery/liquidity/dead-stock summaries, Gems and high-value/low-liquidity warnings, concentration and burden. Acquisition-dependent break-even results and editable strategy/cost comparisons remain Phase 7, which also persists them; Phase 8 exposes decomposable Hunt components. Final Pydantic/OpenAPI contracts and migrations are reviewed in their responsible phases; no API is added by this plan.

## 8. Implementation sequence

| Phase | Reviewable slice |
|---|---|
| 2 — Catalog | First identities/mappings and inventory versions, then regular/extra/choice/figure/subset allocation and scoped rarity; prove no physical double counting with permitted fixtures |
| 3 — Market | First verify capabilities/rights and normalize four-view price/activity observations; then shared caching and bounded priority refresh design/implementation under that phase's explicit authorization |
| 4 — Feasibility | First measure four-view coverage/equivalence and cold/warm/shared-set call behavior; then validate recovery assumptions, liquidity/Gem/burden thresholds and candidate Hunt weighting on representative real sets |
| 5 — Valuation | First exact POV/coverage and liquidity formulas; then opportunity/subset/concentration/density/burden metrics; then recovery, break-even, premium and separate strategy economics with table tests |
| 6 — Set detail | First generated Part-Out Analysis matrix/summary; then paginated Gems/slow-lot/evidence drill-down and cache/refresh states; desktop/mobile acceptance with recognition disabled |
| 7 — Deals | Compare complete/split/full-part-out, actual contents/costs and break-even; save immutable calculation/threshold/assumption/freshness versions under private auth; selective harvest stays evidence-gated |
| 8 — Hunt | Add economics/liquidity/concentration/density/burden/competition/rarity/confidence components, then only Phase 4-reviewed combined scoring and deterministic replay/ties |

Each phase still requires its separate authorization. This plan does not start those phases or change Slice 1B/1C acceptance.

## 9. Validation and acceptance

Test repeated quantities/colors, zero/one/many figures, nested sets, decorated variants, extras/alternates, ambiguous mappings, missing/stale/thin prices, unsupported currencies and independently missing new/used coverage. Exact-decimal fixture totals must reproduce from inputs; changing inclusion flags must prevent mixing snapshots.

Prove that assembled figures and their parts never both contribute, and whole-set/residual-build proceeds are not added to this total. Show distinct priced-lot and priced-unit coverage. No-quote or zero-sample provider records are unavailable unless a legitimate zero-price observation is explicitly supported.

Replace D-024's sold-only two-guide budgeting example with measured four-view budgets: inventory/nested resolution plus potentially four item/color/condition/side guides per distinct key and any additional activity/pagination requests, according to verified capabilities. Measure cold, warm and overlapping sets; repeated quantities never multiply identical fetches. Deduplicate in-flight/queued work, use permitted retention/stale windows, cap concurrency/retries and honor quotas. Do not assume a bulk endpoint or run provider fan-out synchronously in Set Detail.

Phase 4 must verify source flags and reconcile a small representative sample, recording actual website/API settings and timing when comparison is authorized. Published API examples contain ambiguities, so parameter descriptions alone do not prove nested or minifigure expansion behavior. Unit fixtures cannot establish live coverage or website parity.

The expanded benchmark includes small/very large, current/retired, few-lot/high-value and many-lot/low-value sets; repeated quantities, alternates/extras, figure-heavy and valuable nonfigure inventories; high-value/high-velocity, high-value/low-velocity and low-value/high-velocity parts; missing prices, zero sales, high supply and thin samples. Evaluate numerical agreement/reasons for disagreement in all four views, price/activity coverage, proxies/velocity/supply/absorption, cache effectiveness/stale behavior/call budget, Gems, Liquid/Fast Cash/dead thresholds, concentration, burden, recovery models and Hunt candidates. Separate calibration/validation evidence; do not choose cutoffs to maximize scores.

Plan table tests for V-POV, V-REC, L-PROXY, L-VELOCITY, L-SUPPLY, L-ABSORB, L-OCCURRENCE, O-GEM, V-LIQUID, V-FAST, V-DEAD, V-CONCENTRATION, V-BREAK-EVEN, V-PER-LOT, V-PER-PIECE, O-BURDEN, O-COMPETITION, O-RARITY and V-PREMIUM under VALUATION_RULES. Include zero/missing denominators, true zero versus absent sales, actual non-six-month intervals, supply/window skew, partial full-value coverage, unknown versus dead stock, threshold boundaries, stable ranking ties, incompatible premium bases and costs deducted exactly once. New formulas are documented, not implemented/tested by this amendment.

Later browser/API acceptance covers every required Set Detail summary and part field, bounded drill-down, fresh/stale/pending/missing evidence, no false complete totals, no promised sale dates, high-price/low-liquidity cases and recognition-independent direct search. Saved-work tests replay original versions after refresh; Hunt tests explain component contribution and evidence blockers without invented asking prices, arbitrary weights or opaque theoretical-POV ranking.

## 10. Security, privacy and data integrity

Server-side credentials/adapters only; current source-use, display/cache/history rights and account access are prerequisites. No website scraping, seller actions or new infrastructure authorization. Generated contracts contain public response shapes, never credentials.

## 11. Failure, rollback and recovery

Missing rights, mapping, inventory or price coverage produces a visible blocked/partial feature state. The direct whole-set/minifigure workflow remains usable. Do not replace API evidence with scraped HTML or a guessed total. Schema changes require forward reviewed migrations; retain reproducibility only within permitted history rights.

Independent activity failures leave theoretical prices visibly available where valid while blocking unsupported liquidity/recovery. Refresh failures preserve only permitted dated evidence; retry caps, durable deduplication/leases and version checks prevent runaway calls and stale overwrites. Disable an unsupported policy by version rather than silently changing saved forecasts; old results stay historical where retention is allowed. No migration/rollback/resource operation is executed in this documentation task.

## 12. Progress log

- [x] 2026-09-06 — Record Brian's new/used part-out request and review the official public manual.
- [x] Place dependencies in Phases 2–6 and preserve the distinction between component value and realizable proceeds.
- [x] 2026-09-06 — D-025 expands the same plan through Phases 2–8 with four price views, liquidity/opportunities, recovery/strategy analysis, shared refresh and Hunt components. Preserve D-024 history and compatible inventory/evidence rules; no new provider research or implementation.
- [x] Documentation validation: local Markdown links, roadmap/prompt 02–08 alignment, requirement/formula traceability, additive decision history, complete diff/scope and Git status checked; no stage or commit.
- [ ] Phase-specific authorization, source rights/access, live feasibility, implementation and acceptance.

## 13. Open verification gates

Current API/account rights, quotas and retention; exact subset matching-group/extra/alternate behavior; supported item/color coverage and minifigure expansion; parity with the website's chosen settings. These are provider feasibility gates, not reasons to add product work to Phase 1.

Also unresolved: direct aggregate capability and branded terminology rights; occurrence/store/lot semantics and available activity windows; compatible time/scope limits and month normalization; sufficient price/activity and catalog completeness; recovery horizon/model coefficients and actual order/labor support; Gem/Liquid/Fast Cash/dead/burden thresholds; reference-value-coverage basis if needed; justified comparison tolerances, Hunt normalization/weights and sensitivity. [Provider gates](../PROVIDER_GATES.md#part-level-price-activity-and-refresh-gates--d-025) assigns this evidence to Phases 3–4. These are explicit implementation gates, not missing authorization to complete this documentation.

## 14. Outcome and follow-up

The documentation amendment passes independent acceptance for one local documentation checkpoint. D-025 extends [D-024](../DECISIONS.md#d-024--new-and-used-set-part-out-values--2026-09-06) without rewriting its history; R-11 is retained and R-12–R-37 add explicit capabilities. Four-view budgeting and core full-part-out analysis replace the narrower sold-only/comparison-only assumptions; quantity/color, inclusion, no-double-counting, provenance/rights, unknowns, decimals and no-selling-operations safeguards remain.

### Amendment preparation verification — 2026-09-06

Local Python standard-library checks examined all 36 tracked Markdown files: 219 internal links and 6 fragment targets resolve. Roadmap and prompt 02–08 scope, acceptance and expected-result text align. Requirements R-01–R-37 are sequential; R-11–R-37 each have an individual nine-column traceability row. All 19 documented formula IDs appear in valuation rules, this plan's future test matrix and traceability; no formula runtime tests were executed.

The complete documentation diff was reviewed. D-001–D-024 remain unchanged with only D-025 appended; the original gross-cost/net/profit/ROI/max-buy rules remain unchanged. AGENTS.md, security/privacy, originating history, image ingestion, local-development guidance, Phase 1 plan 000/prompt 01 and roadmap phase blocks 0, 1 and 9–16 remain unchanged. Manual review covers four independent price views, unknown/zero/infinite semantics, physical allocation, gross/net separation, evidence-based configurable policies, no sale guarantees, shared bounded refresh and future feasibility/test gates. Brian's confirmed removal supersedes the initial expectation that the untouched installer would still be untracked.

`git diff --check` passes. `git rev-parse HEAD`, `git status --short`, `git diff --name-only`, `git diff --cached --name-only` and `git ls-files --others --exclude-standard` confirm the same Slice 1B HEAD, exactly the 19 Markdown files below, an empty index and no untracked files. No application/configuration/dependency changes, installations, service/database/container operations, provider/network/infra access, staging, commit or push occurred in this amendment. External links and provider/formula feasibility remain unverified.

Exact modified-file inventory (repository-relative):

```text
CODEX_WORKFLOW.md
README.md
docs/ARCHITECTURE.md
docs/DATA_MODEL.md
docs/DECISIONS.md
docs/PRODUCT_SPEC.md
docs/PROJECT_CONTEXT.md
docs/PROVIDER_GATES.md
docs/REQUIREMENTS_TRACEABILITY.md
docs/ROADMAP.md
docs/VALUATION_RULES.md
docs/plans/005-set-part-out-values.md
prompts/02_catalog_and_relationships.md
prompts/03_market_price_provider.md
prompts/04_feasibility_gate.md
prompts/05_valuation_engine.md
prompts/06_set_search_and_detail.md
prompts/07_deal_calculator_and_saved_work.md
prompts/08_sets_to_hunt.md
```

### Independent acceptance review — 2026-09-06

Starting HEAD is d79395223b5d6fedf78e01dabd3202b5526211eb, with exactly the 19 Markdown changes listed above, an empty index and no untracked files or NVIDIA installer. Complete current documents and the full diff pass the product, evidence, inventory, liquidity, intelligence, strategy/Hunt, provider-scale and phase-ownership review. Narrow corrections update the checkpoint handoff and explicitly retain acquisition-dependent break-even and editable strategy/cost comparisons in Phase 7. No decision or numerical policy is added or rewritten.

Independent documentation-only checks confirm 36 tracked Markdown files, 219 resolving internal links including six fragment targets, unique R-01–R-37 with individual nine-column R-11–R-37 traceability, 19 consistent formula IDs, and matching roadmap/prompt 02–08 inputs/scope/acceptance/expected results. D-001–D-024, existing gross/net/profit/ROI/max-buy rules, protected documents and roadmap phases 0, 1 and 9–16 are unchanged. External references, provider feasibility and application tests are outside this review; none was contacted or run. The local checkpoint remains conditional on the exact staged inventory/content review, credential scan and staged diff check; Git supplies its final hash after commit.

**Exact next authorized action after the local checkpoint:** Phase 1 Slice 1C — web shell, local built serving, browser tests, CI, and complete Phase 1 acceptance. Stop before its separately requested implementation. Slice 1C and Phase 2 implementation remain unstarted; all provider verification, numerical policy calibration and device/deployment work remain separately gated.
