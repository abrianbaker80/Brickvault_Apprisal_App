# Focused correction validation

All database runs used the existing owned disposable TEST PostgreSQL harness and
synthetic provider. All listed ledgers report no leftovers and preserved volumes.
No credentials, provider payloads or session-bearing logs are included here.

## New evidence

| Check | Actual result |
| --- | --- |
| Before-fix terminal race | Expected failure: `REPLAN_REQUIRED`, 1 failed in 5.73s. Ledger `c0a350b1797c4dabadadedbb4a45ce7f`. |
| First focused run | 8 passed, 1 test-instrumentation failure in 45.91s. Mismatched receipt correctly raised; counter failed to count the raising lookup. Ledger `e7e6211648b14a68908d4a98e8f18057`. |
| Final barrier suite | 5 passed in 26.08s after moving the test counter before lookup. No further service change. Ledger `320983f308ca40fa9295d832d2a90679`. |
| Python checks | Ruff check + format --check on `contents.py` and `test_contents_refresh.py`; strict mypy on `contents.py`: all passed. |
| API-only package | `node scripts/tasks.mjs build:api`: wheel/sdist and independent installed-wheel import/migration/schema checks passed. Receipt `58e7f9f1949b4951be6caa470018bb92`. Service bytes match wheel, sdist and installed file exactly; SHA-256 in inventory. |
| Preservation and patches | 29 unchanged implementation hashes; original 22 pending paths and 59 baseline files excluding the updated plan unchanged; main HEAD/index unchanged. Both patch postimages verified. |

Selected cases in `services/api/tests/integration/test_contents_refresh.py`:

- `test_late_confirmation_replay_after_committed_progress`: five cases (`progressed`,
  `terminal`, `changed-selection`, `mismatched-receipt`, `invalid-signature`). Two barriers
  hold a duplicate after its real absent receipt read. The other request confirms the
  same receipt and advances one/two synthetic provider requests; only then is the
  duplicate released. Reversed occurrence ordering verifies normalized equality.
  Exact retries return the original operation; negative cases retain their errors.
  Each asserts one operation, unchanged full stored status and no replay-created attempt.
- `test_confirmation_drift_without_matching_receipt_still_rejected`: genuine mapping
  drift before confirmation remains rejected with zero operations/attempts.
- Existing `test_confirmation_race_replay_and_changed_selection`.
- Existing `test_mixed_contents_confirm_run_and_cached_evidence` (including terminal replay).
- Existing `test_mapping_drift_stops_confirmation_and_dispatch`.

The last four cases passed in the first focused run and were not repeated after the
test-only counter fix. Thus nine selected cases have passing evidence, not a claim
of one nine-case clean run. Existing pytest/Starlette deprecation warnings remain.

## Explicitly reused evidence

See [immutable r1 validation](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/cf147bf2f4dace1eb352a2e0426cdd9acac46c7d/astra_response/Contents-Pricing/implementation/r1/VALIDATION.md)
and [r1 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/cf147bf2f4dace1eb352a2e0426cdd9acac46c7d/astra_response/Contents-Pricing/implementation/r1/REVIEW.md).
Unchanged r1 request ceilings, migration/grants, financial/evidence, retention, UI/browser,
restart/uncertain-send and whole-set results are reused. The 22 database cases, 122 units
and 22 UI cases were not rerun as a full suite. No web changes/build/browser rerun.
Prior release/device/provider evidence remains historical, not current live qualification.

Package SHA-256 sums refer to published Git blob bytes (LF text), before checkout
line-ending conversions. Patches contain ordinary blank context lines; their required
space prefixes are diff syntax, not whitespace changes in application source.
