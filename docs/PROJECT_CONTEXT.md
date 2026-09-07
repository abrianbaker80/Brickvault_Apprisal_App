# Project Context

## Owner and audience

Brian is the sole user. BrickVault Appraisal App is one private LEGO sourcing and appraisal application, not a public marketplace or subscription service.

## Governing purpose

The foundation answers a deterministic sourcing question: given a set number or name, its included minifigures, reliable condition-specific market evidence, and acquisition/selling assumptions, is the set worth buying? Brian needs whole-set new/used values, each figure's new/used value and quantity, totals, proceeds, profit, ROI, maximum buy, saved deals, and a Sets to Hunt list.

The [product specification](PRODUCT_SPEC.md) and [valuation rules](VALUATION_RULES.md) govern. Every recommendation must expose its evidence and arithmetic; missing information is unknown, not zero.

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

The approved detailed Phase 1 plan and actual evidence are recorded in [ExecPlan 000](plans/000-local-foundation.md). Slice 1A is accepted at 150caf77820d09c60d028eeeba5b1b4317e11539; Slice 1B isolated PostgreSQL, API, migrations and contracts passes acceptance for the explicitly authorized local checkpoint. The next authorized action is the separately approved Part-Out Value + liquidity documentation amendment, not executed by this review. Slice 1C (web/built serving/CI/acceptance) requires a separate explicit request. [Prompt 01](../prompts/01_scaffold_foundation.md) remains plan-only when reused. No push or infrastructure work is authorized.

Brian also requested separate new/used set part-out values. The [part-out plan](plans/005-set-part-out-values.md) places inventory, market feasibility, deterministic aggregation and display in Phases 2–6. It records API/documentation uncertainty and coverage gates; no valuation feature or authenticated provider access is implemented in Slice 1B.

Later outcomes can personalize resale assumptions. A future sorter integration may help verify contents after purchase, but no sorter integration or separate inventory product is part of this foundation. The starter ZIP remains historical material and never overrides checked-out guidance.
