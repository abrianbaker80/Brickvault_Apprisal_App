# Phase 15A physical TEST review — r2

**READY FOR PHASE 15A REVIEW — 2026-10-18. Acceptance remains pending.**

The approved Share implementation now has physical TEST evidence on Brian's
Samsung SM-S948U, Android 17/API 37. Actual Samsung My Files cold/warm single and
multiple-image Shares reached explicit review and existing/new listing choices.
Restricted storage, partial failure, exact bytes, duplicate/replay, real URI
revocation, native Activity recreation, rotation, process death and auth clearing
were checked against an isolated owned HTTPS/PostgreSQL TEST backend.

Final installed TEST APK SHA-256:
`fcc37bfe0acaabe2fcc1f5c9c3d9faae6c00227e4dc3cac2c857ff518fb22c9c`.
It remains installed, signed out and stopped after cleanup. Restoring the prior
production APK requires the separate install approval recorded in Plan 108.

The exact seven-file planning checkpoint remains local main
`5b029368e0bf8f810deb2a305aa1a03cff5c5c95`. The 31 implementation/document paths
remain uncommitted and unstaged; main remains unpushed. Protected dirty files
remain byte-identical. This publication contains sanitized review evidence only.
[The original r1 source review](../r1/REVIEW.md) remains immutable at
`007a613c970bd394ad52d1d931f02a540179b643`.

- [Physical methods, results and limits](PHYSICAL_DEVICE.md)
- [Focused validation and fixes](VALIDATION.md)
- [Implementation scope](IMPLEMENTATION.md)
- [Machine-readable physical evidence](physical-device-evidence.json)
- [Exact 31-path inventory](inventory.json) and [cumulative patch](implementation.patch)
- [Planning checkpoint](planning-checkpoint.json) and [final APK receipt](apk-receipt.json)
- [Cleanup receipt](evidence/cleanup.json)
- [Publication checks and content digests](review-checks.json)
- [Test harness boundaries and sources](HARNESSES.md)

One device-discovered frontend defect was corrected: an old sign-in notice could
remain after a successful re-share. The fix clears that old notice only when
admitting a new batch. Its three regression cases and the final physical check pass.
The final focused frontend run passed 25 tests in four files. Unchanged backend,
PostgreSQL, native and contract results from r1 remain applicable.

No Facebook compatibility, capture, recognition/provider activity, production
contact or new core valuation campaign is claimed. Accepted Phase 9 core evidence
is reused; fresh TEST catalog unavailability and elapsed-expiry limits are explicit
in the physical report. No 15B or 15C work is authorized or started.
