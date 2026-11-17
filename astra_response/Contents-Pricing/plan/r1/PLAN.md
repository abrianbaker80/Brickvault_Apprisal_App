# Selected contents market refresh — ExecPlan 112

**PLAN ONLY — READY FOR CONTENTS PRICING PLAN REVIEW.** November 16, 2026.
Recommend one delivery for selected, already verified minifigures and exact part/color
items. Reuse the existing provider, cache, valuation and confirmed-refresh machinery.
Add item-level Contents evidence and durable multi-target authorization. Do not make
complete inventory mapping or incomplete-set economics prerequisites for this slice.

## 1. Goal and user-visible outcome

Open a set, inspect its recorded catalog contents, choose a small selection and market
views, inspect the exact request plan, confirm, then see each item's evidence and
selected-scope coverage. Pricing an item proves neither physical ownership nor the
completeness, condition or authenticity of Brian's lot.

## 2. Why now and requirement ownership

This returns to R-03/R-04 and R-11–R-14 contents pricing, with R-35 shared requests and
R-37 presentation. It delivers a bounded part of those requirements, not their closure.
Every-figure mapping/coverage, complete catalog totals and full Part-Out Analysis remain
outstanding where unsupported. `docs/REQUIREMENTS_TRACEABILITY.md`, especially Deferred
Economics Extensions, remains authoritative. No new phase number or Phase 16D is assigned.
Phase 16C source/production remain ACCEPTED / CLOSED; capture remains stopped.

## 3. Current repository state and implementation map

Source authority is local main `97130dac80e3351af62ea8d2168c62fefcaae133`.
Recorded closeout is `2520e2a8e0b41e690c1f59db5183f288108d76fd`,
`astra_response/Phase-16/16C-production/r4/REVIEW.md`. Recorded release/schema are
`phase16c-outcomes-production-r2` / `0019_reviewed_dataset_foundation`; these identities
are not new live verification. Main is unpushed; 22 pre-existing pending application/
documentation paths and prior publications are preserved. Next unused ExecPlan is 112.

| Layer and inspected source | Reusable capability | Exact remaining gap |
| --- | --- | --- |
| `providers/bricklink/requests.py`, `responses.py`, `market/repository.py`, `worker.py` under `services/api/src/brickvault_api/` | SET, MINIFIG and PART price guides; PART requires BrickLink color; independent N/U × sold/stock; normalized Decimal evidence, empty results, shared cache/jobs and attempt ledger | No new client or price transport needed. Supported code and historical bounded proofs do not establish current account access or inventory coverage. |
| `catalog/repository.py`, `query_types.py`, `expansion.py`, `physical.py`; Plans 020/100/101 | Snapshot/source-pinned set inventory revisions, direct part/color and figure rows, separate regular/extra quantities, figure membership, element/provider mapping lookup, nested/assembly bindings and guarded expansion | Contents currently exposes composition counts and figure membership, not a selectable exact part/color inventory. A raw catalog row is not an admitted physical valuation population. Current live inventories/mappings were not queried. |
| `market/models.py`, `valuation/evidence.py`, `providers/bricklink/proof.py`, `calibration/stage_one.py`; Plans 030/040 | Immutable reviewed market mappings for all three types; exact snapshot/namespace/color binding; ITEM, ELEMENT, COLOR, KNOWN_COLORS and SUBSETS discovery; explicit evidence review | Product discovery/review is SET-only. Calibration is owner-driven/P4-01-specific, not a public component crosswalk service. Plan 105 explicitly retains fourteen missing minifigure mappings; recognition labels/name matches do not resolve them. |
| `market/product_refresh_models.py`, `product_refresh.py`, migration 0008, `refresh.py`, `api/refresh.py`; Plan 060 | Read-only plan, signed confirmation, durable idempotency, operation leases, per-view completion, job-generation fencing, quota/retry accounting, resume and uncertain-result reconciliation | Models/SQL bind one SET mapping, exactly four views and 4 identity/4 price/2 retry/10 total limits. UI/API-only changes cannot safely represent multiple component authorizations. |
| `product.py`, `valuation/{evidence,population,engine,arithmetic}.py`; Plans 050/070 | Cached figure and part/color prices already feed quantity-aware theoretical valuation when the existing physical strategy is admitted; exact view/mapping/cache selection and no double counting | Blocked physical expansions intentionally have no contributions or denominator. Add per-item unit evidence independently of whole-inventory admission, without bypassing those aggregate gates. |
| `apps/web/src/{AppraisalDetail,MarketRefresh}.tsx`, `refresh-api.ts` | Contents, evidence/coverage displays, explicit confirmation, read-only status polling, Resume/Recheck progress and reload | Refresh says “Contents refresh is not available”; figure rows have no individual price; ranked contributions are a bounded priced subset, not a complete selectable inventory. |

## 4. In scope and recommended workflow

Deliver **both verified MINIFIG and verified PART/color targets in one workflow**.
Neither needs another pricing adapter. Restricting to figures first would still leave
the known crosswalk dependency; parts-first discovery would add a mapping-review
feature to a refresh slice. Existing verified mappings are the smallest shared entry.
Its real usefulness is conditional on eligible mappings; zero eligible mappings must
produce an honest blocked screen, not synthetic coverage or an acceptance claim.

1. Contents lists direct recorded figure and part/color rows in stable pages of 50,
   pinned to one inventory revision. Show exact namespace/identifier, color, quantity,
   regular/extra distinction, membership/assembly status and mapping eligibility.
   Keep unsupported nested/alternate/assembly rows visible with reasons. First delivery
   does not traverse descendants for selection or resolve alternate choices.
2. Select up to **four distinct canonical targets**, with at most **32 selected source
   occurrence references** and a **16 KiB normalized plan**. Retain repeated source
   rows and their regular/extra quantities; selecting a target does not merge physical
   occurrences. Extras are visible but excluded from selected quantity by default;
   explicit inclusion changes the plan, not the source inventory. No actual-quantity editor.
3. Independently choose any nonempty subset of New/Used × Sold/Active, defaulting to
   all four. Active is the UI label for existing `stock` asking evidence. At most 16
   target/view bindings exist, but at most four may require new price dispatch.
4. Review a plan showing every selected target/view, exact mapping, reuse/join/fetch/
   blocked action, counts, allowance, expiry and exclusions. An over-cap plan is
   non-confirmable and explains what to deselect; never silently truncate or batch it.
   An inventory larger than the cap remains browseable; no Select All refresh or
   automatically chained operations. Four cold targets × four views require 16
   requests and are refused; one cold target × four views fits.
5. Confirm once. Show per-target/view progress and results; allow explicit Resume or
   read-only Recheck progress. Reload item evidence and the current appraisal after
   completion. Changing set, revision, selection, extras or views invalidates the draft.

## 5. Explicit non-goals and remaining contents scope

No mapping creation/discovery in this first delivery; identity requests are exactly
zero. No bulk catalog refresh/reimport, provider-policy change, new dependency,
recognition/dataset/capture work, physical inventory claim, new aggregate formula,
replacement-cost engine, missing-item editor, split-sale profit, labor/recovery model,
economic break-even lots, ROI expansion, Hunt ranking or frozen-forecast recalculation.

Remaining contents pricing includes evidence-backed mapping onboarding, unresolved
figures/part-colors, descendant selection and broader every-item coverage. Retain it
as outstanding R-03/R-04/R-11–R-14 scope, separate from Deferred Economics Extensions.
The latter's missing/damaged contents, adjusted figure quantities, instructions/box/
build, figures plus remaining build, full part-out economics, recovery/burden and
economic break-even lots all remain OUTSTANDING / DEFERRED, not moved or satisfied.

## 6. Decisions, identity and source dependencies

**Grouped plan decision:** approve the mapped-only two-type delivery, four-target/
four-price ceiling, direct recorded inventory scope and single additive migration.
These are recommendations for one plan approval, not separate miniature phases.
No provider permission or policy change is requested by this plan.

Admit exactly one current, verified `market_mapping_revision` matching canonical kind,
UUID, namespace/variant, snapshot and source version. PART additionally matches
canonical part/color IDs and exact BrickLink color; MINIFIG is a whole provider figure,
never a PART substitute. Reject closed, conflicted, ambiguous and unresolved mappings.
No suffix stripping, name similarity, number coincidence or first-match selection.
Catalog provider mappings are evidence candidates, not automatically verified market
mappings. Recheck these bindings at confirmation and before dispatch.

For subsequent mapping onboarding, reuse the existing adapter/discovery ledger and
review semantics rather than importing the catalog again. Parts need a source-backed
element/part/color association, exact ITEM evidence, unambiguous ELEMENT result,
COLOR and KNOWN_COLORS evidence (`proof.py`/`stage_one.py`). Figures need an
authoritative canonical-to-provider whole-figure association plus exact ITEM and
reviewed parent/SUBSETS membership where applicable. Parent membership alone cannot
identify one Rebrickable figure among several BrickLink figures. The unavailable
cross-provider association is a specific source dependency, not permission to guess.
The current product discovery table/reviewer admits SET only; safely supporting new
discovery types and review would be additional contents scope, not an existing feature.

Current live mapping availability, source rights, account access and activation are
unverified. A later authorized activation check must establish at least one eligible
real selected target before claiming live utility. Fixture success does not settle
that gate. Reuse accepted `market_policy` and provider-gate records; do not invent
rates, account allowances, provider access or historical retention rights.

## 7. Data model and API/interface changes

**One migration is necessary:** proposed `0020_contents_market_refresh`, after 0019.
Extend the existing durable operation framework; no second cache, observation store,
request ledger, provider client or calculation engine.

- Add versioned `CONTENTS` operation scope and `PRODUCT_CONTENTS_REFRESH` budget roots
  with 0 identity / 4 price / 2 retry / 6 total ceilings. Existing COMPLETE_SET roots,
  signed v1 plans, limits and history keep their semantics and bytes.
- Add one `product_refresh_target` table: operation/target ordinal, exact canonical
  kind and IDs, snapshot/source/inventory revision, selected occurrence references
  and quantity/inclusion fingerprint, verified mapping revision and target state.
  Enforce correct typed foreign keys and uniqueness per operation/exact target.
  Catalog quantities remain authoritative; clients cannot supply trusted quantities.
- Extend `product_refresh_view` with nullable target reference for legacy SET rows.
  Replace its operation/condition/basis primary key with a stable binding key and
  scoped uniqueness: legacy operation+view; contents operation+target+view. Retain
  cache/job/admitted/current/completed generations and atomic result publication.
  Guard target membership, selected-view cardinality and all immutable plan bindings.
- Keep legacy operation-level `resolved_mapping_id` for SET; contents mapping lives
  on targets. Scope open-operation uniqueness by set and operation scope, allowing
  one open contents operation per set, returning its receipt for competing requests.
  Update affected SQL validation/context/ownership/lease/close capabilities and
  worker completion integration with explicit v1/v2 branches. Do not relax SET guards.
  The SET discovery-evidence table and mapping-review behavior need no expansion.

Public additive contracts in `refresh_models.py`/a contents projection module:

| Route | Contract |
| --- | --- |
| GET `/api/sets/{set_number}/contents` | Snapshot/revision-pinned cursor, 50-row page, total recorded-row state, exact identities/quantities, safe mapping state and four-view unit evidence. Revision change requires reload; no dispatch or demand writes. |
| POST `/api/sets/{set_number}/contents-market-refresh/plan` | Validated source occurrence references, revision, extras and selected views; returns normalized selected scope, target/view actions, counts, blockers and signed expiring confirmation. Read-only. |
| POST `/api/sets/{set_number}/contents-market-refresh` | Signed receipt plus selected-scope input for server recomputation; atomic durable confirmation and explicit execution. Same key/digest returns the original operation. |
| GET `/api/sets/{set_number}/contents-market-refresh` | Active/recoverable contents operation only; safe after reload. |
| GET `/api/contents-market-refresh/{operation_id}` and POST suffix `/resume` | Typed per-target/view status; Resume reconciles then executes only remaining authorized work. Scope-check IDs; retain existing whole-set route/response behavior. |

Reuse/refactor `RefreshService`, `ProductRefreshRepository`, API wiring and
`useMarketRefresh` lifecycle behind typed scope adapters. Add a Contents picker/plan
panel; remove only the obsolete contents-unavailable copy. Generate OpenAPI and
TypeScript via the existing contracts pipeline and use `openapi-fetch`.

The item read projection may inspect verified mapping/cache evidence even when full
physical expansion is blocked. Factor existing exact evidence validation and decimal
unit-price selection into a shared pure helper if needed; never fabricate an admitted
Expansion to obtain a price. Show `quantity_weighted_average`, currency, view, source,
sample/window and fetch/freshness times. Do not create row extended-value or selected
subtotal arithmetic in the browser. Existing server valuation alone supplies any
quantity-aware subtotal when its original physical-admission rules pass.

## 8. Request budget, partial results and recovery

For selected target/view keys, `I = 0`, `P = distinct FETCH keys <= 4`, retry reserve
`R = 2`; displayed maximum possible new attempts is `P + R` when P > 0, otherwise 0,
and can never exceed six. REUSE/JOIN/BLOCKED add zero new initial requests to this
operation. Joined work retains its original accounting and is disclosed separately.
The six-attempt ceiling is an application limit, not an account entitlement.
Shared rolling/global and per-group limits, cooldown/suspension, policy freshness,
display/retention and retry rules remain authoritative; the stricter limit wins.

Deduplicate only equal full cache request keys: provider/account, exact mapping
revision/item/color, condition, basis, currency/geography/options and adapter/normalizer
versions. Reuse fresh eligible evidence or fresh confirmed-empty evidence; never
substitute another condition/view or revive expired content. Join only a compatible
pending job/generation authorized by the existing machinery. Keep all occurrence and
quantity associations despite one outbound request. Reject unresolved canonical alias
conflicts rather than collapsing differing mappings into one apparently verified key.

The signed digest covers selected scope, inventory/mappings, policy/versions, view
actions, cache/job generations and limits. Retain the 15-minute confirmation and
24-hour operation windows. Recompute at confirmation; any material drift requires
replanning before dispatch. Reserve each outbound attempt durably under existing
scope/budget locks. Record success/empty/failure and binding completion atomically.

An individual failed view leaves others intact. Read-only status failure shows
progress unknown and Recheck progress, not an inferred resumable operation. Reload,
duplicate confirmation and a lost acknowledgement recover the original durable receipt.
Explicit Resume first reconciles leases, recorded attempts and exact job generations;
it neither redispatches completed work nor resets quota. Uncertain sends remain counted;
only the existing bounded retry policy may authorize another attempt from the same
remaining reserve. Unresolvable evidence stays `EVIDENCE_UNRESOLVED`.
Terminal replay never reopens a root. After terminal failure/expiry, explicit Retry
prepares a new displayed plan for requested unresolved keys; it reuses eligible
completed evidence, preserves all prior accounting and still requires confirmation.

## 9. Results, security and data integrity

Distinguish unresolved identity, unrequested/no evidence, confirmed empty, stale,
display-ineligible, failed/unavailable and priced. A failed refresh may coexist with
older still-displayable evidence; show both states. Confirmed empty is not zero money.
Enforce display expiry on visible and collapsed content as existing appraisal does.

Show selected target/view counts and selected recorded quantities separately from
full-inventory coverage. Unknown full population has no denominator. For an unadmitted
catalog representation, show unit evidence and recorded quantities only: no complete
figure/set/component value or synthetic coverage. Preserve existing theoretical partial
subtotal labels when admitted; gross component value is not recoverable proceeds/net
profit. Whole figures and descendants never enter the same aggregate allocation;
this slice does not unlock or automatically rank/sum selling strategies.

Existing private authentication, origin/CSRF rules, no-store and session clearing apply.
No browser provider calls, credentials/account identifiers in public projections,
raw responses in plans/logs or provider/model access on page/search/plan/status.
Only explicit Confirm/Resume dispatch; no background refill or quota reset.

## 10. Implementation sequence and directly affected runtime seams

Within one subsequently authorized implementation slice: (1) contracts and additive
schema with shared immutable guards; (2) read projection, bounded planner and execution/
recovery integration; (3) Contents selection/results, focused checks and one stable
acceptance pass. These checkpoints require no repeated routine approval loop.

Include migration Python/SQL resources and head expectations in `scripts/package_api.py`;
update `market/models.py` table inventory, `product_refresh_models.py` table/function/
column registries, `persistence/runtime_grants.py`, affected retention traversal and
schema/package tests. Target writes occur only through constrained capabilities;
revoke PUBLIC execution, fix search paths and enumerate runtime grants. Runtime must
not acquire arbitrary mapping/policy administration privileges.

`backup_format.py` currently explicitly admits 0017/0018/0019 heads. Add 0020 to the
same four-artifact contract only after narrow compatibility checks, retaining historical
admission. Include the new target table in affected backup/restore inventory and
retention ownership checks; preserve operation-to-target/view references. Confirm
production-admin preflight and application readiness use the new exact head. Deployment
packaging must pair compatible API/static/contracts/schema and record migration/grants/
health expectations. No new service, scheduler, credentials, firewall or hosting change.
Do not investigate backup history or rerun unrelated operational campaigns.

## 11. Validation and implementation completion condition

**This planning task runs no tests/builds/services.** Later use synthetic providers,
deterministic clocks/barriers and owned disposable PostgreSQL TEST resources:

- Unit/API: exact figures, suffixed variants and part colors; unknown/ambiguous mapping;
  regular/extras/repeated occurrences; independent views; selected limits; stable pages;
  zero provider dispatch and credential loading on every read/plan/search path.
- PostgreSQL: migration from 0019 preserving SET history, constrained grants/ownership,
  target/view uniqueness, concurrent confirmation, full-key dedup/join, quota ceilings,
  stale plan/mapping rejection, partial failure, lost response, crash/restart, uncertain
  sends and explicit resume without duplicate completion/accounting. Test actual DB
  behavior, not mocked persistence. Narrow package/head/backup-format inventory checks
  and guarded downgrade tests suffice; no full backup/restore campaign.
- Read projection: exact eligible unit statistic and deadline, empty vs unknown vs
  stale/error, selected coverage vs full population, blocked aggregate despite priced
  items, and unchanged admitted cached valuation consuming new component evidence.
  Reuse existing arithmetic/physical tests; add only affected helper regressions.
- React plus one meaningful browser workflow repeated at desktop and narrow viewport:
  mixed mapped figure/part rows, unresolved row, four-view cap feedback, confirm,
  partial completion, reload/recheck/resume and clear evidence/quantity labels.
  Existing whole-set refresh regression remains in the affected suite. No phone,
  dataset, financial calibration or capture campaign.
- Once stable, run affected Python formatting/lint/types/tests, generated-contract
  checks, web lint/types/tests/build and API packaging once. Inspect the complete
  allowlisted diff; independent review once at the application commit boundary.

Implementation is complete for review when both mapped types work end to end with
fixtures/real TEST persistence, no pre-confirm dispatch, bounded exact requests,
durable recovery, honest item evidence/coverage, unchanged whole-set refresh and all
directly affected migration/grant/package checks passing. Report source/TEST completion
separately from real mapping availability, provider qualification and deployment.

## 12. Failure modes, rollback and later activation boundary

No eligible mappings: retain visible exact rows and specific source blockers; never
fetch speculative identities or repeatedly reimport. Policy/account unavailable: show
unavailable and preserve saved operation/evidence. Changed inventory or mapping:
reject confirmation/remaining dispatch and require an explicit new plan. Completed
results remain recorded subject to existing display/retention rights.

Prefer a forward correction after 0020 contains operations. Guard downgrade against
meaningful contents history; do not delete accounting/targets to roll back. A previous
binary requiring 0019 is not a valid rollback against 0020. A later deployment plan
must identify the compatible rollback package or approved recovery point before rollout.

Plan approval alone authorizes no implementation, migration, application commit or
deployment. After separate implementation authorization and review, deployment and
live-provider use still require explicit approval. A live check must use an actual
displayed target/view/request plan with applicable account/policy state; no exploratory
calls. The working server and phone remain untouched in this task. No physical-device
qualification is claimed or required merely to plan the shared web workflow.

## 13. Progress log and open checks

- [x] 2026-11-16: Selective repository inspection; baseline, 22 pending paths and prior
  publication hashes recorded; root UI/schema gaps and unresolved mapping dependency identified.
- [x] 2026-11-16: One bounded ExecPlan prepared; no source, contract or migration edits.
- [ ] Brian approves or revises the grouped scope/migration recommendation.
- [ ] Separately authorize implementation; later activation/live mapping and provider
  checks remain open. No new manual phone check is proposed for source completion.

## 14. Outcome and follow-up

Planning outcome: ready for review, not approved or implemented. Keep this plan
uncommitted on local main; publish only its sanitized review package on astra-response.
Do not rewrite unrelated status documents. The only next requested action is plan
approval. Remaining mapping/coverage and Deferred Economics requirements stay explicit;
no implementation, capture restart, deployment or subsequent economics work follows.
