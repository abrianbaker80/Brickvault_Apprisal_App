# Phase 16C production deployment — maintenance continuation r3

**PHASE 16C PRODUCTION DEPLOYMENT COMPLETE — READY FOR REVIEW**

Executed November 16 America/Chicago (completion November 17 UTC). This closes the
authorized production rollout only. Accepted source/TEST remains closed; wider Phase 16
remains open. No contents-pricing or other feature work started.

## Final pair and acceptance

- Source: `50f66837addf77ddd1c1a69eed0a873c17163a81` from an isolated clean worktree.
- Active release: `phase16c-outcomes-production-r2`, Python `3.13.18`, schema
  `0019_reviewed_dataset_foundation`.
- Manifest SHA-256: `77106cc2df68812fbe7c9e459d1bb43b85f12e1163b2264a3a55a061d43b834c`.
- Installed APK SHA-256: `959124a7581954eff2860f817e25c03cee2592f1d3b223d73880655be79852d3`.
- Existing signer SHA-256: `e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72`.
- One exact retained fixture changed UNKNOWN → SYNTHETIC through the normal guarded
  phone UI, with one stable submission and exact-ID recovery/readback evidence retained
  privately. No new deal or outcome was created. It is excluded from all REAL metrics.
- Phone report/history/reopen/search checks passed. There is one SYNTHETIC record and
  zero eligible REAL records; empty financial totals remain unknown, not fabricated zero.
  Original forecast bytes and outcome history are unchanged. No provider attempts were added.
- Same-signer APK update preserved UID/first-install identity and app data. Brian signed
  in locally. No password, cookies or CSRF values were read. The task-owned forward is
  removed and original forwarding state restored; the new app remains installed and signed in.
- Final server: 14/14 ordinary health checks, zero failed units, kernel
  `6.8.0-149-generic`, no reboot-required marker, healthy mount/PostgreSQL/API/HTTPS/timers.

Evidence: [release](release.json), [activation](activation.json), [APK](apk.json),
[bounded acceptance](acceptance.json).

## Maintenance and recovery

Exact inventory found two new unmatched database snapshots, one each from the failed
November 1 and November 6 10:00 UTC runs, on Proxmox only. Each dump was 768,667,487
bytes; stream hash/size, database marker, production owner and schema 0018 attribution
passed. Neither run had Drive artifacts or a successful receipt. Relevant journals
confirmed failures. The deployed retention implementation matched the accepted source.
This was additional incomplete history, distinct from the earlier accounted October run.

Recorded only those two evidence-backed failures in the existing protected partial-run
ledger under the shared lock. They remain ineligible as successful recovery points.
Read-only retention PLAN passed. All snapshots, receipts and permanent pins were
preserved; no deletion, forget/prune, APPLY, policy change or unknown-history exemption
occurred. The logs retain only a generic failure, so the underlying transport cause and
any recurring trigger remain unestablished. No causal explanation is invented.

Reused the complete November 16 10:11:42 UTC schema-3/0018 backup after all eight artifact
readbacks, both repository integrity checks and an additional configuration archive
readback proving current market-credential inclusion/identity. The established migration
guard then performed its required fresh eight readbacks and two checks before mutation.
No duplicate backup, restore rehearsal or production restore occurred. Backup schedule
remains 04:00 America/Chicago and configured credentials are unchanged.

Verified [Python 3.13.18 official release](https://www.python.org/downloads/release/python-31318/)
source SHA-256 `abb0102e6d4ae027509bcb82327d9dd85515b44a3ba8ad538cfc5e9847029f68`
and the established Thomas Wouters signing key. The optimized side-by-side build,
standard-library probes, locked-dependency checks and service-user 0018 compatibility
passed. Runtime maintenance used a separately identified immutable release whose
application files were byte-identical to the prior release. Python 3.13.16 and that
release remain retained; system Python is unchanged. One controlled VM115-only reboot
activated already-installed updates. No host/other guest work or OS release upgrade occurred.
Stale failed-unit state was cleared only after the underlying conditions passed.

The initial attribution-reader harness had an early-pipe-exit cleanup defect and a wrong
owner assertion. Task-owned readers were identified and stopped gracefully, the harness
was corrected, and normal attribution/recovery verification then passed. No forced
repository unlock or production process termination was used. This inspection defect
is separate from the historical backup failures. [Maintenance evidence](maintenance.json)
retains the distinctions and actual verification results.

## Deployment and compatibility

One normal backend/web build and one matching production APK were produced from the
accepted source. The first release materialization had a Windows CRLF certificate hook;
the final r2 package binds exact accepted Git LF hook bytes under a distinct manifest.
The r1 materialization is retained and was not deployed. No application source changes
or unrelated dependency upgrades were made. Production origins, system-only certificate
trust, matching web assets, existing signer, report/share inclusion and capture exclusion
were checked. No TEST trust, embedded credentials or unfinished capture code was included.

Staged files and imports were verified before activation. Existing 0019 ran through the
guarded owner transaction with enumerated grants, retaining all original table counts,
forecast payloads and outcomes. Runtime grants allow subject read/append and deny
update/delete/truncate. Image-inclusive backup format, configured credential selection,
release health and unchanged schedule passed after activation.

Recovery before any classification write permitted only the existing empty-0019 guarded
downgrade to the retained compatible maintenance release. The successful SYNTHETIC append
now populates 0019: retain the current compatible runtime/history. Do not downgrade,
switch an 0018 runtime onto it, delete history or restore over newer records. No recovery
action was necessary. The old APK and recovery artifacts remain privately retained.

## Preservation, scope and review boundary

[Preservation](preservation.json) verifies all 43 original file hashes, including pending,
protected, stopped capture and untracked review work. Main remains at the accepted SHA,
with an empty index and no source commit or main push. Only the additive
[Plan 111 record](plan111-addition.patch) changed tracked main content for this continuation;
it remains uncommitted. Only this sanitized package is committed/pushed to astra-response.
Earlier r1/r2 publications remain intact.

Accepted source/TEST, REAL aggregation cases and recovery qualification were reused;
no broad campaigns or device lifecycle matrix were repeated. No provider/AI call,
market refresh, dataset CLI, production dataset preparation/export, real corpus,
training or new fixture work occurred. This bounded phone workflow is not broader
capture/recognition or full-original-specification qualification. CONTENTS PRICING
remains the next planning recommendation only.
