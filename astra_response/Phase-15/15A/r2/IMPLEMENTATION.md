# Approved implementation

The complete implementation is in the [cumulative patch](implementation.patch)
against planning checkpoint `5b029368e0bf8f810deb2a305aa1a03cff5c5c95`.
The [inventory](inventory.json) hashes every changed path after UTF-8/LF normalization;
23 code/test/contract snapshots are under `files/`. Documentation changes are in
the patch, preserving historical documentation without republishing whole histories.

- Android receives image SEND/SEND_MULTIPLE through the existing MainActivity and
  [Share plugin](files/apps/android/android/app/src/main/java/com/abrianbaker/brickvault/appraisal/BrickVaultSharePlugin.java).
  [ShareIntake](files/apps/android/android/app/src/main/java/com/abrianbaker/brickvault/appraisal/ShareIntake.java)
  bounds memory to eight entries, 50 MiB aggregate, 25 MiB/file and 256 KiB bridge
  chunks. Provider MIME and stream access wait for verified foreground admission.
- The shared [React review](files/apps/web/src/NativeShareReview.tsx) presents
  per-entry failures, selection and existing/new listing choice before writes.
  It uses the existing Phase 13 client queue and API. Native code owns no listing
  model, HTTP upload client, credentials or financial rules.
- Immutable bytes and UUID/order context remain only in the live process.
  A new WebView authenticates and reads back the destination, marks prior results
  uncertain, and requires explicit retry. Retiring an uncertain entry frees its
  bytes and preserves the immutable context and assigned position high-water mark.
  Process death has no draft or automatic replay.
- The existing upload route accepts only optional `privacy_elevation=restricted`.
  The [server upload owner](files/services/api/src/brickvault_api/listings/service.py)
  monotonically elevates canonical originals and linked thumbnails under the
  existing lock order, including duplicate/shared/replayed submissions. Conflicts
  mutate nothing; there is no migration or second upload protocol.
- In r2, [the adapter](files/apps/web/src/native-share.ts) also copies a new batch's
  nullable native notice during admission. This removes a stale prior-batch auth
  instruction while preserving a new overflow notice and same-batch ACK warning.

No broad media permission, persisted URI grant, spool, image database, worker,
URL fetch, capture/overlay implementation, recognition/training operation or
15B/15C behavior was added. Existing retained-image policy is unchanged.
