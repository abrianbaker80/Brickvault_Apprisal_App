"""Build the real package and independently install its exact locked dependencies."""

import importlib.metadata
import json
import os
import subprocess
import sys
import tarfile
import venv
import zipfile
from pathlib import Path
from uuid import uuid4

import tomllib
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
        "brickvault_api/production_admin.py",
        "brickvault_api/production_backup.py",
        "brickvault_api/persistence/runtime_grants.py",
        "brickvault_api/migrations/versions/0012_product_identity_qualifiers.py",
        "brickvault_api/migrations/sql/0012_product_identity_qualifiers_up.sql",
        "brickvault_api/migrations/sql/0012_product_identity_qualifiers_down.sql",
        "brickvault_api/migrations/versions/0014_settings_profiles.py",
        "brickvault_api/migrations/sql/0014_settings_profiles_up.sql",
        "brickvault_api/migrations/sql/0014_settings_profiles_down.sql",
        "brickvault_api/migrations/versions/0015_notes_source_urls.py",
        "brickvault_api/migrations/sql/0015_notes_source_urls_up.sql",
        "brickvault_api/migrations/sql/0015_notes_source_urls_down.sql",
        "brickvault_api/migrations/versions/0016_hunt_cached_runs.py",
        "brickvault_api/migrations/sql/0016_hunt_cached_runs_up.sql",
        "brickvault_api/migrations/sql/0016_hunt_cached_runs_down.sql",
        "brickvault_api/hunt.py",
        "brickvault_api/hunt_models.py",
        "brickvault_api/api/hunt.py",
        "brickvault_api/lineage_metadata.py",
        "brickvault_api/lineage_metadata_models.py",
        "brickvault_api/api/lineage_metadata.py",
        "brickvault_api/migrations/versions/0013_watchlist_targets.py",
        "brickvault_api/migrations/sql/0013_watchlist_targets_up.sql",
        "brickvault_api/migrations/sql/0013_watchlist_targets_down.sql",
        "brickvault_api/migrations/versions/0011_forecast_revisions.py",
        "brickvault_api/migrations/sql/0011_forecast_revisions_up.sql",
        "brickvault_api/migrations/sql/0011_forecast_revisions_down.sql",
        "brickvault_api/forecasts.py",
        "brickvault_api/migrations/versions/0010_saved_forecasts.py",
        "brickvault_api/migrations/sql/0010_saved_forecasts_up.sql",
        "brickvault_api/migrations/sql/0010_saved_forecasts_down.sql",
        "brickvault_api/auth.py",
        "brickvault_api/api/auth.py",
        "brickvault_api/migrations/versions/0009_private_authentication.py",
        "brickvault_api/migrations/sql/0009_private_authentication_up.sql",
        "brickvault_api/migrations/sql/0009_private_authentication_down.sql",
        "brickvault_api/market/product_refresh.py",
        "brickvault_api/market/product_refresh_models.py",
        "brickvault_api/market/product_refresh_retention.py",
        "brickvault_api/migrations/versions/0008_product_refresh_operations.py",
        "brickvault_api/migrations/sql/0008_product_refresh_operations_up.sql",
        "brickvault_api/migrations/sql/0008_product_refresh_operations_down.sql",
        "brickvault_api/calibration/__init__.py",
        "brickvault_api/calibration/__main__.py",
        "brickvault_api/calibration/arithmetic.py",
        "brickvault_api/calibration/budget.py",
        "brickvault_api/calibration/corpus.py",
        "brickvault_api/calibration/corpus.json",
        "brickvault_api/calibration/coverage.py",
        "brickvault_api/calibration/enumeration.py",
        "brickvault_api/calibration/manual.py",
        "brickvault_api/calibration/models.py",
        "brickvault_api/calibration/report.py",
        "brickvault_api/calibration/stage_one.py",
        "brickvault_api/market/accounting.py",
        "brickvault_api/market/discovery.py",
        "brickvault_api/market/discovery_worker.py",
        "brickvault_api/migrations/versions/0007_provider_discovery_accounting.py",
        "brickvault_api/migrations/sql/0007_provider_discovery_accounting_up.sql",
        "brickvault_api/migrations/sql/0007_provider_discovery_accounting_down.sql",
        "brickvault_api/market/__init__.py",
        "brickvault_api/market/models.py",
        "brickvault_api/market/policy.py",
        "brickvault_api/market/repository.py",
        "brickvault_api/market/retention.py",
        "brickvault_api/market/worker.py",
        "brickvault_api/migrations/versions/0006_market_cache.py",
        "brickvault_api/migrations/sql/0006_market_cache_up.sql",
        "brickvault_api/migrations/sql/0006_market_cache_down.sql",
        "brickvault_api/catalog/query_types.py",
        "brickvault_api/catalog/search.py",
        "brickvault_api/catalog/repository.py",
        "brickvault_api/catalog/expansion.py",
        "brickvault_api/catalog/containment.py",
        "brickvault_api/catalog/benchmark.py",
        "brickvault_api/migrations/versions/0005_catalog_search_indexes.py",
        "brickvault_api/migrations/sql/0005_catalog_search_indexes_up.sql",
        "brickvault_api/migrations/sql/0005_catalog_search_indexes_down.sql",
        "brickvault_api/migrations/versions/0004_catalog_staging.py",
        "brickvault_api/migrations/sql/0004_catalog_staging_up.sql",
        "brickvault_api/migrations/sql/0004_catalog_staging_down.sql",
        "brickvault_api/providers/rebrickable/records.py",
        "brickvault_api/providers/rebrickable/source.py",
        "brickvault_api/providers/rebrickable/parser.py",
        "brickvault_api/catalog/importer.py",
        "brickvault_api/catalog/promotion.py",
        "brickvault_api/catalog/status.py",
        "brickvault_api/catalog/connection.py",
        "brickvault_api/catalog/fingerprint.py",
        "brickvault_api/catalog/builder.py",
        "brickvault_api/catalog/candidate_validation.py",
        "brickvault_api/catalog/staged_validation.py",
        "brickvault_api/catalog/ownership.py",
        "brickvault_api/catalog/cli.py",
        "brickvault_api/migrations/env.py",
        "brickvault_api/migrations/script.py.mako",
        "brickvault_api/migrations/versions/0001_foundation.py",
        "brickvault_api/migrations/versions/0002_catalog_identity.py",
        "brickvault_api/migrations/versions/0003_catalog_inventory.py",
        "brickvault_api/migrations/catalog_ddl.py",
        "brickvault_api/migrations/sql/0002_catalog_identity_up.sql",
        "brickvault_api/migrations/sql/0002_catalog_identity_down.sql",
        "brickvault_api/migrations/sql/0003_catalog_inventory_up.sql",
        "brickvault_api/migrations/sql/0003_catalog_inventory_down.sql",
        "brickvault_api/catalog/__init__.py",
        "brickvault_api/catalog/models.py",
        "brickvault_api/catalog/types.py",
        "brickvault_api/catalog/normalization.py",
        "brickvault_api/catalog/semantics.py",
        "brickvault_api/catalog/validation.py",
    }
    with zipfile.ZipFile(wheel) as archive:
        assert required.issubset(archive.namelist())
        assert archive.testzip() is None
        assert not any(
            "/tests/" in name or "/fixtures/" in name or "/.local/" in name
            for name in archive.namelist()
        )
    with tarfile.open(sdist) as source_archive:
        names = source_archive.getnames()
        for resource in required:
            assert any(name.endswith("/src/" + resource) for name in names)
        assert not any(".env.local" in name or "/.local/" in name for name in names)
        assert not any("/tests/" in name or "/fixtures/" in name for name in names)
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
            "--offline",
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
from importlib.metadata import distribution
from brickvault_api.persistence.database import expected_revisions
from brickvault_api.production_admin import parse_config
from brickvault_api.production_backup import main as backup_main
from brickvault_api.contracts import export
assert pathlib.Path(brickvault_api.__file__).resolve().is_relative_to(pathlib.Path(sys.prefix).resolve())
admin_entry = [entry for entry in distribution('brickvault-api').entry_points if entry.group == 'console_scripts' and entry.name == 'brickvault-production-admin']
assert len(admin_entry) == 1 and admin_entry[0].load() is not None
backup_entry = [entry for entry in distribution('brickvault-api').entry_points if entry.group == 'console_scripts' and entry.name == 'brickvault-production-backup']
assert len(backup_entry) == 1 and backup_entry[0].load() is backup_main
from alembic.script import ScriptDirectory
from brickvault_api.persistence.database import migration_config
from brickvault_api.catalog.models import CATALOG_TABLES
from brickvault_api.catalog.search import search_input
from brickvault_api.catalog.expansion import expand_graph
from brickvault_api.catalog.query_types import SnapshotRef, QueryState
from brickvault_api.catalog.benchmark import BenchmarkManifest
from uuid import UUID
from importlib.resources import files
from brickvault_api.calibration.corpus import load_corpus
from brickvault_api.calibration.budget import corpus_demand
assert len(load_corpus().cases) == 12
assert corpus_demand(load_corpus())['mapping_attempts'] is None
assert expected_revisions() == ('0016_hunt_cached_runs',)
assert tuple(r.revision for r in ScriptDirectory.from_config(migration_config()).walk_revisions()) == ('0016_hunt_cached_runs','0015_notes_source_urls','0014_settings_profiles','0013_watchlist_targets','0012_product_identity_qualifiers','0011_forecast_revisions','0010_saved_forecasts','0009_private_authentication','0008_product_refresh_operations','0007_provider_discovery_accounting','0006_market_cache','0005_catalog_search_indexes','0004_catalog_staging','0003_catalog_inventory','0002_catalog_identity','0001_foundation')
assert len(CATALOG_TABLES) == 53
assert 'catalog_image_reference' not in CATALOG_TABLES
assert search_input('  Synthetic name  ', 20) == 'Synthetic name'
assert expand_graph(SnapshotRef(UUID(int=1), UUID(int=2), UUID(int=3), 'synthetic', True), UUID(int=4), {}).state == QueryState.INCOMPLETE
assert BenchmarkManifest.model_validate_json('{"benchmark_version":"catalog-2c-v1","cases":[{"case_id":"official","capability":"metadata","source_reference":"official-2d","evidence_reference":"deferred","acceptance_category":"OFFICIAL","expected":{}}]}').benchmark_version == 'catalog-2c-v1'
for revision in ('0016_hunt_cached_runs', '0015_notes_source_urls', '0002_catalog_identity', '0003_catalog_inventory', '0004_catalog_staging', '0005_catalog_search_indexes', '0006_market_cache', '0007_provider_discovery_accounting', '0008_product_refresh_operations', '0009_private_authentication', '0010_saved_forecasts'):
    for direction in ('up', 'down'):
        assert files('brickvault_api').joinpath('migrations','sql',revision+'_'+direction+'.sql').read_text()
socket.create_connection = lambda *a, **k: (_ for _ in ()).throw(AssertionError('unexpected connection'))
assert b'/api/ready' in export()
print('Independent installed wheel import, migration graph and credential-free schema passed.')
"""
    print(execute([str(python), "-I", "-c", probe], scratch).strip())
    admin_executable = installed / (
        "Scripts/brickvault-production-admin.exe"
        if sys.platform == "win32"
        else "bin/brickvault-production-admin"
    )
    assert "provision-db" in execute([str(admin_executable), "--help"], scratch)
    backup_executable = installed / (
        "Scripts/brickvault-production-backup.exe"
        if sys.platform == "win32"
        else "bin/brickvault-production-backup"
    )
    assert "verify" in execute([str(backup_executable), "--help"], scratch)
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
    print(f"Package check receipt: {(scratch / 'result.json').relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        package()
    except Exception:  # noqa: BLE001 - redact packaging failures at the CLI boundary.
        print("API packaging failed; no frontend build was attempted.", file=sys.stderr)
        sys.exit(1)
