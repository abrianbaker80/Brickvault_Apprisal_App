"""Offline alert transport tests; no real configuration or network is used."""

import smtplib
import ssl
import sys
import unittest
from unittest.mock import MagicMock, patch

import operational_alert as alert


class AlertTests(unittest.TestCase):
    def test_duplicate_configuration_fields_refused(self) -> None:
        with self.assertRaises(alert.AlertError):
            alert.unique_object([("status", "READY"), ("status", "DEGRADED")])

    def setUp(self) -> None:
        self.config = {
            "schema": 1,
            "purpose": "brickvault-operational-alerts",
            "transport": "smtp-ssl",
            "host": "smtp.gmail.com",
            "port": 465,
            "username": "fixture@gmail.com",
            "sender": "fixture@gmail.com",
            "recipient": "fixture@gmail.com",
            "password": "a" * 16,
        }

    def test_tls_bounded_timeout_and_generic_body(self) -> None:
        with patch.object(smtplib, "SMTP_SSL") as smtp:
            smtp.return_value.send_message.return_value = {}
            alert.deliver(self.config, "TEST")
            self.assertEqual(smtp.call_args.kwargs["timeout"], 20)
            context = smtp.call_args.kwargs["context"]
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(context.check_hostname)
            message = smtp.return_value.send_message.call_args.args[0]
            self.assertNotIn(self.config["password"], message.as_string())
            self.assertNotIn(self.config["recipient"], message.get_content())
            smtp.return_value.close.assert_called_once()

    def test_unknown_category_and_header_injection_refused_before_network(self) -> None:
        with patch.object(smtplib, "SMTP_SSL") as smtp:
            with self.assertRaises(alert.AlertError):
                alert.deliver(self.config, "private-log-content")
            self.config["recipient"] = "fixture@gmail.com\nBcc: other@example.invalid"
            with self.assertRaises(alert.AlertError):
                alert.deliver(self.config, "TEST")
            smtp.assert_not_called()

    def test_authentication_and_recipient_failure(self) -> None:
        with patch.object(smtplib, "SMTP_SSL") as smtp:
            smtp.return_value.login.side_effect = smtplib.SMTPAuthenticationError(
                535, b"private"
            )
            with self.assertRaises(smtplib.SMTPAuthenticationError):
                alert.deliver(self.config, "TEST")
            smtp.return_value.send_message.assert_not_called()
            smtp.return_value.close.assert_called_once()
        with patch.object(smtplib, "SMTP_SSL") as smtp:
            smtp.return_value.send_message.return_value = {
                "fixture@gmail.com": (550, b"no")
            }
            with self.assertRaises(alert.AlertError):
                alert.deliver(self.config, "TEST")

    def test_persistent_dedup_failure_backoff_and_clock_rollback(self) -> None:
        self.assertTrue(alert.due({}, 1000))
        self.assertFalse(alert.due({"attempt": 900, "status": "ACCEPTED"}, 1000))
        self.assertFalse(alert.due({"attempt": 900, "status": "PENDING"}, 1000))
        self.assertTrue(alert.due({"attempt": 300, "status": "FAILED"}, 1000))
        with self.assertRaises(alert.AlertError):
            alert.due({"attempt": 1100, "status": "ACCEPTED"}, 1000)

    def test_cli_redacts_exceptions(self) -> None:
        output = MagicMock()
        with (
            patch.object(sys, "argv", ["alert", "TEST"]),
            patch.object(alert, "send", side_effect=RuntimeError("private-sentinel")),
            patch.object(sys, "stderr", output),
        ):
            self.assertEqual(alert.main(), 1)
        self.assertNotIn("private-sentinel", str(output.mock_calls))


if __name__ == "__main__":
    unittest.main()
