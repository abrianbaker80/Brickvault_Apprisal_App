# ExecPlan 099 — Phase 12 production acceptance

## Production continuation stopped before mutation, 2026-09-30

**BLOCKED — Step 4 detached repair approval cannot bind the failed run/candidate.
Catalog importer repair remains ACCEPTED / CLOSED. Production catalog activation
prerequisite BLOCKED; P12-05 BLOCKED; Phase 12 IN PROGRESS.**

Minimum live admission and exact failed-state admission passed. The exact retained
`p12-05-catalog-repair-r1` bundle passed manifest/source/wheel verification without
a rebuild. During preparation, inspection of the accepted
[approval validator](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/files/scripts/production_catalog.py#L231-L260) found only ten allowed fields: database,
purpose, repair/predecessor releases and manifests, source version/raw/provenance
digests, and migration head. It has no failed-run or candidate identity fields and
rejects extra fields. The continuation's Step 4 explicitly requires those identities
to be bound by that detached approval. Exact IDs supplied to a command are a
different binding mechanism and do not satisfy this required approval contract.

The continuation explicitly prohibits a new repair or improvised production fix.
No alternate approval, schema extension, wrapper patch or substitute artifact was
used. This conflict was discovered before the first production mutation; the
sequence stopped before Step 3's pre-recovery backup. Backups performed by normal
scheduled operations outside this slice are not counted as authorized slice runs.

| Gate | Result in this continuation |
| --- | --- |
| Exact retained artifact | PASS: release `p12-05-catalog-repair-r1`; manifest `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`; source ID `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344`; wheel `a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6` |
| Minimum live admission | PASS: expected VM 115, r6 current, revision 0016, admin/one owner, 13 health checks, retention READY, zero failed units/jobs/imports, trusted private HTTPS and loopback exposure |
| Storage headroom | PASS: 123,552,899,072 bytes free on database volume; database 3,140,015,807 bytes; release volume 20,942,417,920 bytes free |
| Exact failed-state admission | PASS: one provider/source/failed run/candidate, 12 files, exact 1,898,466 staging rows; audit/provenance/fingerprint unchanged; no canonical/validation/activation data; NULL active snapshot, generation 0 |
| Detached approval identity binding | BLOCKED: accepted validator has no failed-run/candidate fields and rejects additions |
| Pre-recovery backup | UNRUN: zero slice backup invocations |
| Repair installation / wrapper deployment / approval creation | UNRUN; local bundle verification alone passed |
| Guarded retirement / switch / one linked retry | UNRUN: zero invocations; the one authorized retry remains unused |
| Production statement timing / fingerprint continuity / structural validation | UNRUN: no production retry observation; accepted isolated evidence is unchanged |
| Activation / generation-one active catalog | UNRUN; active snapshot remains NULL, generation 0 |
| Installed number/name/detail/Watchlist/market behavior qualification | UNRUN; source-known set remains `75331-1`, The Razor Crest; no production application result claimed |
| Post-activation backup | UNRUN: zero slice backup invocations |
| Blocked-state preservation check | PASS: r6, original failed audit/candidate/source/files/counts/security/listeners/timeouts unchanged; all 13 health checks and active/enabled operational timers pass |

VM 115 already had eight CPUs and 16,384 MiB RAM at live admission. No allocation,
startup, PostgreSQL configuration, timeout, migration, grant, market-provider,
owner-state, client/device or Phase 13 changes were made. `statement_timeout`
remains 300,000 ms and `lock_timeout` 10,000 ms. Market observations remain zero.
WAN-forwarding inspection was not repeated after the stop; no fresh WAN gate is
claimed. Private IDs and protected configuration remain outside review evidence.

Only Plans 099/100/101 are changed on main. Main remains at
`0ea8e0e21156bebb9aa4150c270643a0a5d0d571`, index empty; all three protected dirty files retain their accepted
hashes and remain unstaged. The sanitized r4 publication includes the specific
approval contract proof and labels all downstream gates unrun. A separately
reviewed resolution of this approval-contract discrepancy is required before
production mutation. No repair or remaining P12-05 client gate starts here.

Earlier sections below retain dated implementation, authorization and evidence
history; this stopped-continuation status is current.

## Authorized catalog production continuation, 2026-09-30

Brian explicitly authorizes the accepted exact-artifact deployment, guarded
retirement of the preserved failed candidate, exactly one predecessor-linked
fresh retry, separate validated-snapshot activation, one pre-recovery and one
post-activation dual backup, and bounded installed search/detail/Watchlist
resolution. The catalog importer repair remains ACCEPTED / CLOSED. Catalog
activation production qualification is STOPPED / BLOCKED; P12-05 remains BLOCKED and
Phase 12 IN PROGRESS. This authorization supersedes the earlier production
continuation boundary below for this exact sequence only.

Main remains at `0ea8e0e21156bebb9aa4150c270643a0a5d0d571`, with an empty index
and the three protected files byte-identical and unstaged. Reuse accepted r2/r3
repair qualification. No rebuild, new repair, second retry, timeout/resource/
schema/grant change, manual production ANALYZE, market activation, client/device
acceptance, rollback/cold-start rehearsal or Phase 13 work is authorized.
Any stated stop condition preserves durable evidence and stops the sequence.
Sanitized stopped-continuation gate results are recorded above for catalog r4;
private identifiers and configuration stay in protected local production state.

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

## Goal and user-visible outcome

Qualify the accepted private production application and its real recovery paths.
P12-05 is authorized and **BLOCKED — production catalog unavailable**.
Phase 12 remains IN PROGRESS pending ChatGPT review.

## Why now

P12-01 through P12-04E are accepted and closed. This plan exercises the remaining
production acceptance gates without reopening their implementation campaigns.

## Scope and non-goals

In scope: minimal live preflight, current dual recovery point, Windows-initiated
Google Drive-only restore into an isolated PostgreSQL 18 cluster, fresh Windows
owner session, browser/PWA workflows, physical production Android, accepted
release rollback/forward, VM 115 cold start, logout/cleanup, and final dual backup.
No application source fixes, schema changes, provider onboarding, host reboot,
firewall VM mutation, destructive retention, main commit/push, or Phase 13 work.

## Repository state

Accepted main HEAD: `5c673e81a4f1caa13a0909a746d6ba0fffca075e`; index empty.
Protected dirty files remain unstaged and byte-identical:

| File | SHA-256 |
| --- | --- |
| AGENTS.md | F0A354ED80F631910F4CDCB64729209EF4758DE441F3EAAF509DA49395F969B4 |
| services/api/tests/integration/test_catalog_search.py | D06965D560361A06B7A33647EFA5B9B34829F8C34D5D912226D9CD5B3645ABF7 |
| services/api/tests/unit/test_catalog_parser.py | 0251B5C358CD37DE9E07E2CBDFB44913752CADE7050D9EB1B3A885F57D27A041 |

## Decisions and assumptions

Expected release `p12-04e-r6`, source ID
`00c719ac356f881c9929909a22f683831235f222939d28c8892747c8898558f5`, manifest SHA-256
`9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d`.
Normal trusted origin is `https://appraisal.abrianbaker.com`. The accepted absolute
immutable web directory must accompany every release pointer change.

## Data model and interfaces

No source, API, or migration changes. Require revision `0016_hunt_cached_runs`,
exactly one owner principal, and existing owner/runtime/marker/grant contracts.
Use a unique temporary Watchlist item and reversible Settings edits only after
real local owner login; remove/restore them before final backup.

## Implementation sequence and acceptance criteria

1. Verify immutable release, admin verification, services/timers, trusted private
   HTTPS/DNS, UFW/listeners, absent public records/WAN forwarding, repository
   identities, backup age, retention READY, and maintenance-job exclusion.
2. Select latest complete schema-2 receipt. Inspect its configuration identity;
   run exactly one normal backup only if it predates final r6 operations state.
3. Independently unlock protected Windows recovery context and stream all three
   Drive artifacts to a task-owned socket-only PostgreSQL 18 cluster. Recover
   globals/config/database, compare roles/grants/marker/revision/principal/table
   inventory and row counts; stop and remove disposable plaintext afterward.
4. Fresh Windows profile: local owner login, cookie metadata/no-store, real
   CSRF/Origin/Host positive/negative checks, core browser workflows and temporary
   Watchlist persistence. Preserve secrets only in private process memory.
5. Trusted production PWA install/standalone, alive-document offline read-only,
   fresh offline private-data absence, explicit reconnect and update checks.
6. Established production Android build, package/hash inspection, physical LAN
   TLS/auth/data/offline/reconnect; no test CA, localhost or adb reverse.
7. Verify accepted `p12-04d-r1` bytes; atomically rollback pointer and absolute web
   path, restart API, verify authenticated persistence; return r6 and restore
   paused operational timers. Require unchanged schema and healthy deep checks.
8. Read actual firewall/app startup ordering. Gracefully stop only VM 115, prove
   stopped from Proxmox, start it and qualify guest recovery. No host reboot.
9. Remove temporary data, restore Settings, logout browser/Android, verify old
   session replay rejection and private memory clearing.
10. Run exactly one final normal dual backup with six readbacks and repository
    checks; no retention apply/prune. Recheck final security/operations state.
11. Publish sanitized `astra_response/P12-05/r1/` on isolated `astra-response`;
    leave main uncommitted and its index empty.

## Security, privacy and integrity

No password/hash, cookie/token, marker, proxy secret, OAuth/restic material,
recovery run/snapshot ID, private IP/MAC, device serial or recovered plaintext
may enter chat or review artifacts. No persistent plaintext dump on Windows.
Production PostgreSQL must remain running and untouched by the isolated restore.

## Failure, rollback and recovery

A material acceptance defect stops the phase with a specific BLOCKED gate and
sanitized evidence; source fixes require separate review. A failed rollback must
first return to the recorded r6 pointer/web directory and verify recovery.
Task-owned isolated cluster/configuration must be stopped and cleaned safely.

## Progress log

- [x] 2026-09-30: Read authorization and accepted context; verify protected hashes.
- [x] Minimal live preflight and current recovery point.
- [x] Google Drive-only real restore and cleanup.
- [x] STOP: zero production catalog sets/snapshots; installed read-only search
  returns `catalog_unavailable` for number and name queries. No data activation.
- [ ] Browser/session/security workflows.
- [ ] PWA production acceptance.
- [ ] Physical Android production acceptance.
- [ ] Rollback and forward return.
- [ ] VM cold start and host startup reasoning.
- [ ] Logout/data cleanup, final dual backup and final security/operations.
- [ ] Documentation validation and review publication.

## Manual checks

Owner passwords are entered locally only. Pause for OWNER LOGIN INPUT REQUIRED,
PWA INSTALL INTERACTION REQUIRED, or PHYSICAL DEVICE INTERACTION REQUIRED when
that local action is necessary; resume this same conversation afterward.

## Acceptance evidence, 2026-09-30

### Preflight and selected recovery point

Exact r6 manifest and installed manifest-file hashes passed. Production-admin
verification and all 13 existing light health checks passed; zero failed units.
Backup, retention, certificate, health, Python and apt maintenance jobs were idle.
Both recovery repository identities passed. Retention was READY and the latest
complete schema-2 receipt was approximately 4.18 hours old with migration
`0016_hunt_cached_runs`, three artifacts and six snapshots.

Windows resolved the normal hostname to the expected private target; normal TLS
health returned 200. Public Google DNS A/AAAA answers were absent. Windows could
not connect to 18080 or 5432. The accepted listener/UFW/clock/mount/space checks
passed. Read-only OPNsense inspection found zero configured destination NAT and
one-to-one NAT entries; LAN anti-lockout rules were generated. WAN's explicit
rule was the existing ICMP ping rule, with no application TCP forwarding/allow.
The newer rules view showed that WAN rule and normal LAN rules. No router change.

The initial receipt's configuration lacked the final operational state. Exactly
one fresh normal production backup therefore ran: three artifacts, six matching
encrypted readbacks, both repository checks, and protected schema-2 receipt PASS.
Its configuration bytes matched every current required/optional backup file,
including r6 manifest, API/Caddy config, Gmail/health config and retention state.
That fresh receipt was selected privately; run/snapshot IDs are intentionally
excluded. No second pre-restore backup or final acceptance backup was run.

### Independent Google Drive restore — PASS

Windows independently unlocked its accepted protected recovery context and
matched the Drive repository identity. VM 115's Drive credentials were not used
for the restore. Windows restic streamed globals, database and configuration to
pinned SSH; each received artifact matched the selected receipt size and SHA-256.
There was no persistent plaintext Windows dump and no Proxmox repository fallback.

The disposable PostgreSQL 18 cluster used a 256 MiB tmpfs, separate data/socket
directories, port 55435 with empty listen_addresses, and no TCP listener. Available
RAM was approximately 7.1 GiB; the database artifact was under 1 MiB. A temporary
bootstrap superuser avoided collision while restoring postgres/owner/runtime roles.
Root-only recovered configuration recreated the exact database identity/owner/marker
inside this isolated cluster. Live `/var/lib/postgresql/18/main` was not stopped,
restored over, or used as a restore target.

All 76 per-table row counts matched source before and after the rehearsal. Schema
and object inventory/ownership, effective table ACLs, column grants, function
grants and default grants matched. Database PUBLIC privileges and owner/runtime
role attributes/memberships passed the accepted guard. Revision was
`0016_hunt_cached_runs`; exactly one owner principal existed. Recovered owner and
runtime passwords authenticated through SCRAM on the isolated socket, and runtime
least-privilege checks passed. No passwords, verifiers or marker were displayed.

Four disposable restore attempts used the selected existing fresh backup. The
first three stopped at an over-strict evidence-helper comparison of stored ACL
representation; diagnostic narrowing found only 12 catalog staging-table ACLs.
PostgreSQL can represent owner-only grants as an explicit ACL or as NULL/default.
The final helper expanded defaults using PostgreSQL acldefault and sorted grant
entries on both clusters. Every effective grant, object owner and object identity
then matched. No production/source/grant modification was made to obtain PASS.
A Windows closed-pipe reader warning in the first relay was also corrected only
in the ignored helper. Later relays completed without that warning.

Every attempt stopped the disposable cluster, unmounted its tmpfs and removed
the mount directory, restored configuration, database plaintext, source inventory,
guest relay and temporary receipt copy. Sanitized evidence only was retained for
the rehearsal. After final cleanup, live admin verification, exact manifest,
all 13 light checks and zero failed units passed.

### Blocking production data prerequisite

Live and restored counts both show zero catalog providers, sets, snapshots,
active snapshots, import runs and market observations. No owner session, saved
deal, Settings/profile or Watchlist record existed. This restore faithfully
reconstructs the provisioned production database; it does not prove recovery of
nonempty application datasets that have never been loaded into this deployment.

The installed r6 ProductService.search was exercised read-only under the real
runtime DB role with a set-number-shaped query and a name query. Both returned
the fixed `catalog_unavailable` code, without provider dispatch or data mutation.
[ProductService.catalog](r3-context.md#historical-local-source-references) requires
exactly one active accepted nonsynthetic Rebrickable snapshot. The production
database has none. [WatchlistService](r3-context.md#historical-local-source-references)
resolves additions through that same catalog. Therefore a known-set search,
Set Detail and a valid temporary acceptance Watchlist item cannot be qualified.
This is a missing production catalog activation prerequisite, not evidence of
database corruption, an incorrect restore, or a new application-source defect.

The phase stopped here. No fresh-profile owner login, cookie/CSRF/browser workflow,
PWA installation/offline test, Android build/device test, release rollback/forward,
VM cold start, logout/replay test or final acceptance backup was performed. No
temporary owner data was created, so no Settings or Watchlist cleanup was needed.
No owner password was requested or changed; prior logout qualification is not
claimed. The only Chrome work was read-only OPNsense inspection.

### Host ordering and current state

Read-only Proxmox configuration confirms firewall VM 112 onboot=1,
startup order=1,up=15 and application VM 115 onboot=1,order=2. VM 115 was running,
its guest agent responded and the expected reserved address matched. This orders
the firewall before the app with a 15-second startup delay; configuration alone
does not prove firewall readiness, actual host reboot, or P12-05 guest cold recovery.
Neither VM nor Proxmox was rebooted or stopped during this blocked run.

## Outcome and follow-up

**BLOCKED — production catalog unavailable; Part B core workflow prerequisite.**
Preflight, one fresh dual backup, Drive-only real restore and cleanup PASS.
No application/deployment source changes occurred. Only this plan and minimal
CODEX_WORKFLOW/ROADMAP status references changed; helpers remain ignored.
Main is uncommitted at the accepted HEAD with empty index and protected hashes
unchanged. Publish the blocker on `astra-response` under `astra_response/P12-05/r1/`.

Review must first authorize a bounded production catalog activation using an
accepted nonsynthetic source and confirmed provider/data rights, plus any market
evidence needed by the chosen economics workflow. Do not substitute synthetic
fixtures or silently import a development database. After that separate work is
accepted, resume the outstanding P12-05 gates in this conversation. P12-05 is not
READY or CLOSED; Phase 12 remains IN PROGRESS. No Phase 13 work began.

### Catalog prerequisite handoff, 2026-09-30

Brian separately authorized catalog-only activation in
[Plan 100](Plan-100.md) after the accepted P12-05 blocker
review `9df3ef2a492c988b614f1e7a6928f8ad5d1d2b9d`. The retained official source,
guarded invocation and sole pre-import dual backup passed. The import failed
during canonical build; PostgreSQL confirmed cancellation by the existing
five-minute statement timeout. Failed audit/candidate/staging remain; canonical
sets and accepted/active snapshots remain zero. No retry, activation, timeout
change or post-activation backup occurred. Production remains healthy with its
protected security and operations baseline unchanged.

Plan 100 is BLOCKED pending separately authorized importer root-cause repair and
reviewed recovery of the preserved failed state. No remaining Plan 099 gate was
resumed. Its earlier empty-catalog restore counts remain valid historical evidence,
not a statement that the failed import left the whole database unchanged.
Market provider activation remains excluded; the accepted manual sale-assumption
path is sufficient for later Deal Economics acceptance when market evidence is
unavailable. P12-05 remains BLOCKED and Phase 12 IN PROGRESS.


### Catalog repair review handoff, 2026-09-30

[Plan 101](Plan-101.md) separately authorized and
qualified the narrow source importer repair and truthful recovery/linked retry in
isolated PostgreSQL 18, using the full retained official source under unchanged
timeouts. It is IMPLEMENTED / READY FOR REVIEW; the production catalog prerequisite
remains BLOCKED pending acceptance and separately authorized continuation in
[Plan 100](Plan-100.md). Exact production failed state,
r6/0016/security/operations and owner timeouts remain unchanged. No production
recovery, retry, activation or remaining Plan 099 client/device/recovery gate ran.
P12-05 remains BLOCKED; Phase 12 IN PROGRESS; Phase 13 not started.
