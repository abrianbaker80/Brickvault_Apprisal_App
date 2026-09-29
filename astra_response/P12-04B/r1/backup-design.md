# Production backup design

`brickvault-production-backup` is packaged as a console entry point but has not been installed or run against a production BrickVault database. The future service remains inactive.

## Admission guard

The runner requires OS root, root-owned protected configuration and passfiles, distinct restic repository passwords, the reviewed PostgreSQL 18 data directory, the provisioned production database and ownership marker, and exact configured repository IDs. It opens the encrypted rclone configuration and checks that its only remote is the dedicated Drive remote with `drive.file` scope and the recorded client identity. A mismatch refuses backup before a dump starts.

## Artifacts and receipt

One `pg_dump --format=custom` process produces one byte stream. A bounded Python tee sends identical chunks to both restic stdin children while hashing and counting bytes. It checks source and both child exit codes, broken pipes, cancellation and deadline. It never writes a plaintext dump to normal disk. PostgreSQL globals and required production configuration are separate streams under the same run ID. Restic passwords come from protected files, and child stdout/stderr are suppressed at the CLI boundary.

For each artifact, the runner resolves both snapshot IDs, streams an encrypted `restic dump` readback from each, compares size and SHA-256, and checks both repositories. Only then does it create a root-only receipt. `verify <run-id>` repeats readback and repository checks. Errors are redacted at the command boundary.

## Scheduling and retention

`brickvault-backup.service` and `.timer` are prepared but absent from VM 115. The service uses root only for protected input and local PostgreSQL access and has systemd filesystem/process restrictions. Its preflight refuses to run before provisioning.

The proposed policy is **30 daily, 8 weekly, 12 monthly**. `retention-plan <run-id>` verifies a complete run without deletion. Actual forget/prune is deferred: snapshot paths contain the unique run ID, so restic's simple path-grouped `forget` would retain every run. A later reviewed complete-run algorithm must preserve whole multi-artifact receipts and handle partial cross-repository failures before deletion is enabled. No destructive retention ran here.
