# Plan 104 — Phase 14A recognition pilot

## Goal and user-visible outcome

One local Python CLI accepts operator-selected photos and optional sanitized text,
returns uncertain set/minifigure candidates, resolves exact shared catalog identities,
and reports preliminary quality, latency and estimated cost. Phase 14 is IN PROGRESS.

## Why now

Brian authorized 14A on 2026-10-02 after Phase 13 closed. Phase 13 remains CLOSED.

## In scope

One OpenAI adapter and pinned `gpt-4.1-mini-2025-04-14`, 6–8 approved groups,
approximately 25 local catalog references, at most 10 total live attempts, strict
structured results, protected local files and conservative spending/replay control.

## Explicit non-goals

No valuation, schema migration, dashboard, queue, training, embeddings, automatic
model comparison, production access, market activation, deployment or Phase 15/16.

## Current repository state

Local main `d839e51b65f9156e5829740c08d52b59be4c4ec4`; accepted Phase 13 review
`535cb38da575741765986c71508888bee8b77e7f`. Preserve AGENTS.md and the two protected
catalog tests byte-for-byte and unstaged. Main remains uncommitted/unpushed.

## Decisions and assumptions

Implementation is authorized; spending, account policy and exact photos are pending
one combined Brian approval. Proposed cap: USD 0.25; reserve USD 0.02 for every
attempt, including failures/interruption. No automatic retries. Prices and provider
terms were checked against official documentation on 2026-10-02. Details and sources:
[provider decision](provider-privacy-cost.md).

## Data model and API/interface changes

New private CLI package `brickvault_api.recognition`; Pydantic output contract and
existing catalog Identity/SnapshotRef types. No HTTP contract or database changes.
The reference subset is an ephemeral projection of an accepted local catalog snapshot,
never a second catalog. Catalog names/images/labels are not sent to the model.

## Implementation sequence

1. Strict result/input contracts and bounded anonymous image copies.
2. Read-only local catalog projection and exact namespace/identifier resolution.
3. Single provider transport, durable attempt reservation and no silent replay.
4. Six focused fixture tests, changed-code lint/type checks, sanitized review package.
5. After combined approval and local credential setup, run the selected sample once.

## Validation and acceptance criteria

Six tests cover schema/refusal, exact/ambiguous resolution, honest unknown/mixed
results and metrics, spending/replay/interruption, redacted provider failure, and
privacy/input boundaries. No earlier-phase campaigns or frontend/Android builds.
Fixture evidence establishes behavior only, never recognition quality.

## Security, privacy and data integrity

Live defaults off. Bind approval to prepared image/text and catalog digests, model,
limits and account treatment. Strip metadata on copies; retain original bytes.
Operator must review visible personal content before approval. No folder scans,
URL fetching, model tools or revealing filenames/answer labels in model input.
Private model clues stay in protected output; public report contains counts only.
The approved Phase 13 image policy remains unchanged and grants no AI submission rights.

## Failure modes, rollback and recovery

Reserve before network dispatch; uncertain attempts keep the full charge reservation.
No automatic retry/fallback; rerun skips completed groups and blocks uncertain work.
Corrupt or missing initialized ledger fails closed. Stop for manual reconciliation
after interruption; never erase/reinitialize the ledger to recover budget.
Rollback is removal of this uncommitted module; retain private ledger evidence.

## Progress log

- [x] 2026-10-02: scope, baseline, protected hashes and official documentation checked.
- [x] 2026-10-02: combined provider/budget/photo/account approval requested.
- [x] 2026-10-02: implementation complete; six fixtures passed in 2.96 seconds;
  two affected checks passed in 1.04 seconds after report integrity/type fixes.
  Changed-code Ruff lint/format and mypy pass (six Python files).
- [ ] Approved one-time live sample (currently zero calls; no photos selected).
- [x] 2026-10-02: sanitized r1 package assembled for astra-response; publication
  commit and pinned review link are reported in the conversation receipt.

## Open questions or manual checks

Brian selects exact rights-cleared photos, independently confirmed labels and relevant
catalog alternatives; approves cap and account handling; enters a key locally.
Account entitlement cannot be established from public model documentation.

## Outcome and follow-up

Local implementation and focused checks pass. Live attempts/spend are zero; exact
photos, reference subset, account handling and credential setup await the combined
Brian decision. Stop at this gate and resume in this conversation. Wider Phase 14 still requires
direct recognition versus retrieval alone versus retrieval plus verification; no
embedding/vector infrastructure is authorized by 14A.
