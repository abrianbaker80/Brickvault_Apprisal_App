"""Stage and verify a reviewed, hash-bound production release bundle.

Run ``pnpm build`` first. This tool copies only its API artifacts and verified web
build, then exports production dependencies from the unchanged uv lockfile. It
does not install packages, contact a server, or start the application.

``source-id`` binds HEAD and the literal build, test, lock and unit inputs below.
It excludes the status documents that will record the resulting release digest,
and the three preserved dirty files. All other dirty paths cause refusal.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WHEEL = "brickvault_api-0.0.0-py3-none-any.whl"
SDIST = "brickvault_api-0.0.0.tar.gz"
UV_VERSION = "0.12.10"
PWA_FILES = {"icon-192.png", "icon-512.png", "manifest.webmanifest", "sw.js"}
BASE_WEB = {"index.html", "assets"}
ASSET_NAME = re.compile(r"[A-Za-z0-9_-]+\.(?:js|css)\Z")
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}\Z")
HEX_40 = re.compile(r"[a-f0-9]{40}\Z")
HEX_64 = re.compile(r"[a-f0-9]{64}\Z")
MAX_WEB_BYTES = 32 * 1024 * 1024
RELEASE_SOURCE_PATHS = (
    "apps/web/package.json",
    "deploy/systemd/brickvault-api.service",
    "deploy/systemd/brickvault-backup.service",
    "deploy/systemd/brickvault-backup.timer",
    "package.json",
    "pnpm-lock.yaml",
    "scripts/database.py",
    "scripts/package_api.py",
    "scripts/production_admin_secret_proof.py",
    "scripts/release_manifest.py",
    "scripts/test_release_manifest.py",
    "services/api/pyproject.toml",
    "services/api/src/brickvault_api/persistence/runtime_grants.py",
    "services/api/src/brickvault_api/production_admin.py",
    "services/api/src/brickvault_api/production_backup.py",
    "services/api/tests/unit/test_production_admin.py",
    "services/api/tests/unit/test_production_backup.py",
    "services/api/uv.lock",
)
DOCUMENTATION_PATHS = {
    "CODEX_WORKFLOW.md",
    "docs/ROADMAP.md",
    "docs/plans/091-production-runtime-and-deployment.md",
    "docs/plans/092-exact-infrastructure-pre-mutation-review.md",
    "docs/plans/093-base-vm-provisioning.md",
    "docs/plans/094-production-foundation.md",
    "docs/plans/095-dual-recovery-foundation.md",
}
PROTECTED_PATHS = {
    "AGENTS.md",
    "services/api/tests/integration/test_catalog_search.py",
    "services/api/tests/unit/test_catalog_parser.py",
}


class ReleaseError(RuntimeError):
    """Public errors contain no file contents or private configuration."""


def _ordinary_file(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError:
        raise ReleaseError("Required release file is unavailable.") from None
    if (
        path.is_symlink()
        or path.is_junction()
        or not stat.S_ISREG(info.st_mode)
        or info.st_nlink != 1
    ):
        raise ReleaseError("Release file is not an ordinary single-link file.")


def _ordinary_directory(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError:
        raise ReleaseError("Required release directory is unavailable.") from None
    if path.is_symlink() or path.is_junction() or not stat.S_ISDIR(info.st_mode):
        raise ReleaseError("Release directory is unsafe.")


def _ordinary_parents(path: Path, boundary: Path) -> None:
    parent = path.parent
    while parent != boundary:
        if boundary not in parent.parents:
            raise ReleaseError("Release path leaves its expected directory.")
        _ordinary_directory(parent)
        parent = parent.parent
    _ordinary_directory(boundary)


def _web_files(directory: Path) -> list[Path]:
    _ordinary_directory(directory)
    names = {entry.name for entry in directory.iterdir()}
    if names not in (BASE_WEB, BASE_WEB | PWA_FILES):
        raise ReleaseError("Web build has unexpected root files.")
    assets = directory / "assets"
    _ordinary_directory(assets)
    asset_files = sorted(assets.iterdir())
    if not asset_files or any(
        ASSET_NAME.fullmatch(path.name) is None for path in asset_files
    ):
        raise ReleaseError("Web build has unsupported asset files.")
    files = [
        directory / "index.html",
        *(directory / name for name in sorted(PWA_FILES & names)),
    ]
    files.extend(asset_files)
    if len(files) > 100:
        raise ReleaseError("Web build exceeds the supported file count.")
    total = 0
    for path in files:
        _ordinary_file(path)
        total += path.stat().st_size
    if total > MAX_WEB_BYTES:
        raise ReleaseError("Web build exceeds the supported size.")
    return files


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record(bundle: Path, path: Path) -> dict[str, str | int]:
    _ordinary_file(path)
    return {
        "path": path.relative_to(bundle).as_posix(),
        "size": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _source_commit(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    commit = result.stdout.strip()
    if result.returncode or HEX_40.fullmatch(commit) is None:
        raise ReleaseError("Source commit could not be identified.")
    return commit


def _source_id(root: Path, paths: tuple[str, ...] = RELEASE_SOURCE_PATHS) -> str:
    """Digest the literal release input list and reject other dirty workspace paths."""
    if len(paths) != len(set(paths)):
        raise ReleaseError("Release source inventory contains duplicate paths.")
    allowed = set(paths) | PROTECTED_PATHS | DOCUMENTATION_PATHS
    state = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if state.returncode:
        raise ReleaseError("Release source state could not be checked.")
    for record in state.stdout.split(b"\0"):
        if not record:
            continue
        if (
            len(record) < 4
            or record[2:3] != b" "
            or any(marker in record[:2] for marker in (b"R", b"C", b"D", b"U"))
            or record[:1] not in (b" ", b"?")
            or (record[:1] == b"?" and record[:2] != b"??")
        ):
            raise ReleaseError("Release source state includes an unsupported change.")
        try:
            name = record[3:].decode("utf-8")
        except UnicodeError:
            raise ReleaseError("Release source path is invalid.") from None
        if name not in allowed:
            raise ReleaseError("Release source state includes an unreviewed path.")
    digest = hashlib.sha256()
    digest.update(b"brickvault-p12-04b-source-v1\0")
    digest.update(_source_commit(root).encode("ascii") + b"\0")
    for name in sorted(paths):
        path = root / name
        _ordinary_parents(path, root)
        _ordinary_file(path)
        digest.update(name.encode("utf-8") + b"\0")
        digest.update(str(path.stat().st_size).encode("ascii") + b"\0")
        digest.update(bytes.fromhex(_sha256(path)))
    return digest.hexdigest()


def _verify_wheel_source(root: Path, wheel: Path) -> None:
    """Refuse a wheel whose packaged code differs from the reviewed checkout."""
    package = root / "services" / "api" / "src" / "brickvault_api"
    _ordinary_parents(package, root)
    _ordinary_directory(package)
    source_files: dict[str, Path] = {}
    for path in package.rglob("*"):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_dir():
            _ordinary_directory(path)
            continue
        _ordinary_parents(path, package)
        _ordinary_file(path)
        source_files["brickvault_api/" + path.relative_to(package).as_posix()] = path
    try:
        with zipfile.ZipFile(wheel) as archive:
            packaged = {
                item.filename
                for item in archive.infolist()
                if item.filename.startswith("brickvault_api/") and not item.is_dir()
            }
            if (
                not source_files
                or packaged != set(source_files)
                or archive.testzip() is not None
            ):
                raise ReleaseError(
                    "API wheel contents differ from the reviewed source."
                )
            for name, path in source_files.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != _sha256(path):
                    raise ReleaseError(
                        "API wheel contents differ from the reviewed source."
                    )
    except (OSError, zipfile.BadZipFile, KeyError):
        raise ReleaseError("API wheel could not be verified against source.") from None


def _verify_frontend(root: Path) -> None:
    # Reuse the accepted frontend verifier, including its private-value scan.
    command = (
        "import { verifyFrontend } from './scripts/tasks.mjs'; "
        "verifyFrontend(process.cwd());"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", command],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ReleaseError("Accepted frontend release verification failed.")


def _export_requirements(root: Path, destination: Path) -> None:
    uv = (
        root
        / ".local"
        / "tooling"
        / "uv"
        / UV_VERSION
        / ("uv.exe" if os.name == "nt" else "uv")
    )
    _ordinary_file(uv)
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith(
            ("UV_", "BVA_", "PG", "PYTHONPATH", "VIRTUAL_ENV")
        )
    }
    commands = [
        [str(uv), "--version"],
        [
            str(uv),
            "export",
            "--offline",
            "--locked",
            "--no-dev",
            "--no-emit-project",
            "--no-header",
            "--project",
            "services/api",
            "--format",
            "requirements.txt",
            "--output-file",
            str(destination),
        ],
    ]
    version = subprocess.run(
        commands[0],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if version.returncode or not version.stdout.startswith(f"uv {UV_VERSION} "):
        raise ReleaseError("Required repository-local uv version is unavailable.")
    exported = subprocess.run(
        commands[1], cwd=root, env=environment, capture_output=True, check=False
    )
    if exported.returncode:
        raise ReleaseError("Locked production requirements export failed.")
    _ordinary_file(destination)
    text = destination.read_text(encoding="utf-8")
    if "--hash=sha256:" not in text or "brickvault-api==" in text:
        raise ReleaseError("Exported production requirements are incomplete.")


def _copy_checked(source: Path, destination: Path) -> None:
    _ordinary_file(source)
    original_hash = _sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as source_file, destination.open("xb") as target_file:
        shutil.copyfileobj(source_file, target_file, length=1024 * 1024)
    if _sha256(destination) != original_hash:
        raise ReleaseError("Release input changed while being staged.")


def create(root: Path, release_id: str, source_id: str) -> tuple[Path, str]:
    """Make one fresh ignored bundle from a completed repository build."""
    if SAFE_ID.fullmatch(release_id) is None or HEX_64.fullmatch(source_id) is None:
        raise ReleaseError("Invalid reviewed release or source identifier.")
    root = root.resolve(strict=True)
    if _source_id(root) != source_id:
        raise ReleaseError("Release source differs from the reviewed source digest.")
    wheel = root / "services" / "api" / "dist" / WHEEL
    sdist = root / "services" / "api" / "dist" / SDIST
    web = root / "apps" / "web" / "dist"
    for source in (wheel, sdist, web):
        _ordinary_parents(source, root)
    _ordinary_file(wheel)
    _ordinary_file(sdist)
    _verify_wheel_source(root, wheel)
    web_files = _web_files(web)
    _verify_frontend(root)
    commit = _source_commit(root)

    local = root / ".local"
    _ordinary_directory(local)
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", ".local/releases/probe"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if ignored.returncode:
        raise ReleaseError("Release staging directory must be ignored by Git.")
    releases = local / "releases"
    if releases.exists():
        _ordinary_directory(releases)
    bundle = releases / release_id
    try:
        bundle.mkdir(parents=True, exist_ok=False)
    except OSError:
        raise ReleaseError(
            "Release staging directory already exists or is unavailable."
        ) from None
    _copy_checked(wheel, bundle / "api" / WHEEL)
    _copy_checked(sdist, bundle / "api" / SDIST)
    for path in web_files:
        _copy_checked(path, bundle / "web" / path.relative_to(web))
    _export_requirements(root, bundle / "api" / "requirements.txt")
    files = sorted(
        (_record(bundle, path) for path in bundle.rglob("*") if path.is_file()),
        key=lambda item: str(item["path"]),
    )
    manifest = {
        "schema": 1,
        "release_id": release_id,
        "source": {"commit": commit, "reviewed_id": source_id},
        "uv_version": UV_VERSION,
        "files": files,
    }
    if _source_id(root) != source_id:
        raise ReleaseError("Release source changed while artifacts were staged.")
    manifest_path = bundle / "manifest.json"
    with manifest_path.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(manifest, output, indent=2, sort_keys=True)
        output.write("\n")
    digest = _sha256(manifest_path)
    verify(bundle, digest, release_id, source_id)
    return bundle, digest


def verify(bundle: Path, expected_digest: str, release_id: str, source_id: str) -> None:
    """Verify every staged byte using a separately reviewed manifest digest."""
    if (
        HEX_64.fullmatch(expected_digest) is None
        or SAFE_ID.fullmatch(release_id) is None
        or HEX_64.fullmatch(source_id) is None
    ):
        raise ReleaseError("Invalid expected release identity or manifest digest.")
    _ordinary_directory(bundle)
    manifest_path = bundle / "manifest.json"
    _ordinary_file(manifest_path)
    if _sha256(manifest_path) != expected_digest:
        raise ReleaseError("Release manifest digest does not match the reviewed value.")
    try:
        manifest: Any = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        raise ReleaseError("Release manifest is unreadable.") from None
    source = manifest.get("source") if isinstance(manifest, dict) else None
    if (
        not isinstance(manifest, dict)
        or set(manifest) != {"schema", "release_id", "source", "uv_version", "files"}
        or manifest["schema"] != 1
        or manifest["release_id"] != release_id
        or manifest["uv_version"] != UV_VERSION
        or not isinstance(source, dict)
        or set(source) != {"commit", "reviewed_id"}
        or source["reviewed_id"] != source_id
        or not isinstance(source["commit"], str)
        or HEX_40.fullmatch(source["commit"]) is None
        or not isinstance(manifest["files"], list)
    ):
        raise ReleaseError("Release manifest identity or schema is invalid.")
    records = manifest["files"]
    expected_paths: set[str] = set()
    for item in records:
        if not isinstance(item, dict) or set(item) != {"path", "size", "sha256"}:
            raise ReleaseError("Release manifest file record is invalid.")
        name, size, digest = item["path"], item["size"], item["sha256"]
        if not isinstance(name, str) or PurePosixPath(name).as_posix() != name:
            raise ReleaseError("Release manifest path is invalid.")
        parts = PurePosixPath(name).parts
        if (
            name in expected_paths
            or not parts
            or parts[0] not in ("api", "web")
            or any(part in (".", "..") for part in parts)
            or type(size) is not int
            or size < 0
            or not isinstance(digest, str)
            or HEX_64.fullmatch(digest) is None
        ):
            raise ReleaseError("Release manifest path or hash is invalid.")
        expected_paths.add(name)
        path = bundle.joinpath(*parts)
        _ordinary_parents(path, bundle)
        _ordinary_file(path)
        if path.stat().st_size != size or _sha256(path) != digest:
            raise ReleaseError("Release file differs from its reviewed manifest.")
    required = {f"api/{WHEEL}", f"api/{SDIST}", "api/requirements.txt"}
    web = bundle / "web"
    web_paths = {"web/" + path.relative_to(web).as_posix() for path in _web_files(web)}
    if expected_paths != required | web_paths:
        raise ReleaseError("Release manifest omits or adds required files.")
    actual_paths: set[str] = set()
    for path in bundle.rglob("*"):
        if path.is_dir():
            _ordinary_directory(path)
        else:
            _ordinary_file(path)
            actual_paths.add(path.relative_to(bundle).as_posix())
    if actual_paths != expected_paths | {"manifest.json"}:
        raise ReleaseError("Release bundle contains an unreviewed file.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("source-id")
    create_parser = commands.add_parser("create")
    create_parser.add_argument("--release-id", required=True)
    create_parser.add_argument("--source-id", required=True)
    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("bundle", type=Path)
    verify_parser.add_argument("--manifest-sha256", required=True)
    verify_parser.add_argument("--release-id", required=True)
    verify_parser.add_argument("--source-id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "source-id":
            print(_source_id(ROOT))
        elif args.command == "create":
            bundle, digest = create(ROOT, args.release_id, args.source_id)
            print(f"Release bundle: {bundle.relative_to(ROOT)}")
            print(f"Manifest SHA-256: {digest}")
        else:
            verify(args.bundle, args.manifest_sha256, args.release_id, args.source_id)
            print("Release bundle verified against the reviewed manifest digest.")
    except (ReleaseError, OSError, ValueError):
        print(
            "Release bundle operation failed; details and private values redacted.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
