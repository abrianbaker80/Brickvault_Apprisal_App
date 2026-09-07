# Prompt 06 — Set search and detail vertical slice

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Brian enters a set number or name without images, resolves the correct variant, and sees whole-set values plus every included minifigure, quantities, individual values, quantity-aware totals, provenance/freshness, and explicit missing-data indicators.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Use the shared generated /api contract and server-calculated totals. Verify canonical suffix/ambiguity handling, both whole-set conditions and market sides, every figure/quantity, individual new/used prices, permitted image/reference or placeholder, totals/coverage/concentration, freshness and unavailable states. Exercise desktop/mobile Chrome-compatible browser routes with image/recognition modules absent. Do not confuse correcting a recognized identity with direct search.

## Inputs

Verified catalog/market contracts, passed feasibility gate, and tested valuation totals/coverage functions.

## Scope

Direct suffixed-number/name search and a set-detail API/React page with whole-set and minifigure new/used values, quantities/totals, permitted images/references, separate market sides, provenance, and unavailable states.

Display both server-calculated new/used values from the [R-11 part-out plan](../docs/plans/005-set-part-out-values.md), with inclusion choices, price basis, currency, freshness, lot/unit coverage and expanded component details. Browser acceptance must distinguish complete, partial and unavailable totals and identify them as theoretical values.

## Exclusions

Listing sessions, user image uploads, recognition, separate client formulas, saved-deal editing, and deployment. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Brian enters a set number or name without images, resolves the correct variant, and sees whole-set values plus every included minifigure, quantities, individual values, quantity-aware totals, provenance/freshness, and explicit missing-data indicators.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Browser/API acceptance must cover ambiguity, no-figure, repeated-figure, and unavailable-price cases with image modules disabled.

Local fixtures/cached permitted evidence for tests; any live refresh remains within the already verified and explicitly authorized provider scope.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
