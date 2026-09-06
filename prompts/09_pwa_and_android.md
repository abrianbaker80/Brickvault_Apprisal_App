# Prompt 09 — PWA, offline behavior, and Android core app

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Chrome/PWA and Android support set search/detail, deal analysis, saved work, and watchlists through one backend/database, and cached information is dated without representing stale prices as current.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Start with a bounded Capacitor packaging spike and reuse apps/web as the primary interface. Document a different choice only with concrete evidence. Initial offline mode is read-only dated permitted caches; new search, price refresh, recalculation, and writes require connectivity. Test server revisions/conflicts, logout/session-expiry caches, authentication, device URL configuration, and physical core flows. Provider credentials and financial algorithms never move into the bundle.

## Inputs

Private sourcing workflows, shared React UI/API, versioned saved work, and an authorized Android packaging test environment.

## Scope

Installable PWA and preferably Capacitor Android package of the same UI, private auth, dated read-only caches, explicit offline states, and server-revision synchronization.

## Exclusions

Separate native core UI/database/valuation engine, offline financial recalculation/writes, overlay/capture/Share implementation, and home deployment. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Chrome/PWA and Android support set search/detail, deal analysis, saved work, and watchlists through one backend/database, and cached information is dated without representing stale prices as current.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Document the packaging spike and any justified alternative; test physical Android core workflows and auth/cache expiry/sync conflicts separately from compilation.

Authorized local SDK/dependency acquisition and physical Android device testing; device-to-API networking needs explicit secure scope, not home-server access.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
