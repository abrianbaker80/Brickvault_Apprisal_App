# CONTENTS PRICING SAMPLE METADATA CORRECTED — READY FOR FINAL REVIEW

Contents now reads sample_count from the stored normalized occurrence_count.
The former adapter-only keys were absent from stored rows. This is the only
application behavior change: no price, request accounting, mapping, normalization,
contract, schema or frontend change. Null stays null; a recorded zero stays zero;
existing display-ineligible evidence remains suppressed.

**Production verified without refreshing prices:** the unchanged signed-in phone UI
now displays sample 5 for whole MINIFIG idea106 (set 21333-1) and sample 1387 for
PART 3001 White 1 (set 10016-1). They match the retained stored observations.
USD 26.78 and USD 0.10, original fetch times, expiry and Used/Sold scope are unchanged.
Both cached observations were still fresh during verification. Other views remain
unrequested. Server totals of 5 and 29249 units were not substituted for occurrences.

**Zero new provider attempts or refresh operations.** Attempts 7→7, observations 6→6,
operations 3→3, contents targets 2→2; existing market rows are unchanged. No Confirm,
Resume, identity discovery, direct adapter or credential probe was invoked.

Six focused synthetic PostgreSQL cases passed in 37.70s: Sold/Stock × positive, null
and zero counts, real persistence/projection, other-view isolation and expiry
suppression. Affected Python lint/format and production-module mypy passed.
Supplemental test-module mypy reports five existing diagnostics, also reproduced
against HEAD with a shadow file; no new typing diagnostic was introduced. No broad
suite, React campaign or web/APK build ran. The existing renderer was verified with
real cached evidence on the physical phone.

Backend **contents-sample-metadata-production-r1** is active on schema
**0020_contents_market_refresh**, Python 3.13.18. Manifest SHA256:
ca6533b25b409c3154383449faba890a1d6a15200d533294cfd49f6a604131ee.
Accepted feature source remains f79e94092d272a050ced989eb1761b34320bdd28. The release
explicitly includes the exact accepted backup-stream amendment plus this metadata
correction. Only contents.py and wheel RECORD changed from the previous wheel.
Existing web assets, dependency locks and APK were retained byte-identically.
Accepted installed APK identity remains
ef4eea9273929525f434fc464e30b81c1ab47ad1ae7b7675354d7b619c9b7db0;
no reinstall or APK rebuild occurred, and no new package-byte check was needed.

Current preflight/deep-health/recovery checks passed using qualifying prior recovery
evidence and retained compatible schema 0020 rollback. The old immutable release
remains intact. Brian was warned before the normal backend switch/restart; activation
and post-switch health passed. Twenty-five data-table fingerprints were unchanged.
No backup, restore rehearsal, schema operation, runtime upgrade or reboot occurred.
Phone left signed in on 10016-1 Contents; owned inspection forwarding removed.

All 22 original pending paths, three protected files, 59 baseline paths, stopped
capture work, private evidence and previous publications are preserved. Plan 112
was appended only; prior bytes are an exact prefix. Correction/tests and accepted
backup amendment/tests remain uncommitted. Main stays at accepted f79e940, index
empty and unpushed. The original feature checkpoint remains accepted.

The part response still does not independently echo color; the reviewed mapping
and saved request specify White 1. Exact rolling-window boundaries remain unspecified.
The corrected backup timeout defect does not establish the historical failure cause.
The r3 live-price result remains accepted; this closes its sample-display limitation
only, not broader contents coverage or economics.

Evidence: [small correction diff](correction.patch), [exact hashes/preservation](hashes-preservation.json),
[focused and deployment checks](verification.json), [backend/amendment identity](backend.json),
[cached UI/server agreement and zero-call accounting](cached-verification.json),
and [Plan 112 addendum](plan112-addendum.md). Reused accepted evidence:
[r2 backup/deployment](../r2/REVIEW.md), [r3 two-target live check](../r3/REVIEW.md).

Only this sanitized r4 package is committed/pushed on astra-response. No credentials,
private account/session identifiers, executable confirmations or raw provider logs
are included. Stopped for final review; no additional refresh or source closeout.
