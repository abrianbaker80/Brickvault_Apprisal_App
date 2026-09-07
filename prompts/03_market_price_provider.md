# Prompt 03 — Market-price provider integration

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Authorized calls or labeled permitted fixtures preserve four-view price/activity semantics and unknowns. Shared-part refresh tests prove deduplication, quota/backoff bounds, stale/failure isolation and no synchronous per-set fan-out; live aggregate capability and rights are explicitly verified.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Read docs/PROVIDER_GATES.md. Preserve request parameters, provider item namespace/type, mapping revision, raw/normalized condition, sold/current_listing side, exact currency amount, statistic, period, observed/fetched/stale-after times, and supplied sample counts/quantities. Test timeouts/429/backoff, thin/stale/missing results, and mapping conflicts. A source new flag does not by itself prove sealed; used does not by itself prove complete. Do not assume cached observations can be retained forever.

## Inputs

Verified canonical identities/relationships and mappings; provider-gate checklist and permitted fixtures.

## Scope

Server-side set/figure/part observations for NEW/USED and SOLD/CURRENT, exact currency/statistics, sold units/occurrences/window, point-in-time current units and supplied inventory/lot/store counts, freshness and confidence. Verify aggregate capabilities and design shared observation caching, deduplicated priority background refresh, request budgets and bounded concurrency/retries.

Follow [the D-025 part-out plan](../docs/plans/005-set-part-out-values.md) and its Phase 3 checkpoint. Preserve average/quantity-weighted and useful min/max statistics; never infer transactions from occurrences, sellers from lots or historical inventory from current supply. Use the existing backend/PostgreSQL for bounded priority jobs; test cold/warm/overlapping-set budgets, leases, late responses and timestamp skew with fake clocks/barriers. No branded equivalence claim before permission and Phase 4 comparison.

## Exclusions

Scraping, guessed mappings, browser/Android secrets, valuation UI, recognition, unlimited retention assumptions, and infrastructure administration. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Authorized calls or labeled permitted fixtures preserve four-view price/activity semantics and unknowns. Shared-part refresh tests prove deduplication, quota/backoff bounds, stale/failure isolation and no synchronous per-set fan-out; live aggregate capability and rights are explicitly verified.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Verify current official authentication/eligibility, rights/display/cache/retention, quotas/cost, and outbound-IP requirements before live calls or provider-content persistence; missing permissions block that path.

Network/provider access is required for live proof and must be explicitly authorized; recorded-fixture checks remain distinguishable and cannot certify live access.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
