# Prompt 05 — Deterministic valuation engine

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Table-driven tests reproduce every displayed calculation for complete, missing, damaged, repeated, unavailable, and variable-tax/premium cases without double-counting minifigures or costs.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Follow docs/VALUATION_RULES.md exactly. Use Decimal/NUMERIC and decimal-string contracts. Test C(p)=p*(1+t)+A, profit=N-C(p), undefined ROI at zero C, ROI and minimum-profit caps, constraint enablement, downward purchasable-cap rounding/recheck, zero clamp with no-feasible-purchase explanation, nonlinear acquisition rules, currencies, quantity groups, missing/damaged figures, order fees, risk reserve, and no-double-count strategies. Engine tests run without provider credentials or UI.

## Inputs

Phase 4 feasibility outcome, exact valuation rules, verified representative fixtures, and supported evidence policies.

## Scope

Implement pure server-side arithmetic and serializable versioned input/output snapshots for quantities, strategies, adjustments, costs, profit/ROI, both maximum-buy constraints, and blocked/partial results.

Include separate new/used theoretical aggregation under the [R-11 part-out plan](../docs/plans/005-set-part-out-values.md). Verify quantity/color-aware decimal sums, inclusion-policy snapshots, partial coverage and no assembled-figure/component double counting. Theoretical totals do not themselves establish realizable proceeds or a maximum offer.

## Exclusions

UI financial logic, live provider calls required by unit tests, image/AI work, operational individual-piece listing/fulfillment, automatic purchasing, and production access. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Table-driven tests reproduce every displayed calculation for complete, missing, damaged, repeated, unavailable, and variable-tax/premium cases without double-counting minifigures or costs.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Review formula/rounding/constraint examples and unsupported-evidence behavior before exposing recommendations; preserve rights-compliant reproducibility.

Local deterministic fixtures; dependency access only if separately authorized for implementation, no product-provider or server access needed.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
