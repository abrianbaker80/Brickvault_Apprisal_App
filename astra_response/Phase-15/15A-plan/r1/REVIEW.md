# Phase 15 — 15A plan/preflight review r1

**READY FOR PHASE 15 PLAN REVIEW — 2026-10-07.**
**Implementation NOT STARTED / NOT AUTHORIZED.** Phase 14 remains CLOSED;
production recognition NOT QUALIFIED; image-driven retrieval DEFERRED / UNRESOLVED.

Local baseline: `e9c7d1f14ccfdf8784a9d4402a2fc0641184dab9`,
`Close Phase 14 recognition quality spike`. Accepted Phase 14 publication:
`508e27ee36b60c4e645da5b4f911304da32fb4ff`; previous review trees are preserved.
This publication commits sanitized planning documents only on `astra-response`.
Main remains at its accepted local baseline, unstaged and unpushed.

## Review contents

- [Proposed Plan 108](files/docs/plans/108-phase-15-android-share-capture.md)
- [Native architecture and Share design](architecture-and-share.md)
- [Device/preflight, capture, privacy and networking gates](device-and-gates.md)
- [Dated official Android findings](android-api-findings.md)
- [Exact changed-file inventory](changed-files.md)
- [Documentation checks and preserved state](validation.md)
- [Planning patch](planning.patch)

The first implementation request would authorize **15A only**: image-only Android
Share into the existing Capacitor app, explicit existing/new optional listing choice,
reuse of the Phase 13 queue/API, and restricted-privacy elevation on that existing API.
No database migration or second protocol/model. Share items keep exact bytes,
per-file UUID/order, independent failure/retry and authoritative receipt identity.
Proposed ingress limits are eight entries / 50 MiB aggregate / 25 MiB each; memory only.

Physical acceptance must cover one/multiple cold/warm shares, existing/new listing
choice, exact originals, partial failure/retry, duplicate/receipt replay, restricted
privacy, bad/revoked URI/MIME, cancel, auth/backend failures and lifecycle/restart.
No source, fixture, emulator or APK result may substitute for that phone evidence.
No connected ADB device was available now: Android release/API and Facebook packages
are unknown preflight inputs, not plan blockers. Known phone is Galaxy S26 Ultra
(`SM_S948U`); known BrickVault package is `com.abrianbaker.brickvault.appraisal`.

**15B is separate and currently gated at mechanism selection.** API 34 accessibility
window capture is a candidate only after suitability and target-window enforcement
review. MediaProjection alone does not establish the required package allowlist.
An overlay is a visible control, not proof of capture scope or Facebook compatibility.
15B needs accepted 15A phone proof plus separate package/permission/device approval.
15C later polish stays blocked until 15B physically passes and is separately authorized.

The approved Phase 13 retention policy is unchanged. Unknown Share pixels and captures
must be restricted even when the destination listing has photo-source metadata.
The proposed optional `privacy_elevation=restricted` corrects that real admission gap,
including duplicates/replays. No automatic deletion, AI submission or export. Durable
phone spool/crash-resume, if requested later, needs a new privacy decision.

The historical Phase 9 USB TEST TLS path remains the preferred scoped qualification
path. Newer accepted Phase 12 evidence also records production HTTPS Android access;
current installed mode is unverified. Neither history authorizes production contact,
listing writes or network changes in this task. Broader testing access needs approval.

STOP for plan review. No implementation, install, build, service, database, provider,
recognition/browser/device UI or capture qualification occurred. Only sanitized ADB
availability discovery, repository/docs inspection and official Android research ran.
The three protected dirty files remain byte-identical and unstaged.
