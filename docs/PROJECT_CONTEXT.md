# Project Context

## Owner and audience

Brian is the sole user. BrickVault Appraisal App is one private LEGO sourcing and appraisal application, not a public marketplace or subscription service.

## Governing purpose

The foundation answers a deterministic sourcing question: given a set number or name, its included minifigures, reliable condition-specific market evidence, and acquisition/selling assumptions, is the set worth buying? Brian needs whole-set new/used values, each figure's new/used value and quantity, totals, proceeds, profit, ROI, maximum buy, saved deals, and a Sets to Hunt list.

The [product specification](PRODUCT_SPEC.md) and [valuation rules](VALUATION_RULES.md) govern. Every recommendation must expose its evidence and arithmetic; missing information is unknown, not zero.

D-025 makes part-level resale intelligence core alongside whole sets and figures: four NEW/USED × SOLD/CURRENT POV views, supported recoverable gross, liquidity proxies/velocity/supply/absorption, Part-Out Gems, Liquid POV, Fast Cash Value, Dead-Stock Exposure, concentration, break-even lots, value density, burden, competition and scoped rarity. Set Detail and Sets to Hunt use the same server results; theoretical value is not cash and rarity is not liquidity.

## One platform, shared core

Chrome, an installable PWA, and the Android core package share the primary React UI, FastAPI API, user data, and authoritative PostgreSQL database. Catalog identity, set/minifigure relationships, provider mappings, market observations, deterministic valuation, deals, watchlists, settings, and hunting scores belong to that core.

Phase 1 establishes local tooling, shells, migrations, and health/readiness only. Catalog and market feasibility precede valuation, direct search, saved workflows, and hunting. [ROADMAP.md](ROADMAP.md) defines the gates.

## Later Marketplace extension

The originating photo concept addresses sellers who omit set numbers or names. Later user-triggered screenshots, photographs, Android Share, and overlay capture can produce candidate catalog identities for the already-proven core. Recognition never becomes a prerequisite to direct set search or owns independent financial rules.

The [originating summary](ORIGINATING_CHAT_SUMMARY.md) preserves that history. Training-useful original/crop/prediction/correction retention starts when the image feature exists, subject to an explicit privacy and deletion policy. No Facebook scraping, credential interception, unattended navigation, or seller automation is allowed.

## Providers and evidence

Rebrickable and BrickLink are likely catalog/market sources, but access, mapping accuracy, usable new/used sold coverage, retention/display rights, quotas, and historical audit requirements remain unverified gates. Earlier public-document research is preserved with its limits in [PROVIDER_GATES.md](PROVIDER_GATES.md); it is not permission or live account evidence.

Brian previously reported having OpenAI/Gemini keys for the later recognition extension. Do not request secrets in chat, inspect private credentials unnecessarily, or infer current entitlement. All provider secrets and calls remain server-side.

## Hosting and current boundaries

The eventual service should run on Brian's home server under an approved subdomain of abrianbaker.com. The exact hostname, architecture, and access path are not selected by this document.

No home-server, Proxmox, router, DNS, Cloudflare, or production access is currently authorized. Phase 11 requires separate read-only discovery authorization; Phase 12 requires a reviewed deployment plan and distinct execution approval. Local development must isolate this app from the existing PostgreSQL service on port 5432.

## Current checkpoint and future possibilities

The approved detailed Phase 1 plan and actual evidence are recorded in [ExecPlan 000](plans/000-local-foundation.md). Slice 1A is accepted at 150caf7; Slice 1B is accepted and locally committed at d79395223b5d6fedf78e01dabd3202b5526211eb. The subsequent D-025 documentation amendment passes independent acceptance for one local documentation checkpoint. After that checkpoint, the exact next action is **Phase 1 Slice 1C — web shell, local built serving, browser tests, CI, and complete Phase 1 acceptance.** Stop before its separately requested implementation. Slice 1C and Phase 2 implementation remain unstarted. [Prompt 01](../prompts/01_scaffold_foundation.md) remains plan-only when reused; no push or infrastructure work is authorized.

The [existing part-out plan](plans/005-set-part-out-values.md) preserves D-024's useful inventory/inclusion/provenance rules and extends them through Phases 2–8 under D-025, adding normalized activity/shared background refresh, policy feasibility, strategy comparisons/saved assumptions and Hunt components. Full part-out economic analysis is core; operational piece listing/fulfillment remains excluded and selective harvest stays later until supported. Provider capabilities/rights/equivalence, recovery models and final liquidity/Hunt policies remain unverified gates. No provider research, dependency/service/database work or implementation occurred in this amendment.

Later outcomes can personalize resale assumptions. A future sorter integration may help verify contents after purchase, but no sorter integration or separate inventory product is part of this foundation. The starter ZIP remains historical material and never overrides checked-out guidance.
