# P12-04B/r1 — dual encrypted recovery foundation

**Review status:** implemented and ready for independent review. P12-04A is accepted; P12-04 remains in progress. P12-05 and P12-04C have not started.

## Result

Two separate restic repositories were initialized with distinct high-entropy passwords. The Proxmox repository is a bounded, restricted same-host supplemental copy. The Google Drive repository is the off-host copy under `Brickvault_Apprisal_App_Backup/restic-production`, accessed through a new Desktop OAuth client and an encrypted rclone configuration requesting `drive.file`. The existing broader Drive client and configuration were preserved.

VM 115 backed up one synthetic canary to each repository. The Windows laptop independently opened both repositories, restored the matching snapshots into fresh private temporary directories, and verified the exact pre-recorded manifest, file bytes, size, and SHA-256. **Both Windows restores passed.** No production BrickVault data was backed up because no production database exists.

## Live safety and custody

- The Proxmox `rpool/brickvault-backup` ZFS child mounts at `/var/lib/brickvault-backup` with a 64 GiB quota. It is not registered as general VM storage. The `bva-backup` account is key-only, chrooted to internal SFTP, without a login shell or sudo. Existing Proxmox root SSH was retested after the dedicated sshd fragment was reloaded.
- VM backup credentials and repository identity metadata are root-only under `/etc/brickvault/backup`. A separate Windows recovery set under Brian's profile has ACLs limited to Brian, SYSTEM, and Administrators. Its new rclone configuration is encrypted with user-bound DPAPI unlock custody. Repository passwords differ.
- The VM still has PostgreSQL 18.6 bound only to loopback and **zero** BrickVault production databases or roles. The API unit is disabled/inactive with no listener. Caddy, production secrets, DNS, TLS, migration and bootstrap work remain untouched. Backup service and timer definitions are source-only and are not installed or enabled.

## Source and checks

The [backup design](backup-design.md) explains the guarded `brickvault-production-backup` runner, dual stream, encrypted readback, and deferred deletion policy. The [qualification record](recovery-qualification.md), [tool sources](runtime-sources.md), [sanitized commands](commands.txt), and [validation record](validation.txt) contain the point-in-time evidence. [Plan 095](changed/docs/plans/095-dual-recovery-foundation.md) records remaining P12-04 gates. The `changed/` tree mirrors the ten changed source, test, deployment and status files; [cumulative changes.patch](cumulative%20changes.patch) contains only those changes from main `ef7eba53ff2a8c63bd15db1adb589b2e8c3f8449`.

Focused source checks passed: **14 tests**, targeted Ruff and mypy. Linux restic stdin path behavior was probed. `systemd-analyze verify` parsed the future units and reported the expected missing executable because the new backup package has not been installed on VM 115. Accepted P12-04A builds and tests were not rerun.

## Remaining gates

This package is not P12-04 acceptance. A later separately authorized step must provision the production database, qualify a real backup/readback, resolve offline recovery custody for simultaneous VM/laptop loss, install and verify the packaged backup executable, implement and review complete-run retention deletion, and decide when to enable the timer. The existing Cloud project's unverified broader Drive scope is a separate account-level warning; this slice's new remote requests `drive.file` and completed live backup/restore operations.

The three protected dirty files on main retained their accepted SHA-256 hashes and remained unstaged. Main stayed at `ef7eba53ff2a8c63bd15db1adb589b2e8c3f8449` with an empty index. No main commit or push occurred.
