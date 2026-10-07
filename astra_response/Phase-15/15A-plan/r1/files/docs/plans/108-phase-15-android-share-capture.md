# ExecPlan 108 — Phase 15 Android Share and capture preflight

## Goal and user-visible outcome

**READY FOR PHASE 15 PLAN REVIEW — 2026-10-07. Planning/preflight only.**
Phase 15 implementation is **NOT STARTED / NOT AUTHORIZED**. The first separately
authorizable slice, **15A**, receives one or more user-shared images in the existing
Capacitor app, asks Brian to choose an existing Marketplace Listing or explicitly
create a new optional listing, and uses the Phase 13 upload queue/API. **15B** is a
separate visible, allowlisted capture feasibility spike, available for authorization
only after accepted physical Share proof. **15C** identifies later polish only.

Direct set search, valuation, manual upload and Share remain independent of capture
and recognition. Capture failure must leave the supported intake routes available.

## Why this work is being done now

Phase 14 is CLOSED as quality-spike evidence. Production recognition is NOT
QUALIFIED; image-driven retrieval is DEFERRED / UNRESOLVED. Phase 13's accepted
listing/image storage and the existing shared Android core allow useful manual
intake without reopening recognition, provider calls or financial logic.

## In scope

- Now: repository/API inspection, read-only ADB metadata if connected, bounded
  official Android documentation research, this plan and sanitized review publication.
- Proposed 15A: a small native Share receiver/Capacitor bridge, explicit React
  destination/review, existing upload integration, a bounded privacy-elevation
  correction, and focused source plus physical-device acceptance.
- Proposed 15B: one approved supported mechanism, approved package allowlist,
  visible explicit capture/stop controls, and permission/window/lifecycle feasibility.
- 15C: record the later review/crop/order boundary; no detailed workflow or implementation.

## Explicit non-goals

No implementation, dependency installation, services, Gradle sync, builds, APK
installation, UI/device/capture/browser tests, database access/change, production
access, provider/model calls or old qualification suites now. No main staging,
commit or push. No second Android database/listing model, native core UI, client
valuation, new upload protocol, automatic URL fetch, recognition dependency or
schema migration is proposed. No OCR, text extraction, carousel interpretation or
advancement, crop polish, circles/annotations, near-duplicate algorithm, multi-photo
collection polish, training/export or Phase 16 work belongs to 15A/15B.

## Current repository state

- Local `main`: `e9c7d1f14ccfdf8784a9d4402a2fc0641184dab9`,
  `Close Phase 14 recognition quality spike`; index initially empty.
- Accepted Phase 14 review:
  `508e27ee36b60c4e645da5b4f911304da32fb4ff`,
  `astra_response/Phase-14/closeout/r1/`; preserved unchanged.
- Protected dirty files: `AGENTS.md`,
  `services/api/tests/integration/test_catalog_search.py`,
  `services/api/tests/unit/test_catalog_parser.py`; byte-preserved and unstaged.
- `108` was unused. Follow `.agent/PLANS.md`; current authority is this checkout,
  `CODEX_WORKFLOW.md`, prompt 15, roadmap/provider gate, image contract/policy,
  relevant architecture/decisions and accepted Plans 088/099/103.
- Capacitor core/Android 8.5.2, App 8.1.1; Java `MainActivity` only extends
  `BridgeActivity`. Manifest has a MAIN launcher, `singleTask`, configuration-change
  handling, INTERNET permission and disabled backup; no Share receiver or capture service.
  `variables.gradle`: minimum API 24, compile/target API 36. Keep accepted versions.
- Known phone: Samsung Galaxy S26 Ultra, Brian's model spelling `SM_S948U`;
  known app package `com.abrianbaker.brickvault.appraisal`. ADB was available;
  sanitized `devices -l` returned **zero devices**. Android release/API and installed
  Facebook-related package names are **UNKNOWN**, required at implementation preflight.
  No serial was published; no device command beyond availability discovery ran.
- Phase 9 Plan 088 proves TEST TLS via `adb reverse tcp:18443 tcp:18443`, packaged
  WebView `https://localhost`, API `https://localhost:18443`; its closeout removed
  the reverse/app-scoped TEST trust/qualification app. Later Plan 099 Gate 7 records
  accepted production Android HTTPS with system-only trust and no ADB reverse.
  Current source supports both explicit modes. The phone's presently installed
  artifact/mode/reachability is **not verified** by this planning inspection.

## Decisions and assumptions

These are **proposals for review**, not accepted implementation decisions.

1. Extend the existing Java activity with a local Capacitor Share plugin; no third-party
   Share dependency is needed in the plan. Add separate image `ACTION_SEND` and
   `ACTION_SEND_MULTIPLE` DEFAULT intent filters. Handle cold `onCreate` and warm
   `onNewIntent`; register the bridge before delivery. Use a pullable `getPendingShare`
   batch with opaque item tokens: events prompt a pull instead of carrying private bytes
   before React is ready. Acknowledged chunk transfer releases native byte copies.
2. Accept temporary granted `content://` streams only. Never resolve provider URIs to
   filesystem paths, request broad media/storage access, take persistable grants or fetch
   shared links/text. Sender names, MIME declarations and URI metadata are untrusted.
   Use `EXTRA_STREAM` order; use ClipData only if the stream extra is absent. Conflicting
   representations fail as ambiguous input; do not reorder or deduplicate identical entries.
3. Use bounded native/JavaScript memory only. Proposed intake limit: eight entries,
   50 MiB aggregate exact bytes, 25 MiB per entry; reject overflow with per-entry states.
   Enforce limits while reading even when reported size is absent/wrong; bridge chunks
   are at most 256 KiB, with bounded outstanding transfers. Use neutral generated filenames
   instead of source paths/private names. Preview through temporary
   object URLs. No disk spool, persisted draft, preferences/database image queue, gallery
   export, backup or private payload in saved-instance state/logs.
4. Intake may stay in the same live process while Brian reviews; no upload starts from
   intent delivery. Signed-out receipt asks for sign-in and re-share without retaining
   images through authentication. Logout/expiry/cancel clears unsaved bytes/grants and
   object URLs. Backgrounding pauses new admission and upload dispatch; already
   dispatched requests may still commit and require authoritative readback. No worker or service.
   OS task grants are temporary: close streams and release application references;
   never promise to revoke a grant whose lifetime Android controls.
5. Rotation/configuration changes preserve a live queue without reprocessing its intent.
   An in-process activity recreation uses only process memory and an opaque handled
   generation; clear the consumed intent payload. A process restart does not hydrate
   images/URIs or automatically replay an intent/upload. It opens the normal authenticated
   app, reads saved listing state after session verification, then requires explicit re-share.
   Durable crash-resume would need a new privacy/custody decision before implementation.
6. All Share inputs are conservatively `restricted` because pixel provenance is unknown;
   captures are always restricted. Existing listing metadata must not be rewritten to
   obtain this classification. Server retained-image policy remains unchanged.

## Data model and API/interface changes

Reuse `POST /api/listings`, paged `GET /api/listings`, `GET /api/listings/{listing_id}`,
`POST /api/listings/{listing_id}/images` and authenticated image-content routes.
Keep existing owner cookie/session/CSRF/Origin checks and `openapi-fetch`; native code
handles granted bytes only and never receives server credentials or makes API requests.

One real gap requires correction in 15A: `ListingService.upload` currently derives
privacy from `listing.source_type`; `seller_photo`/`listing_photo` yields private.
Thus an unknown screenshot shared to such an existing listing would violate the
approved restricted classification. Its receipt-replay return also precedes escalation.

Propose an optional multipart `privacy_elevation: Literal['restricted'] | None` on the
**same** image route. Absence preserves the existing Phase 13 input semantics; native
Share/capture always supply `restricted`. Update `UploadArguments`/`UploadBody`, the
strict multipart parser, service, generated OpenAPI/TypeScript contracts, `listings-api.ts`
and queue integration. No migration: asset privacy and lineage already exist.
Disallow private/downgrade requests, duplicate fields and unrecognized fields/values.

Escalate canonical originals and applicable thumbnails monotonically, in the existing
transaction, on new uploads, different-UUID exact duplicates and identical-UUID replays.
Check bytes/order conflicts before any elevation on a conflicting replay. Privacy
elevation is not a new UUID identity component: replay returns the identical stored
result and `listing_image_id`, with no extra receipt/order change. Shared originals
must not leave any related thumbnail less restricted. Serialize asset escalation
consistently and validate cross-listing concurrency with real PostgreSQL barriers.

The React review selects a destination before queue allocation. A new listing is
created only after explicit Save/Upload; if creation has an uncertain response, read
the listing list and ask Brian to resolve the destination, never blindly retry creation.
Do not introduce listing-create idempotency as hidden scope expansion. Once the
listing is known, read `next_display_order`, assign each selected entry its UUID and
position before dispatch, retain the queue high-water mark, and use existing maximum
two concurrent uploads. Preserve raw bytes, independent failures, successful receipts,
minimum-successful-receipt gallery order and exact SHA-256 deduplication on the server.

## Implementation sequence with small checkpoints

### 15A — Share Target physical-device spike

**Requires separate explicit implementation authorization, including the proposed
privacy-elevation contract and memory-only intake bounds.**

1. Reconfirm HEAD/index/protected bytes and image API/migration 0017. Obtain phone
   Android release/API read-only; retain known model/package without asking again.
   Record Facebook packages if available, without assuming a package or launching it.
   Select exact APK/backend/TEST ownership and authorized network/device scope.
2. Add the native receive/bridge surface under
   `apps/android/android/app/src/main/java/com/abrianbaker/brickvault/appraisal/`,
   wire `MainActivity.java` and `AndroidManifest.xml`, and expose bounded intent
   intake through a small TypeScript bridge. No capture/overlay/accessibility/FGS
   permission or service in this slice.
3. Add a shared React review/destination adapter in `apps/web/src`, integrate
   `App.tsx`, `ListingsPage.tsx` (including its detail view), `upload-queue.ts`
   and `listings-api.ts`; use the existing auth and queue state machine. Add the native
   intake adapter/review as a small new component, not a second set of listing screens.
4. Implement only the privacy elevation described above in
   `services/api/src/brickvault_api/api/listings.py`, `listings/models.py`,
   `listings/service.py` and generated `packages/contracts` outputs.
5. Run applicable formatter/lint/type checks, focused native lifecycle/URI/resource
   tests, frontend queue/contract checks and real PostgreSQL privacy/replay/concurrency
   tests. Once stable, run the applicable
   slice acceptance once, package/install only under the authorized device scope,
   then execute the checklist below on Brian's phone with approved nonprivate fixtures.
6. Publish sanitized evidence, mark Share QUALIFIED or NOT QUALIFIED and STOP for
   review. No successful 15A result starts 15B automatically.

### 15B — visible allowlisted capture feasibility spike

**Requires accepted 15A physical proof and separate mechanism, package, permission,
privacy and device-test approval. Currently BLOCKED AT MECHANISM SELECTION.**

- Preferred technical candidate to evaluate: API 34+ `AccessibilityService`
  `takeScreenshotOfWindow(windowId)`, rather than display-wide screenshots. Android's
  documented accessibility purpose is assisting users with disabilities; do not choose
  it solely to obtain package visibility without resolving suitability/permission scope.
- `packageNames` filters events, not screenshots. A candidate must identify one current
  application window/root package against Brian's evidence-backed allowlist, bind the
  request to that window, and revalidate identity/visibility on callback. Unknown,
  ambiguous, stale or changed target refuses/discards the frame. No UI text extraction
  or content logging. The public API does not promise atomic identity-plus-frame proof;
  target-change races are an acceptance gate, not assumed solved by event filtering.
- `MediaProjection` single-app capture (API 34+) is an alternative research candidate,
  but documented consent/configuration/callback APIs do not expose/enforce a selected
  package allowlist. It **cannot qualify alone under this request**. Do not replace
  package enforcement with Brian's chooser selection, usage polling or broad display capture.
  A supported design that closes that gap requires review before implementation.
- `TYPE_APPLICATION_OVERLAY` is an optional visible control, not a capture mechanism.
  Where needed, request permission visibly; recheck its grant/visibility before capture.
  If Android/the target hides overlays, capture is unavailable. No transparent control,
  security bypass, automatic tap/swipe/navigation, interception or boot/restart collection.
- Default disabled; enable explicitly for a short visible session; Brian triggers each
  one-frame capture. Stop immediately disables new requests and discards late callbacks.
  Release hardware buffers/display/service resources. Permission revocation, target
  changes, app/process restart or lock ends the session; never restart automatically.
- No upload until Brian previews the single result and explicitly chooses/saves a listing
  through 15A's intake. Retain Share/manual upload when capture fails. If no suitable
  supported allowlisted mechanism exists, report **CAPTURE UNSUPPORTED / NOT QUALIFIED**,
  stop for review and keep 15C blocked. No overlay-free Facebook promise.

### 15C — later boundary only

Only accepted 15B physical support and separate authorization may start a polished
manual multi-photo review/crop/order workflow. This plan does not authorize or design
OCR/text/carousel/near-deduplication/annotations/recognition/dataset features. Each
additional capability would need its own bounded scope and applicable rights/privacy gate.

## Validation and acceptance criteria

All checks below are **PLANNED / NOT RUN**. Builds, fixtures and emulator results
must be labeled separately from phone evidence. Reuse accepted Phase 9 core evidence;
test changed intake/auth/lifecycle boundaries, not the entire old suite.

| 15A physical acceptance | Required observable result |
|---|---|
| Cold/warm image Share; one/multiple images | Explicit review and existing/new listing choice; no implicit listing/create/upload; received order preserved |
| Exact bytes and identity | Server originals match approved fixture hashes; correct `listing_image_id`, per-entry UUID/position; no re-encoding |
| Unsupported MIME/type, malformed URI, corrupt/oversized data | Per-entry honest refusal; backend decode remains authoritative; no broad permission request |
| Unreadable/revoked provider URI | `SecurityException`/missing stream becomes a failed entry; other files remain usable; explicit re-share if grant gone |
| One file fails; retry | Successful entries remain committed; retry uses same live-queue UUID/bytes/order; maximum two dispatches |
| Exact duplicate and lost upload response | New UUID duplicate and same UUID replay preserve relationship/result/order and expected receipt counts |
| Existing private-source listing, shared original, replay | Restricted canonical original and all applicable thumbnails; no downgrade, guessed provenance or metadata rewrite |
| Interrupted upload/backend unavailable | Pause and show failure/uncertainty; explicit session verification and same-queue retry; no background worker or blind listing-create retry |
| Cancel before Save, sign-out/expiry | No new listing/upload before Save; clear unsaved bytes/URLs and auth-sensitive state; already saved server images remain retained |
| Orientation/activity recreation/process death | No duplicate intake/upload; same-process identity retained; cold process exposes no private draft or automatic replay; authenticated readback/re-share |
| Capture absent/disabled, recognition disabled | Manual upload, Share and direct set search/valuation continue independently |

Physical tests use a supported source app Brian explicitly shares from; this does not
require Facebook. Facebook Share/capture compatibility is claimed only if actually
tested later with approved content and a confirmed installed package.

| 15B physical acceptance | Required observable result |
|---|---|
| Permission grant/cancel/revocation | Understandable grant flow; denied/revoked state stops requests/resources; Share/manual available |
| Secure/invalid/unsupported window | Error/blank protected output refused; no bypass and no upload |
| Rotation | Correct target/dimensions; no stale frame, duplicate capture or automatic next capture |
| Target-app/window change and allowlist refusal | Nonallowlisted/unknown/ambiguous target produces no retained/uploaded frame, including in-flight changes |
| Hidden/disabled controls, Stop, lock, process/service restart | No background frame collection; late callbacks discarded; restart disabled |
| One explicit successful capture if supported | Approved target verified on the phone, one reviewed result; not generalized to all Facebook content |
| Unsupported result | Clean Share/manual fallback; capture and 15C remain unqualified/blocked |

15A GO requires passed physical rows and accepted evidence; any unresolved byte,
receipt/order/privacy/auth/lifecycle defect is STOP / NOT QUALIFIED. 15B GO requires
resolved mechanism gates and actual allowed-target device proof; a documented but
unproven API is insufficient. Unsupported capture may close feasibility with an
honest negative result, but cannot authorize 15C.

## Security, privacy, and data-integrity considerations

Carry forward `docs/IMAGE_PRIVACY_POLICY.md` approved 2026-10-01: owner-only,
no-store originals/thumbnails, immutable while retained, no scheduled image/orphan
deletion, encrypted private backups and no training/export/AI/provider submission.
Screenshots can include seller/profile names/photos, notifications, messages,
locations and unrelated content. Show a visible privacy reminder before Save; Brian
may cancel/re-share a safer image. No crop/redaction promise in this spike.
Source links remain inert; no scraping, credential/network interception or seller automation.

Memory-only unsaved custody introduces no retained Android copy or new automatic
server deletion policy. Approval of this intake design and its resource limits is part
of 15A review. If a durable spool/persistable permission/background upload/crash-resume
becomes necessary, STOP for a new privacy decision; do not substitute it silently.
The privacy-elevation API corrects an actual Phase 15 admission conflict, not retention.

Networking now is inspection only. For 15A, prefer the established authenticated
localhost TEST TLS/ADB-reverse path with isolated approved TEST PostgreSQL/blob
storage and the existing owned harness adapted only as needed for image fixtures.
Confirm current migration/image-store readiness in that separately authorized task.
Do not rerun the old Phase 9 campaign. A production APK using canonical HTTPS is
historically qualified, but this task authorizes no production login/listing writes or
server contact. Any test access beyond the approved USB TEST path needs separate
authenticated network/data approval even if exposure already exists. No bind,
firewall, DNS, Caddy, server or PostgreSQL-port changes to solve testing.

## Failure modes, rollback, and recovery

Keep `received -> reviewed -> destination chosen -> queued -> uploading ->
uploaded/duplicate/failed` states explicit. Cancellation clears only unsaved intake;
canceling a dispatched request may leave a committed result, requiring authoritative
readback, not deletion. Permission loss or process death can require re-share; it
does not justify a silent local copy or retry. Order conflicts remain explicit and
use existing remove/reselect behavior; no automatic position reassignment.

Disable the new Share adapter/capture interface to return to the accepted app's
manual intake/core behavior. A candidate APK rollback uses the exact retained
accepted artifact only under separate install approval. No database rollback or
saved-image deletion is necessary/planned. Saved originals/receipts survive disabling
intake. Diagnose same-scope defects; if a root fix requires new architecture,
migration, rights or custody, stop and present the concrete reviewable change.

## Progress log

- [x] 2026-10-07: Confirmed baseline, empty index, protected preimages and unused 108.
- [x] 2026-10-07: Inspected native project/image contracts and accepted Phase 9/12 paths.
- [x] 2026-10-07: ADB availability only: zero connected devices; unknown release/API/packages retained.
- [x] 2026-10-07: Bounded official Android research; package-enforcement and privacy-admission gaps recorded.
- [x] 2026-10-07: Prepared proposed plan/docs and sanitized 15A-plan/r1 review package.
- [ ] Brian accepts/revises the plan and separately authorizes 15A implementation/device scope.
- [ ] 15A implemented and physically accepted; STOP for review.
- [ ] Separate 15B authorization and mechanism gates resolved; physical feasibility; STOP.
- [ ] Separate 15C scope, only if 15B passes.

## Open questions or physical-device/manual checks

Before 15A: record Android release/API, reconnect the known phone, approve memory
bounds/privacy elevation and explicit candidate build/install/TEST backend scope.
No need to repeat known phone model/package, Phase 9 login/Settings/Watchlist/logout
history or USB reverse details. Actual installed mode/artifact is a future preflight
fact, not inferred from a historical receipt.

Before 15B only: confirm installed target package names and Brian's allowlist,
resolve accessibility suitability or another supported enforced-package design,
and approve the exact permission/visible-control device spike. No assumed
`com.facebook.katana`. Unknown device API may rule out API 34 window capture.

## Official Android API findings — checked 2026-10-07

These are platform capabilities, not Facebook permission or compatibility evidence.

- [Receive shared data](https://developer.android.com/develop/ui/compose/sharing/receive):
  SEND/SEND_MULTIPLE and explicit review. Shared text/links are not image-fetch authority.
- [Sharing a file](https://developer.android.com/training/secure-file-sharing/share-file):
  temporary content-URI read grants; handle task lifetime/revocation without assuming persistence.
- [Media projection](https://developer.android.com/media/grow/media-projection) and
  [manager](https://developer.android.com/reference/android/media/projection/MediaProjectionManager):
  API 21 projection; API 34 single-app selection, per-session consent/token restrictions;
  selected-package enforcement not documented. API 34 resize/visibility callbacks help
  rotation, not package identity. Target 36 must respect current consent and FGS rules.
- [Foreground service types](https://developer.android.com/develop/background-work/services/fgs/service-types#media-projection)
  and [background start restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start):
  mediaProjection service/permissions, consent ordering and background limits;
  target 35+ overlay exemption needs visible overlay; no boot-start projection.
- [AccessibilityService](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService),
  [ServiceInfo](https://developer.android.com/reference/android/accessibilityservice/AccessibilityServiceInfo),
  [WindowInfo](https://developer.android.com/reference/android/view/accessibility/AccessibilityWindowInfo):
  display screenshot API 30 versus window screenshot API 34; screenshot capability,
  user-enabled service, secure/invalid-window errors and interactive-window requirements.
  Event package filters do not enforce screenshot scope; accessibility purpose remains a gate.
- [Overlay type](https://developer.android.com/reference/android/view/WindowManager.LayoutParams#TYPE_APPLICATION_OVERLAY),
  [overlay permission](https://developer.android.com/reference/android/provider/Settings#canDrawOverlays(android.content.Context)),
  [FLAG_SECURE](https://developer.android.com/reference/android/view/WindowManager.LayoutParams#FLAG_SECURE),
  [hide overlays](https://developer.android.com/reference/android/view/Window#setHideOverlayWindows(boolean)):
  API 26 overlay controls, special permission, secure/hidden-window refusal; never bypass protection.

## Outcome and follow-up

Planning result: **READY FOR PHASE 15 PLAN REVIEW**. 15A/15B/15C remain unimplemented;
there is no new build, installed artifact, screenshot, capture or physical qualification.
Sanitized publication is separate from local main; main stays at the accepted baseline,
with planning docs uncommitted and the protected dirty files unchanged/unstaged.
Next separately authorizable milestone is **15A only**, subject to the listed approvals.
