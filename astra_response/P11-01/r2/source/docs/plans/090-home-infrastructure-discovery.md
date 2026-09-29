# ExecPlan 090 — P11-01 read-only home infrastructure discovery

**Status: P11-01 ACCEPTED / CLOSED; Phase 11 CLOSED.** ChatGPT accepted the
published r1 discovery evidence. Phase 12 is NEXT / NOT STARTED and requires
separate explicit authorization before any infrastructure or production change.

## Goal and user-visible outcome

Record one bounded read-only inspection of the existing home hosting path and
give Brian one concrete, conditional private deployment design to review for
Phase 12. The observations below describe a reachable guest, not the unseen
Proxmox node or a qualified production service.

## Why this work is being done now

[Phase 10](089-local-packaged-release-readiness.md) closed local packaging,
security and disposable recovery checks. Home placement, backup and HTTPS
depend on actual infrastructure. P11-01 separately authorized read-only
discovery of the workstation and existing home Proxmox/Dell hosting access;
it did not authorize installation, configuration, deployment or production
data access.

## In scope

- Existing workstation SSH/network configuration and one already configured,
  authenticated home VM connection.
- Read-only guest facts relevant to compute, storage, network, existing
  services, proxy and backup patterns.
- Existing public authoritative DNS provider and repository production
  prerequisites, without provider login or changes.
- A conditional Phase 12 topology, change sequence, approval boundary and
  unresolved facts.
- A sanitized report-only review package on `astra-response`, explicitly
  authorized for P11-01.

## Explicit non-goals

No Proxmox/router/firewall/switch/Cloudflare login beyond access already
configured and working; no subnet or unknown-host scan; no raw configuration
or credential collection; no benchmark. No package install, pull, service
start/restart, VM/storage/network/DNS/certificate change, database query or
migration, deployment, application test/build, main push or Phase 12 work.

## Current repository state

At discovery start, `main` HEAD was
`03ab154a7dbbf9b6aaee3c877c3a400732c6fd96` (Phase 10 closeout), and the
index was empty. `AGENTS.md` and two catalog tests were pre-existing dirty
files; their original bytes and unstaged state are protected. Phase 10's local
release and TEST-only recovery evidence is reused, not rerun. Source remains
restricted to local development and TEST runtime targets.

## Observed environment

Evidence labels below are sanitized command summaries. Guest measurements
were one-time readings and do not establish physical host capacity.

| Component | Observed fact | Evidence/command | Confidence |
| --- | --- | --- | --- |
| Workstation path | Windows has OpenSSH and an existing private-address SSH target for a home VM. The configured Proxmox alias contains a placeholder hostname; the known `proxmox` name had no A record. No new login was attempted. | Filtered `~/.ssh/config`, `Get-Command ssh`, `Resolve-DnsName proxmox`. | High for local state; no conclusion about the node itself. |
| Guest identity | The reachable guest is Ubuntu 24.04.4 LTS under KVM. It has 64 assigned vCPUs and 125 GiB assigned RAM; `free` reported 122 GiB available at observation time. These are guest allocations, not spare Dell/Proxmox resources. | Existing SSH with batch/strict host-key checking; `/etc/os-release`, `systemd-detect-virt`, `nproc`, `free -h`. | High for guest; host capacity unknown. |
| Guest storage | Root is ext4 on LVM over a 300 GB virtual disk, with 292 GB filesystem size and 199 GB free. A separate 200 GB virtual disk is unmounted and has no filesystem shown by `lsblk`; its ownership and contents were not examined. No NFS/CIFS/ZFS/Btrfs guest mount was listed. | `df -hT /`, `lsblk`, `findmnt` for named filesystem types. | High for current guest view; disk and host-pool ownership unknown. |
| Guest network | The VM uses a private `/24` address via a gateway that also supplies DNS. The workstation reaches it through its explicit SSH address; workstation DNS did not resolve the VM alias. Bridge, VLAN, firewall and WAN exposure are not visible from these facts. | `ip -br -4 addr`, `ip -4 route`, `resolvectl dns`, targeted workstation DNS check. | High for guest address model; low for wider network. |
| Existing workload | A legacy BrickVault backend runs as a systemd service with automatic restart. PostgreSQL 16 is active and listens on guest loopback port 5432. Other listeners include the legacy app ports. The existing database/service were not queried or altered. | `systemctl list-units`, filtered `systemctl show`, `ss -ltn`, `psql --version`. | High for guest service state at inspection. |
| Proxy/HTTPS | Caddy, nginx, Traefik and Apache units were inactive on this guest, and no guest port 80/443 listener appeared. This does not rule out a proxy on another host. | `systemctl is-active` for four named units, `ss -ltn`. | High for this guest only. |
| DNS authority | The existing public domain resolves publicly and its authoritative nameservers are Cloudflare. No private subdomain, split-DNS override, DNS-01 rights or certificate deployment was inspected. | Targeted `Resolve-DnsName` A/NS queries; no Cloudflare login. | High for current public DNS delegation only. |
| Backup | `pg_dump` is present. No Restic/Borg or application backup unit/timer, and no remote filesystem mount, was observed on this guest. The routine package database timer is not an application backup. Proxmox VM backup, off-host targets and retention remain unknown. | `command -v`, filtered `systemctl list-unit-files/list-timers`, `findmnt`. | Medium: absence is limited to inspected guest mechanisms. |
| Application release boundary | API settings accept only `development`/`test`, fixed loopback database ports/targets and loopback bind/Host/Origin. Android's special HTTPS target is a localhost TEST qualification path. The ordinary web transport uses same origin. | `services/api/src/brickvault_api/settings.py`, `observability.py`, `apps/web/src/api-transport.ts`, `apps/android/capacitor.config.json`. | High for checked-out source; no production runtime tested. |

## Unknown / not authorized

1. **Proxmox node:** identity/version, real CPU/RAM headroom and contention,
   VM/LXC inventory, bridge/VLAN attachment, firewall, storage pools/types,
   free capacity, backup jobs and restore targets. The workstation's
   `proxmox` alias has a placeholder rather than a usable hostname, and
   targeted DNS did not resolve it. Access must be separately restored or
   those facts supplied for review; no host guess or network scan is allowed.
2. **Guest's extra disk:** the 200 GB device has no displayed mount/filesystem;
   it was not opened, initialized or treated as free space. Ownership and
   intended use need owner/Proxmox confirmation before any storage decision.
3. **Proxy and internal DNS elsewhere:** no proxy runs on the inspected guest,
   but another host, gateway or tunnel could host one. The gateway's split-DNS
   capability, current certificates and WAN rules were not inspected because
   router/firewall and external control-plane logins were outside this pass.
4. **Backup destination:** Proxmox backup schedules, off-host storage,
   retention, restore permissions and available capacity were inaccessible.
   The guest's `pg_dump` binary does not prove a functioning backup system.
5. **Production identity and data:** exact private hostname, initial data
   selection (fresh production database versus an approved migration), account
   bootstrap method and provider credential activation require Phase 12
   decisions and approval. No production data or credentials were accessed.

## Decisions and assumptions for the Phase 12 proposal

**Choose a dedicated Ubuntu VM on the existing Proxmox estate, subject to
node capacity and backup-pool confirmation.** The observed Ubuntu/KVM guest
proves that this guest pattern works locally; co-hosting the new app with its
active legacy backend and PostgreSQL would create avoidable service and data
coupling. An LXC offers no demonstrated benefit for this single-user workload.
This is a design choice, not an assertion that the unseen node has capacity.

Initial reservation proposal: **4 vCPU, 8 GiB RAM, 32 GiB OS volume and
128 GiB PostgreSQL data volume** on a pool that the later backup design can
protect. The existing catalog acceptance database measured about 6.4 GB with
retained staging ([catalog operations](../CATALOG_IMPORT.md)); the proposed
data volume is headroom, not a measured production maximum. Confirm host
contention, growth and usable pool before VM creation. Do not use the
existing guest's unmounted disk by inference.

## Recommended Phase 12 topology

- **Network:** attach the new VM to the confirmed private home bridge/VLAN,
  with a stable private address. No WAN forwarding. Permit HTTPS only from
  Brian's approved private clients; permit management only from the approved
  admin path. The precise bridge/VLAN and firewall mechanism await node review.
- **Application:** install a pinned release of the single FastAPI API plus
  verified React build in separate release directories on the new VM. Run one
  restricted systemd API service bound to guest loopback. It serves the built
  web/PWA assets and `/api`; no separate worker, queue, broker or object store.
- **Database:** use one dedicated PostgreSQL cluster/data volume on that VM,
  reachable by the application over a Unix socket or loopback only. Keep it
  distinct from the existing VM's PostgreSQL 16 service and never publish a
  database port. Use reviewed Alembic migrations and least-privilege roles.
- **HTTPS and name:** one private DNS name under the approved domain resolves
  only on the home network to the new VM. Place Caddy on that VM as the sole
  HTTPS entry point, proxying to loopback FastAPI. Use a publicly trusted
  certificate via DNS-01 with a narrowly scoped Cloudflare token, subject to
  verified rights and an approved credential path; do not rely on the Android
  localhost TEST trust mechanism. No public A record or inbound WAN port is
  proposed. Verify the home DNS resolver can serve the private override.
- **Operations:** systemd starts/restarts the pinned app service; journald
  retains sanitized operational logs. A private monitor checks non-sensitive
  `/api/health` and an authenticated readiness check, with disk and backup
  failure alerts. Preserve the prior application release for quick app rollback.
- **Backup/recovery:** take scheduled encrypted PostgreSQL custom-format
  backups plus required role/configuration material to a verified off-host
  destination, with retention and an approved restore drill. A Proxmox VM
  backup may complement this, but a VM snapshot alone does not prove a
  consistent database restore. Back up before schema changes and validate a
  disposable restore against current migration/runtime grants and private
  saved-work readback, as Phase 10 demonstrated only with TEST data.

## Data model and API/interface changes

No Phase 11 schema, API or application change. **Phase 12 cannot deploy this
checkout unchanged:** `settings.py` and database target validation have no
production purpose, while `observability.py` rejects a private subdomain's
Host/Origin and has no reviewed single-proxy HTTPS trust path. Phase 12 must
implement and verify a production configuration mode, exact hostname/Origin,
Secure cookie and trusted-proxy behavior, database ownership/least privilege,
and a production Android transport to the approved HTTPS origin. Keep the
current development/TEST restrictions intact and do not promote qualification
exceptions to production. Any new schema migration needs its own reviewed
scope; none is proposed by discovery.

## Phase 12 change plan (not executed)

| Category | Required later change and gate |
| --- | --- |
| Workload creation/config | Verify node resources and pool, then create the dedicated VM/disks; install OS, pinned PostgreSQL, API release and Caddy; create restricted service accounts and systemd units. |
| Network | Approve exact bridge/VLAN, private address, host/guest firewall rules, management path and client reachability; verify no WAN ingress and no PostgreSQL listener outside loopback/socket. |
| DNS/HTTPS | Approve exact hostname, private DNS override, Cloudflare DNS-01 rights/token storage, certificate issuance/renewal and proxy configuration. Confirm HTTPS from browser and Android with normal platform trust. |
| Secrets | Generate/store production DB/auth/provider and DNS-01 credentials outside source/static assets/logs; approve owner bootstrap and rotation/revocation procedure. Do not copy TEST secrets. |
| Database/data | Create dedicated cluster, roles and database; apply reviewed migrations after backup; decide explicitly whether to start empty or migrate approved existing data. No access to the legacy PostgreSQL service is implied. |
| Backup | Select and verify off-host destination/retention/encryption; configure scheduled database plus role/config backups and optional VM backup; complete an owned disposable restore before acceptance. |
| Monitoring | Configure service and backup alerts, private liveness/readiness, disk capacity thresholds and log retention/redaction. |
| Validation | Implement/verify production runtime and Android transport first; review package hashes, test Host/Origin/CSRF/cookie/TLS boundaries, migration/readiness, private DNS/no WAN/no DB exposure, browser/PWA/approved Android path, backup restore and app rollback. |

## Implementation sequence for later approval

1. Resolve Proxmox, proxy, DNS and backup unknowns; reconcile this topology
   with actual node capacity and existing home hosting standards.
2. Review and implement the production runtime/transport changes with focused
   security tests and a normal release build. Keep development/TEST behavior.
3. Present exact VM, storage, network, DNS, secrets, data and backup changes
   with rollback steps to Brian for **distinct Phase 12 execution approval**.
4. Only after approval, provision the VM/private path, install the pinned
   release, initialize owned data, back it up and validate HTTPS/auth/restore.
5. Record actual results and only then decide whether Phase 12 can close.

## Validation and acceptance criteria

For **P11-01**, inspect the complete documentation diff including this new
file, check Markdown links and roadmap/workflow/traceability consistency, run
`git diff --check`, and verify original HEAD/index and protected SHA-256 bytes.
Publish only sanitized review-package files, then verify remote commit and
read back `REVIEW.md`. No application build, test, device check or production
probe belongs to P11-01. Phase 12 acceptance requires the separate live checks
above; this plan provides no such evidence.

## Security, privacy and data integrity

The public repository and review package must omit SSH keys, credentials,
MACs, serials, public/exact externally identifying addresses, raw configs,
full network inventories and unnecessary device IDs. The table therefore
generalizes the private subnet and SSH destination. PostgreSQL stays private;
provider secrets remain server-side. Application auth, CSRF, Host/Origin and
Secure cookie checks must succeed through the approved HTTPS path before any
non-loopback access. Android TEST certificate/localhost mechanics provide no
production trust or routing evidence.

## Failure modes, rollback and recovery

This discovery made no infrastructure change to roll back. Phase 12 must
preserve the prior release, take a verified pre-migration database backup,
define schema compatibility before app rollback, and use a tested restore
procedure for incompatible changes. If capacity, off-host backup, private
DNS/certificates or the production runtime gate cannot be proven, stop before
exposure or cutover. Do not substitute the existing VM's unverified spare disk
or a VM snapshot for those missing prerequisites.

## Phase 12 approval boundary

Brian must approve the exact host/VM and resource allocation; VM/disk creation;
OS/package and application installation; service starts/restarts; bridge,
address, firewall and routing changes; private/public DNS and Cloudflare
access; certificate issuance/renewal; credential generation/placement and
account bootstrap; database/role creation, migration and any data copy;
backup target/retention and restore drill; monitoring; release cutover and
rollback; and any Android device/network qualification. P11-01 authorizes none
of these operations. Publication of this report is not such approval.

## Risks / blockers grounded in this pass

- **Host-placement gate:** the Proxmox alias is unusable, so node capacity,
  pools, VM conflicts and backup policy are not verified. The proposed new VM
  must not be created until those facts are reviewed.
- **Operational gate:** no existing proxy or application backup was observed
  on the reachable guest, and equivalent services elsewhere remain unknown.
  The private DNS/certificate and off-host backup paths need confirmation.
- **Release gate:** current source rejects production database/hostname
  configuration; the Android route is TEST-only. Phase 12 needs reviewed
  implementation and validation before exposure, not a configuration bypass.
- **Legacy isolation:** the reachable guest already hosts a live backend and
  loopback PostgreSQL. Do not reuse its database, ports or unmounted disk.

## Progress log

- [x] 2026-09-28: Confirmed Phase 10 HEAD, empty index and original protected
  hashes; read current repository guidance and local release handoff.
- [x] 2026-09-28: Completed one bounded read-only workstation/home VM and
  source prerequisite pass; recorded inaccessible Proxmox facts as unknown.
- [x] 2026-09-28: Drafted conditional Phase 12 topology and explicit approval
  boundary for review; no Phase 12 action performed.
- [x] ChatGPT accepted the published P11-01 r1 evidence and authorized this
  documentation-only Phase 11 closeout.

## Open questions and manual checks

Obtain the Proxmox node facts, bridge/pool and backup inventory through
approved access or a supplied read-only export; identify any existing proxy,
private DNS and off-host backup standard. Brian must select the exact hostname,
initial data policy and intended Android production access before Phase 12's
execution plan is final. These are review prerequisites, not requests for
credentials in chat.

## Outcome and follow-up

P11-01 is ACCEPTED / CLOSED and Phase 11 is CLOSED with the unknowns above.
The proposed deployment remains conditional. Phase 12 is NEXT / NOT STARTED;
this document provides no authorization for infrastructure or production
change.
