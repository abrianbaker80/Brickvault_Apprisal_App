# ExecPlan 103 — Phase 13 image ingestion

## Current checkpoint — Phase 13B, 2026-10-01

**Phase 13A ACCEPTED / CLOSED. Phase 13B IMPLEMENTED / READY FOR REVIEW. Phase 13 IN PROGRESS;
Phase 14 NOT STARTED.** Brian accepted [13A r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f59328e7bbe05dce9316940fc41f046a5a55b142/astra_response/Phase-13/13A/r1/REVIEW.md).
Exact accepted 24-file closeout produced local commit
`d14002e244434123dc68b57aefda004a00aa8e89`,
`Implement Phase 13A image ingestion backend`. Complete staged changed lines match
accepted r1; whitespace, 242 Markdown links and protected hashes passed. No 13A
pytest, migration tests, contracts, static checks or builds reran for closeout.
Main was not pushed. This commit is the Phase 13B source baseline.

Brian explicitly authorizes 13B immediately: private Listings navigation, simple
metadata creation, bounded newest-first list, persisted gallery and original
viewing, multi-file queue (two simultaneous uploads), independent retry/removal,
stable UUID/bytes/selection position, and clear conflicts. The generated 13A API
contract stays authoritative. USD follows the existing core currency convention;
there is no user currency setting in the current application-settings response.

### Phase 13B design and implementation

- `ListingsPage.tsx`, `listings-api.ts`, `upload-queue.ts` integrate with existing
  App/AppShell navigation, online-only gating, generated openapi-fetch and session
  transport. Twelve rows per page; each card reads the existing detail projection
  for image count/preview because the accepted list response contains metadata.
- One file per multipart request. Queue positions and UUIDs are assigned before
  dispatch; local next-position never decreases. Retries keep the same File object,
  UUID and position. Uploaded/duplicate submissions stay successful. Failed local
  removal never deletes stored data. Conflict resolution requires refresh/removal/
  reselection; it never silently reallocates an attempt.
- Successful results trigger authoritative detail refresh; aborted/stale reads do
  not replace a newer gallery. Gallery order comes from the server. The short-lived
  original viewer retrieves exact bytes through the authenticated content API.
- Image object URLs exist only in document memory and revoke on unmount/change.
  No local storage, private service-worker caching or provider submission is added.
  Queue/document state is lost on navigation/reload; persisted images reopen.
- Two explicit static shell routes admit `/listings` and UUID listing-detail URLs,
  needed for direct opening/reload; unknown API/assets still return errors. These
  routes are excluded from OpenAPI and do not change the 13A API contract.

### Phase 13B bounded validation and stop condition

Seven focused component/queue/client cases, two browser flows on real disposable
PostgreSQL 18 and filesystem blobs, plus a cheap mobile viewport smoke. Check
frontend types, affected lint/format and one normal frontend build. No broad
suite, 13A test rerun, migration test campaign or extra confidence permutations.
Fresh test-runtime schema provisioning is necessary browser setup, not a repeated
migration qualification. Stop at created real listing, multi-upload/concurrency
2, reload persistence, independent failure/retry and usable 1440x900/390x844 layout.

### Phase 13C remains separately authorized

The [privacy/retention policy](../IMAGE_PRIVACY_POLICY.md) remains **PROPOSED**;
13A source acceptance does not approve production shipping. Phase 13C handles:
Brian's privacy/retention approval; Linux production filesystem qualification;
production migration/release; database plus blob backup/recovery integration;
one real production listing/image acceptance; and final Phase 13 closeout.
Recognition/Phase 14, native capture, crop/reorder, persisted-image deletion,
metadata editing, saved-deal integration and source fetching remain excluded.
PWA/offline listing navigation qualification belongs to shipping; this UI requires
verified connectivity and adds no private offline image persistence.

### Phase 13B progress

- [x] Accepted 13A exact inventory committed locally; protected dirty bytes intact.
- [x] Listing create/list/detail/gallery and bounded upload queue implemented.
- [x] Seven unique focused cases passed: six initially passed, the native-Request
  multipart fixture and client construction were corrected, then the affected
  two-case subset passed. No broad suite or unchanged-case rerun. Lint type/form
  corrections stayed scoped; final affected lint/format and frontend typecheck PASS.
- [x] One normal frontend build PASS (60 modules). No release/backend build.
- [x] Two real browser flows PASS: create + three valid images + original viewing
  + reload/reopen; two-file mixed confirmed/unconfirmed results + independent retry.
  TEST-only fault returned 503 after the fourth upload had really committed; retry
  recovered its stored result. Six requests, five images, five receipts; peak two.
- [x] 1440x900 desktop / 390x844 mobile visual smoke PASS, no consequential overflow.
- [x] Explicit static shell admission corrected from the concrete initial 404;
  one affected Python module Ruff/format/mypy PASS. No backend pytest rerun.
- [x] Browser signed out/closed; owned API/database/blob store cleanup verified;
  prior stopped TEST state restored. No production, providers, PWA/Android or
  later-phase work.
- [x] Prepare/publish `astra_response/Phase-13/13B/r1/`; main 13B edits stay uncommitted,
  index empty and protected files byte-preserved/unstaged. Do not push main.

## Historical Phase 13A implementation evidence

The earlier implementation-stage status/authorization below is preserved history.
The current checkpoint above supersedes its next-step and no-commit statements.

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
