# Marketplace image production capture and recovery

Phase 13C extends the existing two encrypted repositories and protected receipts.
No new repository, automatic image deletion or retention policy is introduced.

## Supported sets and guarded transition

Receipt/proof schema 2 requires exactly database.dump, globals.sql and
configuration.tar, with empty foundation revision or 0016_hunt_cached_runs.
Schema 3 requires those three artifacts **and image-blobs.tar**, with exactly
0017_listing_images. Unknown versions, extra fields, absent image archives,
incomplete destinations and ambiguous snapshot identities are refused. Shared
backup_format admission is used by backup verification, admin proofs and retention;
health uses the same retention validator. Each complete run has two independently
verified copies of every required artifact. Old receipts/proofs/pins stay unchanged.

A fresh schema-2 backup of production 0016 can authorize the reviewed upgrade to
0017 and subsequent enumerated runtime grants. The real backup finalize-proof
command creates the protected proof; migrate and grant-runtime consume its exact
path. This never implies the old application is compatible with the new schema.

## Normal consistent capture

The normal `brickvault-production-backup backup` command owns the existing
backup/retention lock. For 0017 it journals prior API/health-timer states in a
root-only runtime directory, pauses health timers and stops the API, verifies
MainPID=0, then keeps one read-only REPEATABLE READ transaction open. In-flight
requests finish or roll back before capture. An exported snapshot is passed to
pg_dump. The image inventory uses that same snapshot. All referenced keys/hashes/
sizes are verified before the first artifact is sent. Originals and thumbnails
are streamed into image-blobs.tar alongside inventory.json; dump and archives
are never staged as persistent plaintext production files.

The API remains stopped through dual stream/readback and repository checks.
This intentionally causes bounded downtime during image-inclusive backups.
Normal failure and SIGTERM restore prior service state. Scheduled service
ExecStopPost also recovers journaled state after process termination; a live
capture PID or malformed journal prevents unsafe resumption. Failed resumption
retains its protected journal for operator review. Scheduled and manual backups
use the same code and consistency mechanism. No one-off capture bypass exists.

The inventory contains captured table counts, image-table digests, normalized
ownership/grants and every referenced blob key/hash/size. Orphan objects are not
deleted or represented as successful application uploads. Every database blob
must appear in the archive. Complete-run retention handles four artifacts for
schema 3 and three for schema 2, retaining permanent pins and DEGRADED semantics.
Phase 13C performs no live forget/prune.

## Private storage and release admission

The configured BVA_IMAGE_BLOB_ROOT is a 0700 directory owned by the application
account on the existing data filesystem, beside PostgreSQL PGDATA. It is outside
PGDATA, immutable releases and public/static roots. Root backups can read it.
The API unit adds only that narrow writable path; all other hardening remains.
Release activation uses the absolute BVA_WEB_BUILD_DIR and retained immutable
bundle/manifest/locked dependencies. Prepare the new bundle beside the old one.
Before changing schema, retain one verified dual recovery point and exact prior
configuration/service/release identities privately.

On activation failure after 0017, keep maintenance in effect and inspect durable
migration/grant/configuration state. Prefer corrected same-schema forward
activation after review. Do not blindly start the 0016 application, downgrade/drop
image tables, or restore over newer user activity. A destructive historical recovery
requires an explicit operator decision and reconciliation of later data.

## Independent Drive-only recovery

Select every artifact from one protected receipt. Use the already established
independent Windows recovery credentials, confirm the exact Drive repository,
and stream artifacts directly into an isolated off-host target. Never retrieve
with VM Drive credentials or fall back to the Proxmox repository. No persistent
plaintext database dump is written on Windows. Size recovery storage from actual
captured database/artifact size and available memory/filesystem headroom.

Verify all artifact bytes and SHA-256 before restoration. Restore globals,
safely extract the allowlisted protected configuration, create the exact database
identity/locale/owner, then pg_restore with exit-on-error into disposable PostgreSQL
18 with separate data/socket and no TCP listener. Never target live PGDATA.
Extract image-blobs.tar with `image_backup.extract_archive(archive, destination)`;
the destination must be new, absolute and outside production storage. Only exact
inventory members are admitted; links, traversal, duplicates, extra/missing files,
wrong sizes and hashes fail. No generic tar extract or overwrite mode is used.

Compare restored counts, six image tables, lineage/links/receipts/order and normalized
ownership/grants with the embedded captured snapshot inventory, never later live
activity. Verify every referenced original and thumbnail, next_display_order and
owner/runtime SCRAM authentication. Preserve the existing locale/timezone and ACL
default normalization used by the accepted recovery procedure.

Stop/remove only the disposable cluster, sockets, recovered plaintext/configuration,
mounts and task helpers. Retain production intake/images and encrypted backups.
A final short production health/storage/timer check takes no additional backup.

[Approved privacy policy](IMAGE_PRIVACY_POLICY.md). [Plan 103](plans/103-phase-13-image-ingestion.md).
