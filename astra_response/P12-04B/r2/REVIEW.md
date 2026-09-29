# P12-04B/r2 — accepted dual recovery closeout

**P12-04B is ACCEPTED / CLOSED. P12-04 remains IN PROGRESS. P12-04C is NEXT / NOT STARTED; P12-05 has NOT STARTED.** This package records Brian's acceptance of the [r1 implementation and live qualification](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f179992addabb2fc7eb666280c2b218ba1474bfb/astra_response/P12-04B/r1/REVIEW.md). It contains no new live qualification.

Main has one local, unpushed commit, `5b0fc9919d6755d1414527c27592b7df1068c96d` — `Close P12-04B dual recovery foundation`. The [committed inventory](committed-inventory.txt) is exactly ten reviewed P12-04B files. The [cumulative patch](cumulative%20changes.patch) covers only those files from the accepted base `ef7eba53ff2a8c63bd15db1adb589b2e8c3f8449` through that local commit. [Final Plan 095](final-Plan-095.md) records the accepted result and remaining gates.

## Accepted recovery result

Verified official restic 0.19.1 and rclone 1.75.1 support two independently encrypted repositories with distinct passwords. The restricted `bva-backup` account serves the same-host Proxmox copy from `rpool/brickvault-backup` at `/var/lib/brickvault-backup`, bounded by a 64 GiB quota. Google Drive holds the off-host copy at `Brickvault_Apprisal_App_Backup/restic-production` through a separate Desktop OAuth client and protected `drive.file` rclone configuration. The existing broader Drive configuration was preserved.

VM 115 wrote a synthetic canary to both repositories. The Windows recovery context independently restored each one and matched the pre-recorded bytes, size, and SHA-256: **Proxmox PASS; Google Drive PASS.** Protected recovery credentials exist on both VM 115 and Brian's Windows laptop. These results qualify the synthetic recovery foundation; no real production database restore has occurred.

The accepted `brickvault-production-backup` source guards the production identity, streams one `pg_dump` to both destinations without a normal-disk plaintext dump, verifies encrypted readback and repository health, then writes a protected receipt. Nine backup tests and five release-manifest tests, targeted Ruff and mypy, and the live restic stdin probe passed in r1. The service and timer definitions remain uninstalled and inactive. No production database, migration, owner bootstrap, API startup, Caddy, DNS, TLS, or destructive retention occurred.

## Required before production migration

The [receipt-schema integration gate](gates.md#backupadmin-receipt-integration) is explicit: the backup receipt does not yet satisfy `brickvault-production-admin`'s migration proof schema. P12-04C must derive a protected admin proof from a complete, freshly verified dual backup and the exact pre-migration revision tuple. It must never accept arbitrary operator-entered snapshot hashes or weaken the admin gate.

The [offline-custody gate](gates.md#offline-recovery-custody) also remains open. VM and Windows copies survive loss of either one; they do not survive simultaneous loss of both. P12-04C must establish durable offline access to both repositories before migration. [All remaining gates](gates.md#remaining-p12-04-and-p12-05-gates) stay open.

## Closeout validation

The [validation record](closeout-validation.txt) shows exact staged inventory, complete diff review, `git diff --cached --check`, new Markdown link checks, protected hashes, and final main/index/worktree state. The seven source/deployment files outside the three status documents matched r1 byte-for-byte after Git line-ending normalization. The only unstaged files after the local commit are the three protected pre-existing dirty files. No VM, Proxmox, Google Drive, restic, rclone, canary, test, Ruff, or mypy work was rerun for closeout. Main was not pushed.
