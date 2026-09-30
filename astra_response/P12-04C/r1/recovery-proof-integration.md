# Backup receipt to admin recovery proof

The P12-04B backup receipt and admin migration proof had incompatible schemas. P12-04C source integration records schema 2 receipts under the root-owned `/etc/brickvault/backup/receipts` directory. A receipt binds the exact production database and ownership marker, run ID, revision tuple at backup, both repository identities, and each of three artifacts' size, SHA-256 and per-destination snapshot ID.

`brickvault-production-backup finalize-proof <run-id>` accepts only an existing protected receipt. It checks its complete schema and recency, reopens all six encrypted artifact copies, verifies their size/digest, checks both repositories, and compares the current revision tuple before exclusive creation of a protected proof under `/etc/brickvault/backup/proofs`. The proof includes a digest of the exact receipt. Production admin commands revalidate the proof, receipt and both repositories before migration, grants or bootstrap. Operators cannot supply arbitrary snapshot hashes.

Focused validation passed 46 backup/admin tests and five release-manifest tests, with targeted Ruff, format and mypy. This is **source validation only**: the first real production backup failed before any receipt existed, so no production proof has been finalized or exercised by a live migration.
