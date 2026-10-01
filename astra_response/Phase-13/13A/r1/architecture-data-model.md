# Architecture and data model

One FastAPI monolith and authoritative PostgreSQL database remain. New bounded
images/ and listings/ modules have no catalog, valuation or provider dependencies.
Existing authentication/Origin/CSRF/no-store behavior protects all five routes;
short write transactions recheck sessions after image processing. Listing mutations
count as owner activity. No new UI or financial calculations.

| Table | Contract |
|---|---|
| listing | owner-scoped UUID, optional inert source/title/description/Decimal price, currency and UTC timestamps |
| blob | unique SHA-256, immutable key/size, physical bytes |
| image_asset | original/thumbnail semantic kinds, dimensions/format/privacy; unique canonical original per blob |
| image_relation | typed original-to-thumbnail FKs, unique thumbnail-v1 recipe, decoder/recipe metadata |
| listing_image | unique original and visible position per listing; persisted receipt minimum |
| upload_receipt | immutable UUID/hash/position/filename/result; unique UUID and claimed position per listing; same-listing FK |

Deferred PostgreSQL constraint triggers verify visible minimum successful receipt
position and exact original hash at commit. Receipt JSON requires complete non-null
identity/status fields, a null error and exact filename/UUID/link equality. Immutable
records reject update/delete; asset privacy can only escalate. Runtime has enumerated
SELECT/INSERT and narrowly scoped privacy/order/row-lock UPDATE privileges.

No saved-deal link is added: the implemented saved-work schema is immutable forecast
lineages rather than a saved_deal table, so a clean preserved nullable relationship
is not already available. That optional linkage is deferred instead of changing core.
Generated contracts preserve every pre-existing path and schema component exactly;
only listing/image paths and their schemas are added.
