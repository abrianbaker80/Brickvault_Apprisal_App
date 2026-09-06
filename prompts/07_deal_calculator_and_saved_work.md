# Prompt 07 — Deal calculator and saved work

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** A saved deal survives reload and every recommendation reproduces from visible inputs, persisted assumptions, and versioned output, with authenticated access, missing/damaged adjustments, and saved targets/notes/watchlists.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Persist user settings/profile versions, asking/target prices, URLs, notes, figure-unit adjustments, residual-build/instructions/box assumptions, acquisition tax/premiums/travel and selling costs, and immutable input/output snapshots. Add private authentication and revision-conflict tests. Never fetch saved Marketplace URLs. Show both constraint caps and one recommendation, including blocked/undefined states, and prove a saved result reproduces without refetching prices.

## Inputs

Direct set detail and tested valuation engine; reviewed private authentication and persistence design.

## Scope

Asking price, actual contents/condition, build/instructions/box adjustments, selling profiles and costs, proceeds/profit/ROI/max buy, saved sets/deals/notes/watchlists/targets/settings, and Brian-only authentication.

## Exclusions

Recognition/capture, new arithmetic in clients, offline writes, seller automation, provider-rights bypass, and production work. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

A saved deal survives reload and every recommendation reproduces from visible inputs, persisted assumptions, and versioned output, with authenticated access, missing/damaged adjustments, and saved targets/notes/watchlists.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Review authentication and source-retention compatibility before persistent private workflows or any approved non-loopback access; revision conflicts cannot silently overwrite saved work.

Local private tests first; no LAN/public binding change or home access without explicit scope, and provider access remains separately bounded.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
