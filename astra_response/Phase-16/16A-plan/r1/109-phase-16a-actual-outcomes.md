# ExecPlan 109 — Phase 16A actual purchase/resale outcomes

**2026-10-19 — READY FOR PHASE 16A OUTCOMES PLAN REVIEW. Planning only;
implementation requires Brian's separate approval.**

## 1. Goal and user-visible outcome

Add one **Actual outcome** section to an existing saved-deal detail page. Brian can
record bought/not bought, acquisition, inspected contents, preparation costs and
resale totals; see server-calculated actual net/profit and days to sell when known;
and correct an entry while retaining its earlier versions. The original forecast
remains separately labeled and unchanged.

## 2. Why now

Brian resumed this independent outcomes slice after accepting market access and
credential recovery. Reuse the accepted [market closeout r3](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/1b0aa9771c5fcbdaf44c6e4190fd2a425e1412f3/astra_response/Phase-15/market-configuration/r3/REVIEW.md).
The recorded 10350-1 complete-set refresh passed; it does not qualify every set or
strategy. No market/backup work is reopened or reverified here.

## 3. In scope

One operator-entered purchase outcome per saved forecast **lineage** (an original
and its revisions), with successive complete-state entries. A single purchase may
have manually aggregated sale totals, but there is no order or inventory ledger.
Partial or different-strategy sales remain recordable with honest limitations.
This delivers the first bounded portion of R-07's outcomes requirement under
Prompt 16 (`prompts/16_training_dataset_and_hardening.md`), the
Phase 16 roadmap (`docs/ROADMAP.md#phase-16--training-datasets-outcomes-and-recognition-hardening`)
and the later data-model scope (`docs/DATA_MODEL.md#later-listing-image-recognition-and-dataset-module--phases-1316`).

## 4. Explicit non-goals

No dataset export, training-ready labels, hard negatives, splitting, training,
embeddings or recognition. Those wider Phase 16 requirements remain deferred,
unsatisfied and subject to their existing rights/privacy gates. Recording an
outcome grants no source-use or training permission. No bank/email/marketplace
imports, provider work, pricing activation, general accounting, second inventory
model, new native Android screen or photo/capture prerequisite. Deferred Economics
and the accepted manual-economics contract (`docs/plans/102-manual-deal-economics-admission-repair.md`)
remain unchanged. Phase 15B stays stopped/partial/unqualified and excluded from
production; 15C is unstarted and wider Phase 15 remains open.

## 5. Current repository state and reusable implementation

Local main is `6242904bd396eaf1f4ad064e8540f69035527839`, unpushed, index empty.
The 22 existing pending entries, including Plan 108 and all three protected files,
are preserved byte-for-byte. No existing 16A plan was found; 108 is the highest
allocated plan number. Production context is the accepted
`phase15a-market-credential-recovery-r3`, with Share deployed; no live check ran.

The conceptual `saved_deal` in the design document is implemented by
`public.deal_forecast` and its lineage, not an existing generic deal/outcome table.

| Existing code | Reuse and boundary |
| --- | --- |
| forecasts.py (`services/api/src/brickvault_api/forecasts.py`), forecast_models.py (`services/api/src/brickvault_api/forecast_models.py`) | Owner-filtered saved identity, `COALESCE(root_id,id)`, immutable original, `load`/offline replay and typed historical projection. |
| 0010 saved forecasts (`services/api/src/brickvault_api/migrations/sql/0010_saved_forecasts_up.sql`), 0011 revisions (`services/api/src/brickvault_api/migrations/sql/0011_forecast_revisions_up.sql`) | Saved-root/owner foreign keys and database immutability. Do not alter their guards or saved payloads. |
| lineage_metadata.py (`services/api/src/brickvault_api/lineage_metadata.py`), 0015 metadata (`services/api/src/brickvault_api/migrations/sql/0015_notes_source_urls_up.sql`) | Root resolution, transactional authentication, expected-revision conflicts and final-write authorization pattern. Its mutable notes table cannot preserve outcome history. |
| economics_v1.py (`services/api/src/brickvault_api/economics_v1.py`), economics_snapshot.py (`services/api/src/brickvault_api/economics_snapshot.py`) | `MoneyInput`, fixed `arithmetic_context`, `signed_money`, versioned exact forecast replay. Keep frozen V1 unchanged; actual facts do not enter valuation admission. |
| API forecasts (`services/api/src/brickvault_api/api/forecasts.py`), runtime grants (`services/api/src/brickvault_api/persistence/runtime_grants.py`) | Existing session/CSRF/error/no-store boundaries and enumerated privileges. |
| HistoricalForecastPage.tsx (`apps/web/src/HistoricalForecastPage.tsx`), LineageMetadataSection.tsx (`apps/web/src/LineageMetadataSection.tsx`), forecast-api.ts (`apps/web/src/forecast-api.ts`) | Existing `/deals/{id}` workflow, explicit Save/reload/conflict handling, `openapi-fetch` and session client. No new list or navigation destination. |
| generated contracts (`packages/contracts/src/schema.d.ts`), valuation rules (`docs/VALUATION_RULES.md`), saved-data security (`docs/SECURITY_PRIVACY.md#financial-and-saved-data-integrity`) | Generated decimal-string/null contracts, one server arithmetic authority and private financial history. |

## 6. Decisions and assumptions

Recommended design: USD-only, matching the current whole-set saved-forecast
contract; one purchase per lineage; one aggregate actuals record with append-only
corrections; comparisons always name the **original root**, never silently the
latest revision. No actual field is populated from an assumed forecast amount.

Monetary labor is actual paid labor, separately entered from Brian's labor minutes.
Do not assign an hourly wage to his time. Label profit as **actual profit after
recorded monetary costs; unpaid own labor excluded**, with minutes alongside it.
Every cost bucket requires a known amount or explicit zero before dependent totals
are available. Blank means unknown; no default zero or estimated provider price.

## 7. Exact proposed data, API and UI changes

### Data and bounded migration

One additive Alembic revision, proposed `0018_deal_outcome_revisions` after
`0017_listing_images` (recheck availability only when implementation is authorized).
Create only `deal_outcome_revision` with:

- `id uuid` (client submission identity), `owner_id`, `root_forecast_id`,
  `revision integer >= 1`, server `recorded_at`, nullable `correction_reason`
  (required after revision 1; 1–500 characters).
- `actuals jsonb`: a full, strictly validated input object below; `results jsonb`:
  server-produced amounts/states/reasons, comparison reference/results and
  `outcome-calculation-v1` / rounding versions. Each object is bounded to 16 KiB;
  monetary values are decimal strings, never JSON floats. Clients cannot supply results.
- Primary key `id`; unique `(owner_id,root_forecast_id,revision)`; same-owner FK
  `(root_forecast_id,owner_id)` to the existing original saved forecast. Index by
  owner/root/revision for latest/history reads. A trigger checks saved original
  membership, sequential append and fresh authenticated write context, assigns
  the timestamp and rejects UPDATE/DELETE. Serialize appends under the existing
  principal-lock pattern; runtime grants SELECT/INSERT only, no PUBLIC access.

No new mutable head table, forecast column, backfill, catalog dependency or
general event-sourcing framework. Every row is a complete replacement state for
display, not a command to replay. Prior entries remain independently readable.

| `actuals` field(s) | Meaning |
| --- | --- |
| `purchase_decision`: `BOUGHT` / `NOT_BOUGHT` | No row means **not recorded**, not a decision. NOT_BOUGHT requires transaction fields null. |
| `acquired_on`, `purchase_price`, `acquisition_extra_costs` | Nullable calendar date and USD amounts. Purchase price excludes separately recorded tax/premium/pickup costs; extras aggregate those actual outlays once. |
| `contents_state`: `NOT_CHECKED` / `CONFIRMED_MATCH` / `CONFIRMED_DIFFERENT`; `contents_checked_on`, `contents_note` | Brian's explicit inspection against the one-set saved representation. Confirmed states require the check date; difference requires a note, max 1,000 characters. Notes may describe figures/missing items; no guessed quantity inventory or prediction becomes verified contents. |
| `forecast_preceded_purchase`: nullable boolean | Brian confirms the original forecast preceded this purchase; unknown/false prevents a prediction-error claim, without blocking actuals. |
| `replacement_costs`, `labor_minutes`, `labor_costs` | Nullable replacement spend, nonnegative integer minutes and monetary paid-labor amount; never derive money from minutes. |
| `sale_status`: `NOT_SOLD` / `PARTIALLY_SOLD` / `COMPLETE`; `sale_strategy`: `COMPLETE_SET` / `OTHER`; `sale_condition`: `N` / `U` / `UNKNOWN` | COMPLETE explicitly declares all of this purchase disposed through sale and final settlement, with no outstanding return/payment. Different strategy remains recordable but noncomparable. |
| `sale_channel`, `sold_on` | Nullable plain-text channel, max 80 characters, and date of final sale. Multiple-channel totals may be explicitly labeled as such; no per-order tracking. If both dates exist, sale cannot precede acquisition. |
| `item_sale_proceeds`, `shipping_charged` | Nullable actual item revenue **excluding** buyer shipping and pass-through tax; shipping received is separate. Use final settled amounts after any refund once; a marketplace net payout is not item gross. |
| `selling_fees`, `shipping_paid`, `other_selling_costs` | Nullable actual fee, carrier and packaging/other selling spend; exclude acquisition, replacement and labor already recorded elsewhere. No fee estimation from a profile. |

Money uses existing `MoneyInput` limits (nonnegative, up to two decimal places),
nullable without defaults. BOUGHT requires a sale status, initially NOT_SOLD;
sale strategy/condition may be null until recorded. NOT_BOUGHT has null transaction
fields and NOT_CHECKED contents. Known zero is accepted. NOT_SOLD rejects sale receipts;
partial sales can retain cumulative observed receipts/costs, labeled **to date**.
Retained/gifted stock is not a completed sale.

Server equations follow existing money/domain rules (`docs/VALUATION_RULES.md#gross-proceeds-and-selling-costs`):

```text
gross = item_sale_proceeds + shipping_charged
selling_costs = selling_fees + shipping_paid + other_selling_costs
                + replacement_costs + labor_costs
net = gross - selling_costs
acquisition = purchase_price + acquisition_extra_costs
profit = net - acquisition
days_to_sell = sold_on - acquired_on (calendar days, only a completed sale)
```

All operands of an amount must be known; otherwise return null with missing-field
reasons. Negative net/profit remain negative. Zero acquisition still permits profit;
no new ROI, maximum-buy or valuation calculation is added. Profit and time-to-sell
are suppressed for partial/not-sold purchases. A completed sale with missing costs
is **incomplete outcome**, not a completed financial result; known gross may still
show. Missing dates block duration, not otherwise complete monetary arithmetic.
The full outcome is complete only when the purchase/sale facts, dates/channel and
required monetary buckets are known. Persist inputs and versioned server results.

### API

Add `outcome_models.py`, `outcomes.py` and `api/outcomes.py`; register the router in
`main.py`, extend only the new-table runtime grants, and regenerate OpenAPI and
TypeScript under `packages/contracts` during implementation. Use fixed Decimal
context/format helpers from frozen V1 for a small actual-cash calculation; do not
fabricate a supported valuation or call `calculate_v1` with invented market data.

| Proposed route | Behavior |
| --- | --- |
| `GET /api/deal-forecasts/{identifier}/outcome` | Resolve owned saved original/revision to its root; return latest entry or NOT_RECORDED plus history summaries, 20 per page with `before_revision`. No provider/catalog read. |
| `POST /api/deal-forecasts/{identifier}/outcome` | Accept submission `id`, `expected_revision` (0 initially), full `actuals`, and correction reason. Authenticate/CSRF-check, append revision+1 atomically, calculate server results and return the committed entry. |
| `GET /api/deal-forecasts/{identifier}/outcome/entries/{entry_id}` | Owner/root-scoped exact entry read for history and uncertain-write recovery, including its original inputs/results. |

Same submission ID and identical normalized request returns the original committed
entry, even after later corrections; changed content under that ID returns 409
`OUTCOME_ID_REUSED`. A competing expected revision returns 409 `OUTCOME_CONFLICT`.
Missing/inaccessible/unsaved roots return 404 without owner disclosure; validation
is 422; ordinary unavailable responses are typed. A lost response leaves the form
uncertain: look up that ID, retain the draft and require deliberate retry using the
same ID only after recovery. Never silently append again. All reads are private,
online-only/no-store; do not extend offline caches or queue writes.

### UI

Add `OutcomeSection.tsx`, `outcome-api.ts` and minimal existing stylesheet changes
to `HistoricalForecastPage.tsx`, using generated types/session client. Show it on
original and revision pages as **Actual outcome for this saved deal; comparison
baseline: original [ID]**. Keep forecast display and Edit assumptions separate.
An outcome-service failure must not hide the forecast, and an unavailable forecast
must not prevent an owner from reading/recording actuals against its saved identity.

Minimum entry is Bought or Not bought. Bought opens optional acquisition/inspection/
preparation and sale fields; show explicit **unknown** and a deliberate **none/0**
choice per money bucket. A completed financial result needs the applicable amounts;
date/channel omissions remain visible. Show recorded actuals, available derived
totals, missing reasons and permitted comparison beside the immutable prediction.
**Correct entry** copies the latest actuals into an in-memory draft, requires a
reason and appends on Save; **History** opens earlier entries read-only. No automatic
merge on conflicts. Reuse session-cleared draft handling, not localStorage or URLs.

## 8. Immutable forecast and comparability contract

Never write forecast payloads, digests, lineage, inputs, outputs, evidence or version
fields. The original is read through existing frozen decode/integrity/replay,
without current market/profile/catalog evidence. Saved deadlines remain historical;
current evidence stays NOT_CHECKED. Persist the comparison's original ID/digest and
the exact original values used, or its unavailable reason. A missing expected value
stays missing, including a purchase-limits forecast without an assumed purchase.

Return comparison state/reasons **per metric**, separately from actual-result state:

- Comparable sale/net error requires a completed settled sale, all relevant amounts,
  matching USD, exactly the same one-set identity/quantity/condition and Brian's
  CONFIRMED_MATCH contents attestation, COMPLETE_SET strategy, and a successfully
  replayed original with a supported SOLD/SALE_ESTIMATE baseline. Brian must also
  confirm the original preceded the purchase; unknown timing is NONCOMPARABLE.
  Reject a confirmation contradicted by recorded chronology. The attestation
  is operator-entered, not a catalog/provider guarantee or training label.
- Signed monetary error is **actual minus original**, using unrounded/exact stored
  forecast values before currency display. Compare item proceeds with expected sale,
  and net with estimated net using the same complete cost boundary. Label a MANUAL
  baseline as an assumption comparison, not provider forecast accuracy.
- Profit error additionally requires equal known original/actual total acquisition
  cost. Otherwise show both profits and both acquisition bases, mark profit comparison
  NONCOMPARABLE (`ACQUISITION_BASIS_CHANGED`), and do not invent a normalized forecast.
- Changed strategy/contents/condition, partial sale or unverified scope yields
  NONCOMPARABLE, no numeric error. STOCK is an active-listing what-if, not comparable
  prediction accuracy. Null expected fields or failed/unsupported original replay
  yield UNAVAILABLE; actual facts/results can remain available. No original duration
  forecast exists, so there is no time-to-sell prediction error.

Later actual corrections append; they cannot recompute the original against today's
evidence or silently change the baseline to a later forecast revision.

## 9. Implementation sequence after separate approval

1. Add strict actuals/result models and fixed-version money/comparability functions.
2. Add the single migration, append-only service, permissions and three API routes.
3. Generate contracts and add the one detail-page section and recovery/history flow.
4. Run only the affected validation below, inspect the task diff and stop for review.

## 10. Focused future validation and acceptance

**Nothing in this section has run. No tests or builds run during planning.**

- Unit cases for explicit zero vs unknown, shipping counted once, replacement/labor
  counted once, minutes separate, negative profit, zero acquisition, dates and
  partial/completed outcomes; strict comparison gates, exact error sign and missing
  original values. New `test_outcomes.py` unit coverage reuses existing money fixtures.
- Isolated PostgreSQL/API cases for append/history/idempotent lost-response recovery,
  competing expected revisions, owner/root isolation, CSRF/session expiry and direct
  UPDATE/DELETE denial. Reuse the fixture patterns in `test_forecasts.py` and
  `test_forecast_revisions.py`; add focused outcome integration coverage.
- Hash original/root/revision financial bytes and versions before/after actual entry
  and correction. Reopen the same historical URL after fixture evidence changes;
  verify unchanged frozen results. Make provider access fail if attempted. Include
  unavailable-original cases without weakening manual admission.
- Because the schema changes, verify upgrade from 0017 on an owned disposable TEST
  database with an existing saved forecast, explicit runtime grants and empty-table
  down/up. No production migration or broad database restore campaign.
- Focused React outcome-section cases for entry, correction/history, unknown fields,
  comparison reasons, conflict/uncertain recovery and auth/offline gating; one small
  synthetic API/UI flow at desktop and narrow viewport. Check only affected types,
  generated-contract consistency and lint/format during implementation, not a full
  application/Share/capture/device/build qualification campaign.

Acceptance: Brian can record/correct an outcome, see honest incomplete states and
only comparable errors, reopen prior actual entries, and retrieve byte-unchanged
original forecasts. No provider work or client-side financial arithmetic occurs.

## 11. Security, privacy and data integrity

Owner/root filters and final-write authorization apply to every entry and recovery
read. Reject client owner/results/forecast mutations and unknown model fields.
Render channel/inspection/correction text as text, not HTML; log safe IDs/error codes
without financial payloads, seller details or secrets. Outcomes/inspection notes
stay private and confer no training permissions. Existing image/privacy/source-use
restrictions are unchanged.

## 12. Failure modes, rollback and recovery

Conflict keeps the draft and requires reloading the latest entry; timeout uses exact
submission-ID recovery. Missing/invalid historical data suppresses comparison only.
Fix a wrong entry with an appended correction, never deleting history. Migration
adds no forecast backfill; rollback must preserve populated outcomes and refuse an
automatic destructive downgrade. Empty disposable TEST downgrade is sufficient
for this slice; deployment/data rollback requires separate operational approval.

## 13. Decisions for Brian and progress

Approve together: **one purchase per saved lineage with aggregate actuals**, paid
labor money separate from unpaid own minutes, and **original-root comparison with
the strict scope/acquisition gates above**. These are the consequential product
boundaries; no new account, provider-rights or architectural decision is required.
Multiple purchases on one lineage, per-order allocation or priced contents repair
would require a later scoped plan. No physical-device checks are needed for plan approval.

- [x] 2026-10-19: inspected current local saved-forecast/domain/API/UI implementation.
- [x] 2026-10-19: preserved pending/protected work and drafted one bounded 16A plan.
- [ ] Brian accepts the plan and separately authorizes implementation.
- [ ] Implementation and only the focused source validation above.

## 14. Outcome and stop

**Plan ready for review; no implementation performed.** Only this new plan is added
to local documentation; main remains uncommitted for this task, unpushed and index
empty. Publish a plan copy with a concise review, exact documentation inventory and
changed-link/whitespace/preservation checks under
`astra_response/Phase-16/16A-plan/r1/` (next revision if occupied). No tests/builds,
application/migration/generated-contract/dependency edits, database/service startup,
credential reads, phone/server access, provider requests or operational changes.
Stop for plan approval; do not resume capture, 15C or wider Phase 16 work.
