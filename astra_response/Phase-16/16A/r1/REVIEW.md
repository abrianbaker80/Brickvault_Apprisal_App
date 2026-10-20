# Phase 16A — actual outcomes implementation

**READY FOR PHASE 16A OUTCOMES IMPLEMENTATION REVIEW — 2026-10-20.**

ChatGPT took over the approved implementation workflow while Brian's Codex allowance
was unavailable. This is source/owned-TEST evidence, not a production release.
Main remains at `6242904bd396eaf1f4ad064e8540f69035527839`, uncommitted and unpushed
for this task, with an empty index. The original 22 pending/protected entries remain
byte-identical; unfinished 15B capture has not been changed, committed or resumed.

## Working slice

The existing saved-deal page now records one purchase's actual acquisition, inspection,
preparation/labor and aggregated resale facts. Unknown amounts are not zero; explicit
None/0 is deliberate. The server calculates gross, net, acquisition, profit and days
when eligible, keeping unpaid own minutes separate from paid labor. Corrections
append new full-state entries; history remains readable. No original forecast is
rewritten or refreshed, and comparisons name the immutable original rather than a
later revision. Missing/unreplayable forecasts suppress comparison, not actual facts.

One additive migration, `0018_deal_outcome_revisions`, creates the append-only owned
table. Three private APIs support latest/history, append, and exact-entry recovery.
Stable submission IDs, expected revisions and a final authenticated write guard
protect retries/concurrent corrections. The runtime has SELECT/column-limited INSERT;
UPDATE/DELETE and populated downgrade are refused. Generated contracts retain every
existing operation/schema unchanged.

The form preserves conflicting drafts for deliberate reload/save, freezes uncertain
submissions until exact-ID recovery and deliberate retry, and clears private state
on session lock. No durable browser draft or offline write queue was added. The
UI uses server results, not duplicated financial arithmetic. Dates are calendar dates;
the before-purchase contradiction check explicitly uses the original UTC date and
operator attestation for same-day order, as disclosed in the form/plan.

## Evidence

- [Exact 21-path inventory](inventory.json) and [reconstructable cumulative patch](implementation.patch).
- [Plan and implementation checkpoint](PLAN.md); original plan history is retained.
- [Focused validation and preservation](validation.json).
- [Append-only service](files/services/api/src/brickvault_api/outcomes.py),
  [versioned calculation](files/services/api/src/brickvault_api/outcome_calculation.py),
  [models](files/services/api/src/brickvault_api/outcome_models.py),
  [API](files/services/api/src/brickvault_api/api/outcomes.py),
  [shared UI](files/apps/web/src/OutcomeSection.tsx).

11 model/calculation cases, six real PostgreSQL/API cases and six React cases passed.
One real Chromium/API/PostgreSQL workflow recorded actual profit 47.00, appended a
correction to 57.00, reopened the original and revised saved-deal pages, and retrieved
the earlier actual outcome. Frozen original/revision rows stayed identical. Desktop
and 320px behavior, explicit writes, no horizontal overflow and no private durable
browser storage passed. No external request was admitted. A select-label issue found
in the initial browser pass was corrected; only that affected fixture and workflow
were repeated. The failed pass and runner-preflight history remain local.

Affected Ruff/format, strict production typing, TypeScript, ESLint and contract checks
passed. All owned database runs, including the failed browser pass, removed the exact
test databases and restored prior TEST service state with no leftovers. Existing
deprecation warnings remain visible. No APK/native, pricing, Share, capture, backup
or physical-device campaign was rerun.

## Limits and next gate

USD-only; one purchase per saved lineage; aggregate sales rather than an order ledger.
Partial sales have no final profit/duration. Comparison remains strictly per-metric;
a changed acquisition basis cannot yield a misleading comparable profit error.
No ROI, dataset exports, training, recognition or source-rights expansion.
Narrow element screenshots retain the existing sticky navigation's overlap at their
capture scroll position; functional controls and no horizontal overflow were checked,
not a redesign of the app shell. No independently delegated review is claimed.

**Production, the phone, deployed APK and market/backup configuration were untouched.**
No source commit or deployment is authorized by this result. Stop for review.
