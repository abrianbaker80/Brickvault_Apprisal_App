# Corrected service design

P12-04C r1 correctly stopped after the first real backup failed before creating a snapshot or receipt. Its root runner used `runuser -u postgres`, and a transient sandbox reproduced `cannot set user id: Operation not permitted` under `NoNewPrivileges=true`. The proposed relaxation to `NoNewPrivileges=false` was never installed.

The accepted P12-04A PostgreSQL foundation already provides the narrow `brickvault_maintenance` mapping from OS root to database `postgres` on the local Unix socket. The service runs as root, so the corrected runner directly executes the absolute `pg_dump` and `pg_dumpall` binaries through that mapping. No PostgreSQL authentication configuration changed.

The runner removes `RUNUSER` from constants, command construction and executable preflight. It keeps exact socket/user/database selection, uses `--no-password`, closes standard input, clears inherited environment credentials, sets a nonexistent home directory and disables password-file lookup with `PGPASSFILE=/dev/null`. Dump output remains a stream in memory, copied to both encrypted repositories.

The installed unit keeps `NoNewPrivileges=true`, `RestrictSUIDSGID=true`, `PrivateTmp=true`, `PrivateDevices=true`, `ProtectSystem=strict`, `ProtectHome=true`, `ProtectKernelTunables=true`, `ProtectKernelModules=true`, `ProtectControlGroups=true`, the restrictive umask, and the accepted explicit writable directories. No fallback hardening relaxation was needed.
