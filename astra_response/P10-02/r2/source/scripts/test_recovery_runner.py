"""Pure refusal checks for the TEST-only recovery target selection."""

from typing import Any
from uuid import uuid4

import pytest
from database import DatabaseError, Instance
from recovery_runner import dump_path, reserve_dump, validate_selection

RUN = "a" * 32
SOURCE = "brickvault_test_" + "b" * 32
DESTINATION = "brickvault_test_" + "c" * 32


def selection() -> tuple[Instance, dict[str, Any]]:
    selected = Instance("test", {}, "local", "d" * 32)
    record = {
        "run_id": RUN,
        "project": selected.project,
        "instance_owner": selected.owner,
        "recorded_databases": [SOURCE, DESTINATION],
    }
    return selected, record


@pytest.mark.parametrize(
    "change", ["same", "unrecorded", "development", "owner", "run", "name"]
)
def test_recovery_refuses_unowned_or_ambiguous_selection(change: str) -> None:
    selected, record = selection()
    source, destination, run_id = SOURCE, DESTINATION, RUN
    if change == "same":
        destination = source
    elif change == "unrecorded":
        record["recorded_databases"] = [SOURCE]
    elif change == "development":
        selected.purpose = "development"
        record["project"] = selected.project
    elif change == "owner":
        record["instance_owner"] = "e" * 32
    elif change == "run":
        run_id = "e" * 32
    else:
        destination = "brickvault_dev"
    with pytest.raises(DatabaseError, match="distinct, exact run-recorded TEST"):
        validate_selection(selected, run_id, source, destination, record)


def test_dump_path_rejects_untrusted_run_identity() -> None:
    with pytest.raises(DatabaseError, match="Invalid recovery run identity"):
        dump_path("../outside")


def test_existing_dump_is_not_adopted_or_overwritten() -> None:
    run_id = uuid4().hex
    path = dump_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(b"other run")
    try:
        record: dict[str, Any] = {"dump_owned": False}
        with pytest.raises(FileExistsError):
            reserve_dump(run_id, record)
        assert record["dump_owned"] is False
        assert path.read_bytes() == b"other run"
    finally:
        path.unlink()
