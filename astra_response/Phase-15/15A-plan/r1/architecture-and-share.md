# Current native architecture and proposed 15A design

Inspected read-only on 2026-10-07 at local accepted source
`e9c7d1f14ccfdf8784a9d4402a2fc0641184dab9`. Paths below are repository-relative.
No native/source changes are included in this package.

| Existing surface | Finding |
|---|---|
| `apps/android/package.json` | Capacitor Android/core/CLI 8.5.2, App 8.1.1; retain accepted versions |
| `apps/android/android/variables.gradle` | Minimum API 24; compile/target API 36; phone API is unknown |
| `MainActivity.java` | Empty Java `BridgeActivity` subclass under `com/abrianbaker/brickvault/appraisal` |
| `AndroidManifest.xml` | Exported singleTask launcher, configuration handling, INTERNET, no backup; no Share/capture/overlay service/filter |
| `apps/android/capacitor.config.ts` | Bundled shared React webDir; explicit TEST/production HTTPS origin configuration; no remote server.url, mixed content or native HTTP/cookie bypass |
| `apps/web/src/App.tsx`, `ListingsPage.tsx` | Existing optional Marketplace Listings routes and detail/create/gallery/upload UI |
| `upload-queue.ts`, `listings-api.ts` | Stable UUID/position before dispatch; two concurrent independent uploads; same-file retry; generated openapi-fetch transport |
| `session-client.ts`, `api-transport.ts` | Existing cookie/session/CSRF and accepted TEST/production API transport |
| `api/listings.py`, `listings/models.py`, `listings/service.py` | Existing listing/image route validation, server identity, asset privacy, receipt/position transactions |
| Migration `0017_listing_images` | Existing authoritative listing/blob/asset/relation/attachment/receipt tables; no new schema needed |

## Proposed native receive and shared UI handoff

Extend the existing activity with a small registered local Share plugin and image-only
SEND/SEND_MULTIPLE filters. Capacitor's current bridge handles cold and warm intents;
React may not have a listener at cold delivery, so expose a pullable pending-batch API,
opaque batch/item tokens and an event prompting the pull. Do not emit bytes solely
to a not-yet-ready listener. Suppress consumed intent replay on activity recreation.

Read temporary granted content URIs, not guessed file paths. Use stream-extra order,
ClipData only as fallback, and reject contradictory representations. Do not client-dedupe
identical bytes. Ignore shared text/URLs for network fetch; sender metadata is untrusted.
Read actual bounded bytes without decode/re-encode and report per-item unreadable,
unsupported, corrupt or excess errors. Propose eight entries/50 MiB total raw/25 MiB
each; unknown reported size is not permission to read without a limit.

Transfer at most 256 KiB per bridge response with bounded outstanding chunks into
Blob/File; use neutral generated filenames. Acknowledgement releases native copies;
the shared queue retains each File only for its live retry lifetime. No spool, saved
image state, persisted URI grant, local DB, backup, native HTTP or credentials.

The React adapter presents an explicit existing/new listing choice before allocation.
New listing creation occurs only on Save; uncertain POST creation requires authenticated
list readback and explicit resolution, because it has no idempotency key. No blind retry.
Once a listing is known, load `next_display_order`, allocate each item's UUID/intended
position, preserve the queue high-water mark and use the existing upload transport.
Do not reassign failed positions or resend successes after another entry fails.

## Existing HTTP identity and failure contract

- `POST /api/listings`: explicit optional listing creation, 201; no image requirement.
- `GET /api/listings` and `GET /api/listings/{listing_id}`: owner-authenticated records,
  ordered images and `next_display_order`.
- `POST /api/listings/{listing_id}/images`: exactly one file per multipart call, current
  `client_upload_id`/`display_order`, one transaction and individual result.
- New bytes: 201 uploaded; exact already-attached bytes with a new UUID: 200 duplicate,
  existing `listing_image_id` plus new successful receipt.
- Same UUID/bytes/order replay: original stored result/relationship, no extra receipt.
  Different bytes/order: 409 UPLOAD_ID_CONFLICT. Claimed position: DISPLAY_ORDER_CONFLICT.
- Server hashes exact originals, validates single-frame JPEG/PNG/WebP and decoded
  limits, produces thumbnails/lineage and persists minimum-successful-receipt ordering.
- Existing private image content requires owner authentication and no-store. Contracts
  come from Pydantic/OpenAPI, generated TypeScript and openapi-fetch, not handwritten shapes.

## Real privacy-admission gap and root correction

The current service derives privacy from `listing.source_type`. Existing seller_photo
or listing_photo targets produce private images even if a newly shared image is an
unknown screenshot. Identical-UUID replay also returns before asset privacy escalation.
This conflicts with the approved restricted screenshot/unknown-source classification.

Propose optional `privacy_elevation: 'restricted' | None` on the existing multipart
route. Native intake always requests restricted. No value may downgrade privacy;
absence preserves current ordinary upload input behavior. Update strict parser/models,
service, generated contracts, TS transport and queue without a new route or migration.

Keep UUID equality based on bytes/order. After validating that equality, escalate
canonical originals and applicable linked thumbnails before a replay returns. Keep
the response, listing_image_id and receipt/order counts identical. New-UUID duplicate
and cross-listing shared originals likewise inherit the stricter class. Conflicting
replays must not mutate privacy. Real PostgreSQL tests cover first upload, duplicate,
replay, derivative inheritance, cross-listing races, invalid values and no downgrade.

Cancellation/log-out/expiry clears unsaved volatile intake and URLs; dispatched writes
may already have committed, so cancellation is not deletion. Backgrounding pauses
new admission/dispatch; in-flight requests may still commit and require authoritative
readback; no worker/service. Configuration rotation should preserve the live queue;
actual recreation must not re-ingest. Process death loses pending files/UUIDs, exposes
no cold-start private draft and triggers no replay: verify session/read server state,
then explicitly re-share. Durable recovery would need a new custody/privacy approval.
