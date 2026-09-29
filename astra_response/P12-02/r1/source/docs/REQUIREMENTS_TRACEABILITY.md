# Requirements Traceability

## Phase 9 final physical qualification accepted — 2026-09-26

The final accepted device run in
[ExecPlan 088](plans/088-android-https-auth-source.md) closes Phase 9 and the
Phase 9 portion of R-07 and R-09. It added physical proof for all five
market-evidence expiry profiles and the one-shot uncertain Watchlist mutation
to the previously accepted transport/authentication, shared core-flow,
saved-work, offline/reconnect, session-expiry, and fresh-process privacy
evidence. The device honored server deadlines, did not revive stale evidence,
did not replay the uncertain write, and reconciled the single committed
revision-1 row by authoritative readback. No live provider was contacted, and
active qualification resources were cleaned up. R-07 remains partial only for
its separate Phase 16 actual-outcomes scope. Phase 10 is **NEXT / NOT STARTED**.

## Historical Phase 9 physical Android qualification — 2026-09-23

The separately authorized and accepted bounded phone pass in
[ExecPlan 088](plans/088-android-https-auth-source.md) **PASSED** on the
unchanged APK: direct USB TLS, exact Host/Origin/CORS, private login/session,
Settings and Watchlist reads, CSRF settings save, deadline headers, no-store,
passive resume, read-only offline memory, explicit reconnect verification,
fresh-start privacy and logout. No live provider or source change was involved;
owned TEST resources, reverse forwarding and temporary trust were removed.

**R-09 and Phase 9 remain PARTIAL/OPEN** under the existing roadmap gate for
physical Android core workflows and auth/cache expiry/sync conflicts. Search,
set detail, deal analysis, saved-work flows and on-device expiry/conflict cases were outside this
bounded phone pass. The Phase 9 cache/reconnect portion of R-07 has accepted
source and bounded physical evidence, while R-07 overall also retains its
separate Phase 16 actual-outcomes scope. Earlier device-unverified status below
is historical. Phase 10 local release hardening follows Phase 9 closure.

## Phase 9 Slice 3B source qualification - 2026-09-23

Brian authorized the implementation and source checks in [ExecPlan 088](plans/088-android-https-auth-source.md).
**Slice 3B is CLOSED for its accepted local source checkpoint; Slice 3A is
CLOSED; Phase 9 remains OPEN.** Brian authorized the reviewed 33-file local
commit from `bd6a97f49ab1d08e8b6debab09e5338558285eb8`, subject
`Complete Phase 9 Slice 3B secure Android transport qualification`. This
supersedes earlier source-review and unauthorized status.

An explicit qualification build uses `https://localhost` to
`https://localhost:18443`, exact credentialed CORS and owned TEST direct TLS.
Normal browser/PWA builds remain same-origin. Existing cookies, CSRF, session
limits and private document-memory policy remain authoritative. Official native
resume verification is passive; backup/device transfer are excluded, and extra
localhost trust is an explicit debug-only public-certificate input.

Trusted Chromium with real disposable PostgreSQL and Android debug packaging
passed. This is not WebView/device proof. Brian manually removed the temporary
Windows TEST trust certificate; six trust stores and owned TEST resources were
verified clear. The plan records the exact cleanup and source evidence.
Final physical-device qualification remains NOT STARTED and separately authorized.
No phone, ADB, LAN, provider, development database/service, deployment
or push occurred. This acceptance closes only the Slice 3B source checkpoint.

## Phase 9 Slice 3A accepted source/build checkpoint — 2026-09-23

**Slice 3A ACCEPTED / CLOSED FOR ITS SOURCE/BUILD CHECKPOINT.** Brian accepted
[ExecPlan 087](plans/087-android-build-readiness.md) and authorized exactly six documentation files for one
local commit, `Record Phase 9 Slice 3A Android build readiness`, with parent
`9951cc8db5775b229637837ca3e520478f2e8662`. This acceptance supersedes the
review-pending and no-commit status below. Slice 3 overall and Phase 9 remain
IN PROGRESS; Slices 1–2 remain CLOSED.

The existing pinned stack built the accepted debug APK without application,
configuration or version changes. Its exact toolchain, user-local paths, APK
SHA-256 and static facts remain recorded in the plan. The initial Gradle
cache-directory move failure and unchanged successful diagnostic rerun remain
historical evidence; the filesystem cause is unconfirmed. No compatibility
exception was established. Closeout performs lightweight documentation/Git/hash
checks only, with no build, test, tooling installation or incident investigation.

Next: **Phase 9 Slice 3B — Secure USB HTTPS Transport and Android Authentication
Source Qualification — NOT STARTED / NOT AUTHORIZED.** Its future scope is explicit
API base resolution, exact native Origin/CORS support, TEST-only direct TLS,
qualification trust, lifecycle integration and privacy/backup exclusions. The
selected transport/security design remains recorded only in ExecPlan 087.
Physical-phone qualification remains NOT STARTED and requires separate approval
after source/transport readiness review. No operational/network/device work,
development migration, deployment or push is authorized by this checkpoint.

## Phase 9 Slice 3A authorized — Android Build Readiness — 2026-09-23

**Slice 3 IN PROGRESS, bounded to Build Readiness; Phase 9 remains IN PROGRESS.**
[ExecPlan 087](plans/087-android-build-readiness.md) records the accepted conservative toolchain strategy,
user-local setup and build evidence. Slices 1–2 remain CLOSED. This entry
supersedes older statements that Slice 3 is unstarted or entirely unauthorized.

Keep Node 24.14.0, pnpm 11.8.0, Capacitor 8.5.2, Gradle 8.14.3, AGP 8.13.0,
compile/target SDK 36, minimum SDK 24 and Java 21. Only required user-local JDK 21,
SDK tools/packages, licenses, dependency downloads and debug packaging are
approved. Wholesale latest-stable modernization is explicitly deferred.

No transport/auth/security-policy changes, TLS, endpoint/service/database/provider
operations, device/emulator/ADB use, staging, commit, push or deployment.
Static package/build evidence cannot satisfy R-09 physical Android acceptance;
R-07 and R-36 retain their existing remaining scope. The accepted next-stage
transport design is recorded only in ExecPlan 087 and requires separate execution
authorization. Neither Slice 3 nor Phase 9 closes at build readiness.

Build readiness is ready for review: the existing stack produced and statically
verified a debug APK with no application/configuration or version changes. The
plan records its SHA-256, installed tools, initial cache-move failure and successful
diagnostic rerun. Transport, authentication and physical-device evidence remain
outstanding. Documentation and ignored build evidence only; no commit.

## Phase 9 Slice 2 accepted source checkpoint — 2026-09-23

**Slice 2 ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 9 remains
IN PROGRESS.** Brian accepted the implementation, technical evidence and supplied
visual evidence in [ExecPlan 086](plans/086-private-memory-reconnect.md). Slice 1 and Phases 7B/7C/8 remain CLOSED.
This entry supersedes the earlier Slice 2 implementation/review status below.
The authorized local checkpoint contains the reviewed 25-file candidate plus
normal closeout amendments within that same file set. Parent:
`d50f97a203ed9a61e0e5430a4fe85f6fe0f97817`. Subject:
`Complete Phase 9 Slice 2 private offline views and safe reconnect`.

Document-memory private views, public-shell-only service-worker storage, existing
30-minute idle/12-hour absolute session policy and server market-display deadlines
remain unchanged. Offline viewing never renews activity; remote revocation cannot
be discovered until transport returns or the last confirmed deadline expires.
Reconnect verifies first, preserves Deal inputs and never retries mutations.
Watchlist uncertain target/removal outcomes require explicit authoritative read-back.
No database migration or generated contract change; sole head is `0016_hunt_cached_runs`.

Slice 3 — Android Core Qualification — is next, NOT STARTED and NOT AUTHORIZED.
It requires a separately reviewed design for Capacitor `https://localhost`, API
URL/transport, desktop loopback incompatibility, Host/Origin and SameSite/Secure
cookies; JDK 21/Android SDK 36 prerequisites and physical-device authentication,
networking and offline/reconnect qualification remain outstanding. Security and
network exposure must not be loosened to bypass those gates. Full Phase 9 remains
open pending that evidence; R-07 remains partial for later Phase 16 outcomes.
No acceptance rerun, development migration, service/database operations, provider
activity, Android work, deployment or push is part of this closeout.

## Phase 9 Slice 2 authorized — 2026-09-23

**Slice 2 IN PROGRESS.** [ExecPlan 086](plans/086-private-memory-reconnect.md) implements dated
read-only document-memory views and safe reconnect. Brian authorized implementation,
focused validation and owned TEST services; stop for technical/visual review,
without staging or commit. Slice 1 and Phases 7B/7C/8 remain CLOSED. Phase 9 remains
IN PROGRESS; Slice 3 is not started. Earlier Slice 2 prohibitions are historical.

Private data never persists across reload/restart. Only previously authenticated
reads may fall back, within the last confirmed session deadline. Offline use and
passive checks never renew activity. An offline client cannot discover remote
revocation immediately; expiry/logout/principal replacement clear memory.
Reconnect verifies first, rereads visible resources, preserves drafts and never
retries writes or dispatches providers. Watchlist uncertain target/removal writes
require explicit authoritative read-back. No migration, durable private store,
generic sync or offline economics. R-07/R-09/R-36 retain their remaining scope;
Phase 16 and Deferred Economics are unchanged. No development DB/site, provider,
network exposure, Android or deployment work.

## Phase 9 Slice 1 accepted source checkpoint — 2026-09-23

**Slice 1 ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 9 IN PROGRESS.**
[ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md) records Brian's
technical/visual acceptance and authorized local commit. Public shell alone may
persist; API/auth/private responses remain no-store and outside worker caches.
Offline restart restores no private records. Updates are explicit and preserve
active drafts until Brian chooses reload. No migration; head remains
`0016_hunt_cached_runs`. Capacitor 8.5.2 generation/sync is source feasibility only;
no native/device/deployment acceptance or network/authentication relaxation.

Brian confirmed he accidentally closed both development processes: the listener
incident is resolved, no tooling defect is implicated, and no restart/investigation
is needed. Prior separate validation selections and initial corrections stand.
Slice 2 is next, NOT STARTED / NOT AUTHORIZED; Slice 3 remains later and unstarted.
No private durable store, offline writes, generic sync or provider/background
refresh. R-07/R-36 remain partial; Phase 16 and Deferred Economics boundaries
are unchanged. Earlier Slice 1 in-progress/review-pending statements are historical.

**2026-09-23 — Phase 9 Slice 1 IN PROGRESS:**
[ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md) implements the R-09
online PWA/public-shell and bounded native feasibility portion. Private APIs stay
no-store. R-07's private cache/reconnect portion remains Slice 2 and actual outcomes
remain Phase 16; R-07 is still PARTIAL. Physical Android remains Slice 3; R-09 is
not closed. Bounded Phase 8 stays closed, full R-36 partial and Deferred Economics
outstanding/unassigned. Older Phase 9 authorization statements are historical.

## Phase 8 bounded milestone acceptance — 2026-09-23

**Slice 2 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT. Phase 8 is ACCEPTED /
CLOSED FOR ITS BOUNDED SOURCE MILESTONE; full R-36 remains PARTIAL.**
[ExecPlan 084](plans/084-hunt-frozen-evidence-context.md#source-checkpoint-acceptance--2026-09-23)
records accepted implementation, technical evidence and supplied visual evidence.
The prior table's Slice 2 diagnostics are now delivered and accepted: explicit
quality, coverage, concentration, bounded contributors, raw activity/proxy and
existing Liquid/Fast Cash/dead-stock context. Slice 1's profit, ROI, maximum purchase,
signed headroom, qualification/freshness, transparent sorts and immutable history
remain accepted. No composite Hunt score or component-driven financial reorder exists.

The unsupported, calibration-dependent, undelivered and deferred rows below remain
outstanding/unsatisfied: composite ranking/Gem/distribution/calibrated weighting;
seller concentration/global rarity/unsupported-duration metrics; POV premium/scoped
catalog presence/theoretical gross target-prefix; recovery/burden/expected recovery/
recoverable-gross density/economic break-even lots and all Deferred Economics
Extensions. None is satisfied, cancelled or implicitly moved to Phase 9 or Phase 16.
Phase 9 cache/sync is next but NOT STARTED / NOT AUTHORIZED. Earlier pending status
is historical; milestone closure does not replace full R-36 requirements.

## Phase 8 bounded milestone — Slice 2 authorized, 2026-09-22

The [accepted decision](DECISIONS.md#phase-8-bounded-milestone-and-frozen-evidence-context--2026-09-22)
narrows Phase 8 source acceptance to cached whole-set screening plus frozen existing
component context. [ExecPlan 084](plans/084-hunt-frozen-evidence-context.md) is
IN PROGRESS. Slice 1 and 7B/7C remain CLOSED. Phase 8 remains IN PROGRESS and full
R-08/R-36 remains PARTIAL, even if the bounded milestone later closes.

| R-36 family                                                                                                                                  | Current delivery boundary                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Profit, ROI, Maximum Purchase/Buy Under, signed headroom                                                                                     | SATISFIED by Slice 1 under supported whole-set assumptions.                                                 |
| Whole-set qualification, freshness, transparent versioned ordering, immutable history                                                        | SATISFIED by Slice 1.                                                                                       |
| Explicit quality, occurrence/quantity coverage, concentration, raw activity/proxy, bounded contributors, Liquid/Fast Cash/dead-stock context | Implemented/frozen in Slice 2; technical and visual acceptance pending.                                     |
| Velocity/months supply/absorption with unavailable duration; seller concentration; global rarity                                             | Unsupported evidence; outstanding and unsatisfied.                                                          |
| Gem policy, calibrated composite ranking, broader distribution policy                                                                        | Calibration/policy-dependent; outstanding and unsatisfied. No composite score required for bounded Phase 8. |
| POV premium, scoped presence integration, theoretical gross target-coverage prefix                                                           | Undelivered non-economic concepts; outstanding and unsatisfied, excluded from Slice 2.                      |
| Expected recovery, recovery/burden, recoverable density, economic break-even lots and all other Deferred Economics Extensions                | Explicitly deferred/outside this Phase 8 milestone; outstanding/unsatisfied, no new delivery phase.         |

The broad historical R-36 phase/score rows below retain product intent; this decision
governs current milestone completion. No missing component is silently satisfied,
cancelled or replaced by a proxy. Liquid/Fast Cash remain uncalibrated gross
application scenarios; dead-stock exposure is classified value, not predicted loss.

## Phase 8 Slice 1 source acceptance — 2026-09-22

**Slice 1 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 8 remains
IN PROGRESS. Phase 7B and Phase 7C remain CLOSED.** [ExecPlan 083](plans/083-hunt-cached-whole-set-run.md)
records Brian's technical/visual acceptance and distinct validation selections.
Earlier Phase 8 unstarted statements describe prior checkpoints.

R-08/R-36 is PARTIAL: the accepted cached whole-set screener supports up to 20
user-selected canonical sets from Watchlist or explicit catalog search, explicit
ASKING_PRICE/HYPOTHETICAL_TARGET/NONE scenarios, existing whole-set economics,
independent NEW/USED × SOLD/STOCK evidence, SUPPORTED/PARTIAL/BLOCKED/UNKNOWN,
transparent sortable metrics and immutable historical runs with current evidence
not checked. Watchlist targets are never automatic. Seller-listing discovery,
provider dispatch and actual purchase/outcome records are outside this slice.

Composite/calibrated ranking, Gem/rarity/competition/burden and other unsupported
R-36 components remain unresolved or deferred under governing scope. Before another
implementation slice, review what existing evidence can honestly satisfy, what
needs calibration/policy, what requires unavailable evidence and what overlaps the
explicitly Deferred Economics Extensions register below. A composite score is not
assumed required; no invented weights or calibrated expected proceeds/probability
claims follow from acceptance. Extensions remain outstanding, deferred, unsatisfied
and without a delivery phase. Phase 9 cache/sync and Phase 16 outcomes remain
separate. No next implementation is authorized.

## Phase 7C source acceptance and reconciliation — 2026-09-22

Phase 7C Slices 1–4 are ACCEPTED / CLOSED FOR THEIR SOURCE CHECKPOINTS, and Phase
7C is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT. [ExecPlan 079](plans/079-saved-deal-index.md),
[080](plans/080-watchlist-targets.md), [081](plans/081-settings-selling-profiles.md),
and [082](plans/082-notes-source-urls.md) record the Saved Deal Index,
Watchlist/targets, settings/profiles, and Watchlist plus lineage notes/source URLs.
Slice 4 annotations use owner-scoped revision/CAS
contracts and stay outside immutable forecast payloads, digests, replay, timestamps
and calculations. Source URLs are inert HTTP(S) references, not verified evidence.

The original full web result was 149 passed / 6 failed. The six authentication cases
reproduced at the accepted Slice 3 baseline because an existing mock returned null
from the newly required settings request, while the actual absent-settings contract
returns revision-zero defaults. The test-only mock correction passed the focused
Authentication, Profiles, Forecast and Watchlist selection 44/44; the full web suite
was not rerun. This is a stale test fixture exposed by accepted Slice 3 behavior, not
a Slice 4 regression or a production null-settings requirement.

No in-scope Phase 7C source requirement remains unmet. R-07 remains PARTIAL overall:
cache/synchronization and actual purchase/resale outcomes remain assigned to Phases
9 and 16. Phase 8 Hunt is the next roadmap phase but remains unstarted and
unauthorized. Deferred Economics Extensions remain outstanding, deferred, unsatisfied
and without a delivery phase; they are not a Phase 7C acceptance gap. Operational,
deployment, account/device and external-provider qualification is separate and was
not performed.

## Phase 7C Slice 4 implementation in progress — historical status, 2026-09-21

The following dated record preserves the implementation-time status before technical
and visual acceptance. Current acceptance and reconciliation are above.

## Phase 7B source-acceptance reconciliation — 2026-09-18

**7B-4 is ACCEPTED / CLOSED; Phase 7B is ACCEPTED / CLOSED FOR ITS SOURCE
CHECKPOINT.** [ExecPlan 077](plans/077-forecast-revisions.md#source-checkpoint-acceptance-and-phase-7b-reconciliation--2026-09-18)
maps the governing [Phase 7 internal boundaries](ROADMAP.md#phase-7--deal-calculator-and-saved-work)
and accepted whole-set scope to accepted 7B-1–4 evidence. Private authentication,
durable original save/reload, exact historical financial reproduction after live
source change/purge, immutable URLs and append-only revisions with explicit
conflicts satisfy the in-scope source criteria. No source-acceptance gap remains.

This closes the 7B saved-forecast/auth/revision portions of R-07 and the accepted
whole-set saved-replay portion of R-05. It does not mark all R-07 complete:
watchlist, persistent targets/settings, saved-set/notes/URL metadata and Saved Deal
Index retain 7C ownership; later cache/sync and actual outcomes retain Phases 9/16.
7C Slice 1 Saved Deal Index is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT under
[ExecPlan 079](plans/079-saved-deal-index.md), and 7C Slice 2 Watchlist and Targets
is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT under [ExecPlan 080](plans/080-watchlist-targets.md).
Phase 7C remains IN PROGRESS. Settings/Profiles Slice 3 is ACCEPTED / CLOSED FOR ITS
SOURCE CHECKPOINT under [ExecPlan 081](plans/081-settings-selling-profiles.md).
Notes / Source URLs is the next planned slice, not started or authorized here; Phase 8 remains
unstarted. Phase 7 overall remains incomplete, and the Deferred Economics Extensions
register below remains outstanding, deferred, unsatisfied and without a delivery phase.

The accepted technical selections and visual provenance remain separate in
ExecPlans 074–077; no combined clean full-suite pass is asserted. The 7B-1 signed-in
header manual-review limitation remains nonblocking as previously accepted.
Development-database migration, actual-account provisioning, deployment and
device/HTTPS qualification remain deferred and unperformed, not passed or newly
introduced source-checkpoint criteria. Earlier dated status records and original
requirement rows retain their historical context; this entry updates only the
completed source scope.

**Checkpoint 2 now authorized:** [ExecPlan 076](plans/076-save-original-forecast.md) records acceptance of
checkpoint 1 for onward integration and bounded API/replay implementation. Earlier
checkpoint-1-only stops below are historical. UI, deployment and commit remain
unauthorized; 7B-3 is IN PROGRESS.

**Current checkpoint authorization:** [ExecPlan 076](plans/076-save-original-forecast.md) authorizes only
7B-3 checkpoint 1, backend Persistence and Save Authority, with synthetic TEST
validation and technical review. Earlier planning-only boundaries below are historical
for this authorization. 7B-3 remains in progress; API/UI and commit are not authorized.

**Current 7B-3 boundary — 2026-09-17:** The [owner decision](DECISIONS.md#phase-7b-3-owner-retention-and-historical-display-authorization--2026-09-17)
clears private snapshot retention/historical display and supersedes older unresolved
permission gates below. 7B-1/7B-2 are ACCEPTED / CLOSED; Phase 7B is OPEN. Only
decision documentation and 7B-3 planning are authorized; implementation remains pending.
R-07 saved work remains unsatisfied until its separately authorized implementation.

## Phase 7B-2 source checkpoint accepted / closed — 2026-09-17

**7B-2 is ACCEPTED / CLOSED for its source checkpoint.** 7B-1 remains CLOSED;
Phase 7B remains OPEN. Brian accepted the implementation and recorded validation.
This is not deployment or operational qualification. The next boundary is the
retention/display-permission review **before 7B-3**. Provider-backed persistence
remains blocked pending that determination; permission is neither established nor
prohibited. No permission research or later-slice work is authorized by this closeout.

Acceptance and the unchanged 16-file inventory are recorded in [ExecPlan 075](plans/075-exact-snapshot-replay.md).
R-07 saved work and provider-backed persistence remain unsatisfied.

7C, Phase 8 and all Deferred Economics Extensions remain unchanged. The extensions
remain outstanding, deferred, unsatisfied and without an assigned delivery phase.
Earlier pending-review/no-commit entries below preserve their historical checkpoints.

## Phase 7B-2 — conditional replay implementation, 2026-09-17

[ExecPlan 075](plans/075-exact-snapshot-replay.md) supplies a synthetic internal
reproducibility prerequisite for R-07: exact whole-set financial inputs, frozen
execution versions, canonical snapshots and recomputed output comparison. Original
physical/valuation/evidence-quality and eligibility assertions remain historical;
this is not independent evidence reconstruction. Public economics remain unchanged.

7B-2 is implemented pending technical review, not accepted/closed. R-07 saved work,
provider-backed historical retention/display and persistence remain unsatisfied.
7B-1 stays closed. 7C, Phase 8 and the Deferred Economics Extensions register remain
unchanged; the deferred requirements have no new assigned delivery phase.

## Phase 7B-1 source-checkpoint acceptance — 2026-09-17

R-07's Brian-only authentication slice is **ACCEPTED / CLOSED** under
[ExecPlan 074](plans/074-brian-only-authentication.md), with the recorded nonblocking
manual signed-in-header review limitation. R-07 and Phase 7B as a whole remain open;
saved/reproducible work is not satisfied. **7B-2 is next, not authorized.** Provider-backed
history retains its unresolved retention/display-permission gate. All Deferred
Economics Extensions remain outstanding, deferred, unsatisfied and without a delivery
phase. Acceptance is for source only, with no operational or deployment qualification.

## Phase 7B-1 bounded implementation — 2026-09-17

R-07's Brian-only authentication portion is implemented for review under
[ExecPlan 074](plans/074-brian-only-authentication.md): owner bootstrap/reset,
Argon2id, revocable expiring sessions, CSRF and protected existing product routes,
with an expiry/logout UI boundary. This is not acceptance of all R-07 or Phase 7B.
Saved work, reproducible snapshots/receipts/replay, revision UI and the Saved Deal
Index remain unimplemented proposals. No provider retention/display permission is
inferred. Deferred Economics Extensions remain outstanding/deferred/unsatisfied
with no assigned phase; 7C and Phase 8 are unchanged.

## Phase 7A2 whole-set closure — 2026-09-17

**Phase 7A2 Whole-Set Deal Economics: COMPLETE / ACCEPTED / CLOSED.**

Brian's [post-acceptance scope decision](DECISIONS.md#phase-7a2-whole-set-closure-and-explicit-deferral--2026-09-17)
closes the accepted Slice 1/2A/2B whole-set portions of R-05/R-06 only. It does not
complete the broader contents, strategy, recovery or lot-economics requirements.
The register below supersedes older 7A2 ownership and phase-range rows for these
outstanding portions; older acceptance records retain their historical meaning.

### Deferred Economics Extensions

All rows are **OUTSTANDING / DEFERRED, NOT CANCELLED, NOT SATISFIED**. This named
future economics bucket is outside closed 7A2, has no assigned delivery phase,
and requires separate planning/authorization. It is not transferred to Phase 8
or included automatically in 7B/7C. IDs and original requirement history remain.

| Deferred capability                  | Retained requirement IDs                       | Why excluded from closed whole-set scope                                                                                 | Blocker or prerequisite retained                                                                                                                                                              |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Missing/damaged contents adjustments | R-06; R-13 physical integrity                  | Accepted whole-set sale/cost assumptions do not implement actual-content overlays.                                       | Explicit actual/absent quantities and condition evidence; supported adjusted-value or replacement basis; no physical or cost double counting.                                                 |
| Minifigure quantity adjustments      | R-04/R-06; R-13                                | Catalog quantities/totals are not adjusted deal quantities/totals.                                                       | Nonoverlapping physical unit groups, repeated/mixed-condition quantities, catalog-versus-actual reconciliation and coverage.                                                                  |
| Instructions/box/build adjustments   | R-06/R-33                                      | Shipping/cost fields do not model missing packaging, instructions or incomplete/residual builds.                         | Declared inclusion/completeness, physical allocation and explicit adjusted/residual sale evidence or qualified assumptions.                                                                   |
| Figures + remaining-build economics  | R-33; R-05/R-06                                | Whole-set estimates and theoretical figure/component values are not split-sale proceeds.                                 | Admitted disjoint allocation; explicit residual-build sale basis or validated conservative policy; separate selling costs. Whole-set minus theoretical figure value is not residual evidence. |
| Full component part-out economics    | R-33/R-15; R-05/R-06                           | Theoretical POV does not establish recoverable gross, net proceeds or purchase limits.                                   | Accepted physical expansion/allocation, compatible prices, supported recovery and order/cost evidence; intact figures and their components cannot both count.                                 |
| Recovery/burden models               | R-15/R-28/R-29/R-30; economic use of R-23/R-24 | Existing uncalibrated Liquid/Fast Cash gross scenarios and counts do not satisfy validated recovery or burden economics. | Supported horizon/sold-fraction/realized-price assumptions, physical/lot denominators and calibrated burden/order/labor policy; no invented coefficients, orders or hours.                    |
| Economic break-even lots             | R-27; R-33 strategy context                    | Accepted whole-set break-even is a purchase-price ceiling, not a ranked subset of sale lots.                             | Supported physical lots, recovery and ranking/tie policy; subset incremental/fixed selling costs so subset net covers acquisition. Gross target coverage is not economic break-even.          |

Existing theoretical/scenario acceptance remains intact; only the outstanding
economic/adjustment portions are deferred. R-07 authentication/saved work remains
7B/7C; R-08/R-36 Hunt remains Phase 8, without receiving the deferred requirements.

7B can persist the accepted whole-set model without first implementing this bucket.
It must resolve the [frozen snapshot/version and retention questions](DATA_MODEL.md#7b-persistence-questions--unresolved)
and distinguish original historical forecasts from current-evidence recalculation.
No 7B implementation or retention permission follows from 7A2 closure.

## Phase 7A2 Slice 2B — accepted checkpoint, 2026-09-17

**Selling Fee Rules: COMPLETE / ACCEPTED / CLOSED. Brian technical PASS; visual PASS.**
Brian authorizes one local commit on main, subject
`Complete Phase 7A2 Slice 2B Selling Fee Rules`, parent
`8cbffb06baeb78d7c71abdeedfbbd1d5e86f646a`.
[ExecPlan 073](plans/073-selling-fee-rules.md#final-acceptance-and-checkpoint--2026-09-17)
records the final invariant review, validation and exact 21-file checkpoint scope.
Slice 1 and 2A remain accepted; protected unrelated files remain excluded. No push,
later provisional 7A2 work or later-phase authorization. Phase 7A2 overall remains
open. Earlier pending-review and no-commit statements below are historical.

## Phase 7A2 Slice 2B — bounded fee assumptions, 2026-09-17

[ExecPlan 073](plans/073-selling-fee-rules.md) extends bounded R-05/R-06 economics
with exclusive manual or calculated selling/payment fees. It covers two explicit
fee bases, exact percentage arithmetic, one HALF_UP charge boundary, optional fixed
fee and propagation into net/profit/ROI and all accepted purchase limits. Required
evidence, stale/revised-basis checks and transient Deal lifecycle remain unchanged.
No broader marketplace/order/tax schedules or remaining provisional 7A2 requirements
are satisfied by this slice. Technical/visual acceptance is recorded separately.
Implementation and full technical validation PASS; Brian acceptance remains pending.

## Phase 7A2 Slice 2A acceptance — 2026-09-17

Brian accepted the bounded purchase-limit portions of R-05/R-06 technically and
visually. [ExecPlan 072](plans/072-purchase-limits.md) records final invariant review,
the currency-only disclosure correction, validation and exact checkpoint inventory.
No requirement is broadened: 2B selling-fee rules and provisional later 7A2 work
remain unstarted; 7B/7C persistence and Phase 8 Hunt remain deferred.

## Phase 7A2 Slice 2A — technical evidence, 2026-09-17

The bounded purchase-limit requirements below are implemented and technically
validated; [ExecPlan 072](plans/072-purchase-limits.md) records domain, API, database,
contract, lifecycle and responsive evidence. Brian visual review remains pending.
2B and all other deferred requirements remain unstarted.

## Phase 7A2 Slice 2A — bounded R-05/R-06 purchase limits, 2026-09-16

[ExecPlan 072](plans/072-purchase-limits.md) covers transient enabled ROI/profit
targets, signed constraint caps, feasible maximum purchase, binding targets,
asking-price headroom and whole-set break-even purchase ceiling. Fixed acquisition
costs and independent purchase-price tax/premium percentages use exact server math.
Legacy Slice 1 schemas remain unchanged; the same endpoint accepts an opt-in analysis.
Unknown asking price leaves asking-dependent outputs null. Infeasible, disabled,
no-target and unavailable states remain distinct, alongside existing evidence states.
No manual/active-listing assumption upgrades evidence; freshness/revision and draft
lifecycle protections apply to all limits.

This does not complete all R-05/R-06 or R-27/R-33. R-27 part-out break-even lots,
contents/condition adjustments and alternative-strategy economics remain provisional
later 7A2 work. 2B selling-fee rules require separate authorization after 2A review.
R-07 persistence/auth/settings/indexes remain 7B/7C; R-08/R-36 Hunt remains Phase 8.
Technical and visual acceptance are recorded separately in ExecPlan 072.

## Phase 7A2 Slice 1 acceptance — 2026-09-16

The bounded R-05/R-06 implementation in [ExecPlan 071](plans/071-whole-set-deal-economics.md)
is technically and visually accepted by Brian. Closeout reconfirms exact server
valuation consumption, four independent views, support/freshness qualifications,
transient drafts, no provider dispatch or persistence, signed results and undefined
zero-cost ROI. Phase 1–6 evidence rules and the accepted 7A1 lifecycle remain intact.
This closes Slice 1 only; broader R-05/R-06, Slice 2 and later phases remain separate.

## Phase 7A2 Slice 1 — bounded R-05/R-06 implementation, 2026-09-15

[ExecPlan 071](plans/071-whole-set-deal-economics.md) implements whole-set asking,
explicit expected sale, manual shipping/fees/other selling and acquisition costs,
gross/net/profit/ROI through a read-only exact server calculation. The new Deal
section preserves four market views, evidence support and the 7A1 lifecycle.
Revision conflicts/expiry invalidate results; manual/active-listing assumptions
remain labeled; zero acquisition has undefined ROI. Acceptance includes exact
arithmetic, full-table PostgreSQL immutability, no provider activity and responsive
browser/component lifecycle tests. Actual results are recorded in ExecPlan 071.

This is not completion of all R-05/R-06: targets/max-buy/headroom/break-even and
complex fees remain Slice 2; contents adjustments remain later provisional work.
R-07 persistence/auth and R-08/R-36 Hunt remain separate. No new schema or provider
authorization is implied. 7A1 acceptance is unchanged; Slice-1 visual acceptance
remains pending.

## 7A1 product-hero revision mapping - 2026-09-15

The newer authorization adds only an optional exact-set Rebrickable image descriptor
to the existing appraisal read model and replaces the presentation with a product
hero and four independent market cells. This supersedes the earlier presentation-only
boundary below for this specific read projection. Source identity/provenance, null
absence, no additional catalog fetch, unchanged financial/physical rules, private
non-commercial scope and the existing R-35 refresh lifecycle are covered by
[ExecPlan 070](plans/070-set-detail-information-architecture.md). No new requirement
completion, ingestion subsystem or 7A2 functionality is implied.

## Accepted 7A1 refinement mapping - 2026-09-15

[ExecPlan 070](plans/070-set-detail-information-architecture.md) implements presentation only: R-02/R-11/R-12 in Overview/Market; accepted R-03/R-04/R-13/R-14 fields in Contents; R-15/R-23-R-26 existing scenario presentation in **Value Scenarios**; R-35 confirmation/recovery/polling across every context change; R-37 progressive sections. Evidence owns references, dates/windows, policies and detailed limitations. Expiry removes every appraisal-derived surface, including collapsed content. No broader requirement completion, financial policy change or 7A2 capability is implied.

## Approved UI architecture and Phase 6 closure — 2026-09-14

Phase 6 is CLOSED / ACCEPTED within [ExecPlan 060](plans/060-product-surface.md#phase-6-live-acceptance-and-closure--2026-09-14),
including the retained live PASS (one confirmed operation, 0 identity + 4 price +
0 retry attempts; no duplicate traffic after reload; physical gates unchanged).
Earlier pending checkpoints and broad planned requirement rows remain historical or
future scope, not evidence of additional delivered capabilities. No Phase 1–6
semantics, financial rules or requirement IDs change.

[D-033](DECISIONS.md#d-033--decision-first-ui-architecture--2026-09-14) and
[UI/UX Architecture](UI_UX_ARCHITECTURE.md) add the following delivery/acceptance map.
Architecture documentation is approved; every UI-01/Phase 7+ implementation remains
unstarted and separately authorized. The detailed Phase 7 ExecPlan is deferred.

| Existing requirements | Surface / ownership | Required UX acceptance |
|---|---|---|
| R-01 Search | UI-01 shell/Scout; existing set search and URLs. | Exact/suffixed number/name behavior, history/focus, bounded results and honest empty/error states; no new search scope. |
| R-02 Whole-set evidence; R-11/R-12 POV views | 7A1 Overview/Market/Part-Out. | Four independent views and strategy context, eligibility/freshness and explicit partial/null states. |
| R-03/R-04 Figures/totals; R-13/R-14 Physical/coverage | 7A1 Contents/Evidence using accepted fields; justified read projections separately scoped. | Recorded versus admitted quantities, intact/descendant integrity, unavailable rows and server-owned values; bounded priced ranks never imply complete contents. |
| R-05/R-06 Deal math/adjustments; R-27/R-33 Break-even/strategies | 7A2 Deal Economics, independently accepted after 7A1. | Asking/cost/contents changes, supported Buy Under/headroom, gross/net/profit/ROI, both caps, unknown/undefined states, no double-counting or client arithmetic. |
| R-07 Saved work | 7B authentication/reproducible saved deals; 7C Watchlist/targets/settings/index. | Authenticated reload, retention-compatible immutable replay, explicit revisions/conflicts; URLs remain metadata. Actual outcomes stay Phase 16. |
| R-08/R-36 Hunt | Phase 8 opportunity screener. | Supported explained rankings/filters, deterministic ties and explicit hypothetical targets; no invented asking prices or critical missing inputs hidden by scoring. |
| R-09 Shared UI | Responsive acceptance in UI-01/7; packaging/offline in Phase 9. | Desktop/laptop/tablet/phone usability; web screenshots do not establish Android-device/offline acceptance. |
| R-15/R-23–R-26 Recovery/scenarios/concentration | 7A1 presentation of accepted scenarios; new economics in 7A2. | Preserve uncalibrated gross qualifications, subset/full denominators and distinct coverage/quality/support; no invented recovery horizon. |
| R-35 Refresh | Accepted Phase 6 behavior preserved in UI-01/7A1. | Explicit confirmation, durable operation/rejoin, exact attempt accounting, read-only GETs and evidence expiry across navigation. |
| R-37 Part-Out Analysis | 7A1 information architecture; 7A2 acquisition-dependent economics. | Progressive Overview/Market/Contents/Part-Out/Evidence, material reasons near metrics; Deal appears only when implemented. |

Existing data presentation, narrow read projections and missing capabilities are
separated in the architecture brief. Images/lifecycle/history are not current public
fields. No speculative destination or metric implies their availability; optional
listing/images, recognition and capture remain Phases 13–15, outcomes in 16.

## Phase 6B public workflow — 2026-09-14

R-35 now has public read-only planning, explicit confirmation, durable progress and
Resume for COMPLETE_SET, plus React appraisal reload using generated contracts.
R-01 direct search/appraisal GETs remain pure. Four USD/US views retain independent
new/used and sold/stock evidence; confirmed-empty is unknown value. Exact 4/4/2/10
ceilings and stricter constraints persist across rejoin. Contents/P4-01 physical
blockers remain independent. Synthetic acceptance is recorded in
[ExecPlan 060](plans/060-product-surface.md#phase-6b-public-workflow-implementation--2026-09-14);
independent review/checkpoint and first real product acceptance remain separate.

## Phase 6B durable backend prerequisite — 2026-09-14

R-35 shared bounded refresh gains durable whole-set authorization, idempotency,
restart-safe discovery evidence/review and four-view cache/job association through
migration 0008. Existing provider attempts, controls and quantity/condition/basis
semantics remain authoritative; no new quota ledger exists. This is internal
backend infrastructure only. The public explicit plan/confirmation/progress refresh
workflow, contents refresh and broader Phase 6B acceptance remain pending.
Search/appraisal GET immutability and P4-01 physical blockers remain required.
See [scope and actual acceptance](plans/060-product-surface.md#phase-6b-durable-prerequisite-implementation--2026-09-14).

**Phase 6A independently accepted — Phase 6B ready, 2026-09-13:** Set-number/name search and bookmarkable cached appraisal detail pass independent product review for the authorized local checkpoint. Four strategies and four market views preserve partial, unknown and physical-blocked states. The Windows smoke harness now reserves an OS-assigned TEST port; corrected integration acceptance exits successfully. [ExecPlan 060](plans/060-product-surface.md) records the 40-file reviewed inventory, bounded fixes, automated/manual checks and cleanup. ZERO provider requests / ZERO provider credential loading; no new migration or dependency. **Next: separately authorize Phase 6B explicit user-triggered discovery/refresh.** Phase 6B and saved/deal/Hunt work have not started. Earlier entries are historical checkpoints.

## Phase 5C bounded synthesis — 2026-09-12

R-23/R-24 gain policy-adjusted Liquid/Fast Cash APPLICATION_SCENARIO amounts;
R-25 gains unadjusted dead-stock-like exposure with thin/unknown separation.
R-14 retains separate price/policy coverage and partial subtotals. R-26 retains
unchanged concentration; R-33 receives caller-order independent outcomes only.
See [ExecPlan 050](plans/050-valuation.md#phase-5c-approved-implementation-contract--2026-09-12).

R-15 empirical expected recoverable gross is not certified by uncalibrated factors.
R-22 Gems, duration-dependent R-18–R-21, R-05 economics, economic ranking and R-36
Hunt scoring remain deferred. R-37 product presentation remains Phase 6. Historical
broader requirements below remain obligations, not implementation evidence.

## Phase 5B bounded implementation — 2026-09-12

[ExecPlan 050](plans/050-valuation.md#phase-5b-bounded-contract--authorized-2026-09-12)
and `valuation/liquidity.py` cover R-16/R-17/R-21/R-31 provider-native activity,
compatible proxy and current inventory facts; R-18/R-19/R-20/R-21 duration readiness
remains explicitly unsupported without authoritative M. Synthetic formula tests
prove capability, not production duration availability. R-26 concentration uses
exact already-valued occurrences and honest priced-subset labels. R-22/R-30 receive
ranked contribution and operational inputs only, with no Gem or burden classification.
R-33 strategies remain independent. Unit/integration `test_liquidity.py` exercise
these boundaries and P4-01's physically unknown contents.

R-15/R-23/R-24/R-25 recovery values, R-05 economics and R-36/R-37 scoring/product
presentation remain deferred. Phase 5C is unstarted. No UI/API, schema or provider
expansion. Independent acceptance and the ten-file local checkpoint are recorded
in ExecPlan 050; Phase 5C requires separate authorization.

**Phase 5A independently accepted, 2026-09-12:**
`services/api/src/brickvault_api/valuation/` and the new unit/integration
`test_valuation.py` files implement the bounded theoretical subset of R-03/R-04 and
R-11: independent whole-set/contents views, strategy admission, exact quantity-weighted
arithmetic, occurrence attribution and partial market coverage. See
[ExecPlan 050](plans/050-valuation.md) and [valuation rules](VALUATION_RULES.md).
Acceptance passes 233 affected units and eight PostgreSQL cases, including ambient
Decimal-context independence and expiry under the lookup's tightened market policy.
This establishes no recovery/liquidity/profit/ranking formula, residual-build proceeds,
saved workflow, UI or broad product acceptance. Earlier evidence remains historical.

**Phase 4A evidence — 2026-09-12:** [ExecPlan 040](plans/040-calibration.md) and [calibration guide](CALIBRATION.md) map representative corpus, four-view requirements, exact raw subtotals, physical partition safety, independent coverage, read-only cache access, hypothetical admission and manual comparison structures to `calibration/` plus `tests/unit/test_calibration.py` and `tests/integration/test_calibration.py`. These are offline implementation/test evidence only. Live representative coverage, website agreement, final liquidity/POV/deal/Gem/Hunt formulas and product acceptance remain deferred to their separately authorized phases.

**Phase 3C offline accepted — 2026-09-12 UTC:** F5 is corrected and deterministic PostgreSQL regressions pass. [ExecPlan 030, section 18](plans/030-market-provider.md#18-independent-phase-3c-offline-acceptance--2026-09-12-utc) preserves the finding and records final verification and the reviewed 32-file checkpoint scope. Phase 3 is complete locally; Phase 4 requires separate authorization. Historical checkpoints below remain dated evidence.

**Current checkpoint — 2026-09-11:** Phase 2 is locally accepted: official development generation 1, cached no-op and history preservation verified, cleanup correction tested, and all 61 intended files independently reviewed. This acceptance does not establish deployment or the deferred product capabilities. See [ExecPlan 020](plans/020-catalog-foundation.md). Phase 3A passes independent offline acceptance for the authorized local checkpoint: 141 BrickLink tests and 416 Python units pass after two bounded transport corrections. See [ExecPlan 030](plans/030-market-provider.md) for actual verification. Phase 3B discovery correction and bounded live proof passed: three justified mappings, twelve valid price views, 7 identity + 12 price + 0 retry = 19 attempts. Independent acceptance passed after three narrow offline corrections and 218 affected tests; the local checkpoint commit is authorized. See ExecPlan 030 section 17 for evidence qualifications. Credential/IP compatibility was demonstrated for this local run. Phase 3C and its retention/display-rights decisions remain unstarted.

Dated execution records below preserve historical outcomes and then-applicable authorization; their pending or blocked states do not supersede this checkpoint.

**Historical Phase 2D outcome — 2026-09-10 local: BLOCKED at a different development SQL timeout.** The requested observation timeout is proven and corrected by in-transaction candidate color-fact analysis. An independent matching retained-state probe changes SELECT from a 300-second timeout to 0.820762 seconds and full rollback INSERT to 57.537484 seconds; corrected retained official acceptance inserts 1,557,375 observations in 55.291041 seconds and passes 72 pre/postactivation cases plus no-op. All 264 Python units, 22 Node tests, 11 React tests, 196 PostgreSQL tests, six browser cases and build/contracts/package gates pass. Authorized fourth NEW development run `bcf21407-15ab-44bb-b358-17f600282599` instead times out earlier at step 16 `evidence_conflict:elements` in 300.004024 seconds (57014); its cause is not yet proven. Construction rolls back before the corrected observation step, validation, benchmark or activation. Read-only verification confirms zero candidate facts/validation, official generation 0/no receipts, unchanged two synthetic snapshots/four receipts/generation 4, and all three prior failed histories/staging unchanged. A fourth terminal failed run is retained. The accepted Windows publisher, migration 0005, existing indexes and 300-second limit remain unchanged. No fifth import, provider call, staging cleanup, Git checkpoint or Phase 3 work occurs. See the [current 42-item report](PHASE_2D_OBSERVATIONS.md). Earlier stops below remain historical evidence.


**Historical Phase 2D evidence at the R-code stop:** All twelve official gzip sources were acquired under
cleared metadata policy and attribution. Actual hashes, headers, row counts and
bounded parser corrections are recorded in the
[official-source report](PHASE_2D_OFFICIAL_EVIDENCE.md). Relation code `R` still
requires official meaning evidence, so canonical imports, real-set query benchmarks
and development activation are NOT RUN. No product requirement becomes accepted
from acquisition alone. Phase 2 remains incomplete; Phase 3 is not started.

**2026-09-09 Phase 2D gate:** Authorized execution is BLOCKED before acquisition
because current official Downloads/Terms could not be inspected. The
[provider gate report](PHASE_2D_PROVIDER_GATE.md) adds no official catalog coverage
or product acceptance evidence. Phase 2 remains incomplete; Phase 3 is not started.
The Phase 2C checkpoint below and its then-next authorization boundary are historical.

**Phase 2C catalog evidence:** Snapshot-pinned number/name, metadata, version/default,
source inventory, figure/components, matching, extras, element/mapping and relationship
queries are implemented beneath future APIs. The synthetic benchmark and dedicated
PostgreSQL tests provide catalog-input evidence for R-01/R-03/R-04 and R-11/R-13/R-14/
R-20/R-26–R-30/R-32/R-33/R-35–R-37: exact part/color identity, integer quantities,
spares, mutually exclusive representations, full lineage, distinct-set containment
and explicit mapping/completeness states. [ExecPlan 020](plans/020-catalog-foundation.md)
records actual verification. No monetary formula, lot consolidation, liquidity,
global rarity score, first/last appearance metric, pricing or product UI is accepted
by these catalog tests. R-11–R-37 definitions and later ownership remain unchanged.
Independent 2C acceptance passed after three bounded corrections and 183 passing
PostgreSQL tests, for the authorized reviewed local checkpoint. Phase 2 remains
incomplete and 2D unstarted; official acquisition, actual source-schema verification,
real-set benchmarks, coverage and realistic catalog performance require separate
Phase 2D authorization. No complete product requirement is accepted by this slice.

The following paragraph preserves historical 2A/2B acceptance evidence.

**Slice 2A/2B acceptance evidence (2026-09-09):** [ExecPlan 020](plans/020-catalog-foundation.md) preserves independent 2A acceptance and records independently accepted 2B offline loading, stable identities, immutable snapshot history, quantity/spare/relationship preservation, deterministic candidate reports and atomic activation/recovery. Synthetic tests support structural prerequisites of R-01/R-03/R-04/R-11/R-13/R-14/R-20/R-26–R-30/R-32/R-33/R-35–R-37. They establish no live coverage, full query service, price, economic metric, ranking or UI acceptance. Per-requirement ownership and acceptance conditions remain unchanged. Phase 2B is locally accepted after bounded review corrections and 161 passing PostgreSQL tests. Phase 2 remains incomplete; Phase 2C is the next separately authorizable slice and is not started.

## Status and governing contracts

The full product requirements below remain planned. Phase 1 and Phase 2 local catalog foundations are accepted, including official metadata normalization/provenance, development activation, deterministic internal queries and no-op/history preservation. The 72-case benchmark includes expected-incomplete states and does not certify complete physical expansion or external mappings. Product catalog UI, market coverage, valuation, device behavior and deployed infrastructure remain unaccepted. See [ExecPlan 020](plans/020-catalog-foundation.md), [product specification](PRODUCT_SPEC.md), [data model](DATA_MODEL.md), [architecture](ARCHITECTURE.md), [valuation rules](VALUATION_RULES.md), and [roadmap](ROADMAP.md).

| Requirement | Governing specification | Data-model entities | API/UI behavior | Implementation phase | Required acceptance evidence | Current status |
|---|---|---|---|---|---|---|
| R-01 Number/name search, including suffixes | PRODUCT_SPEC R-01; DATA_MODEL Phase 2 | catalog_set, catalog_theme, set_provider_mapping, catalog_import_run | /api/catalog/sets query/resolve/detail; explicit variant ambiguity; direct React entry without images | 2 identities; 6 UI/API | Suffixed 75331-1-style and ambiguous unsuffixed fixtures, deterministic name results, correct detail route with recognition disabled | Planned; catalog and browser evidence not run |
| R-02 Whole-set new/used evidence, separate sold/listings | PRODUCT_SPEC R-02; VALUATION_RULES Market evidence | market_observation, set_provider_mapping, provider_fetch_run/cache, conversion observation | Separate new/sealed and used/complete values where supported, sold/current-listing panels, provenance/time/sample/currency and unavailable state | 3 adapter; 4 feasibility; 6 display | Representative new/used/side/source coverage, stale/thin/missing cases, unsupported condition qualification, rights/access report and browser response | Planned; provider access/rights/coverage unverified |
| R-03 Every figure, quantity, permitted image, individual new/used prices | PRODUCT_SPEC R-03; DATA_MODEL explicit relationships | minifigure, set_inventory_version, set_minifigure, minifigure_provider_mapping, catalog_image_reference, market_observation | Set detail enumerates all figures with quantity, individual values, permitted image/reference or placeholder, source/freshness/unknowns | 2 relationships; 3 evidence; 4 feasibility; 6 display | Exact inventory/quantity comparison for zero/one/many/repeated figures and variants; no guessed mappings or image rights | Planned; completeness/pricing gates not run |
| R-04 Quantity-aware figure totals | PRODUCT_SPEC R-04; VALUATION_RULES Minifigure identity, quantity, and condition | set_minifigure, valuation_input_line/output_line, snapshot | New/used and adjusted totals plus priced/total/unavailable quantities, coverage, concentration and partial/blocked state | 5 arithmetic; 6 catalog totals; 7 adjusted totals | Exact repeated-quantity sums, known empty versus unknown inventory, missing/damaged/partial-price fixtures, zero/undefined concentration cases | Planned; calculation tests not run |
| R-05 Asking-price proceeds/profit/ROI/both max-buy caps | PRODUCT_SPEC R-05; VALUATION_RULES Acquisition cost and Maximum purchase | valuation_snapshot/input/output lines, selling_profile, settings, saved_deal | /api/valuations and deal calculator expose gross/cost/net/acquisition/profit/ROI, target-ROI and min-profit caps, one recommendation/explanation | 5 engine; 7 calculator/persistence | Decimal fixture reproduction, variable purchase tax/premiums, zero-cost undefined ROI, downward caps/clamps, disabled/unsupported constraints and saved snapshot replay | Planned; engine not implemented |
| R-06 Missing/damaged figures, incomplete build, instructions/box, costs | PRODUCT_SPEC R-06; VALUATION_RULES strategies and costs | deal_minifigure_adjustment, deal_build_adjustment, valuation lines, profiles | Adjust per-unit/quantity condition and residual allocation; itemize tax/premium/travel/fees/shipping/packaging/reserve | 5 domain/tests; 7 editing/persistence | Complete/missing/damaged/repeated figures, incomplete build/box/instructions, no double-count physical allocation/costs, unsupported residual evidence | Planned; no adjustment UI/tests |
| R-07 Saved sets/watchlists/targets/URLs/asking/notes/deals/settings; later outcomes | PRODUCT_SPEC R-07; DATA_MODEL Phase 7 and later outcomes | saved_set, watchlist_item, saved_deal, user_settings, selling_profile, valuation_snapshot; later deal_outcome | Private CRUD, revision conflicts, reopen reproducible analysis, URLs as metadata; later outcome append | 7 saved work/auth; 9 cache/sync; 16 actual outcomes | Save/reload/edit-conflict/auth tests, unchanged historical calculation on price refresh, no URL fetch, later outcomes do not rewrite forecasts | Phase 7C and Phase 9 cache/reconnect/expiry/conflict evidence accepted; R-07 PARTIAL only because Phase 16 actual outcomes remain |
| R-08 Sets to Hunt | PRODUCT_SPEC R-08/R-36; VALUATION_RULES strategies and reproducibility | hunt_run, hunt_score_snapshot, hunt_score_component_snapshot, valuation_snapshot, profiles, observations | /api/hunts ranked supported strategy opportunities with preserved split-sale signals plus R-36 part-level components, max-buy and missing-data outcomes | 8 | Versioned deterministic rank/ties; confidence/coverage/stale/thin/concentration/residual/order-burden and R-36 calibration fixtures; no fabricated asking price or theoretical cash | Planned; dedicated phase, no scores produced |
| R-09 Chrome/PWA/Android shared primary UI/API/database | PRODUCT_SPEC R-09; ARCHITECTURE client/offline; D-019 | One authoritative PostgreSQL, private principal/session, saved-record revisions; permitted dated client caches | Same React UI in Chrome/PWA/Android, /api, private auth, read-only offline cache with dates and explicit reconnect needs | 1 shell; 6–8 core flows; 7 auth; 9 PWA/Android/sync | Responsive browser and physical Android search/detail/deal/watchlist checks, package spike, cache/session/date/conflict tests, no client financial/provider logic | SATISFIED for the shared Chrome/PWA/Android requirement; Phase 9 source, package, core flow, transport/auth, offline/reconnect, expiry, and conflict evidence accepted |
| R-10 Private home/subdomain deployment | PRODUCT_SPEC R-10; SECURITY_PRIVACY; ROADMAP Phases 10–12 | Existing authoritative database under approved private deployment; backup/release evidence | Approved abrianbaker.com hostname, authenticated HTTPS, monitoring/recovery; database never public | 10 local hardening; 11 read-only discovery; 12 separately approved deployment | Local disposable restore/release evidence, separately authorized read-only actual infrastructure report, reviewed/authorized deployment with TLS/auth/backup/monitoring/rollback checks | Phase 11 CLOSED in [ExecPlan 090](plans/090-home-infrastructure-discovery.md); Phase 12 IN PROGRESS with P12-01 ACCEPTED / CLOSED in [ExecPlan 091](plans/091-production-runtime-and-deployment.md) and P12-02 AUTHORIZED / IN REVIEW in [ExecPlan 092](plans/092-exact-infrastructure-pre-mutation-review.md). Node capacity/placement facts are now read-only observations; Brian approved `appraisal.abrianbaker.com` for planning and selected encrypted database copies on both existing Proxmox and a new Google Drive folder, with Google Drive off-host. Access/restore, private DNS/certificate rights and live Caddy/TLS/device evidence remain open. No deployment mutation occurred; P12-03–05 are not authorized. |

## Part-out and liquidity requirements — D-025

These requirements extend R-11 independently rather than hiding liquidity under one generic POV item. The governing contracts are [PRODUCT_SPEC](PRODUCT_SPEC.md), [DATA_MODEL](DATA_MODEL.md), [VALUATION_RULES](VALUATION_RULES.md), [PROVIDER_GATES](PROVIDER_GATES.md), [ARCHITECTURE](ARCHITECTURE.md) and [the amended plan](plans/005-set-part-out-values.md). Formula IDs below refer to the authoritative valuation rules; all entities are conceptual future structures. No provider/formula/threshold implementation evidence is asserted.

| Requirement | Governing specification | Data-model entities | Provider/input evidence | Valuation formulas/rules | API/UI behavior | Implementation phase | Required acceptance evidence | Current status |
|---|---|---|---|---|---|---|---|---|
| R-11 New/used POV | PRODUCT_SPEC R-11; VALUATION_RULES V-POV; plan 005 | theoretical_pov_snapshot, set_inventory_line | Verified exact component prices in each condition | V-POV | Separate NEW/USED results | 2–6 | Quantity/color decimal reproduction; one condition missing | Planned; implementation and relevant live/policy gates unverified |
| R-12 SOLD/CURRENT POV | PRODUCT_SPEC R-12; VALUATION_RULES V-POV; plan 005 | market_observation, theoretical_pov_snapshot | Condition/side/statistic/currency/window semantics | V-POV; Market evidence | Four-view matrix with no fallback | 3–6 | Four-view isolation, asking versus sold labels and equivalence settings | Planned; implementation and relevant live/policy gates unverified |
| R-13 Inventory semantics | PRODUCT_SPEC R-13; VALUATION_RULES Physical allocation; plan 005 | part, catalog_color, mappings, set_component_inventory, inventory_choice_group, minifigure_component, subset_membership | Exact source quantities, extra/choice/figure/nested/instruction semantics | Physical allocation; Part-out inputs | Inclusion modes and unresolved group reasons | 2; 5–7 | Alternates/extras/intact/components/nested counts and no residual double counting | Planned; implementation and relevant live/policy gates unverified |
| R-14 POV result/coverage | PRODUCT_SPEC R-14; VALUATION_RULES Part-out inputs, status and coverage; plan 005 | theoretical_pov_snapshot, valuation_output_line | Price/activity availability and independent reference weights if permitted | Part-out inputs, status and coverage | Minimum result contract; partial subtotal versus null full total | 2–6 | Unknown value denominator never 100%; empty/partial/activity coverage and full contract | Planned; implementation and relevant live/policy gates unverified |
| R-15 Expected recoverable POV | PRODUCT_SPEC R-15; VALUATION_RULES V-REC; plan 005 | recoverable_pov_snapshot, valuation_input_line, selling_profile | Supported market activity and recovery/horizon/profile assumptions | V-REC; Gross proceeds and selling costs | Recovery gross, costs, net and profit separately | 4–7 | Gross adjustment/cost reconciliation, unsupported model blocked, immutable replay | Planned; implementation and relevant live/policy gates unverified |
| R-16 Part market activity | PRODUCT_SPEC R-16; VALUATION_RULES Part-level liquidity inputs; plan 005 | market_activity_observation, market_observation | Sold units/occurrences/window, current units/inventories/lots/stores and price statistics | Part-level liquidity inputs | Raw observations and independent price/activity coverage | 3–6 | Missing versus true zero, actual intervals and field meaning preserved | Planned; implementation and relevant live/policy gates unverified |
| R-17 Sell-through proxy | PRODUCT_SPEC R-17; VALUATION_RULES L-PROXY = S/(S+C); plan 005 | part_liquidity_snapshot | Compatible interval S and point-in-time C | L-PROXY = S/(S+C) | Explicit proxy/window label and state | 3–6; 8 | S=C=0 undefined, missing inputs blocked, no historical-turn claim | Planned; implementation and relevant live/policy gates unverified |
| R-18 Monthly velocity | PRODUCT_SPEC R-18; VALUATION_RULES L-VELOCITY = S/M; plan 005 | part_liquidity_snapshot | S and actual positive month window M | L-VELOCITY = S/M | Sold units/month and window convention | 3–6; 8 | Non-six-month/zero/invalid/unknown duration and exact precision | Planned; implementation and relevant live/policy gates unverified |
| R-19 Months of supply | PRODUCT_SPEC R-19; VALUATION_RULES L-SUPPLY = C/V; plan 005 | part_liquidity_snapshot | C with compatible velocity inputs | L-SUPPLY = C/V | Finite/infinite/undefined/insufficient states | 3–6; 8 | Zero velocity and supply, time/scope mismatch and unknown buckets | Planned; implementation and relevant live/policy gates unverified |
| R-20 Set absorption time | PRODUCT_SPEC R-20; VALUATION_RULES L-ABSORB = q/V; plan 005 | set_inventory_line, part_opportunity_snapshot, set_part_out_snapshot | Selected quantity and compatible market velocity | L-ABSORB = q/V | Per-lot demand-equivalent months; set distributions | 2–6; 8 | 2/75 versus 16/4 fixtures, no Brian-market-share or deadline assumption | Planned; implementation and relevant live/policy gates unverified |
| R-21 Sales-occurrence frequency | PRODUCT_SPEC R-21; VALUATION_RULES L-OCCURRENCE = O/M; plan 005 | market_activity_observation, part_liquidity_snapshot | Source-defined O and positive actual M | L-OCCURRENCE = O/M | Occurrences separately from units/orders | 3–6; 8 | 100 units in one versus 60 occurrences; absent count not inferred | Planned; implementation and relevant live/policy gates unverified |
| R-22 Part opportunities/Gems | PRODUCT_SPEC R-22; VALUATION_RULES O-GEM and versioned classification; plan 005 | part_opportunity_snapshot, part_set_presence | Value, demand, supply, sample/freshness and scoped catalog evidence | O-GEM and versioned classification | Dimension breakdown, Gem reasons and slow/unknown classes | 2–6; 8 | Expensive-only/rare-only fail; high/low velocity and threshold boundary cases | Planned; implementation and relevant live/policy gates unverified |
| R-23 Liquid POV | PRODUCT_SPEC R-23; VALUATION_RULES V-LIQUID; plan 005 | liquid_pov_snapshot | Compatible price/activity satisfying validated policy | V-LIQUID | Qualifying value/share/lots, exclusions and version | 4–6; 8 | Threshold sensitivity, missing excluded value and compatible denominator | Planned; implementation and relevant live/policy gates unverified |
| R-24 Fast Cash Value | PRODUCT_SPEC R-24; VALUATION_RULES V-FAST; plan 005 | fast_cash_value_snapshot | Stricter supported liquidity/confidence criteria | V-FAST | Gross basis, qualifying value/share/lots/pieces/confidence | 4–6; 8 | Stricter subset of Liquid, adjusted basis disclosure and no guaranteed date | Planned; implementation and relevant live/policy gates unverified |
| R-25 Dead-Stock Exposure | PRODUCT_SPEC R-25; VALUATION_RULES V-DEAD; plan 005 | dead_stock_exposure_snapshot | Verified slow/zero demand and supply; stale/thin limitations | V-DEAD | Slow/dead value/share/lots/pieces, unknown separate | 3–6; 8 | Missing activity never proven dead; thresholds/version and stale invalidation | Planned; implementation and relevant live/policy gates unverified |
| R-26 Concentration | PRODUCT_SPEC R-26; VALUATION_RULES V-CONCENTRATION; plan 005 | concentration_snapshot, part_opportunity_snapshot | Exact quantity/value and qualifying liquidity references | V-CONCENTRATION | Highest/top-5/top-10 and high-value/high-liquidity shares; figure concentration distinct | 5–6; 8 | Stable ties, fewer than N lots, repeated figures and partial denominators | Planned; implementation and relevant live/policy gates unverified |
| R-27 Break-even lots | PRODUCT_SPEC R-27; VALUATION_RULES V-BREAK-EVEN; plan 005 | break_even_lot_analysis, saved_deal | Supported lot values/recovery and subset costs; acquisition assumption | V-BREAK-EVEN | Two ranked prefixes, identities/quantities/coverage and gross/net distinction | 4–7; 8 | Target reached/not reached/zero, deterministic ties and unknown subset costs | Planned; implementation and relevant live/policy gates unverified |
| R-28 Value per unique lot | PRODUCT_SPEC R-28; VALUATION_RULES V-PER-LOT = recoverable gross/L; plan 005 | operational_burden_snapshot | Supported recoverable gross, consolidated sellable lots | V-PER-LOT = recoverable gross/L | Value density with lot denominator and basis | 4–6; 8 | USD 300/75 versus 300/475; zero/unknown/partial inputs | Planned; implementation and relevant live/policy gates unverified |
| R-29 Value per piece | PRODUCT_SPEC R-29; VALUATION_RULES V-PER-PIECE = recoverable gross/Q_piece; plan 005 | operational_burden_snapshot, minifigure_component | Supported recovery and verified physical expansion | V-PER-PIECE = recoverable gross/Q_piece | Separate physical-piece density and inclusion basis | 2; 4–6; 8 | Intact figures count once by verified pieces; unknown expansion and zero denominator | Planned; implementation and relevant live/policy gates unverified |
| R-30 Operational burden | PRODUCT_SPEC R-30; VALUATION_RULES O-BURDEN; plan 005 | operational_burden_snapshot, selling_profile | Lots/pieces/fragmentation and supported orders/listings/labor | O-BURDEN | Counts, low/high-value shares and versioned broad category | 4–8 | No invented precise labor/orders; burden boundaries and value-density comparison | Planned; implementation and relevant live/policy gates unverified |
| R-31 Market competition | PRODUCT_SPEC R-31; VALUATION_RULES O-COMPETITION; plan 005 | market_activity_observation, part_opportunity_snapshot | Current units, independent inventory/lot/store counts | O-COMPETITION | Separate supply and seller/lot context | 3–6; 8 | 30 pieces/3 versus 28 sellers; no concentration without distribution | Planned; implementation and relevant live/policy gates unverified |
| R-32 Rarity/catalog presence | PRODUCT_SPEC R-32; VALUATION_RULES O-RARITY; plan 005 | part_set_presence, catalog_source_version | Exact part/color verified set relationships and catalog completeness | O-RARITY | Known set count, scoped exclusivity, optional first/last appearances | 2; 4–6; 8 | Versions deduplicated; unresolved alternatives/incomplete catalogs never prove global exclusivity | Planned; implementation and relevant live/policy gates unverified |
| R-33 Strategy comparison | PRODUCT_SPEC R-33; VALUATION_RULES Mutually exclusive strategies; plan 005 | valuation_snapshot, saved_deal, deal_part_adjustment, deal_build_adjustment | Whole-set/figure/part/residual and recovery/cost support | Mutually exclusive strategies; V-REC; existing net/ROI/max-buy rules | Complete, figures plus build, full part-out; later harvest | 4–7 | One active strategy; removed components absent from residual; immutable assumption/freshness replay | Planned; implementation and relevant live/policy gates unverified |
| R-34 POV premium | PRODUCT_SPEC R-34; VALUATION_RULES V-PREMIUM = POV/whole-set - 1; plan 005 | set_part_out_snapshot, market_observation | Comparable condition/side/currency/statistic/window whole-set evidence | V-PREMIUM = POV/whole-set - 1 | Compatible premium or labeled scenario | 3–6; 8 | Zero/unknown denominator, incompatible basis and partial numerator exclusions | Planned; implementation and relevant live/policy gates unverified |
| R-35 Caching/background refresh | PRODUCT_SPEC R-35; ARCHITECTURE shared cache/refresh; PROVIDER_GATES Phase 3; plan 005 | provider_cache_entry, provider_refresh_job, provider_fetch_run | Permitted retention/refresh, quotas and exact query identity | No new arithmetic; preserve evidence provenance and reproducibility | Bounded cached detail, priority refresh and stale/pending states | 3–4; 6 | Cold/warm/shared-set budgets; deduplication, rate-limit/backoff, lease and stale-overwrite tests | Planned; implementation and relevant live/policy gates unverified |
| R-36 Part-level Hunt intelligence | PRODUCT_SPEC R-36; VALUATION_RULES Set aggregation and Hunt components; plan 005 | hunt_run, hunt_score_component_snapshot, hunt_score_snapshot | All compatible strategy/part-out evidence plus mapping/price/activity/sample/freshness confidence | Set aggregation and Hunt components; Phase 4 calibration | Decomposable scores, distributions, economics, density/burden/competition/rarity and blockers | 4; 8 | Representative real-set calibration, no arbitrary weights or theoretical-only high rank; ties/replay | Planned; implementation and relevant live/policy gates unverified |
| R-37 Set-level Part-Out Analysis | PRODUCT_SPEC R-37; VALUATION_RULES Set aggregation; plan 005 | set_part_out_snapshot and referenced component snapshots | All four POV views and compatible derived evidence/rights | Set aggregation; catalog-level V-POV through V-PREMIUM | Matrix, catalog-level summaries, Gems/slow warnings and part evidence drill-down; acquisition-dependent break-even and editable strategy/cost comparisons remain R-27/R-33 in Phase 7 | 5–6 | Complete minimum contract, desktop/mobile, pending/stale/partial/blocked and recognition disabled | Planned; implementation and relevant live/policy gates unverified |

## Phase and evidence discipline

R-11 retains D-024's new/used planning history; D-025 adds R-12–R-37 and extends the same plan through Phases 2–8. No standalone phase, Phase 1 provider/product work or selling-operation implementation is added. R-08's original split-sale signals remain alongside R-36's strategy/part-level Hunt components. Current source rights, aggregate equivalence, recovery assumptions, liquidity thresholds and final Hunt weights remain Phase 3/4 gates.

Phases 1–9 establish the sourcing core; Phase 10 local release precedes separate discovery/deployment approvals. Phases 13–16 are optional image/recognition/native-capture/training enhancements that reuse the same core. D-003 retention begins with that image feature, not the foundation.

Fixture-based contract tests can pass before live entitlement is available, but Phase 4 must not certify product market feasibility without actual authorized coverage/use evidence. Distinguish planned acceptance from recorded results in each ExecPlan. Unknown prices, mappings, source rights, and device behavior remain explicit.

## Phase 1 slice evidence

The canonical [ExecPlan 000](plans/000-local-foundation.md) preserves accepted Slices 1A/1B and records independent Phase 1 local acceptance on 2026-09-07 for the authorized completion checkpoint. The built shell passes desktop/mobile Chromium, real database outage/recovery, transport-failure, Retry, keyboard/focus, loading and sensitive-path tests. Installed Chrome was separately inspected at both sizes during Slice 1C; review made no UI/static correction requiring repeat manual inspection. Full Windows commands, runner ledger-failure cleanup and local CI configuration checks pass. Hosted CI remains deferred; Phase 2 is not started.

| Slice | Bounded deliverable | Required evidence and stop |
|---|---|---|
| 1A | Toolchain/workspace/configuration and exact dependency locks | Supported compatibility and reproducible locked resolution; applicable format/lint/type/orchestration checks; explicitly authorized lock checkpoint; stop before database/application shells |
| 1B | Isolated PostgreSQL, SQLAlchemy/Alembic, API, generated contracts | Real migration/readiness failure tests, database-independent liveness/schema export, deterministic contracts/drift detection; stop before frontend and CI completion |
| 1C | React status shell, built serving, CI, full acceptance | Responsive built UI at 1440 × 900 and 390 × 844, API/static error boundaries, all Phase 1 checks, recorded Windows/local evidence; stop before Phase 2 |

Slice evidence supports only the foundation portion of R-09 and later development readiness. It does not mark set search, pricing, figures, deal math, hunting, PWA/Android, or deployment complete. The implementation documentation-update policy lives in ExecPlan 000 and CODEX_WORKFLOW.md.

## Later image contract retained

[IMAGE_INGESTION.md](IMAGE_INGESTION.md) maps Phase 13 originals/assets/relationships/receipts to independent uploads, listing_image_id, deterministic persisted order, and recoverable successful-duplicate replay. Phases 14–16 add candidate canonical identities, separate confirmation/privacy review, supported native capture, and versioned source-group-safe datasets. These additions are never acceptance prerequisites for R-01 through R-09 core sourcing flows.


## Phase 4B offline discovery accounting - 2026-09-12

Provider prerequisites for direct lookup/market coverage gain one pre-mapping
accounting path, not new valuation or live feasibility evidence. Migration 0007,
`market.accounting`, `DiscoveryRepository` and `calibration.stage_one.StageOne`
connect bounded discovery to explicit mapping review and the accepted price worker.
`test_discovery_accounting.py` covers discriminated shapes, quotas, concurrency,
restart/uncertainty, F5 controls, price separation and a synthetic unmapped-to-reviewed-
to-priced handoff. Migration tests cover price-history preservation and guarded
downgrade; package checks discover head 0007. See [ExecPlan 040](plans/040-calibration.md).

Live use stays 0/0/0/0 against 40/48/8/96 ceilings. Conditional 36/44/8/88 demand and
unresolved physical coverage remain saved preflight evidence. No Phase 5 formula,
coverage claim or additional provider right is accepted here. Independent review
passes after the installed Windows migration-path correction; next is separately
authorized development 0007 migration and P4-01 resumption. See the
[Stage 1 checkpoint](PHASE_4B_STAGE_1.md).
