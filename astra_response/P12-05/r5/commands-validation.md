# Sanitized commands and validation

| Bounded action | Actual result |
|---|---|
| Read exact privately retained r4 FINAL receipt and its protected original bytes | PASS; exact expected artifact sizes/hashes |
| Unlock independent Windows DPAPI/ACL recovery context; restic cat config | Exact Drive identity PASS; no VM Drive credentials |
| Install local PostgreSQL 18 tools with default cluster/service creation inhibited | PASS; no default cluster or process |
| initdb/pg_ctl under dedicated off-host tmpfs; empty listen_addresses/separate socket | PASS; 10 GiB noswap, no TCP listener |
| Windows restic dump each exact receipt-selected Drive artifact directly to disposable consumer | All three sizes/SHA-256 PASS before restore |
| psql -X --no-password with ON_ERROR_STOP=1 for globals | PASS; no failing objects |
| Recovered protected descriptor / exact locale, owner, marker and database grants | PASS |
| pg_restore --exit-on-error --no-password into disposable database | PASS; no failing/skipped objects or diagnostics |
| Immediate source REPEATABLE READ / READ ONLY transaction | All application/catalog counts and required state captured privately |
| Accepted effective ACL / object/role / populated-state comparison | PASS; every table count matched |
| Owner/runtime password connections over isolated SCRAM-only socket | PASS; runtime least privilege preserved |
| pg_ctl stop; umount/remove task tmpfs; remove temporary consumer | PASS; no recovery process/socket/TCP listener or plaintext remains |
| Short production read-only normal health/current/catalog confirmation | PASS; all 13 checks and zero failed units |
| Additive documentation, protected-state and sanitized publication checks | PASS; no application source change |

Private source/backup paths, snapshot IDs, repository URIs, marker, IP/MAC,
catalog UUIDs, passwords/verifiers and credential-bearing commands are withheld.
No production repair, new backup, retention/prune, Gates 1-12 repeat or Phase 13.
