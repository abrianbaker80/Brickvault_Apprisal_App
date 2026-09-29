# P12-04A r1 — production foundation review

## Outcome

**READY FOR P12-04A REVIEW.** VM 115 now has a dedicated PostgreSQL filesystem, verified Python 3.13.15 and uv 0.12.10, signed PGDG PostgreSQL 18.6 on loopback, a guarded production-admin CLI in the repository, and a hash-verified wheel/web release installed in a Python 3.13 venv. The API unit is installed, disabled and inactive. One controlled guest reboot proved the storage, PostgreSQL, SSH, QEMU agent and time state. VM 115 remains **RUNNING**, `onboot=0`.

P12-01, P12-02 and [P12-03](P12-03-CONTEXT.md) remain CLOSED. **P12-04 is IN PROGRESS; P12-05 is NOT STARTED.** This checkpoint ends before production data, secrets, backups, DNS/TLS or exposure. No production database, app roles, migration, runtime grant, owner bootstrap, ownership marker or principal was created. No Caddy, restic, rclone, backup destination/job, DNS record, certificate, firewall/router, provider or legacy VM 107 action occurred.

Main remains at `96b84359078632fef7a7193add663734cec8ba2c` with no P12-04A commit or push and an empty index. The three pre-existing dirty protected files were preserved byte-for-byte and unstaged.

## Review map

- [Source changes](SOURCE_CHANGES.md), [cumulative patch](cumulative%20changes.patch), and the [changed source/test/docs snapshot](source/).
- [Production administration design](production-admin-design.md), including the commands implemented but deliberately unexecuted against VM 115.
- [Runtime sources and patch path](runtime-sources.md).
- [Server storage, PostgreSQL, release and inactive service](server-foundation.md).
- [Sanitized command record](commands.txt) and [validation receipt](validation.txt).
- [Accepted P12-03 context](P12-03-CONTEXT.md).

## Release identity and focused evidence

The immutable staging identity is `p12-04a-r1`, source ID `c65188e2f3bfeecc140175e52f5ecab9a64c850710513c7a2c5aaf3ce9c7bc4c`, manifest SHA-256 `bfc6608efa56d1625f4493fe5e491b587ef95accacacf399fd44de38c6998ce9`, and API wheel SHA-256 `ec3e2ec4716046fae481aa85c76bc0eda1b6d81033c45c1c7548f7c7b16a9cf8`. The source ID binds baseline HEAD plus the literal P12-04A build, tests, lock and unit inputs; status documents and the protected dirty files are excluded to avoid a circular artifact identity. The VM copy passed the separately pinned manifest verification before venv installation.

Thirty focused admin tests passed. A disposable, locally owned PostgreSQL 18.6 proof confirmed SCRAM login, expected success/error paths and zero matches for five synthetic sensitive values in captured server logs; its container was removed. Three targeted real-database grant tests passed in a disposable database, which was removed, and the owned runner returned to stopped state. The production build passed the independent installed-wheel import and admin entrypoint checks, frontend verifier and artifact checks. On VM 115, 26 hash-locked dependencies and the wheel installed; `uv pip check`, installed import as `brickvault`, account/unit checks, and post-reboot storage/PG/listener/SSH/agent checks passed.

The next P12-04 checkpoint still needs reviewed encrypted recovery destinations and receipt, production data/secret custody, private DNS/TLS, proxy and backup implementation, and live acceptance before any migration, bootstrap or traffic serving. This r1 package requests review of the **foundation only**; it does not close P12-04 or qualify P12-05.
