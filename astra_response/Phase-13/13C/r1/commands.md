# Sanitized operation receipts

Protected identities, proof arguments and isolated paths are redacted. These are the operation interfaces used in this bounded task.

```text
pnpm --filter @brickvault/web exec vitest run src/Listings.test.tsx -t "creates through generated metadata"
pnpm build

<prepared-release>/api/venv/bin/brickvault-production-backup backup
<prepared-release>/api/venv/bin/brickvault-production-backup finalize-proof <same verified pre-migration run>
<prepared-release>/api/venv/bin/brickvault-production-admin migrate --recovery-proof <generated protected proof>
<prepared-release>/api/venv/bin/brickvault-production-admin grant-runtime --recovery-proof <same generated protected proof>
<prepared-release>/api/venv/bin/brickvault-production-admin verify
systemctl start --no-block brickvault-backup.service

restic -r <exact protected Drive repository> cat config
restic -r <same Drive repository> dump <same receipt artifact snapshot> <same run>/<artifact>
```

The first backup command ran once before migration. The installed normal service ran once after intake, enforcing the same consistency path as its timer. Normal backup code performed both destination readbacks and repository checks before writing its receipt. Independent Windows restic output was piped directly into the disposable off-host consumer; no VM retrieval credentials or persistent Windows dump were used.

```text
initdb -D <isolated data> -U <bootstrap> --auth-local=trust --auth-host=scram-sha-256 --no-instructions
pg_ctl -D <isolated data> -l <isolated log> -w start
psql -X --no-password -v ON_ERROR_STOP=1 -h <separate socket> -p 55435 -U <bootstrap> -d postgres
pg_restore --exit-on-error --no-password -h <separate socket> -p 55435 -U <bootstrap> -d <exact recreated database> <verified dump>
pg_ctl -D <isolated data> -m fast -w stop
```

The isolated configuration set listen_addresses empty, a separate socket and UTC; all artifact hashes passed before restoration. Strict image_backup.extract_archive admitted only exact regular inventory members. The actual database_inventory implementation compared the captured inventory, then restored-role SCRAM/grant and image receipt/order probes ran. The 9 GiB noswap tmpfs and all disposable plaintext/runtime/helpers were removed.

Final checks used the installed production_health.checks(False), read-only release/schema/catalog/image retention checks and systemctl service/timer/failed-unit state. They took no new backup. Git closeout validated the exact 11-file staged receipt; the final 13C review validated the complete 20-file candidate, zero-context patch reverse check, whitespace, links, source-copy correspondence and private values. No main staging or 13C source commit occurred.
