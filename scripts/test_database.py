import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import database
import pytest
from database import (
    DatabaseError,
    Instance,
    cleanup_database,
    local_context,
    runner_lock,
)


@pytest.mark.parametrize(
    "purpose,name,recorded",
    [
        ("development", "brickvault_dev", ["brickvault_dev"]),
        ("test", "brickvault_dev", ["brickvault_dev"]),
        ("test", "postgres", ["postgres"]),
        ("test", "brickvault_test_" + "a" * 32, []),
    ],
)
def test_cleanup_rejects_before_connecting(
    purpose: str, name: str, recorded: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("Unsafe cleanup reached PostgreSQL")

    monkeypatch.setattr(Instance, "bootstrap", forbidden)
    instance = Instance(
        "development" if purpose == "development" else "test", {}, "local", "owner"
    )
    with pytest.raises(DatabaseError):
        cleanup_database(instance, name, "run", recorded)


def test_exclusive_runner_lock() -> None:
    with runner_lock("unit-test"):
        with pytest.raises(DatabaseError), runner_lock("unit-test"):
            pytest.fail("Concurrent runner acquired lock")
        child = subprocess.run(
            [
                sys.executable,
                "-c",
                "from database import runner_lock, DatabaseError\n"
                "try:\n"
                "    with runner_lock('unit-test'): pass\n"
                "except DatabaseError:\n"
                "    raise SystemExit(42)\n",
            ],
            cwd=database.ROOT / "scripts",
            capture_output=True,
            timeout=10,
            check=False,
        )
        assert child.returncode == 42, (
            "A second process acquired the active runner lock"
        )
    with runner_lock("unit-test"):
        pass


def test_remote_context_rejected_before_daemon(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake(args: list[str], **kwargs: Any) -> str:
        calls.append(args)
        return "remote" if args[-1] == "show" else "ssh://remote.invalid"

    monkeypatch.setattr(database, "run", fake)
    with pytest.raises(DatabaseError):
        local_context()
    assert len(calls) == 2
    assert not any("info" in call for call in calls)


def test_unlabelled_named_volume_is_not_adopted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake(self: Instance, *args: str) -> str:
        if args == ("volume", "ls", "--format", "{{.Name}}"):
            return "brickvault-appraisal-test_data\n"
        return ""

    monkeypatch.setattr(Instance, "docker", fake)
    with pytest.raises(DatabaseError, match="unowned"):
        Instance("test", {}, "local", "token").verify(required=False)


def test_matching_name_and_compose_labels_need_checkout_ownership(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake(self: Instance, *args: str) -> str:
        if args[:3] == ("volume", "ls", "-q"):
            return "brickvault-appraisal-test_data\n"
        if args[:2] == ("volume", "inspect"):
            return json.dumps(
                [
                    {
                        "Labels": {
                            "com.docker.compose.project": self.project,
                            "com.docker.compose.volume": "data",
                            database.OWNER_LABEL: "another-checkout",
                        }
                    }
                ]
            )
        return ""

    monkeypatch.setattr(Instance, "docker", fake)
    with pytest.raises(DatabaseError, match="ownership"):
        Instance("test", {}, "local", "token").verify(required=False)


@pytest.mark.parametrize("failure", [OSError, KeyboardInterrupt])
def test_smoke_api_stops_child_when_initial_ledger_write_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure: type[BaseException]
) -> None:
    import integration_runner

    spawn = subprocess.Popen
    children: list[subprocess.Popen[bytes]] = []
    writes: list[dict[str, Any]] = []

    def start_child(args: list[str], **kwargs: Any) -> subprocess.Popen[bytes]:
        child = spawn(
            [sys.executable, "-c", "import threading; threading.Event().wait()"],
            **kwargs,
        )
        children.append(child)
        return child

    def fail_first_write(path: Path, record: dict[str, Any]) -> None:
        writes.append(dict(record))
        if len(writes) == 1:
            raise failure("injected ledger failure")

    monkeypatch.setattr(subprocess, "Popen", start_child)
    monkeypatch.setattr(integration_runner, "write_record", fail_first_write)
    monkeypatch.setattr(Instance, "target", lambda *args: "unused-before-server-start")
    try:
        with pytest.raises(failure):
            integration_runner.smoke_api(
                Instance("test", {}, "local", "token"),
                "brickvault_test_" + "a" * 32,
                {},
                tmp_path / "smoke.json",
            )
        assert len(children) == 1
        assert children[0].poll() is not None, (
            "Ledger failure leaked the owned API process"
        )
        assert writes[-1]["api_stopped"] is True
    finally:
        for child in children:
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=5)
