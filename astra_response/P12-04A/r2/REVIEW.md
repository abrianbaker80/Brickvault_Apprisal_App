# P12-04A accepted closeout (r2)

**P12-04A is ACCEPTED / CLOSED. P12-04 remains IN PROGRESS. Its next checkpoint and P12-05 are NOT STARTED.** ChatGPT accepted the [published r1 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/22f80286b1b82d7862b922fe2d66fd06fa84cf9b/astra_response/P12-04A/r1/REVIEW.md). This r2 package records the local closeout; it reuses the r1 implementation, test and live-server evidence.

Local main commit: `ef7eba53ff2a8c63bd15db1adb589b2e8c3f8449` — `Close P12-04A production foundation`. Main was not pushed. See the [exact 16-file inventory](COMMITTED_FILES.md), [cumulative patch](cumulative%20changes.patch), [final Plan 094](094-production-foundation.md) and [closeout validation](VALIDATION.md).

## Accepted foundation

VM 115 (`brickvault-appraisal`) runs Ubuntu Server 24.04.5 LTS with `onboot=0`. Its 128-GiB `scsi1` has GPT, one ext4 partition labeled `brickvault-db`, and a required UUID mount at `/var/lib/postgresql`. Signed PGDG Noble PostgreSQL 18.6 is enabled and active with data on that disk and TCP bound only to `127.0.0.1:5432`; no production BrickVault database or roles exist. Signed Python.org CPython 3.13.15 is installed at `/opt/python/3.13.15` without replacing Ubuntu Python 3.12. Official Astral uv 0.12.10 is at `/usr/local/bin/uv` and does not manage Python.

The locked `brickvault` service account has no login or sudo. Release `p12-04a-r1` was installed with 26 hash-locked dependencies and the reviewed API wheel in a Python 3.13 virtualenv. Source ID: `c65188e2f3bfeecc140175e52f5ecab9a64c850710513c7a2c5aaf3ce9c7bc4c`; manifest SHA-256: `bfc6608efa56d1625f4493fe5e491b587ef95accacacf399fd44de38c6998ce9`; wheel SHA-256: `ec3e2ec4716046fae481aa85c76bc0eda1b6d81033c45c1c7548f7c7b16a9cf8`. The API unit is installed, verified, disabled and inactive; its required environment file is absent and no API listener exists.

The guarded `brickvault-production-admin` CLI provides `preflight`, `provision-db`, `migrate`, `grant-runtime`, `bootstrap-owner` and `verify`. The accepted r1 evidence includes 30 focused tests, a disposable PostgreSQL credential/logging proof and three focused runtime-grant database tests. No real production mutation command ran. No production roles, database, marker, migration, runtime grants, owner, application or proxy secrets, Caddy, DNS, certificate, backup repository/job, provider credentials or legacy database access were created.

## Remaining P12-04 gates

- Create and verify both independently encrypted recovery copies before any recovery receipt or first production migration/bootstrap. The receipt itself proves neither backups nor restore.
- Plan and execute guarded production database/role provisioning, migration, runtime grants and owner bootstrap under their separate prerequisites.
- Complete private network scope, secrets, backup jobs and restore verification, DNS, certificates, TLS, Caddy, API startup, monitoring and acceptance in later authorized checkpoints.
- Track CPython 3.13 security releases and use a newly verified signed-source versioned installation for upgrades. Keep Ubuntu `/usr/bin/python3` unchanged.
- Deliberately resolve VM `onboot=0` production startup behavior before Phase 12 closes. Keep the accepted ext4 label `brickvault-db`; do not rename or reformat it.

P12-04 is not complete. This publication does not begin its next checkpoint or P12-05.
