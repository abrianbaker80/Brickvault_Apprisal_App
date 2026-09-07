# Product Specification

## Product statement

BrickVault Appraisal App is one private, self-hosted LEGO sourcing and appraisal platform for Brian. Its foundational core is deterministic set-number/name lookup, catalog relationships, market evidence, valuation, saved deals, and Sets to Hunt. The later Marketplace-photo capability is an optional input into this same core, not a competing product or a prerequisite.

This is a planning repository. The current task is documentation realignment; implementation has not started. See [roadmap](ROADMAP.md), [valuation rules](VALUATION_RULES.md), and [requirements traceability](REQUIREMENTS_TRACEABILITY.md).

## Primary workflow

1. Enter a set number, including a suffix such as 75331-1, or search by set name.
2. Resolve the canonical set and inspect whole-set new/sealed and used/complete values, sold evidence, and separately labeled current-listing context.
3. Review every included minifigure, quantity, permitted image/reference, individual new/used values, and quantity-aware totals with availability and provenance.
4. Enter an asking price or evaluate a target price; choose a whole-set or split-sale strategy and adjust actual contents, condition, and costs.
5. Inspect gross/net proceeds, acquisition cost, profit, ROI, both maximum-buy constraints, and the recommended maximum with its explanation.
6. Save the set, deal, notes, URL, target price, and watchlist entry; reuse personal settings.
7. Review Sets to Hunt based on supported split-sale evidence and reproducible ranking.
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

Provide an explainable, versioned view of opportunities to buy sets, sell selected minifigures separately, and sell the remaining build. Rank supported evidence using profit, ROI, maximum buy, coverage, market activity/freshness, confidence, concentration, residual-estimate dependence, and selling burden. Missing critical evidence blocks a supported rank; thin/stale evidence lowers confidence or blocks under the declared policy.

### R-09 — Shared Chrome, PWA, and Android application

Use one primary React interface for responsive Chrome, an installable PWA, and an Android package, preferably Capacitor unless a documented spike justifies a better choice. All use one FastAPI backend, shared user data, and one authoritative PostgreSQL database. Offline caches are dated, limited replicas, not alternate financial truth. Native code is reserved for later capabilities that require it.

### R-10 — Private self-hosting

Eventually host on Brian's home server at an approved subdomain of abrianbaker.com. No host, Proxmox, router, DNS, Cloudflare, public-access, or production activity is currently authorized. Read-only discovery and deployment require distinct future approvals.

### R-11 — New and used set part-out values

Show separate new and used theoretical component totals for a set, using exact quantities/colors and verified component price evidence. Display inclusion policy, currency, sold/current-listing basis, freshness, priced/total lot and unit coverage, and partial/unavailable states. Keep whole-set sale, assembled minifigures and their parts from being double-counted. This is a sourcing comparison, not guaranteed recoverable proceeds or a new fulfillment workflow. Implement through Phases 2–6 under the [part-out plan](plans/005-set-part-out-values.md); no Phase 1 expansion.

## MVP acceptance scenario

Using a verified representative catalog and permitted price observations, Brian enters 75331-1 or a set name without uploading anything, opens the correct variant, and sees whole-set new/used values, separate sold/listing evidence, all included minifigures and quantities, individual prices, and coverage-aware totals.

He enters an asking price, removes or marks a figure damaged, chooses a sale strategy and costs, and obtains a reproducible proceeds/profit/ROI/max-buy calculation. He saves the deal, notes, URL, target price, and watchlist entry and reopens them unchanged. Sets to Hunt explains a supported opportunity and explicitly blocks one with missing critical evidence. Chrome/PWA and the Android core app use the same data and dated offline behavior.

Fixtures may prove deterministic behavior; they do not prove live provider coverage or permission. Phase 4 records that feasibility gate before product confidence is claimed. The feature-complete core spans Phases 1–9, local release hardening Phase 10, and separately authorized discovery/deployment Phases 11–12.

## MVP non-goals

- Image uploads, listing sessions, screenshot recognition, overlays, camera recognition, and training datasets as core dependencies.
- Custom model training, full individual-piece part-out sales, and theoretical part totals presented as cash.
- Facebook scraping, unattended browsing/capture, seller messaging, or automatic purchasing.
- Public accounts, registration/billing/teams, app-store publication, full accounting, or inventory management.
- Public infrastructure or production changes without the separate Phase 11/12 gates.
- Client-side provider calls, independently implemented client valuation arithmetic, or invented source prices.

## Future image-assisted workflow — Phases 13–16

Brian explicitly uploads/shares/captures photos into a later listing session. Immutable originals and distinct derivatives retain lineage. Recognition through server-side OpenAI/Gemini adapters returns candidate canonical set/minifigure identities and evidence; Brian confirms or corrects them separately from predictions. Confirmed selections feed the existing catalog, relationships, market observations, valuation, and saved-deal services.

This extension adds no parallel catalog, provider mapping, pricing, or offer engine. Preserve independent upload results, listing_image_id, deterministic persisted image ordering, and recoverable receipts for successful duplicates under [image ingestion](IMAGE_INGESTION.md). Share/manual upload remain fallbacks for later overlay capture. Explicit retention/deletion and privacy rules must be approved before image ingestion ships; only confirmed, sanitized data can become training-ready.
