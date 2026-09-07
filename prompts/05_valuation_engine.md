# Prompt 05 — Deterministic valuation engine

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Table-driven exact-arithmetic tests reproduce every valuation/liquidity formula and policy, covering complete/missing/damaged/repeated inventory, four-view and gross/net separation, zero/unknown/infinite states, partial coverage, alternate/extra/figure allocation, stable concentration/break-even ties, subset costs, policy boundaries and acquisition tax/premiums without double-counting.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Follow docs/VALUATION_RULES.md exactly. Use Decimal/NUMERIC and decimal-string contracts. Test C(p)=p*(1+t)+A, profit=N-C(p), undefined ROI at zero C, ROI and minimum-profit caps, constraint enablement, downward purchasable-cap rounding/recheck, zero clamp with no-feasible-purchase explanation, nonlinear acquisition rules, currencies, quantity groups, missing/damaged figures, order fees, risk reserve, and no-double-count strategies. Engine tests run without provider credentials or UI.

## Inputs

Phase 4 feasibility outcome, exact valuation rules, verified representative fixtures, and supported evidence policies.

## Scope

Pure server calculations for four-view theoretical/recoverable POV, proxy/velocity/supply/absorption/occurrences, opportunities/Gems, Liquid/Fast Cash/dead-stock, concentration, break-even lots, value per lot/piece, burden, competition/rarity, POV premium and separate strategy economics. Retain exact costs/profit/ROI/both max-buy constraints and versioned partial/blocked snapshots.

Follow [the D-025 part-out plan](../docs/plans/005-set-part-out-values.md) and its Phase 5 checkpoint. Implement every planned formula test in VALUATION_RULES and only Phase 4-supported policies. Unknown full-value coverage cannot become 100%, absent activity cannot become dead stock and expensive/rare alone cannot make a Gem. Full part-out analysis is core; selective harvest remains evidence-gated and selling operations remain excluded.

## Exclusions

UI financial logic, live provider calls required by unit tests, image/AI work, operational individual-piece listing/fulfillment, automatic purchasing, and production access. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Table-driven exact-arithmetic tests reproduce every valuation/liquidity formula and policy, covering complete/missing/damaged/repeated inventory, four-view and gross/net separation, zero/unknown/infinite states, partial coverage, alternate/extra/figure allocation, stable concentration/break-even ties, subset costs, policy boundaries and acquisition tax/premiums without double-counting.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Review formula/rounding/constraint examples and unsupported-evidence behavior before exposing recommendations; preserve rights-compliant reproducibility.

Local deterministic fixtures; dependency access only if separately authorized for implementation, no product-provider or server access needed.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
