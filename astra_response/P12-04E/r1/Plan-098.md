# ExecPlan 098 - P12-04E production operational hardening

## Goal and user-visible outcome

P12-04E is IMPLEMENTED / READY FOR REVIEW. Production now has complete-run
retention, private Gmail operational alerts, health and maintenance checks,
deliberate VM autostart, and one successful controlled guest reboot.
P12-04 remains IN PROGRESS; P12-05 remains NOT STARTED.

## Why this work is being done now

[Plan 097](context/accepted-p12-04d.md) is accepted/closed.
Its remaining operational gates are the explicit scope of Brian's P12-04E
instructions. This checkpoint does not perform production acceptance.

## In scope

Guarded complete-run retention; permanent pins; disposable destructive proof;
first live plan/NOOP; Gmail SMTP and failure integration; light/deep health;
official Python 3.13 patch detection; standard Ubuntu maintenance monitoring;
ACME notification decision; VM 115 autostart and one guest reboot; immutable
release identity; focused validation and sanitized isolated review publication.

## Explicit non-goals

No main commit/push, mutation of accepted p12-04d-r1, live backup deletion/prune,
migration/bootstrap, certificate issuance, automatic Python replacement,
automatic guest reboot, Proxmox reboot, owner login, browser/PWA/physical Android
acceptance, real production restore, rollback or disaster-recovery acceptance.

## Current repository state

Main HEAD remains `389a30e0ba4cdf6902d48e06277cc6ef1bc2fc6c`; index empty.
AGENTS.md and the two protected catalog tests remain byte-for-byte unchanged
from their accepted dirty baseline, unstaged and excluded from the package.
Implementation is uncommitted on main. Publication alone uses astra-response.

Final immutable release: `p12-04e-r6`.

- Reviewed source ID: `00c719ac356f881c9929909a22f683831235f222939d28c8892747c8898558f5`.
- Manifest SHA-256: `9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d`.
- CPython 3.13.15 under /opt/python/3.13.15; uv 0.12.10.
- Manifest schema 3 binds operations tools, service/timer/drop-in files and the
  certificate hook; verification still accepts schemas 1 and 2.
- BVA_WEB_BUILD_DIR is the absolute immutable release web directory. It must
  never be /opt/brickvault/current/web because the static loader rejects symlinks.

## Decisions and assumptions

No approved alert configuration existed initially. Work stopped at ALERT
DESTINATION REQUIRED. Brian selected private email, explicitly selected Gmail,
and entered a dedicated app password locally through hidden input. Gmail
accepted the single synthetic TEST. The private recipient is never published.

No permission was given to use the address for ACME registration. Keep the
existing absent ACME contact. Renewal service failures, inactive renewal timer,
deploy-hook failure and served-certificate expiry are independently covered by
the operational alert path. No ACME account/certificate change was made.

## Data model and API/interface changes

No application API or database migration. The equivalent retention interface is:

`/opt/brickvault/current/api/venv/bin/python /opt/brickvault/current/deploy/complete_run_retention.py plan`

Use `apply --digest <reviewed-plan-digest>` only under applicable deletion
authority. `scheduled` is reserved for the approved weekly unit. `prune --digest
<reviewed-current-digest>` is a separate explicitly supervised operation, never
an automatic consequence of forget. No live prune occurred here.

### Complete-run algorithm and recovery

One policy item comprises a structurally valid protected schema-2 production
receipt and all three artifacts (database.dump, globals.sql, configuration.tar)
in both independently identified repositories. The planner rejects missing,
extra, malformed, overlapping or ambiguous snapshot identities and changed
receipt/pin metadata. Snapshot paths and tags must match the complete run.

Sort by verified UTC time and then run ID. Keep the newest run in each of the
latest 30 distinct UTC days, 8 ISO weeks and 12 calendar months; take their union
and add permanent pins. The two accepted production recovery points and both
synthetic canaries are permanently pinned. Sparse history retains available
buckets; overlapping policies do not produce artifact-level decisions.

The plan digest binds policy, UTC date, exact keep/delete sets, repository
identities, all receipt digests, complete snapshot metadata, pins and ledger.
Apply gathers again and requires the exact digest. Before deleting anything it
reads back every selected artifact from both destinations and rechecks the plan.
Only the three explicit snapshot IDs for a selected complete run are forgotten
at each destination. Exact surviving snapshot inventories and restic check follow
each destination. Backup, retention and deep planning share a protected flock.

Before any destructive call, persist a DEGRADED ledger and exact transaction
intent. After each successful destination, persist progress. Only complete
success returns READY. First-destination failure, partial cross-repository failure,
interruption or failed post-check leaves durable DEGRADED state and stops all
further deletion. No destructive retry is automatic. Normal configuration reads
remain capped at 64 KiB; retention evidence/ledger reads have a bounded 16 MiB
limit so full snapshot evidence remains readable as history grows.

Pins: /etc/brickvault/backup/retention-pins.json, root:root 0600.
Ledger/transactions: /etc/brickvault/backup/retention/, root:root 0700, files 0600.
Receipts remain available after logical deletion and their digests stay in the
ledger. Protected records use exclusive temporary creation, fsync and atomic
replacement. Raw IDs remain only in protected local evidence.

Operator repair after DEGRADED: stop the retention timer; preserve ledger,
transaction and both repository inventories; establish which operations really
completed, verify pinned history and repository integrity, and review a concrete
recovery/reconciliation plan with Brian. Never clear DEGRADED or replay deletion
blindly. Prune requires READY, unchanged current plan, zero pending candidates,
and prior completed deletion/readback/check evidence; it also persists failure
state before mutation. There is no prune timer.

Six initial retention tests passed (313.085 seconds), including actual forget
against disposable LOCAL Linux restic repositories, complete-run/pin preservation,
changed plan, incomplete/ambiguous history, first-destination and partial
cross-repository failures, and degraded refusal. A later focused Linux root-file
regression proved large protected-state roundtrip, size bounds and permission
refusal; the two policy tests also passed again. No production deletion occurred.

First live invocation: PLAN keep=3, delete=0, digest
`65c14383b67e90edf7e59b8a6b4ff43ec3b7c3b3c156a36e904ab8bb4be5ff7b`.
Digest-bound apply returned NOOP. Ledger remains READY with no deleted runs.
Weekly retention was enabled only after all required disposable and live gates.
Future scheduled runs may apply the reviewed complete-run policy under the
explicit P12-04E authorization; that is distinct from this checkpoint's NOOP.

### External alerts and health

Gmail SMTP uses smtp.gmail.com:465, certificate-verified implicit TLS and a
20-second socket timeout. Root-only configuration is under
/etc/brickvault/operations/. No credential is passed in argv or logged. Messages
contain fixed generic categories only. Protected persistent state distinguishes
PENDING, ACCEPTED and FAILED; accepted categories deduplicate for six hours and
failed/uncertain attempts back off ten minutes. TEST cannot be sent twice.
Gmail SMTP acceptance proves transport acceptance, not that Brian read the mail.

OnFailure covers backup, retention, repeated API failure, Caddy, Certbot,
light/deep health and Python checks. The certificate deploy wrapper alerts on
hook failure while preserving its nonzero result. Service sandboxes receive no
application EnvironmentFile. Real activation API/health/Python failures also
exercised failure notifications; the final stack is healthy.

Light health checks credential-free exact-host trusted HTTPS, exact certificate
SAN and >21-day validity, services/timers, loopback API/DB and approved listeners,
pg readiness/data mount UUID, recent complete receipt (<36 hours), retention READY,
release/manifest/runtime/hook bytes, UFW, clock, guest agent, free space (>=10%,
root >=2 GiB and data >=5 GiB), reboot-required age (<48 hours), and apt policy.
The Linux ss interface suffix is normalized before checking the explicit allowed
endpoints; unexpected loopback and non-loopback ports still fail.
Daily deep health additionally reads both repository identities and validates
complete snapshot/receipt/pin history. Frequent checks do not run restic check.
All probes are owner-credential-free. Healthy health runs are quiet; failures
emit sanitized categories, exit nonzero and invoke external alerts. A stopped
VM cannot send its own alerts; independent whole-host availability monitoring
is not claimed by this guest-local implementation.

### Schedules and runtime maintenance

The verified guest timezone is Etc/UTC. Enabled/active schedules:

| Timer | Cadence |
| --- | --- |
| brickvault-health | 10 minutes after boot and each invocation, up to 30 seconds jitter |
| brickvault-health-deep | Daily 08:15 UTC, up to 15 minutes jitter |
| brickvault-retention | Sunday 09:15 UTC, up to 15 minutes jitter |
| brickvault-python-version | Sunday 10:15 UTC, up to 15 minutes jitter |

Accepted backup and Certbot schedules remain enabled/active. Deep work follows
the established backup window. Calendar operations timers persist missed runs.

Python detection uses only https://www.python.org/downloads/source/ with normal
TLS, same-official-host redirects, bounded compressed and expanded HTTP response
sizes, identity/gzip decoding and final 3.13.x release links. Three bounded lookup
attempts precede failure. Newer patches or repeated lookup failure alert; nothing
is downloaded/installed automatically. Live installed=latest=3.13.15, CURRENT.
The official index and https://www.python.org/downloads/release/python-31315/
are the source authority; no third-party version service is consulted.

Future separately reviewed Python update procedure:

1. Fetch the official Python.org signed source release.
2. Verify its published SHA-256.
3. Verify the release-manager signature with the independently established key.
4. Install into a new versioned /opt/python/<version>, leaving /usr/bin/python3 alone.
5. Create a new immutable release venv from that interpreter and locked dependencies.
6. Run targeted application, installed-wheel, static-build and operational checks.
7. Atomically activate the reviewed release with the absolute immutable web path.
8. Retain the prior interpreter/release for a separately authorized rollback.
9. Remove old versions only after later review.

Ubuntu's existing unattended-upgrades is installed; apt-daily and
apt-daily-upgrade are enabled/active. Periodic package-list refresh and unattended
security upgrades are enabled. Automatic reboot is disabled by policy/default;
no third-party update manager was added. Reboot-required older than 48 hours
fails health and alerts. No reboot-required flag remained after the controlled
reboot. A package request alone does not authorize a reboot.

### VM autostart and controlled reboot

Proxmox discovery confirmed firewall VM 112 (opensense) onboot=1 with
startup order=1,up=15 and the existing application VM 107 at order=2.
After unattended readiness passed, only VM 115 was changed to onboot=1,
startup order=2. Configuration readback passed. Proxmox was never rebooted.

Before the single reboot: recent production backup, alerts, light/deep health,
maintenance state, retention READY and no failed units passed. Backup,
retention, certificate and apt jobs were idle; schedulers were drained without
interrupting jobs. A protected once-only intent and boot ID were recorded.

After reboot: boot ID changed, VM returned, the same reserved IP and interface
MAC were observed through guest-agent readback, and key-only pinned SSH worked.
Data mount, PostgreSQL, API, Caddy, trusted HTTPS health/app 200, UFW, clock,
all eight backup/cert/operations/apt timers, guest agent and listener checks passed.
Light/deep health and official Python check passed again; failed units=0.
This is one guest reboot test, not a Proxmox host boot or disaster-recovery test.

## Implementation sequence

1. Verify main/protected state and accepted live target; resolve alert destination.
2. Implement bounded operations tools and focused tests, using local hidden secrets.
3. Exercise destructive retention only on disposable repositories.
4. Package/install a new immutable release; pin live history; first PLAN and NOOP.
5. Prove Gmail acceptance and operational units, health and maintenance checks.
6. Resolve startup dependencies; gate and perform one guest reboot; verify recovery.
7. Publish sanitized r1 evidence without committing main or beginning P12-05.

## Validation and acceptance criteria

Actual focused evidence: 6 initial disposable/policy retention tests; 1 later
protected-state regression plus 2 policy reruns; 6 alert tests; 6 health/Python
tests; 8 manifest tests; 18 existing backup unit tests. Linux persistent alert
state/dedup/backoff/permission checks passed separately. API package build and
installed-wheel check passed. Targeted Ruff/format/strict mypy and systemd-analyze
verify passed. Regression checks covered IPv4 interface suffixes, unexpected
listeners, official gzip HTTP, decompression size bounds and large retention state.
Live PLAN/NOOP, SMTP acceptance, installed light/deep/Python units, onboot readback
and post-reboot verification passed. No broad historical suites were run.

## Security, privacy, and data-integrity considerations

Published evidence excludes real email, passwords, webhook/tokens, IP/MAC,
run/snapshot/pin IDs, owner data and recovery media identifiers. Configuration
stays root-only, and the production backup now includes the actual protected
Caddy environment path plus operational configuration in its encrypted archive.
No new production backup was forced; the accepted schedule remains responsible
for the next capture. Shared backup/retention locking serializes mutation.

## Failure modes, rollback, and recovery

Stop on failed live alert, ambiguous/pinned/partial history, unexpected current
live candidates, official-source uncertainty, unsafe startup dependencies,
failed guest recovery or lost private API/TLS/DNS. Never silently retry destructive
retention or prune. Prior immutable releases and interpreter remain available.

Activation initially supplied a symlinked web directory and the existing loader
correctly refused it. Work stopped under Brian's explicit API-failure condition.
Brian approved the exact absolute-path repair and resumption; API/private HTTPS
recovered without relaxing the loader. Subsequent same-scope corrections fixed
ss suffix parsing and gzip decoding. Final review corrected the retention state
size bound. Each executable revision used a new immutable release; r6 is final.
The temporary activation outage is resolved, not an outstanding gate.

## Progress log

- [x] 2026-09-30: Main/index/protected hashes and minimum live target verified.
- [x] 2026-09-30: Destination stop resolved; hidden Gmail configuration and one
  remotely accepted TEST completed.
- [x] 2026-09-30: Disposable retention deletion/failure proof; protected live pins;
  first PLAN keep=3/delete=0 and NOOP; no live forget/prune.
- [x] 2026-09-30: Immutable release r6; approved static-path recovery; operational
  failure integration, light/deep/Python and Ubuntu checks passed.
- [x] 2026-09-30: Proven startup order; VM 115 onboot=1/order=2; one reboot and all
  required post-reboot checks passed.
- [x] 2026-09-30: Focused source/package/static/unit verification completed.
- [x] 2026-09-30: Sanitized P12-04E r1 evidence prepared for isolated publication.

## Open questions or physical-device/manual checks

Independent ChatGPT review of P12-04E remains required. All P12-05 gates remain
open: owner login/session/cookie issuance and auth/CSRF/Host/Origin acceptance;
full private browser acceptance; PWA install/offline/reconnect; physical Android
production TLS; real off-host production restore; release rollback rehearsal;
end-to-end disaster-recovery acceptance. None was started or claimed here.

## Outcome and follow-up

READY FOR P12-04E REVIEW. P12-04E IMPLEMENTED / READY FOR REVIEW;
P12-04 IN PROGRESS; P12-05 NOT STARTED. Main remains uncommitted/unpushed,
index empty and protected dirty files preserved. Review publication is limited
to astra_response/P12-04E/r1/ on astra-response. Only subsequent accepted review
can close this checkpoint; completion does not authorize P12-05.
