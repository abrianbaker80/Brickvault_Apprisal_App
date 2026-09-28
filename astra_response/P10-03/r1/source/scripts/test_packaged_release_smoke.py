"""Focused refusal checks for selecting and identifying a packaged API."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from packaged_release_smoke import (
    SmokeError,
    select_package,
    verify_child_identity,
)


class PackageSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.scratch = self.root / ".local" / "package-check" / ("a" * 32)
        self.scratch.mkdir(parents=True)
        self.receipt = self.scratch / "result.json"
        self.receipt.write_text(
            json.dumps(
                {
                    "wheel": "services/api/dist/brickvault_api-0.0.0-py3-none-any.whl",
                    "sdist": "services/api/dist/brickvault_api-0.0.0.tar.gz",
                    "installed_wheel_verified": True,
                }
            ),
            encoding="utf-8",
        )
        python = (
            self.scratch
            / "venv"
            / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        )
        python.parent.mkdir(parents=True)
        python.touch()
        wheel = self.root / "services/api/dist/brickvault_api-0.0.0-py3-none-any.whl"
        wheel.parent.mkdir(parents=True)
        wheel.touch()

    def test_accepts_exact_verified_package_receipt(self) -> None:
        scratch, python = select_package(self.root, self.receipt)
        self.assertEqual(scratch, self.scratch)
        self.assertTrue(python.is_file())

    def test_accepts_native_windows_receipt_separators(self) -> None:
        result = json.loads(self.receipt.read_text(encoding="utf-8"))
        result["wheel"] = result["wheel"].replace("/", "\\")
        result["sdist"] = result["sdist"].replace("/", "\\")
        self.receipt.write_text(json.dumps(result), encoding="utf-8")
        self.assertEqual(select_package(self.root, self.receipt)[0], self.scratch)

    def test_rejects_unverified_or_external_receipt(self) -> None:
        self.receipt.write_text('{"installed_wheel_verified": false}', encoding="utf-8")
        with self.assertRaises(SmokeError):
            select_package(self.root, self.receipt)
        external = self.root / "other" / "result.json"
        external.parent.mkdir()
        external.write_text("{}", encoding="utf-8")
        with self.assertRaises(SmokeError):
            select_package(self.root, external)

    def test_rejects_hard_linked_receipt(self) -> None:
        copy = self.scratch / "other.json"
        os.link(self.receipt, copy)
        with self.assertRaises(SmokeError):
            select_package(self.root, self.receipt)

    def test_rejects_source_import_identity(self) -> None:
        venv = self.scratch / "venv"
        installed = venv / "Lib" / "site-packages" / "brickvault_api" / "__init__.py"
        installed.parent.mkdir(parents=True)
        installed.touch()
        ready = {
            "pid": 1234,
            "port": 18001,
            "prefix": str(venv),
            "package_file": str(installed),
            "isolated": True,
        }
        self.assertEqual(verify_child_identity(ready, self.scratch, 1234), 18001)
        source = self.root / "services/api/src/brickvault_api/__init__.py"
        source.parent.mkdir(parents=True)
        source.touch()
        ready["package_file"] = str(source)
        with self.assertRaises(SmokeError):
            verify_child_identity(ready, self.scratch, 1234)


if __name__ == "__main__":
    unittest.main()
