"""Build the real package and independently install its exact locked dependencies."""

import importlib.metadata
import json
import os
import subprocess
import sys
import tarfile
import tomllib
import venv
import zipfile
from pathlib import Path
from uuid import uuid4

from database import ROOT, DatabaseError, private_path


def package() -> None:
    local_uv = (
        ROOT
        / ".local/tooling/uv/0.12.10"
        / ("uv.exe" if sys.platform == "win32" else "uv")
    )
    scratch = ROOT / ".local/package-check" / uuid4().hex
    private_path(scratch)
    scratch.mkdir(parents=True)
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith(
            ("UV_", "BVA_", "PG", "PYTHONPATH", "VIRTUAL_ENV")
        )
    }
    environment.update(
        {
            "TMP": str(ROOT / ".local/tmp"),
            "TEMP": str(ROOT / ".local/tmp"),
            "TMPDIR": str(ROOT / ".local/tmp"),
            "PYTHONNOUSERSITE": "1",
        }
    )

    def execute(args: list[str], cwd: Path) -> str:
        result = subprocess.run(
            args, cwd=cwd, env=environment, capture_output=True, text=True, check=False
        )
        if result.returncode:
            raise DatabaseError("API packaging command failed; output redacted.")
        return result.stdout

    if not execute([str(local_uv), "--version"], scratch).startswith("uv 0.12.10 "):
        raise DatabaseError("Expected repository-local uv 0.12.10.")
    assert importlib.metadata.version("hatchling") == "1.32.0"
    execute(
        [
            sys.executable,
            "-m",
            "hatchling",
            "build",
            "--target",
            "wheel",
            "--target",
            "sdist",
        ],
        ROOT / "services/api",
    )
    wheel = ROOT / "services/api/dist/brickvault_api-0.0.0-py3-none-any.whl"
    sdist = ROOT / "services/api/dist/brickvault_api-0.0.0.tar.gz"
    required = {
        "brickvault_api/migrations/env.py",
        "brickvault_api/migrations/script.py.mako",
        "brickvault_api/migrations/versions/0001_foundation.py",
    }
    with zipfile.ZipFile(wheel) as archive:
        assert required.issubset(archive.namelist())
        assert archive.testzip() is None
    with tarfile.open(sdist) as source_archive:
        names = source_archive.getnames()
        for resource in required:
            assert any(name.endswith("/src/" + resource) for name in names)
        assert not any(".env.local" in name or "/.local/" in name for name in names)
    constraints = scratch / "constraints.txt"
    with (ROOT / "services/api/uv.lock").open("rb") as lock_file:
        locked_packages = tomllib.load(lock_file)["package"]
    constraints.write_text(
        "\n".join(
            sorted(f"{item['name']}=={item['version']}" for item in locked_packages)
        )
        + "\n",
        encoding="utf-8",
    )
    installed = scratch / "venv"
    venv.EnvBuilder(with_pip=False).create(installed)
    python = installed / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    execute(
        [
            str(local_uv),
            "pip",
            "install",
            "--no-config",
            "--default-index",
            "https://pypi.org/simple",
            "--cache-dir",
            str(ROOT / ".local/uv-cache"),
            "--python",
            str(python),
            "--constraints",
            constraints.as_uri(),
            wheel.as_uri(),
        ],
        scratch,
    )
    probe = """import pathlib, sys, socket
import brickvault_api
from brickvault_api.persistence.database import expected_revisions
from brickvault_api.contracts import export
assert pathlib.Path(brickvault_api.__file__).resolve().is_relative_to(pathlib.Path(sys.prefix).resolve())
assert expected_revisions() == ('0001_foundation',)
socket.create_connection = lambda *a, **k: (_ for _ in ()).throw(AssertionError('unexpected connection'))
assert b'/api/ready' in export()
print('Independent installed wheel import, migration graph and credential-free schema passed.')
"""
    print(execute([str(python), "-I", "-c", probe], scratch).strip())
    (scratch / "result.json").write_text(
        json.dumps(
            {
                "wheel": str(wheel.relative_to(ROOT)),
                "sdist": str(sdist.relative_to(ROOT)),
                "installed_wheel_verified": True,
            }
        ),
        encoding="utf-8",
    )
    print(
        "API wheel and sdist verified; artifacts and independent environment remain ignored inside repository."
    )


if __name__ == "__main__":
    try:
        package()
    except Exception:
        print("API packaging failed; no frontend build was attempted.", file=sys.stderr)
        sys.exit(1)
