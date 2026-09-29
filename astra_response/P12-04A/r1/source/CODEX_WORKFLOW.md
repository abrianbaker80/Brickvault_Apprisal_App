# Codex Workflow for BrickVault Appraisal App

## P12-04A production foundation for review — 2026-09-29

**P12-01/P12-02/P12-03 are CLOSED; Phase 12 and P12-04 are IN PROGRESS;
P12-04A is IMPLEMENTED / READY FOR REVIEW; P12-05 is NOT STARTED.** VM 115 is
running with `onboot=0`. Its dedicated ext4 PostgreSQL data filesystem is
mounted on `scsi1`; PostgreSQL 18.6 uses that filesystem and listens only on
`127.0.0.1:5432`. System-installed Python 3.13.15 and uv 0.12.10 support the
staged, installed-wheel and web release. The API systemd unit is prepared but
disabled, with no API listener. [ExecPlan 094](docs/plans/094-production-foundation.md)
records the sources, implementation and focused validation. No BrickVault
production database, application secrets, backup destination, DNS, certificate
or TLS deployment exists. The P12-03 closeout below remains its dated record;
P12-04A review has not been accepted and P12-04 is not closed.

## P12-03 accepted closeout — 2026-09-29

**P12-03 ACCEPTED / CLOSED** after ChatGPT review of the
[r2 unattended-install and base-OS evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/a9023bcc6a2c933938465b18f79787041499f9f3/astra_response/P12-03/r2/REVIEW.md).
P12-01/P12-02 remain CLOSED; Phase 12 remains IN PROGRESS; **P12-04 is NEXT /
NOT STARTED**. VM 115 remains stopped with `onboot=0` and `scsi0` boot order;
its 128-GiB data disk is still unused. The r2 result and r1 partial checkpoint
below are preserved as dated evidence. No BrickVault application, production
PostgreSQL, Python 3.13 or uv runtime, Caddy, production DNS/certificate,
backup, database/secrets or provider credentials have been deployed to VM 115.
The P12-04/P12-05 gates remain in force. No infrastructure qualification was
rerun for this documentation closeout.

## P12-03 r2 review-ready snapshot — 2026-09-29

**Historical pre-acceptance status: P12-03 IMPLEMENTED / READY FOR REVIEW;
not CLOSED.** Brian superseded the
manual-installer boundary. VM 115 now boots the checksum-verified Ubuntu
24.04.2 ISO's unattended installation from a task-owned NoCloud seed, with
the install confined to its 32-GiB OS disk. Official updates advanced the
installed system to Ubuntu 24.04.5 LTS. `brickvault-admin` has proven
laptop-key SSH and sudo; password and root SSH are disabled, its temporary
password is locked, and QEMU guest-agent is working. Guest and stopped-host
checks confirm the 128-GiB data disk has no partitions, filesystem, LVM
membership, mount or fstab entry. Temporary seed media is removed; the
shared Ubuntu ISO remains intact. The VM is gracefully stopped with
`onboot=0`, `scsi0` boot order and no installer media attached.
[ExecPlan 093](docs/plans/093-base-vm-provisioning.md) records exact
validation and deviations. The r1 blocked section below is historical.
P12-01/P12-02 remain CLOSED; Phase 12 remains IN PROGRESS. ChatGPT review
is still required before P12-03 closure. No P12-04 work is authorized or done.

## P12-03 partial provisioning for review — 2026-09-29

**P12-03 BLOCKED — MANUAL INSTALLER STEP REQUIRED.** Brian authorized the
base VM slice. Fresh repository, host/capacity/bridge/VMID and authoritative
Ubuntu ISO checksum gates passed. VM 115 and its fresh EFI, 32-GiB OS and
128-GiB data volumes, one untagged vmbr1 NIC and verified ISO are provisioned
for review. The VM remains stopped with onboot disabled; the data volume has
no partitions, filesystem/LVM signature or mount. Browser console access
failed on the management certificate, so Ubuntu and administrator SSH are
not installed/established. [ExecPlan 093](docs/plans/093-base-vm-provisioning.md) records exact resources,
checks, the manual installer handoff and rollback boundary. Legacy VM 107 and
all existing guests remain unchanged. P12-01/P12-02 stay CLOSED; Phase 12 is
IN PROGRESS; P12-03 is not CLOSED and no P12-04 work occurred. Earlier dated
P12-03 NEXT / NOT STARTED entries below are historical.

## Phase 12 P12-02 accepted closeout — 2026-09-29

**P12-02 is ACCEPTED / CLOSED after ChatGPT review of the published
[`r1` infrastructure package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/639b10dc483da27d85cd983b204d281e218b5b6c/astra_response/P12-02/r1/REVIEW.md).
Phase 12 remains IN PROGRESS; P12-03 is NEXT / NOT STARTED.** The review
accepted the point-in-time node facts and conditional dedicated VM design in
[ExecPlan 092](docs/plans/092-exact-infrastructure-pre-mutation-review.md).
P12-03, if separately authorized, is limited to creating that new VM and
installing base Ubuntu. It requires fresh VMID/capacity/bridge checks and an
authoritative Ubuntu ISO SHA-256 match before mutation; temporary DHCP and
key-only admin SSH are permitted. The new data disk stays unformatted. It does
not install BrickVault or any database, runtime, proxy, backup or certificate
software, and it does not change router, firewall or DNS policy. Backup,
private DNS/certificate, package-source, production-admin and live acceptance
gates remain P12-04/P12-05 work. Acceptance of P12-02 authorizes no mutation.
No infrastructure change occurred in P12-02.

## Phase 12 P12-02 review snapshot — 2026-09-29

**Historical pre-acceptance status: P12-01 was ACCEPTED / CLOSED; Phase 12 was
IN PROGRESS; P12-02 was AUTHORIZED / IN REVIEW; P12-03–05 were not
authorized.** The configured-key Proxmox SSH check succeeded; the bounded
read-only node pass
identified actual capacity, VM/storage/network inventory and the absence of
configured Proxmox backup jobs/PBS. [ExecPlan 092](docs/plans/092-exact-infrastructure-pre-mutation-review.md)
records the conditional VM placement, new-empty-database policy, full future
mutation order and blockers. No infrastructure or production mutation occurred.
Brian approved `appraisal.abrianbaker.com` for planning. Private DNS and
certificate setup, backup access/restore, stable address/firewall sources and
pinned runtime packages still gate mutation readiness. Brian proposed a new
Google Drive `Brickvault_Apprisal_App_Backup` folder for encrypted off-host
logical backups and selected a second encrypted database copy on the existing
Proxmox server; neither destination has been created. The sanitized P12-02
package was pending ChatGPT review; P12-03 had not begun. The dated P12-01
closeout below is historical.

## Phase 12 P12-01 — production runtime and deployment preflight — 2026-09-28

**Phase 10 and Phase 11 are CLOSED. Phase 12 is IN PROGRESS; P12-01 is
ACCEPTED / CLOSED. P12-02 is NEXT / NOT STARTED.** ChatGPT accepted the
published r1 source, focused local proof and [ExecPlan 091](docs/plans/091-production-runtime-and-deployment.md).
The Proxmox alias still resolves to a placeholder, so no real node facts were
resolved. No VM, storage, network, DNS, certificate, backup, service or
production database mutation occurred. The exact hostname, VM placement,
bridge/VLAN, storage pool, off-host backup, data/bootstrap policy and real
secrets remain unresolved. Real Caddy/TLS/private-DNS behavior, normal-certificate
browser/PWA/Android acceptance and off-host restore remain later gates. Android
has source/config/build evidence only, without an APK or physical-device
acceptance; Phase 9 localhost TEST transport/certificate is not production
evidence. PostgreSQL must never be public. **P12-02 and all infrastructure or
production mutations require separate review and explicit authorization.**

## Phase 11 P11-01 — home infrastructure discovery — 2026-09-28

**P11-01 is ACCEPTED / CLOSED; Phase 11 is CLOSED. At this closeout, Phase 12
was NEXT / NOT STARTED; the P12-01 section above now governs.** ChatGPT
accepted the published r1 discovery evidence. Brian
authorized one read-only pass over the current workstation and existing home
VM/Proxmox access. [ExecPlan 090](docs/plans/090-home-infrastructure-discovery.md)
records the observed guest, access gap to the Proxmox node, source-level
production runtime blockers, and a conditional Phase 12 design. No
infrastructure, application, database, DNS, certificate, or service was
changed. Phase 12 requires separate explicit authorization before any
infrastructure or production change.

## Targeted development and GitHub review packages — 2026-09-27

For each explicitly authorized bounded task, use a small implementation slice,
targeted validation, and one review boundary. Reuse accepted evidence; expand
testing only for a concrete change or failure. Preserve unrelated work and
protected files. A completed, partial, or blocked task gets a self-contained
`astra_response/<task-id>/r<N>/` package on `astra-response`, with an unused
revision each time and cumulative changes against the same implementation
baseline for corrections. Include `REVIEW.md`, a complete task patch including
new files, concise `validation.txt`, final implementation/test files under
`source/`, and only necessary `context/` or baseline files. Distinguish newly
run checks from reused evidence and state limitations and requested review.

Publish only review-package files from an isolated checkout and separate index;
leave the implementation branch, HEAD, index, and unrelated work intact. Append
to remote `astra-response` history, or create a report-only orphan branch if it
does not exist. Inspect the exact staged package for private data, never force
push, push once, verify the remote commit, and read back `REVIEW.md`. This
authorization does not commit or push application code or authorize deployment.

## Phase 10 P10-03 — local packaged-release readiness — 2026-09-28

**P10-01, P10-02 and P10-03 are ACCEPTED / CLOSED. Phase 10 is CLOSED for local
release/security readiness; Phase 11 is NEXT / NOT STARTED.** One normal
offline-locked API/web build and one HTTP smoke of the installed wheel and built
frontend passed with an owned disposable TEST database and loopback API. The
smoke passed 18 HTTP checks for public assets, auth/Settings/CSRF/logout,
current readiness, private cache policy, safe errors, static-root exclusions
and redacted structured logs. Five focused tooling tests passed; earlier
authentication, migration, recovery and Android evidence was reused. Cleanup
restored the prior TEST service state.
[ExecPlan 089](docs/plans/089-local-packaged-release-readiness.md)
reconciles the existing Phase 10 evidence. No new physical Android qualification,
comprehensive security/dependency audit, production disaster-recovery proof,
home-server access or deployment qualification is claimed. Deferred Economics
Extensions and remaining R-36 capabilities stay outstanding and unassigned.

## Phase 10 P10-01 — frontend release-artifact verification — 2026-09-27

**Phase 10 is IN PROGRESS; P10-01 is ACCEPTED / CLOSED.** Frontend build
verification now rejects asset names outside the flat JS/CSS allowlist, linked
build or assets directories, and non-regular or hard-linked output files before
reading their bytes. Existing private-value and sentinel checks and normal
web/PWA acceptance remain. Six focused Windows Node tests, targeted Prettier,
and targeted ESLint passed. This source-only fix does not establish complete
runtime-loader parity or qualify the Phase 10 release.

## Phase 10 P10-02 — local TEST database recovery proof — 2026-09-28

**Phase 10 remains IN PROGRESS; P10-02 is ACCEPTED / CLOSED.** The bounded
`test:recovery` command uses two exact owned disposable TEST databases and a real
PostgreSQL custom dump/restore. The focused fixture checks restored authentication,
Watchlist values and revision, saved-forecast immutable content and replay, runtime
readiness/grants, and unchanged source records. Roles and configuration remain separate
from the dump; this local proof does not qualify production disaster recovery.

## Phase 9 closed — 2026-09-26

**Phase 9 is CLOSED.** Brian accepted the final physical qualification recorded
in [ExecPlan 088](docs/plans/088-android-https-auth-source.md), including all
five market-evidence expiry profiles and the one-shot uncertain Watchlist
mutation. Run `47b0c2d3f3c94daa92188b5eab34d905` used the unchanged accepted
APK. The client honored server deadlines, never replayed the uncertain write,
and reconciled the single revision-1 row through authoritative readback. No
live provider was contacted, and all active qualification resources were
cleaned up. **Phase 10 is NEXT / NOT STARTED** and remains separately
authorizable.

## Historical Phase 9 physical Android qualification — 2026-09-23

**The bounded physical USB HTTPS/authentication pass PASSED; Phase 9 remains OPEN.**
Brian accepted the separately authorized one-phone result recorded in
[ExecPlan 088](docs/plans/088-android-https-auth-source.md). The unchanged
debug APK reached the direct loopback TEST TLS API through `adb reverse`;
physical login, authenticated reads, CSRF settings save, passive resume,
read-only offline memory, explicit reconnect verification, fresh-start privacy
and logout passed. No source defect or live-provider contact occurred. The
reverse rule, app-scoped phone trust, temporary Windows PEM/key, TEST database
and owned listeners/processes were cleaned up. No source, protected dirty file,
index or APK bytes changed; no qualification suite or build was rerun.

The existing [Phase 9 roadmap gate](docs/ROADMAP.md#phase-9--pwa-offline-behavior-and-android-core-app)
still requires physical Android core workflows and auth/cache expiry/sync-conflict
checks. The accepted bounded pass did not test set search/detail, deal analysis,
saved-work flows, or on-device expiry/conflicts. This is the next Phase 9 milestone; Phase 10
local release hardening follows Phase 9 closure. No phone, TEST service,
provider, deployment, push or follow-on implementation is authorized by this
documentation checkpoint. Earlier physical-not-started entries are historical.

## Phase 9 Slice 3B source qualification - 2026-09-23

Brian authorized the implementation and source checks in [ExecPlan 088](docs/plans/088-android-https-auth-source.md).
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
[ExecPlan 087](docs/plans/087-android-build-readiness.md) and authorized exactly six documentation files for one
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
[ExecPlan 087](docs/plans/087-android-build-readiness.md) records the accepted conservative toolchain strategy,
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
visual evidence in [ExecPlan 086](docs/plans/086-private-memory-reconnect.md). Slice 1 and Phases 7B/7C/8 remain CLOSED.
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

**Slice 2 IN PROGRESS.** [ExecPlan 086](docs/plans/086-private-memory-reconnect.md) implements dated
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

Implementation and self-review are complete; **ready for technical/visual review**,
not accepted or closed. ExecPlan 086 records the delivered view matrix, final
validation, initial corrections, storage inspection and owned TEST cleanup.
The original screenshot ZIP and exact incremental inventory are outside tracked
source under `.local/phase9-slice2`. No staging or commit has occurred.

## Phase 9 Slice 1 source-checkpoint closeout — 2026-09-23

**Slice 1 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 9 remains
IN PROGRESS.** Brian accepted implementation, technical evidence and the visual
ZIP in [ExecPlan 085](docs/plans/085-public-pwa-capacitor-feasibility.md).
Authorize the exact reviewed 87-file local checkpoint, with only normal closeout
amendments, from `10904d25732633293dfd7ab3fdf55e1674f10938`:
`Complete Phase 9 Slice 1 installable PWA and Capacitor feasibility`.
Protected edits and all visual/runtime/acceptance artifacts are excluded.
Migration head remains `0016_hunt_cached_runs`; no migration is added.

Durable caching remains public-shell-only; private/API/auth responses remain
no-store and never enter the service-worker cache. Offline restart restores no
private history. Updates remain explicit and notification preserves Deal drafts.
Capacitor source generation/sync is accepted, not native/device/deployment
qualification. Current network and authentication restrictions remain unchanged.

Brian confirmed he accidentally closed the development listeners himself. The
incident is RESOLVED; no Slice 1 tooling defect is implicated and no restart or
attribution investigation is required. Existing test selections remain separate;
no acceptance suite is rerun for closeout.

Slice 2 is next, NOT STARTED / NOT AUTHORIZED; Slice 3 remains later and unstarted.
Private offline policy remains document-memory-only, no offline writes, generic
sync or provider refresh. Phase 7B/7C/bounded 8 remain closed; R-07/R-36 partial,
Phase 16 separate and Deferred Economics outstanding/unassigned. No push,
deployment or operational work. Earlier Slice 1 review-pending entries are history.

## Phase 9 Slice 1 authorized — 2026-09-23

**IN PROGRESS — implementation and self-review only.** Brian accepted the Phase 9
plan and authorized [ExecPlan 085](docs/plans/085-public-pwa-capacitor-feasibility.md):
installable online PWA, public-shell-only durable caching, explicit updates and
bounded local Capacitor feasibility. This supersedes older Phase 9 prohibitions
only for Slice 1. No staging/commit, deployment, development DB/account/provider
work, LAN exposure or physical-device testing.

No private durable browser store is approved. Slice 2's future memory views are
read-only through the last confirmed session deadline, with no offline extension,
mutation or immediate remote revocation claim; logout/principal change/expiry
clear them. Slice 1 does not implement private caching. Slice 2/3 remain unstarted.
Phase 7B/7C and bounded Phase 8 stay closed; R-07/R-36 remain partial, Phase 16
outcomes separate and Deferred Economics outstanding/unassigned.
Stop for technical/visual review; do not close Phase 9.

Implementation and self-review are now ready for that review. ExecPlan 085 records
34 backend unit, 13 frontend and 2 tooling cases as separate passing selections,
actual Chromium worker/offline/update evidence, the verified visual ZIP, native
toolchain limits and the unexplained disappearance of both development listeners.
No full development-runtime preservation or Android acceptance is claimed.

## Phase 8 source-checkpoint closeout — 2026-09-23

**Slice 2 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT. Phase 8 is ACCEPTED /
CLOSED FOR ITS BOUNDED SOURCE MILESTONE.** Brian accepted the implementation,
technical evidence and all supplied visual states in
[ExecPlan 084](docs/plans/084-hunt-frozen-evidence-context.md#source-checkpoint-acceptance--2026-09-23).
The milestone delivers cached whole-set Hunt runs, transparent financial sorting,
immutable history, explicit qualification/freshness and frozen bounded component
context. Full R-36 remains PARTIAL; outstanding requirements are not cancelled,
satisfied or assigned to another phase. Slice 1 and Phase 7B/7C remain CLOSED.

Authorize one local 20-file checkpoint commit from
`9777d2ffd86f99f7ae6a1b47cca9a976aea1f418`:
`Complete Phase 8 Slice 2 frozen Hunt evidence context`.
Protected files and all visual/TEST/runtime artifacts are excluded. Migration head
remains `0016_hunt_cached_runs`; optional `hunt-component-context-v1` changes no
financial/sort versions and requires no migration or legacy rewrite. Prior evidence
is retained as distinct runs; this closeout requests no application tests or services.

Phase 9 cache/sync is next, **NOT STARTED / NOT AUTHORIZED**, including planning.
Phase 16 outcomes remains separate. No deployment, push or later-phase work follows
this commit. Earlier in-progress/review-only/commit-prohibited entries below describe
the prior authorization boundary and are superseded by this acceptance only.

## Phase 8 Slice 2 authorized — Frozen Evidence Context, 2026-09-22

Brian accepted the R-36 review and bounded Phase 8 source milestone: cached
whole-set screening, transparent financial sorting, immutable historical runs,
explicit qualification and bounded existing component-evidence context.
[ExecPlan 084](docs/plans/084-hunt-frozen-evidence-context.md) governs Slice 2,
IN PROGRESS. Slice 1 and 7B/7C remain CLOSED; Phase 8 remains IN PROGRESS.
Full R-36 remains PARTIAL. Composite ranking is not a completion prerequisite;
unsupported/calibration-dependent concepts and Deferred Economics remain
outstanding and unsatisfied without a new delivery phase. This supersedes the
review-pending next action below, not its historical acceptance evidence.

Only frozen context, generated contracts, responsive disclosure, additive governing
reconciliation and guarded disposable TEST acceptance are authorized. No changed
financial/sort/provider behavior, development access, real account work, staging,
commit/push/deployment, Phase 8 closure or next slice.

Slice 2 implementation and self-review are now ready for technical/visual review.
The stable affected selection passed 17 guarded PostgreSQL/API/browser cases,
85 backend unit cases and 10 frontend cases; generated contracts, full types,
affected lint/format and the packaged build passed. Historical Markdown formatting
deviations remain qualified. [ExecPlan 084](docs/plans/084-hunt-frozen-evidence-context.md)
records the exact inventory, corrections, final visual run and preservation evidence.
No technical or visual acceptance, commit or Phase 8 closure is claimed.

## Phase 8 Slice 1 accepted / source checkpoint — 2026-09-22

**Phase 8 Slice 1 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT. Phase 8 remains
IN PROGRESS; Phase 7B and Phase 7C remain CLOSED.** Brian accepted the implementation,
technical evidence, corrected Watchlist browser coverage, spacing correction and
four-image visual review in [ExecPlan 083](docs/plans/083-hunt-cached-whole-set-run.md).
The distinct selections remain separate: final correction selection 9 passed;
final guarded browser rerun 1 passed. Seven unrelated baseline Ruff findings stay
qualified and excluded. Screenshots establish rendered states; authorization,
persistence and provider isolation have separate technical evidence.

The authorized local commit is `Complete Phase 8 Slice 1 cached whole-set Hunt runs`
from parent `7d3e5902a71e54b1e25d4249037c74865b20b34e` on `main`. Its explicit allowlist
contains reviewed Hunt/API/UI/contracts/tests, migration 0016 and packaging,
Watchlist/spacing corrections and required closeout documents. Protected files and
visual/runtime artifacts are excluded. Sole source migration head is
`0016_hunt_cached_runs`, parent `0015_notes_source_urls`.

R-08/R-36 remains partial. Next is a focused review/planning decision on existing
evidence, calibration/policy, unavailable dependencies and overlap with explicitly
Deferred Economics Extensions. Composite/calibrated ranking, Gem/rarity/competition/
burden and unsupported components remain unresolved or deferred under governing
scope. A composite score is not presumed required; no weights are invented.
Extensions stay outstanding, deferred, unsatisfied and without a delivery phase.
Phase 9 cache/sync and Phase 16 outcomes remain separate. No new implementation,
acceptance rerun, services, development migration, account/provider work, deployment,
push or later slice follows closeout. Earlier pending/unstarted statements below
record historical authorization-time status.

## Phase 8 Slice 1 implementation authorized — 2026-09-22

Brian authorized one complete vertical slice, Cached Whole-Set Hunt Run, under
[ExecPlan 083](docs/plans/083-hunt-cached-whole-set-run.md). Slice 1 is IN PROGRESS;
Phase 7B and Phase 7C remain CLOSED. The preceding Phase 7C closeout's statement
that Phase 8 was unstarted records its prior checkpoint and is superseded by this
authorization. Implement and self-review this slice, then stop for technical and
visual review. Use guarded disposable TEST resources only and preserve the three
protected dirty files. No live provider/marketplace, development/production
database/site/account, network exposure, stage, commit, push, deployment or later
slice/phase work is authorized.

## Phase 7C source checkpoint accepted / closed — 2026-09-22

**Phase 7C Slices 1–4 are ACCEPTED / CLOSED FOR THEIR SOURCE CHECKPOINTS, and
Phase 7C is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT.** ExecPlan 082 records
Slice 4's implementation, technical evidence, Brian's five-image visual acceptance,
and the qualified full-web result. The original 149 passed / 6 failed run traced to
stale authentication-test `/api/settings` mocks exposed by the accepted Slice 3
revision-zero settings contract; the baseline reproduced the failures and the
focused four-file selection passed 44/44 after the test-only fixture correction.
This does not assert that the entire web suite has since been rerun.

The authorized local closeout commit is `Complete Phase 7C Slice 4 notes and source
URLs`, from parent `8b3ee4bff10f772760923d4c18eac7402e044137`. The explicit source
allowlist excludes protected files, screenshots, archives and temporary evidence.
No development migration, deployment, account/provider/device operation or push
occurred. Phase 8 Hunt is next but remains unstarted and unauthorized; Deferred
Economics Extensions remain outstanding and are not a Phase 7C gap.

## Phase 7C Slice 4 implementation authorized — 2026-09-21

Historical authorization-time status, superseded by the source-checkpoint acceptance
above:

Brian authorized one bounded complete vertical slice, Notes and Source URLs, under
[ExecPlan 082](docs/plans/082-notes-source-urls.md). Slice 4 is IN PROGRESS. Phase
7B and Slices 1–3 remain CLOSED; Phase 7C remains IN PROGRESS; Phase 8 remains
unstarted. Implement and self-review, then stop for technical and visual review.
Use only guarded disposable TEST resources. Preserve the three protected dirty files.
No development DB/site/account/provider/URL operation, network exposure, stage,
commit, push or deployment. Do not begin Phase 8 or any later slice.

## Phase 7C Slice 3 accepted source checkpoint - 2026-09-21

**Phase 7C Slice 3 Settings and Selling Profiles is ACCEPTED / CLOSED FOR ITS SOURCE
CHECKPOINT.** [ExecPlan 081](docs/plans/081-settings-selling-profiles.md) records
the 45-file commit inventory, migration 0014, the narrowly scoped Watchlist INSERT
compatibility correction, implementation evidence, accepted visuals and TEST cleanup.
The local commit is `Complete Phase 7C Slice 3 settings and selling profiles` from
`f52f827a9f945a0fd1ae40b4414e1ac27558c208`.

Phase 7C remains IN PROGRESS. Phase 7B and 7C Slices 1/2 remain CLOSED. Notes / Source
URLs is the next planned slice; it has not started. No development migration,
deployment or push occurred.


## Phase 7C Slice 2 Watchlist and Targets accepted / source checkpoint — 2026-09-21

On 2026-09-21 Brian authorized implementation of only the authenticated Watchlist
and persistent purchase-target slice recorded in [ExecPlan 080](docs/plans/080-watchlist-targets.md).
The implementation, guarded disposable TEST evidence and visual review were completed
in the authorized original checkout on `main` from `2ba5165efa07b694f0733b7884d17f3d34ea03c3`,
with the protected dirty files preserved byte-for-byte.

**Phase 7C Slice 2 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT.** The reviewed
additive 0013 migration, owner-scoped API/service, generated contracts, shared-shell
Watchlist route, Set Detail Add action, responsive editing/recovery states and browser
flow are recorded in ExecPlan 080. The focused guarded TEST selection passed 74/74;
the built UI/API/PostgreSQL flow passed with duplicate/CAS behavior covered by the
focused database tests. Contract, affected format/lint/type checks and the production
build passed. The three inspected PNGs came from the guarded disposable TEST stack,
and `C:\Users\abria\Downloads\BrickVault-7C-Watchlist-Targets-Visual-Review.zip`
passed CRC verification (SHA-256
`225d8ccf7a1960076579fff9da59a1cc75c68f66b5403d236edc10dcfece306d`). These
selections overlap; no unaffected full application/database/browser suite is claimed.

The authorized local commit is `Complete Phase 7C Slice 2 watchlist and targets`
from parent `2ba5165efa07b694f0733b7884d17f3d34ea03c3`. Only the reviewed Slice 2
paths and necessary plan/workflow/traceability closeout hunks are included; protected
modifications, screenshots/archives, TEST ledgers and unrelated work remain outside
the checkpoint. Phase 7C stays **IN PROGRESS** and Phase 7B stays **CLOSED**.
Settings/Profiles, Notes/URLs, Phase 8 and later 7C slices remain unstarted. No
development migration, database data mutation, account/provider activity, deployment
or push follows. A development profile container was briefly stopped inadvertently
during earlier work and restored healthy; that event is not feature evidence.

## Phase 7C Slice 1 Saved Deal Index accepted / source checkpoint — 2026-09-21

On 2026-09-21 Brian authorized implementation of only the passive authenticated
saved forecast lineage index, responsive `/deals` page, generated contracts, focused
disposable TEST validation and visual review recorded in [ExecPlan 079](docs/plans/079-saved-deal-index.md).
The implementation was completed and submitted for source and visual review; the
acceptance and separately authorized local checkpoint are recorded below.

**Phase 7C Slice 1 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT.** Brian accepted
the implementation, recorded technical evidence and the three visuals in
[ExecPlan 079](docs/plans/079-saved-deal-index.md). The populated desktop capture is
from the real TEST stack; the 320px mixed-result and desktop mixed-result captures
use mocked responses. Screenshots establish rendered presentation, not independent
verification of authorization, interaction or replay. The archive SHA-256 was
independently matched in the review chat. Six focused PostgreSQL/API index tests,
13 static-route unit tests, 52 affected component tests, two mocked built-browser
scenarios and one real built UI/API/PostgreSQL flow pass. Generated contracts,
affected lint/format/type checks and the production build pass; owned TEST resources
were removed or stopped with no leftovers. Selections overlap and do not imply a
full-suite pass. Earlier failures, corrections and unrun checks remain in ExecPlan
079; no unaffected application/database/browser suite was rerun for closeout.

The authorized local commit is `Complete Phase 7C Slice 1 saved deal index` from
`85e5aef917513b6f521b06b63af9314b97813f12`. The index checkpoint includes only the
reviewed 7C Slice 1 paths and necessary plan/workflow/traceability closeout hunks;
protected modifications and UCS title-matching work remain outside it. Phase 7C
stays **IN PROGRESS** and Phase 7B stays **CLOSED**. The next separately authorized
boundary is Watchlist and Targets; it is not started or authorized by this closeout.
Settings/Profiles, Notes/URLs and Phase 8 remain outside this checkpoint. No
operational work or push follows.

## Phase 7B source checkpoint accepted / closed — 2026-09-18

**7B-4 is ACCEPTED / CLOSED. Phase 7B is ACCEPTED / CLOSED FOR ITS SOURCE
CHECKPOINT.** Brian accepts all three 7B-4 implementation checkpoints and the six
supplied visual images. [ExecPlan 077](docs/plans/077-forecast-revisions.md#source-checkpoint-acceptance-and-phase-7b-reconciliation--2026-09-18)
reconciles the governing criteria with accepted 7B-1–4 evidence; no in-scope
source-acceptance gap remains. Existing commands, separate selections, corrections,
warnings and unrun checks retain their recorded qualifications.

One local 48-file commit on main is authorized from
`e2c4987bb9652f53b9a8956bd1597b42a7240976`, subject
`Complete Phase 7B-4 forecast editing and append-only revisions`.
The accepted 47-file candidate gains only a requirements-traceability closeout;
five already-included documents receive additive acceptance records. Protected
modifications remain excluded and byte-preserved. Closeout uses only documentation,
content/hash and Git checks; no new application tests or screenshots.

**Next: separately authorized 7C planning, NOT STARTED.** Watchlist, persistent
targets/settings and Saved Deal Index remain 7C. Phase 7 overall remains incomplete;
Phase 8 is unchanged. Deferred Economics Extensions remain outstanding, deferred,
unsatisfied and without an assigned delivery phase. Development-database migration,
actual-account provisioning, deployment and device/HTTPS qualification remain
separate and unperformed, not newly imposed source-checkpoint blockers. No operational
work, push or later-phase work follows. Earlier pending/open/checkpoint-only entries
below are historical and superseded only for this source closeout.

## Phase 7B-4 Checkpoint 3 authorized — 2026-09-18

Brian accepts Checkpoints 1/2 evidence for onward integration and authorizes the
editor, navigation and acceptance checkpoint in [ExecPlan 077](docs/plans/077-forecast-revisions.md).
Implement and self-review, then stop for technical and visual review without
staging/commit/push. Only guarded disposable synthetic TEST resources are authorized.
7B-1–3 remain CLOSED; 7B-4 IN PROGRESS; Phase 7B OPEN. Earlier checkpoint-only
restrictions below are historical. No later slice or operational work is authorized.

Checkpoint 3 is implemented and self-reviewed: 135 component tests, 61 browser
tests, one bounded real API/PostgreSQL/browser revision flow, affected static/
contract/build and preservation checks pass. Exact assumptions, explicit cached
recalculation, shared Save/conflict recovery and historical navigation are integrated.
TEST resources are cleaned up; six inspected PNGs are in the verified visual-review
archive. ExecPlan 077 records the 19-file incremental inventory, 47-file cumulative
candidate, initial corrections and exact evidence. Technical review and Brian's
visual acceptance remain pending. Stop here without a Git checkpoint or later work.

## Phase 7B-4 Checkpoint 2 authorized — 2026-09-18

Brian accepts Checkpoint 1's reported evidence for onward integration and authorizes
only HTTP and projections in [ExecPlan 077](docs/plans/077-forecast-revisions.md).
Preserve its 20-file foundation, add the revision-preview route/lineage projections/
typed conflict/activity classification and generated contracts, validate with
synthetic disposable TEST HTTP/PostgreSQL, self-review and stop. 7B-4 remains
IN PROGRESS; Checkpoint 3 UI, operational work and staging/commit/push remain
unauthorized. Earlier Checkpoint-1-only statements below are historical.

Checkpoint 2 is implemented and self-reviewed: 26 focused HTTP/PostgreSQL tests,
31 unit checks, affected static checks, generated contract equivalence and typed
consumer checks pass. TEST resources are cleaned up and the accepted persistence
foundation is unchanged. ExecPlan 077 records the exact 12-file incremental scope,
additive response contracts, validation and review stop. Ready for technical review,
not full 7B-4 acceptance; no Checkpoint 3 or Git checkpoint follows.

## Phase 7B-4 Checkpoint 1 authorized — 2026-09-18

Brian approves the reviewed revision plan and authorizes only **Persistence and
Append Authority**, with focused synthetic disposable TEST validation and self-review,
then a technical-review stop. [ExecPlan 077](docs/plans/077-forecast-revisions.md)
records the three checkpoints and current boundary. 7B-4 is IN PROGRESS;
7B-1–3 remain CLOSED and Phase 7B remains OPEN. Private historical retention is
settled. No public API/contracts/auth-activity changes, UI, actual-account/provider
work, development/production DB, deployment, staging, commit or push. Earlier
7B-4 planning-only statements below retain their historical meaning.

Checkpoint 1 is implemented and self-reviewed, with 55 focused PostgreSQL tests,
16 contract/projection unit tests, affected static checks and unchanged public
contract generation passing. Disposable TEST resources are cleaned up. The exact
inventory, commands, corrections and boundaries are in ExecPlan 077. This is ready
for technical review, not acceptance; Checkpoints 2 and 3 have not begun.

## Phase 7B-3 source checkpoint accepted / closed — 2026-09-18

**7B-3 is ACCEPTED / CLOSED for its source checkpoint.** Brian accepts all three
implementation checkpoints and the targeted fixture correction in
[ExecPlan 076](docs/plans/076-save-original-forecast.md). Visual review is complete
for the real TEST-stack desktop Deal/save and historical views, the corrected mocked
320px historical view, and the mocked typed historical failure. The fixture-only
physical/financial contradiction is resolved; production admission, historical
projection and frozen replay are unchanged. Representation admission does not assert
verified seller contents. Mocked visuals and actual API/PostgreSQL evidence remain
distinct; no independent source-code audit, physical-device or deployment qualification
is claimed.

Brian authorizes one local 65-file checkpoint on main from
`918ec781e2b9ba3a0a6ee00ad9611b47de475ed8`, subject
`Complete Phase 7B-3 save and reopen original forecasts`, including the settled private
historical-retention decision and excluding the three protected modifications. This
closeout runs only inventory/content/hash, documentation and Git checks; earlier
application-test evidence is reused, with no new application tests or screenshots.

7B-1/7B-2 remain CLOSED; **Phase 7B remains OPEN**. Next is separately authorized
**7B-4 planning**, not started or authorized here. No operational work, push or later
implementation follows this commit. 7C, Phase 8 and Deferred Economics Extensions
remain unchanged; the extensions remain outstanding, deferred, unsatisfied and without
an assigned delivery phase. Earlier pending-review, permission and checkpoint-only
stops below retain their historical context and do not reopen settled decisions.

## Current authorization — 7B-3 checkpoint 3, UI and Acceptance

Brian accepts Checkpoints 1/2 technical evidence for onward integration and
authorizes Calculate/Save/status recovery, authenticated historical detail and its
specific static route, plus synthetic component/browser and guarded disposable TEST
real-stack acceptance. [ExecPlan 076](docs/plans/076-save-original-forecast.md)
records the implementation and review evidence. Earlier API/backend-only stops below
are historical. Stop for technical and Brian visual review; 7B-3 remains IN PROGRESS,
7B-1/7B-2 remain CLOSED. No later slice, development/production database, actual
account/provider operation, deployment, staging, commit or push is authorized.

## Current authorization — 7B-3 checkpoint 2, API and Replay

Brian accepts checkpoint 1's implementation/evidence for onward integration and
authorizes only the four forecast HTTP routes, minimal historical replay projection,
generated contracts and focused synthetic TEST validation in [ExecPlan 076](docs/plans/076-save-original-forecast.md).
Preserve the accepted dirty foundation and owner-decision updates. Prior checkpoint-1
stops below are historical. Stop after checkpoint-2 self-review; no UI/static routing,
new migration, development/production operation, live provider work, deployment,
staging, commit or push. 7B-3 remains IN PROGRESS; 7B-1/7B-2 remain CLOSED.

Checkpoint 2 is implemented and self-reviewed: four authenticated forecast routes,
minimal verified historical projection and additive generated contracts. ExecPlan
076 records the 21-file incremental inventory, 29 unit / 16 new HTTP-PG / 9 existing
regression passes, safe errors, preserved foundation and TEST cleanup. Stop for
technical review; `/deals/{id}` has no UI/static route yet.

## Current authorization — 7B-3 checkpoint 1, Persistence and Save Authority

Brian authorizes only the backend persistence/authority foundation in
[ExecPlan 076](docs/plans/076-save-original-forecast.md), focused synthetic/guarded
TEST validation and self-review, then a technical-review stop. Public API/UI wiring
remain subsequent 7B-3 checkpoints. Preserve the 12 existing owner-decision updates
and protected bytes. The private retention/display decision is settled; the older
planning-only boundary below is historical. No development/production database,
actual account setup, live providers, exposure/deployment, staging, commit or push.
7B-1/7B-2 stay CLOSED; 7B-3 is implementation-in-progress, not accepted/closed.

Checkpoint 1's internal service, migration, authority guards and transaction plumbing
are implemented. ExecPlan 076 records the literal file inventory, actual lock order,
test evidence/corrections and TEST cleanup. Stop at technical review of this backend
checkpoint; this is not acceptance of the full Save/reopen product slice.

## Current boundary — Phase 7B-3 planning only, 2026-09-17

The [owner decision](docs/DECISIONS.md#phase-7b-3-owner-retention-and-historical-display-authorization--2026-09-17)
clears the retention/historical-display gate for the authorized private scope;
separate written BrickLink clarification is not a prerequisite. Older blocked or
unresolved permission statements below are historical and superseded for that scope.
Verified main is `918ec781e2b9ba3a0a6ee00ad9611b47de475ed8`, with no later review
commit, an empty index and the three protected files unchanged against plan 074's
hashes. 7B-1/7B-2 remain ACCEPTED / CLOSED; Phase 7B remains OPEN.

Only minimal decision/workflow documentation and repository-grounded implementation
planning are authorized. Return the 7B-3 save/bookmark/reopen plan, then stop; no
runtime/test/schema/API/UI changes, tests/builds, installs, services, database or
provider access, credentials, provisioning, deployment, staging, commit or push.
Preserve historical records and existing current-evidence rules under the decision.
7B-4, 7C, Phase 8 and Deferred Economics Extensions retain their stated boundaries.

## Phase 7B-2 source checkpoint accepted / closed — 2026-09-17

**7B-2 is ACCEPTED / CLOSED for its source checkpoint.** 7B-1 remains CLOSED;
Phase 7B remains OPEN. Brian accepted the implementation and recorded validation.
This is not deployment or operational qualification. The next boundary is the
retention/display-permission review **before 7B-3**. Provider-backed persistence
remains blocked pending that determination; permission is neither established nor
prohibited. No permission research or later-slice work is authorized by this closeout.

Acceptance and the unchanged 16-file inventory are recorded in [ExecPlan 075](docs/plans/075-exact-snapshot-replay.md).
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

## Phase 7B-2 — implemented, review pending, 2026-09-17

Brian authorized [exact snapshot capture and offline replay](docs/plans/075-exact-snapshot-replay.md)
from main `d4d70d121868c00e4eb6bfbc964ed5c91d439e43`. The backend candidate implements
exact financial replay conditional on recorded historical qualifications. Original
physical/valuation/evidence-quality and eligibility assertions are preserved, not
independently re-adjudicated. Public contracts and financial behavior remain unchanged.

7B-1 remains CLOSED; 7B-2 is not accepted or closed. Stop for technical review after
the focused checks and self-review recorded in the plan. No staging, commit, push,
development migration/account setup, provider activity or deployment. Durable provider
retention/display remains unresolved. 7C, Phase 8 and Deferred Economics Extensions
remain unchanged. Earlier no-7B-2 entries describe their historical checkpoints.

## Current checkpoint — Phase 7B-1 accepted / closed, 2026-09-17

Brian accepted [7B-1 Brian-only authentication](docs/plans/074-brian-only-authentication.md)
for one local source checkpoint, subject `Complete Phase 7B-1 Brian-only authentication`,
with parent `ac6201e371ca0d022955c45a76154257e407b9f1` on main. **7B-1 is ACCEPTED / CLOSED;
Phase 7B remains OPEN.** Desktop, 320px narrow, phone and locked-session screenshots
passed Brian's visual review. The signed-in header was not supplied to the review
chat: Sign out placement has Astra's reported self-review/browser evidence only,
not manual visual approval here. This is a nonblocking checkpoint limitation.

The recorded PostgreSQL history remains 193 passed / 14 failed initially, followed
by 15 corrective passes covering all 14 failures. The 174 unrun integration cases,
deployed HTTPS, remote CI and physical-device checks remain unrun. Other successful
checks retain their recorded scope; no combined full-suite pass is claimed.

**Next: 7B-2, not authorized.** Provider-backed historical persistence remains gated
by unresolved retention/display permission. Deferred Economics Extensions remain
outstanding, deferred, unsatisfied and without an assigned delivery phase. This
checkpoint authorizes no operational work, deployment, push or later-slice work.
Earlier pending-review/no-commit entries below are historical.

## Phase 7B-1 — authentication authorized, 2026-09-17

Brian authorized only [7B-1](docs/plans/074-brian-only-authentication.md): implement,
test, debug and self-review Brian-only authentication, then stop for review.
The accepted baseline is `ac6201e371ca0d022955c45a76154257e407b9f1` on main.
Only disposable TEST migrations/identities/services and the locked authentication
dependency are authorized. No development migration, actual Brian provisioning,
live provider access, deployment, commit or push. Preserve the three protected
dirty files. 7B-2 and later proposals remain unimplemented; provider-backed history
retention/display permission remains unresolved. Earlier no-7B entries below are
historical. Phase 7A2 remains closed; its deferred extensions stay outstanding.

Implementation, self-review and applicable test evidence are now recorded in the
7B-1 plan. The candidate is ready for Brian's technical/visual review; it is not
accepted or committed. Work stops at 7B-1 with no later-slice authorization.

## Current checkpoint — Phase 7A2 whole-set closure, 2026-09-17

**Phase 7A2 Whole-Set Deal Economics: COMPLETE / ACCEPTED / CLOSED.**

Brian accepted Slice 1/2A/2B technically and visually at
`fbbd98b29b84fe2b60132da8c1bfacc8d5f7ec54` on `main`, then explicitly approved
the [new closure/deferral decision](docs/DECISIONS.md#phase-7a2-whole-set-closure-and-explicit-deferral--2026-09-17).
All outstanding contents/condition and alternative economics now belong to
[Deferred Economics Extensions](docs/REQUIREMENTS_TRACEABILITY.md#deferred-economics-extensions):
outstanding/deferred, not cancelled or satisfied, outside closed 7A2, with no
automatic assignment to Phase 8 or 7B/7C.

This authority supersedes earlier overall-open/not-started statements and broader
7A2 assignments below; prior Slice 1/2A/2B scopes and acceptance remain historical.
Phase 7 overall is not closed. Authentication has no technical dependency on the
deferred bucket; the whole-set model is stable enough for persistence subject to
7B's [frozen snapshot/version and retention questions](docs/DATA_MODEL.md#7b-persistence-questions--unresolved).

Authorized now: documentation reconciliation and one local documentation-only
checkpoint; no push. Preserve byte-for-byte the existing `AGENTS.md`,
`services/api/tests/integration/test_catalog_search.py` and
`services/api/tests/unit/test_catalog_parser.py` changes. No application, test,
schema, contract, dependency, provider configuration or migration changes.
No further 7A2 implementation or 7B work. Next separately authorizable task is the
7B ExecPlan; start a new conversation for that next slice after this checkpoint.

Documentation verification: the 15-file change is additive; all historical bodies
are preserved. All 363 local Markdown links and 42 added anchors resolve; diff
whitespace checks pass. New text passes Prettier. Eleven existing document bodies
already fail whole-file Prettier at the starting commit and are preserved; the
three slice plans and Prompt 07 pass whole-file formatting. The protected SHA-256
values match the accepted baseline. No application tests or services are run for
this documentation-only checkpoint.

## Phase 7A2 Slice 2B — accepted checkpoint, 2026-09-17

**Selling Fee Rules: COMPLETE / ACCEPTED / CLOSED. Brian technical PASS; visual PASS.**
Brian authorizes one local commit on main, subject
`Complete Phase 7A2 Slice 2B Selling Fee Rules`, parent
`8cbffb06baeb78d7c71abdeedfbbd1d5e86f646a`.
[ExecPlan 073](docs/plans/073-selling-fee-rules.md#final-acceptance-and-checkpoint--2026-09-17)
records the final invariant review, validation and exact 21-file checkpoint scope.
Slice 1 and 2A remain accepted; protected unrelated files remain excluded. No push,
later provisional 7A2 work or later-phase authorization. Phase 7A2 overall remains
open. Earlier pending-review and no-commit statements below are historical.

## Phase 7A2 Slice 2B — implementation authorized, 2026-09-17

Brian authorized only Selling Fee Rules after accepted 2A checkpoint
`8cbffb06baeb78d7c71abdeedfbbd1d5e86f646a` on `main`.
[ExecPlan 073](docs/plans/073-selling-fee-rules.md) records the explicit manual versus
percentage/fixed modes, two supported bases, per-transaction rounding and validation.
Implementation and full technical validation now PASS; Brian review is pending.
Preserve accepted Slice 1/2A and all evidence/lifecycle semantics. Stop for review:
no commit, push, providers, persistence, migration or later 7A2/7B/7C/8 work.
The three protected dirty files remain excluded. Earlier no-2B entries are historical.

## Phase 7A2 Slice 2A — accepted checkpoint, 2026-09-17

**Slice 2A COMPLETE / ACCEPTED / CLOSED. Technical PASS; Brian visual PASS.**
Brian authorizes one local commit on `main`, subject
`Complete Phase 7A2 Slice 2A Purchase Limits`, parent
`0e0824ca1a530cb2891c54375d56f4e477cf7072`. The exact 21-file scope, final presentation
correction, invariant review and validation are in
[ExecPlan 072](docs/plans/072-purchase-limits.md#final-acceptance-and-checkpoint--2026-09-17).
Exclude the three protected modified files. No push. Stop before 2B; it remains
unstarted and separately authorized. Earlier pending statements are historical.

## Phase 7A2 Slice 2A — technical PASS, review pending, 2026-09-17

The bounded 2A implementation and full validation are complete; evidence and the
21-file inventory are in [ExecPlan 072](docs/plans/072-purchase-limits.md).
Brian visual review is pending. Stop here: no 2B, commit or push is authorized.
The three protected files remain byte-for-byte unchanged; the index is empty.

## Phase 7A2 Slice 2A — implementation authorized, 2026-09-16

Brian authorized purchase limits under [ExecPlan 072](docs/plans/072-purchase-limits.md),
starting at accepted Slice 1 `0e0824ca1a530cb2891c54375d56f4e477cf7072` on `main`.
Targets, both caps, qualified maximum, headroom, whole-set break-even purchase price
and declared purchase-price acquisition rates are in scope. Validate 2A and stop for
review. **2B is not authorized until after 2A review.** Contents/condition adjustments
and alternative-strategy economics remain provisional, unstarted later 7A2 work.
No persistence, providers, migration, 7B/7C/8, commit or push. Preserve the three
protected modified files. Earlier “no Slice 2” entries are historical boundaries.

## Phase 7A2 Slice 1 final acceptance and checkpoint — 2026-09-16

**Slice 1 COMPLETE / ACCEPTED / CLOSED. Technical PASS; Brian visual PASS.**
Brian accepted the reviewed Whole-Set Deal Economics implementation and explicitly
authorized one local checkpoint on `main`, based on
`8fcde3f058e767e39e1ecc7a960352cbf28b7322`, with subject
`Complete Phase 7A2 Slice 1 Whole-Set Deal Economics`.
[ExecPlan 071](docs/plans/071-whole-set-deal-economics.md#final-acceptance-and-checkpoint--2026-09-16)
records the exact 23-file scope, invariant review, validation and protected hashes.
7A1 and Phase 1–6 semantics remain accepted. No push and no Slice 2.
Earlier uncommitted/pending statements below are historical.

## Phase 7A2 Slice 1 implementation — 2026-09-15

Brian authorized only the whole-set Deal Economics vertical slice under
[ExecPlan 071](docs/plans/071-whole-set-deal-economics.md), starting from
`8fcde3f058e767e39e1ecc7a960352cbf28b7322` on `main`. Implementation and local
technical acceptance are complete; Brian visual acceptance remains pending.
7A1 remains CLOSED. No Slice 2, persistence, auth, overlays, generalized fees,
provider dispatch, migration, infrastructure, commit or push is authorized.
The three pre-existing modified files remain protected. Earlier entries below
retain historical acceptance/authorization context.

## Phase 7A1 final acceptance and closeout - 2026-09-15

**7A1 COMPLETE / ACCEPTED / CLOSED. Technical PASS; Brian visual PASS.**
Brian accepted the current reviewed product-led hero, New/Used by Sold market/Active
listings matrix, Resale form, exact-set Rebrickable image/provenance, and responsive
visual evidence including 390x844 and 320x720. The permanent Brian-only private,
personal, non-commercial-use constraint remains binding. Phase 1-6 semantics and
the single set-scoped request/refresh/poller guarantees remain unchanged.

[Final acceptance record](docs/plans/070-set-detail-information-architecture.md#final-acceptance-and-local-checkpoint---2026-09-15)
records repeated technical PASS, the retained 37 reviewed screenshots, exact
30-file local checkpoint scope and three protected unrelated files. Brian authorizes
one checkpoint on `main` with subject `Complete Phase 7A1 Set Detail and visual revision`.
No further presentation edits, no push, and no Phase 7A2. Earlier pending/rejected
visual checkpoints below are historical. **7A2 remains NOT STARTED.**

## Latest 7A1 visual revision handoff - 2026-09-15

The product-hero / market-matrix rewrite and exact retained Rebrickable image
projection are technically complete. Final PASS: 50 component, 22 tooling, 873
Python and 21 browser tests; contracts, types, lint, scoped formatting and build.
37 new screenshots plus retained before evidence are indexed in
`.local/acceptance/7a1-visual-revision-20260915/README.md`.
Brian's visual acceptance remains pending. No commit, push or 7A2; all accepted
technical/domain semantics remain. See [ExecPlan 070](docs/plans/070-set-detail-information-architecture.md)
for provenance, no-extra-request/poller proof, changed files and database-test limits.

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


## Phase 7A1 accepted implementation scope - 2026-09-15

[ExecPlan 070](docs/plans/070-set-detail-information-architecture.md) records the accepted decision-first migration and implementation authorization. Phase 6 and UI-01 remain CLOSED. Phase 7A1 is technically complete; 45 component and 17 synthetic browser tests, frontend static checks and build pass. Synthetic visual evidence is ready; Brian visual acceptance remains pending. Earlier checkpoint statements below are historical. No 7A2, backend/API, database, provider, dependency, staging, commit or push work is authorized.

**Current checkpoint — UI-01 COMPLETE / ACCEPTED / CLOSED, 2026-09-15:** Brian
accepted the four desktop/phone screenshots and the reviewed shell, persistent
search, Scout/results, responsive behavior, focus treatment and existing Set Detail
inside the shell. Technical acceptance remains PASS; no polish pass or code change
is required. Phase 6 remains CLOSED; Phase 7 is NOT STARTED. Brian authorized one
local checkpoint of the approved UI/UX architecture and UI-01 files, excluding the
three protected pre-existing changes; no push. [UI-01 closeout](docs/plans/061-ui-foundation.md#ui-01-visual-acceptance-and-closeout--2026-09-15)
records acceptance and the deferred 7A1 considerations. **Next: separately authorize
planning for Phase 7A1 — Set Detail Information Architecture, preferably in a new
task after the checkpoint.** Earlier pending/unstarted entries below are historical.

**Current checkpoint — UI-01 implemented; Brian visual acceptance pending,
2026-09-14:** The separately authorized shared shell/search prerequisite passes
34 frontend component tests, 9 synthetic browser tests, web typing/lint/format and
the production build. Desktop/laptop/tablet/phone and 320px layouts preserve accepted
appraisal/refresh behavior; no Phase 7 work, backend/API/dependency change or live
provider traffic. [ExecPlan 061](docs/plans/061-ui-foundation.md#ui-01-implementation-and-technical-review--2026-09-14)
records exact scope, fixes, commands and review screenshots. The three protected
pre-existing files and prior architecture documentation are preserved except for
this workflow and the living UI-01 plan. All work remains unstaged/uncommitted;
the task-owned test web server is stopped. Phase 6 remains CLOSED.
**Next: Brian reviews the four synthetic screenshots; resolve any UI-01 adjustments
before separately authorizing Phase 7A1.** Earlier unstarted statements below record
the documentation gate, not the current implementation status.

**Current checkpoint — Phase 6 CLOSED; UI/UX architecture approved, 2026-09-14:**
The separately authorized development migration and bounded live button acceptance
completed at `0b9b6bae198d19001553e72f2549508dd6400845`. Retained reconciliation is
PASS: one confirmed operation, 0 identity + 4 price + 0 retry = 4 provider attempts,
no duplicate traffic after reads/reload, and unchanged physical gates. See
[Phase 6 closure](docs/plans/060-product-surface.md#phase-6-live-acceptance-and-closure--2026-09-14).
Earlier pending/live-unexecuted entries below remain historical evidence.

Brian approved [D-033 and the UI/UX architecture](docs/UI_UX_ARCHITECTURE.md): one
bounded prerequisite before Phase 7, preserving numbered phases and accepted domain
semantics. **Next implementation slice: [UI-01 — Shared Shell and Persistent Set
Search](docs/plans/061-ui-foundation.md).** This approval authorizes documentation
only; UI-01 and Phase 7 are NOT STARTED. No code/runtime/provider/dependency/Git
action is authorized by recording the plan.

The accepted sequence is Phase 6 COMPLETE → UI-01 → **7A1 Set Detail Information
Architecture** → **7A2 Deal Economics** → **7B Authentication and Reproducible Saved
Deals** → **7C Watchlist / Targets / Settings / Saved Deal Index** → **Phase 8 Hunt**.
7A1 and 7A2 are separate acceptance boundaries, not an indivisible coding slice.
The detailed Phase 7 ExecPlan is deferred until separately requested. Phase 9+
ownership remains unchanged, including image/listing/recognition/capture in 13–15
and actual resale outcomes in 16. Contents refresh remains outside accepted Phase 6.

**Phase 6B public workflow independently accepted — 2026-09-14:** Review corrected
terminal replay configuration dependence, status-read recovery, keyboard focus and
incompatible pause codes. The 25-file local checkpoint passes 53 distinct PostgreSQL
cases, 84 Python units, 27 React tests, synthetic mobile/desktop browser acceptance,
static/contracts/build/package and artifact checks. All 89 review-owned databases
are removed; TEST/APIs are stopped and original resources/protected files preserved.
ZERO provider requests or real provider credential loading; no development access,
migration/dependency change or push. [Independent acceptance](docs/plans/060-product-surface.md#phase-6b-public-workflow-independent-review--2026-09-14)
records findings, scope, actual evidence and the authorized single local commit.
**Next: separately authorize guarded development migration 0008, existing account
configuration and bounded live product button acceptance.** Contents refresh and
Phase 7 remain deferred. Earlier entries preserve their historical status.

**Phase 6B public market refresh implemented — awaiting independent review,
2026-09-14:** Typed plan/confirm/status/active-operation/resume APIs and the React
complete-set refresh flow wrap accepted migration 0008. Explicit confirmation is
required; GETs/planning remain pure and exact 4/4/2/10 ceilings survive rejoin.
Acceptance passes 51 PostgreSQL cases, 84 focused Python unit cases, 25 React cases,
and a real-browser synthetic TEST workflow at mobile/desktop sizes. Static checks,
contracts and package/build checks pass. ZERO live provider requests and provider
credential loading; no development migration, dependency or schema changes.
All 82 task-owned disposable databases are removed. TEST and owned APIs are stopped;
the original container/volume/network inventory is preserved.
Changes remain unstaged/uncommitted on `main` at `b7975d185ce665f2cd243c34728379ce9e645fd6`;
the three historical dirty files remain byte-for-byte protected. Contents refresh
and Phase 7 remain deferred. [ExecPlan 060](docs/plans/060-product-surface.md#phase-6b-public-workflow-implementation--2026-09-14)
records inventory, validation and limitations. **Next: independent review and local
checkpoint commit of the Phase 6B product workflow.** First real migration/button
acceptance remains a later separately authorized action. Earlier entries retain
their historical scope and checkpoint status.

**Phase 6B durable prerequisite independently accepted — 2026-09-14:** Four proven
defects were corrected in migration 0008 and its existing backend scope: expired
transaction-time authorization, initial confirmation expiry, terminal joined-work
binding and embedded discovery payloads. Independent acceptance passes 220 real
PostgreSQL cases, 134 unit/runner cases, typing/lint/format, contracts, installed
package/resources and artifact checks. All 185 review-owned disposable databases
are removed; TEST and the smoke API are stopped. The 33-file local checkpoint is
explicitly authorized; the three unrelated dirty files remain byte-for-byte preserved
and excluded. ZERO provider requests and provider credential loading; no development
access or push. [Independent acceptance](docs/plans/060-product-surface.md#phase-6b-durable-prerequisite-independent-review--2026-09-14)
records the evidence and exact scope. **Next: separately authorize Phase 6B public
refresh API/UI work in a new task.** Phase 7 remains pending. Earlier entries retain
their historical status and permissions.

**Phase 6B durable prerequisite implemented — awaiting review, 2026-09-14:** The
authorized offline implementation includes `0008_product_refresh_operations`,
durable confirmation/execution/evidence/view associations, exact 4/4/2/10 accounting,
UUID4 keys and the 15-minute/24-hour/30-day lifecycle. [ExecPlan 060](docs/plans/060-product-surface.md#phase-6b-durable-prerequisite-implementation--2026-09-14)
records the 33-file inventory and new acceptance evidence: 330 unit/runner cases,
216 distinct PostgreSQL cases after focused corrections, static/package checks and
cleanup. ZERO provider requests and credential loading; no development access,
public refresh API/UI or Phase 7. TEST is stopped; the three unrelated dirty files,
main HEAD and empty index are preserved. All work remains unstaged/uncommitted.
**Next: independent review of this prerequisite.** Any checkpoint commit needs
separate explicit authorization; the product refresh workflow remains pending.

**Phase 6B authorized; stopped at schema prerequisite — 2026-09-13:** Read-only
source inspection at `541cf965f97634d7ce2eaca4d98aa69f8c840bb5` found that migration
0007 restricts accounting roots to P4-01 and has no durable product operation
binding for the selected set, confirmed plan and execution identity. The existing
discovery-to-mapping handoff also needs crash-safe completion design. Sections 10
and 22 of Brian's 6B request require stopping when correct restart/idempotency needs
new schema. [ExecPlan 060](docs/plans/060-product-surface.md#phase-6b-schema-prerequisite-stop--2026-09-13)
records the exact gaps and proposed prerequisite for review. No 6B API/UI, migration,
dependency, database/service operation, provider request or credential loading.
Only this checkpoint and the plan changed; all work remains unstaged/uncommitted.
**Next: Brian authorizes a bounded durable-operation/accounting prerequisite plan.**
The requested 6B independent implementation review/commit remains the later endpoint.
Earlier entries retain their historical status.

**Phase 6A independently accepted — Phase 6B ready, 2026-09-13:** Set-number/name search and bookmarkable cached appraisal detail pass independent product review for the authorized local checkpoint. Four strategies and four market views preserve partial, unknown and physical-blocked states. The Windows smoke harness now reserves an OS-assigned TEST port; corrected integration acceptance exits successfully. [ExecPlan 060](docs/plans/060-product-surface.md) records the 40-file reviewed inventory, bounded fixes, automated/manual checks and cleanup. ZERO provider requests / ZERO provider credential loading; no new migration or dependency. **Next: separately authorize Phase 6B explicit user-triggered discovery/refresh.** Phase 6B and saved/deal/Hunt work have not started. Earlier entries are historical checkpoints.

**Phase 5C independently accepted — Phase 5 complete, 2026-09-12:** Review corrected
zero-activity sample quality while retaining UNKNOWN liquidity and null dollars.
Immutable `valuation-synthesis-v1`, exact thresholds/factors and honest scenario,
partial, exposure and physical boundaries pass 277 affected units and static/package
checks. [ExecPlan 050](docs/plans/050-valuation.md#phase-5c-independent-acceptance--2026-09-12)
records the 13-file local checkpoint and acceptance evidence. No provider request,
credential loading, database access or push. Gems, ranking, deal economics, Hunt
scoring and M-derived metrics remain deferred. **Next: Brian separately authorizes
Phase 6 in a new task.** Earlier entries preserve historical scope and permissions.

**Phase 5C implemented — awaiting review, 2026-09-12:** Brian approved immutable
`valuation-synthesis-v1`, labeled partial dollars and final bounded Phase 5 synthesis.
[ExecPlan 050](docs/plans/050-valuation.md#phase-5c-approved-implementation-contract--2026-09-12)
records the contract and verification: 276 affected units, strict typing/lint/format,
offline package and preservation checks pass. All recovery factors are UNCALIBRATED APPLICATION_SCENARIO
assumptions, not expected proceeds or provider facts. Concentration is annotation
only; Gems, economic ranking, deal economics and Phase 6 remain deferred.
Leave 5C unstaged/uncommitted. **Next: Independent review and local checkpoint
commit of Phase 5C.** Earlier entries preserve historical scope and authorization.

**Phase 5B independently accepted — 2026-09-12:** Review corrected a large-Decimal
ratio failure and verified the bounded liquidity/concentration contract. Acceptance
and the exact ten-file checkpoint are recorded in [ExecPlan 050](docs/plans/050-valuation.md).
Phase 5C is ready for separate authorization and remains unstarted. No push.
**Next: Brian separately authorizes a bounded Phase 5C plan in a new task.**
Earlier entries preserve their historical status.

**Phase 5B implementation — 2026-09-12:** Brian authorizes deterministic liquidity
and concentration diagnostics on accepted Phase 5A. The bounded contract and
verification record are in [ExecPlan 050](docs/plans/050-valuation.md#phase-5b-bounded-contract--authorized-2026-09-12).
S/O/C/I, compatible sell-through proxy, concentration and metric readiness are in
scope; exact production M, recoverability coefficients/dollars, Gem/burden/Hunt
classification, deal economics and 5C are not. Work remains unstaged/uncommitted.
**Next: Independent review and local checkpoint commit of Phase 5B.**
Earlier entries preserve their historical authorization and checkpoint status.

**Phase 5A core deterministic valuation independently accepted, 2026-09-12:**
The separately authorized bounded theoretical engine consumes admitted physical
occurrences, exact quantity-weighted evidence and a versioned code policy. Whole-set
and contents strategies remain independent; failed physical admission has null values,
while missing market evidence can produce a labeled partial subtotal with known
coverage. No migration, provider request, UI, deal economics, 5B/5C or saved workflow.
See [ExecPlan 050](docs/plans/050-valuation.md) for scope and verification.
Independent review corrected ambient Decimal-context leakage and receipt reuse beyond
tightened market-policy deadlines. The 16-file local checkpoint passes 233 affected
units, eight PostgreSQL cases, strict typing, lint/format and installed-package checks.
All nine review-owned TEST databases are removed, TEST is stopped, and the three
unrelated dirty files are preserved. No push. **Next: Brian separately authorizes
Phase 5B recovery/liquidity work in a new task; do not begin it automatically.**
Earlier checkpoints retain their historical status and permissions.

**Physical completeness gating independently accepted — 2026-09-12:**
All 20 slice files pass independent review after bounded descendant-diagnostic and
pinned-child revision corrections. Passing evidence: 133 affected units, eight
PostgreSQL cases, strict typing, lint/format, installed wheel/sdist checks and
178 official projected rows verified against cached source hashes. All eight owned
TEST databases are removed and TEST is stopped; three unrelated dirty files remain
unchanged and excluded. One local checkpoint commit is authorized; no push.
**Phase 5 entry contract is satisfied.** Strategy-specific physical gates must pass
before dependent calculations; unsupported results remain null. Phase 5 itself
requires separate authorization and remains unstarted. See
[independent acceptance](docs/plans/040-calibration.md#independent-physical-completeness-acceptance--2026-09-12).
Earlier entries retain their historical status and permissions.

**Physical completeness gating implemented — awaiting independent review, 2026-09-12:**
The approved bounded prerequisite now supplies versioned, representation-specific
physical assessments, scoped source contracts, read-only ingestion provenance and
one all-or-nothing expansion/calibration admission gate. Official P4-01/02/08/09/10
contents remain UNKNOWN; authored synthetic contracts prove supported paths.
Whole-set eligibility remains independent. No migration, accepted catalog change,
provider request or Phase 5 formula was made. Work is unstaged and uncommitted.
See [implementation and verification](docs/plans/040-calibration.md#physical-completeness-implementation-result--2026-09-12).
**Next: Independent review and local checkpoint commit of the physical-completeness
assessment/gating slice.** Phase 5 needs acceptance of this gate and separate
implementation authorization; it does not require universal catalog completeness.
Earlier entries below preserve their historical scope and permissions.

**Phase 4 final evidence review accepted — 2026-09-12 UTC:** Market acquisition
and calibration feasibility is sufficiently demonstrated for the present architecture
decision. **NO STAGE 2 LIVE CASE NEEDED.** P4-01 accounting remains **36 identity /
44 price / 0 retry / 80 total**; this documentation review made **ZERO additional
provider requests**. Quantity-weighted averages are materially closer to Brian's
manual website values in both NEW views and remain the current calibration statistic.
The comparison is **PARTIALLY COMPARABLE**: exact website geography and algorithm
remain unproven. The matching **37 items / 10 lots** establish count-level agreement,
not every website line identity or universal price accuracy.

Both `inventory_components_incomplete` and `minifigure_membership_unknown` remain
unchanged. S, O, C and current inventory count are usable inputs; exact M and a final
liquidity score remain unsupported. The optional broader-geography 20-request probe
is a future diagnostic only, neither required nor authorized. Stage 2 and Phase 5
remain unstarted. **Next: separately authorize a bounded physical-completeness
semantics planning/review slice before Phase 5 deterministic valuation.** This is
the next higher-value engineering problem; no implementation is authorized here.
See [final evidence review](docs/PHASE_4B_STAGE_1.md#final-evidence-review-and-local-checkpoint--2026-09-12-utc).

The checkpoints below are historical, including their pending website comparison,
earlier Stage 2 recommendation and then-uncommitted Git state. This review authorizes
one local documentation checkpoint only; no push or broader product acceptance.

**Phase 4B Stage 1 live calibration complete — 2026-09-12 UTC:** Development is
migrated to accepted 0007; all 40 catalog digests/history and market policy are
preserved. P4-01 run `40e5120d-6266-4539-a2d9-0bbd1c045d26` consumed **36 identity / 44 price /
0 retry / 80 total**, with 11 verified mappings and zero unresolved. All four
USD/US views were obtained; physical components/figure membership still block
contents totals. Development is stopped, the index is empty, and these Stage 1
documentation changes remain unstaged/uncommitted. **Website comparison is pending
Brian's manual value/settings capture.** Stage 2 and Phase 5 remain unstarted;
the recommendation is at most the same 40/48/8/96 ceiling for one separately
authorized, preflight-bounded case. See [live result](docs/PHASE_4B_STAGE_1.md#live-stage-1-completed--2026-09-12-utc).
Historical records below retain their then-applicable boundaries.


**Phase 4B discovery-accounting independent acceptance — 2026-09-12 UTC:**
All 32 checkpoint files are reviewed; no blocking finding remains. A reproduced
Windows installed-migration failure at a 261-character path is corrected through
native extended paths for Alembic and SQL resources. Passing evidence covers 290
distinct units and 178 distinct PostgreSQL cases across the initial pass and focused
reruns, plus static/package/resource checks. All 105 review-owned TEST databases
are verified absent; TEST is stopped and resources preserved. One local checkpoint
commit is authorized; no push. Live use remains 0/0/0/0, with 40/48/8/96 unspent.
Development and real provider credentials were untouched. Next: Brian separately
authorizes guarded development migration 0007 and resumption of P4-01 Stage 1 under
the existing ceilings and unresolved physical-evidence gates. Do not resume live
execution or begin Phase 5 automatically. See [acceptance](docs/plans/040-calibration.md#independent-discovery-accounting-acceptance--2026-09-12-utc).
Earlier checkpoints below preserve historical implementation and authorization.

**Phase 4B discovery-accounting prerequisite - 2026-09-12 UTC:** Brian authorized
only offline implementation of additive migration 0007. One discriminated provider
attempt ledger now supports discovery before reviewed mapping and retains strict
price cache/job identity. The P4-01 root enforces 40/48/8/96 across child groups,
with shared retries, pacing, suspension and restart-safe accounting. Offline
acceptance passes: 289 units and 104 distinct PostgreSQL cases across the initial
pass and focused correction. Package/static checks pass; work remains unstaged/uncommitted. Development
and real provider credentials are untouched; no live run exists and live use is
0/0/0/0. Next: independent review and local checkpoint commit of this extension.
Do not resume live Stage 1 automatically. See [current report](docs/PHASE_4B_STAGE_1.md)
and [ExecPlan 040](docs/plans/040-calibration.md). Earlier checkpoints below retain
their historical authorization and evidence.

**Phase 4B Stage 1 resumed checkpoint — 2026-09-12 UTC:** Accepted development
migration 0005 → 0006 and default immutable market-v1 policy/scope initialization
succeeded through existing owned/admin paths. Forty catalog-table digests, import
history and official/synthetic pointers are unchanged; development is stopped.
P4-01 binds correctly, with 10 regular lots/quantity 37 and 44 price requirements,
but physical expansion reports unknown components/minifigure membership. Live
admission stopped: accepted Phase 3C accounting has no identity-discovery reservation
path (fetches require verified-mapping price jobs). Brian's resumed instruction
requires a stop for a prerequisite outside the accepted design. Zero attempts; no
live ledger; all 40/48/8/96 allowance remains. A reviewed accounting extension needs
separate authorization. See [current checkpoint](docs/PHASE_4B_STAGE_1.md).
Stage 2 and Phase 5 remain unstarted; earlier migration-stop records below are historical.

**Phase 4B Stage 1 preflight checkpoint — 2026-09-12 UTC:** Brian authorized only
P4-01 (41802-1), with 40 identity initials / 48 price initials / 8 retries / 96 total.
Live work stopped before admission: owned development is at migration 0005 and all
eight Phase 3C market tables are absent; this task explicitly prohibits migration.
Zero provider attempts, no live ledger initialized, all allowance preserved.
The accepted official full-catalog snapshot remains active at generation 1.
Development was restored to its initial stopped state. See the
[Stage 1 checkpoint](docs/PHASE_4B_STAGE_1.md). A separately authorized development
0006/policy prerequisite is needed before resuming preflight; Stage 2 and Phase 5
remain unauthorized. Earlier 4A/3C records below are historical acceptance evidence.

**Phase 4A independent offline acceptance — 2026-09-12 UTC:** The offline calibration harness, fixed corpus, read-only cache lookup and hypothetical admission pass independent review after a bounded revoked-mapping projection correction. See [ExecPlan 040](docs/plans/040-calibration.md) for acceptance evidence and the exact 26-file local checkpoint scope. Next: **Brian chooses Phase 4B scope/traffic ceiling and separately authorizes its access/rights review and live execution.** Phase 4B and Phase 5 remain unstarted; the 400-attempt proposal is unauthorized.

**Phase 3C offline accepted — 2026-09-12 UTC:** F5 is corrected and deterministic PostgreSQL regressions pass. [ExecPlan 030, section 18](docs/plans/030-market-provider.md#18-independent-phase-3c-offline-acceptance--2026-09-12-utc) preserves the finding and records final verification and the reviewed 32-file checkpoint scope. Phase 3 is complete locally; Phase 4 requires separate authorization. Historical checkpoints below remain dated evidence.

**Current checkpoint — 2026-09-11:** Phase 2 is locally accepted: official development generation 1, cached no-op and history preservation verified, cleanup correction tested, and all 61 intended files independently reviewed. This acceptance does not establish deployment or the deferred product capabilities. See [ExecPlan 020](docs/plans/020-catalog-foundation.md). Phase 3A passes independent offline acceptance for the authorized local checkpoint: 141 BrickLink tests and 416 Python units pass after two bounded transport corrections. See [ExecPlan 030](docs/plans/030-market-provider.md) for actual verification. Phase 3B discovery correction and bounded live proof passed: three justified mappings, twelve valid price views, 7 identity + 12 price + 0 retry = 19 attempts. Independent acceptance passed after three narrow offline corrections and 218 affected tests; the local checkpoint commit is authorized. See ExecPlan 030 section 17 for evidence qualifications. Credential/IP compatibility was demonstrated for this local run. Phase 3C and its retention/display-rights decisions remain unstarted.

Dated execution records below preserve historical outcomes and then-applicable authorization; their pending or blocked states do not supersede this checkpoint.

**Historical Phase 2D outcome — 2026-09-10 local: BLOCKED at a different development SQL timeout.** The requested observation timeout is proven and corrected by in-transaction candidate color-fact analysis. An independent matching retained-state probe changes SELECT from a 300-second timeout to 0.820762 seconds and full rollback INSERT to 57.537484 seconds; corrected retained official acceptance inserts 1,557,375 observations in 55.291041 seconds and passes 72 pre/postactivation cases plus no-op. All 264 Python units, 22 Node tests, 11 React tests, 196 PostgreSQL tests, six browser cases and build/contracts/package gates pass. Authorized fourth NEW development run `bcf21407-15ab-44bb-b358-17f600282599` instead times out earlier at step 16 `evidence_conflict:elements` in 300.004024 seconds (57014); its cause is not yet proven. Construction rolls back before the corrected observation step, validation, benchmark or activation. Read-only verification confirms zero candidate facts/validation, official generation 0/no receipts, unchanged two synthetic snapshots/four receipts/generation 4, and all three prior failed histories/staging unchanged. A fourth terminal failed run is retained. The accepted Windows publisher, migration 0005, existing indexes and 300-second limit remain unchanged. No fifth import, provider call, staging cleanup, Git checkpoint or Phase 3 work occurs. See the [current 42-item report](docs/PHASE_2D_OBSERVATIONS.md). Earlier stops below remain historical evidence.


## Current checkpoint and next task

Phase 2 local acceptance remains complete. Phase 3A passes independent offline acceptance for one explicitly authorized local checkpoint commit. [ExecPlan 030](docs/plans/030-market-provider.md) records source review, two corrected transport findings, final hashes and newly executed versus reused verification. Phase 3B passes independent acceptance for the authorized local checkpoint commit; ExecPlan 030 section 17 records the reviewed inventory, corrections, offline verification and preserved live proof. The next separately authorizable task is to resolve Phase 3C retention/display/derivation rights and finalize its persistence/refresh design. No Phase 3C implementation or further provider requests are authorized.

### Historical fourth-run stop

**Historical Phase 2D outcome — 2026-09-10 local: BLOCKED at a different development SQL timeout.** The requested observation timeout is proven and corrected by in-transaction candidate color-fact analysis. An independent matching retained-state probe changes SELECT from a 300-second timeout to 0.820762 seconds and full rollback INSERT to 57.537484 seconds; corrected retained official acceptance inserts 1,557,375 observations in 55.291041 seconds and passes 72 pre/postactivation cases plus no-op. All 264 Python units, 22 Node tests, 11 React tests, 196 PostgreSQL tests, six browser cases and build/contracts/package gates pass. Authorized fourth NEW development run `bcf21407-15ab-44bb-b358-17f600282599` instead times out earlier at step 16 `evidence_conflict:elements` in 300.004024 seconds (57014); its cause is not yet proven. Construction rolls back before the corrected observation step, validation, benchmark or activation. Read-only verification confirms zero candidate facts/validation, official generation 0/no receipts, unchanged two synthetic snapshots/four receipts/generation 4, and all three prior failed histories/staging unchanged. A fourth terminal failed run is retained. The accepted Windows publisher, migration 0005, existing indexes and 300-second limit remain unchanged. No fifth import, provider call, staging cleanup, Git checkpoint or Phase 3 work occurs. See the [current 42-item report](docs/PHASE_2D_OBSERVATIONS.md). Earlier stops below remain historical evidence.

### Historical R-code stop (superseded by current official evidence)

**Phase 2D resumed on 2026-09-09:** User-captured current official policy evidence
cleared metadata acquisition. `catalog:download` acquired all twelve gzip files;
cache, receipts and bounded profile corrections are implemented. The complete
[42-item report](docs/PHASE_2D_OFFICIAL_EVIDENCE.md) identifies the remaining
source-value gate: 2,987 records use `R`, without explicit official code/label
evidence. No canonical import, acceptance DB or development activation occurred.
Next: establish the official label paired with `R`, then use the cached bundle to
resume the original fresh-acceptance sequence. No additional authorization is
needed for the already authorized bounded correction if evidence establishes it.
Phase 2 remains incomplete and Phase 3 is not started. Do not stage or commit.

### Historical initial Phase 2D policy stop

**Phase 2D BLOCKED before acquisition — 2026-09-09.** Implementation was explicitly
authorized, and the exact clean starting checkpoint passed. Current official
Downloads/Terms access failed, leaving the required policy gate unverified. No
download, application change, database access or activation occurred. See the
[42-item gate report](docs/PHASE_2D_PROVIDER_GATE.md) and
[ExecPlan 020](docs/plans/020-catalog-foundation.md). Next: obtain readable current
official policy evidence, then resume Phase 2D at that gate. Phase 2 remains
incomplete; Phase 3 is not started. Changes are documentation-only and uncommitted.

### Historical Phase 2C checkpoint

**Phase 2C independently accepted — 2026-09-09.** Brian authorized this review, bounded corrections and one conditional local checkpoint commit. Three reproduced defects were corrected; all 183 PostgreSQL tests, unit suites, static/contracts checks and package/frontend builds pass. [ExecPlan 020](docs/plans/020-catalog-foundation.md) records independent evidence, the exact 43-file checkpoint inventory and cleanup; [catalog operations](docs/CATALOG_IMPORT.md) describe the internal query boundary. Preserve the historical blocked migration proposal and prior checkpoints. The checkpoint includes only reviewed Phase 2C work and acceptance documentation; no push is authorized. Phase 2 remains incomplete and Phase 2D has not started.

The exact next action, requiring separate explicit authorization, is **Phase 2D — official Rebrickable bulk catalog acquisition, actual header/schema verification, official import/activation, real-set benchmark validation, mapping/semantic coverage report, and realistic full-catalog performance evidence.** Do not begin it automatically.

### Historical Phase 2B checkpoint

**2026-09-09 — Phase 2B independently accepted.** Slice 2B passed independent local acceptance on 2026-09-09 for the authorized local checkpoint. Migration 0004, offline CSV/gzip parsing, typed COPY staging, stable identities, candidate validation, explicit atomic activation, receipts and recovery are accepted against synthetic local evidence. Review corrected nullable version/target validation and terminal-run transitions; all 161 PostgreSQL tests passed. Phase 2 remains incomplete; profiles remain DOCUMENTATION-VERIFIED / LIVE-UNVERIFIED, no official source was acquired, and Phase 2C has not started. The next separately authorizable action is **Phase 2C — deterministic catalog queries and relationship semantics: set number/name lookup, inventories, spares, minifigures, component expansion, nested-set expansion, matching selections, element/part relationships, containment queries, and the benchmark harness.** Do not begin it automatically. [ExecPlan 020](docs/plans/020-catalog-foundation.md) records actual validation and cleanup.

Brian authorized this bounded acceptance review and one conditional local checkpoint commit; no push is authorized. Phase 2C query completion and Phase 2D official-source feasibility require separate explicit authorization. The dated 2A and Phase 1 sections below preserve their historical scope and next actions.

### Slice 2A implementation history

**2026-09-07 — Slice 2A implementation:** Work started at exactly `293e392e33e06bbcb5d339589fc4e74b903b1315` with an empty index and clean tree. [ExecPlan 020](docs/plans/020-catalog-foundation.md) preserves the approved plan, source findings, D-026 refinements and verification record. Identity/provenance/snapshot and inventory migrations, synthetic fixtures, normalization, relational tests, read grants and package checks are implemented; local verification passed. Changes remain unstaged/uncommitted. The exact next action is **Independent Slice 2A acceptance review and local checkpoint commit**. Neither acceptance nor a commit starts 2B automatically.

The next separately authorizable implementation is 2B's offline parser/staging/import/activation slice. It must add active-pointer and activation-history structures together with atomic transition/concurrency tests. No downloader/parser/staging/COPY/import/promotion/activation code or command belongs to 2A; no provider endpoint was contacted. Official bulk acquisition remains 2D. No pricing, POV, liquidity, valuation, Hunt or catalog UI was implemented.

### Accepted Phase 1 checkpoint history

Current checkpoint: **Phase 1 independent local acceptance passed on Windows on 2026-09-07.** Brian separately authorized final review, bounded corrections and one conditional local completion commit. Review started at exactly 5c57731c7e15abdae5d6d1e5a35e46e602bc3618 with an empty index and precisely 17 modified plus 16 new Slice 1C files; no unrelated changes existed. Slices 1A/1B and D-025 remain accepted history. The completion checkpoint contains only those reviewed files and acceptance documentation. No push, branch/worktree change, provider work or Phase 2 implementation is authorized by this review.

The approved detailed [ExecPlan 000](docs/plans/000-local-foundation.md) is the canonical execution record. It preserves accepted Slice 1A/1B evidence and now records the responsive shell, safe built serving, 21 Node/70 Python/11 React unit tests, 28 real PostgreSQL integration tests, six Chromium scenarios, manual Chrome inspection and local CI validation. Local completion does not establish remote CI confirmation or home-server/production deployment.

Approved selections remain TypeScript 5.9.3 with openapi-typescript 7.13.0, repository-local uv 0.12.10, and ESLint 10.10.0 / @eslint/js 10.0.1 / typescript-eslint 8.69.0. No direct dependency or lockfile changes were needed. The exact next action after the local completion commit is: **Phase 2 planning/implementation for LEGO catalog identities, complete set inventories, parts, colors, minifigure relationships, quantities, alternates, extras, inventory versions, and provider mappings.** Do not begin it automatically. Hosted Ubuntu/Windows CI execution remains deferred until an authorized push permits an actual run.

[Prompt 01](prompts/01_scaffold_foundation.md) remains a reusable plan-only review. Its approved review has occurred; reopening that prompt still does not authorize implementation. Historical realignment checkpoint wording in product/history/security documents and dated decisions records the earlier task; current progress belongs here and in ExecPlan 000. Product and security obligations remain unchanged.

## Phase 1 execution boundaries

| Slice | Authorized scope when separately requested | Required stop |
|---|---|---|
| 1A — Toolchain and workspace | Verify stable toolchain/package compatibility; create workspace/manifests/configuration; resolve exact locks; format/lint/type/orchestration foundations; local lock checkpoint only when explicitly authorized | Report actual checks before database infrastructure, connections, application shells, or CI |
| 1B — Database, API, and contracts | Isolated PostgreSQL development/test infrastructure, guarded tooling, SQLAlchemy/Alembic, health/readiness/OpenAPI, deterministic TypeScript contracts, unit/integration checks | Report before frontend/built-serving/browser/CI completion |
| 1C — Web shell, built serving, CI, and acceptance | Responsive React status shell, Vite proxy, FastAPI static serving, browser tests, GitHub Actions, complete Phase 1 acceptance, permitted documentation | Report and stop before Phase 2 |

Each slice requires a separate explicit implementation authorization. Completing one never authorizes the next. Dependency/tool acquisition requires that slice's explicit local/network scope. No product-provider calls, home access, PWA/Android, domain workflow, or existing PostgreSQL on 5432 belongs to Phase 1.

The original Slice 1A implementation request retained working-tree changes for review. The subsequent acceptance request permits one exact-list local checkpoint only if acceptance passes, with an existing Git identity, complete staged review, and no ignored or unrelated files. Never use blanket staging or force-add ignored files; nothing may be pushed.

## Documentation-update rules during Phase 1 implementation

Read-only by default:

- AGENTS.md
- docs/ORIGINATING_CHAT_SUMMARY.md
- docs/PRODUCT_SPEC.md
- docs/VALUATION_RULES.md
- docs/SECURITY_PRIVACY.md

Change one only for a concrete verified contradiction that cannot be accurately documented elsewhere. Any proposed change must be narrow, evidence-backed, and explicitly reported; routine implementation progress does not qualify. Brian's additional explicit request to plan new/used set part-out values authorizes the additive R-11 and valuation subsection, linked to D-024 and the later part-out plan; it does not authorize feature implementation.

The later explicit D-025 documentation amendment authorizes the necessary product, valuation, model, architecture and Phases 2–8 planning changes for POV/liquidity/opportunity intelligence. Preserve decision history, the Phase 1 plans/prompts and security/deployment/image obligations. Amendment preparation permitted local documentation reads/edits/checks only, without staging or commit. Brian's subsequent acceptance request permits narrow Markdown corrections and one conditional local documentation commit; it permits no application/configuration changes, provider/network contact, dependencies, service/container/database startup, infrastructure access or push.

Normal status updates belong primarily in README.md, CODEX_WORKFLOW.md, docs/PROJECT_CONTEXT.md, docs/ROADMAP.md, docs/REQUIREMENTS_TRACEABILITY.md, docs/LOCAL_DEVELOPMENT.md, and docs/plans/000-local-foundation.md. Update docs/ARCHITECTURE.md only for verified implementation details. Keep future domain schemas and accepted historical decisions intact; record newly accepted decisions additively.

Use repository-relative paths wherever sufficient. Resolve the repository root dynamically rather than hard-coding a machine/user/checkout location. [Local development](docs/LOCAL_DEVELOPMENT.md) records tested Phase 1 setup, frontend/backend checks, resource cleanup, deferred hosted CI and the earlier temporary-cache limitation. Historical unstarted/checkpoint wording in the dated product/amendment documents is historical; current implementation status belongs here and in ExecPlan 000.

## Chat strategy

Use one repository and a fresh chat for each major phase; keep tightly scoped plan review and its separately authorized implementation together where practical. Each chat reads [AGENTS.md](AGENTS.md), [product spec](docs/PRODUCT_SPEC.md), [valuation rules](docs/VALUATION_RULES.md), [traceability](docs/REQUIREMENTS_TRACEABILITY.md), current decisions, roadmap, and relevant ExecPlan.

The [originating summary](docs/ORIGINATING_CHAT_SUMMARY.md) is chronological context. Historical image-first instructions and the starter ZIP never override current decisions. Preserve accepted image contracts in their later module.

## Prompt rhythm

1. Select one phase from [ROADMAP.md](docs/ROADMAP.md), and one explicitly named slice for Phase 1.
2. Establish its entry gate, scope, permitted access, and exclusions.
3. Review the self-contained ExecPlan under [.agent/PLANS.md](.agent/PLANS.md).
4. A plan-only request returns the plan in chat and stops. A documentation/local-Git request changes only its authorized Markdown and reviewed Git checkpoint.
5. Implement only the separately requested slice/phase after required access gates are satisfied.
6. Run applicable verification, inspect the full diff, and report actual evidence and limitations.
7. Stage/commit only on Brian's explicit request; never advance automatically or push implicitly.

Prompt 00 is bootstrap/revalidation. Prompt numbers 01–16 map one-to-one to roadmap phases; 1A/1B/1C are execution slices inside Phase 1, not new numbered phases/prompts. Prompts 13–16 remain optional later image work.

## Model, evidence, and special gates

Use current user-selected settings. Do not spawn subagents unless the user or applicable task instructions explicitly request delegation.

Fixtures prove behavior, not live provider entitlement, rights, or market coverage. Phase 3 resolves provider access/use constraints; Phase 4 proves representative feasibility before supported sourcing is claimed. Slice 1B verified only the official PostgreSQL image and relevant technical documentation. D-024 planning reviewed the public BrickLink manual; D-025 performs no new provider research. No authenticated provider request or live coverage/threshold claim follows from either plan.

Phase 9 requires Android package/physical core-flow evidence. Phase 10 hardens a local release. Phase 11 requires explicit read-only home discovery authorization; Phase 12 requires a distinct reviewed deployment authorization. Prompt 15 cannot claim overlay/Facebook compatibility from a build.

Never broaden localhost to LAN/public access implicitly. Keep secrets out of chat/clients. Preserve unrelated uncommitted work; never use blanket stage/reset/clean to simplify a checkpoint.
