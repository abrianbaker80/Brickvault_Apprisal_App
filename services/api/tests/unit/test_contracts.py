import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from alembic.script import ScriptDirectory
from brickvault_api.contracts import export
from brickvault_api.persistence import database


def test_export_is_deterministic_and_independent(tmp_path: Path) -> None:
    assert export() == export()
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith(("BVA_", "PG"))
    }
    child = subprocess.run(
        [
            sys.executable,
            "-c",
            "import psycopg; psycopg.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError('unexpected connection')); from brickvault_api.settings import RuntimeSettings; RuntimeSettings.from_environment=lambda: (_ for _ in ()).throw(AssertionError('unexpected configuration load')); from brickvault_api.contracts import export; import sys; sys.stdout.buffer.write(export())",
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        check=False,
    )
    assert not (tmp_path / ".env.local").exists()
    assert child.returncode == 0
    assert child.stdout == export()
    schema = json.loads(export())
    assert schema["paths"]["/api/ready"]["get"]["responses"]["503"]
    assert (
        schema["components"]["schemas"]["Health"]["properties"]["service"]["const"]
        == "brickvault-api"
    )


def test_openapi_response_contract_allows_document_properties() -> None:
    schema = json.loads(export())
    response = schema["paths"]["/api/openapi.json"]["get"]["responses"]["200"]
    assert response["content"]["application/json"]["schema"] == {
        "type": "object",
        "additionalProperties": True,
    }


def test_migration_resources_preserve_literal_percent_in_package_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packaged = tmp_path / "package 100% ready"
    source = Path(database.migration_config().get_main_option("script_location") or "")
    shutil.copytree(source, packaged / "migrations", ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr(database, "files", lambda name: packaged)
    config = database.migration_config()
    assert Path(ScriptDirectory.from_config(config).dir) == packaged / "migrations"
    assert database.expected_revisions() == ("0001_foundation",)
