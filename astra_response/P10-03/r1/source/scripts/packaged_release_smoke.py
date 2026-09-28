"""One owned TEST HTTP smoke of the installed wheel and normal web build."""

import argparse
import ctypes
import json
import os
import re
import secrets
import signal
import socket
import stat
import subprocess
import sys
import time
from pathlib import Path
from types import FrameType
from typing import Any, cast
from uuid import uuid4


class SmokeError(RuntimeError):
    """Safe, operator-facing failure category."""


class WorkerHandle:
    """Retain the exact Python worker, including behind Windows venv redirectors."""

    def __init__(self, pid: int, launcher: subprocess.Popen[bytes]) -> None:
        if type(pid) is not int or pid <= 0:
            raise SmokeError(
                "Installed API worker reported an invalid process identity."
            )
        self.launcher = launcher
        self.handle: int | None = None
        if os.name == "nt":
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel.OpenProcess.argtypes = [
                ctypes.c_uint32,
                ctypes.c_int,
                ctypes.c_uint32,
            ]
            kernel.OpenProcess.restype = ctypes.c_void_p
            handle = kernel.OpenProcess(0x00100000 | 0x1000 | 0x0001, 0, pid)
            if not handle:
                raise SmokeError("Installed API worker process is unavailable.")
            self.handle = handle
        elif pid != launcher.pid:
            raise SmokeError("Installed API worker is not the owned child process.")

    def alive(self) -> bool:
        if self.handle is None:
            return self.launcher.poll() is None
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetExitCodeProcess.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint32),
        ]
        kernel.GetExitCodeProcess.restype = ctypes.c_int
        status = ctypes.c_uint32()
        if not kernel.GetExitCodeProcess(self.handle, ctypes.byref(status)):
            raise SmokeError("Installed API worker status is unavailable.")
        return status.value == 259  # STILL_ACTIVE

    def stop(self) -> None:
        if self.handle is None:
            return
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel.TerminateProcess.restype = ctypes.c_int
        kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel.WaitForSingleObject.restype = ctypes.c_uint32
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel.CloseHandle.restype = ctypes.c_int
        try:
            if self.alive() and not kernel.TerminateProcess(self.handle, 1):
                raise SmokeError("Exact installed API worker could not be stopped.")
            if kernel.WaitForSingleObject(self.handle, 10000) != 0:
                raise SmokeError("Exact installed API worker did not exit.")
        finally:
            kernel.CloseHandle(self.handle)
            self.handle = None


def select_package(root: Path, receipt: Path) -> tuple[Path, Path]:
    """Select one exact package-check venv, never a checkout or arbitrary Python."""
    root = root.resolve(strict=True)
    receipt = receipt.absolute()
    scratch = receipt.parent
    package_checks = root / ".local" / "package-check"
    if (
        receipt.name != "result.json"
        or scratch.parent != package_checks
        or re.fullmatch(r"[a-f0-9]{32}", scratch.name) is None
        or any(
            path.is_symlink() or path.is_junction()
            for path in (package_checks, scratch, receipt)
        )
        or not receipt.is_file()
        or not stat.S_ISREG(receipt.lstat().st_mode)
        or receipt.lstat().st_nlink != 1
    ):
        raise SmokeError("Expected one ordinary, exact package-check receipt.")
    try:
        result = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise SmokeError("Package-check receipt is unreadable or invalid.") from None
    if not isinstance(result, dict) or not all(
        isinstance(result.get(key), str) for key in ("wheel", "sdist")
    ):
        raise SmokeError(
            "Package-check receipt does not prove the locked wheel install."
        )
    normalized = {
        **result,
        "wheel": result["wheel"].replace("\\", "/"),
        "sdist": result["sdist"].replace("\\", "/"),
    }
    if normalized != {
        "wheel": "services/api/dist/brickvault_api-0.0.0-py3-none-any.whl",
        "sdist": "services/api/dist/brickvault_api-0.0.0.tar.gz",
        "installed_wheel_verified": True,
    }:
        raise SmokeError(
            "Package-check receipt does not prove the locked wheel install."
        )
    python = (
        scratch / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    )
    if not python.is_file() or not (root / normalized["wheel"]).is_file():
        raise SmokeError("Selected package environment or wheel is unavailable.")
    return scratch, python


def child_environment(runtime_url: str, marker: str, build: Path) -> dict[str, str]:
    allowed = {
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "LOCALAPPDATA",
        "APPDATA",
        "HOME",
        "TMPDIR",
    }
    result = {key: value for key, value in os.environ.items() if key.upper() in allowed}
    result.update(
        {
            "PYTHONNOUSERSITE": "1",
            "BVA_RUNTIME_DATABASE_URL": runtime_url,
            "BVA_DATABASE_OWNERSHIP_MARKER": marker,
            "BVA_WEB_BUILD_DIR": str(build),
        }
    )
    return result


def serve_installed(ready: Path) -> None:
    """Executed only by the selected venv Python with -I."""
    import brickvault_api
    import uvicorn
    from brickvault_api.main import create_app
    from brickvault_api.observability import logging_config
    from brickvault_api.settings import RuntimeSettings
    from pydantic import SecretStr

    package_file = Path(brickvault_api.__file__).resolve(strict=True)
    prefix = Path(sys.prefix).resolve(strict=True)
    if not sys.flags.isolated or not package_file.is_relative_to(prefix):
        raise SmokeError("API did not import from its isolated installed package.")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if os.name == "nt":
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    try:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
        settings = RuntimeSettings(
            purpose="test",
            port=port,
            database_url=SecretStr(os.environ["BVA_RUNTIME_DATABASE_URL"]),
            database_ownership_marker=SecretStr(
                os.environ["BVA_DATABASE_OWNERSHIP_MARKER"]
            ),
            static_enabled=True,
            web_build_dir=os.environ["BVA_WEB_BUILD_DIR"],
            auth_allow_loopback_http=True,
        )
        settings.target()
        app = create_app(settings)
        with ready.open("x", encoding="utf-8") as output:
            json.dump(
                {
                    "pid": os.getpid(),
                    "port": port,
                    "prefix": str(prefix),
                    "package_file": str(package_file),
                    "isolated": bool(sys.flags.isolated),
                    "nonce": os.environ["BVA_PACKAGE_NONCE"],
                },
                output,
            )
        uvicorn.Server(
            uvicorn.Config(
                app,
                host="127.0.0.1",
                port=port,
                access_log=False,
                proxy_headers=False,
                log_config=logging_config("INFO"),
            )
        ).run(sockets=[listener])
    finally:
        listener.close()


def verify_child_identity(ready: dict[str, Any], scratch: Path, pid: int) -> int:
    venv = (scratch / "venv").resolve(strict=True)
    try:
        port = ready["port"]
        prefix = Path(ready["prefix"]).resolve(strict=True)
        package_file = Path(ready["package_file"]).resolve(strict=True)
        checks = {
            "pid": type(ready["pid"]) is int
            and ready["pid"] > 0
            and (os.name == "nt" or ready["pid"] == pid),
            "port": type(port) is int and 1 <= port <= 65535,
            "isolated": ready["isolated"] is True,
            "prefix": prefix == venv,
            "package_root": package_file.is_relative_to(venv),
            "site_packages": "site-packages" in package_file.parts,
            "package_module": package_file.name == "__init__.py"
            and package_file.parent.name == "brickvault_api",
        }
    except (KeyError, OSError, TypeError, ValueError):
        raise SmokeError("Server import identity record is incomplete.") from None
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise SmokeError("Server import identity failed: " + ", ".join(failed))
    return cast(int, port)


def require_response(
    response: Any, status: int, label: str, *, private: bool = False
) -> None:
    if response.status_code != status:
        raise SmokeError(
            f"{label}: expected HTTP {status}, got {response.status_code}."
        )
    if private and response.headers.get("cache-control") != "no-store":
        raise SmokeError(f"{label}: private response lacks no-store.")


def run_http(
    origin: str, build: Path, password: str, secrets_to_check: list[str]
) -> dict[str, Any]:
    import httpx

    checks = 0
    public_bodies: list[bytes] = []
    with httpx.Client(base_url=origin, timeout=3, trust_env=False) as client:
        shell = client.get("/")
        require_response(shell, 200, "public shell")
        if (
            not shell.headers.get("content-type", "").startswith("text/html")
            or shell.content != (build / "index.html").read_bytes()
        ):
            raise SmokeError("HTTP shell differs from the selected built frontend.")
        public_bodies.append(shell.content)
        checks += 1
        assets = sorted(
            set(re.findall(rb"/assets/[A-Za-z0-9_-]+\.(?:js|css)", shell.content))
        )
        if not assets or not any(path.endswith(b".js") for path in assets):
            raise SmokeError("Built shell has no representative JavaScript asset.")
        for raw_path in assets:
            path = raw_path.decode("ascii")
            response = client.get(path)
            require_response(response, 200, "built asset")
            if response.content != (build / path.lstrip("/")).read_bytes():
                raise SmokeError("HTTP asset differs from the selected built frontend.")
            public_bodies.append(response.content)
            checks += 1
        for path in ("/manifest.webmanifest", "/sw.js"):
            if (build / path.lstrip("/")).exists():
                response = client.get(path)
                require_response(response, 200, "PWA file")
                if response.content != (build / path.lstrip("/")).read_bytes():
                    raise SmokeError("HTTP PWA file differs from the selected build.")
                public_bodies.append(response.content)
                checks += 1

        denied = client.get("/api/settings")
        require_response(denied, 401, "pre-login protected read", private=True)
        checks += 1
        login = client.post(
            "/api/auth/login",
            json={"password": password},
            headers={"Origin": origin, "X-BrickVault-Login": "1"},
        )
        require_response(login, 200, "login", private=True)
        csrf = login.json().get("csrf_token")
        cookie = client.cookies.get("bva_session")
        if not isinstance(csrf, str) or not csrf or not cookie:
            raise SmokeError("Login did not establish a private session.")
        secrets_to_check.extend((csrf, cookie))
        checks += 1
        ready = client.get("/api/ready")
        require_response(ready, 200, "authenticated readiness", private=True)
        if ready.json() != {
            "status": "ready",
            "database": "ok",
            "migrations": "current",
        }:
            raise SmokeError("Packaged runtime is not current and ready.")
        checks += 1
        current = client.get("/api/settings")
        require_response(current, 200, "Settings read", private=True)
        settings = current.json()
        if not isinstance(settings.get("revision"), int) or not isinstance(
            settings.get("defaults"), dict
        ):
            raise SmokeError("Settings response is incomplete.")
        checks += 1
        update = {
            "expected_revision": settings["revision"],
            "default_profile_id": settings["default_profile_id"],
            "defaults": {**settings["defaults"], "sale_basis": "MANUAL"},
        }
        refused = client.put("/api/settings", json=update, headers={"Origin": origin})
        require_response(refused, 403, "Settings CSRF refusal", private=True)
        checks += 1
        saved = client.put(
            "/api/settings",
            json=update,
            headers={"Origin": origin, "X-CSRF-Token": csrf},
        )
        require_response(saved, 200, "Settings CSRF update", private=True)
        if saved.json()["revision"] != settings["revision"] + 1:
            raise SmokeError("Settings update did not advance its revision.")
        checks += 1
        readback = client.get("/api/settings")
        require_response(readback, 200, "Settings readback", private=True)
        if (
            readback.json() != saved.json()
            or readback.json()["defaults"]["sale_basis"] != "MANUAL"
        ):
            raise SmokeError("Settings update was not read back.")
        checks += 1
        unknown = client.get("/api/p10-03-unknown")
        require_response(unknown, 404, "unknown API route", private=True)
        if (
            not unknown.headers.get("content-type", "").startswith("application/json")
            or b"<html" in unknown.content.lower()
        ):
            raise SmokeError("Unknown API route returned frontend HTML.")
        checks += 1
        for path in ("/.env.local", "/assets/.env.local", "/scripts/database.py"):
            exposed = client.get(path)
            require_response(exposed, 404, "static-root exclusion", private=True)
            public_bodies.append(exposed.content)
            checks += 1
        logout = client.post(
            "/api/auth/logout", headers={"Origin": origin, "X-CSRF-Token": csrf}
        )
        require_response(logout, 204, "logout", private=True)
        checks += 1
        denied_again = client.get("/api/settings")
        require_response(denied_again, 401, "post-logout protected read", private=True)
        checks += 1
    for value in secrets_to_check:
        if value and any(value.encode("utf-8") in body for body in public_bodies):
            raise SmokeError("Public HTTP bytes contain a private value.")
    return {"http_checks": checks, "asset_count": len(assets), "static_root_probes": 3}


def check_log(log: Path, secrets_to_check: list[str]) -> int:
    content = log.read_text(encoding="utf-8")
    if any(value and value in content for value in secrets_to_check):
        raise SmokeError("Packaged API log contains a private value.")
    events: list[dict[str, Any]] = []
    for line in content.splitlines():
        try:
            parsed = json.loads(line)
        except ValueError:
            raise SmokeError(
                "Packaged API log is not structured safe metadata."
            ) from None
        if isinstance(parsed, dict) and parsed.get("category") == "request":
            events.append(parsed)
    if not any(
        event.get("route") == "/api/settings" and event.get("status") == 200
        for event in events
    ):
        raise SmokeError("Packaged API log lacks Settings operation results.")
    if not any(
        event.get("route") == "/api/settings" and event.get("status") == 401
        for event in events
    ):
        raise SmokeError("Packaged API log lacks protected-read denial results.")
    return len(events)


def smoke(receipt: Path) -> None:
    import httpx
    from brickvault_api.auth import AuthService
    from brickvault_api.catalog.connection import CatalogDatabase
    from brickvault_api.settings import TEST_DATABASE
    from database import (
        LOCAL,
        ROOT,
        DatabaseError,
        cleanup_database,
        database_marker,
        instance,
        migrate,
        private_path,
        provision,
        runner_lock,
        write_record,
    )

    scratch, python = select_package(ROOT, receipt)
    private_path(scratch / "result.json")
    build = ROOT / "apps/web/dist"
    if not (build / "index.html").is_file():
        raise SmokeError("Normal built frontend is unavailable.")
    with runner_lock():
        selected = instance("test")
        before = selected.verify(required=False)
        if before is None:
            raise SmokeError("Existing owned TEST container is required.")
        before_resources = selected.inventory()
        running_before = bool(before["State"]["Running"])
        run_id = uuid4().hex
        database = "brickvault_test_" + uuid4().hex
        if TEST_DATABASE.fullmatch(database) is None:
            raise SmokeError("Invalid disposable TEST database name.")
        journal = LOCAL / "runs" / f"{run_id}.json"
        log = LOCAL / "runs" / f"{run_id}.packaged-api.log"
        ready_file = LOCAL / "runs" / f"{run_id}.packaged-api.ready.json"
        for path in (journal, log, ready_file):
            private_path(path)
            if path.exists():
                raise SmokeError(
                    "Owned smoke path collision; existing evidence preserved."
                )
        record: dict[str, Any] = {
            "run_id": run_id,
            "kind": "P10-03-packaged-release",
            "project": selected.project,
            "instance_owner": selected.owner,
            "running_before": running_before,
            "resources_before": before_resources,
            "recorded_databases": [database],
            "status": "starting",
            "leftovers": [],
        }
        write_record(journal, record)
        previous_handler = signal.getsignal(signal.SIGTERM)

        def interrupted(signum: int, frame: FrameType | None) -> None:
            raise KeyboardInterrupt

        signal.signal(signal.SIGTERM, interrupted)
        cleanup_failures: list[str] = []
        child: subprocess.Popen[bytes] | None = None
        worker: WorkerHandle | None = None
        port: int | None = None
        password = ""
        secrets_to_check: list[str] = []
        try:
            selected.up()
            if selected.inventory() != before_resources:
                raise SmokeError("Owned TEST resource inventory changed unexpectedly.")
            with selected.bootstrap() as connection:
                if connection.execute(
                    "SELECT 1 FROM pg_database WHERE datname=%s", (database,)
                ).fetchone():
                    raise SmokeError("Disposable TEST target already exists.")
            record["status"] = "provisioning"
            write_record(journal, record)
            provision(selected, database, run_id)
            migrate(selected, database, run_id=run_id)
            password = secrets.token_urlsafe(32)
            marker = database_marker(selected, run_id)
            owner_url = selected.target(database, "owner")
            runtime_url = selected.target(database, "runtime")
            secrets_to_check = [
                password,
                owner_url,
                runtime_url,
                *(value for key, value in selected.config.items() if "PASSWORD" in key),
            ]
            AuthService(
                CatalogDatabase(owner_url, "test", marker, role="owner")
            ).provision(password)
            record["status"] = "testing"
            write_record(journal, record)
            environment = child_environment(runtime_url, marker, build)
            nonce = secrets.token_hex(16)
            environment["BVA_PACKAGE_NONCE"] = nonce
            secrets_to_check.append(nonce)
            with log.open("x", encoding="utf-8") as output:
                child = subprocess.Popen(
                    [
                        str(python),
                        "-I",
                        str(Path(__file__).resolve()),
                        "--serve",
                        str(ready_file),
                    ],
                    cwd=scratch,
                    env=environment,
                    stdout=output,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
            deadline = time.monotonic() + 20
            while not ready_file.exists():
                if child.poll() is not None or time.monotonic() >= deadline:
                    raise SmokeError(
                        "Installed API exited or timed out during startup."
                    )
                time.sleep(0.05)
            while True:
                try:
                    ready = json.loads(ready_file.read_text(encoding="utf-8"))
                    break
                except (OSError, ValueError):
                    if child.poll() is not None or time.monotonic() >= deadline:
                        raise SmokeError(
                            "Installed API readiness record is incomplete."
                        ) from None
                    time.sleep(0.05)
            if ready.get("nonce") != nonce:
                raise SmokeError(
                    "Installed API readiness nonce does not match this run."
                )
            worker = WorkerHandle(ready.get("pid"), child)
            port = verify_child_identity(ready, scratch, child.pid)
            origin = f"http://127.0.0.1:{port}"
            with httpx.Client(base_url=origin, timeout=2, trust_env=False) as client:
                while True:
                    if not worker.alive() or time.monotonic() >= deadline:
                        raise SmokeError("Installed API did not reach HTTP health.")
                    try:
                        health = client.get("/api/health")
                        require_response(health, 200, "startup health")
                        break
                    except httpx.ConnectError:
                        time.sleep(0.05)
            if not worker.alive():
                raise SmokeError("Installed API exited before HTTP smoke.")
            record["installed_package_verified"] = True
            record["installed_import"] = str(
                Path(ready["package_file"]).relative_to(ROOT)
            )
            record.update(run_http(origin, build, password, secrets_to_check))
            record["status"] = "passed"
        except BaseException:
            record["status"] = "failed_or_interrupted"
            raise
        finally:
            if worker is not None:
                try:
                    worker.stop()
                except SmokeError:
                    cleanup_failures.append("api_worker")
            if child is not None:
                try:
                    if child.poll() is None:
                        child.terminate()
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=5)
                if child.poll() is None:
                    cleanup_failures.append("api_process")
                elif port is not None:
                    with socket.socket() as probe:
                        if probe.connect_ex(("127.0.0.1", port)) == 0:
                            cleanup_failures.append("api_listener")
                record["api_stopped"] = (
                    "api_worker" not in cleanup_failures
                    and worker is not None
                    and "api_process" not in cleanup_failures
                    and "api_listener" not in cleanup_failures
                )
            try:
                if ready_file.exists():
                    ready_file.unlink()
            except OSError:
                cleanup_failures.append("api_readiness_record")
            log_failure: SmokeError | None = None
            if log.exists() and record["status"] == "passed":
                try:
                    record["safe_log_events"] = check_log(log, secrets_to_check)
                except SmokeError as error:
                    record["status"] = "failed_log_check"
                    log_failure = error
            try:
                selected.up()
                if cleanup_database(
                    selected, database, run_id, record["recorded_databases"]
                ):
                    record["removed_databases"] = [database]
            except Exception:
                cleanup_failures.append("database")
            try:
                if not running_before:
                    selected.stop()
                after = selected.verify()
                if after is None:
                    raise SmokeError("Owned TEST container disappeared during cleanup.")
                record["running_after"] = bool(after["State"]["Running"])
                if selected.inventory() != before_resources:
                    cleanup_failures.append("resources")
            except Exception:
                cleanup_failures.append("service")
            record["leftovers"] = cleanup_failures
            if cleanup_failures:
                record["status"] = "cleanup_incomplete"
            write_record(journal, record)
            signal.signal(signal.SIGTERM, previous_handler)
            print(
                json.dumps(
                    {
                        "packaged_smoke": record["status"],
                        "installed_package_verified": record.get(
                            "installed_package_verified", False
                        ),
                        "http_checks": record.get("http_checks", 0),
                        "assets": record.get("asset_count", 0),
                        "safe_log_events": record.get("safe_log_events", 0),
                        "databases_removed": len(record.get("removed_databases", [])),
                        "test_service_restored": record.get("running_after")
                        == running_before,
                        "leftovers": cleanup_failures,
                        "ledger": str(journal.relative_to(ROOT)),
                    }
                )
            )
        if log_failure is not None:
            raise log_failure
        if cleanup_failures:
            raise DatabaseError(
                "Owned packaged-smoke cleanup incomplete; inspect exact ledger."
            )
        if record["status"] != "passed":
            raise SmokeError("Packaged HTTP smoke did not pass.")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Owned packaged release HTTP smoke"
        )
        parser.add_argument("package_check", type=Path, nargs="?")
        parser.add_argument("--serve", type=Path, help=argparse.SUPPRESS)
        args = parser.parse_args()
        if args.serve is not None:
            serve_installed(args.serve)
        elif args.package_check is not None:
            smoke(args.package_check)
        else:
            raise SmokeError("Select the current build's package-check result.json.")
    except SmokeError as error:
        print(f"Packaged release smoke failed: {error}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        print(
            "Packaged release smoke failed; private details redacted.", file=sys.stderr
        )
        sys.exit(1)
