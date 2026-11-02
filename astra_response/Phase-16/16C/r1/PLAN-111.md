# ExecPlan 111 — Phase 16C actual-outcomes reporting

**Status: IMPLEMENTED — READY FOR PHASE 16C OUTCOMES REPORT IMPLEMENTATION REVIEW.**
Baseline: local `main` `e0deef0ba065d19377525a1ba36fc436ee254e6c`;
16A source/production and 16B fixture-only source/TEST are accepted and closed.
Brian approved the grouped decisions and bounded source/TEST slice on 2026-11-02.
Implementation and this plan remain uncommitted on local `main`; only the
sanitized review package is published on `astra-response`.
The [16B closeout](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f8d52dccd005af113fa92eec74c9b30ac7a1a119/astra_response/Phase-16/16B/r3/REVIEW.md),
`docs/plans/109-phase-16a-actual-outcomes.md` and
`docs/plans/110-phase-16b-reviewed-datasets.md` preserve their evidence. This plan
does not reopen them. Capture remains stopped; wider Phase 16 remains open.

## 1. Goal and user-visible outcome

Add one small private outcomes report to the existing shared `/deals` experience.
Brian can see real unsold/partially sold purchases, completed sales with known
financial amounts, missing information, and not-bought decisions; follow each row
to its saved deal and outcome history; and explicitly classify a saved original as
REAL, SYNTHETIC, EXCLUDED or UNKNOWN. Separate counts expose synthetic, excluded and
unknown subjects without contaminating real-performance totals. This is one React
UI and one API, not a new valuation engine or dashboard.

## 2. Why now

16A already records full-state outcomes and comparisons; 16B already supplies a
durable subject ledger. The retained 16A synthetic smoke deal was visibly labeled;
its ledger registration is not established by accepted evidence or verified now.
A report that assumes unclassified records are real would misstate actual results.
Classification is an explicit owner
decision, independent of image review, dataset rights and training eligibility.

## 3. Scope

- Aggregate all owned, saved original forecast roots once, using the greatest
  outcome revision and greatest subject revision for each root, in a consistent
  database snapshot. Forecast revisions and outcome corrections do not add deals.
- Offer classification for each root and a concise current-state report, including
  missing fields, metric-specific denominators, exclusions and deal/history links.
- Reuse stored versioned actuals, results and original-forecast comparisons from
  16A; use the 16B subject revision ledger and its authentication/integrity rules.
- Plan a later separately authorized exact-ID registration of the 16A smoke root,
  from accepted private evidence. No production identification or write is part
  of this plan or automatically authorized by its acceptance.

## 4. Explicit non-goals

No backfill, bulk auto-classification, note-text matching as identity evidence,
provider calls, schema change by default, current market refresh, new ROI,
composite score, per-order accounting, export, image review, dataset preparation,
training, capture, or production/phone operation. No new final profit for partial
sales and no broader Phase 16 completion claim. No dependencies are proposed.

## 5. Current repository state and reuse

- `services/api/src/brickvault_api/outcomes.py`, `outcome_models.py` and
  `outcome_calculation.py` store full actuals and authoritative versioned derived
  results, per-metric comparison state/reasons and exact signed errors. Use stored
  results, not revaluation against current evidence. `api/outcomes.py` already
  provides owned outcome/history reads and write conflict/replay conventions.
- `forecasts.py` and `api/forecasts.py` implement owned saved roots/revisions;
  the `/deals` index is paginated, so its current page is not a report denominator.
  `apps/web/src/DealsPage.tsx`, `HistoricalForecastPage.tsx`, `OutcomeSection.tsx`,
  `outcome-api.ts`, and `navigation` provide the existing UI and link patterns.
- `datasets/models.py` `SubjectReview` and `datasets/service.py` `subject()` use
  UUID submissions, expected revisions, reasons, safe evidence-reference keys,
  replay hashing, owner checks and sticky SYNTHETIC. Migration
  `0019_reviewed_dataset_foundation` already accepts exactly one owned saved
  original root or listing per revision and guards append-only history, sessions,
  consecutive revisions and synthetic stickiness. Absent a row means UNKNOWN.
- The current dataset service requires a BlobStore and its subject operation calls
  release invalidation; its CLI is explicitly TEST/fixture-only. Do not expose that
  CLI or enable production dataset operations. Extract a shared root-only subject
  read/append path without a BlobStore, preserving listing-subject withdrawal and
  any applicable invalidation semantics. Verify root-only changes cannot affect
  a release under the existing data model before omitting image/release calls.
- The image graph currently loads subject revisions before ignoring root-only rows,
  under a bounded collection. Filter that graph query to `listing_id IS NOT NULL`
  in SQL so accumulated root classifications cannot exhaust its cap; retain all
  listing history and conservative graph edges. Add a focused regression.

## 6. Decisions, classification and assumptions

The following are a single recommended design for Brian's review, not decisions
already approved for implementation:

1. **Cohort and dates.** Default to all saved roots. Optional inclusive from/to
   calendar dates filter the UTC date of the immutable original's `saved_at`, not
   purchase, sale, or correction date. This includes not-bought and no-outcome
   roots consistently. Display that this is a saved-deal cohort with **current
   latest state**, not a period-of-sales report or historical as-of snapshot;
   later corrections/classifications can change a past cohort's results. Show
   count outside date range separately. Invalid dates/ranges are rejected.
2. **Real admission.** Only the latest explicit REAL classification enters real
   performance; a missing row or explicit UNKNOWN is UNKNOWN. SYNTHETIC and
   EXCLUDED stay outside every real subtotal. Show separate counts and actionable
   lists, including those with no outcome. A root's classification is not inferred
   from notes, outcomes, image review, or an assumption that a purchase happened.
3. **Owner workflow.** A classification control on each report row and saved deal
   shows current class and revision, explains its reporting effect, requests an
   explicit class, concise reason and opaque evidence-reference key compatible
   with `SubjectReview`, and submits a client-generated UUID plus expected
   revision. Explain SYNTHETIC is permanent under the existing guard. Read back
   after success; on conflict reload and require a deliberate new decision. For an
   uncertain response use the identical ID and payload for safe recovery/replay,
   never silently send a new append. Show classification history read-only without
   exposing private evidence content. Do not put sensitive text in logs or URLs.
4. **Retained smoke.** After separate authorization, locate its exact original
   root ID using the accepted private 16A evidence, independently confirm ownership
   and identity, append SYNTHETIC with the ordinary guarded workflow, and verify
   exact-ID readback and exclusion. Do not publish the private ID/evidence. Before
   then it stays UNKNOWN unless an existing explicit classification says otherwise.

## 7. Report, data model and interface

### Report rules

For the selected cohort, first report total roots and mutually exclusive class
counts. Within REAL, group latest outcome as NOT_RECORDED, NOT_BOUGHT, BOUGHT /
NOT_SOLD, BOUGHT / PARTIALLY_SOLD, or BOUGHT / COMPLETE. Surface each row's
`results.missing_fields`, metric reasons and date/channel omissions; an incomplete
record may overlap its status group and is visibly labeled as such. No outcome is
missing information, not a not-bought decision. Allow classification of every row.
Show an explicit empty state when no roots qualify.

Show minimally: count of unsold and partial purchases, known acquisition totals
for those purchases, observed partial gross receipts to date separately, and for
completed sales known gross, net and profit totals plus count of sales with known
profit. Determine monetary eligibility independently from each stored result
amount: a COMPLETE sale can have known profit while its overall state is INCOMPLETE
(for example, missing channel). No incomplete amount becomes zero; a known zero
is valid. Return no numeric total when zero values are eligible. Preserve negative
net and profit. Actual profit is after recorded monetary costs with unpaid own
labor excluded; show separately the known paid labor amounts and unpaid minutes,
never convert minutes to wages. Partial receipts are cumulative to date, not final
profit, and must not enter completed-sale totals. Amounts are USD, exact decimal
on the server, formatted only at display. Do not aggregate incompatible currencies
if future data differ; report unavailable/excluded instead.

Each displayed subtotal, including labor and comparison statistics, carries the
eligible population, included count, missing/noncomparable count and classification
excluded count (and out-of-date-cohort count separately). Specify mutually exclusive
reasons so counts reconcile; give overlapping diagnostic reasons separately. A
known-only subtotal with any missing eligible values is labeled **partial**, and
none implies complete profitability. Counts state their denominator, including
classification counts and no-outcome roots. List details remain linked to the
root forecast and its existing outcome history; never expose another owner's roots.

For each sale, net and profit comparison independently, use only the latest
stored 16A `COMPARABLE` result against the immutable ORIGINAL and its exact signed
`error_exact` (actual minus original). Split `SELECTED_MARKET` sold-based forecasts
and `MANUAL` assumption comparisons; exclude STOCK active-listing what-if, missing
original, and NONCOMPARABLE/UNAVAILABLE results from numeric comparison. Show
eligible/comparable and excluded-by-reason counts for each basis/metric. Count
unknown or unavailable basis in a separate unassigned-basis bucket, never guess
market or manual; reconcile these buckets to all real cohort candidates. When
at least one comparison exists, show the signed mean error calculated from exact
errors, then rounded for display. State that signed mean can cancel over/under estimates and
is not a confidence or accuracy score. Profit additionally inherits 16A's matching
acquisition-basis gate; there is no time-to-sell forecast error. No new comparison
rules, evidence or current-data recomputation.

### Concrete proposed changes

- No new table or migration is expected. Reuse 0019 `dataset_subject_revision`;
  never add a parallel `is_real` flag. Preserve its database trigger, authorization
  transaction settings, request hash/replay, owner check, expected-revision CAS,
  sticky rule, and append-only grants. If implementation discovers a necessary
  new migration, stop for the separately required decision rather than improvise.
- Add a small report service and Pydantic response models alongside existing
  `outcomes.py`/`outcome_models.py`; add an authenticated no-store
  `GET /api/deal-outcomes/report?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD` with
  summary plus root-level rows. Query all owner roots with latest subject/outcome
  using one consistent snapshot, not the existing paginated forecast index. Return
  100 rows per page ordered by original `saved_at` descending then root UUID;
  compute totals over the entire cohort on every request. Include an opaque snapshot
  fingerprint of the filter/version and all owned ordered root IDs with latest
  outcome and classification revision identities, including roots outside the date
  range because their count is displayed. Subsequent page requests send that fingerprint;
  if a root, outcome or classification changed, return a typed conflict and require
  a restart, rather than combining pages from different states. No leaking owner
  IDs, notes or evidence references. Fail clearly
  rather than return silently partial totals if reads or stored data are invalid.
- Add root-scoped authenticated `GET` and CSRF-protected `POST`
  `/api/deal-forecasts/{identifier}/classification`; resolve owned saved revision
  to original as existing outcomes do. GET returns current class, revision and
  read-only history; POST accepts compatible id, expected revision, classification,
  reason and evidence reference, and implements same-ID replay, conflict, sticky
  synthetic and non-disclosing 404. Establish the existing 0019 transaction-local
  session settings with the real owner auth flow. Do not add image or dataset
  export routes. Reuse/refactor shared subject code without weakening existing CLI
  and listing invalidation. API tests must cover both paths.
- Regenerate OpenAPI/TypeScript in `packages/contracts` and use the generated
  client. Add a compact outcomes section and filters to `DealsPage.tsx`, a small
  classification control reusable on `HistoricalForecastPage.tsx`, report API
  client and responsive styles. Link to the existing saved-root page and its
  `OutcomeSection` history, adding a stable history anchor if needed. Do not
  calculate money, comparison or cohort aggregation in React. Preserve forecast
  rendering if this separate report/classification request is unavailable.

## 8. Implementation record

The approved slice uses the existing `0019_reviewed_dataset_foundation`; no
migration, dependency, parallel classification flag or BlobStore was added. A
shared root-only subject path now uses the existing owner, auth, replay, expected
revision, append-only and sticky-SYNTHETIC guards. Listing-subject withdrawal
behavior is retained, and the listing graph's bounded history query excludes
root-only rows in SQL.

The report service reads each owned original root with its latest outcome and
classification from a consistent snapshot, uses stored versioned calculations
and original comparison results, and returns cohort-wide exact-decimal metrics
plus paged root rows and a restart-on-change fingerprint. Authenticated,
no-store report and root-scoped classification routes use the existing API
contracts. OpenAPI and TypeScript were generated. The `/deals` report and shared
explicit classifier link back to saved-deal outcome history and handle conflicts,
readback, unavailable reports, session locking and narrow layouts.

The implementation stops at local source/TEST review. Production rollout,
deployment of 0019, exact-ID smoke registration, real-corpus work, exports,
training, provider calls and physical-device qualification remain unauthorized.

## 9. Focused validation and acceptance

Use synthetic owned local TEST data. Run affected formatter/linter/type checks,
contract generation/consistency and relevant build; run targeted unit, PostgreSQL
integration and UI checks once stable. Acceptance must demonstrate:

- Multiple forecast revisions and outcome corrections count one root with latest
  outcome/class; owner isolation, consistent snapshot and totals spanning pages;
  pagination restart on an intervening cohort or classification change; default/all
  and inclusive date boundaries, not-bought/no-outcome cohort handling.
- Explicit UNKNOWN, missing class, REAL, EXCLUDED and sticky SYNTHETIC; protected
  cross-owner/unsaved/revision cases, concurrent CAS, same-ID replay, conflicts,
  auth/CSRF, no-store and correct recovery; listing review/invalidation unchanged,
  and many root revisions do not consume the listing graph's bounded history cap.
- Missing vs known zero, negative net/profit, partial receipts without profit,
  separate paid labor/minutes, completed financial amount with missing nonfinancial
  fields, no-values case, counts/reconciliation and visible partial labels.
- Per-metric original comparison eligibility, manual vs market separation, STOCK,
  noncomparable/unavailable exclusions, original acquisition mismatch, exact error
  precision, unassigned basis and denominator/count accuracy; forecast bytes and append-only history
  unchanged by reads and classification; existing immutable guards still apply.
- One synthetic desktop and narrow viewport flow: classify, report, open a deal and
  history, inspect missing information and recover a conflict. Distinguish synthetic
  UI evidence from physical Android or production evidence. No broad qualification
  campaign, real corpus, device, provider or live production calls are implied.

**Observed validation — 2026-11-02.** Contracts consistency, TypeScript, ESLint,
Prettier, Ruff and MyPy checks passed. `node scripts/tasks.mjs build` passed the
API wheel/sdist checks and normal Vite production build. Five focused tests passed
against owned disposable TEST PostgreSQL: three report/classification integration
tests, the listing-graph regression, and one Chromium desktop/320px workflow. The
browser flow verified explicit classification, conflict/reload, readback, missing
information, saved-deal history, date filtering, no browser storage and no blocked
provider request. The runner reported no leftovers. No broad suite or smoke
registration was run.

Reuse the accepted 16A stored outcome/comparison rules and the 16B 0019 subject
ledger and append-only safeguards; neither prior phase was requalified here.

## 10. Security, privacy and integrity

Scope every read/write to authenticated owner; use existing runtime role, auth,
CSRF, database ownership and 0019 trigger/session guards. Use no-store responses,
bounded strict inputs and redacted fixed error codes. Preserve forecasts, full
outcome history and classifications immutably; do not expose hidden owner existence
or credentials. Classification confers no source, display, export or training rights.
Do not require image state or grant production dataset access for this report.

## 11. Failure, rollout and recovery

Last recorded 16A production was on 0018; that is historical evidence, not a
current production read. Local 0019 is accepted only for fixture source/TEST;
the accepted closeout does not record a production deployment. Any later rollout
needs its own reviewed deployment request:
preflight actual schema, 0019 migration and runtime privileges/session settings,
backup/restore inventory and exact-head/health compatibility, application release,
and recovery preserving both outcome and new subject history. 0019 downgrade
refuses populated dataset records; do not delete history to force rollback. A
production report must not silently substitute UNKNOWN for a missing 0019 table:
return an unavailable state. Linux dataset materialization qualification is a
separate dataset gate, not inherently required to report or classify a deal.

## 12. Progress log

- [x] 2026-11-01: Read requested local baseline, final 16A/16B dispositions,
  Prompt 16 and relevant source contracts. Draft one plan; no tests, builds,
  production reads, services, provider calls, backfills or implementation.
- [x] 2026-11-02: Brian approved the grouped decisions and bounded source/TEST
  implementation; no separate planning revision was required.
- [x] 2026-11-02: Implemented the approved slice and passed the focused checks
  recorded in Section 9. Local source and Plan 111 remain uncommitted/unstaged.
- [ ] Separately decide production rollout and exact-ID smoke classification.

## 13. Open decisions and later checks

Review together: (1) saved-date cohort semantics and displayed metric set;
(2) explicit classification and permanent synthetic safeguard, including safe
evidence references; (3) per-metric comparison and partial subtotal labels; and
(4) acceptance and later distinct 0019 deployment/smoke-registration gates.
No physical-device verification is claimed or required for this source/TEST plan.

Wider Phase 16 remains open: permitted real-source corpus and rights/privacy/label
review, reproducible sanitized releases and connected-source splits in their real
context, Linux materialization qualification, remaining recognition hardening and
recovery/receipt regression as applicable, and any richer verified-contents model
remain separately scoped. 15B capture remains stopped/unqualified and 15C unstarted.

## 14. Outcome and stop condition

The bounded Phase 16C implementation is ready for implementation review. Publish
only the sanitized review package on `astra-response`, leave source and this plan
uncommitted/unstaged on local `main`, and stop for review. Do not deploy, classify
the retained production smoke record, close wider Phase 16 or begin another slice.
