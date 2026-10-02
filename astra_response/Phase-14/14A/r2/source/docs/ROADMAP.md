# Valuation-First Roadmap

## Phase 14A local pilot — 2026-10-02 live result

**Phase 14 IN PROGRESS; READY FOR PHASE 14A REVIEW (partial sample).**
Brian approved USD 10.00 lifetime, ten inference attempts and exact `gpt-6-luna`.
Six requests/eleven approved images were sent; five groups completed. G06 exhausted
2,048 output tokens on reasoning and returned incomplete; G07 was not attempted.
No retry/fallback occurred. Estimated cost USD 0.0036058; actual billing is unknown.
Raw top-1/top-3 agreement is 3/17; catalog coverage is separately three exact sets
resolved and fourteen BrickLink figure labels unresolved. No mapping/import was done.
The frozen sample/labels, private ledger/recovery copy and protected files remain
preserved; development stayed stopped, main is unpushed and its index is empty.
Only affected fixtures/lint/types ran. See [Plan 104](plans/104-recognition-quality-pilot.md),
[pilot results](PHASE_14A_PILOT.md) and [provider decision](PHASE_14A_PROVIDER_DECISION.md).
Manual continuation requires an explicit output/reasoning and retry decision.
Phase 13 remains CLOSED. Earlier checkpoints below are historical.

## Phase 13 final closeout — 2026-10-01

**Phase 13A / 13B / 13C: ACCEPTED / CLOSED.
Phase 13 — Marketplace Listing Intake + Images: ACCEPTED / CLOSED.
Phase 14: NEXT / NOT STARTED.** [Plan 103](plans/103-phase-13-image-ingestion.md)
is CLOSED. Accepted evidence is [13C implementation r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/0d010531c122165ec8ec45a58e740c7e4c6853dd/astra_response/Phase-13/13C/r1/REVIEW.md)
and the [schedule addendum](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/30392cfb7f60edd4a6e0f3360ddda66903b37abc/astra_response/Phase-13/13C/r1/backup-schedule.md).
The approved privacy policy and dated implementation evidence remain preserved.

Accepted deployment: `phase13c-marketplace-intake-r1`, `0017_listing_images`,
catalog generation 1 / 28,278 sets. Its immutable manifest/source identity remains
unchanged. The separate [backup schedule](BACKUP_SCHEDULE.md) is daily 04:00
America/Chicago with zero randomized delay, unchanged Persistent behavior and
server timezone; its change caused no additional backup or API interruption.
Image-inclusive backups still temporarily pause the API. The existing Android APK
was not rebuilt. This documentation/Git closeout commits the accepted 22-file
inventory locally, leaves main unpushed and preserves protected dirty bytes.
No operational or testing qualification is repeated. Phase 14 has not started;
all earlier dated status below is historical.

## Historical Phase 13C production delivery — 2026-10-01

**Phase 13A and 13B ACCEPTED / CLOSED. Phase 13C IMPLEMENTED / READY FOR FINAL REVIEW.
Phase 13 IN PROGRESS pending final review; Phase 14 NOT STARTED.**
Accepted 13B local checkpoint is `1c7501092e7fad92a5471fa5571c6d009a1b0c3f`,
`Implement Phase 13B marketplace intake UI`. Brian approved the
[image privacy and retention policy](IMAGE_PRIVACY_POLICY.md) and bounded production delivery
under [Plan 103](plans/103-phase-13-image-ingestion.md). Marketplace Listings are private sourcing records;
Add Marketplace Listing never publishes to an external marketplace.

The immutable `phase13c-marketplace-intake-r1` release is active with
`0017_listing_images`, enumerated runtime grants and private Linux blob storage.
The normal backup path supports legacy three-artifact sets and complete four-artifact
image sets, with a settled API pause and one exported database snapshot. One
pre-migration dual backup and its supported guarded proof preceded activation.
The one retained synthetic intake passed with three images/receipts, and its same
four-artifact dual backup passed independent Windows Drive-only restore: all 82
counts, six blobs, image/catalog/user context, ownership/grants and SCRAM matched.
Disposable recovery was cleaned; all 14 final checks passed, normal timers active,
zero failed units. The combined backup service interval was 376 seconds with a
controlled API pause through capture/readback. The accepted Android APK was not
rebuilt or claimed updated; providers, recognition/native capture and datasets did
not start. The r1 review package is ready for independent final review. Main is unpushed; 13C
changes stay uncommitted with empty index and protected bytes unchanged.

Earlier dated sections remain historical and are superseded by this checkpoint.

## Phase 13B accepted closeout — 2026-10-01

**Phase 13A ACCEPTED / CLOSED; Phase 13B ACCEPTED / CLOSED; Phase 13 IN PROGRESS;
Phase 14 NOT STARTED.** Accepted 13A r1 is checkpointed locally as
`d14002e244434123dc68b57aefda004a00aa8e89` (`Implement Phase 13A image ingestion backend`).
[Plan 103](plans/103-phase-13-image-ingestion.md) now governs explicitly authorized private Listings UI and
bounded two-file upload queue. Production/privacy shipping remains separately
authorized Phase 13C. Proposed retention policy is unapproved. Main is unpushed;
Accepted 13B is checkpointed locally; index empty and protected files unchanged.
Earlier 13A status below is historical. No recognition, native capture or deployment.


## Phase 13A authorized source implementation — 2026-10-01

**Phase 13A IMPLEMENTED / READY FOR REVIEW; Phase 13 IN PROGRESS;
Phase 14 NOT STARTED.** Phase 12 and P12-05 remain ACCEPTED / CLOSED.
[Plan 103](plans/103-phase-13-image-ingestion.md) implements only the optional
backend/data/storage foundation. Direct lookup and financial modules remain
independent of images. The [privacy/retention proposal](IMAGE_PRIVACY_POLICY.md)
still requires Brian's shipping approval. Focused synthetic/disposable validation
is distinct from production, browser upload UI, Android and recognition evidence.
Phase 13B upload UI is deferred and separately authorizable after 13A review.

## Phase 12 final closeout — 2026-10-01

**P12-05: ACCEPTED / CLOSED. Phase 12: ACCEPTED / CLOSED.
Phase 13: NEXT / NOT STARTED.** Brian independently accepts
[final r5 evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/57dec1e5f7b0538c75f2a17a824c15aba3083dc2/astra_response/P12-05/r5/REVIEW.md) at 57dec1e5f7b0538c75f2a17a824c15aba3083dc2.
[Plan 099](plans/099-phase-12-production-acceptance.md) is CLOSED;
[Plan 102](plans/102-manual-deal-economics-admission-repair.md) is
CONTRACT REVIEW COMPLETE / CLOSED — NO REPAIR REQUIRED.

The accepted production baseline is `p12-05-catalog-repair-r1`, migration
`0016_hunt_cached_runs`, catalog generation 1 / 28,278 sets. R5 qualifies
the populated FINAL backup through independent Windows Google Drive-only
recovery, exact restored-state comparison and complete disposable cleanup.
Those accepted results are reused here; this closeout performs only
documentation/Git validation. Prior dated blocker/resume evidence is retained
below. Closure does not authorize or start Phase 13.


## Final populated Drive recovery — 2026-10-01

P12-05 IMPLEMENTED / READY FOR FINAL ACCEPTANCE; Phase 12 READY FOR FINAL
ACCEPTANCE; Phase 13 NOT STARTED. The remaining real populated final-backup
recovery proof passed via independent Windows Google Drive-only recovery into
off-host isolated PostgreSQL 18. Production comparison, ownership/least privilege,
catalog audit and cleanup matched; disposable recovery resources were removed
and production stayed healthy. R4 gates remain accepted and were not repeated.
[Plan 099](plans/099-phase-12-production-acceptance.md) records r5. Final acceptance
and main closeout remain pending; this status starts no subsequent phase.


## Final P12-05 acceptance ready for review — 2026-10-01

**READY FOR P12-05 / PHASE 12 FINAL REVIEW. Phase 12 IN PROGRESS pending independent
acceptance.** Gates 1-7 reused; corrected Gate 8 immutable r6 rollback and exact
catalog-repair forward return passed, including authenticated exact probe persistence.
VM115-only real graceful cold stop/start passed after actual VM112-before-115
startup-order verification. The probe is removed, Settings restored, no saved
forecast exists, zero valid sessions, and THIS continuation's just-revoked replay
returned 401/no-store. Exactly one final normal dual backup passed all three
artifacts/six encrypted readbacks/both repositories. Final security/operations,
immutable/installed byte checks, deep health, retention and network exposure PASS.
[Plan 099](plans/099-phase-12-production-acceptance.md) records the evidence and limits. Plan 102 remains CLOSED —
NO REPAIR REQUIRED. Prior r3/r2/r1 remain dated history; final sanitized review is
`astra_response/P12-05/r4/`. Main stays uncommitted/unpushed at e64f2d8, index empty,
protected dirty bytes unchanged. No source/schema change, provider activation,
broad tests, Phase 13 or final human acceptance is implied.


## P12-05 current stop at Gate 8 — 2026-10-01

**BLOCKED — required immutable rollback operational compatibility. Gates 1-7 PASS;
P12-05 and Phase 12 remain IN PROGRESS.** Production PWA and physical Android
acceptance passed with the documented evidence limits. The required `p12-04d-r1`
rollback lacks scripts used by installed health, retention, Python-maintenance
and alert services, and its renewal hook conflicts with the health equality
contract. No pointer change or rollback was attempted; the repaired release
remains installed. The temporary Watchlist is removed, Settings restored, Android
signed out, PWA at sign-in, and no valid owner session or saved forecast exists.
New-token replay remains unexercised; accepted earlier Windows replay 401 is reused.
VM recovery, final backup (zero invocations) and final operations acceptance remain
pending. [Plan 099](plans/099-phase-12-production-acceptance.md) records the blocker, evidence and next reviewed
compatibility disposition. Gate 5 and Plan 102's no-repair closure remain accepted.
Prior r2/r1 evidence stays preserved; sanitized blocked review goes to
`astra_response/P12-05/r3/`. Main stays uncommitted/unpushed with empty index and
unchanged protected dirty bytes. Earlier status below is dated history.


## P12-05 Gate 5 correction and continuation — 2026-10-01

**Gate 5 PASS; manual economics diagnostic CLOSED — NO REPAIR REQUIRED.
P12-05 IN PROGRESS / RESUMABLE FROM GATE 6; Phase 12 IN PROGRESS.**
Brian accepted the manual-economics r1 diagnosis and corrected the acceptance
criterion: MANUAL selects sale price after qualified valuation admission. The
observed production UNKNOWN/null full economics conforms to frozen V1; no bug,
V2, replay change, application repair or new deployment is warranted.
[Plan 099](plans/099-phase-12-production-acceptance.md) records accepted Gates 1-5 and ordered PWA, physical Android, immutable
recovery, cleanup, one final dual backup and operations/review continuation.
Plan 102 is CONTRACT REVIEW COMPLETE — NO REPAIR REQUIRED. Prior r2/r1 pause
evidence and all earlier dated prose remain preserved and superseded as status.
Ordinary unsaved previews follow normal expiry/cleanup; no unsafe deletion or
forced row-count-zero criterion applies. No market activation or Phase 13.
Main remains uncommitted/unpushed, index empty and protected dirty bytes intact.

## P12-05 remaining acceptance stop, 2026-09-30

**Catalog importer repair and production catalog activation prerequisite ACCEPTED /
CLOSED. P12-05 BLOCKED — Gate 5 manual Deal Economics admission; Phase 12 IN PROGRESS.**
From accepted main `e64f2d812bf90255005c88e8d1f68b4c8ab0d7af`, the real fresh-profile
owner session/security checks, Windows shell/search/detail/Settings, and unique
temporary Watchlist create/update/persistence passed. The manual-sale forecast
preview received the explicit price but returned null sale/net/profit/ROI because
the existing v1 backend requires supported market evidence before selecting MANUAL.
[Plan 099](plans/099-phase-12-production-acceptance.md) records the exact stop.
No application repair, provider activation, schema/configuration change or deployment
was performed. A repair requires separate authorization and replay/version review.

Settings defaults were restored, the temporary Watchlist item removed, and the
browser signed out; old-session replay returned 401. One unsaved preview remains
under normal expiry/cleanup rules, so complete temporary-data cleanup is not claimed.
PWA, physical Android, rollback/forward, VM stop/start, final backup and final
operations qualification remain unrun. The blocked review is published separately
under `astra_response/P12-05/r2/`; main remains uncommitted/unpushed, index empty,
and protected dirty files unchanged. Earlier sections retain dated history.

## Accepted repair closeout, 2026-09-30

**Catalog importer repair ACCEPTED / CLOSED. Production catalog activation
prerequisite BLOCKED pending separately authorized production recovery/retry/activation.
P12-05 BLOCKED; Phase 12 IN PROGRESS.** Brian accepted the
[r2 repair package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/REVIEW.md)
and authorized only the exact 15-file local closeout checkpoint and r3 publication.
Reuse accepted r2 qualification; this closeout performs no live connections,
tests, builds, production recovery/retry/activation or candidate release install.
Remaining P12-05 client/device gates stay blocked. The implementation scopes,
repository snapshots and review-ready statements below are dated pre-closeout history.

## P12-05 catalog repair review, 2026-09-30

**Catalog importer repair IMPLEMENTED / READY FOR REVIEW. Catalog prerequisite
BLOCKED pending repair acceptance; P12-05 BLOCKED; Phase 12 IN PROGRESS.**
[Plan 101](plans/101-catalog-importer-performance-repair.md) proves the exact
inventory_lines:parts timeout and narrow atomic 100,000-row span repair, one full
retained-source import and clean repeat at unchanged 300000/10000 ms limits,
independent semantic equality and truthful guarded retirement/explicit linked retry.
Focused tests, normal package/release proof and final unchanged production checks
passed. No migration or production recovery/retry/activation/deployment occurred.
Main remains uncommitted/index empty; protected files unchanged. R2 review evidence
does not authorize the concrete future production continuation recorded in
[Plan 100](plans/100-production-catalog-activation.md). Remaining Plan 099
client/PWA/Android/rollback/cold-start gates remain unrun; Phase 13 did not start.
The following stopped-attempt and closeout sections remain dated history.

## P12-05 catalog prerequisite stopped, 2026-09-30

**Catalog prerequisite BLOCKED — production import statement timeout.
P12-05 BLOCKED; Phase 12 IN PROGRESS.** Brian authorized catalog-only activation
in [ExecPlan 100](plans/100-production-catalog-activation.md). Retained official
source integrity/rights, guarded wrapper validation and the sole pre-import dual
backup passed. The existing importer then failed during canonical build under its
unchanged five-minute statement timeout. Failed audit, candidate and all staging
rows remain; canonical sets and accepted/active snapshots remain zero. No activation,
retry, timeout change or post-activation backup ran. Read-only stopped-state health,
security and operations passed. A separate narrow importer root-cause repair and
reviewed failed-state recovery are needed before another production attempt.
Main remains uncommitted with empty index and protected dirty files unchanged.
Remaining Plan 099 gates remain unrun; earlier sections are dated history.

## P12-05 authorized acceptance, 2026-09-30

**P12-05 BLOCKED — production catalog unavailable. Phase 12 IN PROGRESS.**
Brian authorized [ExecPlan 099](plans/099-phase-12-production-acceptance.md)
for real production client, restore, rollback and VM cold-start acceptance.
Preflight, one fresh dual backup, independent Google Drive-only restore and
cleanup passed. All 76 restored table counts and effective grants matched, but
production has zero catalog sets and no active accepted snapshot; installed
number/name search returns `catalog_unavailable`. Client, rollback, cold-start
and final-backup gates remain unrun. Separate catalog activation review is needed.
No application source fixes or main commit/push are authorized by this slice.
The closeout status below is historical and is superseded by this authorization.

## P12-04E / P12-04 accepted closeout, 2026-09-30

**P12-04E ACCEPTED / CLOSED. P12-04 ACCEPTED / CLOSED.
Phase 12 IN PROGRESS. P12-05 NEXT / NOT STARTED; not authorized by this closeout.**
Brian accepted the [published r1 package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/6f06662b394471aaef2a136c59d7ed4f3becd676/astra_response/P12-04E/r1/REVIEW.md).
[ExecPlan 098](plans/098-production-operational-hardening.md) records the accepted complete-run
30 daily / 8 weekly / 12 monthly retention and permanent foundational pins,
disposable destructive tests, first live PLAN keep=3/delete=0 and APPLY NOOP,
private Gmail SMTP TEST acceptance, operational failure alerts, light/deep health,
Python 3.13.15 CURRENT at evidence time, standard Ubuntu security maintenance
without automatic reboot, and deliberately absent ACME contact with independent
renewal/deploy/expiry notifications. The accepted immutable release is p12-04e-r6.
VM 115 onboot=1/startup order=2 and one controlled guest reboot passed with all
required services/timers, reserved address and trusted HTTPS; zero failed units.

P12-04A runtime/storage, B dual recovery, C database/owner/recovery-point activation,
D private HTTPS and E operational hardening are all CLOSED. This closes production
deployment only. Closeout reuses r1 evidence; no live connections, tests, lint,
type checks, builds, alerts, retention or reboot are rerun. The exact 28-file local
checkpoint uses `Close P12-04 production deployment`; main is not pushed and the
three protected dirty files remain unchanged and unstaged.

P12-05 retains real owner/session/cookie/security acceptance, full browser/PWA,
physical production Android, real off-host Google Drive restore, immutable rollback
and forward return, end-to-end disaster recovery, and final security/operations
review. Guest-local alerts cannot report loss of VM 115 or the whole Proxmox host;
the guest reboot is not Proxmox host-boot recovery evidence. Both limitations carry
into P12-05. No host-level monitor or destructive host-boot test is added here.
Earlier checkpoint sections are historical; Phase 12 is not complete.

## P12-04D accepted closeout, 2026-09-29

[ExecPlan 097](plans/097-private-https-application-activation.md) records the stable
DHCP reservation/private DNS, normally trusted DNS-01 certificate and renewal,
immutable `p12-04d-r1`, active loopback API/Caddy and private-LAN UFW policy.
Windows HTTPS and synthetic Android-Origin HTTP smoke passed. P12-04D is
**ACCEPTED / CLOSED**. P12-04 remains IN PROGRESS; P12-05 is
NOT STARTED. Earlier checkpoints below are historical.

Brian accepted the [accepted r1 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/REVIEW.md). This closeout reuses that evidence without live, test or build reruns. The next P12-04 operational-hardening checkpoint is NEXT / NOT STARTED. Plan 097 retains all P12-04 and P12-05 gates; the absent ACME contact email is an operational note, and the unrelated legacy backup identity is not a deployment blocker.

## P12-04C accepted closeout, 2026-09-29

**P12-04C is ACCEPTED / CLOSED**, recorded in [ExecPlan 096](plans/096-production-database-activation.md). The corrected `p12-04c-r4` runner uses accepted root-to-postgres peer authentication and retains `NoNewPrivileges=true`. Offline custody, both real dual backups and readbacks, the generated migration proof, migration to `0016_hunt_cached_runs`, runtime grants, one owner bootstrap and independent admin verification passed. The daily backup timer is enabled/active, both real runs and synthetic canaries remain, and the API is disabled/inactive with PostgreSQL loopback-only. P12-04 remains IN PROGRESS; P12-04D is NEXT / NOT STARTED; P12-05 is NOT STARTED. Production exposure/operations and P12-05 acceptance gates remain open.

Brian accepted the [r2 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/REVIEW.md). Closeout reuses that evidence without live/test/build/recovery reruns. The full remaining-gate list stays open in Plan 096. Earlier checkpoint sections below are historical.

## P12-04B accepted closeout — 2026-09-29

**P12-04B is ACCEPTED / CLOSED after review of the
[r1 dual-recovery package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f179992addabb2fc7eb666280c2b218ba1474bfb/astra_response/P12-04B/r1/REVIEW.md).
P12-04 remains IN PROGRESS; P12-04C is NEXT / NOT STARTED; P12-05 has not
started.** [ExecPlan 095](plans/095-dual-recovery-foundation.md)
records separately encrypted Proxmox supplemental and Google Drive off-host
repositories. Windows independently restored and verified the synthetic canary
from both. Production backup source and inactive unit definitions are prepared;
no production database, application service, proxy or timer is active. Backup/admin
receipt integration and offline recovery credential custody are hard pre-migration
gates for P12-04C.

## P12-04A accepted closeout — 2026-09-29

**P12-01/P12-02/P12-03 are CLOSED; Phase 12 and P12-04 are IN PROGRESS;
P12-04A is ACCEPTED / CLOSED; the next P12-04 checkpoint and P12-05 are NOT
STARTED.** VM 115 is
running with `onboot=0`, a dedicated ext4 PostgreSQL data mount, PostgreSQL
18.6 bound to loopback, versioned source-built Python 3.13.15 and uv 0.12.10. The
packaged API wheel and web release are staged; the API unit is disabled and
serves no traffic. [ExecPlan 094](plans/094-production-foundation.md) records
the foundation and validation. Production database creation, secrets, backups,
DNS, certificates and TLS remain later P12-04 work. The
[accepted r1 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/22f80286b1b82d7862b922fe2d66fd06fa84cf9b/astra_response/P12-04A/r1/REVIEW.md)
closes only P12-04A. Resolve VM `onboot=0` deliberately before Phase 12 closes.
The accepted P12-03 closeout below remains historical.

## P12-03 accepted closeout — 2026-09-29

**P12-03 ACCEPTED / CLOSED** after ChatGPT reviewed the
[r2 base-VM package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/a9023bcc6a2c933938465b18f79787041499f9f3/astra_response/P12-03/r2/REVIEW.md).
P12-01/P12-02 remain CLOSED; Phase 12 remains IN PROGRESS; **P12-04 is NEXT /
NOT STARTED**. The dedicated Ubuntu VM remains stopped, with the 128-GiB
data disk unused and no installer media. The r2 implementation record and
r1 partial checkpoint below are historical. No BrickVault deployment,
production PostgreSQL, Python 3.13/uv runtime, Caddy, DNS/certificate,
backup, production database/secrets or provider credentials exist on VM 115.
All P12-04/P12-05 gates remain unchanged.

## P12-03 r2 review-ready snapshot — 2026-09-29

**Historical pre-acceptance status: P12-03 IMPLEMENTED / READY FOR REVIEW;
not CLOSED.** The dedicated VM 115
has Ubuntu Server installed from the verified 24.04.2 ISO on the 32-GiB OS
disk and updated from official Ubuntu repositories to 24.04.5 LTS.
Administrator key-only SSH, sudo, conservative SSH hardening, time sync,
standard updates and QEMU guest-agent passed validation. The 128-GiB data
disk is untouched by both guest and stopped-host checks. VM 115 is stopped,
`onboot=0`, booting from `scsi0`, with installation media detached and the
task-owned seed removed. [ExecPlan 093](plans/093-base-vm-provisioning.md)
holds the execution and evidence. The earlier blocked/manual entry below is
historical. P12-01/P12-02 remain CLOSED; Phase 12 remains IN PROGRESS;
P12-03 awaits ChatGPT review. No P12-04 work was done or authorized.

## P12-03 partial provisioning for review — 2026-09-29

**P12-03 BLOCKED — MANUAL INSTALLER STEP REQUIRED.** Brian authorized the
base VM slice. Fresh repository, host/capacity/bridge/VMID and authoritative
Ubuntu ISO checksum gates passed. VM 115 and its fresh EFI, 32-GiB OS and
128-GiB data volumes, one untagged vmbr1 NIC and verified ISO are provisioned
for review. The VM remains stopped with onboot disabled; the data volume has
no partitions, filesystem/LVM signature or mount. Browser console access
failed on the management certificate, so Ubuntu and administrator SSH are
not installed/established. [ExecPlan 093](plans/093-base-vm-provisioning.md) records exact resources,
checks, the manual installer handoff and rollback boundary. Legacy VM 107 and
all existing guests remain unchanged. P12-01/P12-02 stay CLOSED; Phase 12 is
IN PROGRESS; P12-03 is not CLOSED and no P12-04 work occurred. Earlier dated
P12-03 NEXT / NOT STARTED entries below are historical.

## Phase 12 P12-02 accepted closeout — 2026-09-29

**Phase 12 IN PROGRESS; P12-02 ACCEPTED / CLOSED; P12-03 NEXT / NOT
STARTED.** ChatGPT accepted the published
[`r1` infrastructure review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/639b10dc483da27d85cd983b204d281e218b5b6c/astra_response/P12-02/r1/REVIEW.md).
[ExecPlan 092](plans/092-exact-infrastructure-pre-mutation-review.md) now
limits P12-03, when separately authorized, to the dedicated VM and base
Ubuntu installation. Fresh VMID, capacity and bridge checks and an
authoritative ISO SHA-256 match precede any mutation. Temporary DHCP and
key-only admin SSH are permitted; the data disk remains unformatted.
Encrypted Proxmox and Google Drive database copies, private DNS/certificate,
production runtime/database/admin tooling and live-client/restore acceptance
remain P12-04/P12-05 gates. P12-02 acceptance itself authorizes no mutation.

## Phase 12 P12-02 infrastructure review snapshot — 2026-09-29

**Historical pre-acceptance status: Phase 12 was IN PROGRESS; P12-01 was
ACCEPTED / CLOSED; P12-02 was AUTHORIZED / IN REVIEW; P12-03–05 were not
authorized.** A bounded read-only Proxmox pass succeeded and selected a
conditional dedicated VM topology in
[ExecPlan 092](plans/092-exact-infrastructure-pre-mutation-review.md). Backup
access/restore, private DNS and the ordinary certificate path, approved
address/firewall sources, and pinned production runtime packages remain
blockers. Brian selected a future Google Drive folder named
`Brickvault_Apprisal_App_Backup` for encrypted off-host logical backups and
selected a second encrypted database copy on existing Proxmox. Brian approved
`appraisal.abrianbaker.com` for planning; no job, folder or DNS change was
made. No deployment mutation or live client/restore proof occurred. The
P12-01 checkpoint below records its 2026-09-28 status.

## Phase 12 P12-01 source checkpoint — 2026-09-28

**Phase 10 CLOSED; Phase 11 CLOSED; Phase 12 IN PROGRESS. P12-01 is ACCEPTED /
CLOSED; P12-02 is NEXT / NOT STARTED.** The production runtime and Android HTTPS
source/local preflight in [ExecPlan 091](plans/091-production-runtime-and-deployment.md)
is accepted. No infrastructure deployment occurred. The configured Proxmox
target remains a placeholder, so actual host capacity, storage/network
inventory and off-host backup facts still gate placement. The exact hostname,
private DNS/TLS path, data/bootstrap policy and secrets remain open. Real
Caddy/TLS and normal-certificate browser/PWA/Android acceptance, plus off-host
restore, remain later gates. Phase 9 localhost TEST transport is not production
evidence. P12-02 and later infrastructure or production mutation require
separate review and explicit authorization. PostgreSQL is never public.

## Phase 11 discovery checkpoint — 2026-09-28

**P11-01 is ACCEPTED / CLOSED; Phase 11 is CLOSED. At this historical closeout,
Phase 12 was NEXT / NOT STARTED; P12-01 now governs above.** The accepted
read-only pass and conditional Phase 12 topology are
in [ExecPlan 090](plans/090-home-infrastructure-discovery.md). Proxmox node,
backup and proxy details remain unverified where configured access was absent.
Phase 12 requires separate explicit authorization before any infrastructure
or production change.

## Phase 9 closed — 2026-09-26

**Phase 9 is CLOSED.** All four slices and the governing physical Android gate
are accepted. Final run `47b0c2d3f3c94daa92188b5eab34d905` used the unchanged
accepted APK (SHA-256
`67e2f4caa79441dbfa1b7df42a747e50217ee3fd24e7da7b7dc657920d80fdaf`)
and localhost TEST certificate SHA-1
`53DC8EF2A454BF022A5D1EB0881DEB2F33DC99C1`.

The accepted device evidence covers shared search/detail/deal and saved-work
flows, direct TLS and exact Host/Origin/CORS, authentication/session/CSRF,
read-only offline memory, explicit reconnect verification, session expiry,
fresh-process privacy, all five market-evidence expiry profiles, and the
one-shot uncertain Watchlist mutation. The uncertain write committed once at
revision 1, was not replayed, and reconciled by authoritative readback. Server
deadlines controlled evidence display; expired observations were not revived.
No live provider was contacted. Qualification resources were cleaned up.

**Phase 10 — Local release and security hardening is NEXT / NOT STARTED.**
No Phase 10 implementation or deployment is authorized by this closeout.

## Historical Phase 9 physical Android qualification boundary — 2026-09-25

**The accepted physical Android core, auth, saved-work, offline/reconnect,
session-expiry and fresh-process privacy checks have passed; Phase 9 remains
OPEN.** No live provider was contacted, and qualification resources were cleaned
up. Details are in [ExecPlan 088](plans/088-android-https-auth-source.md).

The only unqualified physical gates are market/evidence expiry and deterministic
uncertain Watchlist mutation/sync-conflict behavior. TEST-only deterministic
controls are recorded in ExecPlan 088; they do not themselves satisfy the
physical gate. Phase 10 local release hardening follows only after these two
checks pass. Older physical-not-started statements are historical.

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
[ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md) authorizes an online
PWA, public-shell-only persistence and bounded Capacitor feasibility. Slice 2
private memory views/reconnect and Slice 3 physical Android remain unstarted.
Earlier Phase 9 prohibitions below are superseded only for this slice. No phase
closure/commit/deployment; 7B/7C/bounded 8 remain closed, R-07/R-36 partial and
Phase 16/Deferred Economics boundaries unchanged.

## Phase 8 bounded source milestone accepted / closed — 2026-09-23

**Phase 8 is ACCEPTED / CLOSED FOR ITS BOUNDED SOURCE MILESTONE; Slice 2 is
ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT.**
[ExecPlan 084](plans/084-hunt-frozen-evidence-context.md#source-checkpoint-acceptance--2026-09-23)
records Brian's technical and visual acceptance. Slice 1's cached whole-set runs,
transparent financial ordering, immutable history and qualification/freshness,
together with Slice 2's frozen bounded component context, satisfy that milestone.

Full R-36 remains PARTIAL. Composite ranking, Gem policy, broader distribution/
calibration policy and future calibrated weighting remain policy-dependent. Seller
concentration, global rarity and duration-dependent velocity/months-supply/absorption
without authoritative observation duration remain unsupported. POV premium, scoped
catalog-presence integration and theoretical gross target-coverage prefix remain
undelivered. Recovery/burden, expected recovery, recoverable-gross value density,
economic break-even lots and all Deferred Economics Extensions remain deferred and
unsatisfied, without cancellation or implicit phase assignment.

Phase 9 cache/sync is the next major phase, NOT STARTED / NOT AUTHORIZED; no planning
or implementation starts here. Phase 16 outcomes remains separate. Earlier open
Phase 8 entries are historical and do not reopen this accepted bounded milestone.

## Phase 8 bounded source milestone — Slice 2 IN PROGRESS, 2026-09-22

Brian accepted the R-36 review and [bounded milestone decision](DECISIONS.md#phase-8-bounded-milestone-and-frozen-evidence-context--2026-09-22):
cached whole-set screening, transparent financial sorting, immutable history,
explicit qualification and bounded existing component evidence. Slice 1 and 7B/7C
remain CLOSED. [ExecPlan 084](plans/084-hunt-frozen-evidence-context.md) authorizes
only Frozen Evidence Context; Phase 8 remains IN PROGRESS pending later acceptance.

The broad Phase 8 scope/acceptance below is narrowed by this decision, not erased.
Full R-36 remains PARTIAL. Composite scoring is not required. Unsupported duration,
seller/global-rarity evidence, Gem/ranking/distribution policy, undelivered premium,
scoped presence and theoretical target prefixes remain outstanding. Recovery/burden,
recoverable density, economic break-even lots and every Deferred Economics Extension
remain unsatisfied and outside this milestone, without a new delivery phase.

Slice 2 is implemented and self-reviewed, awaiting technical/visual acceptance.
Its validation and unchanged financial/legacy boundaries are recorded in ExecPlan 084.

## Phase 8 Slice 1 source checkpoint accepted / closed — 2026-09-22

**Slice 1 is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 8 remains
IN PROGRESS. Phase 7B and Phase 7C remain CLOSED.** [ExecPlan 083](plans/083-hunt-cached-whole-set-run.md)
records technical and four-image visual acceptance. Earlier Phase 8 unstarted
statements describe prior checkpoints. R-08/R-36 remains partial.

Next is a focused review/planning decision: distinguish requirements honestly
supported by existing evidence, calibration/policy needs, unavailable evidence
and overlap with explicitly Deferred Economics Extensions. Composite/calibrated
ranking, Gem/rarity/competition/burden and unsupported components remain unresolved
or deferred under governing scope. Do not assume a composite score is required or
invent weights. Extensions remain outstanding, deferred, unsatisfied and without a
delivery phase. Phase 9 cache/sync and Phase 16 outcomes remain separate. No later
implementation follows this local source checkpoint.

## Phase 7C source checkpoint accepted / closed — 2026-09-22

Slices 1–4 are ACCEPTED / CLOSED FOR THEIR SOURCE CHECKPOINTS, and Phase 7C is
ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT. [ExecPlan 082](plans/082-notes-source-urls.md)
records Slice 4's implementation, technical evidence, five accepted screenshots and
the authentication-fixture classification. The original 149 passed / 6 failed web
run reproduced at the Slice 3 baseline because existing auth mocks returned null for
the newly required settings resource; the actual absent-settings contract returns
revision-zero defaults. A focused four-file selection passed 44/44 after the
test-only mock correction; the full web suite was not rerun.

Phase 8 Hunt is the next roadmap phase and remains unstarted and unauthorized.
Deferred Economics Extensions remain outstanding, deferred, unsatisfied and without
an assigned delivery phase; they are not a Phase 7C gap. No development migration,
provider/account/device operation, deployment or push occurred.

## Phase 7C Slice 4 authorized and in progress — historical status, 2026-09-21

At implementation authorization, Brian authorized the bounded Notes and Source
URLs implementation in [ExecPlan 082](plans/082-notes-source-urls.md), followed by
technical and visual review. This authorization-time status is superseded by the
source-checkpoint acceptance above.

## Phase 7C Slice 3 accepted source checkpoint - 2026-09-21

**Settings and Selling Profiles is ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT.**
[ExecPlan 081](plans/081-settings-selling-profiles.md) records the accepted
implementation, evidence and local checkpoint. Phase 7C remains IN PROGRESS.
Phase 7B and 7C Slices 1/2 remain CLOSED. **Notes / Source URLs is the next planned
slice; it is not started or authorized by this checkpoint.** Phase 8 and Deferred
Economics Extensions are unchanged.


## Phase 7B source checkpoint accepted / closed — 2026-09-18

**7B-4 is ACCEPTED / CLOSED; Phase 7B is ACCEPTED / CLOSED FOR ITS SOURCE
CHECKPOINT.** The [governing-criteria reconciliation](plans/077-forecast-revisions.md#source-checkpoint-acceptance-and-phase-7b-reconciliation--2026-09-18)
uses accepted 7B-1–4 authentication, exact replay, original save/reopen and revision
evidence. No in-scope source criterion remains unmet. Brian accepts all three
7B-4 checkpoints and the six visuals with their real TEST versus mocked provenance.

Next is **7C planning, separately authorized and NOT STARTED**. Watchlist,
persistent targets/settings and Saved Deal Index remain 7C; Phase 7 overall remains
incomplete and Phase 8 is unchanged. Deferred Economics Extensions remain
outstanding, deferred, unsatisfied and without an assigned delivery phase.
Development migration, actual-account provisioning, deployment and device/HTTPS
qualification remain separate, unperformed operational work. This local source
closeout authorizes no push or later work. Earlier dated open/pending entries below
remain historical; their current-status wording is superseded by this record.

## Phase 7B-4 Checkpoint 1 in progress — 2026-09-18

Brian authorizes [ExecPlan 077](plans/077-forecast-revisions.md) Checkpoint 1 only:
internal persistence and append authority, focused synthetic disposable TEST checks
and self-review, then technical review. 7B-1–3 remain CLOSED; 7B-4 is IN PROGRESS,
not accepted, and Phase 7B remains OPEN. Public API/contracts and editor/navigation
are subsequent checkpoints. No deployment, actual-account/provider operations or
Git checkpoint. 7C and Phase 8 are unchanged; Deferred Economics Extensions remain
outstanding, deferred, unsatisfied and without an assigned delivery phase.

## Phase 7B-3 source checkpoint accepted / closed — 2026-09-18

Brian accepts the full save/reopen source checkpoint and targeted fixture correction
in [ExecPlan 076](plans/076-save-original-forecast.md), including completed visual review.
**7B-3 is ACCEPTED / CLOSED; 7B-1/7B-2 remain CLOSED; Phase 7B remains OPEN.** Next is
separately authorized 7B-4 planning, not started by this local closeout. The settled
private historical-retention decision remains in force. No deployment, operational or
physical-device qualification is implied. 7C, Phase 8 and Deferred Economics Extensions
retain their boundaries; extensions remain outstanding, deferred, unsatisfied and
without an assigned delivery phase. Earlier checkpoint-only and permission-gate entries
below preserve their historical context.

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

## Phase 7B-2 source checkpoint accepted / closed — 2026-09-17

**7B-2 is ACCEPTED / CLOSED for its source checkpoint.** 7B-1 remains CLOSED;
Phase 7B remains OPEN. Brian accepted the implementation and recorded validation.
This is not deployment or operational qualification. The next boundary is the
retention/display-permission review **before 7B-3**. Provider-backed persistence
remains blocked pending that determination; permission is neither established nor
prohibited. No permission research or later-slice work is authorized by this closeout.

Acceptance and the unchanged 16-file inventory are recorded in [ExecPlan 075](plans/075-exact-snapshot-replay.md).

7C, Phase 8 and all Deferred Economics Extensions remain unchanged. The extensions
remain outstanding, deferred, unsatisfied and without an assigned delivery phase.
Earlier pending-review/no-commit entries below preserve their historical checkpoints.

## Phase 7B-2 — implemented, technical review pending, 2026-09-17

[ExecPlan 075](plans/075-exact-snapshot-replay.md) adds internal exact financial
capture/replay with preserved historical qualification assertions. Synthetic replay
does not establish full evidence reconstruction or provider retention/display rights.
7B-1 remains CLOSED; 7B-2 and Phase 7B are not accepted/closed. No later slice starts.
7C and Phase 8 retain their existing scope; Deferred Economics Extensions remain
outstanding, deferred, unsatisfied and without an assigned delivery phase.

## Phase 7B-1 source checkpoint closed — 2026-09-17

[7B-1 Brian-only authentication](plans/074-brian-only-authentication.md) is
**ACCEPTED / CLOSED** for the local source checkpoint, with the documented
nonblocking signed-in-header manual-review limitation. Phase 7B remains **OPEN**.
**Next: 7B-2, not authorized.** Provider-backed historical persistence still requires
resolution of retention/display permission. All Deferred Economics Extensions remain
outstanding, deferred, unsatisfied and without an assigned delivery phase.
No deployment/operational qualification or later-slice implementation is accepted.
Earlier implementation/pending-review entries below preserve historical states.

## Phase 7B-1 authentication implementation — 2026-09-17

The overall 7B direction is accepted. Only [7B-1](plans/074-brian-only-authentication.md)
is authorized for implementation/testing/self-review, followed by Brian review.
Authentication protects the current whole-set workspace; the saved-deal index,
snapshots, calculation receipts, replay and revisions remain later proposals.
No development migration, actual account setup, provider activity, exposure or
deployment follows. Older no-7B statements below describe prior authorization.
Deferred Economics Extensions stay outstanding without a phase assignment;
7C and Phase 8 retain their scope and require separate authorization.

## Phase 7A2 whole-set milestone closed — 2026-09-17

**Phase 7A2 Whole-Set Deal Economics: COMPLETE / ACCEPTED / CLOSED.**

Brian explicitly accepts this narrowed milestone after Slice 1/2A/2B technical and
visual acceptance at `fbbd98b29b84fe2b60132da8c1bfacc8d5f7ec54`. The
[closure decision](DECISIONS.md#phase-7a2-whole-set-closure-and-explicit-deferral--2026-09-17)
records the complete delivered scope: whole-set selected-market/manual sale and
shipping/cost assumptions; net/profit/loss/ROI; targets, both purchase limits,
Maximum Purchase / Buy Under, binding targets and signed headroom; whole-set
break-even purchase ceiling; purchase-price tax/premium assumptions; exclusive
manual/calculated selling fees, both supported bases and charge rounding; evidence,
stale-basis and lifecycle protections.

**Deferred Economics Extensions** owns all outstanding contents/condition,
minifigure quantity, instructions/box/build, split-sale/full-component economics,
recovery/burden and economic break-even-lot requirements. The
[requirement register](REQUIREMENTS_TRACEABILITY.md#deferred-economics-extensions)
preserves IDs, exclusions and prerequisites. They are outstanding/deferred, not
cancelled or satisfied, outside closed 7A2 and not moved to Phase 8, 7B or 7C.
No delivery phase or implementation authorization is assigned to that bucket.

Current sequence: accepted 7A1 → **7A2 CLOSED (whole-set milestone)** →
**7B planning, separately authorized** → 7C → Phase 8 Hunt. Phase 7 overall remains
incomplete. Authentication does not depend technically on the deferred bucket;
the whole-set Deal model is stable enough to persist once 7B resolves its frozen
snapshot/version contract, historical-versus-current behavior and retention gate.
See [7B open persistence questions](DATA_MODEL.md#7b-persistence-questions--unresolved).

This post-acceptance decision supersedes earlier overall-open/not-started entries
and the broader Phase 7 scope/acceptance and no-capability-moves clause below
**only for the newly deferred requirements**. Those entries preserve historical
planning and slice acceptance; they are not unfinished requirements inside closed
7A2. No further 7A2 implementation, 7B execution or push is authorized.

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

## Phase 7A2 Slice 2B — Selling Fee Rules authorized, 2026-09-17

Implement only [ExecPlan 073](plans/073-selling-fee-rules.md): explicit manual or
percentage-plus-fixed fees on item sale or gross proceeds, with declared transaction
rounding and existing purchase-limit integration. Slice 1/2A remain accepted.
2B implementation and technical validation PASS; Brian review remains pending before
closeout. No other provisional
7A2 work, 7B/7C persistence, Phase 8 Hunt, provider traffic, migration, commit or push.

## Phase 7A2 Slice 2A closed — 2026-09-17

**Purchase Limits Slice 2A: COMPLETE / ACCEPTED / CLOSED.** Technical PASS and Brian
visual PASS, including the final disclosure correction. One exact local checkpoint
is authorized; [ExecPlan 072](plans/072-purchase-limits.md) records scope and evidence.
No push. 2B remains NOT STARTED; later provisional 7A2 work is unchanged. Neither
Slice 2 overall nor Phase 7A2 is closed. Earlier pending entries are historical.

## Phase 7A2 Slice 2A — implemented, review pending, 2026-09-17

Purchase limits have technical PASS under [ExecPlan 072](plans/072-purchase-limits.md).
Brian visual review remains pending; the implementation is uncommitted. Stop before
2B. Neither Slice 2 nor Phase 7A2 as a whole is declared complete.

## Phase 7A2 Slice 2A authorized — 2026-09-16

[ExecPlan 072](plans/072-purchase-limits.md) implements transient whole-set purchase
limits: target ROI/minimum profit, both caps, maximum/headroom, break-even purchase
ceiling and declared purchase-price-based acquisition rates. Slice 1 remains closed.
Stop after 2A validation and Brian review; **2B selling-fee rules remain unstarted and
need explicit authorization**. Contents/condition and alternative-strategy economics
remain later provisional 7A2 requirements, not completed or transferred to Phase 8.
No provider traffic, migration, persistence, 7B/7C/8, commit or push.

## Phase 7A2 Slice 1 closed — 2026-09-16

**Whole-Set Deal Economics Slice 1: COMPLETE / ACCEPTED / CLOSED.**
Technical PASS and Brian visual PASS. Brian authorizes one local checkpoint of
exactly the reviewed slice; [ExecPlan 071](plans/071-whole-set-deal-economics.md)
records acceptance and validation. No push. Slice 2 remains NOT STARTED; the full
7A2 roadmap is not declared complete. Earlier pending entries are historical.

## Phase 7A2 Slice 1 — whole-set economics, 2026-09-15

Brian authorized only the whole-set Deal Economics vertical slice in
[ExecPlan 071](plans/071-whole-set-deal-economics.md). Implementation and technical
acceptance are complete; Brian visual acceptance is pending.
7A1 remains accepted/closed. Slice 2 and later work are unstarted: no targets,
Buy Under/headroom, break-even feature, complex fee policies, persistence/auth,
contents overlays or Hunt. Later contents planning remains provisional.
No commit or push is authorized. The earlier unstarted/checkpoint entries below
are historical; the broader 7A2 phase goals remain separate from this bounded slice.

## Phase 7A1 final acceptance and closeout - 2026-09-15

**7A1 COMPLETE / ACCEPTED / CLOSED. Technical PASS; Brian visual PASS.**
Brian accepted the current reviewed product-led hero, New/Used by Sold market/Active
listings matrix, Resale form, exact-set Rebrickable image/provenance, and responsive
visual evidence including 390x844 and 320x720. The permanent Brian-only private,
personal, non-commercial-use constraint remains binding. Phase 1-6 semantics and
the single set-scoped request/refresh/poller guarantees remain unchanged.

[Final acceptance record](plans/070-set-detail-information-architecture.md#final-acceptance-and-local-checkpoint---2026-09-15)
records repeated technical PASS, the retained 37 reviewed screenshots, exact
30-file local checkpoint scope and three protected unrelated files. Brian authorizes
one checkpoint on `main` with subject `Complete Phase 7A1 Set Detail and visual revision`.
No further presentation edits, no push, and no Phase 7A2. Earlier pending/rejected
visual checkpoints below are historical. **7A2 remains NOT STARTED.**

## 7A1 visual revision checkpoint - 2026-09-15

The original 7A1 visual design was rejected; its technical foundation is accepted.
The authorized Product Hero and Market Comparison revision now includes the narrow
optional retained Rebrickable image projection and generated contract, with no
schema or valuation change. Technical verification and visual evidence are complete;
Brian's redesigned visual acceptance remains pending. Phase 7A2 is NOT STARTED.
[ExecPlan 070](plans/070-set-detail-information-architecture.md) records final checks.

## Phase 7A1 implementation boundary - 2026-09-15

Brian accepted [ExecPlan 070](plans/070-set-detail-information-architecture.md) and authorized 7A1 frontend implementation. Overview / Market / Contents / Value Scenarios / Evidence replace the report; Value Scenarios is the refined name for the earlier Part-Out section. Technical acceptance PASS: 45 component tests, 17 synthetic browser tests, frontend static checks and build. Synthetic visual evidence is ready; Brian visual acceptance remains pending. Phase 6/UI-01 remain CLOSED, and 7A2 remains NOT STARTED. This updates the earlier next-planning/unstarted checkpoint without creating a new numbered phase.

**Current checkpoint — UI-01 COMPLETE / ACCEPTED / CLOSED, 2026-09-15:** Technical
acceptance and Brian's desktop/phone visual acceptance PASS. Preserve the reviewed
implementation; no UI-01 polish is required. Phase 6 remains CLOSED and Phase 7 is
NOT STARTED. Next is separately authorized **7A1 — Set Detail Information
Architecture planning**. [UI-01 closeout and deferred design considerations](plans/061-ui-foundation.md#ui-01-visual-acceptance-and-closeout--2026-09-15)
record the compact neutral identity and valuation-first direction; Deal Economics
remains 7A2. Earlier prerequisite/pending statements below are historical.

**Current checkpoint — Phase 6 CLOSED / ACCEPTED, 2026-09-14:** The separately
authorized development migration 0008 and bounded live product-button acceptance
passed at `0b9b6bae198d19001553e72f2549508dd6400845`: one confirmed operation,
0 identity + 4 price + 0 retry attempts, ledger 80 → 84, no duplicate traffic after
reload, and unchanged physical gates. [Closure evidence](plans/060-product-surface.md#phase-6-live-acceptance-and-closure--2026-09-14)
supersedes earlier pending-live status while preserving historical records.

**Approved UI/UX gate — documentation only:** [D-033](DECISIONS.md#d-033--decision-first-ui-architecture--2026-09-14)
and [UI/UX Architecture](UI_UX_ARCHITECTURE.md) establish one bounded prerequisite:
**Phase 6 COMPLETE → UI-01 → 7A1 Set Detail Information Architecture → 7A2 Deal
Economics → 7B Authentication and Reproducible Saved Deals → 7C Watchlist / Targets
/ Settings / Saved Deal Index → Phase 8 Hunt.** Numbered phases and prompts remain
unchanged. UI-01 and Phase 7 are unstarted; the next implementation authorization is
[UI-01 — Shared Shell and Persistent Set Search](plans/061-ui-foundation.md) alone.
The detailed Phase 7 ExecPlan is deferred until separately requested. Architecture
approval does not authorize implementation, services, providers or a Git checkpoint.

**Phase 6B public workflow independently accepted — 2026-09-14:** The 25-file local
checkpoint passes independent API/UI/durability review with bounded corrections.
[Acceptance evidence](plans/060-product-surface.md#phase-6b-public-workflow-independent-review--2026-09-14)
distinguishes synthetic testing from the next separately authorized guarded
development migration/account configuration and live product button acceptance.
Contents refresh and Phase 7 remain deferred; no live work or push occurred.

**Phase 6B public workflow implementation — 2026-09-14:** Complete-set planning,
explicit confirmation, durable progress/resume and appraisal reload are implemented
over accepted migration 0008. Synthetic acceptance and independent review govern this
checkpoint; no live provider acceptance or development migration has occurred.
Contents refresh and Phase 7 remain deferred. Next: independent review and local
checkpoint commit. [ExecPlan 060](plans/060-product-surface.md#phase-6b-public-workflow-implementation--2026-09-14)
records the current evidence; earlier entries remain historical.

**Phase 6A independently accepted — Phase 6B ready, 2026-09-13:** Set-number/name search and bookmarkable cached appraisal detail pass independent product review for the authorized local checkpoint. Four strategies and four market views preserve partial, unknown and physical-blocked states. The Windows smoke harness now reserves an OS-assigned TEST port; corrected integration acceptance exits successfully. [ExecPlan 060](plans/060-product-surface.md) records the 40-file reviewed inventory, bounded fixes, automated/manual checks and cleanup. ZERO provider requests / ZERO provider credential loading; no new migration or dependency. **Next: separately authorize Phase 6B explicit user-triggered discovery/refresh.** Phase 6B and saved/deal/Hunt work have not started. Earlier entries are historical checkpoints.

## Phase 5C bounded completion policy — 2026-09-12

Brian approved [5C synthesis](plans/050-valuation.md#phase-5c-approved-implementation-contract--2026-09-12)
as the final bounded Phase 5 slice: uncalibrated versioned Liquid/Fast Cash gross
scenarios, dead-stock-like exposure, evidence categories and honest partial coverage.
[Independent acceptance](plans/050-valuation.md#phase-5c-independent-acceptance--2026-09-12)
completes bounded Phase 5; Phase 6 requires separate authorization and is unstarted.

The historical broad Phase 5 scope below is not a completion claim for economics,
Gems, M-dependent metrics, burden classifications, rarity, premium or other deferred
capabilities. Gems require user experience/approved thresholds; economic ranking,
costs/profit/ROI/max-buy and purchase recommendations remain later deal work; Hunt
scoring remains Phase 8. Concentration is annotation only. Future Phase 6 must show
unsupported capabilities honestly rather than fill the older complete Part-Out
Analysis concept with invented values.

**Phase 4A independently accepted offline — 2026-09-12 UTC:** [ExecPlan 040](plans/040-calibration.md) records independent acceptance and the 26-file local checkpoint scope. Offline 4A does not complete the live feasibility gate below. Final recovery/liquidity/Gem/burden/Hunt formulas remain Phase 5 or their later product phase. Next is Brian's separate Phase 4B scope/traffic-ceiling and access/rights authorization; no live traffic ceiling is authorized and Phase 4B remains unstarted.

**Phase 3C offline accepted — 2026-09-12 UTC:** F5 is corrected and deterministic PostgreSQL regressions pass. [ExecPlan 030, section 18](plans/030-market-provider.md#18-independent-phase-3c-offline-acceptance--2026-09-12-utc) preserves the finding and records final verification and the reviewed 32-file checkpoint scope. Phase 3 is complete locally; Phase 4 requires separate authorization. Historical checkpoints below remain dated evidence.

**Current checkpoint — 2026-09-11:** Phase 2 is locally accepted: official development generation 1, cached no-op and history preservation verified, cleanup correction tested, and all 61 intended files independently reviewed. This acceptance does not establish deployment or the deferred product capabilities. See [ExecPlan 020](plans/020-catalog-foundation.md). Phase 3A passes independent offline acceptance for the authorized local checkpoint: 141 BrickLink tests and 416 Python units pass after two bounded transport corrections. See [ExecPlan 030](plans/030-market-provider.md) for actual verification. Phase 3B discovery correction and bounded live proof passed: three justified mappings, twelve valid price views, 7 identity + 12 price + 0 retry = 19 attempts. Independent acceptance passed after three narrow offline corrections and 218 affected tests; the local checkpoint commit is authorized. See ExecPlan 030 section 17 for evidence qualifications. Credential/IP compatibility was demonstrated for this local run. Phase 3C and its retention/display-rights decisions remain unstarted.

Dated execution records below preserve historical outcomes and then-applicable authorization; their pending or blocked states do not supersede this checkpoint.

**Historical Phase 2D outcome — 2026-09-10 local: BLOCKED at a different development SQL timeout.** The requested observation timeout is proven and corrected by in-transaction candidate color-fact analysis. An independent matching retained-state probe changes SELECT from a 300-second timeout to 0.820762 seconds and full rollback INSERT to 57.537484 seconds; corrected retained official acceptance inserts 1,557,375 observations in 55.291041 seconds and passes 72 pre/postactivation cases plus no-op. All 264 Python units, 22 Node tests, 11 React tests, 196 PostgreSQL tests, six browser cases and build/contracts/package gates pass. Authorized fourth NEW development run `bcf21407-15ab-44bb-b358-17f600282599` instead times out earlier at step 16 `evidence_conflict:elements` in 300.004024 seconds (57014); its cause is not yet proven. Construction rolls back before the corrected observation step, validation, benchmark or activation. Read-only verification confirms zero candidate facts/validation, official generation 0/no receipts, unchanged two synthetic snapshots/four receipts/generation 4, and all three prior failed histories/staging unchanged. A fourth terminal failed run is retained. The accepted Windows publisher, migration 0005, existing indexes and 300-second limit remain unchanged. No fifth import, provider call, staging cleanup, Git checkpoint or Phase 3 work occurs. See the [current 42-item report](PHASE_2D_OBSERVATIONS.md). Earlier stops below remain historical evidence.


**Historical R-code stop (2026-09-09; superseded above):** Policy cleared by current user-captured
official evidence; all twelve official gzip files acquired automatically.
Canonical import is blocked pending the evidenced label for raw relation code `R`.
The [official-source report](PHASE_2D_OFFICIAL_EVIDENCE.md) separates acquisition
and parser evidence from unrun database acceptance, benchmarks and activation.
Phase 2 remains incomplete; Phase 3 is not started. Earlier dated stops below
describe their historical attempts.

**2026-09-09: Phase 2D BLOCKED before acquisition.** The explicitly authorized
execution passed its clean entry gate but could not verify current official
Downloads/Terms. No source download, code or database change occurred. See the
[provider gate report](PHASE_2D_PROVIDER_GATE.md). Next: resolve current official
policy evidence and resume Phase 2D at that gate; Phase 2 remains incomplete and
Phase 3 is not started. Earlier checkpoint/slice-status statements below are history.

**Phase 2C independently accepted:** Internal queries, relationship semantics and
synthetic benchmarks pass review with approved index-only migration 0005, three
bounded corrections and 183 passing PostgreSQL tests. See the Phase 2 slice status
below and [ExecPlan 020](plans/020-catalog-foundation.md) for the authorized local
checkpoint evidence. Phase 2 remains incomplete; 2D is unstarted.

The following paragraph preserves the preceding 2B checkpoint.

**Historical implementation status (2026-09-09):** Slice 2B passed independent local acceptance on 2026-09-09 for the authorized local checkpoint. Migration 0004, offline CSV/gzip parsing, typed COPY staging, stable identities, candidate validation, explicit atomic activation, receipts and recovery are accepted against synthetic local evidence. Review corrected nullable version/target validation and terminal-run transitions; all 161 PostgreSQL tests passed. Phase 2 remains incomplete; profiles remain DOCUMENTATION-VERIFIED / LIVE-UNVERIFIED, no official source was acquired, and Phase 2C has not started. The next separately authorizable action is **Phase 2C — deterministic catalog queries and relationship semantics: set number/name lookup, inventories, spares, minifigures, component expansion, nested-set expansion, matching selections, element/part relationships, containment queries, and the benchmark harness.** Do not begin it automatically. [ExecPlan 020](plans/020-catalog-foundation.md) records evidence; [offline import](CATALOG_IMPORT.md) describes operation. Earlier phase checkpoints below are historical.

## Status and phase map

Historical Phase 1 checkpoint: **Phase 1 independent local acceptance passed on Windows; the reviewed foundation is the local completion checkpoint.** [ExecPlan 000](plans/000-local-foundation.md) records shell/static/browser/CI evidence and preserves accepted Slice 1A/1B history. D-025 remains documentation-only future product scope. Remote GitHub CI execution is deferred; home-server/production deployment has not occurred. The exact next action after the local completion commit is **Phase 2 planning/implementation for LEGO catalog identities, complete set inventories, parts, colors, minifigure relationships, quantities, alternates, extras, inventory versions, and provider mappings.** Do not begin Phase 2 automatically. Recognition remains an optional Phase 14 input; Prompt 01 remains PLAN ONLY. No phase entry/completion itself authorizes implementation, network access, services, staging, commit or push.

Each roadmap phase maps to exactly one numbered prompt. Prompts 13–16 refine the later image extension; they do not displace Phases 1–12. Inputs and gates must be satisfied before advancing.

| Phase | Name | Prompt |
|---|---|---|
| 0 | Bootstrap and plan | [00_bootstrap_plan.md](../prompts/00_bootstrap_plan.md) |
| 1 | Repository and local foundation | [01_scaffold_foundation.md](../prompts/01_scaffold_foundation.md) |
| 2 | Catalog and set/minifigure relationships | [02_catalog_and_relationships.md](../prompts/02_catalog_and_relationships.md) |
| 3 | Market-price provider integration | [03_market_price_provider.md](../prompts/03_market_price_provider.md) |
| 4 | Representative-set feasibility gate | [04_feasibility_gate.md](../prompts/04_feasibility_gate.md) |
| 5 | Deterministic valuation engine | [05_valuation_engine.md](../prompts/05_valuation_engine.md) |
| 6 | Set search and detail vertical slice | [06_set_search_and_detail.md](../prompts/06_set_search_and_detail.md) |
| 7 | Deal calculator and saved work | [07_deal_calculator_and_saved_work.md](../prompts/07_deal_calculator_and_saved_work.md) |
| 8 | Sets to Hunt | [08_sets_to_hunt.md](../prompts/08_sets_to_hunt.md) |
| 9 | PWA, offline behavior, and Android core app | [09_pwa_and_android.md](../prompts/09_pwa_and_android.md) |
| 10 | Local release and security hardening | [10_release_and_security_hardening.md](../prompts/10_release_and_security_hardening.md) |
| 11 | Read-only home-server discovery | [11_home_server_discovery_read_only.md](../prompts/11_home_server_discovery_read_only.md) |
| 12 | Approved home-server deployment | [12_home_server_deployment_explicit.md](../prompts/12_home_server_deployment_explicit.md) |
| 13 | Marketplace image ingestion | [13_marketplace_image_ingestion.md](../prompts/13_marketplace_image_ingestion.md) |
| 14 | Recognition quality spike | [14_recognition_spike.md](../prompts/14_recognition_spike.md) |
| 15 | Android share and overlay capture | [15_android_capture_overlay.md](../prompts/15_android_capture_overlay.md) |
| 16 | Training datasets, outcomes, and recognition hardening | [16_training_dataset_and_hardening.md](../prompts/16_training_dataset_and_hardening.md) |

## Phase 0 — Bootstrap and plan

- **Inputs:** Authoritative product definition, current guidance, decision history, and the product-scope audit.
- **Scope:** Read/revalidate the unified product and bounded Phase 1 ExecPlan; keep valuation-first ordering and historical decisions explicit.
- **Exclusions:** Application implementation, installations, services, provider/network calls, infrastructure access, and staging/commits.
- **Acceptance:** The in-chat plan preserves the ten requirements and defines only the local foundation, with reviewable assumptions and a stop before edits or implementation.
- **Gate:** The reviewed documentation baseline is the Phase 0 checkpoint; subsequent revalidation is plan-only unless Brian separately requests Markdown/local-Git work.
- **Access and evidence:** Local read-only files only; no network, devices, or servers.

## Phase 1 — Repository and local foundation

- **Inputs:** Approved product/architecture and canonical [ExecPlan 000](plans/000-local-foundation.md); a separate explicit implementation request for the selected slice.
- **Scope:** React/Vite responsive shell, FastAPI shell, isolated PostgreSQL, SQLAlchemy/Alembic empty baseline, health/readiness/OpenAPI and generated TypeScript contracts, strict checks, provider-free CI, and local setup documentation.
- **Exclusions:** Catalog imports/providers/prices/valuation/search/deals/authentication/Sets to Hunt, listings/images/recognition, PWA/Android, and home-server/deployment work.
- **Acceptance:** The implemented local web shell and API run against an isolated migrated database with reproducible contract/format/lint/type/unit/integration/build checks, CI definitions, and built-serving desktop/mobile browser evidence. No product tables or external providers are required.
- **Gate:** Each of Slices 1A, 1B, and 1C requires separate explicit implementation authorization and ends with a report; completion does not authorize the next slice. Prompt 01 is reusable plan-only review. Slice 1B acceptance authorizes only its bounded corrections and conditional local checkpoint; it does not begin Slice 1C.
- **Access and evidence:** Slice 1A may verify/install local toolchains and resolve packages only under its explicit dependency/network scope, with no services/database work. Slice 1B separately authorizes isolated local database/API work. Slice 1C separately authorizes web/CI/local acceptance. Never contact product providers, existing PostgreSQL on 5432, or home infrastructure.

### Slice 1A — Toolchain and workspace

Verify supported toolchains/compatibility; create workspace/manifests/configuration and exact locks; add format/lint/type/orchestration foundations; resolve and commit locks only under the slice's explicit local-Git authorization. Report applicable checks and stop before database or application-shell work.

### Slice 1B — Database, API, and contracts

After separate authorization, add isolated development/test PostgreSQL, guarded tooling, SQLAlchemy/Alembic, health/readiness/OpenAPI, deterministic TypeScript contracts, and real unit/integration/contract checks. Report and stop before frontend/built-serving/browser/CI completion.

### Slice 1C — Web shell, built serving, CI, and acceptance

After separate authorization, add React status UI, Vite proxy, FastAPI built serving, browser smoke tests, and GitHub Actions. Run every full Phase 1 acceptance criterion, update permitted documentation, report, and stop before Phase 2. The slice split does not weaken final acceptance.

## Phase 2 — Catalog and set/minifigure relationships

**Slice status:** 2A/2B/2C/2D are locally accepted. The official development catalog is active at full-catalog generation 1; independent review, cached no-op and history preservation pass. See [ExecPlan 020](plans/020-catalog-foundation.md) for evidence reuse and remaining capability/platform limitations. Phase 3A passes independent offline acceptance for the authorized local checkpoint; see [ExecPlan 030](plans/030-market-provider.md). Phase 3B passes independent acceptance; Phase 3C remains unstarted.

D-025 extends the existing [part-out plan](plans/005-set-part-out-values.md) through Phases 2–8 with PRODUCT_SPEC R-11–R-37. Full part-out analysis is core; operational individual-piece listing/fulfillment and theoretical totals presented as cash remain excluded. No standalone phase or Phase 1 product/provider/queue work is added. Selective harvest stays later until supported; each phase requires separate authorization.

- **Inputs:** Completed local foundation; explicit identity/quantity contracts and permitted local catalog fixtures.
- **Scope:** Repeatable set/figure/part/color identities and exact provider mappings, suffix/name/theme semantics, inventory versions/provenance, separate regular/extra quantities, alternate/matching resolution, intact/component figure and nested subset relationships, sourced instructions and later permitted packaging, and scoped exact part/color rarity relationships.
- **Exclusions:** Pricing/valuation implementation, browser search/detail workflow, image ingestion, embeddings, recognition, scraping, and infrastructure changes.
- **Acceptance:** Permitted fixtures resolve representative numbers/names, preserve canonical variants and every figure/part/color quantity including repeated figures, expose malformed data and ambiguous mappings, resolve required choices, keep extras separate and prove physical inventory is never double-counted. Unknown mapping/expansion/catalog coverage cannot prove completeness or exclusivity.
- **Gate:** Review import/source-use rights before source data is used; no arbitrary suffix stripping or first-match mapping; fixtures do not establish provider access.
- **Access and evidence:** Local fixtures suffice for implementation checks; live catalog/download requests require separately authorized network access and verified source permissions.

## Phase 3 — Market-price provider integration

**Slice status:** 3A passes independent offline acceptance after two bounded transport corrections, with 141 BrickLink and 416 Python tests passing. The 3A checkpoint is committed. The separately authorized 3B discovery correction and capped live proof pass independent acceptance for the local checkpoint commit; see section 17 for offline corrections and evidence limits. 3C remains separately authorized with unresolved retention/display-rights decisions. The complete sequence and evidence are in [ExecPlan 030](plans/030-market-provider.md).

- **Inputs:** Verified canonical identities/relationships and mappings; provider-gate checklist and permitted fixtures.
- **Scope:** Server-side set/figure/part observations for NEW/USED and SOLD/CURRENT, exact currency/statistics, sold units/occurrences/window, point-in-time current units and supplied inventory/lot/store counts, freshness and confidence. Verify aggregate capabilities and design shared observation caching, deduplicated priority background refresh, request budgets and bounded concurrency/retries.
- **Exclusions:** Scraping, guessed mappings, browser/Android secrets, valuation UI, recognition, unlimited retention assumptions, and infrastructure administration.
- **Acceptance:** Authorized calls or labeled permitted fixtures preserve four-view price/activity semantics and unknowns. Shared-part refresh tests prove deduplication, quota/backoff bounds, stale/failure isolation and no synchronous per-set fan-out; live aggregate capability and rights are explicitly verified.
- **Gate:** Verify current official authentication/eligibility, rights/display/cache/retention, quotas/cost, and outbound-IP requirements before live calls or provider-content persistence; missing permissions block that path.
- **Access and evidence:** Network/provider access is required for live proof and must be explicitly authorized; recorded-fixture checks remain distinguishable and cannot certify live access.

## Phase 4 — Representative-set feasibility gate

- **Inputs:** Catalog/mapping versions, normalized market adapter, permitted observations, and a documented representative sample.
- **Scope:** Benchmark modern/retired and suffixed variants, zero/one/many/repeated figures including dominant figures, unresolved mappings, missing/stale/thin evidence and supported residual-build assumptions alongside representative inventories and four POV views, authorized BrickLink-displayed equivalence/differences, price/activity coverage, proxy/velocity/supply/absorption semantics, large-set call budgets/cache/stale behavior, recovery assumptions, Gem/Liquid/Fast Cash/dead-stock/concentration/burden metrics and candidate Hunt normalization/weighting.
- **Exclusions:** Recognition benchmarks, scaling imports instead of evaluating coverage, fabricated provider access/rights, product UI expansion, and production access.
- **Acceptance:** A reproducible representative real-set report establishes whole-set/minifigure NEW/USED coverage and whether deterministic sourcing is supported, partial or blocked, then records four-view numerical agreement or comparison gaps/reasons, rights and coverage, cold/warm/shared-set budgets and liquidity behavior. It validates or blocks candidate recovery/liquidity/Gem/burden/Hunt policies with sensitivity evidence; fixtures cannot certify live feasibility or final thresholds.
- **Gate:** No live rights/account/coverage claim before this gate actually runs; fixture-only evidence cannot pass live-product feasibility, and critical unsupported mappings/evidence block advancement to supported recommendations.
- **Access and evidence:** Live feasibility requires authorized provider/network access and Brian review; offline fixtures can rehearse the report only, with live gates explicitly unresolved.

## Phase 5 — Deterministic valuation engine

**Bounded 5A and 5B independently accepted:** [ExecPlan 050](plans/050-valuation.md)
records the theoretical core and separately authorized S/O/C/I, sell-through proxy,
concentration, ranked-lot diagnostics and metric readiness. Exact production M and
duration metrics remain unsupported. Recovery dollar values/coefficients, Gem and
burden/Hunt classifications, 5C synthesis, deal economics and public API/UI remain
unstarted. Next: separately authorize a bounded Phase 5C plan in a new task.
The broader phase scope below is not authorization to begin deferred work.

- **Inputs:** Phase 4 feasibility outcome, exact valuation rules, verified representative fixtures, and supported evidence policies.
- **Scope:** Pure server calculations for four-view theoretical/recoverable POV, proxy/velocity/supply/absorption/occurrences, opportunities/Gems, Liquid/Fast Cash/dead-stock, concentration, break-even lots, value per lot/piece, burden, competition/rarity, POV premium and separate strategy economics. Retain exact costs/profit/ROI/both max-buy constraints and versioned partial/blocked snapshots.
- **Exclusions:** UI financial logic, live provider calls required by unit tests, image/AI work, operational individual-piece listing/fulfillment, automatic purchasing, and production access.
- **Acceptance:** Table-driven exact-arithmetic tests reproduce every valuation/liquidity formula and policy, covering complete/missing/damaged/repeated inventory, four-view and gross/net separation, zero/unknown/infinite states, partial coverage, alternate/extra/figure allocation, stable concentration/break-even ties, subset costs, policy boundaries and acquisition tax/premiums without double-counting.
- **Gate:** Review formula/rounding/constraint examples and unsupported-evidence behavior before exposing recommendations; preserve rights-compliant reproducibility.
- **Access and evidence:** Local deterministic fixtures; dependency access only if separately authorized for implementation, no product-provider or server access needed.

## Phase 6 — Set search and detail vertical slice

**Accepted scope clarification — 2026-09-14:** Phase 6 is closed under
[ExecPlan 060](plans/060-product-surface.md). The broad original scope/acceptance below
is preserved as product intent, not a claim that imagery, complete valued figure
rows, Gems, all concentration/burden metrics or history now exist. Existing data
presentation moves into 7A1; justified read projections remain explicit scoped work;
new economics belongs to 7A2 and Hunt ranking to Phase 8. Unsupported ambitions do
not reopen accepted phases or authorize backend work for UI convenience.

- **Inputs:** Verified catalog/market contracts, passed feasibility gate, and tested valuation totals/coverage functions.
- **Scope:** Direct suffix/name search and shared API/React detail for whole-set/figure NEW/USED evidence, individual prices and quantity-aware totals, separate market sides, permitted images/references and provenance plus Part-Out Analysis: four POV views, recoverable gross, Liquid/Fast Cash/dead-stock, premium, coverage/freshness, Gems and high-value/low-liquidity warnings, top-5/top-10 concentration, density/burden and paginated part evidence with bounded refresh states.
- **Exclusions:** Listing sessions, user image uploads, recognition, separate client formulas, saved-deal editing, and deployment.
- **Acceptance:** Desktop/mobile API/browser checks resolve numbers/names with recognition disabled and show whole-set values, every included figure/quantity/individual price/quantity-aware total and all required Part-Out Analysis fields, independent four-view coverage, evidence drill-down and fresh/stale/pending/partial/blocked states. No client arithmetic, synchronous hundreds-of-provider-calls request or guaranteed sale claim is accepted.
- **Gate:** Browser/API acceptance must cover ambiguity, no-figure, repeated-figure, and unavailable-price cases with image modules disabled.
- **Access and evidence:** Local fixtures/cached permitted evidence for tests; any live refresh remains within the already verified and explicitly authorized provider scope.

## Phase 7 — Deal calculator and saved work

**Approved prerequisite and internal boundaries — 2026-09-14:** Complete
[UI-01](plans/061-ui-foundation.md) before Phase 7 frontend implementation. It extracts
shell/search/tokens and centralizes existing navigation only; it does not migrate
Set Detail. When separately requested, the detailed Phase 7 ExecPlan must preserve
the existing inputs/gates below and use these independently accepted boundaries:

| Internal slice | Scope and acceptance boundary |
|---|---|
| 7A1 — Set Detail Information Architecture | Reorganize existing appraisal into Overview, Market, Contents, Part-Out and Evidence; compact identity, explicit market/strategy context, decision summary, visible evidence states and responsive disclosure. No new Deal engine or calculations. |
| 7A2 — Deal Economics | Add asking/acquisition assumptions, actual condition and supported missing/damaged contents, acquisition/selling costs, Buy Under/headroom, gross/net/profit/ROI, supported liquidity/burden/break-even and deterministic recommendations. Server-owned calculations; separate acceptance from 7A1. |
| 7B — Authentication and Reproducible Saved Deals | Reviewed private auth/persistence, retention-compatible immutable forecasts, reproducible reopening after market refresh and explicit revision conflicts. |
| 7C — Watchlist / Targets / Settings / Saved Deal Index | Reuse saved records and the Deal workspace for targets, profiles/settings, saved sets/notes/URLs and indexes. No alerts, fetched listings or resale operations. |

These are internal slices, not new roadmap phases. No existing Phase 7 capability
moves to another phase. Saved/current appraisals stay distinct; both maximum-buy
caps and one supported recommendation remain required. Resolve source-retention
compatibility before durable forecasts; calculated outputs are not automatically
exempt. All implementation remains separately authorized.

- **Inputs:** Direct set detail and tested valuation engine; reviewed private authentication and persistence design.
- **Scope:** Asking price, actual contents/condition and missing/damaged figure/part/build/instruction/box allocation, profiles/costs and separate complete-set, figures-plus-build and full-part-out comparisons with theoretical/recoverable gross, net/profit/ROI/max-buy, liquidity/burden and break-even lots. Persist saved sets/deals/notes/watchlists/targets/settings, assumptions/thresholds/calculation versions/freshness and Brian-only authentication; selective harvest remains later until supported.
- **Exclusions:** Recognition/capture, new arithmetic in clients, offline writes, seller automation, provider-rights bypass, and production work.
- **Acceptance:** Authenticated saved sets/deals/notes/watchlists/targets/settings survive reload; strategy comparisons reproduce original allocation and missing/damaged adjustments, recovery/threshold/profile versions, evidence freshness, costs and outputs after market refresh. Verify removed parts/figures leave residual value, gross versus net break-even coverage, unknown costs/recovery, revision conflicts and unchanged original forecasts.
- **Gate:** Review authentication and source-retention compatibility before persistent private workflows or any approved non-loopback access; revision conflicts cannot silently overwrite saved work.
- **Access and evidence:** Local private tests first; no LAN/public binding change or home access without explicit scope, and provider access remains separately bounded.

## Phase 8 — Sets to Hunt

**Current execution status — 2026-09-22:** Slice 1, Cached Whole-Set Hunt Run, is
ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT under
[ExecPlan 083](plans/083-hunt-cached-whole-set-run.md). Phase 8 remains IN PROGRESS.
It is limited to user-selected cached whole-set scenarios and immutable run snapshots;
it adds no composite score and does not complete the broader Phase 8 scope below.
Technical and four-image visual review passed. Remaining R-36 scope requires the
focused review/planning decision recorded above; no composite score is presumed required.

**Approved UI direction — 2026-09-14:** Hunt is the reseller opportunity screener in
the shared shell, activated only when supported ranking exists. Use compact tables,
explained component scores and useful supported filters, with a compact phone view.
Do not invent lifecycle/history filters, asking prices or precise ranks for unknown
inputs. Watchlist does not imply alerts. Later phase ownership remains unchanged:
PWA/Android in 9; listing sessions/images in 13; recognition in 14; capture in 15;
actual purchase/resale outcomes in 16.

- **Inputs:** Supported market/valuation snapshots, saved targets/profiles, feasibility policies, and deterministic sample opportunities.
- **Scope:** Decomposable Hunt components for asking-price economics or labeled hypothetical targets, POV premium/recoverable/Liquid/Fast Cash/dead-stock, Gems/figure/part/top-5/top-10/high-liquidity concentration, proxy/velocity/supply/absorption distributions, break-even lots, density/burden/listings/orders, rarity, competition and price/activity/mapping/sample/freshness confidence.
- **Exclusions:** Scraping for deals, automatic purchases/contact, invented asking prices, theoretical part-out cash, recognition, and production access.
- **Acceptance:** Reproducible rankings compare supported strategies and expose each input/component/version/tie rule and evidence blocker. Phase 4-reviewed calibration governs any combined score; missing critical data, high theoretical price or rarity alone cannot create a precise supported high rank.
- **Gate:** Test ties, missing/thin/stale prices, concentration, residual assumptions, and selling burden; disclose a hypothetical acquisition assumption when no asking price exists.
- **Access and evidence:** Local fixture/cached snapshot evaluation; separately authorized provider refresh only under established quotas/rights.

## Phase 9 — PWA, offline behavior, and Android core app

**Status: CLOSED on 2026-09-26.** The accepted source, package, and physical
evidence is recorded in [ExecPlan 088](plans/088-android-https-auth-source.md).

- **Inputs:** Private sourcing workflows, shared React UI/API, versioned saved work, and an authorized Android packaging test environment.
- **Scope:** Installable PWA and preferably Capacitor Android package of the same UI, private auth, dated read-only caches, explicit offline states, and server-revision synchronization.
- **Exclusions:** Separate native core UI/database/valuation engine, offline financial recalculation/writes, overlay/capture/Share implementation, and home deployment.
- **Acceptance:** Chrome/PWA and Android support set search/detail, deal analysis, saved work, and watchlists through one backend/database, and cached information is dated without representing stale prices as current.
- **Gate:** Document the packaging spike and any justified alternative; test physical Android core workflows and auth/cache expiry/sync conflicts separately from compilation.
- **Access and evidence:** Authorized local SDK/dependency acquisition and physical Android device testing; device-to-API networking needs explicit secure scope, not home-server access.

## Phase 10 — Local release and security hardening

**Status: CLOSED for local release/security readiness.** P10-01, P10-02 and
P10-03 are ACCEPTED / CLOSED. [ExecPlan 089](plans/089-local-packaged-release-readiness.md)
reconciles one current web/API build and packaged HTTP smoke (18 HTTP checks),
five focused tooling tests, and reused authentication, migration, recovery and
Android evidence. No new physical Android qualification, comprehensive
security/dependency audit, production disaster-recovery proof, home-server
access or deployment qualification is claimed. Deferred Economics Extensions
and remaining R-36 capabilities stay outstanding and unassigned.

- **Inputs:** Feature-complete core web/PWA/Android, auth, migrations, versioned data, and disposable local release fixtures.
- **Scope:** Local release packaging, security/auth/secret review, migration/rollback checks, backup/restore rehearsal, observability, and release/check documentation.
- **Exclusions:** Home-server discovery, Proxmox/router/DNS/Cloudflare changes, public exposure, production deployment, and image modules.
- **Acceptance:** The locally packaged application passes security, authentication, secret handling, migrations, disposable backup/restore, observability, and release checks without touching production infrastructure.
- **Gate:** Record actual check results and unresolved release blockers; local readiness is not deployment authorization.
- **Access and evidence:** Local/disposable services only; security-feed/dependency network access requires explicit task scope, and Android release checks distinguish physical evidence.

## Phase 11 — Read-only home-server discovery

**Status: P11-01 ACCEPTED / CLOSED; Phase 11 CLOSED.** Brian separately
authorized P11-01 read-only access to the workstation and existing home hosting
environment. ChatGPT accepted the published r1 evidence. The observed facts
and unknowns are in [ExecPlan 090](plans/090-home-infrastructure-discovery.md).
At Phase 11 closeout, Phase 12 was NEXT / NOT STARTED and still needed separate
authorization. The P12-01 authorization above permits source/local work and
read-only preflight only; infrastructure or production change remains gated.

- **Inputs:** Completed local release evidence and Brian's separate explicit authorization naming discovery targets/access.
- **Scope:** Read-only discovery of actual Proxmox, networking, storage, proxy/tunnel, backup, monitoring, and rollback constraints; document facts and unknowns.
- **Exclusions:** Any remote/local infrastructure configuration mutation, installs, service starts/restarts, deployments, database writes, DNS/Cloudflare/router changes, or application commit. P11-01 separately authorizes the isolated, report-only GitHub review-package publication described in the workflow.
- **Acceptance:** A read-only report identifies actual infrastructure constraints and a proposed deployment boundary without making changes.
- **Gate:** Separate explicit discovery authorization is mandatory before any connection; discovery permission is never deployment permission.
- **Access and evidence:** Only explicitly authorized home/network/control-plane read access; no credentials in chat or broad exploratory target discovery.

## Phase 12 — Approved home-server deployment

- **Status:** IN PROGRESS; P12-01, P12-02 and P12-03 ACCEPTED / CLOSED.
  P12-04A, P12-04B and P12-04C are ACCEPTED / CLOSED;
  P12-04D is ACCEPTED / CLOSED;
  P12-04 remains IN PROGRESS and P12-05 has not started. The recovery
  foundation is in [ExecPlan 095](plans/095-dual-recovery-foundation.md); activation
  and remaining gates are in [ExecPlan 096](plans/096-production-database-activation.md).
- **Inputs:** Phase 11 actual findings, local release artifacts, reviewed deployment/backup/rollback plan, exact approved hostname and targets, and distinct explicit execution authorization.
- **Scope:** Execute only the approved deployment steps and validate private application operation under the selected abrianbaker.com subdomain.
- **Exclusions:** Unapproved host/network/DNS changes, public PostgreSQL, unrelated systems, recognition scope, and implicit staging/commits.
- **Acceptance:** The approved subdomain passes authenticated HTTPS, backup/restore, monitoring, and rollback checks, and PostgreSQL is never publicly exposed.
- **Gate:** Do not connect or execute without both reviewed concrete plan and separate deployment approval; DNS/tunnel/router changes must be explicitly included in that plan's authorization.
- **Access and evidence:** Only specifically approved production/home/DNS/control-plane actions; stop at a changed target or material discovery mismatch before broadening scope.

## Phase 13 — Marketplace Listing Intake + Images

**ACCEPTED / CLOSED.** [Plan 103](plans/103-phase-13-image-ingestion.md) and the
accepted 13C implementation/schedule evidence above close this phase.

- **Inputs:** Proven deterministic core, separately requested image ExecPlan, and reviewed image privacy/retention/deletion policy.
- **Scope:** Optional listing metadata/session workflow, multi-file upload, immutable originals, exact dedupe, thumbnails/lineage, listing_image_id, independent partial success, stable UUID/display_order, duplicate receipts, and report-only consistency checking.
- **Exclusions:** Recognition/model calls, new catalogs/pricing/offer formulas, native capture, near-duplicate/crop polish, training exports, automatic deletion, and infrastructure changes.
- **Acceptance:** Images attach to optional listings without affecting direct lookup, original bytes/lineage survive restart, and real concurrency/failure tests prove deterministic order and recoverable successful-duplicate receipts.
- **Gate:** Apply IMAGE_INGESTION.md and approve explicit retention/deletion/privacy policy before shipping; current documentation never authorizes image handling or production deployment.
- **Access and evidence:** Local authorized image fixtures and isolated services; no source-URL fetching or provider calls, and production rollout remains separately authorized.

## Phase 14 — Recognition quality spike

**NEXT / NOT STARTED.** Separate authorization is required before work begins.

- **Inputs:** Proven core/image ingestion, rights-cleared catalog references, separately confirmed listing examples, and approved provider/spending scope.
- **Scope:** Candidate set/minifigure identities using shared catalog/mappings, server-side OpenAI/Gemini adapters, text clues, retrieval/verification comparison, analysis provenance, and separate corrections.
- **Exclusions:** A parallel catalog/mapping/valuation engine, model-invented finance, custom training, full catalog/vector infrastructure without evidence, Android capture, and deployment.
- **Acceptance:** A repeatable small-catalog evaluation measures identification/retrieval/unknown/cost/latency behavior and routes candidate canonical identities into the same core while direct set search works with recognition disabled.
- **Gate:** Verify current model/account/image-use/retention/cost conditions before live calls; fixture results are not paid-provider benchmarks or confirmed labels.
- **Access and evidence:** Explicitly authorized paid/provider network scope for live evidence; no claims of live accuracy from synthetic fixtures.

## Phase 15 — Android share and overlay capture

- **Inputs:** Working shared-UI Android core, proven image API, recognition findings, approved retention policy, and Brian's physical-device details.
- **Scope:** Needed native Share extension and isolated visible user-triggered allowlisted capture spike; only after device proof, manual multi-photo review/crop/order and result handoff with robust partial retries.
- **Exclusions:** A second native core app, automatic browsing/swipes/clicks, Facebook traffic/credential interception, unattended capture, independent valuation, and unapproved infrastructure access.
- **Acceptance:** Physical-device evidence proves supported Share/capture flows and fallback/permission/failure behavior while the same core UI/API/data and direct lookup remain usable when capture is disabled.
- **Gate:** Separate spike results from polished follow-on work; do not claim Facebook compatibility from an APK/emulator or move past a failed device gate.
- **Access and evidence:** Explicitly authorized Android SDK/device tests and supported-API research; any secure device/backend networking is scoped separately from production administration.

## Phase 16 — Training datasets, outcomes, and recognition hardening

- **Inputs:** Proven deterministic app and optional image/capture flows, reviewed labels/privacy policy, and preserved valuation histories.
- **Scope:** Append purchase/resale outcomes, forecast-versus-actual reports, reviewed label states, sanitized versioned exports, hard negatives, connected-source-safe splits, image security/recovery and backup regression.
- **Exclusions:** Custom model training, automatic promotion of predictions, provider-rights assumptions, deleting originals outside policy, duplicated valuation rules, and unapproved production operations.
- **Acceptance:** Actual outcomes append without rewriting forecasts, and a reproducible sanitized dataset/export plus regression evidence preserves confirmed-label provenance, connected-source split integrity, receipts/order, and recoverable data.
- **Gate:** Verify export/source rights and every training-ready confirmation/privacy decision; physical capture limitations remain explicit and custom training needs a new request.
- **Access and evidence:** Local/disposable export and backup checks; private data/provider/device/production access only when separately authorized for the exact check.

## Shared acceptance authority

Use [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [VALUATION_RULES.md](VALUATION_RULES.md), [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md), [PROVIDER_GATES.md](PROVIDER_GATES.md), and [SECURITY_PRIVACY.md](SECURITY_PRIVACY.md). Product phases remain planned; foundation evidence is limited to the accepted slices recorded in ExecPlan 000. Dated research and fixtures do not constitute provider or physical-device proof.
