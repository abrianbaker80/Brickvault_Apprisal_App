# Same populated combined recovery set

One image-inclusive normal dual backup completed: four artifacts, **eight destination readbacks**, exact hashes/sizes and repository checks, one protected schema-3 receipt. Its exact same Drive snapshots were selected for recovery. Every earlier receipt/pin remained unchanged; no additional backup was taken.

| Artifact | Bytes | Both copies and pre-restore hash |
| --- | ---: | --- |
| configuration.tar | 20480 | PASS |
| database.dump | 768651105 | PASS |
| globals.sql | 1454 | PASS |
| image-blobs.tar | 143360 | PASS |

Database size for capacity planning: 6580893375 bytes. The independent Windows Drive credentials confirmed the exact repository; VM credentials were not used for retrieval, with no Proxmox fallback. Windows relayed directly into off-host WSL without a persistent plaintext dump.

Existing WSL SQLAlchemy 1.4 failed to import the verifier before cluster creation/artifact retrieval. A disposable Python 3.13.15 runtime installed the exact hash-locked production libraries (SQLAlchemy 2.0.52, psycopg 3.3.5 and existing dependencies). Its dedicated SQLAlchemy connection uses tuple rows and a real UTC transaction; authentication probes keep dictionary rows. The production lock exports 3.13 wheel hashes, so matching Python also preserved hash enforcement. No application dependency/source/release changed and no backup repeated. The accepted PostgreSQL restore procedure remained intact.

Actual recovery used PostgreSQL 18 in a **9 GiB noswap tmpfs**, separate data/socket and no TCP listener. All four sizes/hashes passed before restore. Globals, eight allowlisted protected configuration/release files and the exact database identity restored, then pg_restore completed with zero failed/skipped objects. Strict extraction admitted only inventory regular members and exact original/thumbnail hashes.

All **82 table counts**, six image-table digests, blob inventory, normalized schema/object ownership/ACLs, roles/grants and catalog/auth/settings/watchlist context matched the captured backup inventory. Catalog remained generation 1, one accepted nonsynthetic snapshot and 28,278 sets. Owner/runtime SCRAM and least privilege passed. Relations, listing links and receipts resolved to present valid bytes; all referenced blobs, order and next_display_order=3 passed.

Comparison used this exact archive's frozen inventory, without requiring later live records or real user settings to be empty. [Machine evidence](validation.json). [Cleanup](recovery-cleanup.md).
