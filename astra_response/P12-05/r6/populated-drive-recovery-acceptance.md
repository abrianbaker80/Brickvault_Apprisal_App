# Populated FINAL Google Drive-only recovery — accepted

Brian independently accepted [r5](../r5/REVIEW.md), `57dec1e5f7b0538c75f2a17a824c15aba3083dc2`.
This closeout reuses that evidence and did not perform another recovery or backup.

All three FINAL artifacts came from the same privately retained protected receipt.
The exact Drive repository identity matched; independent Windows credentials
retrieved them without VM115 Drive credentials or Proxmox repository fallback.
Each size/SHA-256 passed before restore:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| globals.sql | 1,454 | `214d2260cef07c00095f0365dfee465062771d912647007e0eade51eb4dd5587` |
| configuration.tar | 20,480 | `345bf0c016c777f76073dacdafa6f9746bbe578e37f23319f6c6c1a6304f88d9` |
| database.dump | 768,622,342 | `64a3357acec037c86af98214f3a63a29686278aa2f68d2fde92478b08502e0cc` |

Globals, protected configuration/exact database identity and the populated dump
restored into task-owned off-host PostgreSQL 18, with separate data/socket, no
TCP listener and disposable noswap tmpfs. No persistent plaintext dump was created
on Windows. The qualifying restore completed without failing/skipped objects.
All 76 application/catalog table counts, normalized ownership/effective grants,
role contract, owner/runtime SCRAM authentication and least privilege matched.
Full populated catalog audit, principal/settings/cleanup and known-set comparisons
passed. Generation 1 / 28,278 sets, one active accepted snapshot and activation
receipt, failed predecessor audit and successful linked retry were preserved.

Accepted cleanup stopped the disposable cluster, removed its data/socket and all
recovered plaintext/configuration, unmounted/removed tmpfs and confirmed no recovery
process/listener remained. The accepted short production read-only health check
passed all 13 normal checks with zero failed units and unchanged release/catalog.
The four actual restore attempts and local operator corrections remain documented
in r5 and [Plan 099](Plan-099.md); closure does not erase the earlier blocker.

Sources: [restore procedure/results](../r5/final-current-state-drive-restore.md),
[full comparison](../r5/restored-data-comparison.md),
[comparison record](../r5/restored-data-comparison.json) and
[cleanup](../r5/recovery-cleanup.md). No recovered private metadata is republished.
