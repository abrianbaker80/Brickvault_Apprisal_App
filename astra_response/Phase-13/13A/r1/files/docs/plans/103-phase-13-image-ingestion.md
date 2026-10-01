# ExecPlan 103 — Phase 13 image ingestion

## Goal and user-visible outcome

Phase 13A implements optional private listing/image backend foundations while
direct catalog search, valuation, Watchlist and Deals remain independent.
Phase 13 IN PROGRESS; Phase 14 NOT STARTED. Phase 12 remains ACCEPTED / CLOSED.

## Why this work is being done now

Brian explicitly authorizes 13A from main 653fae52ef5cb852985e2c36039b20523776f3b9,
with minimal change-scoped validation and a separate source review before shipping.
The [preserved ingestion contract](../IMAGE_INGESTION.md) governs this implementation.

## In scope

Migration 0017_listing_images adds listing, blob, image_asset, image_relation,
listing_image and upload_receipt. Implement the five documented HTTP routes,
filesystem BlobStore, actual decode and thumbnail-v1, PostgreSQL receipt/order
transactions and a report-only consistency library.

## Explicit non-goals

No polished browser upload UI (13B), Android, recognition, model/provider calls,
source-URL fetching, crop UI, deletion/retention automation, production migration,
infrastructure, deployment or main commit/push. No broad historical test campaign.

## Current repository state

Branch main; accepted HEAD 653fae52ef5cb852985e2c36039b20523776f3b9; empty index.
AGENTS.md and the two protected catalog tests remain byte-preserved and unstaged.
Accepted Phase 12 source schema is 0016_hunt_cached_runs; no live system is accessed.

## Decisions and assumptions

- UUIDs, UTC timestamps, Decimal database prices/string JSON; missing differs from zero.
- No saved-deal FK is introduced: the implemented core uses immutable forecast
  lineages rather than the proposed saved_deal table. A later linkage needs its own review.
- Filesystem SHA-256 keys, same-directory staging and atomic hard-link publication.
  An existing object is verified and never overwritten. No blob deletion interface.
- Pillow 12.3.0 preserves the selected decoder baseline; python-multipart 0.0.32
  supplies bounded multipart parsing. No OpenCV or provider dependency.
- BVA_IMAGE_BLOB_ROOT is optional; image upload/content fail closed when absent.
  Storage is outside configured static output and repository web source roots.
- Unknown image sources/screenshots are restricted; explicitly classified
  seller_photo/listing_photo originals are private. Shared assets can only escalate
  to restricted; thumbnails inherit the stricter original classification.
- Listing reads are owner-scoped. Existing session/Origin/CSRF/no-store controls
  protect all routes; mutation transactions recheck the session after processing.

## Data model and API/interface changes

The six tables preserve the minimal model. Unique canonical originals and distinct
thumbnail semantics, typed lineage FKs, same-listing receipt FK, immutable
successful receipts, exact hash/result constraints and deferred minimum-order
checks enforce the contract in PostgreSQL. Runtime receives enumerated grants,
with no blob/receipt/lineage delete or metadata overwrite privileges.

POST /api/listings; GET /api/listings (default 50, max 100, stable newest-first);
GET /api/listings/{id}; POST /api/listings/{id}/images;
GET /api/images/{asset_id}/content. Metadata URL is inert HTTP(S) only.
Generated OpenAPI/TypeScript records backend changes without a frontend build.

## Implementation sequence

1. Preserve baseline/protected state and inspect relevant contracts/conventions.
2. Add frozen forward/reverse SQL, bounded modules, settings and route registration.
3. Add focused synthetic tests and validate both disposable migration paths.
4. Run changed-file Ruff/format/mypy and credential-free contract generation/check.
5. Publish exact changed files and cumulative patch under Phase-13/13A/r1 on
   isolated astra-response. Leave main uncommitted/index empty.

## Validation and acceptance criteria

Approximately 8–15 meaningful API/storage/database cases, including exact bytes,
thumbnail PNG/WebP handling, duplicates/replay/conflicts, failed DB commit, shared
blob, grouped invalid images, consistency reports and one real ordering scenario.
Fresh disposable DB reaches head; accepted 0016 upgrades to head; downgrade smoke
is confined to disposable data. Use existing owned TEST instance/cleanup ledger.
No broad suites, browser tests, frontend/production builds or concurrency permutations.
Stop once these focused checks pass; fix a directly scoped failure and rerun only affected checks.

## Security, privacy, and data-integrity considerations

The [proposed policy](../IMAGE_PRIVACY_POLICY.md) is for Brian's shipping review,
not approval. Use synthetic images only. Bound streamed multipart before spooling,
reject invalid/animated/oversized images, and process decoding outside the event loop.
No paths, filenames, metadata or image bytes enter logs. Content is authenticated
and no-store. Blob storage/backups must remain private at eventual deployment.

## Failure modes, rollback, and recovery

Blob publication precedes metadata commit: a failed commit may leave complete
unreferenced objects. Never report success before commit; retries reuse verified
immutable bytes. No automatic deletion/repair. The report-only library identifies
missing/corrupt/referenced/unreferenced/staging objects. Definitive orphan reports
require uploads stopped. Local filesystem atomic publication failure or a broader
transaction defect stops the slice. Production recovery needs database-plus-blob
backup design and separate authorization.

## Progress log

- [x] 2026-10-01: Phase 13A authorized; baseline and preserved contract inspected.
- [x] 2026-10-01: Bounded backend/migration implementation prepared.
- [x] Focused disposable validation: 14 cases PASS; eight affected cases PASS after
  response/JSON-null admission corrections. Both cleanup ledgers report no leftovers.
- [x] Fresh PostgreSQL 18 -> 0017 and 0016 -> 0017 preserve existing auth data;
  disposable 0017 -> 0016 -> 0017 smoke PASS. No production migration.
- [x] Generated contracts regenerated/checked; final changed-file static checks recorded in review.
- [x] Sanitized source review prepared for publication on astra-response;
  main/index/protected boundary verified. Publication commit receipt is returned separately.

## Open questions or physical-device/manual checks

Brian must review shipping retention/deletion/recovery duration and private backup
policy. Linux deployment filesystem qualification and browser UI are deferred;
Windows synthetic atomic publication is the local evidence target. Phase 14 is unauthorized.

## Outcome and follow-up

**Phase 13A IMPLEMENTED / READY FOR REVIEW. Phase 13 IN PROGRESS;
Phase 14 NOT STARTED.** Fourteen meaningful cases passed in 13.86 seconds;
eight affected cases passed in 10.62 seconds after narrow source-review corrections.
Fresh/upgrade/downgrade smoke used PostgreSQL 18 and synthetic data only; all
owned disposable databases were removed. Existing TestClient dependency warnings
are recorded without introducing a test-stack migration. No broad suite, browser,
frontend/production build, provider, device or production operation ran.
The only next milestone after 13A review is separately authorized Phase 13B UI work.
