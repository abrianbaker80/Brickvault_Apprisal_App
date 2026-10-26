# Phase 16B fixture-only implementation review — r1

**READY FOR PHASE 16B FIXTURE-ONLY IMPLEMENTATION REVIEW — 2026-10-26.**

Source/TEST implementation of approved [Plan 110](PLAN-110.md), including all three
owner clarifications. Application source, migration, tests and repository Plan 110
remain uncommitted on local main `e76d5f18f810c5942d6c1c8692c261015229c802`.
Only this sanitized review package is authorized for publication on astra-response.
16A source/production remain ACCEPTED / CLOSED; wider Phase 16 remains OPEN.

## Working vertical slice

`python -m brickvault_api.datasets` uses configured owned TEST runtime settings,
interactive getpass and existing AuthService; it revokes its session on exit.
There is no production mode or real-training release purpose. No new dependency,
HTTP API, web/native screen or generated-contract change.

The minimum flow is classify a selected listing (`subject-review --input`), prepare
its private crop preview (`prepare --input --output`), independently review labels,
privacy and three permissions (`review --input`), inspect an explicit target/seed
selection (`preview --input`), and pin it (`release --input`). Then `materialize`
and `verify` use the exact release ID. `status --submission-id` recovers the immutable
result and reports current release usability; `withdraw --input` appends history.
Inputs are strict bounded JSON; previews/outputs are private and outside Git/static
roots. Fixture manifests say `FIXTURE_ONLY_NOT_TRAINING_DATA`.

Five new tables in `0019_reviewed_dataset_foundation` preserve subject/review
revisions, immutable releases/items and withdrawal events. Reuse listing_image,
original/blob/thumbnail/receipt lineage, real decoding, BlobStore, authentication
and append/replay patterns. New sanitized blobs retain explicit crop/recipe/hash
lineage without overwriting originals or widening existing image_asset kinds.

Identity confirmation, purchase-inspection evidence, privacy approval of exact
sanitized pixels, and source/export/training permission are independent. Guesses,
financial actuals, omitted candidates and bare rejections never become verified
labels or negatives. Explicit negative pairs are supported. Rebrickable content,
unknown/expired/revoked rights and unreviewed privacy block admission. Durable
UNKNOWN/REAL/SYNTHETIC/EXCLUDED classification excludes fixtures from future real
analytics; synthetic provenance cannot silently be changed to real.

The full metadata graph includes nonselected/ineligible bridges, exact originals,
derivatives and declared source groups. Only explicitly selected/admitted bytes
are prepared/materialized. Transitive components stay together. Pinned manifests
include deterministic versions, seed, selection hash, labels, partitions and hashes;
private evidence/lineage stays in the database. Exported payloads omit raw originals,
source URLs, private filenames, seller/listing text and financial/provider records.
Standalone releases reproduce exactly; combining releases is unsupported.

Relevant upload/privacy, classification/review and derivative mutations coordinate
with publication and withdraw invalidated component snapshots, including component
growth and new shared crops. Encoding/copying happens outside the lock; final
publication rechecks ownership, auth, eligibility/expiry and withdrawal under it.
Kernel reservations and atomic file publication support exact-ID recovery after
interruption. Retained history is never rewritten; already copied bytes are not
claimed recallable. No automatic live deletion.

## Compatibility and actual validation

Wheel/sdist, release source inventory, enumerated runtime grants, exact schema/head
admission and dataset inventory fingerprints include 0019. The existing centralized
backup-format allowlist feeds backup, retention and health consumers. The four-artifact
schema-3 contract remains: DB-backed manifests and BlobStore-backed derivatives need
no fifth artifact. Accepted old heads still validate; unknown/multiple heads fail.
Backup retention, encryption and permanent pins are unchanged.

[Focused validation](focused-validation.json): **65 unit/operational tests passed**;
**all 40 selected PostgreSQL integration cases have passing evidence**. The final
pass had 39 passes and one stale 0017 test expectation; after correction, only that
case was rerun and passed. Nine release-manifest cases were rerun after its final
inventory update and passed. Focused Ruff/mypy and the isolated installed wheel/
sdist, migration graph and credential-free schema checks passed.

Evidence includes the authenticated CLI entry point with generated TEST settings/
password-prompt input (in-process harness; real auth/DB/blob/filesystem), admission,
replay, transitive excluded bridges, crop-driven growth, expiry and withdrawal races,
interrupted publication, affected upload/privacy/receipt/order/parser paths, and one
real disposable DB/blob round-trip preserving exact active outputs, withdrawn state
and inventory fingerprints. This is source/TEST proof, not a deployed-terminal or
production qualification claim. Existing test-library warnings remain. Raw private
logs are excluded; failing traces can contain generated TEST session values.

## Inventory, preservation and limits

[Exact 22-path inventory/hashes](changed-inventory.json),
[cumulative patch against accepted local main](cumulative.patch), and
[preservation receipt](preservation.json). The plan copy renders repository-relative
links as source references; exact updated source-plan bytes are pinned in the
inventory and included in the patch. The approved original plan bytes are retained
privately under their owner-supplied hash.

All 22 pre-existing pending paths remain byte-identical and unstaged, including
AGENTS.md, both protected catalog tests and stopped 15B code. The local planning
package is unchanged. Main stays at its accepted commit, with an empty index and
no main push. Owned TEST databases were removed, volumes/prior running state
preserved, and cleanup ledgers report no leftovers. Review is by the implementing
assistant; no independently delegated review is claimed.

No existing private corpus, Phase 14 input, production record, provider/model call,
real-source acquisition, custom training, production recovery, web/APK build,
phone/server access or deployment occurred. Windows filesystem/ACL and real local
Docker PostgreSQL were exercised; Linux materialization filesystem runtime is
unqualified. The retained 16A production smoke root was not registered/backfilled.
Real corpus rights, that fixture gate, real analytics/export readiness, wider
reporting/hardening and production deployment remain outstanding.

Stop for implementation review. No deployment, corpus collection or training follows.
