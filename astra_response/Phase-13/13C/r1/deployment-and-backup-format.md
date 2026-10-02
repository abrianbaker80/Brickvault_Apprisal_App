# Deployment and compatible consistent capture

Release `phase13c-marketplace-intake-r1`, migration `0017_listing_images`.
Source baseline `1c7501092e7fad92a5471fa5571c6d009a1b0c3f` plus uncommitted 13C changes.
Reviewed source ID `791f09c12fbc7d8642e6578fc2e2428296dc63b7cb3a5af46aac90795bdffd08`.
Manifest SHA-256 `378bce4053dd9afb6d0d229536475353c727a80fecb25be2ca488a2740697d11`.
Wheel SHA-256 `c9d4c9841d9c54067a7e314e3dfe57dbde89de993bf9c5f69cc83a4861bd8e9d`.

Fresh admission verified the accepted 0016 release, ownership/runtime contract, catalog generation 1 / 28,278 sets, normal health, storage headroom and no maintenance conflict. One synthetic application-account proof on the chosen production data filesystem verified atomic non-overwriting publication, same-byte inode reuse, hashing and reading; its disposable directory was removed.

Private application-owned 0700 storage is outside PGDATA, static roots and immutable releases. Root backups can read it. BVA_IMAGE_BLOB_ROOT and absolute BVA_WEB_BUILD_DIR use the existing protected configuration mechanism. Only the narrow writable path and backup journal permissions were added; other unit hardening remains. The new immutable bundle was prepared beside the accepted release.

Exactly one normal pre-migration dual backup and supported finalize-proof preceded guarded migrate/grant-runtime. Migration and grants each ran once, preserving existing data. The six new tables retain least privilege. API was stopped before schema/activation and restarted only after the image-aware backup path and storage were ready.

The local helper initially misparsed the backup CLI's prefixed success message. Durable inspection found exactly one complete receipt; only proof finalization continued, without another backup. Activation health then found the intentionally paused backup/retention timers. Restoring their original states and repeating that failed check resolved the orchestration error; migration/deployment did not repeat. A read-only intake probe was corrected to the accepted restricted privacy classification for manual/unknown sources; no stored record was altered.

Schema-2 receipts/proofs require exactly three artifacts and empty/0016 revision. Schema 3 requires exactly four artifacts and 0017, including mandatory image-blobs.tar. Shared strict admission binds exact ownership/database/repository identities, digest and freshness. Unknown, extra, malformed or missing formats fail. Retention includes every artifact in its complete run; health shares its reader. Old receipts/proofs/pins and DEGRADED policy stay unchanged. No live forget/prune occurred.

The normal backup path journals prior API/health timer state, stops/settles the API, then holds one read-only REPEATABLE READ exported snapshot. It verifies every referenced blob and captures counts/digests/grants from that snapshot. pg_dump consumes the same snapshot; originals/thumbnails plus inventory stream as the fourth artifact. The pause remains through both encrypted readbacks and repository checks. Finally and scheduled ExecStopPost restore original state; failed resumption retains the protected journal. The installed normal service exercised this exact path. The observed service interval was 376 seconds; the API pause occupies its capture/readback portion.

Before schema change, the return strategy explicitly forbade starting the old 0016 app against 0017, dropping new tables or automatically restoring over newer data. Ambiguous failure requires durable inspection and an operator decision; reviewed same-schema forward activation is preferred. Destructive historical recovery needs separate authorization and reconciliation.

See the [source recovery runbook](files/docs/IMAGE_BACKUP_RECOVERY.md) and [approved policy](approved-policy.md).
