# ExecPlan 094 — P12-04A production foundation

## Goal and user-visible outcome

VM 115 now has a private production foundation for BrickVault: dedicated PostgreSQL storage, Python 3.13, pinned uv, PostgreSQL 18, a guarded production administration CLI, a hash-verified packaged release and an inactive API unit. Production data, secrets, backup, DNS and TLS remain for later P12-04 checkpoints. P12-04A is IMPLEMENTED / READY FOR REVIEW; review publication and independent acceptance remain pending. P12-04 remains IN PROGRESS.

## Why this work is being done now

Brian explicitly authorized P12-04A after accepting P12-03. The accepted Ubuntu base VM is ready for foundation work, while first production migration/bootstrap still requires reviewed encrypted recovery paths. [Plan 091](091-production-runtime-and-deployment.md), [Plan 092](092-exact-infrastructure-pre-mutation-review.md) and [Plan 093](093-base-vm-provisioning.md) retain the earlier decisions and evidence.

## In scope

- Reverify VM and blank `scsi1`, format only that disk as GPT/ext4 and mount by UUID at `/var/lib/postgresql` without `nofail`.
- Install official, integrity-verified CPython 3.13 in a versioned system path, official uv 0.12.10 and signed PGDG PostgreSQL 18.
- Keep PostgreSQL local to `127.0.0.1:5432` with cluster data on the mounted disk and restrictive local authentication.
- Implement and test the packaged production administration CLI with exact production-target and ownership guards.
- Build a locked API/web release with hashes, stage only reviewed artifacts, create the no-login service account, release layout and inactive systemd unit.
- Recheck storage persistence, SSH, guest agent, listeners, account permissions and absence of production secrets and database.

## Explicit non-goals

No production BrickVault database, roles, migration, owner bootstrap, password, ownership marker or proxy secret. No Caddy, private DNS, certificate, backup repository/job, Google Drive, Cloudflare, firewall/router change, provider call or legacy VM 107 access. No main commit/push or P12-05 work.

## Current repository state

Main is `96b84359078632fef7a7193add663734cec8ba2c` with an empty index at entry. `AGENTS.md` and the catalog search/parser test files are the only starting worktree changes; their accepted SHA-256 values were confirmed and will remain byte-for-byte unchanged and unstaged.

## Decisions and assumptions

The trusted Proxmox readback found VM 115 stopped, `onboot=0`, q35/OVMF, four host vCPUs, 8192 MiB RAM, `scsi0` 32 GiB, `scsi1` 128 GiB, one `vmbr1` NIC and guest agent enabled. Only VM 115 was started. Its changed DHCP address was obtained from the agent. Laptop SSH was allowed only after the ED25519 network key matched the guest-agent-proven fingerprint. The guest reports Ubuntu 24.04.5 LTS, hostname `brickvault-appraisal`, root on `scsi0` `/dev/sda2`, and the originally unpartitioned 137,438,953,472-byte `scsi1` disk with the expected stable SCSI serial. Read-only `lsblk`, `wipefs`, `blkid`, mount and fstab checks found no prior data-disk use. No BrickVault, PostgreSQL or Caddy installation was present before foundation changes.

The reviewed `scsi1` is now GPT with one ext4 partition, `/dev/sdb1`. An initial filesystem label request exceeded ext4's 16-byte limit and was truncated; after inspecting the partial state, the label was explicitly corrected to `brickvault-db`. The filesystem is mounted at `/var/lib/postgresql` through a UUID `fstab` entry with required-mount behavior (no `nofail`). The actual UUID and raw host evidence stay in ignored local records. Remount and boot-ID-proven reboot checks confirmed that the root and data filesystems return on their intended disks.

The [official CPython 3.13.15 xz source](https://www.python.org/ftp/python/3.13.15/Python-3.13.15.tar.xz) matched SHA-256 `1e66a7945a48390ee4c2a4268a0e4185884059a13c4aab6d148aa208deea4a76`, and its detached signature verified against Thomas Wouters's release key fingerprint `7169605F62C751356D054A26A821E680E5FA6305`. Its build and installation into `/opt/python/3.13.15` completed; the installed interpreter reports Python 3.13.15 with OpenSSL 3.0.13 and passed the required runtime checks. Ubuntu's system `/usr/bin/python3` remained unchanged. This source-built interpreter requires explicit monitoring of 3.13 security releases and a verified signed-source rebuild into a new versioned prefix; unattended apt alone cannot patch it.

The official Astral uv 0.12.10 Linux GNU archive matched its published SHA-256 `173d95a0c32d18c896c46ba6fafbf3cf9c14ab74b033f81b76c883ef492a976b`; uv is installed at `/usr/local/bin/uv`. No uv-managed Python is permitted. The PGDG Noble signing key fingerprint was verified as `B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8`; the signed installed PostgreSQL package is `postgresql-18=18.6-1.pgdg24.04+2`.

The `18/main` cluster is active and enabled with data at `/var/lib/postgresql/18/main` on `/dev/sdb1`. A systemd mount dependency requires `/var/lib/postgresql` before cluster startup. TCP binds only `127.0.0.1:5432`, with SCRAM authentication on loopback; IPv6 loopback is rejected. The local socket maps OS `root` and `postgres` to database `postgres` through `brickvault_maintenance`, and ordinary local users retain peer authentication. Cluster-wide credential logging controls are `log_statement=none`, `log_min_error_statement=panic`, `log_parameter_max_length=0` and `log_parameter_max_length_on_error=0`. Post-reboot checks confirmed cluster location, readiness and loopback-only listener. A laptop-origin PostgreSQL TCP check found no reachable external endpoint. Checks found no production BrickVault database or production roles.

The locked, no-login `brickvault` system account has only its own group and no sudo rights. `/opt/brickvault`, `/opt/brickvault/releases` and `/etc/brickvault` are `root:brickvault` mode `0750`; `/var/lib/brickvault` is `brickvault:brickvault` mode `0700`. Release `p12-04a-r1` and its virtualenv were installed under the protected release layout. The API unit is installed but disabled and inactive; its mandatory production environment file is absent, and no API listener exists. VM 115 remains running with Proxmox `onboot=0`.

The reviewed release source ID is `c65188e2f3bfeecc140175e52f5ecab9a64c850710513c7a2c5aaf3ce9c7bc4c`. Release `p12-04a-r1` has manifest SHA-256 `bfc6608efa56d1625f4493fe5e491b587ef95accacacf399fd44de38c6998ce9` and API wheel SHA-256 `ec3e2ec4716046fae481aa85c76bc0eda1b6d81033c45c1c7548f7c7b16a9cf8`. The pnpm release build, independent installed-wheel import and frontend verification passed locally; the transferred manifest hashes verified on VM 115. The VM virtualenv installed 26 hash-locked dependencies plus that wheel. Installed-wheel import and `brickvault-production-admin` entrypoint checks passed as the `brickvault` user.

## Data model and API/interface changes

No schema or API route changes. The new packaged `brickvault-production-admin` interface has `preflight`, `provision-db`, `migrate`, `grant-runtime`, `bootstrap-owner` and `verify` commands. Its source accepts only the exact production database/owner/runtime names and loopback target from a protected, root-owned local descriptor; the descriptor and recovery receipt do not exist on VM 115 in P12-04A. Maintenance requires OS root, the local PostgreSQL socket and a verified `postgres` session through the narrow peer map; it rejects PostgreSQL and application environment overrides. Provisioning refuses existing or partial target state. Migration, runtime grants and bootstrap require an operator-verified, recent two-copy recovery receipt bound to the database marker and revision state. Bootstrap also requires a local TTY with hidden password input and an empty principal table.

Credential-bearing SQL uses a guarded maintenance session that sets and reads back effective PostgreSQL logging and activity settings and refuses unreviewed preload libraries. Role provisioning computes distinct SCRAM-SHA-256 verifiers client-side, so plaintext role passwords never enter the SQL statement. The owner bootstrap writes its Argon2 hash through a guarded peer session switched to the owner role. The CLI prints generic errors rather than driver, path or credential details. Thirty focused, synthetic unit tests passed for target and ownership guards, recovery receipt, credential sentinel handling, logging refusal and CLI redaction. A separate disposable PostgreSQL 18 logging proof and three focused local PostgreSQL runtime-grant tests passed; their disposable database was removed and runner stopped. The installed-wheel import and admin entrypoint passed as the `brickvault` user on VM 115. VM 115 has not executed any CLI production mutation.

## Implementation sequence

1. Complete: verify package sources and blank-disk target, then create GPT/ext4 on the reviewed `scsi1`; correct the ext4 label to `brickvault-db`, mount by UUID and verify remount from `fstab`.
2. Complete: install signed PGDG PostgreSQL 18.6 only after the data mount; create the 18/main cluster on that filesystem; constrain its listener and local authentication; verify active service, data location, socket and absence of BrickVault database/roles.
3. Complete: verify signed CPython 3.13.15 source and official uv 0.12.10 archive; install both without replacing the Ubuntu system Python or downloading an uv-managed Python.
4. Complete: implement and test the admin CLI; build the installed-wheel/web release from locked inputs, independently verify its frontend and wheel, and produce the content-hash manifest.
5. Complete: create the restricted `brickvault` account and directories; transfer verified release artifacts, install 26 hash-locked dependencies and the wheel, and install a disabled/inactive API unit without its mandatory environment file.
6. Complete: perform targeted repository and server validation. One boot-ID-proven reboot checked root/data mounts, PostgreSQL, SSH, guest agent, time, account, listener and absence of production secrets/database/roles. Leave VM 115 running with `onboot=0`.
7. Pending: prepare a sanitized `astra-response` r1 package for independent review; leave main uncommitted and its index empty.

## Validation and acceptance criteria

The boot-ID-proven reboot confirmed that the data mount persists and PostgreSQL's data directory resolves onto `scsi1`. PostgreSQL binds only 127.0.0.1, and laptop-origin TCP access to its port was refused or unreachable. Exact CPython/uv/PGDG provenance and versions are recorded above. The pnpm build, frontend verifier, manifest hashes, independent installed-wheel import, VM wheel import and admin entrypoint passed. Thirty admin CLI synthetic unit tests, a separate disposable credential-logging proof and three local PostgreSQL grant tests passed. The API unit remains disabled and inactive, with no listener or populated production environment file. Post-reboot checks also covered SSH, guest agent, time, account permissions and absence of production database, roles and secrets. The three protected file hashes still match the accepted values and the main Git index is empty.

## Security, privacy and data integrity

All raw VM addresses, host keys, filesystem UUIDs and operational outputs remain in ignored local evidence; the public review package contains sanitized summaries. No production secret, database, role, marker or account principal has been created. Only the reviewed `scsi1` was partitioned and formatted. The production admin interface rejects ambiguous ownership/target state, protects credential-bearing SQL at the database-session boundary and redacts errors. Foundation and test evidence do not establish that first production mutation or backup recovery is ready.

## Failure modes, rollback and recovery

The disk write was gated on matching serial, size, partition/signature/mount state and root-disk identity. The overlong ext4 label caused a stopped partial disk step; the next step inspected its GPT/ext4 state and corrected only the label before mounting. Stop future installation if source integrity or repository signature fails. Keep any partially prepared VM private; do not fabricate acceptance or move PostgreSQL from an accidental OS-disk cluster. No destructive rollback, VM deletion or legacy guest operation is in scope. A source-build maintenance owner must be explicit because apt does not patch it.

## Progress log

- [x] 2026-09-29: Main HEAD/index and three protected hashes matched the accepted checkpoint.
- [x] 2026-09-29: Trusted host readback matched VM 115's accepted stopped configuration; started only VM 115.
- [x] 2026-09-29: Guest host key was verified through Proxmox agent before approved-key SSH.
- [x] 2026-09-29: Guest read-only OS/root/data disk and absence checks passed.
- [x] 2026-09-29: Reviewed `scsi1` was partitioned and formatted; the ext4 label was corrected to `brickvault-db` after a safe stop, then the UUID mount and remount passed.
- [x] 2026-09-29: Python.org CPython 3.13.15 source hash/signature and official uv 0.12.10 archive hash passed. The versioned Python build and uv installation passed; Ubuntu system Python remained unchanged.
- [x] 2026-09-29: Signed PGDG `postgresql-18=18.6-1.pgdg24.04+2` and the disk-backed, local-only 18/main cluster passed; production database and roles are absent.
- [x] 2026-09-29: Locked `brickvault` account and protected base directories passed account/permission checks.
- [x] 2026-09-29: Admin CLI source and 30 focused synthetic tests passed, including the credential logging guard; a separate disposable PostgreSQL 18 logging proof passed. No real production CLI mutation was run.
- [x] 2026-09-29: pnpm release build, independent wheel import and frontend verification passed; release `p12-04a-r1` and its manifest hashes verified on VM 115. Twenty-six locked dependencies and the wheel were installed; the `brickvault` user imported the wheel and invoked the admin entrypoint.
- [x] 2026-09-29: Three focused local PostgreSQL grant tests passed; their disposable database was removed and test runner stopped.
- [x] 2026-09-29: The API unit was installed disabled/inactive without its mandatory environment file or any listener.
- [x] 2026-09-29: One boot-ID-proven VM reboot passed root/data mounts, local PostgreSQL, SSH, agent, time, account, listener and no-production-state checks; external PostgreSQL TCP was not reachable from the laptop. VM 115 remains running with `onboot=0`.
- [x] 2026-09-29: The three protected SHA-256 values still match and main's index remains empty; the sanitized r1 review package was assembled from the literal 16-file task inventory.
- [ ] Obtain independent P12-04A review and acceptance.

## Open questions and manual checks

The later backup, DNS/TLS and first production-data gates remain unresolved. The CLI recovery receipt is only a guard for independently verified dual-destination backups; it is not itself backup or restore proof. No browser, PWA, Android or restore acceptance is part of P12-04A.

## Outcome and follow-up

P12-04A is IMPLEMENTED / READY FOR REVIEW. Runtime, release, installation and reboot checks passed; the sanitized r1 review package is prepared and independent acceptance is pending. No production database, roles, migration, owner bootstrap or later backup/DNS/TLS work was performed. P12-04 remains IN PROGRESS; P12-05 is NOT STARTED.
