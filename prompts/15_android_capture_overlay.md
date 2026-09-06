# Prompt 15 — Android share and overlay capture

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Physical-device evidence proves supported Share/capture flows and fallback/permission/failure behavior while the same core UI/API/data and direct lookup remain usable when capture is disabled.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. First create a bounded native-extension/physical-device spike: Share to existing/new optional listing, then supported screenshot APIs, visible allowlisted capture, permission revocation/secure windows/rotation/failure/disablement, and manual fallback. The first spike excludes OCR, crop polish, and carousel interpretation; keep experimental capture behind a disableable interface so Share remains functional. Only after that gate passes, plan polished manual multi-photo collection, exact/near-dedupe, crop/circle/reorder, optional permitted text extraction, review, and result handoff as a separately requested checkpoint. Preserve listing_image_id and UUID/display_order/receipt semantics across retries. Never automate Facebook swipes/clicks.

## Inputs

Working shared-UI Android core, proven image API, recognition findings, approved retention policy, and Brian's physical-device details.

## Scope

Needed native Share extension and isolated visible user-triggered allowlisted capture spike; only after device proof, manual multi-photo review/crop/order and result handoff with robust partial retries.

## Exclusions

A second native core app, automatic browsing/swipes/clicks, Facebook traffic/credential interception, unattended capture, independent valuation, and unapproved infrastructure access. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Physical-device evidence proves supported Share/capture flows and fallback/permission/failure behavior while the same core UI/API/data and direct lookup remain usable when capture is disabled.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Separate spike results from polished follow-on work; do not claim Facebook compatibility from an APK/emulator or move past a failed device gate.

Explicitly authorized Android SDK/device tests and supported-API research; any secure device/backend networking is scoped separately from production administration.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
