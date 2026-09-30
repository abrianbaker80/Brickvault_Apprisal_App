"""Deterministic health and official-version parser regressions."""

import gzip
import io
import time
import unittest
import urllib.request
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import operational_alert as protected
import production_health as health
import python_maintenance as maintenance


class HealthTests(unittest.TestCase):
    def test_loopback_and_unexpected_listeners(self) -> None:
        good = "LISTEN 0 100 127.0.0.1:18080 0.0.0.0:*\nLISTEN 0 100 127.0.0.1:5432 0.0.0.0:*\nLISTEN 0 100 *:443 *:*"
        self.assertTrue(health.listeners_valid(good))
        self.assertTrue(
            health.listeners_valid(good + "\nLISTEN 0 100 127.0.0.53%lo:53 0.0.0.0:*")
        )
        self.assertFalse(
            health.listeners_valid(good.replace("127.0.0.1:5432", "0.0.0.0:5432"))
        )
        self.assertFalse(health.listeners_valid(good + "\nLISTEN 0 100 *:80 *:*"))
        self.assertFalse(health.listeners_valid(good + "\nLISTEN 0 100 *:2019 *:*"))
        self.assertFalse(
            health.listeners_valid(good + "\nLISTEN 0 100 127.0.0.1:2019 0.0.0.0:*")
        )
        self.assertFalse(
            health.listeners_valid(good + "\nLISTEN 0 100 192.0.2.1%eth0:53 0.0.0.0:*")
        )

    def test_stale_backup_and_space_thresholds(self) -> None:
        now = datetime(2026, 9, 30, tzinfo=UTC)
        self.assertTrue(
            health.recent_backup(
                [{"verified_at_utc": (now - timedelta(hours=24)).isoformat()}], now
            )
        )
        self.assertFalse(
            health.recent_backup(
                [{"verified_at_utc": (now - timedelta(hours=37)).isoformat()}], now
            )
        )
        self.assertFalse(health.recent_backup([], now))
        self.assertFalse(health.disk_ok(1000, 99, 1))
        self.assertFalse(health.disk_ok(1000, 200, 201))
        self.assertTrue(health.disk_ok(1000, 200, 100))

    def test_certificate_exact_san_and_expiry(self) -> None:
        certificate = {
            "subjectAltName": (("DNS", health.HOST),),
            "notAfter": "Oct 30 00:00:00 2026 GMT",
        }
        now = datetime(2026, 9, 30, tzinfo=UTC).timestamp()
        self.assertTrue(health.certificate_ok(certificate, now))
        self.assertFalse(health.certificate_ok(certificate, now + 20 * 86400))
        certificate["subjectAltName"] = (("DNS", "wrong.invalid"),)
        self.assertFalse(health.certificate_ok(certificate, now))


class PythonTests(unittest.TestCase):
    def test_official_http_identity_gzip_and_response_bounds(self) -> None:
        html = b'Stable Releases <a href="/downloads/release/python-31315/">release</a>'

        class Response(io.BytesIO):
            url = maintenance.SOURCE

            def __init__(self, raw: bytes, encoding: str) -> None:
                super().__init__(raw)
                self.headers = {"Content-Encoding": encoding}

        for encoding, raw in [("identity", html), ("gzip", gzip.compress(html))]:
            with patch.object(
                urllib.request,
                "urlopen",
                return_value=Response(raw, encoding),
            ):
                self.assertEqual(maintenance.lookup(), (3, 13, 15))
        for encoding, raw in [
            ("br", html),
            ("identity", b"x" * (maintenance.MAX_RESPONSE + 1)),
            ("gzip", gzip.compress(b"x" * (maintenance.MAX_RESPONSE + 1))),
            ("gzip", b"invalid gzip"),
        ]:
            with (
                patch.object(
                    urllib.request,
                    "urlopen",
                    return_value=Response(raw, encoding),
                ),
                self.assertRaises((OSError, ValueError)),
            ):
                maintenance.lookup()

    def test_only_official_final_313_links_and_numeric_order(self) -> None:
        html = 'Stable Releases <a href="/downloads/release/python-3139/">old</a><a href="/downloads/release/python-31315/">new</a><a href="/downloads/release/python-31499/">other</a><a href="/downloads/release/python-31316rc1/">pre</a><a href="https://third-party.invalid/downloads/release/python-31399/">untrusted</a>'
        self.assertEqual(maintenance.latest_from_html(html), (3, 13, 15))
        with self.assertRaises(ValueError):
            maintenance.latest_from_html("unexpected page")

    def test_repeated_lookup_failure_and_newer_version(self) -> None:
        with (
            patch.object(protected, "directory"),
            patch.object(protected, "write_state") as saved,
            patch.object(
                maintenance, "lookup", side_effect=OSError("private")
            ) as lookup,
            patch.object(time, "sleep"),
        ):
            self.assertEqual(maintenance.main(), 1)
            self.assertEqual(lookup.call_count, 3)
            self.assertEqual(saved.call_args.args[1]["status"], "LOOKUP_FAILED")
        with (
            patch.object(protected, "directory"),
            patch.object(protected, "write_state") as saved,
            patch.object(maintenance, "lookup", return_value=(3, 13, 999)),
        ):
            self.assertEqual(maintenance.main(), 1)
            self.assertEqual(saved.call_args.args[1]["status"], "UPDATE_AVAILABLE")


if __name__ == "__main__":
    unittest.main()
