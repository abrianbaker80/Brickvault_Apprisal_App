# Direct-root peer probe

A read-only transient service ran as root/root with the intended backup working directory, state/cache directories, write-path restrictions and all accepted sandbox settings, including `NoNewPrivileges=true` and `RestrictSUIDSGID=true`.

The probe confirmed OS uid/gid 0 and kernel `NoNewPrivs=1`. A credential-free local socket query confirmed current/session database identity `postgres`, no TCP address, no Alembic revision table and no application principal table.

Both direct commands succeeded with nonempty output consumed only in volatile memory:

    /usr/lib/postgresql/18/bin/pg_dump --format=custom --no-password --host=/var/run/postgresql --username=postgres --dbname=brickvault_appraisal_prod
    /usr/lib/postgresql/18/bin/pg_dumpall --globals-only --no-password --host=/var/run/postgresql --username=postgres

The child environment contained only PATH, HOME=/nonexistent and PGPASSFILE=/dev/null; standard input was closed. No password was supplied or requested. Before/after repository snapshot sets were identical, with one accepted synthetic canary per destination. Receipt/proof directories remained empty and the production revision tuple remained empty.

Safe result codes: DIRECT_PEER_IDENTITY_AND_UNMIGRATED_PASS; DIRECT_ROOT_DATABASE_PASS; DIRECT_ROOT_GLOBALS_PASS; NO_NEW_SNAPSHOTS_OR_RECEIPT_PROOF_UNMIGRATED_PASS; NO_NEW_PRIVILEGES_TRUE_DIRECT_PEER_PROBE_PASS.
