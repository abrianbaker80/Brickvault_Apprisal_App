# Prompt 02 — Catalog and set/minifigure relationships

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Permitted fixtures resolve representative numbers/names, preserve canonical variants and every figure/part/color quantity including repeated figures, expose malformed data and ambiguous mappings, resolve required choices, keep extras separate and prove physical inventory is never double-counted. Unknown mapping/expansion/catalog coverage cannot prove completeness or exclusivity.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Test 75331-1-style suffix preservation, ambiguous unsuffixed resolution, name queries at the catalog service boundary, repeated quantities, a verified zero-figure inventory versus unknown inventory, malformed quarantine, idempotent imports, and conflicting provider mappings. Permitted images/references are optional catalog display metadata, not user listing-image ingestion.

## Inputs

Completed local foundation; explicit identity/quantity contracts and permitted local catalog fixtures.

## Scope

Repeatable set/figure/part/color identities and exact provider mappings, suffix/name/theme semantics, inventory versions/provenance, separate regular/extra quantities, alternate/matching resolution, intact/component figure and nested subset relationships, sourced instructions and later permitted packaging, and scoped exact part/color rarity relationships.

Follow [the D-025 part-out plan](../docs/plans/005-set-part-out-values.md) and its Phase 2 checkpoint. Verify acyclic expansion, physical-piece versus sellable-unit counts, optional exact part/color images, deduplicated known-set counts and first/last appearances where supported. Prices and calculations remain later.

## Exclusions

Pricing/valuation implementation, browser search/detail workflow, image ingestion, embeddings, recognition, scraping, and infrastructure changes. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Permitted fixtures resolve representative numbers/names, preserve canonical variants and every figure/part/color quantity including repeated figures, expose malformed data and ambiguous mappings, resolve required choices, keep extras separate and prove physical inventory is never double-counted. Unknown mapping/expansion/catalog coverage cannot prove completeness or exclusivity.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Review import/source-use rights before source data is used; no arbitrary suffix stripping or first-match mapping; fixtures do not establish provider access.

Local fixtures suffice for implementation checks; live catalog/download requests require separately authorized network access and verified source permissions.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
