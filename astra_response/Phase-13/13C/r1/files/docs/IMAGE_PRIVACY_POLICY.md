# Approved image privacy and retention policy

**APPROVED BY BRIAN — Phase 13C, 2026-10-01.**

Marketplace Listings are private records of marketplace ads Brian evaluates.
Adding a record never publishes to Facebook, eBay, Poshmark or another marketplace.
Only Brian's authenticated owner session may access metadata, originals and thumbnails.
Raw screenshots and unknown sources are restricted; other listing images are private.
Derivatives inherit the applicable stricter classification. Shared canonical originals
can escalate privacy, never downgrade it. Classification grants no external rights.

Phase 13 submits no images to AI or providers and performs no training or dataset
export. Source URLs are saved references and are never automatically fetched.
Logs exclude image bytes, private filenames/text, credentials and authorization headers.

Originals and thumbnails have no scheduled deletion date. They remain retained until
an intentionally authorized future deletion feature is used. Originals are immutable
while retained. There is no automatic live-image or orphan deletion and no persisted
listing/image Delete control in this release. A future shared-blob deletion feature
must preserve every surviving reference. Report-only orphan inspection never deletes
or repairs objects and requires settled uploads for a definitive result.

Private storage is outside PostgreSQL PGDATA, static roots and immutable releases.
API image responses require owner authentication and use no-store; private API/image
bytes are never durably cached by the service worker. Client object URLs are temporary
and revoked when private views leave the document.

Image-containing backups remain encrypted and private. Historical backups follow
the existing approved retention and permanent-pin rules. Old backups are not rewritten;
permanent pins are not removed. Pinned recovery copies are not promised to expire.
The [combined recovery runbook](IMAGE_BACKUP_RECOVERY.md) binds database references
and actual bytes in a consistent recovery set.

Recognition remains Phase 14, native capture Phase 15, and dataset/export work Phase 16.
None is authorized here. [Plan 103](plans/103-phase-13-image-ingestion.md).
