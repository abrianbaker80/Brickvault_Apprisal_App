# ExecPlan 092 — P12-02 exact infrastructure pre-mutation review

## Goal and authority

P12-01 is accepted. P12-02 was explicitly authorized on 2026-09-29 for one
configured-key SSH access check, bounded read-only Proxmox discovery, deployment
decisions, and this review package. **P12-02 remains in progress and pending
ChatGPT review. No P12-03, P12-04, or P12-05 mutation is authorized.** This plan
records what a later approval would cover; it does not request or perform an
infrastructure change. [ExecPlan 091](091-production-runtime-and-deployment.md)
remains the accepted P12-01 source/runtime record. Its separate P12-03 base
provisioning, P12-04 application/data deployment, and P12-05 acceptance gates
remain separate even though the full future mutation order is shown here.

## Scope and method

Read only the configured `proxmox` SSH alias and the known node's Proxmox/Linux
configuration. No LAN scan, alternate authentication, guest-file access,
legacy PostgreSQL access, provider call, backup run, install, service change,
or production secret was used. The configured noninteractive SSH authentication
succeeded once as root on node `pve`; subsequent SSH sessions ran only the
read-only inventory commands listed in the sanitized review receipt. The local
main HEAD and index stayed at `c91f0bb2f76497dcf69a5f9887c885871871ddb9`
and empty; the three pre-existing protected dirty files were left unstaged and
byte-for-byte unchanged.

## Observed infrastructure facts

These are a 2026-09-29 snapshot, not reserved resources or deployment proof.
Precise device identifiers, MACs, management addresses and raw firewall/network
configuration are intentionally absent from this publishable plan.

| Area | Read-only finding | Planning consequence |
| --- | --- | --- |
| Node | `pve`, standalone (no Corosync cluster configuration); PVE `9.1.6`, kernel `6.17.13-2-pve` | One selected node; no cluster failover is available. |
| CPU/load | 2 Xeon E5-2695 v4 sockets, 36 physical cores/72 logical CPUs; load 0.57/0.72/0.77 during the pass | Four more vCPUs are plausible, but running guests already assign 77 vCPUs; recheck contention at execution. |
| RAM | 188.8 GiB total, about 40.2 GiB used and 148.6 GiB available at the snapshot | Running guests assign about 144.5 GiB maximum; adding 8 GiB fits physical RAM on paper, subject to a fresh check. |
| Inventory | VMIDs 100–114 and 201–202 exist; running 107 legacy `brickvault-vm`, 112 firewall VM, and LXCs 113/114. VMID 115 was the next available ID at the pass. | Do not reuse VM 107, its database, or its unmounted disk. Recheck 115 immediately before creation. |
| Storage | `local-zfs` supports VM images and has about 381 GiB available; its `rpool` is online but has one observed leaf device. `sas_raid0_lvmthin` supports VM images and has about 6.93 TiB available; its name denotes a RAID0 pool. `local` supports ISO/templates/backups and shares the host `rpool`; parent `sas_raid0` reports no allocatable free space. | Prefer both new disks on `local-zfs` for the initial 160 GiB allocation, leaving about 221 GiB reported free before growth/snapshots. Neither pool nor `local` is an off-host recovery destination. |
| OS media | `local:iso/ubuntu-24.04.2-live-server-amd64.iso` is present. | A reviewed Ubuntu Server 24.04.2 install can use existing media; verify its provenance/hash before boot. |
| Network | `vmbr1` is active, private and attached to a physical uplink. The existing BrickVault VM and running LXC 113 use it; LXC 113 is configured for DHCP. No VLAN-aware setting or tag was observed for this path. `vmbr0` and portless `vmbr10` also exist. | Select untagged `vmbr1`; stable address reservation and approved client/management source ranges remain to be confirmed. Do not modify bridges. |
| Firewall | Proxmox firewall reported `disabled/running`; node `enable=0`. A NIC-level `firewall=1` flag on an existing VM does not prove enforcement. | Guest firewall and an approved upstream private-access rule are required before exposure; do not assume Proxmox is filtering. |
| VM backup | No Proxmox backup jobs; `local` is the only observed backup-capable storage; no PBS storage was configured. | Brian selected encrypted database copies on Proxmox and Google Drive. A separate VM-level backup is deferred until an encrypted target, access/capacity policy and restore path are reviewed. A plain `local` archive cannot satisfy encrypted or off-host recovery. |
| Proxy/DNS | LXC 110 named `proxy-ddns` is stopped. P11-01 observed no active reverse proxy on the legacy guest. The workstation resolves known `pve.local` and uses its default gateway as DNS; that does not prove which DNS service manages new records. P11-01 found public-domain delegation to Cloudflare. No existing private override or DNS-01 authority was verified. | Place Caddy in the new VM. Private DNS service, Cloudflare rights, certificate issuance/renewal and Android private reachability remain unresolved. |

No guest files or application data were inspected. This pass does not prove
storage redundancy, available backup bandwidth, router policy, ownership of a
free private IP, certificate rights, or production reachability.

## Selected conditional topology

This is one preferred design, subject to the unresolved prerequisites below.

| Decision | Selection and reason |
| --- | --- |
| Node / VM | Dedicated Ubuntu Server VM on `pve`, proposed VMID **115** if still free, name `brickvault-appraisal`. It isolates the app from live legacy VM 107. |
| Compute | 1 socket, 4 vCPU, 8 GiB fixed RAM, no ballooning; retain the Phase 11 estimate given current headroom and recheck before reservation. |
| Disks | 32 GiB OS `scsi0` and 128 GiB PostgreSQL/data `scsi1`, both `local-zfs`; separate ext4 filesystems in the guest. The data disk is exclusively owned by this VM. No existing guest disk is adopted. |
| Network | One VirtIO NIC, untagged `vmbr1`; no bridge or VLAN mutation. Use an approved DHCP reservation for a stable private address, with exact lease and source ranges verified before exposure. No public A/AAAA record or WAN forwarding. |
| Name | **`appraisal.abrianbaker.com`**, approved by Brian for planning on 2026-09-29. Browser/PWA use this exact HTTPS origin. Packaged production Android derives `https://android.appraisal.abrianbaker.com` as its WebView Origin and calls the same HTTPS API host. DNS/certificate mutation remains unapproved. |
| Proxy/API | Caddy on the VM terminates private-client HTTPS `:443`, preserves the exact original `Host`, overwrites `X-BrickVault-Proxy` with its protected shared secret, and proxies only to FastAPI `127.0.0.1:18080`. Uvicorn uses `proxy_headers=False`; no client-supplied proxy identity or forwarded header is authoritative. |
| Database | One new empty `brickvault_appraisal_prod` database in a dedicated PostgreSQL **18** cluster on the data disk, matching the accepted local PostgreSQL 18.6 major. PostgreSQL listens only on guest `127.0.0.1:5432`; local postgres administration may use its Unix socket. Dedicated `brickvault_appraisal_prod_owner` and `brickvault_appraisal_prod_runtime` roles have separate 64-lowercase-hex passwords. PostgreSQL is never public. The exact package source/version pin must be reviewed. |
| Accounts/layout | Unprivileged no-login `brickvault` service account. Root:`brickvault` `0750` release directories under `/opt/brickvault/releases/<reviewed-commit>/` with `api/` wheel/venv and `web/` verified readable, regular static files; atomic `/opt/brickvault/current` symlink. Persistent data only in PostgreSQL and protected `/var/lib/brickvault`; retain the previous release for rollback. |
| Units/config | `brickvault-api.service` runs installed `python -m brickvault_api.main` as `brickvault` with a protected `EnvironmentFile`. `/etc/brickvault/api.env` is root:`brickvault` `0640`; `/etc/brickvault/caddy.env` is root:`caddy` `0640`; directories are `0750`. A separate protected provider-credential root is absent until later approval. |
| Backups/monitoring | Brian selected encrypted PostgreSQL logical copies on both the existing Proxmox server and a new Google Drive folder named `Brickvault_Apprisal_App_Backup`. Create two independent encrypted repositories from one protected daily `pg_dump -Fc` plus role/config recovery bundle; propose 30 daily, 8 weekly and 12 monthly recovery points per destination, subject to capacity. Google Drive is the off-host recovery copy; Proxmox is same-host supplemental recovery. A separate VM backup is deferred. Systemd/journald plus private health, authenticated readiness, capacity and backup-failure alerts are proposed. **Both destinations' access, encryption keys, quota/capacity, restores and alert delivery are unverified.** |

The repository requires Python `>=3.13,<3.14`, uv `==0.12.10`, no uv Python
downloads and a system Python interpreter. Ubuntu Server 24.04 defaults to
Python 3.12. The OS image therefore cannot run the accepted API without a
reviewed, supportable Python 3.13 package/build and patching path. The local
PostgreSQL proof is pinned to 18.6; using the Ubuntu default PostgreSQL major
would silently change that baseline. Choose a verified PostgreSQL 18 package
source/version before installation. These are package-source blockers, not
permission to change application version constraints.

Package/challenge references: [Ubuntu 24.04 release notes](https://documentation.ubuntu.com/release-notes/24.04/),
[PostgreSQL's Ubuntu package instructions](https://www.postgresql.org/download/linux/ubuntu/),
and [Caddy's DNS challenge behavior](https://caddyserver.com/docs/automatic-https).

The application already validates its production Host/Origin, Secure cookies,
CSRF, proxy identity, loopback database target and ownership marker under the
accepted P12-01 source contract. The above topology has no real TLS, DNS,
PostgreSQL, browser, Android or restore acceptance yet. The certificate must be
ordinary platform-trusted TLS, never the Phase 9 TEST CA/localhost/ADB path.

## First production data and bootstrap policy

Start with a **new empty** database. Do not query, copy or migrate the legacy
BrickVault PostgreSQL instance; no repository requirement establishes a legacy
data dependency. Create the two restricted login roles, create the database
owned by the owner role from `template0`, set its random ownership comment in
the required `brickvault-appraisal:<32hex>:<32hex>` format, revoke PUBLIC
database/schema privileges, and grant only runtime CONNECT/schema USAGE. Apply
the packaged Alembic graph through current head `0016_hunt_cached_runs` as the
owner, then the repository's enumerated runtime grants. The app connects as
runtime and verifies owner, marker and migration head before serving.

Passwords, the ownership marker and proxy secret are generated on the new VM
with protected hidden input/files, never placed in command arguments, Git,
logs or review artifacts. The API environment holds the runtime URL, marker,
approved origin, loopback bind/port and static path; Caddy receives the same
proxy secret from its own protected file. Brian's first principal is created
with a local TTY and hidden password/confirmation prompt as the owner role
after migration/grants. No password is requested in chat. Provider credentials
are introduced only after the base app, authentication, backup and private TLS
path are proven. Before any provider credential use, resolve the absolute
directory canonically, verify it is outside Git and writable only by the
approved administrator, and verify each file's restrictive mode/ownership.

**Required source/tooling gate:** current `pnpm db:migrate` and
`scripts/auth_admin.py` target development or disposable TEST only. Bare
Alembic is deliberately blocked. Before P12-04, implement and review a
guarded production admin command that validates the exact target/owner/marker,
creates only the approved roles/database from protected local input, runs
packaged Alembic with an injected owner connection, applies the enumerated
grants, and bootstraps via `AuthService.provision` with a hidden TTY prompt.
The proposed interface is `brickvault-production-admin preflight|provision-db|migrate|grant-runtime|bootstrap-owner|verify` with protected local config paths.
**This command does not exist at P12-02 and must not be invoked as if it did.**

## DNS, HTTPS and private access

The proposed flow is private client → private DNS resolution for
`appraisal.abrianbaker.com` → Caddy `:443` on the new VM → FastAPI
`127.0.0.1:18080` → PostgreSQL `127.0.0.1:5432`. Caddy's future site must use
an explicit `header_up Host {host}` and overwrite
`header_up X-BrickVault-Proxy {$BVA_PROXY_SHARED_SECRET}` for the single
loopback `reverse_proxy` upstream. Browser/PWA and Android must receive a
normal platform-trusted certificate for the approved application hostname.
No public DNS address or inbound WAN route is proposed.

P11-01 found Cloudflare authoritative nameservers, so DNS-01 may be suitable
for a private hostname. No Cloudflare account rights, scoped credential path,
DNS-01 client/renewal method or local private DNS override was verified.
**Certificate and private DNS commands are therefore intentionally not chosen
or executable.** Neither a self-signed/user-installed Android CA nor temporary
public exposure is an acceptable substitute. Stock Caddy does not include a
Cloudflare DNS provider module; a reviewed, pinned plugin build or a separate
reviewed DNS-01 issuer would be required. Caddy's automatic HTTPS can also
create an HTTP `:80` redirect listener, so the final configuration and private
firewall check must explicitly account for that port. See the official
[Caddy global options](https://caddyserver.com/docs/caddyfile/options) for
DNS modules and the automatic HTTP listener.

## Backup, restore and rollback design

The authoritative recovery layer is a daily `pg_dump -Fc` of the dedicated
database plus `pg_dumpall --globals-only` role material, protected service
configuration and the deployment manifest.

Brian selected **encrypted database copies on both** the existing Proxmox
server and Google Drive folder `Brickvault_Apprisal_App_Backup`. A root-only
backup runner captures `pg_dump -Fc` and `pg_dumpall --globals-only` into the
Proxmox repository using restic `backup --stdin-from-command`, which fails the
snapshot if the dump command fails. A root-only manifest/config snapshot must
include the database ownership marker, role names, migration/release version
and protected settings. Tag and record all required snapshot IDs under one
backup-run ID; an unpaired or failed snapshot is not a valid recovery point.
Do not use a plain `pg_dump | restic backup --stdin` pipe, which can hide dump
failure. This avoids a persistent plaintext database dump on guest storage.
Use two independent restic repositories and distinct repository keys: one
through a dedicated, no-sudo, SFTP-only Proxmox backup account confined to a
reviewed directory on host storage, and one through a dedicated reviewed
rclone Google Drive OAuth client. The guest's root-only backup runner holds
the restricted SFTP identity, OAuth token and repository keys outside Git;
the application service account cannot read them. The runner uses restic
`copy --from-repo` to transfer only the complete run's snapshots to Google
Drive, re-encrypting them under the second repository key. Verify host
identity, destination capacity/quota and ownership before any connection or
repository creation. Keep both repository key recovery materials and Google
Drive recovery access separately in an approved offline location. Neither
account, directory, folder, key or repo exists yet.

Propose 02:15 local time, 30 daily/8 weekly/12 monthly recovery points on each
destination subject to measured capacity. Each scheduled run must verify the
complete run's encrypted snapshots/readback at both destinations, record
separate freshness and alert on either failure. A failed Drive copy leaves the
Proxmox snapshots intact for a bounded retry and marks off-host recovery
stale; it never counts as a complete dual-destination run. Before every later
migration, capture and verify both copies, including the Google Drive off-host
copy, and record schema compatibility/rollback. Use a protected unattended
token; do not rely on rclone's retiring shared client ID. The official [restic
SFTP and rclone
backends](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html),
[restic command-backed backup](https://restic.readthedocs.io/en/stable/040_backup.html),
[restic repository copy](https://restic.readthedocs.io/en/stable/045_working_with_repos.html),
and [rclone Google Drive setup](https://rclone.org/drive/) establish tool
interfaces, not account rights or unattended operation on this VM.

A restore rehearsal independently recovers from each repository to a separate
disposable database/VM, reapplies roles and database comment, restores with
`pg_restore`, verifies ownership marker/Alembic head, runtime grants, auth and
representative saved-work readback, then removes only the owned disposable
resources after review. The Google Drive rehearsal must succeed with the
Proxmox repository unavailable, proving recovery after total host loss.
Never test restore over production.

The observed `local` store can hold Proxmox VM archives, but it shares host
storage and no job, encryption, access or retention policy exists. A VM
snapshot or local-only `vzdump` cannot replace logical off-host recovery.
The Proxmox logical repository would remain on the same physical server as
the VM, so it does not protect against node/storage loss. The observed `local`
file store shares `rpool` with the selected VM disks; backup growth could
impair both. Do not choose its repository path until a dedicated dataset/path,
quota, minimum free-space floor and alerts are reviewed. The large
`sas_raid0_lvmthin` VM-disk pool is not automatically a file repository. The
Google Drive repository is the off-host recovery copy. A VM-level backup is a separate,
deferred layer until a production-safe encrypted target and restore path are
reviewed. The new Google Drive folder and Proxmox logical repository are
future mutations, not actions performed in P12-02.

Before cutover preserve the previous application release, database backup,
configuration and DNS value. On failed validation, disable the Caddy route,
stop the app and leave the new VM/data intact for diagnosis. Repoint the
`current` symlink only when the previous schema is compatible. For an
incompatible migration, restore the verified off-host logical backup and
role/config material to an owned recovery database before rolling the app
back. Revert only the exact DNS/firewall entries created by the approved
mutation, after recording their previous state. Do not automatically destroy
the VM, disks or database.

## Ordered future mutation runbook — **not executed**

Every row is a future mutation requiring its own approved gate. Values in
angle brackets are prerequisites to resolve and review, not shell arguments
to run literally. P12-03 currently covers base VM/OS provisioning only;
P12-04 covers database, app, DNS/TLS, backups and monitoring; P12-05 covers
real-client/restore acceptance. Approval of this document alone authorizes
none of them.

| # / gate | Target and command/tool | Expected state and intended change | Immediate verification | Failure rollback/stop |
| --- | --- | --- | --- | --- |
| 1 / P12-03 | `pve`: `pvesh get /cluster/nextid`, `qm config 115`, `pvesm status` before `qm create 115 --name brickvault-appraisal --memory 8192 --balloon 0 --cores 4 --sockets 1 --cpu host --machine q35 --bios ovmf --scsihw virtio-scsi-single --ostype l26 --onboot 0` | 115 must still be free and both node/pool headroom checks pass; create only this stopped VM definition. | `qm config 115`, inventory and host capacity show exact allocation. | If mismatched, keep it stopped and disable onboot; no broad VM cleanup. Replan any ID conflict. |
| 2 / P12-03 | `pve`: `qm set 115 --efidisk0 local-zfs:1,efitype=4m,pre-enrolled-keys=1`; `qm set 115 --scsi0 local-zfs:32,discard=on,iothread=1,ssd=1`; `qm set 115 --scsi1 local-zfs:128,discard=on,iothread=1,ssd=1` | VM stopped, selected pool has verified free capacity; allocate one EFI, one OS and one exclusively new data disk. | `qm config 115`, `pvesm status`; no existing volume was attached. | Leave VM stopped; delete only explicitly created volumes after separate destructive approval. |
| 3 / P12-03 | `pve`: `qm set 115 --net0 virtio,bridge=vmbr1,firewall=1`; no VLAN tag. | `vmbr1` and approved private DHCP reservation/routing exist; attach one NIC, no bridge/firewall mutation. | `qm config 115` shows one untagged `vmbr1` NIC; later guest gets only its reserved private lease. | Stop VM and detach only the new NIC after preserving config if wrong. |
| 4 / P12-03 | `pve`: verify installed ISO hash/provenance; `qm set 115 --ide2 local:iso/ubuntu-24.04.2-live-server-amd64.iso,media=cdrom`; `qm set 115 --boot 'order=ide2;scsi0'`; `qm start 115`; Ubuntu Server installer via approved console; after installation set boot to `scsi0`. | VM is new/stopped; install Ubuntu 24.04.2 to `scsi0` only, hostname `brickvault-appraisal`, approved admin key and reserved DHCP; do not format `scsi1` in installer. | Guest reports expected release, private lease, OS filesystem and untouched data disk; `qm config 115` shows correct boot disk. | Stop VM/onboot; retain disks for diagnosis, no legacy change. |
| 5 / P12-03 | Guest: approved `apt-get update` and exact reviewed package manifest; install a supportable system Python 3.13 and pinned uv 0.12.10 from reviewed sources; create no-login `brickvault` via `useradd --system`; `install -d` release/config/state directories with reviewed ownership/modes. | Fresh guest, Python source/version/hash and patch path, admin path and package manifest reviewed. Ubuntu 24.04's default Python 3.12 is insufficient. | `python3.13 --version`, `uv --version`, `dpkg-query`, `id brickvault`, `stat` and `systemctl` show versions/permissions; only SSH from approved admin range is reachable. | Stop before app exposure; revert only the new account/directories/packages after dependency review. |
| 6 / P12-04 | Guest: partition/format only verified `scsi1`, mount by verified filesystem UUID at `/var/lib/postgresql`; install reviewed PostgreSQL 18 from a verified/pinned package source; set `listen_addresses='127.0.0.1'`, `port=5432`, restricted `pg_hba.conf`, then start local cluster. | Disk identity/ownership confirmed and no data exists; configure one isolated PostgreSQL 18 cluster and no public listener. | `lsblk`, `findmnt`, `postgres --version`, `pg_isready -h 127.0.0.1`, `ss -ltn` and external deny check prove data mount, version and loopback-only listener. | Stop PostgreSQL, close guest firewall path, preserve data disk; do not touch VM 107. |
| 7 / P12-04 | Guarded future `brickvault-production-admin preflight` and `provision-db` with protected input: create `brickvault_appraisal_prod_owner` and `_runtime` LOGIN roles without SUPERUSER/CREATEDB/CREATEROLE/REPLICATION/BYPASSRLS; outside the roles transaction create `brickvault_appraisal_prod` owned by owner from `template0`; set ownership marker; revoke PUBLIC DB/schema, grant runtime CONNECT/schema USAGE. | Fresh dedicated cluster; exact names unused; reviewed admin tool available; secrets generated on host with hidden input and restricted files. | Query only role attributes, database owner/comment and grants; verify no public grants and no secret output. | Revoke new access and stop; retain dedicated DB for reviewed cleanup instead of automated drop. |
| 8a / P12-04 | `pve`: after verified storage-path/capacity review, create a dedicated no-sudo SFTP-only `bva-backup` account and owned, confined repository directory on host storage using reviewed `useradd`/`install -d`/SSH restriction configuration. Do not grant guest root or Proxmox management access. | Exact filesystem path, quota, free-space floor, retention isolation, account restrictions, SSH host identity and authorized key are reviewed; no target/account currently exists. **Exact path and SSH restriction commands remain blocked.** | Guest backup identity can access only its repository and cannot obtain shell, sudo or Proxmox API access; host free-space floor is enforced/alerted. | Disable only the new key/account access; preserve repository data for diagnosis and reviewed cleanup. |
| 8b / P12-04 | Approved Google Drive account and guest: create only `Brickvault_Apprisal_App_Backup` after review; install pinned restic/rclone and protected OAuth/SFTP/repository-key files; initialize Proxmox restic at `sftp:bva-backup@<verified-host>:/<reviewed-backup-path>/repository` and separate Drive restic at `rclone:bva-drive:Brickvault_Apprisal_App_Backup/repository` with `--from-repo`/`--copy-chunker-params` for later `restic copy`. | Both account scopes, unattended credentials, host identity, path/quota/capacity, separate key recovery and alert route are verified. **None was proven or created in P12-02.** | Open both repositories with their own keys from guest and independently from recovery context; no secret appears in command arguments/logs. | Disable credentials, preserve initialized repositories for reviewed cleanup. |
| 8c / P12-04 | Guest root-only runner: `restic -r <Proxmox-repo> backup --stdin-from-command -- pg_dump -Fc ...` and a separate guarded `pg_dumpall --globals-only` capture; add root-only owner-marker/config/manifest snapshot with the same run ID; `restic -r <Drive-repo> copy --from-repo <Proxmox-repo> <run-snapshot-IDs>`; configure daily systemd timer, retention and per-destination alerts. | Empty dedicated DB, verified role access, both encrypted repos and keys, capacity and a reviewed backup-run script exist. Run before first migration and again before each later migration; no plaintext dump pipe/file. | Dump exit codes, complete snapshot set, independent restic checks/readback, age/alert delivery and disposable restore from each repo pass. | Disable timer, retain valid Proxmox snapshots if Drive copy fails, mark off-host backup stale and stop migration; never prune without readback. |
| 9 / P12-04 | Release builder and guest: verify source commit, wheel and web build hashes; copy only reviewed artifacts to `/opt/brickvault/releases/<reviewed-commit>/api` and `/web`; create pinned virtualenv and install wheel with locked dependencies. | Clean reviewed build and protected release directory exist; no mutable checkout is served. | `stat`, package metadata, frontend byte verifier and artifact hashes match approved manifest; static assets are regular files. | Keep prior `current`; quarantine failed release, no cutover. |
| 10 / P12-04 | Guarded future `brickvault-production-admin preflight`, `migrate`, `grant-runtime`, `verify` as owner, after the verified dual-destination pre-migration backup from step 8c. | New DB and approved packaged migration graph exist; tool is implemented/reviewed; apply through `0016_hunt_cached_runs` and enumerated runtime grants only. | Owner/marker/head/runtime least-privilege checks pass; runtime cannot perform DDL. | Do not serve; for incompatible failure restore verified logical backup into owned recovery target before app rollback. |
| 11 / P12-04 | Guest: create `/etc/brickvault/api.env` and `/etc/brickvault/caddy.env` through protected hidden input, root-owned `0640` and separate service groups; set Caddy/API secret equality without printing values. | Approved hostname and secret custody; configure production DB URL, marker, origin, loopback `18080`, static directory and shared proxy identity. | `stat`, canonical paths and redacted config preflight pass; no secret in process args, web files or logs. | Stop services, revoke/reissue compromised secrets; preserve protected prior config. |
| 12 / P12-04 | Approved guest/upstream firewall tools: allow `:443` from approved private-client range and SSH from admin range; deny other inbound ports, especially `5432` and `18080`. | Exact source ranges/rule ownership known; no Proxmox firewall protection assumed. **Exact upstream command remains blocked.** | Independent client reachability and deny checks show only private HTTPS; PostgreSQL/API remain loopback. | Restore saved exact rules, stop new services and do not expose the host. |
| 13 / P12-04 | Guest: install reviewed `brickvault-api.service` with `User=brickvault`, protected `EnvironmentFile`, `ExecStart=<release-venv>/bin/python -m brickvault_api.main`; `systemctl daemon-reload`, start on loopback only. | DB/grants/release/config verified; service starts without provider credentials. | `systemctl status`, `ss -ltn`, loopback health/readiness and safe logs; no non-loopback API port. | Stop/disable new unit; retain prior release and database. |
| 14 / P12-04 | Approved private-DNS authority: create only `appraisal.abrianbaker.com` private override to reserved VM address; approved DNS-01 authority: issue/renew ordinary platform-trusted certificate with narrowly scoped rights. | Prior DNS state captured; authority, tool, credential path and client resolution confirmed. **Exact tools/commands remain blocked.** | Private clients resolve only the approved VM; external DNS has no public app address; certificate chain/renewal test passes with normal client trust. | Restore exact prior DNS entry and revoke only newly issued credential/certificate if required; do not start Caddy. |
| 15 / P12-04 | Guest: install a reviewed/pinned Caddy artifact and protected Caddy environment; site `appraisal.abrianbaker.com` with exact Host, overwritten proxy header, `reverse_proxy 127.0.0.1:18080`; `caddy validate`, then start only after step 14 and firewall verification. | Exact approved host, DNS-01 module or external issuer, certificate files/renewal and firewall sources resolved; no inherited client proxy identity. | Config validation, expected `:443` listener, explicit `:80` decision, negative direct-header/Host/Origin checks and no sensitive access logging. | Stop Caddy site, keep API loopback; restore prior Caddy config if any. |
| 16 / P12-04 | Guarded future `brickvault-production-admin bootstrap-owner` at a local TTY with hidden password/confirmation. | Migration, backup and private TLS/app path pass; no principal exists; create Brian's one principal via `AuthService.provision`. | Authenticated login/CSRF/logout through HTTPS, no password or verifier in logs/artifacts. | Disable access and use reviewed hidden-input reset/revocation path; no silent credential reuse. |
| 17 / P12-04/05 | Guest/monitor: journald retention, systemd restart policy, private health and authenticated readiness checks, disk/backup alerts; perform private browser/PWA/Android checks and a disposable off-host restore rehearsal. | DNS/TLS, backups and application service verified, with approved client/device scope. | Normal certificate trust, Host/Origin/proxy/CSRF/cookies, no public DB/API, restore and rollback checks pass; record exact evidence. | Stop cutover and new services, revert only owned DNS/firewall changes, preserve data and prior release. |

The displayed `qm`, package and systemd commands are review proposals. The
operator must re-read and diff exact existing state immediately before each
future mutation; no placeholder value or guessed source range can be executed.
P12-03 can only be authorized for its actual base-provisioning subset once its
own prerequisites are resolved. The remaining rows retain separate P12-04/05
approval and acceptance gates.

## Blockers and review verdict

1. **Dual encrypted backup access:** Brian selected encrypted PostgreSQL
   copies on both existing Proxmox and new Google Drive folder
   `Brickvault_Apprisal_App_Backup`. No SFTP-only Proxmox account/directory,
   Google Drive folder/remote, repository, job or independent recovery path was
   observed or created. Verify host filesystem path, quota and free-space
   floor; restricted account, SSH identity and deletion/retention isolation;
   unattended OAuth rights, Drive ownership/quota, two distinct encryption
   keys with offline recovery, alerts and separate restores. Proxmox remains
   same-host; Google Drive is required for off-host recovery.
2. **Private DNS and ordinary certificate:** Brian approved
   `appraisal.abrianbaker.com` for planning only. The private DNS authority/override, DNS-01 account rights,
   credential path, exact issuance/renewal tool and normal client reachability
   are unknown. Do not invent Cloudflare credentials or expose a public port.
3. **Private address/firewall sources:** confirm an owned DHCP reservation and
   exact client/admin source ranges and upstream rule owner before network or
   firewall mutation. Proxmox firewall is not enabled.
4. **Production administration:** implement/review the guarded owner migration,
   grants and hidden-input bootstrap tool before P12-04. Existing development
   and disposable TEST helpers are not production provisioners.
5. **Pinned runtime sources:** select and verify a supportable system Python
   3.13 source for Ubuntu 24.04, uv 0.12.10 artifact, PostgreSQL 18 package
   source/version, and the Caddy DNS-01 issuer/plugin and renewal strategy.
   Neither Ubuntu's default Python 3.12 nor an unreviewed PostgreSQL major is
   compatible with the accepted local stack.
6. **Operational acceptance:** select alert delivery and complete a real off-host
   restore, private browser/PWA/Android normal-TLS acceptance, and rollback
   rehearsal before Phase 12 closure.

**P12-02 review package verdict: BLOCKED — dual-backup access/restore and
private DNS/certificate/access facts are missing.** The selected VM shape and ordered
runbook are reviewable, but the full deployment plan is not mutation-ready.
ChatGPT review has not closed P12-02; P12-03 has not begun.

## Progress log and outcome

- [x] 2026-09-29: Verified expected main HEAD, empty index and the three
  protected pre-existing file hashes against the prior record.
- [x] 2026-09-29: Ran `ssh -G proxmox`, one noninteractive configured-key
  authentication check, then bounded direct read-only Proxmox/Linux inventory.
- [x] 2026-09-29: Chose one conditional VM topology, new-empty-data policy,
  source-aligned proxy/database model and future mutation/rollback order.
- [x] 2026-09-29: Brian approved `appraisal.abrianbaker.com` for planning and
  selected encrypted database copies on existing Proxmox and Google Drive
  folder `Brickvault_Apprisal_App_Backup`; no destination was configured.
- [ ] ChatGPT review of the sanitized P12-02 package and resolution of the
  listed infrastructure and account-rights facts.
- [ ] Any P12-03/04/05 mutation or live acceptance; separately authorized.

No VM, disk, bridge, VLAN, firewall, DNS, certificate, backup job, PostgreSQL
instance, service, package, secret or application deployment was created or
changed in P12-02.
