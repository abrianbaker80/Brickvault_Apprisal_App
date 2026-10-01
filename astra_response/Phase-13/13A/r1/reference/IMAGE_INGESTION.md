# Later Listing and Image Ingestion

## Status, scope, and preserved work

This is the preserved image contract from the unexecuted, earlier image-first ExecPlan 000, relocated to Phase 13 under D-018/D-021. It does not authorize work or impose requirements on Phase 1. See roadmap (`ROADMAP.md`), product specification (`PRODUCT_SPEC.md`), and security/privacy (`SECURITY_PRIVACY.md`).

Phase 13 adds optional listing sessions, manual listing metadata, immutable originals, independent uploads, exact deduplication, thumbnails, and listing/detail UI to the already-working sourcing platform. A saved deal can optionally reference a listing; direct set search and valuation never require one. Catalog identities, provider mappings, and financial rules remain owned by the core.

Phase 13 excludes recognition/model calls, new pricing logic, Android-native capture, training exports, near-duplicate detection, crop UI, and automatic retention deletion. Later recognition is Phase 14, Share/overlay experiments Phase 15, and dataset/outcome work Phase 16.

Before this feature ships, Brian must review an explicit retention/deletion policy for raw screenshots, seller photo originals, derivatives, backups, and exports, including purpose, access, duration, and intentional deletion/recovery procedures. Screenshots can contain personal names, profiles, locations, messages, and notifications. Immutability prohibits accidental overwrite; it does not waive an approved deletion policy. Keep original bytes while retained; no automatic deletion is authorized by this contract.

## Later tooling and product behavior

The earlier image-processing planning baseline selected Pillow 12.3.0, with OpenCV only for a later demonstrated need; recheck stable compatibility in the authorized image task, not now. Keep decode/thumbnail work bounded and outside the async event loop. Local filesystem storage remains behind BlobStore so an S3-compatible adapter can be added later without changing domain semantics.

Optional listing editing/archiving, successful-image removal/reordering, and crop UI require their own later checkpoint; removal of a failed queue item is not deletion of a saved original. Default listing currency follows the core user setting (USD was the earlier planning default), with exact decimal asking prices and missing distinct from zero.

## Detailed Phase 13 contract

### Minimal persisted model

Use UUID identifiers, timezone-aware UTC timestamps, foreign keys, and database constraints.

| Record | Purpose and constraints |
|---|---|
| `listing` | Source type, optional URL/title/description/asking price, currency, timestamps. Asking price uses decimal storage and string JSON representation; missing price differs from zero. |
| `blob` | One row per SHA-256, with unique storage key, byte count, and creation timestamp. Represents physical bytes. |
| `image_asset` | References a blob and records decoded format, dimensions, kind, and privacy classification. Originals and thumbnails remain distinct semantic assets even if bytes happen to match. A partial unique index permits only one canonical original asset per blob. |
| `image_relation` | Parent, child, transformation version, and transformation metadata. Unique thumbnail recipe per original; foreign keys prevent missing parent/child assets. |
| `listing_image` | Listing-to-original relationship with persisted `display_order`. Unique `(listing_id, original_asset_id)` and `(listing_id, display_order)`; nonnegative order check. |
| `upload_receipt` | Successful client UUID, filename, content hash, immutable requested `display_order`, `listing_image_id`, and stored result. Unique `(listing_id, client_upload_id)` and `(listing_id, display_order)`; nonnegative order check. A composite foreign key ensures the referenced listing-image belongs to the same listing. |

Reuse the canonical original asset for identical uploaded bytes. Associate it with multiple listings through separate relationships. There is no separate image relationship for each duplicate receipt.

Do not create recognition, confirmation, outcome, or training tables prematurely. Future predictions and confirmation events remain separate. Future dataset grouping must account for originals shared across listings, so exact duplicates cannot cross evaluation partitions.

### HTTP contract

| Route | Behavior |
|---|---|
| `POST /api/listings` | Create a listing; return `201`. Metadata may be omitted. |
| `GET /api/listings` | Return newest-first results with stable ordering and bounded pagination: default 50, maximum 100. |
| `GET /api/listings/{id}` | Return metadata, ordered image/thumbnail references, and `next_display_order`, or `404`. Each image entry has `listing_image_id`, original/thumbnail asset IDs, and its persisted `display_order`. |
| `POST /api/listings/{id}/images` | Accept exactly one multipart `file`, `client_upload_id` UUID, and integer `display_order`. Each request is independently committed. |
| `GET /api/images/{asset_id}/content` | Stream known asset bytes through the API; never expose filesystem paths. |

API errors remain API errors. The frontend fallback must not serve HTML for unknown `/api` routes or missing static assets.

Generate OpenAPI from Pydantic schemas without requiring a live database or provider credentials. Generate TypeScript types from that schema and use `openapi-fetch`; do not manually duplicate server request/response types. Contract verification regenerates into temporary output and fails on drift. [OpenAPI TypeScript client documentation](https://openapi-ts.dev/openapi-fetch/).

### Upload results and retries

Every selected file has a stable client-generated upload UUID. Its per-file result contains:

```text
client_upload_id
filename
status: uploaded | duplicate | failed
listing_image_id: UUID | null
error: null | { code, message }
```

- New attachment: `201`, `uploaded`, a new listing-image relationship, and a new receipt.
- Same bytes already attached to that listing, with a new UUID and available intended position: `200`, `duplicate`, the existing `listing_image_id`, and a new receipt for this UUID and position.
- Retry of an already committed UUID with identical bytes and `display_order`: `200`, the original stored result and `listing_image_id`. Reuse its receipt without creating another.
- Reuse of a committed UUID with different bytes or `display_order`: `409`, `UPLOAD_ID_CONFLICT`. Do not move the existing relationship or modify its receipt.
- A new UUID claiming a position already owned by another receipt: `409`, `DISPLAY_ORDER_CONFLICT`, even when the bytes match. Check UUID replay before treating its own position as a conflict.
- Validation or storage failure: appropriate non-2xx status and a stable error code. No successful receipt or listing-image change commits for a failed request.

The server hashes bytes itself. Enforce idempotency, position ownership, and duplicate protection using PostgreSQL constraints and conflict handling. Serialize the short receipt/link/order transaction per listing with a database row lock; validate and process bytes before that lock. Do not rely on a process-local lock for consistency.

Every successful duplicate must commit its receipt and any deterministic ordering update in the same transaction before the server returns success. Failed attempts do not permanently bind a UUID; browser retries still preserve its intended bytes and position. Re-selecting a different file is a new submission with a new UUID.

The browser maintains queued, uploading, successful, duplicate, and failed states. It uploads at most two files concurrently and allows independent retry/removal of failures. Transport errors and early request rejection are normalized into the same result shape using the browser's known UUID and filename.

Successful files are never resubmitted because another file failed. Later analysis consumes successfully stored images independently of failed queue entries; Phase 13 adds no analysis controls.

### Deterministic ordering

1. Before dispatching a selection, the client reads `next_display_order` and assigns each file consecutive integer positions in selection order. The first position is the greater of that server value and the client's next-unused-position counter. That counter starts at zero, advances to one past the highest position assigned, and never decreases during the queue's lifetime, including when failed entries are removed. Thus its high-water mark accounts for pending and failed files without an off-by-one ambiguity. Persist successful intended positions in receipts; retain pending/failed UUID-position pairs in the browser queue for its lifetime.
2. `next_display_order` is zero for no receipts, otherwise one greater than the maximum successful receipt position. Derive it from all receipts, including duplicates, rather than only visible listing-image rows. It is an allocation hint, not a cross-client reservation.
3. Never compact gaps, reuse an outstanding failed position within the queue, or assign positions when a request finishes. Retrying after another file succeeds uses the same UUID, bytes, and intended position. Reopening a listing restores successful data; persisting an unfinished browser file queue across reloads is outside Phase 13.
4. A unique original occupies the minimum `display_order` among its successful receipts for that listing. Persist this minimum in `listing_image.display_order` in the same transaction as each new receipt. This rule also applies when a lower-position duplicate finishes after a higher-position copy.
5. Return listing images in ascending persisted `display_order`. The database's unique position constraints prevent ties. Receipt positions remain claimed even if deduplication means a position has no separate visible image.
6. Stale clients may propose an already claimed position. Return `DISPLAY_ORDER_CONFLICT` without silently choosing a replacement position. The UI explains the conflict and permits removing/reselecting only that failed file after refreshing positions; reselection gets a new UUID. An ordinary retry never changes position.

Example: Brian selects `A@0, B@1, A-copy@2`, where A and A-copy have identical bytes. Whether position 2 or position 0 completes first, all successful results leave two listing images ordered `A@0, B@1` and three receipts at positions 0, 1, and 2. A replay of either A submission returns the same `listing_image_id` without an additional record. If B fails and is retried, it keeps position 1. A later selection starts at position 3.

This specifies ordering for independently uploaded files without introducing a batch-reservation endpoint or making the whole selection atomic.

### Image processing and BlobStore

Initial configurable limits:

- 25 MiB per file; 26 MiB multipart request ceiling.
- 40 megapixels and 16,000 pixels on either side.
- Single-frame JPEG, PNG, and WebP.
- Reject animations, unsupported formats, corrupt/truncated files, and decompression bombs.

Enforce request limits while receiving bytes, including chunked uploads. Inspect actual format and fully decode accepted images; filenames and declared MIME types are insufficient evidence.

Hash and store the exact uploaded bytes. Orientation changes and metadata removal apply only to derivatives.

Thumbnail recipe `thumbnail-v1`:

- Apply EXIF orientation.
- Fit within 512 × 512 without enlargement.
- Convert to RGB; composite transparency onto white.
- Encode JPEG at quality 85 without inherited EXIF or other source metadata.
- Record recipe parameters and decoder version in lineage.

The filesystem `BlobStore` exposes conditional immutable publication, read, stat, and enumeration. Keys derive solely from SHA-256, for example `sha256/ab/cd/<hash>`.

Write to a temporary file on the same filesystem, flush it, and atomically publish without replacing an existing object. Verify an existing object before reuse. Require storage that supports the adapter's atomic publication semantics; verify the implementation on Windows and, before deployment, the intended Linux filesystem. No home-server access is authorized by this plan.

Generate and publish both original and thumbnail before committing their metadata, relationship, ordering, and receipt in one database transaction. Return success only after that transaction commits.

## Failure modes and recovery

Filesystem publication and PostgreSQL commit do not form one transaction. Design explicitly for that boundary:

- **Publication fails:** roll back metadata and report a retryable failure.
- **Database commit fails after publication:** complete unreferenced blobs may remain. Preserve them; retries can reuse them.
- **Process exits before commit:** staging or unreferenced objects may remain, but no successful receipt exists.
- **Response is lost after any successful result, including a duplicate:** the receipt recovers the original result and relationship.
- **Ordering or UUID conflict:** no new successful receipt, link, or order change commits. Do not silently choose another position.
- **Existing hash key contains incorrect bytes:** fail closed and report corruption; never overwrite it.
- **Thumbnail processing fails:** do not report successful attachment; preserve previously published bytes for recovery.

The consistency command is report-only. Run a definitive orphan audit while uploads are stopped. Document recovery by retry, or restoration of missing/corrupt objects from a verified backup. Do not implement automatic deletion.

Use forward migrations for retained development data. Test downgrade/re-upgrade only on a disposable database. Future operational recovery requires a consistent database-plus-blob backup; home-server backup/deployment work remains outside Phase 13.

## Acceptance evidence

### Phase 13 acceptance

- A fresh development database reaches the expected Alembic head; repeating the upgrade is harmless.
- Brian creates a listing and uploads JPEG, PNG, and WebP files through the browser.
- Retrieved originals match the uploaded files by hash and byte comparison.
- Each original has a distinct thumbnail asset and recorded transformation lineage.
- Repeated and simultaneous exact uploads produce one physical original blob and one image relationship per listing.
- Reusing bytes across two listings shares the blob and preserves both listing relationships.
- Every successful duplicate with a new UUID has a receipt; replay after a lost duplicate response returns its stored result and the same `listing_image_id`.
- Replaying any committed UUID creates no additional receipt or relationship; changing its bytes or intended order yields `UPLOAD_ID_CONFLICT`.
- Reversed completion orders for distinct files return the same final intended order, including after restart.
- The `A@0, B@1, A-copy@2` scenario produces the same persisted image order and receipt positions in both completion orders.
- Retrying a lower-position failure after higher-position successes preserves its original position and UUID.
- Claiming another receipt's position yields `DISPLAY_ORDER_CONFLICT` without moving existing images; selection after a duplicate uses the receipt high-water mark.
- A mixed selection preserves valid uploads and displays individual failures. Retrying/removing a failure does not re-upload successful files.
- Decoder, size, dimension, animation, MIME, and malformed multipart tests exercise real processing.
- Injected filesystem and database failures never produce success with missing committed assets. Receipt, relationship, and ordering changes roll back together.
- A lost response after commit is recoverable through idempotent retry.
- Refreshing and restarting local services preserves the listing, metadata, images, and order.
- The built frontend works through FastAPI at desktop and mobile viewports, including direct listing-detail navigation.
- Unknown API routes return JSON errors; source files, local configuration, and blob directories cannot be reached through static serving.
- Generated contracts match the API, and every relevant formatter, linter, type check, test, and build passes.

Integration tests use real PostgreSQL and temporary filesystem storage. Use deterministic barriers for races and inject failures at I/O boundaries; do not replace the upload use case with mocks.

A definitive storage consistency command is report-only: enumerate missing, corrupt, unreferenced, and staging objects without deleting them, and run with uploads stopped. Preserve the original plan's future command intention as a Phase 13 requirement: pnpm storage:check --dry-run, alongside actual upload/browser/integration tests; this command does not exist in the planning repository.

Do not claim Phase 13 complete without proving the retention policy, private authenticated access, immutable bytes, exact duplicate races, successful-duplicate lost-response replay, and deterministic order on a real PostgreSQL/filesystem path. New source URLs are metadata only and are never fetched.

## Follow-on capture, recognition, and dataset lineage

Rebrickable's current Terms, recorded from Brian's first-party page evidence on
2026-09-09 in the provider policy record (`PHASE_2D_PROVIDER_GATE.md`), prohibit AI
training with Rebrickable content. Its images and downloaded catalog metadata are
not approved training material. Training datasets must use independently permitted
or user-owned sources; any Rebrickable-derived training use requires a separate
explicit rights review and provider authorization. Metadata import or permission
to display an image does not grant training rights. No image or AI implementation
is part of Phase 2D.

Later capture_session records group explicit user captures with minimal client/device/version/time metadata; object_region records selected geometry and derived asset lineage. Add these only when their later use case exists.

Phase 14 records analysis_run, provider_call_log, candidate_match, and append-only identity_confirmation. A candidate references a canonical core set or minifigure; an unresolved guess is separate from a verified mapping. Strict structured results preserve rank, confidence, supporting evidence, contradictions, and requested additional views; permit unknown, insufficient evidence, custom build, mixed sets, and non-LEGO outcomes rather than forcing identity. Return multiple candidates where evidence supports them. The shared valuation API consumes the selected identity, never model-invented prices.

Preserve the earlier simple review workflow: open an optional listing, analyze successful images despite other upload failures, inspect status/evidence, confirm or enter a different identity, and reopen the append-only audit trail. Those image-derived identities use the same direct-search and valuation services; a manual price scenario is labeled and cannot masquerade as sourced evidence. Any later expansion to scalable reference retrieval must retain source rights, idempotent incremental indexing/re-embedding, deterministic ties, and coverage/cost reporting without a parallel catalog.

Later image kinds include raw screen capture, listing-photo crop, object crop, normalized analysis image, and training derivative; privacy classes distinguish restricted raw material from reviewed sanitized crops. Record transformation recipes/coordinates and provider/model/prompt versions without secret/raw-payload logs.

Label states are unreviewed, partially_labeled, confirmed, purchase_verified, training_ready, and excluded. A prediction cannot promote itself. Only Brian-confirmed or purchase-verified labels with privacy review become training-ready. Preserve corrections and appropriate hard negatives.

Versioned dataset releases preserve immutable manifests, hashes, source provenance, selection rules, seed, positive/negative pairs, and split membership. Every connected listing/source group, including exact originals shared across listings, stays in one train/validation/test partition. Dataset exports are sanitized and reproducible; custom training remains a separately requested later experiment.
