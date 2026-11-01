# Phase 16B corrected fixture-only implementation review — r2

**READY FOR PHASE 16B CORRECTED FIXTURE-ONLY IMPLEMENTATION REVIEW — 2026-11-01.**

Both R1 source-review findings are corrected within approved Plan 110. Application
changes since R1 are limited to `datasets/service.py`, `test_datasets.py` and the
plan progress/outcome. No new migration, dependency, API, UI or consent framework.
Application source, migration, tests and plan remain uncommitted on local main
`e76d5f18f810c5942d6c1c8692c261015229c802`; its index is empty and main is unpushed.

## Findings and disposition

**1. Exact bytes across original/derivative roles — corrected.** The graph now
uses `blob:<sha256>` for originals, prepared dataset derivatives and thumbnail
lineage. Historical source-group/derivative edges and ineligible bridges remain.
A known derivative uploaded as another listing's original immediately grows the
component and appends withdrawal for the affected older release, before the new
image is classified or prepared. Semantic provenance stays in private lineage;
pinned release data is never rewritten. No perceptual matching or release combining.

The regression covers both dataset derivatives and thumbnails. Patterned synthetic
pixels ensure the reupload's automatic thumbnail differs from A's derivative;
B's later crop also differs. Both selected items share a component/partition, and
the old release remains byte-for-byte unchanged in its stored result and withdrawn.
Both role variants failed against R1 due to the missing immediate withdrawal event.

**2. Preparation clearing shared-source prohibitions — corrected.** Exact-byte
admission still uses the latest row and requires review of a newly prepared crop.
A separate lookup supplies the latest explicit non-null review for shared-original
source/provenance checks. Preparation cannot hide source-use/export/training denial
or revocation, or prohibited Rebrickable source/label provenance. No old permission
or pixel approval is assigned to the new crop. Only an explicit evidence-backed
review can correct the effective state; withdrawn releases never reactivate.

Eight cases cover DENIED and REVOKED for all three permissions plus both prohibited
provenance fields. Two successive preparations leave the approved sibling blocked,
release creation refused and prior withdrawal intact. The new crop remains
REVIEW_REQUIRED. Explicit reviewed correction permits a new release without
rewriting or reactivating the old one. The source-provenance case reproduced the
R1 defect before the correction.

## Actual bounded validation

[Focused validation and artifact hashes](focused-validation.json):

- **15 PostgreSQL cases passed:** ten new parameterized cases above, plus transitive
  excluded bridges/component growth, shared-original privacy escalation, equal-crop
  growth, permission expiry/correction, and withdrawal before final publication.
- **One graph unit passed:** deterministic components/partitions with a transitive
  excluded bridge and reversed edge order.
- **Ruff format/lint passed** for both changed Python files; **mypy passed** for the
  service. Existing pytest assert-rewrite warning remains.
- **Fresh API wheel/sdist passed:** isolated installed import, exact migration graph
  and credential-free schema. Both archive copies of the corrected service match
  its final source SHA-256; wheel/sdist hashes are recorded in the validation file.
- Owned disposable TEST cleanup reports no leftovers, preserves volumes and restores
  prior running state. Synthetic images, real auth/PostgreSQL/BlobStore/filesystem;
  no production or real-corpus evidence.

Unchanged auth/CLI parsing, migration/grants, upload receipt/order/parser, operational
compatibility and disposable DB/blob round-trip evidence are explicitly reused from
[R1 validation at 29e33cb7](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/29e33cb7fbc472439915c981f50df297943a99db/astra_response/Phase-16/16B/r1/focused-validation.json).
Its 65/40-case evidence is historical, not a new run. No broad replay or new recovery
campaign. R2 supersedes the affected grouping/shared-admission proof and has its own
fresh package evidence. Raw session-bearing logs and image datasets stay private.

## Review artifacts, preservation and remaining limits

[Small R1-to-R2 correction diff](r1-to-r2.patch), [cumulative patch against accepted
main](cumulative.patch), [exact final 22-path inventory/hashes](changed-inventory.json),
[updated plan copy](PLAN-110.md), and [preservation receipt](preservation.json).
The plan copy renders repository links as source references; exact source bytes
are pinned in the inventory and cumulative patch.

All 22 pre-existing pending/protected paths, both local planning-package files and
all six R1 package files remain byte-identical. Nineteen implementation paths are
unchanged from R1. Stopped 15B work is untouched. Only this seven-file sanitized R2
package is authorized for the astra-response commit/push; no application commit.
No independently delegated review is claimed.

Purpose remains `FIXTURE_ONLY_NOT_TRAINING_DATA`, with TEST-only execution. Real
source/rights admission, retained production smoke-root classification, real
analytics/export/training readiness and Linux materialization runtime qualification
remain outstanding. No production access, deployment, fixture registration, provider
or model calls, real acquisition, capture, financial expansion, web/APK build or
phone check occurred. Standalone releases cannot be assumed safe to combine.

Stop for review. Phase 16B is not closed; wider Phase 16 remains open.
