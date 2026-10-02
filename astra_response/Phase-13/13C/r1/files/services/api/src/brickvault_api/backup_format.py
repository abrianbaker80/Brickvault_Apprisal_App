"""Strict shared admission for legacy and image-inclusive recovery sets."""

import re
from datetime import UTC, datetime, timedelta
from typing import Any

LEGACY_ARTIFACTS = ("database.dump", "globals.sql", "configuration.tar")
IMAGE_ARTIFACTS = (*LEGACY_ARTIFACTS, "image-blobs.tar")
LEGACY_REVISION = "0016_hunt_cached_runs"
IMAGE_REVISION = "0017_listing_images"
HEX32 = re.compile(r"[a-f0-9]{32}\Z")
HEX64 = re.compile(r"[a-f0-9]{64}\Z")
FIELDS = {
    "schema",
    "purpose",
    "database",
    "ownership_marker",
    "run_id",
    "revisions_at_backup",
    "verified_at_utc",
    "repositories",
    "artifacts",
}


def required_artifacts(schema: Any, revisions: Any) -> tuple[str, ...]:
    if type(schema) is not int or type(revisions) is not list:
        raise ValueError("Invalid recovery format.")
    if schema == 2 and revisions in ([], [LEGACY_REVISION]):
        return LEGACY_ARTIFACTS
    if schema == 3 and revisions == [IMAGE_REVISION]:
        return IMAGE_ARTIFACTS
    raise ValueError("Unsupported recovery format or revision.")


def validate_receipt(
    run: str,
    record: dict[str, Any],
    repositories: dict[str, Any],
    marker: str,
    now: datetime | None = None,
) -> tuple[str, ...]:
    artifacts = required_artifacts(record.get("schema"), record.get("revisions_at_backup"))
    if (
        HEX32.fullmatch(run) is None
        or set(record) != FIELDS
        or record["purpose"] != "production"
        or record["database"] != "brickvault_appraisal_prod"
        or record["ownership_marker"] != marker
        or record["run_id"] != run
        or record["repositories"] != repositories
        or set(repositories) != {"proxmox", "drive"}
        or type(record["artifacts"]) is not dict
        or set(record["artifacts"]) != set(artifacts)
        or type(record["verified_at_utc"]) is not str
    ):
        raise ValueError("Invalid production receipt.")
    stamp = datetime.fromisoformat(record["verified_at_utc"])
    if stamp.utcoffset() != timedelta(0) or stamp > (now or datetime.now(UTC)):
        raise ValueError("Invalid receipt time.")
    seen: set[str] = set()
    for row in record["artifacts"].values():
        if (
            type(row) is not dict
            or set(row) != {"bytes", "sha256", "snapshots"}
            or type(row["bytes"]) is not int
            or row["bytes"] <= 0
            or type(row["sha256"]) is not str
            or HEX64.fullmatch(row["sha256"]) is None
            or type(row["snapshots"]) is not dict
            or set(row["snapshots"]) != set(repositories)
        ):
            raise ValueError("Invalid artifact receipt.")
        for identity in row["snapshots"].values():
            if type(identity) is not str or HEX64.fullmatch(identity) is None or identity in seen:
                raise ValueError("Ambiguous snapshot identity.")
            seen.add(identity)
    return artifacts
