# Final current-state Google Drive-only restore — PASS

The three artifacts were selected from the same privately retained FINAL P12-05
schema-2 receipt, not a latest-snapshot guess. Exact Drive repository identity
matched. Independent Windows ACL/DPAPI-protected recovery context performed every
Drive retrieval; VM115 Drive credentials were not used. No Proxmox repository
fallback or new backup invocation. No repository/backup/snapshot identity or
credential is published.

| Artifact | Bytes | SHA-256 verified before restore |
|---|---:|---|
| globals.sql | 1,454 | `214d2260cef07c00095f0365dfee465062771d912647007e0eade51eb4dd5587` |
| configuration.tar | 20,480 | `345bf0c016c777f76073dacdafa6f9746bbe578e37f23319f6c6c1a6304f88d9` |
| database.dump | 768,622,342 | `64a3357acec037c86af98214f3a63a29686278aa2f68d2fde92478b08502e0cc` |

The accepted Windows credential unlock, restic stream, globals/configuration/
database restore and qualification procedure was reused. Actual incompatibilities
required operator adaptations: the earlier consumer was on VM115, whereas this
request requires off-host recovery; its 8 MiB dump guard/256 MiB tmpfs also cannot
fit the populated 768,622,342-byte dump. The consumer therefore ran in existing
Windows WSL Ubuntu with task-owned separate PostgreSQL 18 data and socket, empty
listen_addresses and no TCP listener. A 10 GiB tmpfs with noswap contained recovered
plaintext; source size was about 6.13 GiB and available recovery RAM exceeded
12 GiB. Exact production database locale/encoding were recreated.

Missing PostgreSQL 18 tools were installed locally using the official PGDG Ubuntu
repository, with default cluster creation and service startup inhibited. This
changed no production machine or application dependency/release. The accepted
provisioned-identity guard was reused without changed checks. All selected hashes
passed before globals, protected configuration/database identity and database.dump
were restored. Psql used ON_ERROR_STOP; pg_restore used exit-on-error. No skipped
or failing objects or restore diagnostics. The initial populated restore succeeded
but its comparison stopped because current production Watchlist contained one
item. Cleanup passed. After Brian cleared Watchlist and signed out locally, a
second database restore passed but an operator transaction-ordering error
prevented comparison; disposable cleanup passed again. Correcting SET TRANSACTION
to precede the first guard query allowed the third restore to match all counts
and security. Its full audit hashes differed under the local America/Chicago
timezone versus production Etc/UTC; a disposable initdb-only probe confirmed the
default. The recovery timezone was set to exact production Etc/UTC. The fourth
restore of the same backup completed full exact qualification, without excluding
data or comparison fields. No production repair or new backup.

Windows streamed plaintext directly into the disposable off-host environment;
no persistent plaintext database dump was created on Windows. Private metadata,
configuration, verifiers and recovery logs stayed in memory or protected tmpfs
and were removed after verification. [Cleanup](recovery-cleanup.md).

An initial setup admission stopped before any artifact restore because a mount
option assertion included findmnt's trailing newline. A mount-only check proved
the cause, cleanup passed and the operator parser was corrected while retaining
the noswap requirement. The extracted guard's dataclass decorator was retained
before restore. The recorded Watchlist blocker is retained as dated history in
Plan 099. No application repair, backup retry or weakened contract.
