<!-- Review copy: repository-relative links rendered as source references. Exact source bytes are hash-pinned in changed-inventory.json. -->
# ExecPlan 110 — Phase 16B reviewed labels and sanitized dataset foundation

**2026-10-23 — READY FOR PHASE 16B PLAN REVIEW. Planning only; uncommitted.**

**2026-10-26 — Grouped decisions approved; fixture-only source/TEST implementation authorized.**
Reviewed bytes preserved privately at `.local/phase16b/reviewed-plan-110.md`, SHA-256
`86d5341c82e499f810815f924cb5ff627bcc884efdac3396b598ee6e1d876123`.
Binding clarifications: preview/release bind explicit bounded owned targets and
purpose into the digest; bridge metadata is allowed but only selected image bytes
are prepared/exported. Encoding/copying stays outside locks; final publication
rechecks ownership, eligibility, permissions/expiry and withdrawal under the shared
principal lock. Releases reproduce independently; no safe-combination claim.
Component growth and shared-derivative links also withdraw affected releases.
Production smoke-root registration and real-source export remain unauthorized.

## 1. Goal and user-visible outcome

One CLI-first vertical slice lets Brian explicitly review image identities, privacy
and rights, then preview and materialize a reproducible private dataset release.
Prove the entire path with generated synthetic images; this does not establish a
real training-ready corpus. No custom training or new recognition calls.

## 2. Why now; delivered versus remaining Phase 16

Plan 109's final closeout (repository reference: `docs/plans/109-phase-16a-actual-outcomes.md#production-deployment-local-closeout---2026-10-22`)
and [accepted publication](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/a79a7de14b0bbccbecfb2a9e8038f17b28cc2c3e/astra_response/Phase-16/16A-production/r4/REVIEW.md)
close 16A source AND production. Delivered: owner-scoped append-only actuals,
exact-money results, immutable original-forecast comparison with per-metric
comparability, correction/history UI and operational schema compatibility.
Production identity remains `phase16a-outcomes-production-r3`, schema
`0018_deal_outcome_revisions`; no fresh operational verification is claimed.

Remaining under Prompt 16 (repository reference: `prompts/16_training_dataset_and_hardening.md`):
reviewed labels/negatives, privacy/rights admission, sanitized reproducible releases,
connected splits, and affected image/security/recovery regression evidence. 16A's
per-deal comparison is delivered; cross-deal forecast-error/cohort reporting,
normalized verified-contents inventory and broader recognition-quality/hardening
remain outstanding. They are not silently satisfied by this foundation. Older
workflow/roadmap status and pending capture edits are historical, not authority to
reopen 16A. Wider Phase 16 remains OPEN.

## 3. In scope

One additive migration, five small dataset tables, a private authenticated local
CLI, deterministic selection/splitting/materialization, and directly affected
compatibility checks. Real-source records default ineligible. Fixture releases
use a distinct purpose that cannot be promoted to a real training release.

## 4. Explicit non-goals

No React/Android UI, HTTP API, generated contracts, new dependencies, image-upload
protocol changes, automatic label imports, embeddings, vectors, training, new AI
calls, acquisition or source fetching. No cross-deal financial report, new valuation
math, automatic live deletion or general consent platform. 15B stays stopped and
unqualified; 15C stays unstarted. No deployment or real-corpus export is authorized.

## 5. Current state and reusable implementation

Local `main` is `e76d5f18f810c5942d6c1c8692c261015229c802`, unpushed; index empty.
All 22 pre-existing pending paths are preserved, including AGENTS.md, both protected
catalog tests and stopped capture code. 109 is the highest existing plan; 110 was
unused. The requested `astra_response/Phase-16/16B-plan/r1/` was unused locally and
in the inspected local publication refs. No server, device or private corpus read.

| Existing implementation | Reuse and limit |
| --- | --- |
| `listings/service.py`, migration `0017_listing_images` | Owned listings, listing_image IDs, original asset/blob SHA-256, thumbnail lineage, immutable receipts and deterministic order. No existing dataset tables. |
| `images/processing.py`, `images/storage.py` | Bounded real decode and atomic immutable BlobStore publication/read/stat. Do not change original bytes or thumbnail recipe. |
| `recognition/local.py: sanitized_image`, private-file/ACL helpers | Existing metadata-free RGB JPEG recipe and filesystem checks; extract provider-independent helpers without importing pilot execution. Metadata stripping does not remove private pixels. |
| `recognition/contracts.py`, `recognition/evaluation.py` | Distinction between proposals, independently confirmed labels and exhaustive labels; existing private pilot files are not durable dataset reviews or training permission. No automatic import. |
| `outcomes.py`, `auth.py`, `catalog/connection.py` | Ownership guard, authenticated transaction, principal serialization, append/replay/conflict patterns. Financial actuals never become labels. |
| `backup_format.py`, `image_backup.py`, operational scripts | Existing four-artifact image-inclusive recovery contract and dynamic inventory; extend exact supported heads, never accept arbitrary future schemas. |

Paths in this table are relative to `services/api/src/brickvault_api/` unless stated.
Conceptual analysis/capture/confirmation tables in older docs are not evidence that
those tables exist. The current image_relation permits only thumbnail-v1; dataset
crop lineage belongs in the new review/item records, not a silent widening of it.

## 6. Decisions and assumptions — one grouped approval

Recommend approving together: **(a)** CLI-first local workflow and the bounded
0019 migration; **(b)** conservative unknown/fixture/source-rights rules and explicit
reviewed negative pairs; **(c)** private immutable release retention plus append-only
withdrawal, with no automatic deletion or redistribution. Retain released sanitized
bytes/manifests privately until separately authorized disposal; corrections withdraw
use immediately but do not rewrite history. Existing encrypted backup/pin rules
remain; pinned copies are not promised to expire.

This grouped approval would authorize fixture-only implementation and isolated TEST
checks, not production operations, a real corpus, real export or training. Actual
real-corpus source/export/training permissions and any incompatible retention terms
must be reviewed together later; no approval marathon for routine coding decisions.

## 7. Data model and interface changes

Propose `0019_reviewed_dataset_foundation` after 0018, with normal Alembic version
and paired up/down SQL files. No existing outcome, forecast, receipt or image row
is rewritten. Five tables, UUID IDs, owner FK, server UTC times, bounded strict
payloads (64 KiB/review), no PUBLIC privileges:

| Table | Exact responsibility |
| --- | --- |
| `dataset_subject_revision` | Full-state append-only classification of exactly one owned listing OR saved original forecast root (exclusive nullable FKs). Fields: submission id, owner, subject FK, revision, expected predecessor, `UNKNOWN/REAL/SYNTHETIC/EXCLUDED`, reason/evidence reference, and listing-only declared source-group UUIDs (max 32) plus `related_sources_reviewed` attestation. Unique subject/revision; reason required for correction. Shared original hashes inherit the strictest exclusion. Group assertions remain conservative historical edges. |
| `dataset_review_revision` | Append-only full review of an owned listing_image: submission id, revision/predecessor, original hash, optional proposed identities with private evidence digest, independent positive labels and explicit negative pairs, Brian reviewer/time/basis, privacy review, source/export/training permission decisions and evidence references, prepared derivative blob FK/hash/recipe. Missing states are UNKNOWN; reason required on correction. |
| `dataset_release` | Immutable release UUID/owner/purpose, seed, algorithm/recipe/schema/tool versions, pinned selection and graph snapshot, canonical sanitized manifest JSON/hash, private lineage/selection JSON/hash, submission request hash. No mutable status column. |
| `dataset_item` | Immutable release membership: release/item IDs, exact review and subject revision FKs, derivative blob FK/hash, opaque group and partition, independent label keys/negative pairs, crop/transform lineage. Unique release/listing_image and same-owner enforced across all references. |
| `dataset_release_event` | Append-only release withdrawal (reason code, cause review/classification ID, server time); effective usability is derived. Corrections/revocations atomically withdraw every affected release. No destructive rewrite or automatic reactivation. |

Use typed Pydantic models in `datasets/models.py`, not unconstrained JSON. DB checks,
FKs and guards enforce same-owner membership, append ordering, immutable rows and
fresh authenticated write context. Use existing principal-lock order consistently
for review, classification, release finalization and withdrawal. Submission UUID
plus equal normalized content replays the original result; changed content conflicts;
stale expected revision conflicts. No process-local lock as database authority.

**Independent admission dimensions.** Each positive is `UNREVIEWED`,
`BRIAN_CONFIRMED`, `PURCHASE_VERIFIED` or `WITHDRAWN`, with image-specific scope,
quantity when actually known, evidence basis and reviewer. Purchase verification
requires explicit inspection evidence; BOUGHT/CONFIRMED_MATCH in outcome actuals
does not suffice. Partial labels remain partial, never exhaustive by implication.
Negatives require an explicit `CONFIRMED_NOT_THIS_IDENTITY` decision for this
image/selected region, identity and reason. Rejection, omission, low score, unknown
contents or a positive for another identity supplies no automatic negative.

Privacy is `UNREVIEWED/APPROVED/REJECTED` for the exact sanitized-byte hash and
recipe. Rights record separate `UNKNOWN/PERMITTED/DENIED/REVOKED` source-use,
export and training decisions, with provenance, evidence reference, scope and
optional expiry; private display/download/API-submission permission never fills
them. Eligibility is computed, never an operator-editable training_ready flag.
Require applicable positive/negative review, all permissions, approved final pixels,
known real classification and no conflicting shared-source prohibition. Rebrickable
images AND downloaded catalog content remain excluded, including derivative data.
Private canonical identity links can use the existing catalog; exported label keys
and label evidence must be independently authored/permitted. Do not copy catalog
names, descriptions, inventories or provider payloads into training material.

**Fixture exclusion.** Absent subject revision means UNKNOWN/ineligible for real
analytics/selection, not REAL. Add a shared classification predicate for future
analytics and this exporter; there is no analytics job in this slice. Fixture mode
accepts only explicit SYNTHETIC subjects, emits `FIXTURE_ONLY_NOT_TRAINING_DATA`,
and never mixes real rows. Keep the retained 16A smoke root immutable. Its exact
UUID must later be resolved from the accepted private receipt by authorized Brian
and entered through `subject-review`; never discover it through note-text matching
alone. No production backfill now. Real analytics/export remains blocked until that
durable classification and real-corpus admission are complete. Synthetic status
cannot be cleared by an ordinary review; correcting it needs explicit owner guidance.

**CLI, no API/UI changes.** Add `datasets/{__init__,__main__,models,service,export}.py`
and provider-independent `images/sanitization.py`. Proposed invocation:
`uv run --project services/api python -m brickvault_api.datasets <command>`.
Commands: `subject-review --input`, `prepare --input`, `review --input`,
`preview --purpose --seed`, `release --preview-id --id`,
`materialize --release-id --output`, `verify --release-id --output`, and
`withdraw --release-id --reason-code`. A `status --submission-id` read recovers
uncertain writes and their exact committed results. Input documents carry submission UUID,
expected revision and explicit targets; bounded strict parsing, no arbitrary SQL,
source URLs, credential arguments or arbitrary corpus traversal. `preview` is
read-only and returns its canonical selection digest as preview-id, not another table.

Use guarded configured runtime DB/BlobStore only, with interactive `getpass` and
existing AuthService login/check/session lifecycle; tokens stay in memory and are
revoked on exit. No owner-role bypass, new authentication system or server endpoint.
Brian's minimum flow: classify a listing, prepare a crop, inspect the private local
preview, submit independent identity/privacy/rights decisions, inspect eligibility
counts/reasons, then explicitly release/materialize/verify. All commands fail closed
on unavailable DB, ownership/auth failure or unknown scope. New sessions do not
silently retry uncertain writes: reread the submission UUID before deliberate retry.

## 8. Selection, sanitization and reproducibility contract

Prepare only from committed owned originals through BlobStore. Fully decode with
existing limits, orient, optionally crop by explicit integer bounds in oriented
coordinates, fit within 1024 square, RGB/white, JPEG quality 85, strip metadata.
Record `dataset-sanitize-v1`, crop, Pillow version and output hash. Brian must inspect
the final pixels for seller faces/names, addresses, notifications and unrelated text;
reject unsafe images that a crop cannot safely isolate. No OCR/redaction model or
automatic approval. Store derivative bytes as a new existing blob row; review/item
FKs preserve original-to-derivative lineage without changing image_asset kinds.
Preparing or correcting bytes invalidates the prior privacy approval.

Build an undirected graph over ALL owned listings, original hashes, known derivative
lineage and declared source-group edges, including ineligible/excluded bridge nodes.
Connected components include transitive A–B–C relationships. Links using the same
sanitized output hash also connect. Same listing, shared exact original and declared
related source/capture groups can never cross splits. No URL fetch or seller-identity
inference. Brian must attest source-group completeness for a real admitted corpus;
unknown relatedness blocks admission. No claim of perceptual-duplicate detection.

Pin a sorted graph snapshot, all eligibility revision IDs and selected items in one
coordinated selection. Require an explicit bounded manifest of owned listing_image
targets and purpose; never implicitly select every eligible record.
Component ID is a hash of canonical sorted internal
node keys; SHA-256 of version/seed/component ID assigns integer buckets 0–7999 train,
8000–8999 validation, 9000–9999 test. Seed is an explicit unsigned 64-bit decimal;
use canonical UTF-8 JSON and SHA-256, never Python hash/random iteration order.
Small fixtures may yield empty partitions; never split a component to fill quotas.

At finalization recheck auth, latest reviews/permissions/expiry and graph digest
under the principal lock; stale preview conflicts. Serialize listing upload commit
and privacy escalation with this same short lock (before listing row lock), so new
shared content cannot race finalization. On graph/privacy change withdraw releases
whose pinned components/admission are invalidated. Keep decode outside locks.
Derivative preparation/review uses this lock too; adding equal sanitized hashes
must invalidate any prior conflicting partition assignments.
Across releases, a newly merged component spanning prior partitions withdraws the
affected releases; never silently present combined releases as leakage-free.

Immutable manifest contains purpose, versions, seed, selection/split rules, opaque
item/group IDs, independent labels, partitions, dimensions and derivative hashes.
The private DB lineage snapshot retains original hashes, receipt/listing_image and
review references; the materialized export excludes original hashes, private input
filenames, source URLs, seller/listing text, financial actuals and raw provider data.
Payload names are opaque hashes. Canonical manifest and sorted file checksum list
are identical when replaying the same pinned release; wall clock and machine paths
are excluded from hashed content. Historical reproduction never reselects latest data.

Materialize into a fresh private directory outside Git/static roots; restrictive
ACLs, no symlink traversal or overwrite. Stage and fsync complete files, verify all
hashes, recheck release eligibility then atomically publish the directory. Interrupted
release/materialization recovers by submission/release ID; existing blobs are verified,
not overwritten. No archive reader or new testing framework. Withdrawn releases fail
materialize/verify-for-use; private audit metadata remains readable. Already copied
bytes cannot be recalled: mark unusable, report affected release IDs, and require a
new release after correction. Retention/deletion conflicts block use pending guidance.

## 9. Migration and operational compatibility

Implement compatibility in this slice, before readiness claims: update
`persistence/runtime_grants.py` with enumerated SELECT/INSERT only on the five
tables and reviewed guard functions; no UPDATE/DELETE. Update
`scripts/package_api.py` wheel/sdist inclusion and literal migration graph/head;
`scripts/release_manifest.py` source inventory; `backup_format.py` exact head
allowlist; `production_backup.py`, `image_backup.py`,
`scripts/complete_run_retention.py` and `scripts/production_health.py` consumers.
Inspect `production_admin.py`/schema ownership guards for literal assumptions too.
Keep accepted 0016 legacy and 0017/0018 recovery admission unchanged; unknown and
multiple heads still fail. Do not change the 53-table catalog inventory count.

Recommend retaining backup schema 3 and its four artifacts: full database.dump
already carries new rows and image-blobs.tar carries derivative blobs. Manifest
bytes are DB-backed; materialized directories are disposable, reconstructible and
not a fifth backup artifact. Extend inventory fingerprints for all five tables,
including review/rights/withdrawal contents, not just counts. Verify restore can
reconstruct the exact release and its withdrawn state. New live head requires its
matching package/grants/health version; old runtime compatibility is not presumed.
Existing backup retention, encryption and permanent pins remain unchanged.

## 10. Implementation sequence after approval

1. Add schema/models/classification and review service with real disposable
   PostgreSQL admission, conflicts and replay; generated synthetic fixtures only.
2. Add crop preparation, explicit review CLI, graph selector and immutable release
   materialization; connect upload/privacy finalization locking without changing
   receipt/order semantics. No prediction promotion or imported real corpus.
3. Finish operational compatibility and one affected acceptance pass; record exact
   evidence and remaining real-data/production gates. One review stop for the slice.

## 11. Targeted validation and acceptance criteria

No checks below run during planning. Later use existing pytest infrastructure:

- New `test_dataset_admission.py` and real-PostgreSQL `test_datasets.py`: independent
  identity/privacy/rights gates, partial labels, explicit negatives, Rebrickable and
  unknown/expired/revoked permissions, same-owner guards, revision/idempotency races,
  sticky fixture/root exclusion and fixture/real mode separation.
- New `test_dataset_export.py`: metadata/private-pixel fixture crop review, strict
  input bounds, stable bytes/hash/seed, A–B–C ineligible bridge and duplicate-derived
  leakage, changed group withdrawal, review/revocation-finalization barriers,
  interrupted publication and zero raw text/URLs/financial/provider metadata output.
- Focus existing `test_listing_images.py`, `test_listing_share_privacy.py` and
  `test_listing_upload_arguments.py` on changed lock/privacy and real decoder paths:
  duplicate/lost-response receipt recovery, order/minimum/high-water, malformed
  multipart/decode/size rejection. Reuse unchanged accepted parser evidence; do not
  edit or rerun protected catalog tests merely for this slice.
- Extend `test_outcome_backup_compatibility.py`/`test_image_backup_seams.py` and
  relevant packaging/health/retention cases for 0019 versus accepted old heads.
  One disposable DB+blob round-trip containing reviews, fixture classification,
  active/withdrawn release and receipts/order proves exact re-materialization and
  grants/inventory. No full production disaster-recovery rehearsal.
- Focus Ruff/mypy on changed Python, and one affected wheel/package check. No web
  or Android build, physical-device campaign, provider call or blanket TEST replay.

## 12. Security, failure modes, rollback and recovery

Follow image policy (repository reference: `docs/IMAGE_PRIVACY_POLICY.md`),
ingestion (repository reference: `docs/IMAGE_INGESTION.md`), privacy (repository reference: `docs/SECURITY_PRIVACY.md`), and
provider prohibition (repository reference: `docs/PHASE_2D_PROVIDER_GATE.md`). Fixed error codes/counts only
in ordinary logs. Raw review evidence references remain private, not export payload.
Missing/corrupt blobs fail closed; published unreferenced derivative blobs are
preserved for report-only audit/retry. No automated orphan purge.
Corrections, classification changes and revocations append history and withdraw
affected releases atomically. No forecast/outcome rewrite. After live use, recover
forward; downgrade/drop tests are disposable-only. Deployment, backup operations,
private receipt access and production fixture registration require separate scope.

## 13. Progress and open checks

- [x] 2026-10-23: Read accepted closeout, current implementation and relevant policy;
  drafted one plan. No tests/builds, dependencies, services or exports.
- [x] 2026-10-26: Brian approved grouped decisions and fixture-only implementation,
  with explicit bounded selection, short final-publication coordination and standalone
  release clarifications recorded above. No second plan-review cycle.
- [x] 2026-10-26: Five tables and authenticated CLI implemented. Affected validation
  passes; no physical-device check needed. Source/TEST implementation awaits review.
- [x] 2026-11-01: R1 review identified two in-scope defects. Exact blob hashes now
  connect original, dataset-derivative and thumbnail roles; shared-source checks
  retain the latest explicit permission/provenance review across preparations.
  No new planning round, schema change, pinned-manifest rewrite or production action.
- [ ] Later, separately: independently permitted real corpus and exact retained
  smoke-root classification. No IDs/private evidence copied into this publication.

## 14. Outcome and stop condition

Planning ends at this reviewable uncommitted plan/package. Implementation completes
only when synthetic reviews/releases reproduce exactly, admission and transitive
split failures are proved, withdrawal and fixture exclusions persist, and 0019
package/grants/backup/inventory/retention/health compatibility passes affected checks.
Report FIXTURE-ONLY evidence and stop for review. Real readiness, deployment,
training, capture and wider Phase 16 completion are not conferred.

### Fixture-only implementation outcome — 2026-10-26

Implemented `datasets/{models,service,export,__main__}.py`, shared bounded
`images/sanitization.py`, migration 0019, enumerated runtime grants, and five-table
inventory fingerprints. Exact schema admission is centralized in `backup_format.py`;
existing health, backup and retention consumers inherit the reviewed 0019 head while
retaining old-head validation. Wheel/sdist and release source inventories include
the new source/migration/tests. No dependency, router, contract or screen changes.

Actual CLI: `python -m brickvault_api.datasets` in the repository-managed uv/venv.
It accepts configured owned TEST runtime settings only, prompts through getpass,
uses existing AuthService, and revokes its session on exit. JSON inputs are strict,
private and at most 64 KiB. Workflow: `subject-review --input`,
`prepare --input --output` (private selected-image preview), `review --input`,
`preview --input` (explicit purpose/targets/seed), `release --input` (same selection
plus preview digest/submission ID), `materialize --release-id --output`,
`verify --release-id --output`, `withdraw --input`, and `status --submission-id`.
Status separates the immutable result from current release usability. The CLI has
no production mode and no real-training purpose.

All decoding/copying occurs before final publication coordination. Persistent
private exact-release reservation markers use kernel locks that release on process
exit; atomic per-file publication and exact byte checks recover interrupted writes
without overwriting originals or mixing releases. Relevant uploads/privacy changes,
subject/review corrections and newly shared crop derivatives invalidate affected
component snapshots. Independent releases remain unsupported for combining.

Validation: 65 affected unit/operational cases passed. Nine release-manifest cases
were rerun after adding affected test paths to its inventory and passed. The final
PostgreSQL pass had 39 passing cases and one stale historical test assertion that
still expected 0017; updating that assertion to the reviewed 0019 head and rerunning
only that case passed. Thus all 40 selected integration cases have passing evidence,
including the full authenticated CLI flow, expiry/revocation/publication barriers,
new shared-crop growth and one real disposable pg_dump/restore plus blob archive
round-trip retaining active/withdrawn releases and exact fingerprints/outputs.
The CLI entry point runs in-process in the harness with generated TEST settings
and password-prompt input; authentication, parsing, database and blob operations
are real. This is source/TEST evidence, not a deployed interactive-terminal claim.
All runner ledgers report no leftovers and preserve volumes/prior running state.

Focused Ruff formatting/lint and mypy checks passed (Windows source and Linux
types for Linux operational image-backup code). API wheel/sdist, isolated installed
imports, exact migration graph and credential-free schema check passed. Windows
ACL creation was corrected to use access-only .NET control sections rather than
requesting unavailable SACL privileges. Existing pytest/Starlette warnings remain;
no dependency expansion follows from those warnings. No full historical suite,
web/APK build, production recovery, phone/server or provider activity occurred.

Limitations: fixture-only, generated images, Windows filesystem/ACL execution and
real PostgreSQL in owned local Docker TEST. Linux materialization filesystem runtime
is unqualified. No private corpus or real permissions are admitted, no 16A smoke
root is backfilled, and real analytics/export/training readiness is not claimed.
16A stays closed, capture stays stopped, wider Phase 16 remains open. Main source,
migration, tests and this plan remain uncommitted; only the sanitized review package
may be committed/pushed on astra-response under the explicit publication exception.

### R2 targeted source-review corrections — 2026-11-01

R1 and its evidence remain immutable history. Its separate original/derived hash
nodes missed cross-role exact-byte links; its latest-row lookup let preparation
hide an explicit shared-source prohibition. The corrected graph uses `blob:<sha256>`
for every byte role while retaining semantic lineage privately. Uploading a known
derivative as an original now immediately grows the component and appends withdrawal
for an affected pinned release, before the new image is classified or prepared.
Historical source-group and derivative edges and excluded bridges remain intact.

Exact-byte admission still requires the latest derivative review. Separately, shared
original checks consult the latest non-null explicit review for source/export/training
denials or revocations and prohibited source/label provenance. Any number of new
preparations leaves those prohibitions effective; only an explicit evidence-backed
review can correct them. Such a correction cannot reactivate a withdrawn release.
No permissions or pixel approval are copied onto a newly prepared derivative.

Targeted verification passed: 15 PostgreSQL cases (two cross-role reuploads, eight
shared-prohibition cases, five affected regressions), one deterministic graph unit,
Ruff on both changed Python files and mypy on the service. The fresh wheel/sdist
passed isolated installed import, migration graph and credential-free schema checks;
both archives contain the exact corrected service bytes. Owned TEST cleanup reports
no leftovers and restores prior running state. Details are in the R2 review package.
Unchanged R1 auth, schema, receipt/order and disposable DB/blob
recovery evidence is reused, not rerun or represented as a new recovery campaign.
Source, tests and this plan remain uncommitted; only sanitized R2 review artifacts
may be published. Stop for review; fixture, real-data and production limits remain.
