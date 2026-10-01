# Proposed image privacy and retention policy

**PROPOSED FOR BRIAN'S REVIEW — NOT PRODUCTION SHIPPING APPROVAL.**

Purpose: optional Brian-owned private marketplace sourcing/listing review.
Access: Brian's existing private owner session only. Original seller/listing
photos are private; raw screenshots and unknown sources are restricted. Explicit
seller_photo/listing_photo classification records the uploader's intended class,
not automated content recognition. All derivatives inherit the stricter original
class; sharing a canonical original can escalate privacy but never downgrade it.
Classification does not confer export, provider or training rights.

Original bytes stay immutable while retained. Phase 13 implements no deletion,
automatic retention, AI/provider submission, training or export. Source URLs are
metadata only and never fetched. Private filenames remain metadata/owner response
only; logs exclude names, private text, image bytes and credentials.

Storage and future backups must remain private, outside all public/static roots.
API bytes require authentication and no-store responses. Phase 13A uses only
synthetic local fixtures and is not deployed. A definitive report-only orphan
inspection requires uploads stopped and does not delete/repair any objects.

Before shipping, Brian must approve retention durations for originals,
screenshots, derivatives, backups and exports; intentional deletion/removal and
shared-blob reference handling; and consistent database-plus-blob backup/recovery.
Immutability protects against accidental overwrite and does not override an
eventual deliberately approved deletion policy. Manual deletion workflows are
deferred beyond 13A. [Plan 103](plans/103-phase-13-image-ingestion.md).
