# Prompt 00 — Bootstrap and plan

**Mode:** Plan only

**Expected result:** The in-chat plan preserves the ten requirements and defines only the local foundation, with reviewable assumptions and a stop before edits or implementation.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Read every checked-out guidance/product document, .agent/PLANS.md, and the current ExecPlan before proposing changes. Preserve D-001 through D-021 historical meaning and apply the current additive decisions, including D-022's Phase 1 slice/checkpoint boundaries. Return an in-chat plan only; do not persist edits unless Brian separately requests a Markdown checkpoint. Revalidation cannot reactivate the historical image-first sequence.

## Inputs

Authoritative product definition, current guidance, decision history, and the product-scope audit.

## Scope

Read/revalidate the unified product and bounded Phase 1 ExecPlan; keep valuation-first ordering and historical decisions explicit.

## Exclusions

Application implementation, installations, services, provider/network calls, infrastructure access, and staging/commits. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

The in-chat plan preserves the ten requirements and defines only the local foundation, with reviewable assumptions and a stop before edits or implementation.

Validate the plan against the ten requirements and the phase boundary; do not claim application checks ran.

## Gate and access

The reviewed documentation baseline is the Phase 0 checkpoint; subsequent revalidation is plan-only unless Brian separately requests Markdown/local-Git work.

Local read-only files only; no network, devices, or servers.

## Stop condition

Return the in-chat plan and stop without edits or implementation.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
