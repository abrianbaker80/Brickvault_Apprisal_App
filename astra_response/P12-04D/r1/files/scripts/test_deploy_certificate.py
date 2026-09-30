"""Linux root-only certificate deployment tests; all service commands are mocked."""

import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import deploy_certificate as deploy


@unittest.skipUnless(
    os.name == "posix" and getattr(os, "geteuid", lambda: -1)() == 0,
    "Run in an isolated root-owned Linux temporary directory",
)
class CertificateDeploymentTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(dir="/root")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.destination = self.root / "tls"
        self.files = {
            "fullchain.pem": b"trusted certificate",
            "privkey.pem": b"matching key",
        }
        for name, value in (("DESTINATION", self.destination),):
            patcher = patch.object(deploy, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        environment_patch = patch.object(
            deploy, "caddy_environment", return_value={"PATH": "/usr/bin:/bin"}
        )
        environment_patch.start()
        self.addCleanup(environment_patch.stop)

    def install(self, *, active: bool = False) -> bool:
        with patch(
            "deploy_certificate.subprocess.run",
            return_value=SimpleNamespace(returncode=0 if active else 3),
        ):
            return deploy.install(self.files, 0)

    def test_stopped_service_pair_permissions_and_idempotence(self) -> None:
        with patch.object(deploy, "run") as command:
            self.assertFalse(self.install())
            first = os.readlink(self.destination / "current")
            self.assertFalse(self.install())
            self.assertEqual(first, os.readlink(self.destination / "current"))
            for name, expected in self.files.items():
                path = self.destination / "current" / name
                self.assertEqual(path.read_bytes(), expected)
                self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            self.assertTrue(
                all("reload" not in call.args[0] for call in command.call_args_list)
            )

    def test_validation_failure_removes_first_pointer(self) -> None:
        with (
            patch.object(deploy, "run", side_effect=deploy.CertificateError()),
            self.assertRaises(deploy.CertificateError),
        ):
            self.install()
        self.assertFalse((self.destination / "current").is_symlink())

    def test_reload_failure_restores_previous_pair_and_retains_generations(
        self,
    ) -> None:
        with patch.object(deploy, "run"):
            self.install()
        previous = os.readlink(self.destination / "current")
        self.files = {
            "fullchain.pem": b"renewed certificate",
            "privkey.pem": b"renewed key",
        }
        with (
            patch.object(deploy, "run", side_effect=[b"", deploy.CertificateError()]),
            self.assertRaises(deploy.CertificateError),
        ):
            self.install(active=True)
        self.assertEqual(previous, os.readlink(self.destination / "current"))
        self.assertEqual(len(list(self.destination.glob("cert-*"))), 2)

    def test_symlink_destination_and_changed_generation_refused(self) -> None:
        other = self.root / "other"
        other.mkdir()
        self.destination.symlink_to(other, target_is_directory=True)
        with self.assertRaises(deploy.CertificateError):
            self.install()
        self.destination.unlink()
        with patch.object(deploy, "run"):
            self.install()
        (self.destination / "current" / "privkey.pem").write_bytes(b"replaced key")
        with self.assertRaises(deploy.CertificateError):
            self.install()

    def test_other_lineage_and_unsafe_private_permissions_refused(self) -> None:
        with self.assertRaises(deploy.CertificateError):
            deploy.certificate_inputs(self.root)
        private = self.root / "key"
        private.write_bytes(b"private")
        private.chmod(0o644)
        with self.assertRaises(deploy.CertificateError):
            deploy.read_protected(private, private=True)


if __name__ == "__main__":
    unittest.main()
