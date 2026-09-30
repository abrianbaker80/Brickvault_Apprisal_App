# Focused source validation

Fifty-four tests passed: 49 production backup/admin tests and five release-manifest tests. New coverage verifies direct PostgreSQL commands using the exact local socket, database and user without a privilege-transition wrapper; the existing no-persistent-output check remains. A real child-process test verifies closed stdin, no inherited password/service credentials and disabled password-file lookup.

Existing tests retain identical dual-stream bytes/digest behavior, failure on either failed destination or failed source, redacted CLI errors, complete receipt validation, six readbacks, receipt-digest/marker/revision/staleness binding and admin mutation refusal without the generated proof.

Targeted Ruff with the repository rule set, format checks and strict mypy passed. The full release build passed the independent wheel, migration graph and frontend verifier. No unrelated historical test suite or synthetic restore qualification was rerun.

Commands:

    python -m pytest -c services/api/pyproject.toml services/api/tests/unit/test_production_backup.py services/api/tests/unit/test_production_admin.py scripts/test_release_manifest.py -q
    python -m ruff check --select E4,E7,E9,F,I,UP,B <six affected source/test files>
    python -m ruff format --check <six affected source/test files>
    python -m mypy --config-file services/api/pyproject.toml <production_backup.py, production_admin.py, release_manifest.py>
    pnpm build

The final focused test run reported 54 passed. Formatting reported six files already formatted; mypy reported no issues in three source files.
