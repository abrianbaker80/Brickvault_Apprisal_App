# Pre-recovery dual backup

Exactly one normal dual backup invocation passed. Proxmox PASS; Google Drive
PASS; three artifacts streamed without persistent plaintext; six encrypted
readbacks, exact hashes/sizes and both repository checks passed. Protected
schema-2 receipt SHA-256: `40a0018c30ef9e7deb59a6793b587e1d9bf80d3747a506f4bc8a58c840cf6b78`.
Migration captured: 0016_hunt_cached_runs. Current release: `p12-04e-r6`.
Source catalog state stayed exact before/after the backup. Generation at backup:
0. Elapsed: 222.446 seconds.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| configuration.tar | 20,480 | `3ec57ccb0f4749832c82c540fe334c90e187c53b466abe9028f2d039c46616f3` |
| database.dump | 273,449,903 | `bc2f36923061a4694411fbc120aeb1f9418444996f139ab918e6298c4087b878` |
| globals.sql | 1,454 | `e5d7e764b5f6aedc6a14de28ab7ea748b3e48364239448f3f2cd35e651bfdb07` |

No proof finalization, retention apply/prune, restore, persistent plaintext dump,
new destination or credentials. Normal scheduled backups outside this slice are
not counted as these explicitly authorized invocations. Repository/snapshot IDs,
paths, ownership marker, configuration and run UUIDs remain protected.


The original failed audit/candidate/source/12-file/1,898,466-row staging state was rechecked unchanged before installation/retirement. Canonical/validation/activation rows were zero; active snapshot NULL, generation 0.
