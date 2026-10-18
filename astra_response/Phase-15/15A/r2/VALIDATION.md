# Actual validation

The unchanged r1 implementation baseline passed 13 backend units, 16 focused
real-PostgreSQL cases, 16 native JUnit tests, contract drift, affected format/lint/type
checks and TEST build inspection. Android lint had zero errors and 19 existing
resource/layout/version warnings. Those accepted focused results were reused.

On 2026-10-18 the stale-notice regression failed before its fix. After the one-field
admission fix, the final focused run passed **25 tests in four files**:
NativeShare (12), NativeShareReview (8), NativeShareSession (1), NativeLifecycle (4).
New cases cover old sign-in notice clearing, overflow notice preservation and
same-batch acknowledgment warning preservation. Targeted ESLint and Prettier pass.
The sanitized final qualification build, frontend verification, Capacitor sync and
offline Gradle assemble pass; all eight built web files match packaged bytes.
The final native/config/public-certificate payload is unchanged from the first
successfully installed TEST package. The installed final APK hash was read back
from the phone and matched the [receipt](apk-receipt.json).

Two test preparation defects were corrected and retained as historical evidence:

1. The original r1 build omitted the retained Android user-directory setting and
   selected another debug key. Android rejected the update without modifying the
   installed app or data. Rebuilding with the retained key corrected the signing
   provenance; no uninstall/data clear bypass was used. Both keystores and the
   exact original APK were preserved.
2. The first ActivityScenario harness lost intent-based lifecycle tracking after
   the consumed Share intent was scrubbed. It failed before calling recreation.
   The repaired harness uses the public lifecycle monitor and Activity.recreate,
   with actual destruction/creation/resume latches. The final physical run passed
   **one instrumentation test**, recording a new Activity/WebView in the same PID.
   This was a harness failure, not an application crash finding.

Physical results and limitations are in [PHYSICAL_DEVICE.md](PHYSICAL_DEVICE.md).
The final read-only source/evidence review found no unresolved material security,
lifecycle, byte-order, identity or retry defect. Documentation verification resolved
481 local targets, including 87 fragments; whitespace checks passed.

All source remains unstaged/uncommitted. No unchanged expensive acceptance campaign,
provider/model call, production test or new catalog/valuation campaign was run.
