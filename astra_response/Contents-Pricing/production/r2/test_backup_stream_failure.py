"""Real synthetic children exercise finalization, redaction and failure cleanup."""

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from brickvault_api import production_backup as backup


def child(code: str) -> list[str]:
    return [sys.executable, "-c", code]


SOURCE = child("import sys;sys.stdout.buffer.write(b'x'*1024)")
SINK = child("import sys;sys.stdin.buffer.read()")


def test_finalization_uses_stream_deadline_not_unrelated_30_second_cap() -> None:
    slow = child("import sys,time;sys.stdin.buffer.read();time.sleep(31)")
    assert backup.stream_to_two(
        SOURCE, [SINK, slow], [os.environ, os.environ], deadline_seconds=45
    ) == (1024, hashlib.sha256(b"x" * 1024).hexdigest())


@pytest.mark.parametrize("failure", ["producer", "sink", "timeout", "spawn"])
def test_failure_has_safe_stage_status_and_reaps_children(
    failure: str, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    created: list[subprocess.Popen[bytes]] = []
    original = subprocess.Popen

    def record(*args: object, **kwargs: object) -> subprocess.Popen[bytes]:
        p = original(*args, **kwargs)  # type: ignore[call-overload]
        created.append(p)
        return p  # type: ignore[no-any-return]

    monkeypatch.setattr(backup.subprocess, "Popen", record)
    # Raw secrets, newline injection, signed URLs and stderr floods must never escape.
    noisy = (
        "import sys;sys.stderr.write(('secret-value https://private/?sig=secret-value\\n'*8192));"
    )
    source = SOURCE
    sinks = [SINK, SINK]
    deadline = 10.0
    if failure == "producer":
        source = child(noisy + "sys.stdout.buffer.write(b'x');sys.exit(7)")
    elif failure == "sink":
        sinks[1] = child(noisy + "sys.stdin.buffer.read();sys.exit(9)")
    elif failure == "spawn":
        sinks[1] = ["missing-synthetic-backup-command"]
    else:
        sinks[1] = child(noisy + "import time;sys.stdin.buffer.read();time.sleep(30)")
        deadline = 0.5
    started = time.monotonic()
    with pytest.raises(backup.BackupStreamError) as error:
        backup.stream_to_two(source, sinks, [os.environ, os.environ], deadline_seconds=deadline)
    diagnostic = error.value.diagnostic
    assert diagnostic["workers_alive"] == 0
    assert created and all(p.poll() is not None for p in created)
    assert "secret-value" not in caplog.text + str(error.value) + json.dumps(diagnostic)
    assert "https://" not in caplog.text + json.dumps(diagnostic)
    if failure in ("producer", "sink"):
        index, code = (0, 7) if failure == "producer" else (2, 9)
        assert diagnostic["reason"] == "nonzero_exit"
        assert diagnostic["children"][index]["exit_before_cleanup"] == code
        assert diagnostic["children"][index]["stderr_bytes"] > 100_000
    elif failure == "timeout":
        assert diagnostic["reason"] == "deadline" and diagnostic["stage"] == "finalize"
        assert diagnostic["children"][2]["exit_before_cleanup"] is None
        assert time.monotonic() - started < 8
    else:
        assert diagnostic["reason"] == "spawn_failure" and diagnostic["role"] == "drive"


def test_failed_stream_cannot_write_complete_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(backup, "RECEIPT_DIR", tmp_path)
    monkeypatch.setattr(backup, "_configuration_files", lambda: ())
    monkeypatch.setattr(backup, "_run_id", lambda: "a" * 32)
    monkeypatch.setattr(backup, "_producer", lambda *_: SOURCE)
    failed = child("import sys;sys.stdin.buffer.read();sys.exit(9)")
    destinations = tuple(
        SimpleNamespace(command=lambda *_, c=c: c, environment=lambda: os.environ)
        for c in (SINK, failed)
    )
    monkeypatch.setattr(backup, "DESTINATIONS", destinations)
    config: Any = SimpleNamespace()
    with pytest.raises(backup.BackupStreamError):
        backup._capture(config, ("0019_reviewed_dataset_foundation",), 3, ("database.dump",))
    assert not list(tmp_path.iterdir())


@pytest.mark.skipif(os.name != "posix", reason="Production process groups are POSIX")
def test_timeout_closes_descendant_pipe_and_reaps_owned_parent() -> None:
    sink = child(
        "import subprocess,sys,time;sys.stdin.buffer.read();"
        "subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);"
        "time.sleep(60)"
    )
    with pytest.raises(backup.BackupStreamError) as error:
        backup.stream_to_two(SOURCE, [SINK, sink], [os.environ, os.environ], deadline_seconds=0.5)
    assert error.value.diagnostic["workers_alive"] == 0
    assert all(s["exit_after_cleanup"] is not None for s in error.value.diagnostic["children"])
