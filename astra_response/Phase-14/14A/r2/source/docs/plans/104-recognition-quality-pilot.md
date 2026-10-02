# Plan 104 — Phase 14A recognition pilot

## Goal and user-visible outcome

One local Python CLI accepts operator-selected photos and optional sanitized text,
returns uncertain set/minifigure candidates, resolves exact shared catalog identities,
and reports preliminary quality, latency and estimated cost. Phase 14 is IN PROGRESS.

## Why now

Brian authorized 14A on 2026-10-02 after Phase 13 closed. Phase 13 remains CLOSED.

## In scope

One OpenAI adapter and exact `gpt-6-luna`, 6–8 approved groups,
up to 30 retained local catalog references (three verified for this run), at most 10 total live attempts, strict
structured results, protected local files and conservative spending/replay control.

## Explicit non-goals

No valuation, schema migration, dashboard, queue, training, embeddings, automatic
model comparison, production access, market activation, deployment or Phase 15/16.

## Current repository state

Local main `d839e51b65f9156e5829740c08d52b59be4c4ec4`; accepted Phase 13 review
`535cb38da575741765986c71508888bee8b77e7f`. Preserve AGENTS.md and the two protected
catalog tests byte-for-byte and unstaged. Main remains uncommitted/unpushed.

## Decisions and assumptions

Brian's amended approval raises the lifetime cap to USD 10.00, preserves ten total
attempts and exact `gpt-6-luna`, and authorizes a model-wide maximum-input reservation
without token counting. The per-request bound is USD 0.232036 using 922,000 maximum
input tokens and the approved 2,048 total output tokens at worst applicable rates.
Sharing remains disabled; exact prepared sample approval is frozen. Raw recognition
and catalog resolution are distinct. Three exact retained set references are used;
fourteen confirmed BrickLink figure labels remain canonically unresolved. No fallback,
retry, mapping write, reimport or database startup occurred in the live run.
See the [provider decision](../PHASE_14A_PROVIDER_DECISION.md).

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
No automatic retry/fallback; rerun validates and reuses completed results and blocks uncertain work.
Corrupt or missing initialized ledger fails closed. Stop for manual reconciliation
after interruption; never erase/reinitialize the ledger to recover budget.
Rollback is removal of this uncommitted module; retain private ledger evidence.

## Progress log

- [x] 2026-10-02: scope, baseline, protected hashes and official documentation checked.
- [x] 2026-10-02: combined provider/budget/photo/account approval requested.
- [x] 2026-10-02: implementation complete; six fixtures passed in 2.96 seconds;
  two affected checks passed in 1.04 seconds after report integrity/type fixes.
  Changed-code Ruff lint/format and mypy pass (six Python files).
- [x] 2026-10-02 continuation: received conditional model/budget approval; migrated
  the same adapter to Responses, explicit static-prefix caching, full result reuse
  validation and cache/reasoning accounting. Seven affected fixture tests passed
  in 3.80 seconds; strict mypy six files and Ruff passed. No live proof inferred.
- [x] API sharing verified disabled, local key file present, seven groups/13 images
  prepared; original hashes unchanged. Final sample review is pending.
- [x] Schema v2 admits G06's eight exact identities and up to twelve visible objects;
  three affected tests passed in 3.16 seconds, plus Ruff and strict mypy. Output cap
  remains 2,048 tokens; truncation is a retained failed attempt, never retried.
- [x] Final exact sample and project/model metadata approved; amended USD 10.00 cap
  admits the model-wide maximum-input reservation without counting submissions.
- [x] One-time sample run stopped at G06: six requests, five completed; G07 unattempted.
- [x] 2026-10-02: sanitized r1 package assembled for astra-response; publication
  commit and pinned review link are reported in the conversation receipt.

## Open questions or manual checks

Review the partial results. Manual G06 continuation requires explicit approval for
a revised output/reasoning allowance and retry, keeping the failed attempt counted.
G07 must remain unattempted until that decision. No further request is authorized
by this completed one-run execution. Crosswalk acquisition/mapping writes and wider
Phase 14 comparisons require separate scope decisions.

## Outcome and follow-up

Six live requests/eleven image inputs; five completed groups, one incomplete G06,
one unattempted G07. Raw top-1/top-3 agreement 3/17; three expected sets resolve,
fourteen figure labels do not. Reported usage 9,118 input and 5,388 output (including
4,403 reasoning) tokens; estimated USD 0.0036058, actual billing unavailable. Retained
reservations USD 1.392216. No retries, counting submissions or result reuses.

Six affected fixtures passed in 3.42 seconds and one final redaction/transport check
in 0.69 seconds, plus a synthetic-ID fixture recheck in 0.81 seconds; Ruff and strict mypy passed. Main unpushed, empty index, protected
hashes/sample unchanged, recovery retained, development stopped. Sanitized r2 review
publication follows this run; see the [existing pilot report](../PHASE_14A_PILOT.md).
Wider Phase 14 direct/retrieval comparisons remain unqualified.

## Earlier preflight record (superseded status)

The following keeps the prior blocked-state history; the outcome above is current.

## Approved sample and preflight result

Brian explicitly approved the seven prepared groups/13 photos and listing texts,
conditional on the remaining checks. The private sample approval binds prepared.json
and the review document by SHA-256. A project-scoped model metadata GET succeeded:
`gpt-6-luna` is visible to the supplied key. This is not image/schema inference proof.
No photos or inference prompt were sent; attempts/spend/reuses remain zero.

The owned loopback development database at 127.0.0.1:55432 was stopped. It was started
for read-only diagnosis and restored to stopped. Ownership matched. Its installed
revision is `0012_product_identity_qualifiers`; this checkout requires
`0017_listing_images`. The catalog guard correctly refuses access. Applying existing
migrations 0013 through 0017 would change the development schema and is pending
Brian's authorization; no migration, catalog import or production access occurred.
The model-specific image-token billing bound remains unverified after a focused
refresh of official documentation; no fallback or cost-gate bypass is enabled.


### Authorized catch-up result — 2026-10-02

Brian separately authorized existing development migrations 0013–0017. One protected
recovery copy was verified, the chain/runtime grants passed, and existing catalog
and saved context checks matched. Development is stopped. No new migration exists.
The three confirmed sets resolve; fourteen BrickLink minifigure IDs lack catalog
mappings. Image-cost/counting admission remains blocked, with zero photo-counting
submissions and zero inference. See the [existing pilot report](../PHASE_14A_PILOT.md)
for the brief migration and independent cost-admission evidence.
