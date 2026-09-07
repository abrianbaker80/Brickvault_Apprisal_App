# Product Specification

## Product statement

BrickVault Appraisal App is one private, self-hosted LEGO sourcing and appraisal platform for Brian. Its foundational core is deterministic set-number/name lookup, catalog relationships, market evidence, valuation, saved deals, and Sets to Hunt. The later Marketplace-photo capability is an optional input into this same core, not a competing product or a prerequisite.

The sourcing product remains planned. The local foundation through Slice 1B is committed at d79395223b5d6fedf78e01dabd3202b5526211eb; Slice 1C is not started. The Part-Out Value and liquidity amendment is documentation only under D-025. See [roadmap](ROADMAP.md), [valuation rules](VALUATION_RULES.md), and [requirements traceability](REQUIREMENTS_TRACEABILITY.md).

## Primary workflow

1. Enter a set number, including a suffix such as 75331-1, or search by set name.
2. Resolve the canonical set and inspect whole-set new/sealed and used/complete values, sold evidence, and separately labeled current-listing context.
3. Review every included minifigure, quantity, permitted image/reference, individual new/used values, and quantity-aware totals with availability and provenance.
4. Inspect Part-Out Analysis: four condition/market views, part-level demand/supply, Part-Out Gems, recoverable gross, liquidity, coverage and burden. Enter an asking price or evaluate a target price; compare whole-set, figures plus remaining build and supported full part-out strategies, adjusting actual contents, condition and costs. Selective harvest remains later until supported.
5. Inspect gross/net proceeds, acquisition cost, profit, ROI, both maximum-buy constraints, and the recommended maximum with its explanation.
6. Save the set, deal, notes, URL, target price, and watchlist entry; reuse personal settings.
7. Review Sets to Hunt using supported strategy economics, part-level liquidity, concentration, competition, rarity, burden and reproducible component explanations.
8. Use the same React interface and server data in Chrome, the PWA, and Android; later record actual outcomes.

Every step through the sourcing core works with all image and recognition modules disabled. Saving a listing URL does not fetch it or create an image listing session.

## Authoritative requirements

### R-01 — Set-number and name search

Accept explicit suffixed identifiers such as 75331-1 and name queries. Preserve canonical variant identity; unsuffixed or ambiguous input must produce an explicit resolution choice, not an arbitrary match. Provider-scoped identifiers are mapped with provenance and review state.

### R-02 — Whole-set market evidence

Display new/sealed and used/complete values separately, subject to evidence that supports those condition/completeness claims. Separate sold-market evidence from current-listing context. Show source, provider item ID, currency, observation period/time, freshness, sample information, and unavailable/stale/thin states; asking prices are not sold prices.

### R-03 — Included minifigures

Show every included minifigure's identity, quantity, permitted image or image reference, individual new value, individual used value, source, freshness, and explicit unknown/unavailable state. Cross-provider mappings and complete relationships must be proven before claiming complete coverage.

### R-04 — Minifigure totals

Show quantity-aware new and used totals plus adjusted deal totals. Report priced/total/unavailable quantities, coverage, concentration, and partial/blocked status. A known no-figure set differs from an unknown inventory.

### R-05 — Deal mathematics

Given an asking price and visible assumptions, show expected gross proceeds, selling costs, net proceeds, total acquisition cost, expected profit, ROI, maximum purchase by target ROI, maximum purchase by minimum required profit, and one recommended maximum with an explanation. [VALUATION_RULES.md](VALUATION_RULES.md) governs every calculation and rounding rule.

### R-06 — Contents and cost adjustments

Support absent figures, damaged/incomplete figures, incomplete remaining build, and missing instructions/box where relevant. Record fees, seller shipping, packaging, acquisition tax, buyer premiums, travel/pickup, risk reserve, and other explicit configured costs. Do not double-count a physical item or a cost.

### R-07 — Saved work and settings

Persist saved sets, watchlist entries, target purchase prices, Marketplace/other listing URLs, asking prices, notes, deal analyses, user valuation settings, and selling profiles. Later append actual purchase/resale outcomes without rewriting the original forecast. Saved records reference canonical sets and immutable calculation versions, not required photo sessions.

### R-08 — Sets to Hunt

Provide an explainable, versioned view of opportunities across the supported mutually exclusive sale strategies. Retain profit, ROI, maximum buy, figure coverage/concentration, residual-estimate dependence and selling burden; add the first-class part-level signals in R-36. Missing critical evidence blocks a supported rank; thin/stale evidence lowers confidence or blocks under the declared policy. High theoretical POV alone cannot justify a high rank.

### R-09 — Shared Chrome, PWA, and Android application

Use one primary React interface for responsive Chrome, an installable PWA, and an Android package, preferably Capacitor unless a documented spike justifies a better choice. All use one FastAPI backend, shared user data, and one authoritative PostgreSQL database. Offline caches are dated, limited replicas, not alternate financial truth. Native code is reserved for later capabilities that require it.

### R-10 — Private self-hosting

Eventually host on Brian's home server at an approved subdomain of abrianbaker.com. No host, Proxmox, router, DNS, Cloudflare, public-access, or production activity is currently authorized. Read-only discovery and deployment require distinct future approvals.

### R-11 — New and used set part-out values

Show separate NEW and USED theoretical component totals using exact quantities/colors and verified prices. Preserve D-024's inclusion, provenance, coverage and no-double-counting rules. D-025 extends the [existing part-out plan](plans/005-set-part-out-values.md) through Phases 2–8 with the requirements below; no Phase 1 expansion or fulfillment workflow is implied.

### R-12 — Sold and current POV views

Provide NEW + SOLD, NEW + CURRENT, USED + SOLD and USED + CURRENT independently. Each states exact price statistic, currency, observation/freshness, inclusion rules, intact/component minifigure mode and extra-part mode. CURRENT means current-for-sale asking evidence, never completed sales; no silent cross-view fallback.

### R-13 — Physical inventory semantics

Preserve canonical/provider part identity, exact color/variant, regular/extra quantities, alternate/matching groups, inventory version, figure/subset membership and provenance. Support verified intact versus component figure allocation, instruction/booklet inventory where relevant and permitted packaging only when later supported. Required choices resolve explicitly; alternate possibilities are not all present and extras do not silently become required pieces.

### R-14 — POV result and evidence coverage

Every result preserves set/inventory identity, selected quantities and unique lots, priced/unpriced quantities and lots, missing lines, value/quantity/activity coverage with honest denominators, source observations/timestamps, inclusion resolutions, calculation version and complete/partial/blocked reasons. Unknown price remains UNKNOWN. An unknown full-value denominator yields undefined value coverage, never a fabricated 100%; partial subtotals stay visibly partial. The minimum contract is in the part-out plan and DATA_MODEL.

### R-15 — Expected recoverable part-out value

Expose deterministic, versioned, explainable expected recoverable gross separately from theoretical POV, net proceeds and profit. Account for liquidity, sales/supply, unsold/low-value/long-tail lots, evidence quality, consolidation, listings/orders and burden through supported assumptions. Itemized fees, shipping, packaging and labor are deducted once when deriving net proceeds. No unsupported recovery coefficient or theoretical cash claim.

### R-16 — Part-level market activity

For exact part/color/condition and compatible market scope, retain sold quantity, sale occurrences, actual observation window, sold price statistics, current quantity, inventories/lots/stores where exposed, current statistics, timestamps, freshness and sample confidence. Current supply is a point-in-time snapshot; recent sales cover an interval. Unknown provider fields stay unknown.

### R-17 — Sell-through proxy

Show S / (S + C) for compatible recent sold quantity S and current supply C. Label it a market-liquidity proxy, with the actual window; use “six-month” only for a verified six-month window. It is not a historical inventory-turn rate. Zero denominator is undefined, never 0%.

### R-18 — Monthly sales velocity

Show sold units divided by actual observation-period months, separately from occurrence frequency. Preserve the window and versioned month-normalization convention; do not assume six months or substitute transaction counts for units.

### R-19 — Months of supply

Show current quantity divided by monthly unit velocity, with explicit finite, infinite, undefined or insufficient-evidence state under VALUATION_RULES. Zero or unavailable velocity cannot cause division by zero or fake liquidity. This indicator is not a promised sale timeline.

### R-20 — Set-quantity absorption time

For each lot show selected quantity contributed by one set divided by monthly unit velocity. Explain demand-equivalent months, preserve zero/unknown cases and aggregate distributions at set level. Market-wide demand is not Brian's captured demand and does not establish a liquidation deadline.

### R-21 — Sales-occurrence frequency

Preserve supplied occurrence count and frequency separately from sold units. One occurrence containing 100 pieces differs from 60 occurrences containing 100 pieces; do not call provider occurrences transactions or orders unless source semantics establish that meaning.

### R-22 — Part opportunities and Part-Out Gems

Expose value, demand, supply, absorption, confidence and catalog-presence dimensions before any combined score. Version classifications HIGH VALUE / HIGH LIQUIDITY, HIGH VALUE / MEDIUM LIQUIDITY, HIGH VALUE / LOW LIQUIDITY, LOW VALUE / HIGH VELOCITY, VERY SLOW / DEAD-STOCK CANDIDATE and INSUFFICIENT DATA. A Gem needs material contributed value plus supported liquidity/confidence, never price alone. Show exact identity/color/quantity, permitted image/reference, unit/contributed value, activity/supply/occurrences/sellers, proxy/velocity/supply-months/absorption, rarity, freshness and reason, with unavailable fields marked.

### R-23 — Liquid POV

Show the portion of theoretical POV qualifying under documented liquidity/confidence rules, its percentage, qualifying lots and value excluded as slow, thin or unknown. Unknown inventory value stays unvalued and separately counted. Thresholds are configurable, deterministic and versioned, validated in Phase 4; no guaranteed proceeds.

### R-24 — Fast Cash Value

Show theoretical or explicitly conservatively adjusted gross for a stricter near-term liquidity policy, percentage of POV, qualifying lots/pieces, threshold/version and confidence. Label the chosen basis. Select configurable thresholds only after Phase 4 validation; do not promise a sale date.

### R-25 — Dead-Stock Exposure

Show supported slow/dead theoretical value, percentage, lots and quantity with classification/version. Zero/near-zero sales, excessive supply or low frequency may support the classification; stale/thin evidence weakens it. Missing evidence produces INSUFFICIENT DATA, not proven dead stock.

### R-26 — Value concentration

Show highest-value lot, top-5/top-10 values and POV percentages, high-value-lot concentration and high-liquidity-value concentration. Preserve figure concentration separately. Disclose partial denominators and deterministic lot/tie rules; reveal both valuable few-lot and fragmented many-lot inventories.

### R-27 — Break-even lots

Given an acquisition target, show highest theoretical-value and value/liquidity/confidence-ranked lot prefixes needed to cover it. Return lots, quantities, identities, theoretical and supported recoverable contributions, inventory percentages and confidence. Distinguish gross target coverage from economic break-even after costs; neither guarantees sales. Insufficient qualifying contribution is explicit.

### R-28 — Value per unique lot

Show expected recoverable gross divided by selected unique sellable lot count, with its recovery assumptions and denominator. Preserve undefined/partial states; this operational-efficiency measure is not a standalone recommendation.

### R-29 — Value per piece

Show expected recoverable gross divided by total selected physical piece quantity, independently of value per lot. Disclose how intact figures/subsets contribute to physical counts; unknown expansion cannot become a guessed denominator.

### R-30 — Operational burden

Preserve unique lots, physical pieces, expected listings/orders where supported, average lot value, low/high-value-lot percentages and fragmentation. LOW/MEDIUM/HIGH categories require deterministic versioned rules; precise labor hours require evidence. Costs and recovery assumptions remain separately explained.

### R-31 — Market competition

Show current units, inventory/lot count and seller/store count separately where exposed. Thirty pieces across three versus 28 sellers is different evidence. Do not derive seller concentration without the underlying distribution.

### R-32 — Rarity and catalog presence

Count known sets containing the exact part/color combination, with catalog scope/version/completeness and optional first/last appearances. Claim exclusive-to-one-set or low-set-count only within demonstrated scope. Rarity is separate from liquidity and cannot qualify a Gem alone.

### R-33 — Part-out strategy comparison

Compare complete set; selected figures plus remaining build; full part-out; and later selective high-value-lot harvest when supported. Each result preserves theoretical and expected gross, selling/acquisition costs, net, profit, ROI/max-buy, burden, liquidity and confidence. Only one strategy is active; each physical unit appears once within it. Removed figures/parts cannot remain in residual value.

### R-34 — POV premium

Show POV / comparable whole-set value - 1 using matching condition, SOLD/CURRENT basis, currency and disclosed statistic/window/inclusion assumptions. Zero or unknown whole-set denominator is undefined. Incompatible comparisons are labeled scenarios and excluded from default ranking.

### R-35 — Provider caching and background refresh

Reuse normalized exact part/color observations across sets. Phase 3 designs rights-compliant caching, deduplicated priority background refresh, freshness windows, stale-while-refresh where allowed, bounded concurrency, quota handling, retry/backoff, provider intervals, failure isolation and provenance. Set Detail must not synchronously fan out hundreds of provider calls. No queue/worker belongs to Phase 1.

### R-36 — Part-level Sets-to-Hunt intelligence

Decompose purchase economics, POV premium/recoverable/Liquid/Fast Cash/Dead-Stock measures, Gems and concentrations, supply/absorption distributions, break-even lots, value density, burden, competition, rarity and price/activity/mapping/sample/freshness confidence. An eventual combined score is deterministic, versioned and calibrated on representative real sets in Phase 4; do not choose final weights now. Required evidence gaps block or reduce support explicitly.

### R-37 — Set-level Part-Out Analysis

Set Detail exposes all four POV views and the catalog-level R-14–R-34 metrics, including price/activity coverage, counts of qualifying high-value/Gem lots with quantities shown separately, total selected pieces/lots and confidence. Acquisition-dependent break-even results and editable strategy/cost comparisons enter through the Phase 7 deal workflow. Provide evidence drill-down, high-value/low-liquidity warnings and pending/stale/partial/blocked states. Generated API contracts supply server results; direct number/name lookup remains independent of recognition.

## Part-Out Analysis UX concept — planned Phase 6

| Theoretical Part Out Value | SOLD evidence | CURRENT asking evidence |
|---|---|---|
| NEW | Amount or explicit unavailable state | Amount or explicit unavailable state |
| USED | Amount or explicit unavailable state | Amount or explicit unavailable state |

Below the matrix, show selected basis and inclusion controls, expected recoverable gross, Liquid POV, Fast Cash Value, Dead-Stock Exposure, POV premium, coverage/freshness, unique lots, physical pieces, value per lot/piece and burden. Gem cards show quantity, unit/contributed value, activity and liquidity reasons; a separate high-value/low-liquidity area exposes slow demand. Top-5/top-10 and fast-liquidity panels disclose denominators and policy versions. Every metric links to permitted source observations and its formula/assumptions. No placeholder amount is live evidence or a promised outcome.

## MVP acceptance scenario

Using a verified representative catalog and permitted price observations, Brian enters 75331-1 or a set name without uploading anything, opens the correct variant, and sees whole-set new/used values, separate sold/listing evidence, all included minifigures and quantities, individual prices, and coverage-aware totals.

He enters an asking price, removes or marks a figure damaged, chooses a sale strategy and costs, and obtains a reproducible proceeds/profit/ROI/max-buy calculation. He saves the deal, notes, URL, target price, and watchlist entry and reopens them unchanged. Sets to Hunt explains a supported opportunity and explicitly blocks one with missing critical evidence. Chrome/PWA and the Android core app use the same data and dated offline behavior.

He also compares the four POV views, inspects valuable liquid lots versus high-value slow lots, sees partial price/activity coverage, and compares supported full part-out economics against complete/split sale. Saved analyses retain allocation, recovery assumptions and thresholds; Hunt explanations include liquidity and burden rather than ranking on theoretical value alone. Selective harvest stays unavailable until its evidence gate passes.

Fixtures may prove deterministic behavior; they do not prove live provider coverage or permission. Phase 4 records that feasibility gate before product confidence is claimed. The feature-complete core spans Phases 1–9, local release hardening Phase 10, and separately authorized discovery/deployment Phases 11–12.

## MVP non-goals

- Image uploads, listing sessions, screenshot recognition, overlays, camera recognition, and training datasets as core dependencies.
- Custom model training, operational individual-piece listing/fulfillment or inventory management, and theoretical part totals presented as cash. Full part-out analysis is core under D-025; selling operations remain excluded.
- Facebook scraping, unattended browsing/capture, seller messaging, or automatic purchasing.
- Public accounts, registration/billing/teams, app-store publication, full accounting, or inventory management.
- Public infrastructure or production changes without the separate Phase 11/12 gates.
- Client-side provider calls, independently implemented client valuation arithmetic, or invented source prices.

## Future image-assisted workflow — Phases 13–16

Brian explicitly uploads/shares/captures photos into a later listing session. Immutable originals and distinct derivatives retain lineage. Recognition through server-side OpenAI/Gemini adapters returns candidate canonical set/minifigure identities and evidence; Brian confirms or corrects them separately from predictions. Confirmed selections feed the existing catalog, relationships, market observations, valuation, and saved-deal services.

This extension adds no parallel catalog, provider mapping, pricing, or offer engine. Preserve independent upload results, listing_image_id, deterministic persisted image ordering, and recoverable receipts for successful duplicates under [image ingestion](IMAGE_INGESTION.md). Share/manual upload remain fallbacks for later overlay capture. Explicit retention/deletion and privacy rules must be approved before image ingestion ships; only confirmed, sanitized data can become training-ready.
