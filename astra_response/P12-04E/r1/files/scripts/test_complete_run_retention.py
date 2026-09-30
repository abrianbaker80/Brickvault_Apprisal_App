"""Synthetic policy tests plus real forget in disposable LOCAL restic repositories."""

import copy
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

import complete_run_retention as retention
import operational_alert as protected

NOW = datetime(2026, 9, 30, tzinfo=UTC)


def receipt(
    number: int, when: datetime, repositories: dict[str, Any]
) -> dict[str, Any]:
    run = f"{number:032x}"
    return {
        "schema": 2,
        "purpose": "production",
        "database": "brickvault_appraisal_prod",
        "ownership_marker": "test-marker",
        "run_id": run,
        "revisions_at_backup": [],
        "verified_at_utc": when.isoformat(),
        "repositories": repositories,
        "artifacts": {
            a: {
                "bytes": 4,
                "sha256": hashlib.sha256(b"test").hexdigest(),
                "snapshots": {
                    d: hashlib.sha256(f"{run}/{a}/{d}".encode()).hexdigest()
                    for d in retention.DESTINATIONS
                },
            }
            for a in retention.ARTIFACTS
        },
    }


class PolicyTests(unittest.TestCase):
    def test_daily_weekly_monthly_union_and_ties(self) -> None:
        receipts = {
            f"{i:032x}": receipt(i, NOW - timedelta(days=i), {}) for i in range(1, 451)
        }
        kept = retention.select_keep(receipts, NOW)
        dates = [datetime.fromisoformat(receipts[r]["verified_at_utc"]) for r in kept]
        self.assertTrue(all(f"{i:032x}" in kept for i in range(1, 31)))
        self.assertGreaterEqual(len({d.strftime("%G-%V") for d in dates}), 8)
        self.assertEqual(len({d.strftime("%Y-%m") for d in dates}), 12)
        self.assertLess(len(kept), 30 + 8 + 12)
        newer = receipt(999, NOW - timedelta(days=1), {})
        receipts[newer["run_id"]] = newer
        self.assertIn(newer["run_id"], retention.select_keep(receipts, NOW))
        self.assertNotIn(f"{1:032x}", retention.select_keep(receipts, NOW))

    def test_partial_receipt_and_ambiguous_snapshot_refusal(self) -> None:
        value = receipt(1, NOW, {})
        value["artifacts"].pop("globals.sql")
        with self.assertRaises(retention.RetentionError):
            retention.validate_receipt(value["run_id"], value, {}, "test-marker", NOW)
        value = receipt(1, NOW, {})
        value["artifacts"]["globals.sql"]["snapshots"] = value["artifacts"][
            "database.dump"
        ]["snapshots"]
        with self.assertRaises(retention.RetentionError):
            retention.validate_receipt(value["run_id"], value, {}, "test-marker", NOW)


@unittest.skipUnless(
    os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() == 0,
    "Protected-state Linux root filesystem required",
)
class ProtectedStateTests(unittest.TestCase):
    def test_large_retention_record_roundtrip_and_bounded_read(self) -> None:
        with tempfile.TemporaryDirectory(dir="/root") as directory:
            path = Path(directory) / "transaction.json"
            value = {"snapshot_evidence": "x" * 100_000}
            protected.write_state(path, value)
            with self.assertRaises(protected.AlertError):
                protected.protected_json(path)
            self.assertEqual(retention.read_state(path), value)
            with (
                patch.object(retention, "MAX_STATE_BYTES", 100_000),
                self.assertRaises(protected.AlertError),
            ):
                retention.read_state(path)
            path.chmod(0o644)
            with self.assertRaises(protected.AlertError):
                retention.read_state(path)


@unittest.skipUnless(
    os.name == "posix" and shutil.which("restic"), "Disposable Linux restic required"
)
class DisposableResticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        password = self.root / "password"
        password.write_text("synthetic-disposable-password")
        password.chmod(0o600)
        self.environment = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": str(self.root),
            "RESTIC_PASSWORD_FILE": str(password),
            "RESTIC_CACHE_DIR": str(self.root / "cache"),
        }
        self.repositories: dict[str, Any] = {}
        for d in sorted(retention.DESTINATIONS):
            self.command(d, "init")
            self.repositories[d] = {
                "uri": str(self.root / d),
                "id": json.loads(self.command(d, "cat", "config"))["id"],
            }
        self.receipts = {}
        for n in range(1, 5):
            record = receipt(n, NOW - timedelta(hours=6 - n), self.repositories)
            run = record["run_id"]
            self.receipts[run] = record
            for artifact in sorted(retention.ARTIFACTS):
                for d in sorted(retention.DESTINATIONS):
                    self.command(
                        d,
                        "backup",
                        "--stdin",
                        "--stdin-filename",
                        f"{run}/{artifact}",
                        "--tag",
                        run,
                        input_data=b"test",
                    )
                    record["artifacts"][artifact]["snapshots"][d] = json.loads(
                        self.command(d, "snapshots", "--json", "--tag", run)
                    )[-1]["id"]
                    # Query by exact path because snapshot listing order is not an identity.
                    rows = json.loads(
                        self.command(d, "snapshots", "--json", "--tag", run)
                    )
                    record["artifacts"][artifact]["snapshots"][d] = next(
                        x["id"] for x in rows if x["paths"] == [f"/{run}/{artifact}"]
                    )
        canaries = {}
        for d in sorted(retention.DESTINATIONS):
            self.command(
                d,
                "backup",
                "--stdin",
                "--stdin-filename",
                "canary",
                "--tag",
                "canary",
                input_data=b"canary",
            )
            row = json.loads(self.command(d, "snapshots", "--json", "--tag", "canary"))[
                0
            ]
            canaries[d] = {row["id"]: retention.digest(row)}
        self.pins: dict[str, Any] = {
            "schema": 1,
            "repositories": self.repositories,
            "runs": {
                r: retention.digest(self.receipts[r])
                for r in [f"{1:032x}", f"{2:032x}"]
            },
            "canaries": canaries,
        }
        self.ledger = {
            "schema": 1,
            "status": "READY",
            "deleted": {},
            "last_transaction": None,
        }
        self.calls: list[tuple[str, list[str]]] = []
        self.alerts = 0

    def command(self, d: str, *args: str, input_data: bytes | None = None) -> bytes:
        path = self.root / d
        assert path.parent == self.root and d in retention.DESTINATIONS
        r = subprocess.run(
            ["restic", "-r", str(path), *args],
            input=input_data,
            capture_output=True,
            env=self.environment,
            timeout=30,
            check=False,
        )
        if r.returncode:
            raise RuntimeError("Disposable restic command failed")
        return r.stdout

    def gather(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        snapshots = {
            d: json.loads(self.command(d, "snapshots", "--json"))
            for d in retention.DESTINATIONS
        }
        return (
            retention.make_plan(
                self.receipts,
                self.repositories,
                "test-marker",
                snapshots,
                self.pins,
                self.ledger,
                NOW,
            ),
            self.receipts,
            copy.deepcopy(self.ledger),
        )

    def forget(self, d: str, ids: list[str]) -> None:
        self.calls.append((d, ids))
        self.command(d, "forget", *ids)

    def readback(self, run: str, record: dict[str, Any]) -> None:
        for a, row in record["artifacts"].items():
            for d in retention.DESTINATIONS:
                self.assertEqual(
                    self.command(d, "dump", row["snapshots"][d], f"/{run}/{a}"), b"test"
                )

    def check(self, d: str, expected: set[str]) -> None:
        rows = json.loads(self.command(d, "snapshots", "--json"))
        self.assertEqual({r["id"] for r in rows}, expected)
        self.command(d, "check")

    def save(self, ledger: dict[str, Any], transaction: dict[str, Any]) -> None:
        self.ledger = copy.deepcopy(ledger)
        (self.root / "ledger.json").write_text(json.dumps(ledger))
        (self.root / "transaction.json").write_text(json.dumps(transaction))

    def notify(self) -> None:
        self.alerts += 1

    def test_real_complete_run_forget_pins_readback_and_noop(self) -> None:
        plan, _, _ = self.gather()
        self.assertEqual(plan["delete"], [f"{3:032x}"])
        result = retention.apply_plan(
            plan["digest"],
            self.gather,
            self.forget,
            self.readback,
            self.check,
            self.save,
            self.notify,
        )
        self.assertEqual(result, "COMPLETE")
        self.assertEqual(len(self.calls), 2)
        self.assertTrue(all(len(ids) == 3 for _, ids in self.calls))
        plan, _, _ = self.gather()
        self.assertEqual(plan["delete"], [])
        self.assertEqual(
            retention.apply_plan(
                plan["digest"],
                self.gather,
                self.forget,
                self.readback,
                self.check,
                self.save,
                self.notify,
            ),
            "NOOP",
        )
        self.assertEqual(len(self.calls), 2)

    def test_changed_history_and_partial_snapshot_refused(self) -> None:
        plan, _, _ = self.gather()
        self.pins["runs"][f"{3:032x}"] = retention.digest(self.receipts[f"{3:032x}"])
        with self.assertRaises(retention.RetentionError):
            retention.apply_plan(
                plan["digest"],
                self.gather,
                self.forget,
                self.readback,
                self.check,
                self.save,
                self.notify,
            )
        self.assertEqual(self.calls, [])
        identity = self.receipts[f"{4:032x}"]["artifacts"]["database.dump"][
            "snapshots"
        ]["drive"]
        self.command("drive", "forget", identity)
        with self.assertRaises(retention.RetentionError):
            self.gather()

    def test_partial_cross_repository_failure_durable_degraded(self) -> None:
        plan, _, _ = self.gather()

        def fail_second(d: str, ids: list[str]) -> None:
            if self.calls:
                raise RuntimeError("disposable second-destination failure")
            self.forget(d, ids)

        with self.assertRaises(retention.RetentionError):
            retention.apply_plan(
                plan["digest"],
                self.gather,
                fail_second,
                self.readback,
                self.check,
                self.save,
                self.notify,
            )
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.alerts, 1)
        self.assertEqual(
            json.loads((self.root / "ledger.json").read_text())["status"], "DEGRADED"
        )
        with self.assertRaises(retention.RetentionError):
            self.gather()

    def test_first_destination_failure_stops_without_deletion(self) -> None:
        plan, _, _ = self.gather()

        def fail(d: str, ids: list[str]) -> None:
            raise RuntimeError("disposable first-destination failure")

        with self.assertRaises(retention.RetentionError):
            retention.apply_plan(
                plan["digest"],
                self.gather,
                fail,
                self.readback,
                self.check,
                self.save,
                self.notify,
            )
        self.assertEqual(self.calls, [])
        self.assertEqual(self.alerts, 1)
        with self.assertRaises(retention.RetentionError):
            self.gather()


if __name__ == "__main__":
    unittest.main()
