"""Focused release-bundle integrity and refusal checks."""

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_manifest  # noqa: E402


class ReleaseManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / ".local").mkdir()
        api = self.root / "services" / "api" / "dist"
        api.mkdir(parents=True)
        (api / release_manifest.WHEEL).write_bytes(b"wheel-bytes")
        (api / release_manifest.SDIST).write_bytes(b"sdist-bytes")
        web = self.root / "apps" / "web" / "dist"
        (web / "assets").mkdir(parents=True)
        (web / "index.html").write_bytes(
            b'<script src="/assets/main-01234567.js"></script>'
        )
        (web / "assets" / "main-01234567.js").write_bytes(b"const ready = true;")
        self.web = web
        self.release_id = "p12-04a-r1"
        self.source_id = "a" * 64

    def _create(self) -> tuple[Path, str]:
        def export(_root: Path, destination: Path) -> None:
            destination.write_text("alembic==1.19.2 --hash=sha256:" + "a" * 64 + "\n")

        with (
            patch.object(release_manifest, "_verify_frontend"),
            patch.object(release_manifest, "_source_commit", return_value="b" * 40),
            patch.object(release_manifest, "_source_id", return_value=self.source_id),
            patch.object(release_manifest, "_verify_wheel_source"),
            patch.object(release_manifest, "_export_requirements", side_effect=export),
            patch(
                "release_manifest.subprocess.run",
                return_value=SimpleNamespace(returncode=0),
            ),
        ):
            return release_manifest.create(self.root, self.release_id, self.source_id)

    def test_manifest_binds_all_artifacts_and_rejects_changed_bytes(self) -> None:
        bundle, digest = self._create()
        release_manifest.verify(bundle, digest, self.release_id, self.source_id)
        manifest = json.loads((bundle / "manifest.json").read_text())
        self.assertEqual(
            {item["path"] for item in manifest["files"]},
            {
                "api/" + release_manifest.WHEEL,
                "api/" + release_manifest.SDIST,
                "api/requirements.txt",
                "web/index.html",
                "web/assets/main-01234567.js",
            },
        )
        (bundle / "api" / "requirements.txt").write_text("changed\n")
        with self.assertRaises(release_manifest.ReleaseError):
            release_manifest.verify(bundle, digest, self.release_id, self.source_id)

    def test_manifest_requires_external_digest_and_exact_identity(self) -> None:
        bundle, digest = self._create()
        with self.assertRaises(release_manifest.ReleaseError):
            release_manifest.verify(bundle, "0" * 64, self.release_id, self.source_id)
        with self.assertRaises(release_manifest.ReleaseError):
            release_manifest.verify(bundle, digest, self.release_id, "c" * 64)
        (bundle / "extra.txt").write_text("unexpected")
        with self.assertRaises(release_manifest.ReleaseError):
            release_manifest.verify(bundle, digest, self.release_id, self.source_id)

    def test_unexpected_frontend_file_is_refused_before_staging(self) -> None:
        (self.web / "private.json").write_text("private")
        with self.assertRaises(release_manifest.ReleaseError):
            self._create()
        self.assertFalse((self.root / ".local" / "releases").exists())

    def test_source_digest_ignores_protected_bytes_and_rejects_unreviewed_paths(
        self,
    ) -> None:
        scripts = self.root / "scripts"
        scripts.mkdir()
        included = scripts / "release_manifest.py"
        included.write_bytes(b"reviewed source")
        protected = self.root / "AGENTS.md"
        protected.write_bytes(b"original protected bytes")
        plan = self.root / "docs" / "plans" / "094-production-foundation.md"
        plan.parent.mkdir(parents=True)
        plan.write_bytes(b"status pending")
        state = SimpleNamespace(
            returncode=0,
            stdout=(
                b" M AGENTS.md\0?? docs/plans/094-production-foundation.md\0"
                b"?? scripts/release_manifest.py\0"
            ),
        )
        with (
            patch.object(release_manifest, "_source_commit", return_value="b" * 40),
            patch("release_manifest.subprocess.run", return_value=state),
        ):
            first = release_manifest._source_id(
                self.root, ("scripts/release_manifest.py",)
            )
            protected.write_bytes(b"changed protected bytes")
            plan.write_bytes(b"manifest recorded")
            self.assertEqual(
                first,
                release_manifest._source_id(
                    self.root, ("scripts/release_manifest.py",)
                ),
            )
            included.write_bytes(b"changed reviewed source")
            self.assertNotEqual(
                first,
                release_manifest._source_id(
                    self.root, ("scripts/release_manifest.py",)
                ),
            )
        state.stdout = b"?? unexpected.txt\0"
        with (
            patch.object(release_manifest, "_source_commit", return_value="b" * 40),
            patch("release_manifest.subprocess.run", return_value=state),
            self.assertRaises(release_manifest.ReleaseError),
        ):
            release_manifest._source_id(self.root, ("scripts/release_manifest.py",))
        state.stdout = b"M  scripts/release_manifest.py\0"
        with (
            patch.object(release_manifest, "_source_commit", return_value="b" * 40),
            patch("release_manifest.subprocess.run", return_value=state),
            self.assertRaises(release_manifest.ReleaseError),
        ):
            release_manifest._source_id(self.root, ("scripts/release_manifest.py",))

    def test_wheel_must_contain_exact_current_package_source(self) -> None:
        package = self.root / "services" / "api" / "src" / "brickvault_api"
        package.mkdir(parents=True)
        (package / "__init__.py").write_bytes(b"package")
        admin = package / "production_admin.py"
        admin.write_bytes(b"reviewed admin")
        wheel = self.root / "services" / "api" / "dist" / release_manifest.WHEEL
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr("brickvault_api/__init__.py", b"package")
            archive.writestr("brickvault_api/production_admin.py", b"reviewed admin")
        release_manifest._verify_wheel_source(self.root, wheel)
        admin.write_bytes(b"new admin change")
        with self.assertRaises(release_manifest.ReleaseError):
            release_manifest._verify_wheel_source(self.root, wheel)


if __name__ == "__main__":
    unittest.main()
