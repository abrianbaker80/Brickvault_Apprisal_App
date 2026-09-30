# Production backup evidence — blocked catalog prerequisite

Exactly one normal pre-import production dual backup passed. Proxmox and Google
Drive each received all three encrypted artifacts; six encrypted readbacks
matched their source sizes and SHA-256 digests, both repository checks passed,
and a protected schema-2 receipt was written. Revision remained
`0016_hunt_cached_runs`; source table counts were unchanged during the backup.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| database.dump | 579623 | dbed36bf72435275c1b6d4fc65108fb6862b04738f7ab1f00df44d63f950073c |
| globals.sql | 1454 | cc19980f358e82ae2d9b57beaa8a4e5002d65f43c09f717a9ab4624925e12cdd |
| configuration.tar | 20480 | 3ec57ccb0f4749832c82c540fe334c90e187c53b466abe9028f2d039c46616f3 |

Protected receipt SHA-256:
`0f02c76c5c45acc5940fb45cafa29fb347cf6944d04cd11262732d5622376d59`.
This recovery point contains the pre-import database, whose catalog tables were
empty. It does not establish recovery of an activated catalog.

The sole import subsequently ended with `database_failure`. No snapshot was
accepted or activated. The required post-activation backup and targeted backup
metadata sanity check are **UNRUN**. No second backup, migration recovery proof,
restore rehearsal, retention apply or prune was performed in this prerequisite.
The terminal import history, candidate and staging rows remain preserved.
