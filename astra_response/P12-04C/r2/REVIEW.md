# P12-04C r2 — production database activated

**READY FOR P12-04C REVIEW.** The corrected backup runner uses the existing local root-to-postgres peer mapping directly. `runuser` is removed, and the installed service retains `NoNewPrivileges=true` and all other accepted sandbox protections.

The [accepted r1 blocked checkpoint](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/faa633933488cd7c054870d7b3cddff700c73c7c/astra_response/P12-04C/r1/REVIEW.md) remains intact. Its first failed backup created no snapshot/receipt. The provisioned database and roles were preserved. No PostgreSQL authentication change or fallback hardening relaxation was needed.

## Results

| Gate | Result |
|---|---|
| Offline custody | PASS on the accepted replacement SD bundle |
| Direct-root peer dump under NoNewPrivileges=true | PASS for pg_dump and pg_dumpall; no persistent dump or new snapshot |
| Focused source validation | 54 tests, targeted Ruff, format and mypy PASS |
| Immutable release | p12-04c-r4 installed and verified; r3 intact |
| One authorized pre-migration backup retry | PASS: both repositories, all three artifacts, six readbacks, size/SHA-256 matches, both repository checks |
| Derived recovery proof | PASS: protected receipt digest, marker, empty revision tuple, fresh timestamp, exclusive root-owned creation |
| Migration | PASS: 0016_hunt_cached_runs |
| Runtime grants | PASS: enumerated grants and least-privilege checks |
| Owner bootstrap/admin verify | PASS: one owner, password entered only through local hidden-input TTY |
| Post-bootstrap dual backup | PASS: both repositories, all artifacts, six readbacks, matching sizes/hashes and checks |
| Daily timer | enabled/active; next trigger 2026-09-30 03:22:03 UTC |
| API/network | API disabled/inactive; no api.env or Caddy; PostgreSQL only 127.0.0.1:5432 |

Both real backup receipts and the pre-migration proof are protected. Both real runs and each original synthetic canary are retained, with seven snapshots per destination. No destructive retention or additional manual scheduled backup ran. Backup/readback success is recorded; a real production restore drill remains a P12-05 gate.

## Evidence

- [Service correction and hardening](service-design.md)
- [Direct-peer probe](direct-peer-probe.md)
- [Source validation](source-validation.md)
- [Full release identity and hashes](release-identity.md)
- [Real recovery and activation evidence](recovery-and-activation.md)
- [Offline custody](offline-custody.md)
- [Plan 096](Plan-096.md), [remaining gates](remaining-gates.md), [validation](validation.txt), [sanitized commands](commands.txt)
- [Cumulative P12-04C patch](cumulative%20changes.patch) and [changed source/deploy/tests/docs](files/)

## Exact nine-file task inventory

- CODEX_WORKFLOW.md
- deploy/systemd/brickvault-backup.service
- docs/ROADMAP.md
- docs/plans/096-production-database-activation.md
- scripts/release_manifest.py
- services/api/src/brickvault_api/production_admin.py
- services/api/src/brickvault_api/production_backup.py
- services/api/tests/unit/test_production_admin.py
- services/api/tests/unit/test_production_backup.py

Main remains at `5b0fc9919d6755d1414527c27592b7df1068c96d`, uncommitted/unpushed with an empty index. The three protected dirty files are excluded and retain their accepted hashes. This publication contains no passwords, exact marker, OAuth/SSH credentials, private address, private run IDs or removable-media identifiers.

**P12-04C IMPLEMENTED / READY FOR REVIEW; P12-04 IN PROGRESS; P12-04D and P12-05 NOT STARTED.**
