# Prompt 02 — Catalog and set/minifigure relationships

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Verified fixtures resolve representative numbers/names and return every included minifigure with correct quantities, including duplicates and variants, while ambiguous mappings and malformed data remain explicit.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Test 75331-1-style suffix preservation, ambiguous unsuffixed resolution, name queries at the catalog service boundary, repeated quantities, a verified zero-figure inventory versus unknown inventory, malformed quarantine, idempotent imports, and conflicting provider mappings. Permitted images/references are optional catalog display metadata, not user listing-image ingestion.

## Inputs

Completed local foundation; explicit identity/quantity contracts and permitted local catalog fixtures.

## Scope

Repeatable imports of sets, suffixed-number normalization, names/themes, minifigures, versioned quantity relationships, provider-scoped mappings, provenance, and source versions.

R-11 also requires the catalog portion of the [part-out plan](../docs/plans/005-set-part-out-values.md): versioned component/color quantities, exact mappings, extras/alternates/matching groups and mutually exclusive assembled-figure allocation. Verify these with permitted fixtures; pricing and totals belong to later phases.

## Exclusions

Pricing/valuation implementation, browser search/detail workflow, image ingestion, embeddings, recognition, scraping, and infrastructure changes. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Verified fixtures resolve representative numbers/names and return every included minifigure with correct quantities, including duplicates and variants, while ambiguous mappings and malformed data remain explicit.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Review import/source-use rights before source data is used; no arbitrary suffix stripping or first-match mapping; fixtures do not establish provider access.

Local fixtures suffice for implementation checks; live catalog/download requests require separately authorized network access and verified source permissions.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
