# 15A production continuation — 2026-10-19

**SHARE-ONLY PRODUCTION DEPLOYMENT COMPLETE — READY FOR REVIEW**
All three maintenance blockers are resolved. The accepted Share-only application
is available in production; its matching production APK remains installed, signed
in and usable. The single two-image physical production integration workflow passed.

Current release: `phase15a-share-production-r2`, database `0017_listing_images`.
Manifest SHA-256: `24d90a375ba4f099c84a7770aa3dfa06335a38e9e9d3d28975464680112d2099`.
Installed APK SHA-256: `724f5da86fad1dbf3fa0c7cbb5ace022e02115b84f96427d4f40f932f773efbc`.
Signer: `e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72`.
Exact application source remains `e3c04d90b1646b9b9dad73325bf1491fb8326943`.
The distinct operational amendment and canonical Linux hook packaging have their
own manifest/source identities in [identities](identities.json).

## Maintenance and recovery

All seven October 13 snapshots belong to one failed production backup invocation.
Both configuration archives match the production ownership marker/database and
captured release. The three common artifacts have identical bytes across repositories.
Proxmox has database.dump, globals.sql, configuration.tar and image-blobs.tar;
Drive has the first three and lacks image-blobs.tar. No complete success receipt
exists for that run. Its original low-level transfer error is not available from
the historical generic service log and is not guessed.

The minimal [operational patch](operations/retention-ledger-v2.patch) extends the
existing backed-up retention ledger to version 2. It records a verified FAILED_INCOMPLETE
disposition bound to exact snapshot metadata/content hashes, ownership and repositories.
Those snapshots remain retained and excluded from successful recovery/retention
eligibility. Unknown history, changed evidence, successful-run overlap and pin/receipt
tampering still fail. Original receipts, pins and ledger fields remain unchanged.
No snapshot deletion, forget/prune, pin removal, fabricated success or backdating.
Seven [focused fixtures](operations/test_partial_backup_history.py), one existing
partial-receipt refusal fixture, Ruff static checks and formatting pass. No accepted
15A qualification campaign was repeated. [Reconciliation receipt](backup-reconciliation.json).

The existing October 19 09:07:19 UTC schema-3 database-plus-blob recovery point was
verified through the supported verifier: all eight artifact streams matched their
sizes/hashes and both encrypted repository checks passed. Receipt bytes stayed exact.
The same fresh, ownership/schema-matched point was reused. No additional backup,
live-data restore or disaster-recovery rehearsal. [Verification](recovery-verification.json).

[Python 3.13.16 official source](https://www.python.org/downloads/release/python-31316/)
passed the published SHA-256 and retained release-manager GPG-key verification.
It was built/installed alongside 3.13.15; Ubuntu's Python and prior immutable
releases remain. Locked replacement environments passed imports/dependency checks.
One graceful reboot of **VM115 only** activated `6.8.0-147-generic`; no reboot is pending.
Installed light/deep/Python checks pass, the non-destructive retention plan passes,
and no units are failed. [Runtime/kernel receipt](runtime-kernel.json).

## Deployment and phone state

The application wheel/web were built from isolated accepted source, with retained
absolute Android signing/cache paths. A long Windows build path was corrected by
using a shorter clean worktree, without source edits. One production APK was built.
Its Share filters/plugin are present; application-owned capture code/UI/services
and permissions are absent. Production API/WebView origins and system-only trust
are verified; no TEST certificate/API, ADB reverse or native HTTP/cookie bypass.

The first immutable Share artifact failed the certificate-hook byte check because
Windows checkout CRLF entered the POSIX executable. Durable inspection proved all
other manifest bytes/runtime identities valid. A new immutable r2 packages that
hook from the exact accepted canonical Git LF bytes, matching the installed hook.
The first artifact/failure evidence remain; application wheel/web/APK were not rebuilt
or changed for this correction. Readiness now waits for HTTPS before the startup
probes. No health requirement was weakened. [Deployment receipts](deployment-receipts.json).

The same-signer/code-1 APK was installed with `adb install -r`. Installed bytes match;
UID/first-install identity and app data are preserved. No uninstall, data clear,
forced downgrade or signing-key replacement. [Phone receipt](phone-installation.json).

Brian confirmed local sign-in, then normal set search for 10350 passed. Samsung
My Files sent exactly two harmless task-owned images through the ordinary Android
Sharesheet to BrickVault. Both native originals and decoded review previews matched
the selected order. The new synthetic Marketplace Listing destination was explicit,
and Save was clicked once: one listing and two uploads returned HTTP 201.

Authenticated original-content readbacks matched both fixture SHA-256 hashes and
byte lengths. All four original/thumbnail content responses returned `no-store`.
Read-only admin joins verified restricted originals and thumbnails, positions 0/1,
client UUID/content-hash/receipt-to-listing-image identities and thumbnail-v1 lineage.
After clearing only the live Share queue, the saved listing reopened from Marketplace
Listings with both decoded images in order. The clearly labeled synthetic record is
retained under the approved policy; no persisted data was deleted. Final counts are
2 listings / 5 listing images / 5 receipts, exactly the expected smoke deltas.
The two task-owned phone fixtures and inspection forward were removed. The new
production APK stays installed and signed in. [Smoke receipt](production-smoke.json).

One initial read-only evidence assertion incorrectly required an extra `private`
cache directive. The accepted contract requires exactly `no-store`, which all four
live responses supplied. The local checker was corrected; no application change,
repeat Save/upload, maintenance or build followed.

The healthy rollback pair is `phase13c-runtime-ops-r1` plus the retained prior
production APK `045210d0…1ddd2`; it preserves the corrected operational ledger/runtime.
No rollback was needed. Any application rollback must preserve newer database data
and elevated privacy, without database restoration.

API/Caddy/PostgreSQL and all required timers are normal, with zero failed units.
The 04:00 America/Chicago backup schedule is unchanged. Task-owned worktrees,
transfer archives and completed compiler tree are cleaned; release/recovery/failure
evidence and signed source archives remain. [Final state](final-state.json).
Original 22 dirty/untracked paths and 387 private evidence files are preserved;
only one additive Plan 108 section and the separately authorized operational source/
fixture changes are task-owned. Main is unpushed; its index is empty and all main
work remains uncommitted. [Preservation](preservation-validation.json).

15A Share is production available. Accepted [15A physical TEST evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/335b76098acc4c9130a3b8b8120b770b207781e8/astra_response/Phase-15/15A/r2/REVIEW.md)
was reused; no lifecycle/permission/fault campaign was repeated. 15B capture remains
excluded, partial/unqualified, preserved and not resumed. 15C is not started. Set
10350's prior missing market values remain separate; no pricing/recognition/provider
investigation was performed. No operational failure remains unresolved.
