# Upload and ordering semantics

POST /api/listings creates optional metadata with 201. GET /api/listings uses stable
newest-first order and offset pagination (default 50, maximum 100).
GET /api/listings/{id} returns metadata, image/thumbnail asset IDs, listing_image_id,
persisted visible order and next_display_order. POST /api/listings/{id}/images accepts
one multipart file, client_upload_id UUID and nonnegative integer display_order.
GET /api/images/{asset_id}/content streams authenticated known asset bytes, no-store,
with nosniff and no filesystem path. Original bytes are verified before response.

| Submission | Result |
|---|---|
| New attachment | 201 uploaded; new receipt/link |
| Same original, new UUID/available position | 200 duplicate; new receipt, same listing_image_id |
| Exact UUID/bytes/position replay | 200 original stored result; no new rows |
| Committed UUID changed bytes or position | 409 UPLOAD_ID_CONFLICT |
| New UUID claims another receipt position, even duplicate bytes | 409 DISPLAY_ORDER_CONFLICT |
| Rejected processing/storage or failed DB transaction | non-2xx; no successful receipt/link/order mutation |

Known-file errors return the failed per-file result shape. Early parse/transport
rejections return stable API errors; the 13B client will normalize using its known
UUID/filename. Receipt replay returns its original filename/result, even if a retry
supplies a different filename. A committed UUID is checked before decode and again
under the listing lock. Failed attempts do not bind a UUID.

Processing/hash/blob publication precede the short PostgreSQL listing-row lock.
Metadata, receipt, link and minimum visible order commit atomically. Allocation
history comes from all successful receipt positions, including duplicate receipts:
next_display_order is max+1. No gap compaction or conflict reassignment. Lower-position
duplicates lower the existing visible order while retaining every claimed position.
The single real overlapping A-copy@2/B@1, then A@0 scenario yields A@0/B@1,
receipts 0/1/2 and high-water 3; a new service/storage instance reads that persisted state.
