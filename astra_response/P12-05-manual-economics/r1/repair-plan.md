# ExecPlan 102 — Manual Deal Economics admission and compatibility review

## Goal and user-visible outcome

**BLOCKED — governing contract forbids MANUAL economics independent of market
admission.** P12-05 remains BLOCKED at Gate 5; Phase 12 remains IN PROGRESS.
The requested outcome is calculable user-entered sale assumptions while market
valuation remains UNKNOWN. No executable repair or new version is implemented.

## Why this work is being done now

The accepted P12-05 r2 production evidence recorded a MANUAL 200 forecast returning
UNKNOWN and null sale/gross/net/profit/ROI. Shipping and costs were recognized.
Brian authorized bounded diagnosis, compatibility review, source repair if its
contract conditions permit it, focused isolated validation and review publication.
The explicit stop condition applies when the governing contract does not support
MANUAL independent of market admission. Production interaction is prohibited.

## In scope

Trace calculation models, API/capture/persistence, replay, historical/index/revision
reads, fingerprints, UI, later phase contracts and normal expiry cleanup. Preserve
the existing blocker documentation; record the stop and publish its evidence.

## Explicit non-goals

No application/test changes, contract reinterpretation, new calculator, schema or
migration, provider activation, production login/preview/cleanup/deployment/restart/
backup, PWA/Android/rollback/VM acceptance, main commit/push or Phase 13.

## Current repository state

Main HEAD is `e64f2d812bf90255005c88e8d1f68b4c8ab0d7af`; the index is empty.
The existing CODEX_WORKFLOW, ROADMAP and Plan 099 blocker edits are preserved.
The three protected dirty files match their accepted SHA-256 values and remain
unstaged. Accepted production release context is `p12-05-catalog-repair-r1`, reused
from r2; production has not been accessed or freshly verified in this slice.
Catalog importer repair and catalog activation remain ACCEPTED / CLOSED.

## Decisions and assumptions

- Plan 071's accepted checkpoint explicitly forbids full dependent economics for
  PARTIAL/BLOCKED/UNKNOWN even with a manual sale assumption. VALUATION_RULES repeats
  this rule for exact replay; it is an accepted contract, not an accidental guard.
- Plans 073/075/076/077/079/081 and the Phase 8/9 extensions preserve that contract:
  fee assumptions, saving/revisions/indexes/defaults/frozen context/document memory
  do not authorize independent MANUAL admission.
- Path A fails both governing-contract and replay compatibility conditions. A
  guard change alters a valid historical MANUAL+UNKNOWN result from null economics.
- Future changed financial admission would require a separate execution version
  and recorded-version dispatch preserving V1. Path B is not implemented because
  the governing-contract stop condition applies before that work is authorized.
- This is not a finding that a larger schema redesign is unavoidable. Existing
  nullable amounts and MANUAL provenance can carry values, but accepted status/UI
  semantics explicitly couple full arithmetic availability to qualified evidence.

## Data model and API/interface changes

None. `whole-set-economics-v1` is the frozen execution contract, distinct from
`deal-economics-v1` / `purchase-limits-v1` result variants, `whole-set-snapshot-v1`
storage schema and `whole-set-usd-rounding-v1` rounding. Canonical snapshot bytes
persist calculation version, exact inputs, historical qualifications, expectations
and digest. Saved reads recompute with V1 and compare expectations; outputs are not
merely frozen display values. Unknown execution versions fail without fallback.
The digest includes every resolved field except itself, including execution
versions/request/basis/expected outputs. `basis_revision` is a separate identity
hash of valuation/evidence/policy inputs, not reconstructable history.

## Implementation sequence

1. Verify accepted HEAD/index/protected hashes and preserve prior documentation.
2. Trace governing contracts and authoritative runtime/replay/UI paths.
3. Stop executable repair on the explicit governing-contract conflict.
4. Confirm unchanged V1 and cleanup with bounded offline/owned TEST evidence.
5. Add only this plan and a minimal Plan 099 status note; publish a blocked review
   on `astra-response`, `astra_response/P12-05-manual-economics/r1/`.

## Validation and acceptance criteria

Current diagnostic evidence: 112 economics/snapshot unit tests PASS; two isolated
PostgreSQL expiry/bounded-cleanup integration tests PASS with cleanup ledger passed
and no leftovers. Four synthetic capture/encode/decode/replay cases PASS and retain
V1 versions/bytes. No source repair acceptance is claimed.

With MANUAL 200, purchase 100, charged shipping 10, fees 15, paid shipping 8,
other selling costs 2 and acquisition costs 5, unchanged V1 on a SUPPORTED fixture
returns sale 200.00, gross 210.00, selling costs 25.00, net 185.00, acquisition
105.00, profit 80.00 and ROI 76.2%. Its market amount remains the separate synthetic
180.05. With zero-observation UNKNOWN, MANUAL and SELECTED_MARKET retain UNKNOWN
and null sale/gross/net/profit/ROI; selling costs 25.00 and acquisition 105.00 remain.
The requested MANUAL+UNKNOWN behavior therefore remains undelivered.

The tests cover unsupported status/manual admission, exact supported MARKET and
MANUAL results, validation of invalid/missing money, zero acquisition, basis
identity, immutable/canonical payloads, unsupported versions, integrity/replay
mismatch and clock/Decimal independence. Existing expiry/change guards and UI
abort/generation checks are unchanged; no browser suite is rerun. Ruff/format/mypy,
builds and broad suites are not run because executable files are unchanged.

## Security, privacy, and data-integrity considerations

No production/development saved records were queried; absence of live history is
not assumed. Local test payloads use synthetic identities and prices. No provider
dispatch, credentials, owner/session access or private saved content is needed.
Public artifacts exclude private paths, identifiers and raw integration logs.

## Failure modes, rollback, and recovery

Changing V1 in place would invalidate expectation comparisons for admitted historic
captures, making reads fail closed rather than silently display new numbers. Leave
V1 and stored records intact. No operational rollback is necessary for this
documentation-only result. Failed publication must preserve main and prior reviews.

## Progress log

- [x] 2026-09-30: Accepted repository/protected-file guards passed.
- [x] 2026-09-30: Contract conflict and exact replay dependency identified.
- [x] 2026-09-30: 112 unit tests, four offline cases and two owned TEST cleanup
  tests passed; no leftover disposable databases.
- [x] 2026-09-30: Blocked plan/status and bounded review package prepared.
- [ ] Implement independent MANUAL admission: stopped on governing contract.
- [ ] Production continuation: not authorized by this repair slice.

## Open questions or physical-device/manual checks

A separate explicit decision must supersede the accepted qualified-basis admission
policy and define honest calculation availability versus market/physical
qualifications. Any subsequent implementation must preserve old V1 replay and
select/dispatch a new recorded execution version. No larger redesign or migration
requirement is established here. Device/production gates remain unrun.

## Outcome and follow-up

Exact admission change: none. Migration required for this stopped slice: no.
Current production's previously reported ordinary UNSAVED preview is untouched.
The existing guard prevents premature/saved deletion; owner-scoped cleanup removes
only expired unsaved captures, at most 100 per call, on a later normal preview.
The isolated expiry test proves the pending state, normal deadline, refusal to save
after expiry, cleanup on preview and protection of saved history. This is TEST
evidence, not a claim that production cleanup has occurred.

Current slice changes only this plan and the minimal Plan 099 note. Existing
workflow/roadmap/blocker prose and protected modifications are preserved. Review
publication is authorized on the isolated artifact branch; main remains uncommitted
and unpushed. P12-05 Gate 5 and Phase 12 status remain unchanged.
