import copy
import hashlib
import unittest
from datetime import UTC, datetime, timedelta

import complete_run_retention as r

NOW = datetime(2026, 10, 19, 18, tzinfo=UTC)


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


class PartialHistoryTests(unittest.TestCase):
    def setUp(self):
        self.repos = {
            d: {"uri": "synthetic-" + d, "id": sha(d)} for d in r.DESTINATIONS
        }
        self.rows = {d: [] for d in r.DESTINATIONS}
        self.receipts = {}
        self.pins = {
            "schema": 1,
            "repositories": self.repos,
            "runs": {},
            "canaries": {},
        }
        self.ledger = {
            "schema": 1,
            "status": "READY",
            "deleted": {},
            "last_transaction": "",
        }
        self.required = r.ARTIFACTS | {"image-blobs.tar"}
        for n in [1, 2]:
            run = f"{n:032x}"
            record = {
                "schema": 3,
                "purpose": "production",
                "database": "brickvault_appraisal_prod",
                "ownership_marker": "fixture-marker",
                "run_id": run,
                "revisions_at_backup": ["0017_listing_images"],
                "verified_at_utc": (NOW - timedelta(hours=n)).isoformat(),
                "repositories": self.repos,
                "artifacts": {},
            }
            for artifact in sorted(self.required):
                identities = {}
                for d in sorted(r.DESTINATIONS):
                    row = self.row(run, artifact, d)
                    self.rows[d].append(row)
                    identities[d] = row["id"]
                record["artifacts"][artifact] = {
                    "bytes": 4,
                    "sha256": sha("test"),
                    "snapshots": identities,
                }
            self.receipts[run] = record
            self.pins["runs"][run] = r.digest(record)
        for d in sorted(r.DESTINATIONS):
            row = {"id": sha("canary-" + d), "paths": ["/canary"], "tags": ["canary"]}
            self.rows[d].append(row)
            self.pins["canaries"][d] = {row["id"]: r.digest(row)}
        self.failed = f"{3:032x}"
        snapshots = {d: {} for d in r.DESTINATIONS}
        for d in sorted(r.DESTINATIONS):
            for artifact in sorted(self.required):
                if d == "drive" and artifact == "image-blobs.tar":
                    continue
                row = self.row(self.failed, artifact, d)
                self.rows[d].append(row)
                snapshots[d][row["id"]] = {
                    "artifact": artifact,
                    "metadata_sha256": r.digest(row),
                    "bytes": 4,
                    "sha256": sha("test"),
                }
        self.disposition = {
            "schema": 1,
            "purpose": "failed-production-backup-disposition",
            "database": "brickvault_appraisal_prod",
            "ownership_marker": "fixture-marker",
            "repositories": self.repos,
            "runs": {
                self.failed: {
                    "status": "FAILED_INCOMPLETE",
                    "recorded_at_utc": NOW.isoformat(),
                    "revisions_at_capture": ["0017_listing_images"],
                    "evidence_sha256": sha("evidence"),
                    "snapshots": snapshots,
                }
            },
        }

    def row(self, run, artifact, d):
        return {
            "id": sha(run + artifact + d),
            "paths": [f"/{run}/{artifact}"],
            "tags": [run],
            "hostname": "brickvault-appraisal",
            "username": "root",
            "summary": {"total_bytes_processed": 4},
            "time": (NOW - timedelta(days=1)).isoformat(),
        }

    def plan(self, disposition=None):
        ledger = copy.deepcopy(self.ledger)
        ledger.update(
            schema=2,
            partial_runs=self.disposition if disposition is None else disposition,
        )
        return r.make_plan(
            self.receipts,
            self.repos,
            "fixture-marker",
            self.rows,
            self.pins,
            ledger,
            NOW,
        )

    def test_retains_seven_exact_failed_snapshots_outside_success_eligibility(self):
        original = copy.deepcopy((self.receipts, self.pins, self.ledger, self.rows))
        plan = self.plan()
        self.assertEqual(plan["keep"], sorted(self.receipts))
        self.assertEqual(plan["delete"], [])
        self.assertNotIn(self.failed, plan["receipts"])
        self.assertEqual(
            plan["partial_dispositions_digest"], r.digest(self.disposition)
        )
        self.assertEqual(original, (self.receipts, self.pins, self.ledger, self.rows))
        self.assertEqual(
            sum(len(x) for x in plan["snapshots"].values()),
            sum(len(x) for x in self.rows.values()),
        )

    def test_unknown_history_still_refused(self):
        self.rows["drive"].append(self.row(f"{4:032x}", "database.dump", "drive"))
        with self.assertRaises(r.RetentionError):
            self.plan()

    def test_no_disposition_still_refuses_partial_history(self):
        with self.assertRaises(r.RetentionError):
            r.make_plan(
                self.receipts,
                self.repos,
                "fixture-marker",
                self.rows,
                self.pins,
                self.ledger,
                NOW,
            )

    def test_missing_or_modified_retained_snapshot_refused(self):
        for changed in ["missing", "modified"]:
            with self.subTest(changed=changed):
                original = copy.deepcopy(self.rows)
                if changed == "missing":
                    self.rows["drive"].pop()
                else:
                    self.rows["drive"][-1]["username"] = "other"
                with self.assertRaises(r.RetentionError):
                    self.plan()
                self.rows = original

    def test_wrong_marker_repository_status_and_future_time_refused(self):
        for kind in ["marker", "repository", "status", "future"]:
            with self.subTest(kind=kind):
                value = copy.deepcopy(self.disposition)
                if kind == "marker":
                    value["ownership_marker"] = "wrong"
                elif kind == "repository":
                    value["repositories"]["drive"]["id"] = sha("wrong")
                elif kind == "status":
                    value["runs"][self.failed]["status"] = "SUCCESS"
                else:
                    value["runs"][self.failed]["recorded_at_utc"] = (
                        NOW + timedelta(seconds=1)
                    ).isoformat()
                with self.assertRaises(r.RetentionError):
                    self.plan(value)

    def test_complete_run_cannot_be_disposed_as_partial(self):
        row = self.row(self.failed, "image-blobs.tar", "drive")
        self.rows["drive"].append(row)
        self.disposition["runs"][self.failed]["snapshots"]["drive"][row["id"]] = {
            "artifact": "image-blobs.tar",
            "metadata_sha256": r.digest(row),
            "bytes": 4,
            "sha256": sha("test"),
        }
        with self.assertRaises(r.RetentionError):
            self.plan()

    def test_successful_history_pins_and_receipts_remain_strict(self):
        for kind in ["overlap", "pin", "receipt"]:
            with self.subTest(kind=kind):
                receipts, pins, disposition = copy.deepcopy(
                    (self.receipts, self.pins, self.disposition)
                )
                if kind == "overlap":
                    self.disposition["runs"][next(iter(self.receipts))] = (
                        self.disposition["runs"].pop(self.failed)
                    )
                elif kind == "pin":
                    self.pins["runs"][next(iter(self.receipts))] = sha("wrong")
                else:
                    self.receipts[next(iter(self.receipts))]["artifacts"].pop(
                        "image-blobs.tar"
                    )
                with self.assertRaises(r.RetentionError):
                    self.plan()
                self.receipts, self.pins, self.disposition = receipts, pins, disposition


if __name__ == "__main__":
    unittest.main()
