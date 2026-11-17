# Selected component mapping onboarding — ExecPlan 113

**PLANNING ONLY — READY FOR SELECTED COMPONENT MAPPING ONBOARDING PLAN REVIEW.**
November 17, 2026. One proposed implementation slice; approval and implementation
are pending. Plan 112's selected-refresh SOURCE/TEST and bounded production delivery
remain **ACCEPTED / CLOSED**. No new numbered phase is assigned.

## 1. Goal and user-visible outcome

Add **Review identity** to the shared Contents workflow. Brian selects unmapped
direct catalog contents, sees evidence and specific blockers, confirms a bounded
identity request plan when useful, reviews each supported exact binding, and hands
approved targets to the existing separately confirmed price-refresh workflow.
Deliver exact-element parts and the narrowly supported whole-figure proof in one
interface. Unsupported figures remain visible; parts need not wait for a general
figure crosswalk. An approval establishes a catalog/provider binding, never physical
ownership, completeness, condition, authenticity or successful price retrieval.

## 2. Why now, scope and explicit non-goals

The two manually admitted examples establish reusable proof patterns, not repeatable
catalog onboarding. This slice advances R-03/R-04, R-11–R-14, R-35 and R-37. It does
not close every-figure pricing, complete inventory coverage or broader part-out scope.
`docs/REQUIREMENTS_TRACEABILITY.md`, `docs/VALUATION_RULES.md` and
`docs/PROVIDER_GATES.md` remain authoritative.

In scope: direct recorded whole figures and exact part/color rows; source-bound
eligibility, bounded discovery, durable evidence, independent binding review, and
handoff to accepted pricing. Reuse the existing extras/occurrence semantics.

Out of scope: missing-item editing, replacement costs, adjusted quantities,
split-sale/part-out economics, Hunt intelligence, valuation or normalization changes,
physical admission, frozen forecasts/outcomes, recognition/datasets, advanced capture,
descendant/alternate selection, catalog imports, new providers and source-rights policy
changes. These original requirements remain outstanding, not satisfied or cancelled.
No general identity administration, arbitrary evidence uploads or mapping replacement
UI is included. Conflicts receive an explicit review disposition but remain blocked
for replacement outside this unmapped-target slice.

## 3. Current repository state and evidence authority

Source authority is **local main `20f78c74574834ade40dd4697e04ed3788e5f5d3`**.
Accepted closeout is [production r5](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/6b5b2402743cc0b7d5614c4c08d6efc7c1ebbcc9/astra_response/Contents-Pricing/production/r5/REVIEW.md).
Recorded release/schema are `contents-sample-metadata-production-r1` /
`0020_contents_market_refresh`; these are historical identities, not live verification.
No matching onboarding plan exists; 113 is the next unused ExecPlan.

Read `docs/plans/112-selected-contents-market-refresh.md`, especially sections 18–19
and 25, for the accepted admissions. `fig-012609 → MINIFIG idea106` used the sole
regular intact figure on both sides of an exact parent inventory, quantity one,
zero extras and no alternate/counterpart ambiguity. `3001 / Rebrickable White 15 →
PART 3001 / BrickLink White 1` used element `300101` plus independent color evidence.
Original provider evidence is dated **2026-09-11**; **2026-11-17** records binding
review against current source rows. This plan reuses those conclusions without
requalifying them, opening private evidence or hard-coding their identities.

Historical `10350-1` has multiple figures and many part rows. It illustrates the
desired selection workflow, not a solvable benchmark. The fourteen unresolved
figures remain a separate exact-identity evidence gap; inspected repository records
do not resolve them. No current catalog-wide or production inspection occurred.

## 4. Evidence/source capability and dependencies

The operations below exist in the BrickLink adapter. Their availability in code and
historical proofs does not establish current approved account use, rights or retention.

| Target category | Existing evidence | Additional facts from existing operations | Limit / first-delivery behavior |
| --- | --- | --- | --- |
| Part with usable exact element/part/color evidence | Accepted snapshot, exact canonical part variant and known physical color, direct occurrence, source `element_mapping` and lineage | `ELEMENT` identifies provider part/color candidates; exact PART `ITEM`, `COLOR`, `KNOWN_COLORS` corroborate the binding | Four initial calls without reuse. Require a unique exact ELEMENT result and all independent checks. Catalog mapping status alone is not verified market identity. |
| Part with ambiguous/unavailable association | Source rows, unresolved color/association state and any variant evidence | A usable exact source element can justify one bounded ELEMENT read; returned candidate metadata may add facts | No element seed: no discovery route. Ambiguous ELEMENT: stop downstream requests. ITEM existence, equal IDs/names or known-color presence cannot choose the canonical part. Unknown/sentinel color stays blocked. |
| Whole figure with independently supported exact evidence | Exact canonical/source figure membership and an eligible exact parent SET mapping; historical reviewed proof establishes the narrow pattern | Parent `SUBSETS` with both break flags false, then exact whole `MINIFIG ITEM` | Parent proof requires sole intact regular figure on both sides, positive matching quantity, zero extras and no alternatives/counterparts; exact source checks must pass. Two calls with mapped parent and no reuse. |
| Whole figure with unsupported cross-provider identity | Canonical figure ID/name and possibly parent membership | SUBSETS can enumerate parent figures; ITEM can describe a nominated provider ID | Neither supplies a general figure crosswalk. Multiple figures cannot be paired by name, order or membership. Show `AUTHORITATIVE_FIGURE_ASSOCIATION_MISSING`; no speculative enumeration/candidate guessing. |

An unmapped/unsupported parent is `EXACT_PARENT_MAPPING_REQUIRED`; this slice does
not silently discover or map the parent. The existing separate SET workflow can
establish it, followed by a new component plan. Only the established unique-parent
route and eligible typed evidence from earlier operations of this workflow are admitted
for figures in this delivery. Runtime evidence reuse means product-persisted typed
facts under their approved lifecycle. The accepted historical private proof files
and mappings remain baseline evidence; this slice does not ingest them or add a
private-file importer. Zero-call plans become possible through eligible prior product
operations; no additional historical unmapped-target proof is assumed available.
A future external crosswalk needs its own exact provenance and permitted-use contract.
No public documentation lookup was necessary to identify these repository limits.

## 5. Recommended workflow and grouped decisions

1. Keep Contents paging and pricing eligibility. Add separate mapping eligibility,
   exact canonical namespace/variant/color and evidence/blocker summaries. A row can
   be selectable for identity review while unavailable for pricing. No page load,
   search, plan or status request dispatches to a provider.
2. Select up to **four distinct targets / 32 occurrences / 16 KiB normalized selection**.
   Server resolves source references and quantities. Show unsupported selections
   and exclusions explicitly; confirm only the displayed supported subset. Oversize
   or over-budget plans require deselection, never truncation or chained batches.
3. Review the identity plan: requested operations/dependencies, evidence reuse and
   original dates, target attribution, permissions/blockers, initial count, retry
   reserve, maximum attempts and expiry. **Confirm identity discovery** authorizes
   only that graph. A zero-call retained-evidence plan still gets a durable receipt.
4. Present each candidate with both namespaces, whole-figure versus PART identity,
   both colors where applicable, exact source and parent/element provenance,
   distinguishing facts, original evidence dates, validator result and conflicts.
   Candidate generation and validation do not approve a mapping. Brian individually
   selects **Approve supported binding**, **Reject**, or leaves it unresolved.
   Unsupported facts cannot be overridden by confirmation or free-text assertion.
5. Successful review atomically creates one approved mapping revision and receipt.
   Reload Contents; **Review price requests** prepares the existing price plan with
   approved occurrences preselected. It never auto-confirms or fetches a price.

**One grouped approval decision:** this evidence-limited workflow; four-target scope;
six-initial/two-retry identity ceiling; typed durable evidence and one additive migration;
per-target in-app review with no overwrite privilege. Once separately implemented and
activated for approved provider use, ordinary supported selections/discovery/reviews
occur in-app without another engineering task. New sources/rights, unsupported identity
claims and mapping replacement remain outside that standing product authorization.

## 6. Reused code and exact implementation surface

Paths below are repository-relative; backend paths start at `services/api/src/brickvault_api/`.

| Existing module | Reuse / bounded change |
| --- | --- |
| `catalog/repository.py` (`get_element_mappings`, provider mappings), `catalog/query_types.py`, source facts/bindings | Selected indexed reads pinned to snapshot/source/inventory. Check each mapping's state and color semantics; an overall `OK` result is not blanket verification. No catalog scan or mutation. |
| `providers/bricklink/{requests,responses,proof}.py`, `calibration/stage_one.py` | Reuse adapters and exact review invariants. Extract pure per-target proof checks into proposed `market/component_identity.py`; preserve the historical three-item proof harness and P4-01 calibration contracts. Never invoke that fixed manifest as a general API. |
| `market/{discovery,discovery_worker,accounting,product_refresh,product_refresh_models}.py`, `refresh.py` | Existing attempt reservation, provider/group limits, operation leases, signed confirmation, idempotency and reconciliation; add a discriminated mapping scope and typed normalized evidence. |
| `market/repository.py::review_mapping`, `market/models.py::MappingRevision` | Preserve identity, replay, canonical/provider conflict, locking and explicit predecessor rules. New runtime admission is narrower: only previously unmapped supported bindings, never arbitrary calls to the owner-level reviewer. |
| `contents.py`, `contents_models.py`, `market/contents_refresh.py`, `api/contents.py` | Keep current pricing behavior; additive eligibility/provenance projection. Proposed `component_mapping.py`, `component_mapping_models.py`, `market/component_mapping.py`, `api/component_mapping.py` own mapping plan/review/status logic. |
| `apps/web/src/{ContentsPricing.tsx,contents-api.ts,useRefreshWorkflow.ts,contents.css}` | Shared selection and lifecycle, a `ContentsMapping.tsx` review panel and typed `mapping-api.ts`; show separate discovery/review/pricing states. Generated `packages/contracts` OpenAPI/TypeScript via existing pipeline and `openapi-fetch`. |

### Additive API contracts

| Route | Behavior |
| --- | --- |
| GET `/api/sets/{set_number}/contents` | Add safe mapping-onboarding state/reason and canonical/provider evidence summary; preserve existing pricing fields and pagination. |
| POST `/api/sets/{set_number}/contents-mapping/plan` | Revision, occurrence IDs, extras only; read-only signed normalized plan. No client-trusted provider IDs, quantities or evidence. |
| POST `/api/sets/{set_number}/contents-mapping` | Exact selection + signed confirmation; durable receipt before explicit execution. |
| GET `/api/sets/{set_number}/contents-mapping` | Current/recoverable operation for this set and scope. |
| GET `/api/contents-mapping/{operation_id}`; POST suffix `/resume` | Read-only per-target/request/review status; explicit reconciliation and remaining authorized discovery only. |
| POST `/api/contents-mapping/{operation_id}/targets/{target_id}/review` | Candidate/proof digest, expected source/mapping state, idempotency UUID, approve/reject disposition. Approve requires a fresh signed review challenge expiring no later than the earliest operation, proof or display-eligibility deadline; recheck exact supported evidence and conflicts in transaction. Return original receipt on exact replay. |

Public models separate `SOURCE_BLOCKED`, `DISCOVERY_READY/PENDING/FAILED`,
`EVIDENCE_AMBIGUOUS/EXPIRED`, `REVIEW_READY/REJECTED/CONFLICT`, and `MAPPED`.
These states never imply `PRICED`. Safe conflict IDs/details remain visible; raw
responses, account scope, private paths and credentials never enter client contracts.

## 7. Data model, privileges and operational compatibility

**Propose one migration `0021_selected_component_mapping`.** An interface-only change
is insufficient: current `provider_discovery_evidence` persists only SET `NativeItem`
as `NORMALIZED_ITEM`; other discovery results live in memory. Existing CONTENTS guards
forbid identity dispatch and require verified price-target bindings. SET evidence has
one-attempt and one-mapping constraints inappropriate for shared component proofs.

- Add versioned `MAPPING` operation scope / `PRODUCT_CONTENTS_MAPPING` budget root
  to the existing `product_refresh_operation` framework. Retain SET/v1 and CONTENTS/v2
  behavior unchanged. Use the existing identity subgroup; price allowance is zero,
  no price views/jobs. Scope open-operation uniqueness by set and scope; extend close/
  context guards so zero price views cannot prematurely close pending mapping review.
- Reuse `product_refresh_target` with explicit MAPPING-only rules allowing unresolved
  mappings and binding exact canonical kind, variant/color, snapshot/source, inventory,
  occurrences and selection fingerprint. Existing pricing targets remain strictly
  verified. Store the resulting mapping only through the guarded review transition.
- Add `component_mapping_request`: immutable planned request node, constrained
  dependency selectors, realized exact selector, logical-request UUID and completion
  references. All attempts/costs remain solely in `provider_fetch_run` and existing
  `provider_budget_group`; this table schedules proof dependencies, not another ledger.
- Add `component_mapping_request_target`: request-to-target proof role/attribution,
  including shared COLOR, ITEM or KNOWN_COLORS reads. Enforce same operation and exact
  source-compatible membership. Distinct targets keep distinct review decisions.
- Extend `provider_discovery_evidence` with a scope-discriminated minimal component
  payload: exact ITEM; ELEMENT target list; COLOR ID/name/code/type; KNOWN_COLORS IDs;
  SUBSETS figure IDs, quantities, extras and alternate/counterpart facts. Preserve
  full ambiguity-relevant facts; oversized/incomplete evidence blocks proof rather
  than truncating away alternatives. Original SET shape/guards stay intact.
- Add append-only `component_mapping_review`: exact target/proof digest, source row
  and file digests, original attempt/evidence references and dates, validator version,
  reviewer/time/disposition, expected mapping state and resulting mapping revision.
  Link through mapping `evidence_reference`; do not force a multi-evidence proof into
  the legacy SET-only `discovery_evidence_id`. A retained-source binding records the
  old evidence date and new review date separately; no synthetic provider attempt.

Use owner-installed narrow SECURITY DEFINER capabilities for operation transitions,
evidence publication under a live attempt/lease, and supported binding admission.
Admission takes persisted operation/target/proof references, not arbitrary mapping
columns; it checks source membership, proof status, expiry, expected absence, both
canonical and provider selector conflicts, and replay inside the existing catalog,
provider and advisory lock discipline. Revoke PUBLIC execution, fix search paths,
enumerate grants and keep runtime mapping access SELECT-only outside these functions.
No owner credentials in API, broad mapping INSERT/UPDATE, or policy/DDL privileges.
Rejected/conflicted candidates must not be written through `review_mapping` with
`conflicted` state: that method can close accepted mappings. Preserve all existing
mapping history; replacement still requires its explicit predecessor review contract.

Update affected SQL/Python inventories in `market/{models,product_refresh_models}.py`,
`persistence/runtime_grants.py`, migration Python/SQL resources, `scripts/package_api.py`,
`market/{retention,product_refresh_retention}.py` traversal and exact schema/readiness
expectations. Extend `backup_format.py::IMAGE_REVISIONS`
head compatibility and affected backup/table inventories for 0021, retaining earlier
heads and the existing four-artifact format. Reuse the accepted `production_backup.py`
stream/timeout fix unchanged. This is compatibility work, not backup redesign or hardening.

Minimal live payloads keep the current policy-bounded lifecycle (currently no longer
than operation expiry and `min(86400, policy.retention_seconds)`). UI display uses its
separate eligibility deadline. Approved minimal mapping/review assertions follow the
existing mapping retention authority; raw API responses are not added. Expiry purges
payloads without deleting accounting or authorized review lineage; retain digests and
nullable evidence links/tombstones so purge cannot cascade into accepted mappings.
Retained evidence reuse is allowed only where its existing rights and exact facts
support it, not through a new general historical corpus or an expiry exemption.

## 8. Identity request plan, budget and cost control

Use **at most six new initial identity requests + two retries = eight attempts;
zero price requests**. The existing default interactive policy limit is eight; shared/global,
rolling-day, cooldown, suspension and rights restrictions can only reduce availability.
These are application ceilings, not provider entitlements or a promise of free calls.
Expose unavailable account cost/allowance honestly. Never raise policy limits to fit.

Build a bounded dependency graph from actual proof requirements. A cold part uses
ELEMENT → exact ITEM and KNOWN_COLORS, plus COLOR; a supported mapped-parent figure
uses SUBSETS → MINIFIG ITEM. If a dependent provider ID is not known before Confirm,
the signed plan names the source node and rule: **only the unique exact result**,
correct type/color and at most one dependent target. Display that conditional selector
and its maximum call count; never authorize a wildcard search or branch over candidates.
An ambiguous/empty/mismatched result stops its dependent nodes without consuming them.

Deduplicate equal provider/account/operation/full-parameter/adapter-policy keys and
compatible source proof bindings, retaining all target edges. Reuse only permitted,
compatible evidence with original dates and sufficient remaining eligibility. Pending
compatible work may be joined by reference to its original operation/logical request;
it retains its original budget attribution. No takeover or redispatch if a join fails:
expose failure and require an explicit new plan. Keep cross-operation dependency order
acyclic. Evidence reuse and joins consume zero new initials but are listed separately.

Let `I` be distinct non-reused authorized initial nodes, including conditional nodes,
`0 <= I <= 6`; `R = 2` when `I > 0`, otherwise zero; displayed maximum is `I + R <= 8`.
Show actual dispatched/skipped/remaining counts separately from that worst-case bound.
One cold part costs 4. Two colors sharing exact provider PART metadata/known-colors
cost 6 only when equality is already evidenced or the signed graph requires both unique
ELEMENT results to converge on that PART before shared downstream calls. Divergence
blocks that branch and requires replanning, never extra calls. Without that restriction,
the worst-case two-part graph costs 8 initials and is refused. Two different parts
sharing only COLOR cost 7 and are over cap. Quantity does not multiply calls.
Completed reusable proof may permit four targets at lower cost.
Insufficient current allowance makes the plan non-confirmable; no silent reserve loss.

The existing price Confirm remains **0 identity / 4 price / 2 retry**. Discovery approval,
binding review and price approval are separate actions and durable authorizations.

## 9. Conflict, replay, partial completion and recovery

Use the existing 15-minute signed confirmation and 24-hour execution window. The
digest covers selection/source/inventory, evidence identities/dates, graph/dependencies,
mapping state, policy/validator versions, reuse/join keys and limits. Recompute before
new confirmation. Check existing receipt first so a late exact replay returns its
original operation even after later catalog drift; altered payload/key reuse conflicts.

Reserve attempts durably before dispatch. Publish typed result and logical-node
completion atomically under matching lease/generation. Resume reconciles original
attempts before work: completed nodes never repeat; lost acknowledgements return stored
receipts; uncertain sends remain counted and can use only the existing remaining retry
reserve. No exact-once claim about an external provider response lost before persistence.
Never reset accounting, reopen a terminal root or silently create a replacement batch.

Targets complete independently. A valid target can be reviewed while another is
blocked/failed; review performs no provider calls. Discovery completion and review
disposition are separate: keep the operation paused with reason `MAPPING_REVIEW`
while eligible decisions remain, without reserving a dispatch lease. Close when all
targets are decided/blocked or the operation expires. Expired proof is unavailable for
new review; replan explicitly and reuse eligible completed facts without resetting
prior spend. Recheck status is read-only; failed polling means progress unknown.

Check source/snapshot/inventory, both identity namespaces/colors, parent mapping,
proof facts and current conflicts at review and before each dispatch. Material drift
blocks remaining work and requires a new plan; completed evidence retains its old
lineage. A concurrent exact mapping is reported already mapped after reconciliation;
a competing canonical or provider binding is a visible conflict, never an overwrite.
Review UUID+digest replay returns the same decision/mapping. Different decisions or
proof under the same UUID conflict; changing a rejected candidate requires a new
explicit plan/review revision. No bulk approval or automatic supersession.

## 10. Implementation sequence

Within one subsequently authorized slice, without routine reapproval loops:

1. Extract exact proof invariants and selected source resolver; implement typed graph,
   models and the single migration/capabilities with affected inventories/compatibility.
2. Wire bounded planner, shared discovery accounting/evidence, durable recovery and
   guarded review; add generated API contracts and the Contents review/handoff panel.
3. Run focused validation below once stable; resolve same-scope defects, update this
   plan with actual results, and obtain one independent review at the commit boundary.
   Implementation approval alone does not authorize staging, commit or deployment.

## 11. Focused validation and acceptance criteria

**No tests or builds during planning.** Later use existing pytest/PostgreSQL, frontend
test and browser harnesses; no new framework or full historical suite.

- Pure proof/planner checks: exact variants and both colors; known/unknown/ambiguous
  element; unique-parent versus multi-figure; unsupported IDs; old evidence date versus
  current binding; shared-request attribution and 4/6/7-call examples; no hard-coded seeds.
- Real isolated TEST PostgreSQL: mapping scope migration/ownership/grants and invalid
  capability inputs; concurrent canonical/provider conflicts using deterministic
  barriers; exact confirm/review replay, late replay after source drift, lost response,
  partial completion, uncertain attempt/retry exhaustion and stale lease fencing.
  Verify no direct runtime mapping write, no replacement of accepted mappings, and
  retained evidence expiry/purge compatibility with review/accounting lineage.
- API/component tests: private auth/origin/CSRF/no-store, wrong set/scope/target IDs,
  unsupported approval rejection, current-source drift, discovery/pricing separation,
  unchanged selected-price ceilings and mappings. Extend focused
  `tests/integration/test_contents_refresh.py`, discovery/accounting tests, and proposed
  `test_component_mapping.py`; preserve the two protected catalog test files.
- One meaningful synthetic desktop/narrow-viewport workflow using
  `apps/web/e2e/contents-acceptance.mjs`: supported new part, visible unsupported figure,
  displayed budget/Confirm, per-target review, reload/recovery and separate pricing
  handoff. Use a synthetic identity different from both accepted examples.
- Affected formatter/lint/type checks, contracts generation and web build; narrow
  migration/package/grant/retention/backup-head compatibility checks. Reuse unchanged
  adapter, valuation, image, backup-fix and prior phone evidence. No disaster-recovery
  rehearsal or new phone campaign. Repeat expensive checks only after relevant change.

SOURCE/TEST completion requires the supported path and honest blocked path, coherent
budget/recovery and privilege evidence, preservation of accepted mapping/price behavior,
and the reviewed source diff. It is not general catalog coverage or live completion.

## 12. Security, failure modes, rollback and later live gates

Existing Brian-only authentication, CSRF/origin rules, session clearing, attribution,
no-store and server-only provider credentials apply. No secrets/raw payloads/private
filenames in logs. Do not load provider credentials on read/plan/status. Bound normalized
payload sizes and reject incomplete proof. No physical or recognition assertions arise.

Later live activation requires separate deployment/provider-use approval, applicable
rights/retention and account/registered-IP/quota readiness, reviewed 0021 package/grants,
and the existing backup/readiness/rollback mechanisms. Preserve accepted backup evidence;
perform only checks the later approved deployment actually requires. This plan grants
no server, production, phone, provider or credential access.

Disable mapping dispatch/review if readiness fails while leaving cached Contents and
accepted pricing available. Roll back only through schema-compatible releases; do not
drop mapping/review history or delete accepted mappings. If compatibility prevents an
old binary rollback, keep writes disabled and correct forward under the deployment plan.

**Later bounded real-use completion:** Brian selects one additional supported real
target, neither `fig-012609/idea106` nor `3001/White15 → 3001/White1`. Prefer an exact-element
part found in the selected set; 10350-1 is optional. The deployed product must display
its actual identity plan, obtain in-app discovery/review approval, admit the exact
supported binding, and hand it to a separately confirmed existing price plan (one
Used/Sold view is sufficient). Record original evidence dates, actual requests/retries,
mapping receipt and price result. A provider failure is honest partial evidence, not
successful pricing. If no permitted authoritative source or eligible additional target
exists, stop with that exact blocker; no guessed mapping, expanded sweep or coverage claim.

## 13. Progress log and open manual checks

- [x] 2026-11-17: inspected local accepted main, relevant contracts and historical
  admissions; assessed parts and figures without live operations or requalification.
- [x] 2026-11-17: prepared one recommended plan; preserved 22 pre-existing pending
  paths, protected files, stopped capture and previous publications.
- [ ] Brian approves this grouped plan and explicitly authorizes implementation.
- [ ] SOURCE/TEST implementation and focused evidence; independent review/commit gate.
- [ ] Separate live activation approval and one additional supported real-use check.

No unresolved design choice is delegated to an ordinary per-item engineering task.
Outstanding evidence checks are exact additional-target eligibility and approved live
source use; no physical-device check is needed for the proposed shared UI source slice.

## 14. Outcome and follow-up

Planning only. This plan stays uncommitted on main with an empty index and no main
push. Only the sanitized planning package is authorized for publication under
`astra_response/Contents-Mapping/plan/r1/` on `astra-response`. No source/migration/
contract/dependency changes, tests/builds, service/database startup, mapping writes,
provider calls, exports, maintenance or deployment occurred. Unrelated dirty workflow,
roadmap and decision documents are preserved. Stop for plan approval; do not start
implementation, another mapping admission, price retrieval or alternative-sale economics.
