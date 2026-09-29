# P12-04B: dual encrypted recovery foundation

Status: **P12-04B implemented and ready for review**. P12-04A is accepted. P12-04 remains open. P12-05 has not started.

## Scope and guardrails

This slice prepares independently encrypted Proxmox and Google Drive recovery repositories before a production database exists. It does not create a production database or roles, run migrations, bootstrap an owner, start the API, install Caddy, request TLS, or enable the backup timer. The three protected dirty files remain outside this slice. The repository index and `main` commit remain unchanged.

## Verified tooling

| Tool | Version | Source and verification |
| --- | --- | --- |
| restic | 0.19.1 | [Official GitHub release](https://github.com/restic/restic/releases/tag/v0.19.1). The project's published checksum file had a valid signature from fingerprint `CF8F18F2844575973F79D4E191A6868BD3F7A907`; Linux and Windows archive digests matched. Root owns the VM executable. |
| rclone | 1.75.1 | [Official rclone release](https://rclone.org/downloads/). The published checksum file had a valid signature from fingerprint `FBF737ECE9F8AB18604BD2AC93935E02FF3B54FA`; the Linux archive digest matched. Root owns the VM executable. |

The Windows recovery context uses the verified restic 0.19.1 archive and installed rclone 1.75.1. No installer pipe was used. Proxmox required no package installation.

## Proxmox supplemental repository

The same-host copy is supplemental and does not satisfy off-host disaster recovery. The healthy `rpool` had about 375 GiB available before creation. The dedicated `rpool/brickvault-backup` child mounts at `/var/lib/brickvault-backup` with a 64 GiB quota, compression enabled, and atime disabled. It is not general VM storage. The quota can be changed without relocating the repository.

The `bva-backup` account has a locked password, no sudo or login shell, and an `internal-sftp` chroot. Only `/repository` inside the chroot is writable. A dedicated sshd fragment disables forwarding and TTY use and requires public-key authentication. The exact prior sshd state was saved privately. `sshd -t` passed before reload, and the existing root SSH path was retested afterward. VM and Windows recovery keys are distinct; only their public keys reside on Proxmox. Shell, password authentication, chroot-root writes, and access outside the chroot were denied in focused tests.

The independently encrypted restic repository is `sftp:bva-proxmox-repository:/repository`. Its repository ID begins `db58f878c2`. A restic snapshot listing and repository check passed.

## Google Drive boundary

The off-host target is `Brickvault_Apprisal_App_Backup/restic-production`. Rclone's shared Google client ID is being retired, so Brian authorized a dedicated Google OAuth client. The project already had a separate client and rclone remote with full Drive scope. Those files and the existing remote were preserved. A new Desktop client was created for this slice; its separate rclone remote requests only `drive.file`, which limits access to files the app creates or opens. The project is in production publishing status, and Google Drive API was already enabled. Brian completed the interactive Google authorization. The new encrypted rclone configuration contains the resulting token. No Google credential is in Git or the review package.

The target folder did not exist in a scoped exact-path check before creation. VM 115 created only `Brickvault_Apprisal_App_Backup/restic-production` with the new remote. The separate Drive restic repository ID begins `a82ca12e8252`; initialization, empty snapshot listing, and `restic check` passed.

## Credential custody and recovery qualification

The VM holds two distinct high-entropy restic passfiles, its dedicated Proxmox transport key, an encrypted rclone configuration, a root-only rclone unlock file, and a root-only repository identity record under `/etc/brickvault/backup`. The separate Windows recovery set is under Brian's local profile in `AppData/Local/BrickVault/Recovery`, with ACLs limited to Brian, SYSTEM, and Administrators. It contains the Proxmox recovery key, pinned host identity, both restic passwords, the new OAuth client record, and the separate encrypted `drive.file` rclone configuration. Windows protects its rclone unlock material with the existing user-bound DPAPI mechanism. VM 115 is not the sole holder of either repository's access. Recovery from simultaneous VM and laptop loss still requires an offline custody decision before production migration.

A task-owned synthetic canary with a random run ID, timestamp, manifest, and SHA-256 was backed up separately from VM 115 to both repositories. The Proxmox snapshot begins `51a00359234d`; the Drive snapshot begins `be729419380a`. In two independent Windows-only restic restores, each snapshot was opened with its own recovery credentials, restored into a fresh private temporary directory, and checked against the exact pre-recorded manifest, file bytes, size, and SHA-256. Each task-owned restored tree was removed after success. **Proxmox independent Windows restore: PASS. Google Drive independent Windows restore: PASS.** The Proxmox copy remains same-host supplemental recovery; only the Drive copy is off-host.

## Future production backup runner

`brickvault-production-backup` is source-only in this slice. Its preflight requires root, protected configuration and credential files, the reviewed PostgreSQL cluster/data directory, provisioned production database and role ownership markers, exact repository IDs, and the expected narrow Drive client/scope. It streams one `pg_dump` custom-format output to two restic children with bounded queues, cancellation, exit-code checks, byte count, and SHA-256. PostgreSQL globals and required production configuration are separate encrypted artifacts under the same run ID. Each artifact is read back from both repositories and hashed before a protected receipt is written. No normal-disk plaintext dump is created.

The service and timer definitions are prepared in `deploy/systemd`. They have not been installed, started, or enabled on VM 115. The service runs as root to read protected inputs and uses systemd filesystem and process restrictions; its runner refuses execution before production provisioning. The proposed retention remains 30 daily, 8 weekly, and 12 monthly. The `retention-plan` command verifies a complete run and states the policy without deletion. Complete-run deletion and pruning remain a separate future operator step; restic's simple path-grouped forget would be incorrect because each snapshot path contains a unique run ID. No prune or destructive retention ran in this slice.

Focused validation passed: nine new backup tests and five release-manifest tests, targeted Ruff and mypy checks, and a live Linux restic stdin path probe. `systemd-analyze verify` parsed the two future unit files but warned that the backup executable is not installed on VM 115, as required by the inactive boundary. The package build and broader accepted P12-04A checks were not rerun. The source runner remains unqualified against a production database because that database does not exist.

## P12-04 gates after this slice

1. Publish and obtain independent review of the sanitized P12-04B/r1 package. This implementation status is not acceptance.
2. Complete installed-package and systemd executable verification only at the separately approved release step.
3. P12-04C must separately review production provisioning, first real backup/readback, retention application, offline credential custody, and timer activation. No production database or API startup is authorized here.
