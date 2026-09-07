# Provider and Device Evidence Gates

## Status and authority

No network resource or external provider was accessed during documentation realignment. The notes below preserve dated bootstrap research from 2026-09-05, not fresh verification. No successful authenticated call, account entitlement, permitted retention policy, representative market coverage, or physical Android behavior has been established by these documents.

Use [ROADMAP.md](ROADMAP.md) for authorization gates and [VALUATION_RULES.md](VALUATION_RULES.md) for evidence semantics. Never scrape HTML, infer permission from private use, or request secrets in chat.

## Catalog and market gates — Phases 2–4

Phase 2 can prove import/identity behavior with permitted local fixtures. Keep explicit canonical set/minifigure records, quantity relationships, provider namespaces, source versions, and mapping review states. Suffixed variants and differing providers' minifigure IDs must not be joined by guessed names or an arbitrary first result.

Phase 3 verifies current official authentication, account eligibility, source-use/display/cache/retention rules, quotas, cost, and outbound-IP requirements before authorized calls or provider-content persistence. Recorded fixtures must have suitable provenance/use rights and be labeled as fixtures. If rights conflict with reproducible saved valuations, record the conflict and block the affected integration; do not silently violate terms or discard audit requirements.

Phase 4 is a separate representative-set feasibility gate, not just a smoke test or recognition benchmark. Cover modern/retired, zero/one/many figures, repeated quantities, a valuable dominant figure, variants/suffixes, unresolved mappings, missing prices, and stale/thin observations. Assess whole-set and per-figure new/used sold evidence, separate current listings, source condition meaning, identifier mappings, quantities, sample windows/counts, freshness, and permitted residual-build estimation.

Record request budgets, provider response/error evidence, approved cache/freshness/retention practices, coverage counts by category, unresolved cases, and a supported/partial/blocked conclusion. Fixture-only runs must say live access/coverage remain unverified and cannot satisfy the live-product feasibility gate. Unknown sample counts and unavailable prices remain unknown, not zero.

Do not claim new/sealed or used/complete if a source's condition flag does not establish those properties. Do not confuse stock listings with completed sales. Rights to metadata, images, provider submission, training, display, caching, and historical snapshots are separate questions.

## Preserved Rebrickable bootstrap findings

The previously reviewed official v3 documentation describes sets, parts, minifigures, and inventories; account API-key authentication; approximately one request per second and 429 handling; CSV downloads for bulk catalogs; and no pricing data. Prefer server-side authorization headers rather than key-bearing URLs.

Downloads/terms pages were inaccessible at bootstrap. Catalog/image reuse, source redistribution, provider submission, and training permissions remain unverified. These notes do not establish Brian's current account access or any current quota.

Research references for a separately authorized future check: [Rebrickable API documentation](https://rebrickable.com/api/v3/docs/).

## Preserved BrickLink bootstrap findings

The published manual previously reviewed describes catalog/price-guide endpoints, OAuth-style HMAC-SHA1 signing, consumer/token credentials, registered client IPs, and current-stock versus six-month-sold statistics with condition/geography/currency parameters.

An accessible legacy terms page stated a default 5,000-call daily allowance and caching/display-freshness restrictions; the current terms page did not expose substantive text at bootstrap. Do not treat the legacy allowance as a current contract. Recheck current account/seller eligibility, authentication, outbound IP, quotas, retention/display terms, and permission for snapshots before implementation.

Research references for a separately authorized future check: [published manual](https://static.bricklink.com/alpha/default/api_wiki.html), [legacy terms](https://www.bricklink.com/help.asp?helpID=2436), [current terms location](https://www.bricklink.com/v3/terms_of_use_api.page).

## Set part-out evidence gate — added 2026-09-06

The new/used [part-out plan](plans/005-set-part-out-values.md) follows public-manual verification of subset inventory and item price-guide methods. An aggregate set part-out-price endpoint was not found in the reviewed method list. Treat inventory-plus-price aggregation as the planned integration, subject to authenticated feasibility and current rights. Verify nested/matching/extra/alternate behavior, source flags, distinct item/color request budgets, and equivalent settings before claiming parity with BrickLink's website. No authenticated provider requests occurred in this planning check.

## Part-level price, activity and refresh gates — D-025

This amendment uses repository planning only: no BrickLink, Rebrickable, eBay, Facebook Marketplace, AI or other provider was contacted. The preceding manual/terms observations remain dated historical findings, not new verification or access authorization. R-11–R-37 in [PRODUCT_SPEC](PRODUCT_SPEC.md) are requirements conditional on the evidence below, not claims that every provider exposes those fields.

### Phase 2 inventory and mapping evidence

Verify canonical/provider part and color/print identity, quantity and separately represented extras, alternate/matching cardinality/resolution, inventory versions, nested subsets and minifigure/component membership. Prove whether instructions/booklets and later packaging are represented and permitted. Verify each intact-versus-component expansion before complete counts or allocation claims. Exact part/color set counts need catalog scope/completeness and deduplicated canonical set relationships; unresolved alternatives cannot prove exclusivity. Optional image display/cache rights are separate, and no borrowed variant image is acceptable.

### Phase 3 capability and field verification

Initially calculate from authoritative inventory plus normalized item-level market observations. Explicitly check current authorized capabilities for direct aggregate POV or equivalent data; record endpoint/parameters, rights, coverage and meaning if one exists, or absence/unavailability if not. A permitted aggregate result is additional evidence/benchmarking, not permission to omit required lot-level provenance. Do not call our output “BrickLink Part Out Value” until equivalence and terminology/display permission are demonstrated.

| Evidence family | Verify and preserve where available |
|---|---|
| Query identity | Provider item type/ID, exact color, mapping revision, NEW/USED, SOLD/CURRENT, currency, geography and all source-affecting request parameters |
| Sold prices | Average, quantity-weighted average, useful minimum/maximum, statistic semantics, currency, source observation interval and sample adequacy; absent statistics never silently substitute |
| Sold activity | Recent sold unit quantity; sale-occurrence count and its exact source meaning; window start/end/duration and boundary rules; units and occurrences remain separate |
| Current prices/supply | Current average/quantity-weighted prices, point-in-time quantity, active inventory and lot counts, seller/store count where separately exposed, sample and observation timestamp |
| Confidence/freshness | Source observed-at, fetched-at and stale-after; independent price/activity availability, coverage, age/skew limits, sample/quantity confidence and dispersion where exposed |
| Rights | Current account eligibility/authentication, display/naming/image/cache/history permissions, request quota/cost and outbound-IP constraints; reproducible-snapshot compatibility |

Do not invent beginning inventory, historical inventory exposure, transaction structure, seller distributions or individual store velocity. If only interval sold activity and current supply exist, S/(S+C) is explicitly a proxy. Unknown fields remain null/insufficient evidence; a genuine supplied zero must retain a verified window and field meaning. Combining incompatible scope/time observations is blocked for the affected metric. Provider listing/lot counts do not automatically mean transactions or sellers.

### Phase 3 request budgets and background refresh

Design normalized observation storage and shared provider caching with exact query identities, cross-set deduplication, provider-specific freshness/refresh intervals, permitted stale-while-refresh, priority jobs/workers, bounded concurrency, rate-limit handling, capped retries/backoff, per-key failure isolation and refresh provenance under [ARCHITECTURE](ARCHITECTURE.md#shared-observation-cache-and-priority-refresh). No synchronous hundreds-of-calls Set Detail design and no Phase 1 worker/queue.

Budget cold inventory/nested resolution plus every distinct item/color/condition/market-side query. A four-view design may need up to four price-guide requests per unique item/color if the provider separates each view, plus separately needed activity/pagination calls; exact capability and counts must be measured, not assumed. Warm overlapping sets reuse compatible observations; a repeated part quantity is not a repeated fetch. Distinguish cached data, in-flight work, negative results and expired forbidden-to-display data.

Prioritize explicit searches, watchlists, Hunt candidates, high-value/high-liquidity lots, stale high-value evidence and broader coverage with bounded quota allocation/fairness. Verify deduplicated work, lease/retry recovery, observation ordering, quota exhaustion, cancellation and stale-data behavior using deterministic barriers/fake clocks in later tests. Do not create extra providers/dependencies/infrastructure merely to support this design.

### Phase 4 representative POV and liquidity benchmark

Compare calculated POV with BrickLink-displayed POV where authorized and practical. Record exact set/inventory version, NEW/USED, SOLD/CURRENT, statistic, currency/region, observation time, nested/figure/extra/alternate/instruction flags and matched/unmatched settings. Report absolute/relative numerical differences and reasons; define justified tolerances before judging agreement, never apply unexplained correction factors. Where comparison is unavailable or impractical, record the reason and unverified equivalence; do not claim a successful comparison or permitted branded naming.

Cover small and very large sets; current/retired; few-lot/high-value and many-lot/low-value; repeated quantities, alternates and extras; figure-heavy sets and valuable non-minifigure parts; high-value/high-velocity, high-value/low-velocity and low-value/high-velocity parts; missing prices, zero sales, very high supply and thin samples. Measure each condition/side's price and activity coverage, proxy/velocity/supply/absorption behavior, supply-versus-occurrence semantics, cold/warm/overlapping-set call volume, cache effectiveness, latency and stale/failure behavior.

Evaluate candidate Gem, Liquid POV, Fast Cash, dead/slow and burden rules, recovery-model horizons/assumptions, concentration and value-density outputs, break-even subset costs, and Hunt normalization/weights/correlated metrics on representative real sets. Record candidate versions, sensitivity and separate calibration/validation results; numerical cutoffs and final Hunt weights are not approved by this amendment. Aggregate market activity cannot establish Brian-specific recovery fractions, labor hours or a sale deadline without additional evidence. Persist a supported/partial/blocked conclusion per capability; a fixture rehearsal cannot pass live feasibility.

## Later AI and recognition gate — Phase 14

Keep OpenAI/Gemini adapters, model IDs, embedding dimensions, prompts, and spending caps configurable and server-side. Prior bootstrap notes described Gemini multimodal image embeddings through gemini-embedding-2 and text-only gemini-embedding-001; model availability, account access, image-use permission, provider data retention, costs, and quality must be reverified in the requested spike.

Use 25–100 deliberately similar/dissimilar catalog sets with rights-cleared references and independently confirmed examples. This is a subset/index of the shared catalog, never a parallel catalog or separate provider mapping system. Compare direct multimodal identification, retrieval alone, and retrieval plus verification; measure top-1, top-3, retrieval recall, unknown handling, latency, and cost. Do not add full vector infrastructure or custom training without demonstrated need.

No paid calls or benchmark results are implied by these notes. Future research reference: [Gemini embeddings](https://ai.google.dev/gemini-api/docs/embeddings). OpenAI use likewise requires official documentation and actual account access in that later authorized task.

## Android core packaging gate — Phase 9

Prefer Capacitor to package the primary React UI; no compatibility spike, installable package, offline synchronization, or physical-device workflow has yet been verified. Document a better choice only if the bounded packaging spike demonstrates a concrete reason. Keep financial arithmetic on the API and test private authentication, cache age, offline states, and saved-record conflict handling on Brian's device.

## Later Android capture gate — Phase 15

Obtain the phone model, Android version, and configured Facebook package before selecting native APIs/toolchain. Earlier public documentation described API 34 takeScreenshotOfWindow and per-session MediaProjection consent; this is not proof of overlay-free Facebook capture.

Prove Share ingestion first, then a visible, user-triggered and allowlisted control. Test permission revocation, secure/unsupported windows, rotation, upload interruption, duplicate receipt replay, display order, disablement, and fallback behavior. Builds/emulators do not establish physical-device compatibility. Network access beyond loopback requires an approved authenticated access design; no silent binding changes.

Future research references: [AccessibilityService](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService), [MediaProjection](https://developer.android.com/media/grow/media-projection). No automatic swipes, clicks, interception, background collection, or seller automation is permitted.
