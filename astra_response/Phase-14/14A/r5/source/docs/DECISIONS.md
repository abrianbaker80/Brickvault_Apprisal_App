# Project Decisions

## Accepted Phase 12 final closure — 2026-10-01

Brian independently accepts [P12-05 r5](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/57dec1e5f7b0538c75f2a17a824c15aba3083dc2/astra_response/P12-05/r5/REVIEW.md) at
57dec1e5f7b0538c75f2a17a824c15aba3083dc2. **P12-05: ACCEPTED / CLOSED.
Phase 12: ACCEPTED / CLOSED. Phase 13: NEXT / NOT STARTED.**
[Plan 099](plans/099-phase-12-production-acceptance.md) is CLOSED.
[Plan 102](plans/102-manual-deal-economics-admission-repair.md) is
CONTRACT REVIEW COMPLETE / CLOSED — NO REPAIR REQUIRED. Qualified valuation
admission, frozen V1 replay and the accepted Gate 5 criterion remain intact.

The final populated Drive-only recovery and accepted r1-r4 gates close Phase 12;
the accepted evidence limits remain in force. This decision authorizes only the
literal five-file local documentation commit and separate r6 review publication.
Main is not pushed; protected dirty bytes stay unchanged and unstaged. Plans
100/101 and executable catalog repair are excluded. No live qualification or
test/build work is repeated. Historical decisions and dated blocker/resume
evidence below remain intact; their pending-status language is superseded here.


## Final populated Drive recovery — 2026-10-01

Brian accepted P12-05 r4 except for restoring its populated final backup. The
authorized continuation reused that exact existing protected receipt and
independent Windows Drive context, with no backup rerun, Proxmox fallback or
production mutation. Actual empty-rehearsal size and on-VM placement constraints
required bounded operator adaptations for the existing Windows WSL off-host
PostgreSQL 18 cluster, socket-only and tmpfs noswap. Accepted restore and effective
ownership/grant/SCRAM checks were retained. Populated recovery, full table-count
comparison, catalog/retry audit and complete cleanup passed. P12-05 and Phase 12
are READY FOR FINAL ACCEPTANCE, not yet closed; Phase 13 remains NOT STARTED.
[Plan 099](plans/099-phase-12-production-acceptance.md) is authoritative.


## Accepted P12-05 rollback target disposition — 2026-10-01

For Plan 099 Gate 8, Brian explicitly replaces the older infrastructure checkpoint
`p12-04d-r1` with immediate accepted operational predecessor `p12-04e-r6`.
P12-04D predates current health/retention/Python/alert/hook dependencies and remains
immutable. R6 binds that accepted operational contract and shares revision 0016
with the catalog-repair release. Both exact immutable releases remain unchanged;
this corrects the acceptance target, without a source patch or weakened check.
Actual r6 rollback and exact repaired forward return passed authenticated private
persistence, followed by cleanup/replay, real VM115 cold recovery and one final
dual backup. [Plan 099](plans/099-phase-12-production-acceptance.md) records evidence.
Earlier blocker evidence remains preserved. Independent Phase 12 acceptance and
main closeout remain pending; no Phase 13 is authorized by this readiness.


## P12-05 Gate 5 acceptance criterion corrected — 2026-10-01

Brian accepts the [Plan 102](plans/102-manual-deal-economics-admission-repair.md)
contract diagnosis: MANUAL is price selection after qualified valuation admission,
not an admission bypass. Keep whole-set-economics-v1 frozen, including exact
historical recomputation/expectation comparison. Production MANUAL + UNKNOWN/null
full economics conforms; no application bug, repair, V2, migration or new deployment
is required. [Plan 099](plans/099-phase-12-production-acceptance.md) Gate 5 is PASS
and resumes at Gate 6. Prior blocked reviews remain dated evidence. Ordinary unsaved
preview expiry is not a saved deal and does not require forced deletion for cleanup.
This corrects production acceptance only; no valuation/financial contract changes.

## Phase 9 final physical qualification accepted and phase closed — 2026-09-26

Brian accepts the final physical Android evidence in
[ExecPlan 088](plans/088-android-https-auth-source.md). Phase 9 and all its
slices are **CLOSED**. The accepted run exercised all five deterministic market
expiry profiles and the one-shot uncertain Watchlist mutation on the unchanged
APK. Server deadlines remained authoritative, stale evidence was not revived,
the uncertain write committed once at revision 1, no retry was issued, and
authoritative readback reconciled the device. Existing TLS, Host/Origin/CORS,
authentication/session/CSRF, private-memory, reconnect, expiry, and
fresh-process privacy controls remained intact. No live provider was contacted;
active qualification resources were removed. Phase 10 is **NEXT / NOT
STARTED**.

## Historical bounded physical Android qualification — 2026-09-23

Brian accepts the separately authorized one-phone USB HTTPS/authentication pass
recorded in [ExecPlan 088](plans/088-android-https-auth-source.md). The accepted
debug APK was installed unchanged; exact localhost TLS/Host/Origin/CORS,
login/session/logout, a CSRF settings save, private Settings/Watchlist reads,
passive resume, safe read-only disconnect, verified reconnect and fresh-start
privacy passed. No source defect or live-provider contact was found. The app,
reverse rule, temporary TEST certificate/key/trust, listener and disposable
database were removed; no rebuild or suite rerun is part of this acceptance.

This closes the **bounded physical transport/authentication qualification**, not
Phase 9. The existing [Phase 9 roadmap gate](ROADMAP.md#phase-9--pwa-offline-behavior-and-android-core-app)
still requires physical Android core workflows and auth/cache expiry/sync-conflict
checks; search/detail, deal analysis, saved work and on-device expiry/conflict were not
qualified by this pass. Phase 9 remains OPEN; Phase 10 follows its closure.
Earlier source-only and physical-not-started decisions below remain historical.

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

## Phase 9 accepted cache policy and Slice 1 authorization — 2026-09-23

Brian accepts [ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md).
Only the public application shell is durably cached. No private IndexedDB,
localStorage/sessionStorage, canonical snapshots, durable drafts or PostgreSQL
replication. APIs/auth remain no-store. Updates require explicit user action.

Later Slice 2 may retain already viewed private projections in document memory,
read-only through the last confirmed session deadline. No offline extension,
mutation or immediate remote revocation claim; logout/principal change/expiry
clear that memory. This does not authorize Slice 2 implementation.

Slice 1 includes online PWA and bounded source-level Capacitor feasibility only.
No native account/network workaround, global tooling or physical device. Phase 9
remains IN PROGRESS; technical/visual acceptance and commit are not implied.
R-07 still has separate Phase 16 outcomes; full R-36 and Deferred Economics retain
their accepted outstanding boundaries. Earlier Phase 9 prohibitions are historical.

## Phase 8 bounded source acceptance — 2026-09-23

Brian accepts Slice 2's implementation, technical evidence and supplied visual
evidence. Slice 2 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 8 is
ACCEPTED / CLOSED FOR ITS BOUNDED SOURCE MILESTONE under the 2026-09-22 decision.
[ExecPlan 084](plans/084-hunt-frozen-evidence-context.md#source-checkpoint-acceptance--2026-09-23)
preserves the distinct validation runs, accepted ZIP hash and exact local commit scope.

This closes the cached whole-set screener, transparent financial ordering, immutable
history, explicit qualification/freshness and frozen bounded component context.
It does not claim full R-36 satisfaction: unsupported evidence, calibration/policy
requirements, undelivered premium/scoped-presence/target-prefix concepts and every
Deferred Economics Extension remain outstanding and unsatisfied with no new phase
assignment. Context is explanatory only; financial outputs and all seven sorts are
unchanged, with no composite score, provider calls or historical current-evidence
lookup. Legacy context is not reconstructed. Existing uncalibrated semantics remain.

Authorize only the local checkpoint commit. Phase 9 cache/sync is next but NOT
STARTED / NOT AUTHORIZED, including planning; Phase 16 outcomes remains separate.
Earlier review-pending and implementation-only boundaries are historical.

## Phase 8 bounded milestone and Frozen Evidence Context — 2026-09-22

Brian accepts the focused R-36 review. Phase 8 completes a cached whole-set
opportunity screener with transparent financial sorting, immutable historical runs,
explicit qualification and bounded existing component-evidence context. Composite
scores, arbitrary weights, Gem/rarity/seller-competition scoring, recovery/burden,
recoverable value density, economic break-even lots and other Deferred Economics
Extensions are not prerequisites for this bounded source milestone.

Authorize only [Slice 2 — Frozen Evidence Context](plans/084-hunt-frozen-evidence-context.md),
IN PROGRESS. Capture PART_OUT_WITH_INTACT_FIGURES for the selected condition/basis
from the same appraisal, preserving legacy runs without backfill or current reads.
Finances, whole-set qualification and ordering are unchanged. Scenarios retain
accepted uncalibrated application semantics, never expected recovery, probability,
predicted loss, burden or rank. No new calibration is approved.

Full R-36 remains PARTIAL. Duration metrics, seller concentration, global rarity,
Gem policy, calibrated ranking and broader distributions remain unsupported or
calibration-dependent. POV premium, scoped presence and theoretical gross target
coverage remain undelivered. Deferred Economics remains outstanding, unsatisfied
and unassigned to a delivery phase. This narrows Phase 8 milestone acceptance;
it cancels or satisfies none of those requirements. The bounded source milestone
may close after subsequent acceptance, but not during this implementation.
Slice 1 and 7B/7C remain CLOSED.

Use optional nested `hunt-component-context-v1` within the unchanged candidate
envelope. Migration 0016 already admits this payload extension, so no schema
migration is introduced. Existing immutable rows remain unchanged.

## Phase 8 Slice 1 source-checkpoint acceptance — 2026-09-22

Brian accepts the Cached Whole-Set Hunt Run implementation, technical evidence,
corrected Watchlist browser coverage, spacing correction and four-image visual
review in [ExecPlan 083](plans/083-hunt-cached-whole-set-run.md). **Slice 1 is ACCEPTED /
CLOSED FOR ITS SOURCE CHECKPOINT; Phase 8 remains IN PROGRESS.** Phase 7B/7C remain
CLOSED. The local commit subject is `Complete Phase 8 Slice 1 cached whole-set Hunt runs`,
from parent `7d3e5902a71e54b1e25d4249037c74865b20b34e`.

R-08/R-36 remains partial. Remaining ranking/calibration, Gem/rarity/competition/
burden and unsupported components need focused review of existing evidence,
calibration/policy, unavailable dependencies and Deferred Economics Extensions
overlap before further implementation. A composite score is not presumed required.
Extensions stay deferred, unsatisfied and without a delivery phase. Phase 9
cache/sync and Phase 16 outcomes remain separate. No development migration, services,
account/provider work, deployment, push or later implementation is part of closeout.
Earlier dated unstarted/pending statements remain historical.

## Phase 7C source-checkpoint acceptance — 2026-09-22

Brian accepts Phase 7C Slice 4's implementation, technical evidence and five-image
visual review. **Slice 4 and Phase 7C are ACCEPTED / CLOSED FOR THEIR SOURCE
CHECKPOINTS.** [ExecPlan 082](plans/082-notes-source-urls.md) records the evidence,
including the visual archive SHA-256
`a0099ad8d7764d6b59879461cc013e8ef3cf8ce6f7eed0e5d4392e4167b66dac` and the
qualified 149-passed/6-failed original full web result.

Those six failures were stale existing authentication test fixtures exposed by
accepted Slice 3 settings behavior (classification C), not a Slice 4 regression.
They reproduced from the Slice 3 baseline: auth mocks returned null for the required
settings resource, while the implemented API's absent-settings response is a
revision-zero defaults object. The focused Authentication, Profiles, Forecast and
Watchlist tests passed 44/44 after changing only those mock responses to the existing
`noSettings` fixture. No production behavior changed, and the full web unit suite was
not rerun; do not report the historical 149/6 run as a current whole-suite pass.

The authorized local commit is `Complete Phase 7C Slice 4 notes and source URLs`
from parent `8b3ee4bff10f772760923d4c18eac7402e044137`. Phase 8 Hunt is next but is
unstarted and unauthorized. R-07 remains partial due to separately assigned Phase 9
cache/sync and Phase 16 actual outcomes. Deferred Economics Extensions remain
outstanding, deferred and unsatisfied without an assigned delivery phase; they are
not a Phase 7C acceptance gap. No development migration, provider/account/device
operation, deployment or push occurred. Earlier dated pending-review statements
below preserve their historical status.

## Phase 7B source-checkpoint closure — 2026-09-18

Brian accepts the three 7B-4 implementation checkpoints and six-image visual review.
**7B-4 is ACCEPTED / CLOSED; Phase 7B is ACCEPTED / CLOSED FOR ITS SOURCE
CHECKPOINT.** [ExecPlan 077](plans/077-forecast-revisions.md#source-checkpoint-acceptance-and-phase-7b-reconciliation--2026-09-18)
maps the current governing scope to accepted 7B-1–4 evidence with no remaining
in-scope source criterion. This does not close all Phase 7 or the broader R-07.

The settled private historical-retention authorization below, exact frozen replay,
immutable historical URLs, explicit current-cache recalculation, deliberate
parent-conflict recovery and same-ID committed-save recovery remain unchanged.
Desktop editor/navigation images use the real TEST stack; narrow editor/navigation
and both conflict views use mocked fixtures. Brian found no blocking layout or
qualification inconsistency. Rendered-state review does not independently verify
interaction, authorization or persistence; technical evidence remains separately
qualified in the plan.

Authorize one local 48-file commit from
`e2c4987bb9652f53b9a8956bd1597b42a7240976`,
`Complete Phase 7B-4 forecast editing and append-only revisions`.
Only normal closeout documents change now; no application tests, captures,
operational work or push. Next is separately authorized 7C planning, not started:
watchlist, persistent targets/settings and Saved Deal Index remain there. Phase 8
is unchanged. Deferred Economics Extensions remain outstanding, deferred,
unsatisfied and without an assigned delivery phase. Deferred development migration,
actual-account provisioning, deployment and device/HTTPS qualification are neither
passed nor new source-checkpoint blockers. Earlier status entries are historical.

## Phase 7B-4 linear forecast revisions — 2026-09-18

Brian approves one linear lineage per original, appendable only from its latest
saved member, using two immutable nullable root/parent columns and a unique saved
child constraint. Original IDs, canonical financial bytes and exact historical URLs
remain intact. Explicit condition, SOLD/STOCK, sale/fee-mode and request-variant
changes may remain in the lineage; full canonical set identity stays fixed.
Conflicts require deliberate parent selection and a new current-evidence calculation/
review, never retargeting or automatic rebase. Each record replays independently.

Only [ExecPlan 077 Checkpoint 1](plans/077-forecast-revisions.md) is authorized:
internal persistence/append authority and focused TEST validation, then review.
7B-4 is IN PROGRESS; 7B-1–3 stay CLOSED. Retention authorization is settled.
No public API/UI, deployment, actual account/provider work or Git checkpoint.
7C/Phase 8 remain unchanged; Deferred Economics Extensions remain outstanding,
deferred, unsatisfied and without an assigned delivery phase.

## Phase 7B-3 source checkpoint accepted / closed — 2026-09-18

Brian accepts Checkpoints 1–3 and the targeted fixture correction recorded in
[ExecPlan 076](plans/076-save-original-forecast.md). **7B-3 is ACCEPTED / CLOSED for
its source checkpoint.** The real TEST-stack desktop Deal/save and historical views,
corrected mocked narrow historical view and mocked typed failure state have completed
visual review. The narrow fixture previously combined unsupported physical admission
fields with supported finances; the success fixture and focused regressions correct
that test data. No production admission, historical projection or frozen replay changed.
"Complete for this resale form. Admitted in the original assessment" describes
representation admission, not verified seller contents.

The private historical-retention authorization below remains settled and is included
in the same checkpoint. Current-evidence eligibility stays separate from saved history's
lifetime. Authentication, immutable originals, owner-filtered recovery and exact replay
retain their accepted semantics. Mocked visual checks are distinct from actual
API/PostgreSQL acceptance; this is not an independent source-code audit, physical-device
validation or deployment qualification.

One local commit is authorized from main `918ec781e2b9ba3a0a6ee00ad9611b47de475ed8`:
`Complete Phase 7B-3 save and reopen original forecasts`. No operational work or push.
7B-1/7B-2 remain CLOSED and Phase 7B remains OPEN. 7B-4 planning is next but not started
or authorized. 7C, Phase 8 and Deferred Economics Extensions stay unchanged; extensions
remain outstanding, deferred, unsatisfied and without an assigned delivery phase.
Earlier authorization and pending-review entries below are historical.

## Phase 7B-3 checkpoint 3 authorization — 2026-09-18

Brian accepts the existing persistence/API checkpoints for onward integration and
authorizes the bounded UI/acceptance work in [ExecPlan 076](plans/076-save-original-forecast.md).
The private historical-retention decision remains settled. Existing architecture,
financial rules and authentication policy are unchanged. Technical and visual
acceptance of checkpoint 3 remain pending; 7B-3 stays IN PROGRESS. Earlier
checkpoint-only restrictions below are historical, and no later slice or operational
deployment/Git work is authorized by this implementation.

**Checkpoint 2 now authorized:** [ExecPlan 076](plans/076-save-original-forecast.md) records acceptance of
checkpoint 1 for onward integration and bounded API/replay implementation. Earlier
checkpoint-1-only stops below are historical. UI, deployment and commit remain
unauthorized; 7B-3 is IN PROGRESS.

**Current checkpoint authorization:** [ExecPlan 076](plans/076-save-original-forecast.md) authorizes only
7B-3 checkpoint 1, backend Persistence and Save Authority, with synthetic TEST
validation and technical review. Earlier planning-only boundaries below are historical
for this authorization. 7B-3 remains in progress; API/UI and commit are not authorized.

## Phase 7B-3 owner retention and historical-display authorization — 2026-09-17

**The project retention/historical-display gate is CLEARED FOR THIS AUTHORIZED
PRIVATE SCOPE.** Brian reports personally reading the full BrickLink API terms
and explicitly authorizes retaining historical BrickLink-derived data and
calculations, replaying them and displaying them later in this permanently private,
Brian-only, personal, non-commercial application. His stated interpretation is that
the restrictions discussed in the prior review concern website/public consumption
rather than his private historical use. This records project-owner authorization
based on his review and interpretation, not separate written permission from
BrickLink or an independently established legal conclusion.

This decision supersedes earlier unresolved retention/display gates and any
recommendation to block this scope pending provider clarification. Prior research
and dated checkpoints below remain historical context. Separate written BrickLink
clarification, further terms research, provider contact, another risk-acceptance
step and an assumptions-only substitute are not prerequisites for 7B-3.

Retain only the implemented [7B-2 snapshot population](plans/075-exact-snapshot-replay.md).
Original qualifications remain historical assertions; exact inputs drive financial
recomputation and stored expectations remain comparison targets. Saved historical
records have no newly imposed blanket expiry: original `valid_until` and source
retention dates remain historical facts, not saved-record deletion/display limits.
Reopening must survive live-source change/purge without pinning live catalog/cache
rows. Current-evidence admission, freshness, cache/provider-request rules,
attribution and authentication remain intact. This authorizes no public sharing,
redistribution, commercial deployment, raw-response archive, image/member-data
archive or new backup/export system.

Verified planning baseline: main `918ec781e2b9ba3a0a6ee00ad9611b47de475ed8`, empty
index and the three protected modifications with their recorded hashes; no later
permission-review commit exists. 7B-1 and 7B-2 remain ACCEPTED / CLOSED; Phase 7B
remains OPEN. This run authorizes only minimal decision/workflow documentation and
repository-grounded 7B-3 planning. Runtime/test code, schemas/migrations, API/UI,
tests/builds, installs, services, database/credential/provider access, provisioning,
deployment, staging, commits and pushes remain unauthorized. Stop after the record
and plan. 7B-4 retains editing/current recalculation/revision appending; 7C retains
the Saved Deal Index, watchlist and persistent targets/settings. Phase 8 is unchanged;
Deferred Economics Extensions remain outstanding, deferred, unsatisfied and without
an assigned delivery phase.

## Phase 7B-2 source checkpoint accepted / closed — 2026-09-17

**7B-2 is ACCEPTED / CLOSED for its source checkpoint.** 7B-1 remains CLOSED;
Phase 7B remains OPEN. Brian accepted the implementation and recorded validation.
This is not deployment or operational qualification. The next boundary is the
retention/display-permission review **before 7B-3**. Provider-backed persistence
remains blocked pending that determination; permission is neither established nor
prohibited. No permission research or later-slice work is authorized by this closeout.

Acceptance and the unchanged 16-file inventory are recorded in [ExecPlan 075](plans/075-exact-snapshot-replay.md).
One local commit on main is authorized from
`d4d70d121868c00e4eb6bfbc964ed5c91d439e43`, subject
`Complete Phase 7B-2 exact snapshot capture and offline replay`. No push or
operational work follows. The accepted implementation recomputes exact finances
from authoritative inputs under explicit schema/calculation/rounding versions;
qualifications, provenance and eligibility remain historical assertions. Capture
finalization follows final acceptance, and ordinary HTTP requests never prepare,
finalize or encode snapshots. No durable provider-backed snapshot or public
save/replay capability is included.

7C, Phase 8 and all Deferred Economics Extensions remain unchanged. The extensions
remain outstanding, deferred, unsatisfied and without an assigned delivery phase.
Earlier pending-review/no-commit entries below preserve their historical checkpoints.

## Phase 7B-2 — approved conditional financial replay boundary, 2026-09-17

Brian approved **exact financial replay conditional on recorded historical
qualifications**, then authorized the bounded backend implementation and synthetic
validation in [ExecPlan 075](plans/075-exact-snapshot-replay.md). This explicitly
qualifies earlier broader replay wording: financial amounts, ratios, caps,
feasibility, binding constraints, headroom, financial states/reasons and existing
presentation are recomputed. Original physical/valuation qualifications, evidence
quality, provenance and eligibility facts are historical assertions. Their financial
admission consequences are reapplied, but their underlying evidence is not rebuilt
or independently re-adjudicated. Stored financial expectations never enter formulas.

The exact schema/calculation/rounding identifiers are `whole-set-snapshot-v1`,
`whole-set-economics-v1` and `whole-set-usd-rounding-v1`. One frozen v1 implementation
serves public wrappers and replay. New financial behavior requires a new execution
version; unknown combinations fail explicitly. An unkeyed digest detects changes,
not authenticity or permission. Original `basis_revision` is an identity assertion.
Historical reproduction does not renew `valid_until` or establish current eligibility.

7B-1 remains CLOSED; this implementation is not acceptance/closure of 7B-2 or R-07.
No persistence, save/replay endpoint/UI, signing, migration, authentication change,
catalog lock/revision workflow or retention service is included. Provider-backed
retention/display remains unresolved, including derived outputs. No live providers,
actual account setup, development database access, deployment or Git checkpoint is
authorized. 7C, Phase 8 and Deferred Economics Extensions remain unchanged.

## Phase 7B-1 source checkpoint accepted / closed — 2026-09-17

Brian accepted [7B-1](plans/074-brian-only-authentication.md) and authorized one
local checkpoint commit from `ac6201e371ca0d022955c45a76154257e407b9f1`.
Desktop, 320px narrow, phone and locked-session views passed manual visual review.
The signed-in header was not supplied to the review chat; Sign out placement has
Astra's reported self-review/browser evidence, not manual visual approval here.
That limitation is nonblocking for this source checkpoint. No new UI work is requested.
The reconciled test history and all unrun checks remain qualified as recorded.

7B-1 is **ACCEPTED / CLOSED**; Phase 7B remains **OPEN**. Next is **7B-2, not authorized**.
No operational qualification, migration, actual account setup, provider activity,
deployment, push or later implementation follows. Provider-backed history remains
gated by unresolved retention/display permission; Deferred Economics Extensions
remain outstanding, deferred, unsatisfied and without an assigned delivery phase.
The earlier implementation-only authorization below remains historical.

## Phase 7B-1 authentication authorization — 2026-09-17

Brian accepted the overall Phase 7B direction and authorized implementation, tests
and self-review of **Brian-only authentication only**, followed by a review stop.
[ExecPlan 074](plans/074-brian-only-authentication.md) records this bounded slice.
Migration 0009 contains the singleton principal, throttle control and hashed opaque
sessions. Argon2id uses the locked argon2-cffi library. Bootstrap/reset are hidden-input
local owner commands; reset preserves identity and revokes all existing sessions.
Application identity remains separate from provider account scope.

Implementation may use only guarded disposable TEST databases and synthetic accounts.
It does not authorize development/production migration, Brian account provisioning,
provider credentials/calls, network exposure, deployment, staging, commit or push.
7B-2+ snapshot/replay/receipt/revision designs remain proposals. Historical provider
retention/display permission remains unresolved, not declared prohibited. 7A2 remains
closed; Deferred Economics Extensions remain outstanding, deferred and unsatisfied,
without a delivery phase. 7C and Phase 8 are unchanged. Implementation is not acceptance.

## Phase 7A2 whole-set closure and explicit deferral — 2026-09-17

**Phase 7A2 Whole-Set Deal Economics: COMPLETE / ACCEPTED / CLOSED.**

After accepting Slice 1, Slice 2A and Slice 2B technically and visually, and
reviewing the remaining roadmap requirements, Brian explicitly narrows the 7A2
milestone to the accepted whole-set implementation at
`fbbd98b29b84fe2b60132da8c1bfacc8d5f7ec54` on `main`. This is a new product
scope/roadmap decision, not a claim that the original broader milestone was met.

Completed scope: whole-set Deal Economics; explicit selected-market/manual sale
assumptions; buyer-paid shipping, shipping expense and other selling/acquisition
cost assumptions; net proceeds, profit/loss and ROI; target ROI and minimum profit,
both purchase caps, Maximum Purchase / Buy Under, binding targets and signed
headroom; whole-set break-even purchase ceiling; purchase-price-based tax and
buyer-premium assumptions; exclusive manual/calculated selling-fee rules with
ITEM_SALE_PRICE or GROSS_PROCEEDS (item sale plus buyer-paid shipping), optional
fixed transaction fee and one HALF_UP charge rounding event; stale-basis,
qualification and transient-draft lifecycle protections. No realized proceeds or
unsupported evidence claim is introduced.

**Deferred Economics Extensions** is the single outstanding/future economics
bucket. It retains missing/damaged contents, minifigure quantity, instructions/box/
build adjustments, figures plus remaining-build economics, full component part-out
economics, recovery/burden models and economic break-even lots. These requirements
are **OUTSTANDING / DEFERRED, NOT CANCELLED, NOT SATISFIED**. Their IDs, reasons,
prerequisites and history remain in the
[deferral register](REQUIREMENTS_TRACEABILITY.md#deferred-economics-extensions).
They are outside the closed 7A2 milestone, are not assigned to Phase 8 or silently
added to 7B/7C, and require separate scoping and authorization. Existing Phase 8
Hunt ownership is unchanged; no future delivery phase is selected here.

This decision supersedes earlier assignments of those capabilities to unfinished
7A2, including D-033's broader boundary and the earlier no-capability-moves clause.
It also supersedes earlier overall-open/not-started statements. Prior Slice 1/2A/
2B records remain historical evidence of their actual scope and acceptance; none
is rewritten as if this narrowing had already occurred. Phase 7 overall is not closed.

Authentication has no technical dependency on Deferred Economics Extensions.
The accepted whole-set Deal model is stable enough to persist, subject to 7B's
explicit frozen snapshot/version contract and retention gate. Historical reopening
must be distinct from recalculation against current evidence. The
[7B persistence questions](DATA_MODEL.md#7b-persistence-questions--unresolved)
remain design questions, not decisions implemented by this closure.

Brian authorizes documentation reconciliation and one local documentation-only
checkpoint. No further 7A2 implementation, 7B work, provider calls, migrations or
push. Next separately authorizable task: the bounded 7B authentication and
reproducible whole-set saved-deal ExecPlan.

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

## Phase 7A2 Slice 2B — explicit fee rules, 2026-09-17

Brian authorized [ExecPlan 073](plans/073-selling-fee-rules.md). Keep the manual total
selling/payment fee and add an exclusive calculated rule: combined percentage rate,
ITEM_SALE_PRICE or GROSS_PROCEEDS (item sale plus buyer-paid shipping), optional fixed
fee once per whole-set transaction. Round the exact combined charge to USD cents
with HALF_UP, then feed that charged amount into existing exact net/profit/ROI/caps.
This explicitly defined fee-charge boundary does not round sale evidence or change
2A's downward-cent purchase ceilings and revalidation. No marketplace rules inferred.

Old requests default to MANUAL and still require their manual fee. CALCULATED
requires a rule and rejects a simultaneous manual amount, including zero. An
unsupported whole-set basis leaves calculated fees and selling-cost totals null;
manual assumptions cannot bypass the gate. No persistence, migration, providers,
presets, buyer-tax/order modeling, later phases, commit or push. Review is pending.

## Accepted Slice 2A closeout — 2026-09-17

Brian accepted Purchase Limits technically and visually, including normal currency
precision in the cap disclosure with raw recurring decimals omitted from product UI.
Exact server values, cent-floor feasibility and evidence/lifecycle protections remain
unchanged. [ExecPlan 072](plans/072-purchase-limits.md) records the bounded 21-file
local checkpoint authorization. Slice 2A is closed; 2B remains unstarted and requires
separate explicit authorization. No push or completion claim for the rest of 7A2.

## Phase 7A2 Slice 2A — accepted purchase-limit boundary, 2026-09-16

Brian authorizes [ExecPlan 072](plans/072-purchase-limits.md) through validation and
review only. Whole-set break-even is the greatest cent purchase price with estimated
profit >= 0 under the same qualified basis; it is not part-out break-even lots.
Explicit transient ROI/minimum-profit constraints produce both signed caps, the
lowest feasible maximum, binding targets and signed asking-price headroom. Omitting
the asking price is permitted in the opt-in analysis, leaving dependent outputs null.
No targets enabled means no target recommendation. Infeasible and unavailable amounts
stay null with reasons; zero acquisition never gains a defined ROI.

The initial acquisition model has fixed expenses plus independent tax/premium rates
applied directly to purchase price. Preserve exact charges until display rounding.
No tax-on-premium, tiers, per-charge tax rounding or unsupported bases are inferred.
Purchasable caps floor to cents and are verified against exact costs/constraints;
rounded raw quotients are explanation-only. Keep Slice 1 contracts and evidence
semantics; extend its existing endpoint with an explicit versioned request/result.
No persistence/schema/provider activity. 2B selling-fee rules wait for separate
authorization after 2A review; provisional contents/strategy work remains unstarted.

## Accepted Slice 1 closeout — 2026-09-16

Brian confirms technical and visual PASS for Whole-Set Deal Economics Slice 1 and
authorizes exactly one local checkpoint on `main`. Preserve the reviewed behavior
and the three unrelated modified files. The [ExecPlan 071](plans/071-whole-set-deal-economics.md)
23-file inventory is the commit allowlist. No push, Slice 2 or expanded economics.
This supersedes earlier pending visual-acceptance and no-commit statements for
this bounded checkpoint only; private, personal, non-commercial use remains binding.

## Phase 7A2 Slice 1 — accepted whole-set economics boundary, 2026-09-15

Brian accepts the narrowed [ExecPlan 071](plans/071-whole-set-deal-economics.md).
Use exact internal whole-set valuation results with an opaque reviewed-basis
revision and read-only revalidation. Client market amounts are not inputs.
Explicit selected-market/manual sale assumptions and manual transaction amounts
produce estimated gross/net/acquisition/profit/ROI; signed economics leaves the
accepted valuation validation unchanged. PARTIAL/BLOCKED/UNKNOWN never gain full
dependent economics, STOCK remains a what-if and zero acquisition has undefined ROI.
Same-condition diagnostic evidence participates in the basis revision without
mixing price views. Ineligible diagnostic evidence cannot block an otherwise
eligible price merely by contributing a past deadline.

The transient Deal editor shares the existing set-page lifetime and refresh owner.
No targets/caps, complex fee policy, profiles, persistence/auth, overlays, residual
or recovery model, alternative-strategy economics or Hunt enters this slice.
Later contents planning remains provisional. Technical and Brian visual acceptance
are separate; no commit/push or next slice follows automatically.

## Accepted private-use and 7A1 visual revision constraint - 2026-09-15

Arbitrage / BrickVault Appraisal App is permanently a strictly private, personal,
non-commercial application used only by Brian for his LEGO collecting hobby and
finding good deals. It will not be publicly distributed, offered as a service,
monetized, or used as a commercial product. This supersedes earlier assumptions
about potential commercial/public use; it does not establish blanket provider rights.

Brian explicitly authorizes the exact retained Rebrickable set-image reference for
catalog identification in 7A1, resolving this bounded display gate. Use direct image
display with restrained source attribution, no gallery, cache, acquisition subsystem,
provider switch, guessed URLs or seller-condition inference. Image provenance and
availability are independent of market evidence and its accounting. Preserve prior
technical acceptance; the first 7A1 visual design was rejected. The substantial
product-hero / market-matrix revision is authorized; visual acceptance remains pending.


### D-033: accepted 7A1 plan refinements - 2026-09-15

Brian accepts and authorizes frontend implementation under [ExecPlan 070](plans/070-set-detail-information-architecture.md). Value Scenarios replaces the proposed Part-Out section, preserving the selected representation. Market and Evidence have distinct comparison/refresh versus audit responsibilities. Expiry gates every appraisal-derived surface, including collapsed content; retained identity is identity only. Native URL context and one set-scoped refresh owner preserve confirmation, recovery and polling across sections. No API/domain/dependency change, provider/database activity, 7A2, staging, commit or push is authorized. Technical completion and Brian visual acceptance are separate gates.

### D-033 — Decision-first UI architecture — 2026-09-14

**Status: ACCEPTED by Brian; documentation-only execution.** Phase 6 is closed by
the retained [live acceptance](plans/060-product-surface.md#phase-6-live-acceptance-and-closure--2026-09-14).
Earlier pending-live entries below remain historical; Phase 7 has not started.

Insert **UI-01 — Shared Shell and Persistent Set Search** before Phase 7, preserving
all numbered phases. The [canonical UI/UX architecture](UI_UX_ARCHITECTURE.md) adopts
BrickEconomy-inspired information hierarchy, restrained financial/data presentation,
persistent set search, progressive Scout/Hunt/Watchlist/Deals navigation, compact
Set Detail, shared market/strategy context and responsive sourcing. The primary
workflow is acquisition decision-making, not investment/community browsing. This
does not clone a site, create a provider integration or rename the product.

The boundary precedes Phase 7's editable economics and saved workflows, avoiding
immediate frontend rework. Deferring the shell would rebuild that work; folding it
into a large Phase 7 coding slice obscures acceptance; a standalone redesign phase
would pull forward unsupported capabilities. UI-01 has its own
[bounded ExecPlan](plans/061-ui-foundation.md), with no backend/API or domain changes.

Phase 7 retains its capability ownership, with separate acceptance boundaries:
**7A1 — Set Detail Information Architecture**, **7A2 — Deal Economics**,
**7B — Authentication and Reproducible Saved Deals**, and **7C — Watchlist / Targets
/ Settings / Saved Deal Index**. Do not combine 7A1 and 7A2 into an indivisible coding
slice. The detailed Phase 7 ExecPlan is deferred until separately requested.

Accepted four-view independence, physical/quantity/assembly integrity, exact server
arithmetic/final-only rounding, partial/null semantics, scenario qualifications,
eligibility/freshness/coverage, provenance, retained evidence and provider confirmation/
accounting remain authoritative. UI exposes these states without inventing support,
summing strategies or hiding material blockers. Current data presentation comes
first; narrow read projections require real use; missing capabilities retain their
phase gates. No speculative navigation, chart or value may imply an absent capability.

Hunt remains Phase 8; actual outcomes remain Phase 16; image/listing/recognition/
capture remain Phases 13–15. Authentication/persistence design and source-retention
compatibility remain Phase 7 gates. This decision authorizes documentation, not code,
dependencies, runtime/provider changes, deployment, staging, commit or push. Reversible
UI work must preserve existing behavior and unrelated files; validate per slice with
focused regression and responsive/accessibility review.

### D-033 implementation acceptance and follow-up — 2026-09-15

Brian accepts UI-01 technically and visually: COMPLETE / ACCEPTED / CLOSED, with
the reviewed implementation preserved and no polish pass. One local architecture
and UI-01 checkpoint is separately authorized; unrelated protected work and push
are excluded. Phase 6 remains CLOSED; Phase 7 remains NOT STARTED.

The existing Set Detail observations are deferred design considerations for 7A1,
not UI-01 defects. [ExecPlan 061 closeout](plans/061-ui-foundation.md#ui-01-visual-acceptance-and-closeout--2026-09-15)
records Brian's compact, light/neutral identity and valuation-first direction and
the continued separation of 7A1 presentation from 7A2 Deal Economics. D-033's
accepted architecture and numbered phase ownership remain unchanged.

## Phase 6B — Public complete-set workflow (2026-09-14)

The separately authorized product workflow wraps accepted migration 0008 without
new schema or dependencies. Read-only planning and all GETs never dispatch or load
provider credentials. Confirmation and explicit Resume alone start bounded execution
under the same durable operation/root and exact 4/4/2/10 ceilings. Public responses
project safe progress and omit provider account identifiers and native evidence.

An application HMAC authenticates the public confirmation receipt; its signing key
stays in the API process and is unrelated to provider authorization signatures.
Unconfirmed plans replan after API restart. Confirmed retries recover the immutable
stored receipt even when concurrent execution has changed the current plan. No new
plan ledger, accounting store, worker service or automatic restart dispatcher exists.

Only COMPLETE_SET's four USD/US views participate. Eligible cache and confirmed-empty
evidence are reused; contents remain independently blocked/unknown. Provider scopes,
suspension and stricter budgets remain authoritative. First real product acceptance
and development migration remain pending after review/checkpoint. Details and
validation are in [ExecPlan 060](plans/060-product-surface.md#phase-6b-public-workflow-implementation--2026-09-14).

## Phase 6B — Approved durable backend prerequisite (2026-09-14)

Brian explicitly authorizes additive migration 0008 and offline implementation of
typed calibration/product roots, durable product operation/view associations and
bounded normalized discovery evidence. The accepted attempt ledger and price worker
remain authoritative. UUID4 keys use database timestamps for the 15-minute initial
confirmation window; no UUID dependency is added. Product roots retain 4/4/2/10
ceilings without category transfer, and lower provider/group budgets still win.
Product admission lasts at most 24 hours, discovery content at most 24 hours and
operational metadata uses existing policy (currently 30 days), with purgeable content
references and narrow runtime capabilities. Discovery success/evidence is atomic;
mapping review remains a separate conservative deterministic step. This supersedes
the historical no-0008 stop only for this prerequisite. No public refresh API/UI,
live provider access, development migration or Phase 7 is authorized. See
[implementation and acceptance](plans/060-product-surface.md#phase-6b-durable-prerequisite-implementation--2026-09-14).

## Phase 6A accepted implementation scope — 2026-09-13

Brian authorized local search/detail over accepted catalog and Phase 5 calculations.
This additive entry changes no financial policy or provider ceiling. The product API
pins the official accepted catalog and requires a unique existing cached USD/US
account scope; otherwise market evidence is unavailable. Private account IDs are
not public. Four strategies and four market views remain independent. Recorded
source quantities never establish physical totals. Failed physical assessment
blocks contents strategies even when market evidence exists. Synthesis remains a
labeled uncalibrated gross scenario without proceeds, profit, ROI or max-buy policy.
The browser clears evidence when its earliest current eligibility deadline arrives.
Phase 6B discovery/refresh requires separate authorization. No migration, dependency,
provider call or provider credential loading. [ExecPlan 060](plans/060-product-surface.md)
records the implementation and subsequent independent acceptance for the local checkpoint.

## Phase 5C — Approved uncalibrated synthesis policy (2026-09-12)

Brian approves Model A as immutable `valuation-synthesis-v1`, labeled partial/subset
dollars, and ending bounded Phase 5 after 5C acceptance. The exact contract is in
[ExecPlan 050](plans/050-valuation.md#phase-5c-approved-implementation-contract--2026-09-12).
Recovery factors are application assumptions, not calibrated provider facts,
expected proceeds, sale probabilities or a promised horizon.

The historical Liquid POV unadjusted-subset definition is preserved and superseded
for 5C by policy-adjusted gross scenarios. Unknown factors remain null; zero factors
exclude from a scenario without declaring inventory worthless. Thin-sample exposure
remains unknown. Partial metrics never create full amounts. Concentration changes
neither dollars nor sample categories. Gems await real user experience and approved
thresholds. Economic ranking, costs/profit/ROI/max-buy/offers and Hunt scoring remain
later work. No provider activity, schema, public interface or persistence is added.
Independent acceptance corrects zero-activity sample quality without changing policy:
numeric S=O=C=0 is THIN_SAMPLE evidence with UNKNOWN liquidity and null dollars.
The 13-file local checkpoint completes bounded Phase 5; see
[acceptance evidence](plans/050-valuation.md#phase-5c-independent-acceptance--2026-09-12).
Phase 6 requires separate authorization.

This file preserves durable decision history. The original D-001 through D-017 text below records earlier approvals, not an instruction to revive superseded scope. Current applicability is determined by the additive D-018 through D-021 decisions. References to image-first Phase 1 or the former plan path in historical entries are superseded as stated below.

## Accepted

### D-001 — Private single-user product

The application is built solely for Brian. No public registration, billing, team roles, or app-store distribution is required.

### D-002 — Self-hosted source of truth

Images, labels, appraisals, and provider credentials will be controlled by Brian's server. Clients call the server rather than external providers directly.

### D-003 — Save training-useful data from the beginning

The MVP must preserve immutable originals, useful crops, prediction history, and Brian's corrections. Dataset labeling is part of the product, not an afterthought.

### D-004 — Human confirmation separates prediction from truth

An AI result cannot automatically become a verified training label.

### D-005 — Retrieval and verification precede custom training

Index reference images and metadata, retrieve candidates, and use multimodal verification before investing in a custom model.

### D-006 — Explicit user-triggered Facebook capture only

Do not scrape, intercept, or autonomously navigate Facebook. Brian triggers each capture/session.

### D-007 — Keep ordinary uploads and Android Share as fallbacks

The app must remain usable when the overlay/accessibility path breaks or Facebook changes its UI.

### D-008 — Risk-first development

Prove the image-storage path, Android capture feasibility, and recognition quality in isolated milestones before building the complete workflow.

## Accepted foundation decisions — 2026-09-05

Brian approved these decisions during architecture review and the documentation checkpoint. Their implementation is a separate task. D-001 through D-008 above retain their original text.

### D-009 — React + Vite + TypeScript browser UI

Use React + Vite + TypeScript in `apps/web`. This supersedes browser framework proposal P-002. Keep the frontend cleanly separated from the server and its static host.

### D-010 — FastAPI production static serving

FastAPI is the API and production application server and serves the frontend's static build from a configurable directory. Static serving can later move to Caddy or another reverse proxy without rewriting the frontend. No production deployment is authorized by this decision.

### D-011 — API namespace and generated contracts

All server API routes use `/api`, including health, readiness, and OpenAPI. Clients use the same server contract; the web build uses relative `/api` URLs and a Vite development proxy. Generate TypeScript from Pydantic-derived OpenAPI in `packages/contracts` and use `openapi-fetch`. API errors must not become frontend HTML responses.

### D-012 — Independent partial-success uploads

Send one image per multipart request. Each file has its own result and transaction. Preserve successful uploads when another fails; allow retrying/removing a failed file without re-uploading successes. Successful images may proceed to analysis in later milestones despite other failures. Phase 1 adds no analysis.

### D-013 — Idempotent per-file retries and successful duplicate receipts

Assign a client upload UUID before dispatch. The request includes intended `display_order`; retries preserve the UUID, bytes, and position. Every successful result, including an exact duplicate, creates or reuses a durable receipt. Replay returns the stored result and relationship without additional records. A committed UUID reused with different bytes or order yields `UPLOAD_ID_CONFLICT`. Store successful receipts and any relationship/order changes in one transaction.

### D-014 — Listing-image identifier

The per-file result field is `listing_image_id`. It identifies the listing-to-image relationship; it is distinct from the original asset ID, thumbnail asset ID, and physical blob hash. Return it for both successful new and duplicate uploads, and use null for failures.

### D-015 — Deterministic persisted image ordering

Assign consecutive intended `display_order` values in client selection order before uploads begin, using the server receipt high-water mark and outstanding local queue positions. Retry the same position. Persist each receipt's intended position and each unique listing image's minimum successful receipt position. This handles duplicates arriving out of order without making the final display order depend on request completion or commit order.

Enforce unique `(listing_id, client_upload_id)` and `(listing_id, display_order)` on receipts, plus unique original and position per listing-image relationship. Return `DISPLAY_ORDER_CONFLICT` for another UUID claiming an owned position; do not silently reassign it. Removing/reselecting only the failed file after refreshing positions is a new submission with a new UUID, not an ordinary retry. Gaps and duplicate receipt positions remain accounted for by the high-water mark. ExecPlan 000 defines the exact transaction and acceptance scenarios.

### D-016 — Foundation architecture and scope

Use a Python/FastAPI modular monolith, PostgreSQL with SQLAlchemy/Alembic migrations, and immutable content-addressed filesystem blobs behind a `BlobStore` interface. Separate physical blobs from semantic image assets, lineage, listing relationships, and receipts. Use uv for Python and pnpm for web/contracts. No runtime schema creation, queues, background workers, MinIO, AI, Android, authentication, or remote deployment in Phase 1. Development is loopback-only and uses isolated PostgreSQL instances.

This adopts proposals P-001 and P-005. P-004 is adopted as PostgreSQL now, pgvector only when retrieval is implemented. P-003 remains the accepted future direction: native Kotlin/Jetpack Compose Android, with exact toolchain and physical-device feasibility established in its own milestone.

### D-017 — Documentation checkpoint and historical starter

The active sources of truth are checked-out guidance, current documents, and `docs/plans/000-foundation-and-risk-spikes.md`. The starter ZIP is historical material and is not restored or consulted as active instructions. A documentation checkpoint does not authorize implementation, dependency installation, service startup, home-server access, or a Git commit. Start Phase 1 only after a separate explicit implementation request.

## Accepted realignment decisions — 2026-09-05

### D-018 — One unified valuation-first product

Brian establishes one private LEGO sourcing and appraisal platform. Deterministic catalog identity, set/minifigure quantities, provider mappings, market observations, valuation, saved work, and Sets to Hunt form the foundational core. Direct suffixed set-number/name search must work with every image feature disabled.

This supersedes D-008 only with respect to development sequencing: image storage, Android capture, and recognition move to Phase 13 onward rather than gate the sourcing MVP. Its rationale for bounded, evidence-backed risk work remains; the early risks are now provider mappings, rights, coverage, and deterministic financial correctness.

D-003's "from the beginning" scope starts when image ingestion is implemented, not in the catalog/valuation foundation. Its original retention rationale remains, subject to an explicit privacy/retention/deletion policy before that later feature ships. D-005's retrieval-before-custom-training rule applies within the later recognition module, not before deterministic sourcing.

D-001, D-002, D-004, D-006, and D-007 remain substantively applicable; image-specific obligations take effect in their later module. Recognition returns candidate canonical identities into the same catalog/relationships/mappings/market/valuation core and owns no duplicate catalog or financial engine.

### D-019 — Shared React interface for Chrome, PWA, and Android

Use the same primary React + Vite + TypeScript application for responsive Chrome, an installable PWA, and an Android package, preferably through Capacitor unless a documented Phase 9 spike proves a better choice. All share one FastAPI API, user data, and authoritative PostgreSQL database.

This supersedes D-016's reference to P-003 as a native Kotlin/Compose core-client direction. Native code may extend apps/android later for genuinely required Share/overlay behavior; it does not reimplement core screens, provider calls, or valuation rules. Packaging and physical-device compatibility remain unverified.

Initial offline behavior is read-only access to permitted, explicitly dated cached views. Fresh search, recalculation, and writes require the backend; online edits use server revisions and explicit conflicts. Client caches are not authoritative databases.

### D-020 — Authoritative financial, identity, and evidence rules

Adopt [VALUATION_RULES.md](VALUATION_RULES.md) and [DATA_MODEL.md](DATA_MODEL.md): exact decimal money, explicit currencies/conversions, quantity-bearing set/minifigure relationships, verified provider-scoped mappings, separate new/used and sold/listing evidence, and missing data as unknown.

Sale strategies cannot double-count physical figures/builds/components. Define gross/selling/net proceeds, acquisition-dependent costs, profit, ROI with zero-cost undefined state, target-ROI and minimum-profit maximums, conservative rounding/clamps, and deterministic versioned explanations. Missing required evidence blocks recommendations.

Phase 4 representative feasibility must establish supported sourcing evidence before confidence is claimed. Provider access/rights/retention, live coverage, and device behavior remain future gates; documented endpoints or fixtures do not prove them.

### D-021 — Rebased foundation and preserved later contracts

Replace the unexecuted image-first ExecPlan 000 with [000-local-foundation.md](plans/000-local-foundation.md), covering only local web/API shells, isolated PostgreSQL, migration tooling, generated health/readiness contracts, checks, and setup documentation. It has no product tables or image/listing/provider routes.

D-009 React/Vite, D-010 FastAPI static serving, and D-011 /api/generated contracts remain active. D-016's modular monolith, PostgreSQL/Alembic, uv/pnpm, loopback isolation, and no unnecessary infrastructure remain active; image/BlobStore work moves out of Phase 1.

D-012 through D-015 remain accepted upload semantics for Phase 13: independent partial success, listing_image_id, stable client UUID/position retries, deterministic persisted minimum-receipt ordering, and durable successful-duplicate receipts. Historical references to Phase 1 in those entries no longer assign their implementation phase. The complete preserved contract is [IMAGE_INGESTION.md](IMAGE_INGESTION.md).

D-017's stop/authorization and historical-ZIP boundaries remain active; its former plan path is historical and replaced by the link above. The current checkpoint is documentation realignment. After Brian reviews it, the next action is Prompt 01 in Plan mode; implementation still requires a separate explicit request.

The roadmap and prompts now align one-to-one from 00 through 16. Phase 10 hardens only a local release; Phase 11 requires separate read-only home discovery authorization; Phase 12 requires a reviewed plan and distinct deployment approval. No current server/DNS/production access, application implementation, dependency change, staging, or commit is authorized.

## Accepted documentation baseline refinement — 2026-09-05

### D-022 — Canonical Phase 1 plan, portable paths, and bounded execution

Persist the approved detailed [ExecPlan 000](plans/000-local-foundation.md) as the canonical Phase 1 execution plan. D-001 through D-021 retain their original text and accepted historical meaning; earlier current-checkpoint sentences describe their dated approvals rather than the latest task state.

Use repository-relative paths wherever sufficient; no machine, username, or checkout location is an architectural requirement. Phase 1 has three separately authorized slices: 1A toolchain/workspace and exact locks; 1B isolated PostgreSQL, SQLAlchemy/Alembic, API and generated contracts; 1C responsive web shell, built serving, CI and complete acceptance. Completing one slice never authorizes the next. The split does not weaken final acceptance or add product-domain, image, provider, PWA/Android, or deployment work.

The Slice 1A plan includes an exact-lock local checkpoint only under an explicit slice execution/local-Git request. The present checkpoint authorizes documentation and one reviewed local baseline commit only, with no push; it authorizes no implementation, installs, services, database connections, networks, or infrastructure access.

During Phase 1 implementation, AGENTS.md, ORIGINATING_CHAT_SUMMARY.md, PRODUCT_SPEC.md, VALUATION_RULES.md, and SECURITY_PRIVACY.md are read-only by default. Change one only for a concrete verified contradiction that cannot be accurately documented elsewhere; propose a narrow evidence-backed change and report it explicitly. Normal progress belongs in the current workflow/setup/plan/roadmap/traceability documents listed in ExecPlan 000, with architecture edits limited to verified details.

[CODEX_WORKFLOW.md](../CODEX_WORKFLOW.md) and ExecPlan 000 carry current checkpoint and slice status. Prompt 01 remains reusable plan-only review; the next separately authorizable implementation action is Slice 1A only.

### D-023 — Approved Slice 1A tooling corrections — 2026-09-05

Brian authorizes TypeScript >=5.9.3,<5.10, initially 5.9.3, with openapi-typescript 7.13.0; this supersedes the incompatible TypeScript 6 proposal. ESLint >=10.0.0,<11, initially 10.10.0, with @eslint/js 10.0.1 and typescript-eslint 8.69.0 replaces the end-of-life ESLint 9 proposal. Select one workspace compiler and preserve strict peer checks, supported flat configuration, and stable supported direct dependencies.

Official standalone uv 0.12.10 may be installed under ignored .local/tooling/uv/0.12.10/ with published artifact integrity verification. Invoke it explicitly and enforce its exact version. Global uv 0.10.7 and system/user configuration remain untouched; no automatic Python downloads are permitted. Retain Hatchling and use --no-install-project only for Slice 1A dependency synchronization, with actual application installation/build required once source exists.

Persist these approvals even if subsequent installation is blocked; approvals are not test evidence. Slice 1A alone is authorized, with working-tree changes retained for review and no staging/commit, application source, services, databases, infrastructure, or automatic advancement. D-001 through D-022 retain their historical meaning.

### D-024 — New and used set part-out values — 2026-09-06

Brian requests separate new/used set part-out values in the sourcing product. Add the feature through Phases 2–6 under [the part-out plan](plans/005-set-part-out-values.md): quantity/color-aware inventory, verified component pricing, feasibility, deterministic aggregation, and set-detail display. These are theoretical component totals with evidence and coverage, distinct from supported net proceeds/profit/max-buy. Assembled figures and their components cannot both count. Operational individual-piece selling remains outside the initial scope.

Public BrickLink documentation describes subset inventories and per-item guides; aggregate API availability, live account access, rights, coverage and website-calculator parity remain unverified. No provider calls or Phase 1 feature implementation is authorized by this planning addition. D-001 through D-023 retain their history.

### D-025 — Core part-out and liquidity intelligence — 2026-09-06

Brian authorizes a documentation-only product amendment expanding D-024 through existing Phases 2–8. Preserve its identity, quantity, inclusion, coverage and theoretical-value rules. Add four NEW/USED × SOLD/CURRENT POV views, expected recoverable gross, part activity/liquidity/opportunity analysis, Part-Out Gems, Liquid POV, Fast Cash Value, Dead-Stock Exposure, concentration, break-even lots, value density, burden, competition, rarity, strategy comparison and first-class Hunt components under PRODUCT_SPEC R-11 through R-37 and [the amended plan](plans/005-set-part-out-values.md).

Full part-out economic analysis becomes core; the earlier exclusion for operational piece listing/fulfillment remains. Selective harvest stays deferred until supported. Expected recoverable POV means gross before itemized selling costs; net proceeds and profit follow D-020, with no repeated cost deduction. Current supply and interval sales support explicitly labeled proxies, not historical inventory turnover or guaranteed liquidation. Missing evidence is neither zero value nor proven dead stock.

Phase 3 must verify permitted direct aggregate capabilities without assuming one exists, normalize exact part/color observations and design shared caching/priority background refresh in the existing backend/PostgreSQL architecture. Phase 4 validates provider equivalence, coverage, recovery assumptions, liquidity classifications and candidate Hunt weighting before policy thresholds are selected. No arbitrary coefficients, final weights or numerical liquidity cutoffs are adopted here. “BrickLink Part Out Value” requires demonstrated equivalence and permitted terminology/display use.

This request expressly permits the required additive product, valuation, architecture and model clarifications despite D-022's default Phase 1 implementation documentation restrictions. It changes no Phase 1 deliverable, security/deployment/image decision, dependency or implementation. D-001 through D-024 retain their original text and history. No provider contact, installation, service/database/container startup, staging or commit occurs in this amendment; the next task is review and local commit of the documentation only.

### D-026 — Versioned catalog foundation and bounded Phase 2 slices — 2026-09-07

Brian approves [ExecPlan 020](plans/020-catalog-foundation.md) and separately authorizes Slice 2A implementation only. Canonical sets, parts, colors, minifigures, themes, categories and exact part/color combinations use application UUIDs. Provider identities remain separately namespaced and map through typed, evidenced review records. One typed inventory-line table represents exactly one part/color, minifigure, nested set or unresolved source target, preserving separate regular and extra quantities. Inventories preserve source identity/version, canonical owner and snapshot revision independently.

Use immutable source evidence, stable canonical identities and snapshot facts; freeze validated and accepted snapshots. Composite foreign keys enforce source-bundle, owner, part/color and snapshot compatibility. Matching candidates represent multi-line bundles with evidenced cardinality; component/nested bindings preserve explicit child revisions and partition state. Unknown semantics remain unknown. The partial unique verified-mapping constraint also applies while building candidates; competing proposals remain representable without two verified targets.

The approved image refinement excludes `catalog_image_reference` from 2A. No documented bulk reference field establishes a present need; later reference support requires source and rights evidence. Active-pointer and activation-history tables are deferred together to 2B under Brian's expressly permitted narrow deferral: their consistency needs the atomic activation transaction and concurrency verification. The approved immutable-candidate/atomic-pointer architecture remains unchanged. No activation API, command or placeholder behavior exists in 2A.

Migrations 0002/0003 carry independently frozen SQL resources; current SQLAlchemy Core definitions cannot retroactively alter them. Migration 0001 remains empty and unchanged. Runtime gets enumerated catalog SELECT grants only. The existing guarded owner/test paths, ports, dependencies and infrastructure remain authoritative. Slice 2B adds offline parsing/staging/import/activation only after separate authorization; 2C adds complete query semantics and 2D requires separately authorized official bulk acquisition. Synthetic 2A evidence proves no provider coverage. Changes remain unstaged and uncommitted for independent acceptance review.

### D-027 — Offline import and atomic activation implementation — 2026-09-08

Brian separately authorizes Phase 2B only at accepted checkpoint `5026ddf04bdcc8aed96e7d1aae9ef074572fce9b`. Implement D-026’s immutable candidate and atomic pointer design using twelve typed run-owned staging tables plus durable validation, pointer and activation-receipt tables in frozen migration 0004. Provider advisory ownership, bounded COPY transactions, candidate validation/freezing and explicit generation-checked publication preserve history. A caller-supplied receipt UUID makes uncertain activation commits recoverable; reactivation creates a new audited generation. Status is read-only: it classifies abandoned runs from lock evidence, and the next import persists interruption after acquiring ownership.

Only invented local fixtures are used. The structural source profile is documentation-verified/live-unverified; production accepts local gzip files only after separately approved acquisition. CSV fixtures have a narrow LF Git attribute so recorded hashes survive Windows checkouts. These implementation choices add no dependency, service, provider request, financial rule or query UI. [ExecPlan 020](plans/020-catalog-foundation.md) records verification; independent 2B acceptance and local checkpoint commit remain the next separate action. D-001 through D-026 are preserved.

### D-028 — Approved indexed catalog queries and synthetic semantics — 2026-09-09

Brian explicitly authorizes Phase 2C implementation and subsequently resolves the
reported migration-plan gate by approving `0005_catalog_search_indexes`. It adds
only the documented normalized-name B-tree and PostgreSQL built-in `simple`
text-search GIN index, plus matching model/head/package checks. No extension,
denormalized product column, new table, dependency change or revision to migrations
0001–0004 is authorized by this exception. The original blocked-gate record remains
in [ExecPlan 020](plans/020-catalog-foundation.md).

Queries pin one accepted snapshot; physical expansion requires evidenced compatible
partitions and explicit required choices. Complete physical output never includes
both intact and expanded representations or unselected alternatives. Source
coverage remains independently unknown; incomplete physical selection yields
diagnostics without a misleading partial inventory. Raw source lines and lineage
remain queryable. Benchmarks distinguish synthetic PASS/FAIL from official DEFERRED;
they establish no provider rights, production scale, pricing or full Phase 2
acceptance. All 2C work stays uncommitted for independent acceptance review.

### D-029 — Bounded Phase 2C acceptance corrections — 2026-09-09

Brian separately authorizes independent Phase 2C review, substantiated bounded
corrections and exactly one conditional local checkpoint commit. Eight adversarial
real-PostgreSQL regressions reproduce three defects: containment selection
validation dependent on a matching target, unresolved targets omitted from
unassessed containment, and boundary whitespace surviving name normalization.

Validate supplied matching groups/options/cardinality before searching, in both
direct and expanded containment; preserve absence uncertainty for eligible
unresolved targets. Collapse whitespace before trimming and lowercasing in the
name query, model and still-uncommitted 0005 B-tree expression. The migration
remains exactly two indexes with unchanged 0001–0004, tables and dependencies.
Strengthen natural planner assertions and measure containment query counts without
forcing index scans or claiming official-scale performance. [ExecPlan 020](plans/020-catalog-foundation.md)
records reproduced failures, corrections and final independent acceptance gates.

D-001 through D-028 and the historical blocked migration proposal retain their
meaning. The local checkpoint requires passing final and staged audits. Phase 2
remains incomplete; Phase 2D official acquisition, real-source feasibility and
performance evidence require separate authorization. No provider contact, pricing,
Part-Out Value, liquidity, valuation, Hunt, catalog API/UI or push is authorized.

### D-030 — Phase 2D metadata policy evidence and training restriction — 2026-09-09

Brian explicitly clears the previously blocked metadata policy gate with current
first-party Downloads/Terms text viewed in normal Chrome. The
[provider record](PHASE_2D_PROVIDER_GATE.md) preserves the failed automated page
retrieval and subsequent user-supplied evidence. The Downloads page's specific
compressed-CSV automation exception permits the listed bulk metadata resources
under once-daily acquisition and Rebrickable acknowledgement; it does not permit
page scraping, arbitrary bot traffic, browser credential reuse or challenge bypass.
Local metadata acquisition/storage/application use is authorized, while full-source
redistribution and all image implementation remain outside this phase.

Current Terms prohibit training AI models with Rebrickable content, including its
images and downloaded catalog metadata. Future training data must come from
independently permitted/user-owned sources unless separately reviewed explicit
provider authorization is obtained. Image display permission and metadata import
do not establish training rights. No image, AI, financial or Phase 3 code follows
from this decision. Existing accepted decisions and the historical policy stop
remain intact; all Phase 2D activation/source-semantic gates still apply.

### D-031 — Correct official bulk relationship codes before import — 2026-09-09

Brian supplied current first-party Rebrickable Downloads-page text: `(P)rint, Pai(R), Su(B)-Part, (M)old, Pa(T)tern, (A)lternate`. This supersedes the prior B=pair/S=sub-part planning assumption. Current accepted codes are exactly P=print, R=pair, B=sub_part, M=mold, T=pattern, A=alternate. S is not an alias. The prior 2,987-row R rejection correctly stopped acquisition-to-canonical progression and remains historical evidence. Correction and complete cached profile verification occurred before canonical construction.

Source code, direction, evidence and both identities remain separate. Pair does not merge parts; sub-part does not supply a complete quantity/color component inventory; alternate does not establish an inventory choice group. No physical, mapping, pricing or activation invariant is changed. Actual counts and first-acquisition hash verification are in [the official evidence report](PHASE_2D_OFFICIAL_EVIDENCE.md). Existing synthetic source files contain only P and were not rewritten; historical database snapshots are not edited.


### D-032 — Phase 2D direct containment and source-color sentinel — 2026-09-09

Brian authorizes correction of the confirmed catalog-wide prefilter limit and supplies the application meaning of Rebrickable 9999 `[No Color/Any Color]`. Direct containment starts with exact target lines in PostgreSQL, selects applicable revisions, and guards distinct matching output with limit+1. Coverage remains globally assessed, with exact unassessed count and bounded diagnostic IDs; unknown absence, possible alternatives, extras and pinned source evidence remain explicit. Recursive expansion retains independent safety limits. No index or migration is authorized or introduced for convenience.

Existing color facts encode `sentinel` separately from `known` physical color and `unresolved` unknown color. The exact -1 `[Unknown]` identity stays distinct. Physical observations/element mappings associated with 9999 remain unresolved by exact color, without deleting identities, source lines or quantities. RGB supplies no physical-color inference. Exact 9999 matching is never a wildcard. Future market/POV joins require explicit provider mapping evidence; no price code is introduced. Import/validation versions advance for changed normalization; historical snapshots remain immutable.

Acceptance must rerun from cached original bytes in fresh disposable PostgreSQL before the separately gated development activation. Preserve all policy, relationship and failed acceptance history. Do not redownload, stage, commit, access infrastructure or begin Phase 3.


Official repeat acceptance exposed reference-query planning against statistics from the prior COPY run. The importer now explicitly analyzes each completed staging table before structural checks, making validation independent of asynchronous autovacuum scheduling. This updates planner statistics only; it adds no index, migration, dependency, retention policy or source-semantic rule. A real PostgreSQL regression disables automatic maintenance on isolated fixture tables and confirms both new/prior run IDs are available to the planner and the repeated import is an auditable no-op. The prior slow statement, cancellation and cleaned disposable run remain recorded in the Phase 2D evidence.


## D-033 — Preserve development at the construction-timeout gate (2026-09-09 local)

**Historical Phase 2D outcome — 2026-09-09 local: BLOCKED at development candidate construction.** The containment and color-9999 corrections pass fresh official acceptance (72 PASS, zero FAIL/DEFERRED/UNSUPPORTED/UNAVAILABLE) and a verified cached no-op repeat. All 189 PostgreSQL and six browser/API/static regressions pass. Development required the existing accepted migration 0005, then its full official build hit the existing 300-second statement timeout before candidate validation or activation. Its two synthetic snapshots, four receipts and generation-4 active pointer remain unchanged; the official pointer is empty at generation 0 with zero receipts. Phase 2 remains incomplete and Phase 3 is not started. Work is uncommitted; the next task is to diagnose the retained-development build timeout before resuming Phase 2D. Earlier gates below remain history. The existing migration 0005 was required and applied without changing historical snapshots/receipts/pointer. The failed import remains terminal and its unvalidated candidate remains unpublished. No timeout increase, failed-run resume, guessed query fix or official activation is accepted. Exact statement/query-plan diagnosis remains required.

## D-034 — Reconcile existing evidence before inserting fresh evidence (2026-09-09 local)

The authorized disposable retained-history reproduction identifies
`evidence_reconcile:inventory_parts` as the exact 300-second timeout. With statistics
from 58 synthetic evidence rows, PostgreSQL chooses a merge join on source-file ID
and filters row locators after joining, estimating two matches for a 1,557,375-row
file group. The fresh control uses a hash join on both keys and finishes the same
SQL in 57.243333 seconds; its complete 72-case benchmark and cached no-op pass.

A separate disposable savepoint reproduces the bad natural plan, refreshes only
`catalog_evidence` statistics and executes the identical UPDATE with EXPLAIN ANALYZE
and buffers. It changes to a two-key hash join, processes 1,557,375 matches against
1,867,494 evidence rows and completes in 46.949014 seconds. The savepoint and UPDATE
data changes are rolled back; all diagnostic statistics are discarded with the
disposable database. This experiment proves
the plan/statistics dependency; it is not a development repair command.

Freshly inserted evidence already has its staging-reserved UUID. Candidate construction
now reconciles only preexisting evidence before inserting fresh rows. This removes the
unnecessary full-file rewrite and the newly created duplicate-key join group while
preserving frozen-source reuse. No index, migration, planner setting, timeout change,
source-semantic version change or cleanup policy is introduced. The real PostgreSQL
regression fails under the previous ordering and passes after correction, including
exact existing-evidence reuse and immutable historical evidence. Full corrected
fresh/retained acceptance and regressions remain prerequisites for a new development
run; the terminal failure from D-033 must remain unchanged.

## D-035 — Refresh committed candidate inventory statistics before validation (2026-09-09 local)

The evidence-order correction passes full retained and fresh acceptance, but exposes
an avoidable validation plan: `validate:inventory_sets:inventory_owner` estimates
2,043 candidate lines, materializes the snapshot, and rescans it for 5,210 source
rows. The snapshot actually contains 1,588,405 lines. The instrumented fresh query
takes 201.036245 seconds; retained validation also exhibits temporary spill reads.
The inventory-line table has no ANALYZE statistics when that plan is chosen.

Controlled disposable experiment `94970d8448ec4b19b008609b8c882948` disables automatic
analysis only on its inventory-line table, reproduces the materialized plan, then
refreshes only that relation's statistics inside a savepoint. The identical SELECT
uses the existing `ix_catalog_inventory_line_evidence_id_source_version_id` index,
has no Materialize node, and completes in 33.701 ms. The savepoint ends without
retaining data changes; the disposable database and all diagnostic statistics are
removed. No new index or planner switch is involved.

The importer now explicitly analyzes `catalog_inventory_line` in a separate owned
transaction after candidate construction commits and before validation plans are
selected. This is a measured maintenance boundary on one shared fact table;
historical rows are unchanged. Existing staging analysis remains in place. Import
and validation semantic versions remain unchanged because catalog meaning and
validation rules are unchanged. The 300-second statement limit remains unchanged.
A deterministic real PostgreSQL regression disables automatic maintenance on its
isolated table, verifies exact relation cardinality and the new snapshot's column
statistics before validation on initial/refresh imports, and fails before this
correction. All four focused construction/history/telemetry/statistics tests pass
afterward. Final fresh/retained acceptance and full regressions still gate development.


## D-036 — Preserve development after progress-report publication failure (2026-09-09 local)

D-034/D-035 pass corrected fresh and retained official acceptance (72 cases/no-op),
192 PostgreSQL regressions and six browser/API/static cases before development is
accessed. A new development run completes the former timeout SQL in 0.448011 s with
the original failed staging present. It later fails in its progress callback after
successful default-minifigure SQL. A complete orphaned temporary report, missing
console completion and overlapping observer read narrow the failure to publication.
A disposable Windows handle-sharing experiment reproduces PermissionError/WinError 5
in the unchanged atomic publisher, with success after closing the reader. The
original OS error was not retained, so the overlapping reader's exact role remains
an evidence-backed inference rather than a captured native exception.

The new run is terminal failed/import_failure, its construction rolls back and its
candidate remains unvalidated with zero lines/validation rows. No official activation
occurs; generation 0/no receipt and synthetic generation 4/four receipts/two snapshots
remain unchanged. The original failed run/candidate and exact staging digests also
match. Both failures, cached source and file-publication experiment remain evidence.

Brian's original section 46 requires BLOCKED classification before development
activation. Do not resume either terminal run or sidestep the observer race by
avoiding reads. The next root correction must retain atomic complete-file publication,
handle bounded transient Windows sharing contention, preserve safe numeric failure
metadata and include a deterministic sharing regression. No such publisher change,
new migration/index, timeout increase, cleanup or Phase 3 work is made at this gate.
See the [32-item diagnostic report](PHASE_2D_BUILD_DIAGNOSTICS.md).

## D-037 — Atomic report publication and database authority (2026-09-09 local)

Brian authorized the bounded root correction after D-036. One shared standard-library publisher validates owned paths, serializes completely, flushes/fsyncs/closes an exclusive same-directory temp and atomically replaces with a five-second monotonic numeric Windows sharing/access retry policy. It never deletes the old report first. Exact owned-temp cleanup and independent allowlisted diagnostics preserve observability. Native CreateFileW release/exhaustion tests observe errno 13 / winerror 5; the original lost error remains unknown. Brian’s overlapping live read remains chronology, not proof of its original error code.

Only auxiliary atomic-replace availability can degrade progress; PostgreSQL run/snapshot/receipt state remains authoritative. Invalid serialization and final acceptance publication remain strict, including explicit acceptance writes inside callbacks. A report failure never substitutes for an activation receipt or authorizes blind SQL replay. The owner-only source-bound preactivation benchmark reads a frozen validated candidate in a read-only transaction; public queries still require accepted snapshots.

Required Windows gates pass: 264 Python units, 195 PostgreSQL tests, six browser cases, native publication regressions and corrected-runtime disposable official 72-case pre/postactivation acceptance plus cached no-op. NEW development run `53e6dc98-d0a4-4fe5-be78-3fddae4498bb` stages successfully but step 123 part_color_observations:inventory_parts times out at 300.007193 s. This new material failure ends the authorized attempt before validation/benchmark/activation; its SQL cause is unproven. Official generation stays 0 with zero receipts. Synthetic history and both prior failed histories are unchanged; the new third terminal failed run/staging are preserved. Final BLOCKED evidence and normal read/update succeed. No provider, schema/index, timeout, dependency, infrastructure or Git boundary changed. Phase 2 remains incomplete and Phase 3 is not started. [Design and required 33-item report](PHASE_2D_PUBLICATION.md).

## D-038 — Candidate color statistics before observation construction (2026-09-10 local)

The bounded retained-state diagnosis reproduces the observations timeout with two
accepted synthetic snapshots, four receipts, three failed official staging runs
and actual new-candidate prerequisites. Existing run predicates exclude every old
staging row logically. Tiny historical color-fact statistics instead estimate one
new-candidate color where 275 exist, selecting repeated inventory probes behind a
large underestimated part/color intermediate. No existing observation history is
joined by the statement.

An independent disposable reproduction changes only candidate color-fact statistics:
baseline SELECT times out at 300.005025 s; corrected SELECT takes 0.820762 s;
full rollback INSERT with all constraints takes 57.537484 s. Staging/identity
statistics, row cardinalities and historical facts are unchanged. Earlier sequential
savepoint probes are explicitly exploratory because relation estimates can survive
rollback; they are not the isolated causal proof.

Execute `ANALYZE catalog_color_fact` immediately after new candidate color facts
inside the constructing transaction. Automatic analysis cannot see those uncommitted
facts. The exact observation SQL, stable identities/evidence, sentinel interpretation
and retained history remain unchanged. No index, migration, timeout, semantic version
or dependency change is needed. A deterministic real PostgreSQL regression fails
before and passes after this correction; full retained-source disposable acceptance
passes 72 cases before/after activation and cached no-op. Complete regressions and
development acceptance remain separate gates. See [the observation diagnosis](PHASE_2D_OBSERVATIONS.md).

D-038 final execution gate: all 196 PostgreSQL tests and six browser cases pass. NEW fourth development run `bcf21407-15ab-44bb-b358-17f600282599` passes staging/bundle validation but times out at the separate earlier step 16 `evidence_conflict:elements` (300.004024 s, 57014). The corrected observation step is not reached. Its cause remains unproven. Read-only verification confirms candidate rollback, official generation 0/no receipt, both synthetic snapshots/four receipts/generation 4 and all three old failed histories unchanged. The fourth terminal failed history is preserved. No fifth attempt or further SQL correction occurs in this bounded authorization; diagnose the new evidence-conflict operation before a separately authorized new development attempt. Phase 2 remains incomplete; Phase 3 is not started.


## D-039 — Evidence statistics at changed dataset boundaries (2026-09-10 local)

A retained-heap disposable reproduction executes the fifteen actual prerequisites
before `evidence_conflict:elements`, with four failed official staging populations
and accepted synthetic history intact. It demonstrates 102,919 transaction-visible
evidence rows against an estimate of 58 in a large reusable heap. A nested loop
materializes the underestimated evidence relation; the SELECT times out at
300.007521 seconds with no blockers and observed temporary-file reads. Only
in-transaction evidence ANALYZE changes execution to 0.104259 seconds; analysis
costs 0.202576 seconds. Logical and large-index/compact-heap controls do not time out.
The sibling relationship check also takes 116.709883 seconds in retained-heap state.
The original development plan was lost; this reproduction and saved pre-failure
allocation/statistics establish the supported mechanism, not recovery of that plan.

After `evidence_insert:{dataset}` adds rows, explicitly analyze `catalog_evidence`
before downstream datasets consume that population. Include the final changed
population for identity construction and validation, and skip analysis when all
evidence is reused. Keep the exact conflict/reconciliation/insert SQL, constraints,
source identifiers and immutable provenance. This is a transaction-local lifecycle
correction; no schema, index, statistics target, timeout, dependency or semantic
version change is required. Preserve the existing staging, color-fact and inventory-
line analysis boundaries. Automatic maintenance cannot see new uncommitted rows.

The fresh acceptance runner no longer performs an extra database-wide ANALYZE before
benchmarking: acceptance must exercise the production lifecycle. Existing diagnostics
capture fresh activity snapshots, blocker IDs and target prepared-plan state. A new
statistics-readiness regression fails before correction; all four conflict/null
regressions pass before it, and nine focused PostgreSQL checks pass afterward.
Full fresh/retained acceptance, controlled failure/new retry, complete regressions
and the conditionally authorized fifth development attempt remain separate gates.
See [the current planning diagnosis](PHASE_2D_OBSERVATIONS.md).


## D-040 — Statistics before mapping validation and expansion binding (2026-09-10 local)

The retained failed-construction/new-retry discovery run passes, but its plans expose
additional avoidable work. Expansion binding estimates one current inventory line
and takes 20.820696 seconds; set metadata validation materializes an estimated 24
current mappings where 28,278 exist and takes 14.939172 seconds. Review these before
development instead of treating a passing timeout gate as complete planning evidence.

Analyze each populated typed mapping table after its insert; the six validators
share the affected join template. Analyze completed inventory lines before in-build
binding construction and keep the committed validation refresh. Preserve transaction
boundaries, predicates, null/provenance checks, constraints, schema, indexes, timeout
and dependencies. Two readiness regressions fail before correction; eleven combined
focused checks pass afterward. Repeat final fresh/retained acceptance and compare
all durable catalog row digests across no-op. Earlier discovery passes remain evidence,
not the final development gate.


## D-041 — Revision statistics before catalog consumption (2026-09-10 local)

Final fresh acceptance exposed a direct-figure containment coverage timeout after
successful import validation. Exact-backend capture shows active execution without
blockers, no prepared target query, and absent revision snapshot statistics. The
materialized applicable-inventory population is substantially underestimated at its
snapshot-filtered consumer. Automatic analysis later changes the plan and permits
the same query to finish. A bounded disposable copy preserving the applicable
inventory foreign keys reproduces the timeout; analyzing revisions alone changes
execution to 153 ms with unchanged coverage results. A copy omitting those foreign
keys is explicitly not accepted as the causal control.

Analyze catalog_inventory_revision after its last digest update, before default
selection and subsequent readers. Do not rely on maintenance timing, raise query
limits, alter containment semantics, or introduce an out-of-band acceptance repair.
A separate error-reporting correction stops a benchmark immediately after query
cancellation, retaining the safe case ID rather than issuing more statements in
its aborted transaction. Real PostgreSQL regressions cover both lifecycle readiness
and cancellation/rollback. Final full acceptance remains required.

## D-042 — Restore owned services independently of evidence publication (2026-09-11)

The final independent review reproduced required-report publication bypassing
service restoration in `catalog_smoke`. Brian authorized the narrow correction:
after verified ownership and initial-state capture, an outer `finally` attempts
normal service restoration independently of publication and exact-owned deletion.
Required publication remains strict, and unpublished database evidence is retained.
An initially running service remains running. Concurrent publication/restoration
failures preserve the publication exception and safely report failed restoration
with unknown final state; no success is inferred. Shared publication, ownership,
database retention and importer behavior are unchanged. Deterministic tests execute
the actual runner orchestration with simulated external resources. Focused evidence,
final review and development no-op preservation are recorded in
[ExecPlan 020](plans/020-catalog-foundation.md).

## 2026-09-11 — BrickLink offline proof and terms-aligned retention gate

Brian authorized Phase 3B offline preparation only. Supplied API Terms received
September 11 and USER-CONFIRMED registration qualify the prior open gate; credential,
registered-IP and live behavior remain unverified. Preserve accepted product goals,
but separate availability, freshness, display eligibility and retention. Treat guides
as item content conservatively; stale labels/local retimestamps cannot authorize
expired display. Six-hour display limits are not universal deletion requirements.
Long-lived raw/normalized history, derived valuations and mapping assertions require
documented rights/retention decisions before implementation. Private use is not an
exemption or blanket permission for future cross-marketplace features.

The initial proof uses in-memory responses and minimal durable engineering accounting,
12 price views plus five identity/color reads, four global retries and an absolute
24-attempt ceiling (21 with this smaller identity plan). No automatic budget reset,
real credential loading, live requests, Phase 3C persistence or formula changes are
authorized here. See [ExecPlan 030](plans/030-market-provider.md#13-phase-3b-offline-preparation--2026-09-11)
and [operator disclosures/configuration](BRICKLINK_PROBE.md).


## 2026-09-11 - Candidate discovery and evidence-bound live proof

Brian authorized correction of the circular review prerequisite and continuation under
one fixed ledger: up to 8 identity initials, 12 price initials, 4 global retries, 24 total.
Candidate identity eligibility is separate from exact canonical/provider price eligibility;
source binding, identity references, target dimensions and review facts are rechecked
before signing, reservation and dispatch. A boolean or HTTP success cannot confer review.
Element and intact-figure subset evidence reuse the accepted adapter. Reviews remain
probe-local; no catalog mapping or market persistence. The completed proof consumed 19
attempts and all 12 views were valid priced observations. Acceptance review is next;
retention/display-rights decisions still precede Phase 3C. Earlier preparation limits
above remain historical and do not supersede this authorized execution.


## Phase 3C — Bounded current evidence and owner maintenance (2026-09-12 UTC)

Brian authorized offline implementation of the reviewed Phase 3C plan. Supplied
BrickLink terms and immutable application policy defaults remain separate. Price
content is current evidence with short operational retention, not a permanent market
history warehouse. Exact historical forecast replay after purge remains a Phase 7
rights decision; existing saved-work product requirements are not removed.

The existing service role is reused with enumerated market operations and unchanged
catalog SELECT-only permissions. Mapping/policy administration and purge remain owner
operations. Scope locks serialize runtime admission/publication and mapping changes;
no mapping UPDATE grant is added merely to permit SELECT FOR SHARE. Every request
account shares one provider quota pool initially, so credential rotation cannot reset
accounting. Internal adapter retries are disabled in the single-attempt wrapper.

To enforce current-plus-preceding retention with owner-only deletion, admission waits
for bounded owner maintenance before a third observation can be fetched. This is an
explicit maintenance dependency and deferred state, not hidden content accumulation
or a worker DELETE grant. See [market operations](MARKET_OPERATIONS.md) and
[ExecPlan 030](plans/030-market-provider.md). No live use or acceptance is implied.

## Phase 4A — Offline calibration before live demand authorization (2026-09-12 UTC)

Brian authorized only the fixed representative corpus and offline calibration
harness. Calibration reuses accepted catalog expansion and market records, with an
explicit read-only cache transaction and pure hypothetical budget projection.
Physical uncertainty blocks combined contents arithmetic; whole-set evidence remains
separate. Raw quantity-weighted subtotals and input-availability diagnostics do not
implement final Phase 5 valuation/liquidity/Gem/Hunt policies.

The proposed 400-attempt Phase 4B ceiling remains provisional. Corpus source demand
must inform a separately chosen scope and ceiling. Permanent calibration reports
retain metadata and references without numerical market-derived totals/rankings;
purged observations may prevent exact replay. No retention rights are expanded.
See [ExecPlan 040](plans/040-calibration.md) and [calibration guide](CALIBRATION.md).


## Phase 4B - One provider attempt ledger before mapping (2026-09-12 UTC)

Identity discovery precedes verified price-cache identity. Authorized migration 0007
therefore discriminates the existing attempt ledger instead of fabricating a mapping
or adding a separate discovery quota system. Price shape and attribution stay strict;
discovery cannot reference observations. Immutable root groups and one-level children
preserve P4-01 category/retry/total limits alongside existing group/provider ceilings.
Active accounting survives retention until explicit terminal closure. Independently
validated provider controls survive stale-result rejection through monotonic cooldown
and suspension merging. Discovery content itself is not persisted.

This is an offline engineering decision under Brian's prerequisite authorization.
No live ledger/call, development migration, new dependency, valuation behavior or
retention right is implied. See [data model](DATA_MODEL.md), [operations](MARKET_OPERATIONS.md)
and [ExecPlan 040](plans/040-calibration.md).

## Physical representation eligibility before valuation (2026-09-12)

Accepted bulk import provenance establishes recorded data and ingestion, not
exhaustive physical membership, authoritative absence or disjoint ownership.
Use derived/injected, revision-and-digest-scoped evidence contracts and versioned
internal physical assessments; no database migration is required for this slice.
Missing proof stays UNKNOWN even when source counts reconcile. Synthetic proofs
are explicitly scoped to synthetic snapshots and cannot certify official data.

Only VERIFIED_COMPLETE or COMPLETE_FOR_REPRESENTATION admits the selected physical
representation. COMPLETE_SET needs one saleable set identity, independently of
exploded contents and actual seller condition. Split-sale and part-out modes require
their own exhaustive membership and allocation proofs. Expansion replaces parents;
unknown components do not block an independently proven intact representation.
No incomplete output or silent fallback may become a complete valuation denominator.

Phase 5 may later implement deterministic strategies while some real sets remain
UNKNOWN, after this prerequisite is independently accepted and Phase 5 separately
authorized. Each strategy gates dependent values on its exact assessment; unsupported
results are blocked/null, never estimated or zero-filled. Price, condition, recovery
and liquidity retain independent gates. See the
[bounded prerequisite](plans/040-calibration.md#physical-completeness-prerequisite--approved-implementation-2026-09-12).

## Phase 5A — Deterministic theoretical core (2026-09-12)

Brian authorizes the bounded implementation in [ExecPlan 050](plans/050-valuation.md).
Use the admitted physical representation and exact quantity-weighted observations
for independent whole-set, intact-figure part-out, full-component part-out and
figures-plus-remaining-build theoretical results. Physical uncertainty blocks all
dependent amounts/denominators; market incompleteness may produce a labeled partial
subtotal only for a valid population. Repeated ancestry occurrences remain distinct.

The immutable code policy versions statistic, extras and rounding, with default extras
exclusion, final-only ROUND_HALF_UP and no zero replacement for unavailable evidence.
Read-only exact-key lookup preserves current mapping, scope, freshness and display
eligibility. Results carry references and transient values; no schema or persistent
provider history is added. A component subtotal is not residual-build sale proceeds.
Comparison does not sum or rank mutually exclusive strategies. 5B/5C, usable M,
recovery/liquidity, deal economics, UI and saved workflows remain deferred. Independent
review and local checkpoint commit are the next action; this implementation is unstaged.

### Phase 5A independent acceptance (2026-09-12)

The bounded review fixes two reproduced defects: caller Decimal exponent/trap state
could corrupt arithmetic or fail final rounding, and a fresh read-only receipt could
outlive a tightened policy's deadlines. Arithmetic now uses an isolated explicit
context while reusing the shared exact-sum calculation. The internal cache receipt
carries its lookup policy for calculation-time reclassification and policy-ID
provenance, without altering stored observations or public contracts. The reviewed
checkpoint has 16 files, including two narrowly affected market modules; no migration
or dependency change is needed. Acceptance and cleanup evidence are in ExecPlan 050.
After the local checkpoint, Phase 5B requires separate authorization in a new task.

## Phase 5B — Policy-neutral liquidity and concentration (2026-09-12)

Brian separately authorizes the [bounded 5B contract](plans/050-valuation.md#phase-5b-bounded-contract--authorized-2026-09-12)
at accepted 5A `ce03709`. Preserve provider-native SOLD units S and sale-occurrence
count O, STOCK units C and inventory/listing count I. O is not unique orders/buyers;
I is not unique sellers. Only exact-compatible eligible evidence supports S/(S+C),
labeled SELL_THROUGH_PROXY. Confirmed-empty/missing evidence never becomes zero.

Exact usable months M remains unsupported by current evidence. Production analysis
cannot override M; standalone synthetic formula inputs prove future duration
capability only. Raw finite ratios retain exact numerators/denominators; terminating
Decimal quotients are exact, recurring quotients use versioned 50-significant-digit
ROUND_HALF_UP, independent of caller context. Duration formulas use original inputs
rather than a rounded velocity. Zero-demand duration has explicit infinite/undefined
reasons without nonfinite output values.

Concentration consolidates already-valued physical contributions only for analysis,
with stable canonical ties, while original occurrence/quantity accounting remains.
Partial valuation yields PRICED_SUBSET_CONCENTRATION, without unknown-value weighting.
Each strategy/view remains independent and physical failure suppresses contents
diagnostics. Activity/readiness uses the existing 5A eligible market-guide contract;
price-excluded guides remain explicitly excluded rather than bypassing that gate.

Market evidence describes activity, supply and concentration; it cannot determine
Brian's recovered value fraction or horizon. Liquid POV, Fast Cash, Dead-Stock dollars,
recovery/Gem/burden/Hunt policy and deal economics require separate later decisions.
No migration, dependency, public route, provider call/credential, development DB or
5C work. Independent review and a local checkpoint remain the next action.

### Phase 5B independent acceptance (2026-09-12)

Review reproduced Python's integer-string digit limit rejecting a valid large
Decimal ratio. Precision sizing now uses exact Decimal integer conversion, with
regressions beyond 4300 digits under hostile caller context. Numeric policy and
rounding remain unchanged. ExecPlan 050 records acceptance and the ten-file local
checkpoint; a bounded Phase 5C plan requires separate authorization in a new task.


## Phase 7C Slice 3 settings and profile assumptions - 2026-09-21

The authorized slice in [ExecPlan 081](plans/081-settings-selling-profiles.md) uses
owner-scoped typed settings and user-authored selling profiles. Profiles replace
shipping, selling fees/costs, additional acquisition costs, tax and buyer premium;
settings own new-draft sale mode and enabled Purchase Limits targets. No new formula,
currency or actual purchase field is introduced. Name uniqueness is owner-scoped
case-insensitive exact matching after trimming outer whitespace.

Absent settings read as revision zero without creating a row. First explicit PUT
requires revision zero; subsequent updates and profile updates/deletes require the
current revision. A default profile must be explicitly unset/replaced before deletion.
Settings resolve that profile in one database read snapshot. A new ordinary draft
copies resolved values once. An existing draft retains independent values across
Settings navigation; failed initialization and interrupted reauthentication require
explicit reload. Apply fetches the selected profile and replaces only its defined
fields, clearing preview/capture without calculation or Save. Historical replay and
revision initialization never consult these mutable resources. No profile pointer or
schema extension enters frozen saved snapshots. Technical and visual review were pending before the following acceptance.

### Source-checkpoint acceptance - 2026-09-21

Brian accepts Phase 7C Slice 3's reported implementation, technical evidence and
four-image visual review for its source checkpoint. Settings and Selling Profiles
are ACCEPTED / CLOSED FOR THIS SOURCE CHECKPOINT; Phase 7C remains IN PROGRESS.
The local commit is `Complete Phase 7C Slice 3 settings and selling profiles`,
parent `f52f827a9f945a0fd1ae40b4414e1ac27558c208`. The recorded 45-file inventory
includes the `watchlist.py` server-owned INSERT-column correction; migration 0013
and accepted Slice 2 semantics are unchanged. Migration 0014 is the sole head.
Notes / Source URLs is the next planned slice and is not started by this acceptance.
No development migration, deployment or push occurred. ExecPlan 081 preserves
evidence and qualifications.

## Phase 7C Slice 4 Notes and Source URLs — authorization-time status, 2026-09-21

Brian authorizes only the bounded Watchlist-note and saved-forecast-lineage
note/source-URL implementation in [ExecPlan 082](plans/082-notes-source-urls.md).
User-authored annotations use owner-scoped revision/CAS and remain outside frozen
forecast payloads, digests, replay, saved timestamps, provider evidence and financial
calculations. Source URLs are inert absolute HTTP(S) references; they are neither
fetched nor treated as verified evidence. Slice 4 is IN PROGRESS; 7B and 7C Slices
1–3 remain CLOSED, Phase 7C remains IN PROGRESS, and Phase 8 remains unstarted.
Use guarded disposable TEST resources only, preserve the protected dirty files, and
stop after self-review for technical and visual review. No development database/site/
account, provider or remote URL activity, staging, commit, push, deployment or later
phase work is authorized.


## Phase 14A bounded recognition baseline — 2026-10-02

Brian authorizes source implementation under [Plan 104](plans/104-recognition-quality-pilot.md)
after Phase 13 closeout. Use one local Python CLI and one pinned model, strict
uncertain identity proposals, exact shared catalog references and a protected
attempt ledger. No migration or UI is required. Provider/photo/account/dollar
approval remains pending; a ten-attempt ceiling does not authorize spending.
No predictions become catalog mappings, training labels or valuation evidence.
The [provider decision](PHASE_14A_PROVIDER_DECISION.md) records the recommendation
and current gates. Wider direct/retrieval/retrieval-plus-verification comparison
remains Phase 14 work; embeddings require measured need and approval.


## Phase 14A combined approval and cost controls — 2026-10-02 continuation

Brian replaces the earlier model proposal with exact `gpt-6-luna` and approves a
persistent $0.25/ten-attempt pilot, conditional on exact sample and privacy checks.
This supersedes the earlier pending-spending decision, without authorizing fallback,
production images, training, deployment, another phase or a main commit/push.
Use the existing ledger and adapter, stable documented prefix caching, ordered
hash/schema-verified exact-result reuse, and explicit cache/reasoning cost accounting.
No parallel agents, cache-warming calls or repeated accuracy measurements.

Read-only account inspection found API sharing enabled for all projects. No setting
was changed. Official model/pricing documentation supports the requested features,
but the image billing table/calculator omits GPT-6 Luna. Live admission fails closed
until a model-specific input bound is verified. The old reservation/formula is not
reused. See [current provider decision](PHASE_14A_PROVIDER_DECISION.md). Live totals
remain zero; the combined local checklist covers account settings, key and photos.


## Phase 14A selected mixed-lot capacity correction

The selected G06 example contains eight user-confirmed exact identities plus three
partial/combined-parts figures. Increase the existing bounded object and expected-label
limits from six to twelve, versioning the output schema as recognition-14a-v2. Preserve
the 2,048 output-token cap, persistent spending limits and incomplete-response stop.
All tentative and partial identities remain outside exact-identity scoring. Seven
groups/13 images are prepared locally with unchanged originals; final sample approval
and remaining provider/catalog gates precede any live dispatch.


## Phase 14A amended live approval and partial result — 2026-10-02

Brian explicitly superseded the USD 0.25 lifetime cap with USD 10.00, retaining exact
`gpt-6-luna` and ten total inference attempts. A model-wide maximum-input reservation
replaces the counting-endpoint prerequisite. Exact kind/namespace/identifier raw
recognition agreement is scored independently of catalog resolution. The fourteen
confirmed BrickLink figure IDs remain valid raw labels and unresolved canonically;
no guessed mapping, valuation promotion or automatic confirmation is authorized.
The exact seven groups/13 photos/texts and original denominators remain frozen.

The approved run sent six requests/eleven images. Five groups completed; G06 returned
incomplete after using its entire 2,048 output tokens on reasoning, stopping before
G07. No retry or fallback was sent. Estimated token-derived cost USD 0.0036058;
invoice cost is unavailable. The failure remains counted/reserved. Review the
[existing report](PHASE_14A_PILOT.md); a manual continuation needs explicit allowance
and retry approval. Development, catalog/import state, protected files and the main
index were preserved. Only sanitized review publication is authorized; main stays
uncommitted/unpushed. This outcome does not close wider Phase 14 or start Phase 15/16.


## Phase 14A r2 acceptance and two-call amendment — 2026-10-02

Brian accepted published r2 at 108f7f6d65a38ebead7701d3c0f7f2d62ed3b5ab as honest
partial pilot evidence, without closing 14A or establishing recognition quality.
The explicit amendment authorizes G07 once then one fresh G06 retry, with unchanged
Luna/Medium, prompt/schema, inputs and scoring. Only output allowance/deadline become
16,384 tokens/180 seconds. Original history/failed G06 and reservations are retained;
new files/protocol are versioned and retry 8 links to predecessor 6. No other call
or future tuning/model comparison is authorized. The existing USD 10.00 cap remains.

Both requests completed. Cumulative sample coverage is seven groups, eight lifetime
requests, raw 3/17: three sets matched, fourteen figures did not. G07 correctly returned
custom_build. This is weak figure-recognition evidence despite completed processing.
Catalog figure coverage remains a distinct limitation. Lifetime token-derived estimate
USD 0.0058142; actual billing unavailable; USD 1.877792 retained reservations. The two
unused lifetime attempts are not authorized. Original r2 evaluation/result hashes
match. Three affected fixture checks and source static checks passed; no broad work.
Publish only sanitized r3 review, preserving r1/r2; main stays uncommitted/unpushed,
index empty, protected files unchanged. [Existing report](PHASE_14A_PILOT.md) contains
separate original, amended and cumulative views. Stop for recognition-quality review.


## Phase 14A one Sol comparison authorization — 2026-10-03


**READY FOR PHASE 14A MODEL-COMPARISON REVIEW.** Brian authorized only G06,
`gpt-6.1-sol`, lifetime attempt 9, compared with completed Luna attempt 8 under
the same approved request/sample/scoring. Sol completed; both score 0/8 top-1/top-3.
Luna's whole-sample 3/17 remains unchanged. Catalog figure mappings remain unresolved.
Nine lifetime calls, token-estimated USD 0.0489202, retained USD 7.373552,
unreserved USD 2.626448 under the unchanged USD 10 cap. Attempt 10 is unauthorized.
Three affected fixtures and targeted lint/type checks passed; all old evidence and
protected files remain intact. Development stays stopped, main unpushed/index empty.
Stop for review; no further calls, tuning, mapping writes, deployment or later phase.
Earlier dated checkpoints below preserve their prior scope and results.
