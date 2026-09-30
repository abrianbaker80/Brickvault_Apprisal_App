# P12-04C r3 — accepted closeout

**P12-04C ACCEPTED / CLOSED. P12-04 IN PROGRESS. P12-04D NEXT / NOT STARTED. P12-05 NOT STARTED.**

Brian accepted the [r2 package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/REVIEW.md). This publication records the local checkpoint and carries forward that accepted evidence. No live, test, build or recovery work was rerun. The r1 and r2 folders are preserved.

## Local checkpoint

Commit: `0d29d5f7f07f379ade834ee22cfaf4e7da9587c4`

Subject: `Close P12-04C production database activation`

Parent: `5b0fc9919d6755d1414527c27592b7df1068c96d`

Main was committed locally and was not pushed. Its index is empty; only the three protected pre-existing modifications remain. Their accepted hashes are unchanged and they remain unstaged; see [closeout validation](closeout-validation.txt).

## Exact committed inventory

- `CODEX_WORKFLOW.md`
- `deploy/systemd/brickvault-backup.service`
- `docs/ROADMAP.md`
- `docs/plans/096-production-database-activation.md`
- `scripts/release_manifest.py`
- `services/api/src/brickvault_api/production_admin.py`
- `services/api/src/brickvault_api/production_backup.py`
- `services/api/tests/unit/test_production_admin.py`
- `services/api/tests/unit/test_production_backup.py`

[Commit record](local-commit.txt), [inventory](committed-inventory.txt), [cumulative P12-04C patch](cumulative%20changes.patch), [final Plan 096](Plan-096.md), and [exact file copies](files/).
The presentation plan adjusts two relative links; its exact committed counterpart is under `files/docs/plans/`.

## Accepted production and recovery state

The following describes accepted r2 evidence, not a new live observation:

- Offline custody PASS on replacement removable media, with the phrase held separately. The first exposed-phrase medium was retired/destroyed. Credential recovery survives simultaneous VM/laptop loss.
- Immutable release `p12-04c-r4`; source ID `6c0ca52d142b2018c2a4b7a72342705196e1cb72e883cb352e91a3f167cb6536`; manifest SHA-256 `980b7d9894eeee745bd8c7e8222714790f8ac6a56e7812d1d0c6d9fd29ae96a8`.
- Direct root `pg_dump` / `pg_dumpall` use the reviewed Unix-socket peer mapping. `runuser` is removed; PostgreSQL authentication is unchanged. `NoNewPrivileges=true`, `RestrictSUIDSGID=true` and all accepted sandbox settings are retained. Direct-root probes passed without a persistent plaintext dump.
- `brickvault_appraisal_prod` and its owner/runtime roles were provisioned and verified. Migration reached `0016_hunt_cached_runs`. Runtime enumerated least privileges passed; no schema/database CREATE, TEMPORARY or migration writes; PUBLIC grants revoked.
- Exactly one private owner was bootstrapped through local hidden-input TTY. Password and ownership marker remain private. Independent production-admin verification passed.
- Real pre-migration and post-bootstrap backups each contain `database.dump`, `globals.sql` and `configuration.tar` in independently encrypted Proxmox supplemental and Google Drive off-host repositories. Each run passed six encrypted readbacks, byte/SHA-256 comparisons and both repository checks, producing a protected schema-2 receipt.
- The generated pre-migration proof binds the exact database, private marker, empty revision tuple, receipt digest, repository and snapshot identities, and fresh UTC verification time. Migration, grants and bootstrap used only that generated proof. No proof was fabricated. The later receipt records `0016_hunt_cached_runs`.
- Both real runs and synthetic canaries were retained; no forget/prune occurred. The timer was enabled/active, with next trigger at evidence time `2026-09-30 03:22:03 UTC`. The backup service was inactive after successful completion.
- The API was disabled/inactive, with no `api.env`, API listener, Caddy, DNS or certificate/TLS setup. PostgreSQL listened only on `127.0.0.1:5432`.

## Accepted validation reused

54 focused tests, targeted Ruff, format, strict mypy, production build, independent wheel verification, frontend verifier, release manifest, installed CLI/migration graph, direct-root probes, both real backup/readback runs and independent admin verification passed in r2. None was rerun for closeout.

- [Source validation](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/source-validation.md)
- [Service design](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/service-design.md) and [direct-peer probes](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/direct-peer-probe.md)
- [Release identity](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/release-identity.md)
- [Real recovery and activation](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/recovery-and-activation.md)
- [Offline custody](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/offline-custody.md)

## Remaining gates

Remaining gates stay OPEN:

- Complete-run destructive retention implementation/review.
- Production API configuration/secrets and API startup.
- Private DNS, trusted production certificate, Caddy and private HTTPS path.
- Firewall/client-source policy.
- Monitoring and alert destination.
- Deliberate production VM onboot behavior.
- CPython 3.13 maintenance/update monitoring.
- Unrelated protected-backup identity rotation review recorded in Plan 096.
- P12-05 real production restore, browser/PWA acceptance, physical Android normal-TLS acceptance and rollback rehearsal.

Real backup/readback success does not qualify a real production restore. P12-04D and P12-05 were not started during closeout.
