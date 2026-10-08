# Implemented Share intake and data integrity

The manifest now advertises image SEND/SEND_MULTIPLE on the same singleTask app
activity. MainActivity registers the local plugin and scrubs consumed/history/restored
Share intents. Cold delivery waits for the existing authentication outcome; warm delivery
uses the same pending-batch pull/event surface. Signed-out/expired intake is discarded
with a sign-in/re-share notice. No broad storage/media or capture permission was added.

Only granted content URIs are accepted. Stream-extra order is preserved, ClipData is
fallback only and contradictory inputs are refused. Provider MIME resolution and byte
reads run in the bounded verified-foreground reader. Invalid/unreadable/revoked/provider
runtime failures affect their own entries. Metadata/bytes remain limited to eight entries,
50 MiB aggregate raw bytes, 25 MiB each and 256-KiB chunks; source filenames are replaced
with neutral names. Actual single-frame format/dimension validation remains server-owned.

Native bytes and shared File/object-URL previews exist only in process/document memory.
No persisted URI grant, spool, preferences/database image draft, gallery export or
background upload service exists. Native pause invalidates admission, closes active reads
and discards late work; new verification is needed on resume. A synchronous queue predicate
checks current foreground/session/batch state at dispatch, avoiding React-effect timing races.

Brian reviews images and explicitly selects an existing Marketplace Listing or saves a
new optional listing. Existing create/detail/list/image API and generated OpenAPI types
remain authoritative. The client never fetches shared text/links or calls providers.
Each upload retains its UUID, bytes, display_order and authoritative listing_image_id;
the existing two-slot queue preserves independent failure/retry/removal and successes.

## Same-process recovery

ACK marks handoff without dropping the bounded original snapshot. Volatile reviewed
selection/create-uncertainty and immutable listing/item/upload-UUID/order context are
checkpointed before HTTP writes. A recreated document reauthenticates, hydrates exact
bytes and reads the saved listing. Every recovered upload remains uncertain until an
**explicit same-identity retry** recovers its receipt; a visible gallery image alone is
not proof of that UUID's receipt. Restoration sends no writes automatically.

Creation uncertainty is checkpointed before POST listing. Unknown creation outcomes
require listing readback and an explicit destination choice; no blind create retry.
Failed-entry removal checkpoints a monotone selected-item retirement mask, releases
that native/JS byte reference and survives recreation. UUID/order bindings do not change;
the high-water mark includes retired positions. Clear/logout/expiry releases all volatile
custody. A killed process retains nothing and cannot replay the original intent.

## Restricted-only server admission

The existing image multipart route accepts optional `privacy_elevation=restricted`;
absence preserves ordinary Phase 13 input behavior. Private/downgrade requests, extra
or duplicate fields and invalid values are refused. Native intake always requests restricted,
including when the selected listing's source type is seller_photo/listing_photo.

Privacy escalation is separate from UUID bytes/order identity. Within the existing
auth_control/listing/asset transaction lock order, originals and every applicable linked
thumbnail become restricted monotonically for new, duplicate, shared and exact replay
requests. A replay still returns the identical stored result/relationship and creates no
extra receipt; identity/order conflicts mutate nothing. No migration or duplicate model.

One real HTTP probe found Starlette multipart-limit exceptions bypassing the FastAPI-
subclass catch. Catching the base exception corrects normalization to INVALID_MULTIPART;
limits and assertions were not weakened. Retained-image deletion/backup policy is unchanged.
