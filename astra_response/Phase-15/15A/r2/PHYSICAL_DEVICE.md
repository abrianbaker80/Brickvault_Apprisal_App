# Physical TEST evidence — 2026-10-18

Device: Samsung SM-S948U, Android 17/API 37. Target package:
`com.abrianbaker.brickvault.appraisal`, min API 24, target/compile API 36.
The first compatible TEST APK was `eb18c911…085bcf`; the final notice-fixed TEST
APK was `fcc37bfe…b22c9c`. Both use the retained public signer SHA-256
`e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72`.
The localhost HTTPS API used only the owned disposable TEST database at migration
`0017_listing_images`, private synthetic blobs and a disposable account. The phone
system trust store and network settings were not changed.

| Check | Observed result |
|---|---|
| Real source-app discovery/reception | Samsung My Files Sharesheet offered BrickVault. Cold authenticated and warm single/multiple Shares reached explicit review; cold signed-out Share retained nothing through sign-in and required re-share. |
| Review/destination | No listing/image POST before Save. Existing listing duplicate and explicit new-listing creation/upload both passed. Received JPEG/WebP order was preserved. |
| Exact originals | Five authenticated HTTP original-content reads exactly matched approved PNG/JPEG/WebP and provider A/C hashes/byte counts. [Readback](evidence/authenticated-originals.json). |
| Partial input refusal | A controlled distinct-UID provider demonstrated missing stream, unsupported GIF and 25 MiB+1 refusal while A/C remained usable. A shell-sent non-content URI was refused. Corrupt PNG reached the authoritative backend decoder and failed INVALID_IMAGE while siblings retained success. [Native results](evidence/input-refusals.json). |
| Genuine revoked URI | Provider confirmed READ(B) GRANTED, revoked only its unique B URI while returning A, then confirmed DENIED. B failed URI_UNREADABLE; A/C were saved. [Method/result](evidence/provider-revocation.json). |
| Concurrency/retry | Three-entry corrupt case observed maximum two concurrent uploads. Explicit corrupt retry kept UUID/bytes/order and added no receipt. |
| Duplicate/privacy | Exact duplicate kept its existing listing-image relationship/order and added one receipt. Matching original and thumbnail elevated from private to restricted. Shared exact originals remained restricted across listings; all ten final assets were restricted. |
| Real lost response | CDP aborted one actual image response after server 201. Both submitted images remained saved; UI paused with uncertainty. Authenticated recovery required explicit retry of the same UUID/position, returning its stored result. [Fault/requests](evidence/network-faults.json). |
| Actual Activity recreation | Public Activity.recreate destroyed/created/resumed the real Activity. PID stayed 20869; Activity and WebView identities changed. Immutable queue context, selected-ID retirement mask, zero retired bytes and next position 2 survived. No automatic upload occurred. Explicit retry kept 9 links/12 receipts. [Lifecycle and identities](evidence/lifecycle-recovery.json), [before](evidence/lost-before-retry.json), [after](evidence/replay-same-receipts.json). |
| Rotation | Per-app orientation changes produced landscape 795×339 and portrait 384×777 CSS viewports with the same queue context. Original requestedOrientation -1 was restored. No global rotation setting changed. |
| Backend stopped/restarted | An actual stopped listener caused an honest pause, retained the live bytes and made zero listing POSTs. After restart, explicit session verification, refreshed destination selection and Save succeeded. No network-setting toggle or automatic retry. |
| Cancel/auth/process death | Cancel and sign-out removed pending native bytes/previews. Real server session revocation produced 401 and cleared the batch with zero blob previews. Force-stop/relaunch produced a new PID with no draft or automatic replay; saved server images remained. [State readbacks](evidence/auth-lifecycle-clearing.json). |
| Manual fallback | The existing listing's manual field opened Android Photo Picker; Browse/DocumentsUI selected an owned fixture and the Phase 13 queue completed upload. Capture/recognition remained absent. |

Server observability reconciles **17 image POSTs = 13 receipts + 2 explicit same-UUID
replays + 2 corrupt failures**, and exactly three listing creates (one seed, two phone
actions). No unaccounted write request occurred. [Write ledger](evidence/server-write-ledger.json).
The final saved TEST state was three listings, nine links, thirteen receipts and
five originals plus five thumbnails. [Saved state](evidence/final-saved-state.json).

Accepted Phase 9 core lookup/valuation qualification was reused as required by
Plan 108. This fresh TEST database has no active official catalog; direct search
honestly displayed unavailable. No catalog seed override, import, provider call or
new full valuation qualification was performed. A fresh elapsed-time expiry campaign
was not rerun: physical sign-out and real server revocation exercised Share clearing,
and focused auth/lifecycle tests cover the new state boundaries. These limits are
distinct from the passed physical Share checks.

Cleanup removed the exact disposable database/private blob store/credential file,
restored the prior stopped TEST service state, preserved volumes, removed both test
helper packages, five generated phone files/folder and their media rows, ten owned
CDP forwards and the TEST reverse rule. Native intake is empty. The final TEST app
remains installed, signed out and stopped; its retained production predecessor was
not reinstalled without separate approval. [Cleanup](evidence/cleanup.json).

No Facebook activity/compatibility, capture/overlay, provider/model call, production
contact, 15B or 15C result is claimed. STOP for Phase 15A review.
