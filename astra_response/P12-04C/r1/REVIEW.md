# P12-04C r1 — blocked production activation checkpoint

**BLOCKED at the first real pre-migration backup.** This package records a partial, fail-closed P12-04C result for review. It does not qualify production migration or mark P12-04C ready.

Offline custody passed on a replacement removable SD card. The backup/admin integration passed focused validation, and immutable release `p12-04c-r3` was installed on VM 115 with the API inactive. The protected production descriptor and exact database/roles were provisioned; the database remains unmigrated with no application owner principal.

The one authorized production backup service start exited 1 before creating a new snapshot or protected receipt. A read-only transient service probe reproduced the failure: `NoNewPrivileges=true` prevents the root backup runner from switching to `postgres` for `pg_dump`. With that setting disabled and all other tested hardening intact, `runuser`, `pg_dump`, `pg_dumpall` and configuration tar streams passed. The corrected service definition is included here **as a local source change only**. It has not been installed on VM 115, and the production backup has not been retried.

## Review focus

- [Recovery-proof integration](recovery-proof-integration.md): schema 2 receipt, six encrypted readbacks, protected proof, revision and marker binding, and admin fail-closed validation.
- [Offline custody](offline-custody.md): replacement-media PASS and the disqualified first bundle, with no secret or media identifier.
- [Production state](production-db-activation.md) and [backup failure](real-backup-evidence.md): exact point reached and read-only root-cause diagnosis.
- [Plan 096](Plan-096.md), [validation](validation.txt), [sanitized commands](commands.txt), [cumulative patch](cumulative%20changes.patch) and [exact changed files](files/).

P12-04B remains ACCEPTED / CLOSED. Its synthetic Proxmox and Google Drive restore qualifications and backup source foundation are the starting context; no synthetic restore was rerun. P12-04 is IN PROGRESS, P12-04C is BLOCKED, and P12-05 has NOT STARTED.

## Boundary

No recovery proof, migration, runtime grant, owner bootstrap, post-bootstrap backup or timer activation occurred. The API stayed disabled/inactive. The first failed backup created no new snapshot in either repository. No backup artifacts, repository credentials, OAuth material, ownership marker, application password, private address or removable-media identifier are in this package.

`main` remains at `5b0fc9919d6755d1414527c27592b7df1068c96d`; it was not committed or pushed. Its index remains empty. The three pre-existing protected dirty files remain excluded from the nine-file P12-04C patch. Review and authorization to resume the failed live backup checkpoint are needed before installing the corrected unit and making another production backup attempt.

## Exact P12-04C changed-file inventory

- `CODEX_WORKFLOW.md`
- `deploy/systemd/brickvault-backup.service`
- `docs/ROADMAP.md`
- `docs/plans/096-production-database-activation.md`
- `scripts/release_manifest.py`
- `services/api/src/brickvault_api/production_admin.py`
- `services/api/src/brickvault_api/production_backup.py`
- `services/api/tests/unit/test_production_admin.py`
- `services/api/tests/unit/test_production_backup.py`
