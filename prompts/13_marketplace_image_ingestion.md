# Prompt 13 — Marketplace image ingestion

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** Images attach to optional listings without affecting direct lookup, original bytes/lineage survive restart, and real concurrency/failure tests prove deterministic order and recoverable successful-duplicate receipts.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Read docs/IMAGE_INGESTION.md in full and preserve its exact identity/ordering/receipt/failure contract. Test A@0, B@1, A-copy@2 in reversed completion orders; changed UUID bytes/order conflicts; receipt high-water append; lower-position retry; shared originals; real decoder/size/format errors; DB/filesystem failures; and lost successful-duplicate response replay. Approve retention/deletion/privacy policy before shipping. Direct set lookup must pass unchanged with the image module disabled.

## Inputs

Proven deterministic core, separately requested image ExecPlan, and reviewed image privacy/retention/deletion policy.

## Scope

Optional listing metadata/session workflow, multi-file upload, immutable originals, exact dedupe, thumbnails/lineage, listing_image_id, independent partial success, stable UUID/display_order, duplicate receipts, and report-only consistency checking.

## Exclusions

Recognition/model calls, new catalogs/pricing/offer formulas, native capture, near-duplicate/crop polish, training exports, automatic deletion, and infrastructure changes. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

Images attach to optional listings without affecting direct lookup, original bytes/lineage survive restart, and real concurrency/failure tests prove deterministic order and recoverable successful-duplicate receipts.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Apply IMAGE_INGESTION.md and approve explicit retention/deletion/privacy policy before shipping; current documentation never authorizes image handling or production deployment.

Local authorized image fixtures and isolated services; no source-URL fetching or provider calls, and production rollout remains separately authorized.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
