"""Complete-run retention. All identifiers stay in protected local state."""

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import operational_alert as protected

ARTIFACTS = {"database.dump", "globals.sql", "configuration.tar"}
DESTINATIONS = {"proxmox", "drive"}
HEX32 = re.compile(r"[a-f0-9]{32}\Z")
HEX64 = re.compile(r"[a-f0-9]{64}\Z")
PINS = Path("/etc/brickvault/backup/retention-pins.json")
STATE = Path("/etc/brickvault/backup/retention")
LOCK = Path("/run/brickvault-backup-retention.lock")
MAX_STATE_BYTES = 16 * 1024 * 1024


class RetentionError(RuntimeError):
    """Retention must stop without disclosing private history."""


def read_state(path: Path) -> dict[str, Any]:
    # Full snapshot evidence and the durable deleted-run ledger exceed config size.
    return protected.protected_json(path, max_bytes=MAX_STATE_BYTES)


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def stamp(value: Any, now: datetime) -> datetime:
    if not isinstance(value, str):
        raise RetentionError("Invalid receipt time.")
    result = datetime.fromisoformat(value)
    if result.utcoffset() != timedelta(0) or result > now:
        raise RetentionError("Invalid receipt time.")
    return result


def validate_receipt(
    run: str,
    record: dict[str, Any],
    repositories: dict[str, Any],
    marker: str,
    now: datetime,
) -> None:
    if (
        HEX32.fullmatch(run) is None
        or set(record)
        != {
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
        or type(record["schema"]) is not int
        or record["schema"] != 2
        or record["purpose"] != "production"
        or record["database"] != "brickvault_appraisal_prod"
        or record["ownership_marker"] != marker
        or record["run_id"] != run
        or record["repositories"] != repositories
        or record["revisions_at_backup"] not in [[], ["0016_hunt_cached_runs"]]
        or not isinstance(record["artifacts"], dict)
        or set(record["artifacts"]) != ARTIFACTS
    ):
        raise RetentionError("Invalid production receipt.")
    stamp(record["verified_at_utc"], now)
    seen = set()
    for row in record["artifacts"].values():
        if (
            not isinstance(row, dict)
            or set(row) != {"bytes", "sha256", "snapshots"}
            or type(row["bytes"]) is not int
            or row["bytes"] <= 0
            or not isinstance(row["sha256"], str)
            or HEX64.fullmatch(row["sha256"]) is None
            or not isinstance(row["snapshots"], dict)
            or set(row["snapshots"]) != DESTINATIONS
        ):
            raise RetentionError("Invalid artifact receipt.")
        for identity in row["snapshots"].values():
            if (
                not isinstance(identity, str)
                or HEX64.fullmatch(identity) is None
                or identity in seen
            ):
                raise RetentionError("Ambiguous snapshot identity.")
            seen.add(identity)


def select_keep(receipts: dict[str, dict[str, Any]], now: datetime) -> set[str]:
    ordered = sorted(
        receipts,
        key=lambda r: (stamp(receipts[r]["verified_at_utc"], now), r),
        reverse=True,
    )
    keep: set[str] = set()
    for period, count in (("day", 30), ("week", 8), ("month", 12)):
        buckets: set[str] = set()
        for run in ordered:
            date = stamp(receipts[run]["verified_at_utc"], now)
            key = (
                date.strftime("%Y-%m-%d")
                if period == "day"
                else date.strftime("%G-%V")
                if period == "week"
                else date.strftime("%Y-%m")
            )
            if key not in buckets:
                if len(buckets) == count:
                    break
                buckets.add(key)
                keep.add(run)
    return keep


def make_plan(
    receipts: dict[str, dict[str, Any]],
    repositories: dict[str, Any],
    marker: str,
    snapshots: dict[str, list[dict[str, Any]]],
    pins: dict[str, Any],
    ledger: dict[str, Any],
    now: datetime,
) -> dict[str, Any]:
    if (
        set(pins) != {"schema", "repositories", "runs", "canaries"}
        or pins["schema"] != 1
        or pins["repositories"] != repositories
        or not isinstance(pins["runs"], dict)
        or len(pins["runs"]) < 2
        or not isinstance(pins["canaries"], dict)
        or set(pins["canaries"]) != DESTINATIONS
        or set(ledger) != {"schema", "status", "deleted", "last_transaction"}
        or ledger["schema"] != 1
        or ledger["status"] != "READY"
        or not isinstance(ledger["deleted"], dict)
        or set(snapshots) != DESTINATIONS
    ):
        raise RetentionError("Pins or retention state are invalid/degraded.")
    if not set(pins["runs"]).issubset(receipts) or not set(ledger["deleted"]).issubset(
        receipts
    ):
        raise RetentionError("Protected receipt history is missing.")
    if set(pins["runs"]) & set(ledger["deleted"]):
        raise RetentionError("Pinned history was selected for deletion.")
    live: dict[str, dict[str, Any]] = {}
    expected: dict[str, dict[str, tuple[str, str]]] = {d: {} for d in DESTINATIONS}
    all_ids: set[str] = set()
    for run, receipt in receipts.items():
        validate_receipt(run, receipt, repositories, marker, now)
        receipt_digest = digest(receipt)
        if run in pins["runs"] and pins["runs"][run] != receipt_digest:
            raise RetentionError("Pinned receipt changed.")
        if run in ledger["deleted"]:
            if ledger["deleted"][run] != receipt_digest:
                raise RetentionError("Deleted receipt changed.")
        else:
            live[run] = receipt
        for artifact, row in receipt["artifacts"].items():
            for destination, identity in row["snapshots"].items():
                if identity in all_ids:
                    raise RetentionError("Snapshot shared across runs.")
                all_ids.add(identity)
                if run in live:
                    expected[destination][identity] = (run, artifact)
    normalized: dict[str, list[dict[str, Any]]] = {}
    for destination in sorted(DESTINATIONS):
        canaries = pins["canaries"][destination]
        if not isinstance(canaries, dict) or not canaries:
            raise RetentionError("Canary pins missing.")
        rows: dict[str, dict[str, Any]] = {}
        for row in snapshots[destination]:
            identity = row.get("id")
            if (
                not isinstance(identity, str)
                or HEX64.fullmatch(identity) is None
                or identity in rows
            ):
                raise RetentionError("Ambiguous repository snapshot list.")
            rows[identity] = row
        if set(rows) != set(expected[destination]) | set(canaries):
            raise RetentionError("Partial or unrecognized backup history.")
        if set(canaries) & all_ids:
            raise RetentionError("Canary overlaps production artifacts.")
        for identity, row_digest in canaries.items():
            if digest(rows[identity]) != row_digest:
                raise RetentionError("Pinned canary identity changed.")
        for identity, (run, artifact) in expected[destination].items():
            row = rows[identity]
            if row.get("paths") not in [
                [f"/{run}/{artifact}"],
                [f"{run}/{artifact}"],
            ] or row.get("tags") != [run]:
                raise RetentionError(
                    "Snapshot path/tag does not match its complete run."
                )
        normalized[destination] = [rows[key] for key in sorted(rows)]
    keep = select_keep(live, now) | set(pins["runs"])
    plan = {
        "schema": 1,
        "policy": [30, 8, 12],
        "date_utc": now.date().isoformat(),
        "keep": sorted(keep),
        "delete": sorted(set(live) - keep),
        "repositories": repositories,
        "receipts": {r: digest(v) for r, v in sorted(receipts.items())},
        "snapshots": normalized,
        "pins_digest": digest(pins),
        "ledger_digest": digest(ledger),
    }
    plan["digest"] = digest(plan)
    return plan


def apply_plan(
    expected_digest: str,
    gather: Any,
    forget: Any,
    readback: Any,
    check: Any,
    save: Any,
    notify: Any,
) -> str:
    """Adapters permit real disposable restic tests without production credentials."""
    plan, receipts, ledger = gather()
    if plan["digest"] != expected_digest:
        raise RetentionError("Retention plan changed; no deletion performed.")
    if not plan["delete"]:
        save(ledger, {"status": "NOOP", "plan": plan})
        return "NOOP"
    # Verify the exact six bytes streams before the first irreversible action.
    for run in plan["delete"]:
        readback(run, receipts[run])
    refreshed, _, _ = gather()
    if refreshed != plan:
        raise RetentionError("History changed during readback; no deletion performed.")
    transaction: dict[str, Any] = {"status": "DEGRADED", "plan": plan, "completed": []}
    ledger = dict(ledger, status="DEGRADED", last_transaction=plan["digest"])
    save(
        ledger, transaction
    )  # Durable fail-closed intent before either repository mutates.
    remaining = {d: {row["id"] for row in plan["snapshots"][d]} for d in DESTINATIONS}
    try:
        for run in plan["delete"]:
            for destination in sorted(DESTINATIONS):
                identities = sorted(
                    receipts[run]["artifacts"][a]["snapshots"][destination]
                    for a in ARTIFACTS
                )
                forget(destination, identities)
                remaining[destination].difference_update(identities)
                check(destination, remaining[destination])
                transaction["completed"].append(
                    {"run": run, "destination": destination, "snapshots": identities}
                )
                save(ledger, transaction)
            ledger["deleted"][run] = digest(receipts[run])
        transaction["status"] = "COMPLETE"
        save(dict(ledger, status="READY"), transaction)
        return "COMPLETE"
    except BaseException:  # noqa: BLE001 - fail closed even on process interruption.
        # Even a killed process leaves DEGRADED on disk; only operator review can clear it.
        try:
            notify()
        except Exception:  # noqa: BLE001, S110 - preserve failure and protected transaction.
            pass
        raise RetentionError("Retention DEGRADED; operator repair required.") from None


def run(command: str, requested_digest: str | None) -> str:
    import fcntl

    from brickvault_api import production_admin as admin
    from brickvault_api import production_backup as backup

    if os.geteuid() != 0:
        raise RetentionError("Root is required.")
    os.umask(0o077)
    descriptor = os.open(LOCK, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != 0
            or info.st_nlink != 1
            or stat.S_IMODE(info.st_mode) != 0o600
        ):
            raise RetentionError("Unsafe backup/retention lock.")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config = backup._preflight()
        protected.directory(STATE)
        destinations = {d.name: d for d in backup.DESTINATIONS}

        def gather() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
            backup._verify_destination_identity()
            identities, _ = backup._validated_identity(
                admin._parse_json(
                    admin._protected_file(backup.BACKUP_DIR / "repositories.json")
                )
            )
            repositories = {
                d.name: {"uri": d.repository, "id": identities[d.name]}
                for d in backup.DESTINATIONS
            }
            receipts = {}
            for path in sorted(backup.RECEIPT_DIR.iterdir()):
                if path.suffix != ".json" or HEX32.fullmatch(path.stem) is None:
                    raise RetentionError("Unexpected receipt directory entry.")
                receipts[path.stem] = protected.protected_json(path)
            pins = protected.protected_json(PINS)
            ledger = read_state(STATE / "ledger.json")
            snapshots = {
                d.name: json.loads(
                    backup._restic(d, "snapshots", "--json", capture=True)
                )
                for d in backup.DESTINATIONS
            }
            return (
                make_plan(
                    receipts,
                    repositories,
                    config.marker,
                    snapshots,
                    pins,
                    ledger,
                    datetime.now(UTC),
                ),
                receipts,
                ledger,
            )

        def save(ledger: dict[str, Any], transaction: dict[str, Any]) -> None:
            # Write DEGRADED first; a later failed transaction write must still prohibit deletion.
            if ledger["status"] == "DEGRADED":
                protected.write_state(STATE / "ledger.json", ledger)
            protected.write_state(
                STATE / (transaction["plan"]["digest"] + ".json"), transaction
            )
            if ledger["status"] == "READY":
                protected.write_state(STATE / "ledger.json", ledger)

        def readback(run_id: str, receipt: dict[str, Any]) -> None:
            for artifact, row in receipt["artifacts"].items():
                for d in backup.DESTINATIONS:
                    backup._readback(
                        d,
                        row["snapshots"][d.name],
                        artifact,
                        row["bytes"],
                        row["sha256"],
                        run_id,
                    )

        def forget(destination: str, identities: list[str]) -> None:
            backup._restic(destinations[destination], "forget", *identities)

        def check(destination: str, expected: set[str]) -> None:
            d = destinations[destination]
            rows = json.loads(backup._restic(d, "snapshots", "--json", capture=True))
            if {row["id"] for row in rows} != expected:
                raise RetentionError("Post-deletion repository state differs.")
            backup._restic(d, "check")

        plan, _, _ = gather()
        if command == "plan":
            # Counts and a digest disclose no raw run or snapshot identifiers.
            return f"RETENTION_PLAN keep={len(plan['keep'])} delete={len(plan['delete'])} digest={plan['digest']}"
        if command == "scheduled":
            requested_digest = plan["digest"]
        if requested_digest is None or HEX64.fullmatch(requested_digest) is None:
            raise RetentionError("An exact current plan digest is required.")
        if command == "prune":
            current, _, ledger = gather()
            if (
                current["digest"] != requested_digest
                or current["delete"]
                or not ledger["last_transaction"]
            ):
                raise RetentionError(
                    "Prune requires an unchanged safe plan after completed retention."
                )
            previous = read_state(STATE / (ledger["last_transaction"] + ".json"))
            if previous["status"] != "COMPLETE":
                raise RetentionError(
                    "Prune requires completed deletion/readback/checks."
                )
            transaction = {"status": "PRUNE_PENDING", "plan": current}
            save(dict(ledger, status="DEGRADED"), transaction)
            try:
                for destination in sorted(DESTINATIONS):
                    backup._restic(destinations[destination], "prune")
                    check(
                        destination,
                        {row["id"] for row in current["snapshots"][destination]},
                    )
                transaction["status"] = "PRUNE_COMPLETE"
                save(ledger, transaction)
                return "RETENTION_PRUNE_COMPLETE"
            except Exception:  # noqa: BLE001 - never retry destructive maintenance.
                protected.send("RETENTION")
                raise RetentionError(
                    "Prune DEGRADED; operator review required."
                ) from None
        return "RETENTION_" + apply_plan(
            requested_digest,
            gather,
            forget,
            readback,
            check,
            save,
            lambda: protected.send("RETENTION"),
        )
    finally:
        os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "apply", "scheduled", "prune"])
    parser.add_argument("--digest")
    args = parser.parse_args()
    try:
        print(run(args.command, args.digest))
        return 0
    except Exception:  # noqa: BLE001 - live identifiers/credentials remain private.
        print("RETENTION_REFUSED; inspect protected state", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
