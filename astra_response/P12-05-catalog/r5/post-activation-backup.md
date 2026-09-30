# Post-activation dual backup

Exactly one normal dual backup invocation passed. Proxmox PASS; Google Drive
PASS; three artifacts streamed without persistent plaintext; six encrypted
readbacks, exact hashes/sizes and both repository checks passed. Protected
schema-2 receipt SHA-256: `2548a2a4a64974406d8f25ed5c0329dcca815d9d267819aa44463d73f87ee358`.
Migration captured: 0016_hunt_cached_runs. Current release: `p12-05-catalog-repair-r1`.
Source catalog state stayed exact before/after the backup. Generation at backup:
1. Elapsed: 754.849 seconds.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| configuration.tar | 20,480 | `04c3d86bc697e4ca38ed53d24214fe5829b487c3c09afef30fed626edfbde1f7` |
| database.dump | 768,620,272 | `b2a24e4645ce67732af42778222bc10c5dd72c220ab1e1673def717ac59d8238` |
| globals.sql | 1,454 | `544c973b8c5d79159ca193bfdd87731873984648273b232bed03950e206bad19` |

No proof finalization, retention apply/prune, restore, persistent plaintext dump,
new destination or credentials. Normal scheduled backups outside this slice are
not counted as these explicitly authorized invocations. Repository/snapshot IDs,
paths, ownership marker, configuration and run UUIDs remain protected.


The guarded source state contained 28,278 sets, exactly one accepted active snapshot, one activation receipt, generation 1 and the failed predecessor/successful linked retry. That state stayed exact during backup and final inspection. Normal configuration capture included the repaired release manifest, current absolute web path and repaired health identity. The repaired release/locked runtime remains independently verified as the exact retained artifact; configuration.tar is the normal configuration backup, not a release-bundle archive.
