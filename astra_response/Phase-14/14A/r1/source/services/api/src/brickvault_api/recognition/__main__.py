"""Run from this checkout: python -m brickvault_api.recognition --help."""

import argparse
import getpass
import json
import subprocess
import sys
import warnings
from datetime import date, timedelta
from pathlib import Path
from typing import Never

from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.recognition.contracts import (
    MODEL,
    CatalogRequest,
    Ledger,
    PilotError,
)
from brickvault_api.recognition.local import (
    approved,
    digest,
    locked,
    prepare,
    private_directory,
    read_bytes,
    read_model,
    write_bytes,
    write_model,
)
from brickvault_api.recognition.pilot import evaluate, execute, export_subset, protocol_digest

ROOT = Path(__file__).resolve().parents[5]
PRIVATE = ROOT / ".local" / "recognition-14a"


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        raise PilotError("invalid_arguments")


def main(args: list[str] | None = None) -> int:
    parser = Parser(
        description="Private Phase 14A pilot. No command defaults to live execution.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "command",
        choices=("init", "prepare", "subset", "draft-approval", "seal", "key", "run", "report"),
    )
    try:
        command = parser.parse_args(args).command
        if not (ROOT / "AGENTS.md").is_file() or not (ROOT / ".git").exists():
            raise PilotError("repository_checkout_required")
        # A future ignore-rule change must not turn credentials into tracked content.
        ignored = subprocess.run(
            ["git", "check-ignore", "--quiet", "--", str(PRIVATE / "api-key.txt")],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        tracked = subprocess.run(
            ["git", "ls-files", "--", str(PRIVATE)], cwd=ROOT, capture_output=True, check=False
        )
        if ignored.returncode or tracked.returncode or tracked.stdout.strip():
            raise PilotError("private_ignored_untracked_directory_required")
        if command == "init":
            PRIVATE.parent.mkdir(mode=0o700, exist_ok=True)
            private_directory(PRIVATE, create=True)
            write_bytes(PRIVATE / "selection.json", b'{"groups": []}\n')
            write_bytes(
                PRIVATE / "catalog-request.json", b'{"snapshot_id": "", "identities": []}\n'
            )
        else:
            private_directory(PRIVATE)
            with locked(PRIVATE):
                if command == "prepare":
                    prepare(PRIVATE)
                elif command == "subset":
                    # Reuse repository-owned development configuration and ownership guards.
                    # No service startup, migration, import, or production configuration path.
                    sys.path.insert(0, str(ROOT / "scripts"))
                    from database import LOCAL, database_marker, instance

                    if not (LOCAL / "development.json").is_file():
                        raise PilotError("development_ownership_required")
                    development = instance("development")
                    development.verify()
                    database = CatalogDatabase(
                        development.target("brickvault_dev", "runtime"),
                        "development",
                        database_marker(development, "development"),
                        "runtime",
                    )
                    request = read_model(PRIVATE / "catalog-request.json", CatalogRequest)
                    write_model(PRIVATE / "subset.json", export_subset(database, request))
                elif command == "draft-approval":
                    draft = {
                        "approved": False,
                        "approved_by": "Brian",
                        "provider": "openai",
                        "model": MODEL,
                        "prepared_sha256": digest(read_bytes(PRIVATE / "prepared.json")),
                        "subset_sha256": digest(read_bytes(PRIVATE / "subset.json")),
                        "protocol_sha256": protocol_digest(),
                        "dollar_cap": "0.25",
                        "max_attempts": 10,
                        "standard_api_retention_accepted": False,
                        "account_data_sharing_disabled_confirmed": False,
                        "selected_photos_and_text_approved": False,
                        "prices_verified_on": "2026-10-02",
                        "expires_on": (date.today() + timedelta(days=7)).isoformat(),
                    }
                    write_bytes(PRIVATE / "approval.json", json.dumps(draft, indent=2).encode())
                elif command == "seal":
                    approved(PRIVATE)
                    # This marker survives a lost/deleted ledger and forbids reinitialization.
                    write_bytes(PRIVATE / "sealed", b"One pilot only. Preserve ledger.\n")
                    write_model(
                        PRIVATE / "ledger.json",
                        Ledger(
                            approval_sha256=digest(read_bytes(PRIVATE / "approval.json")),
                            attempts=[],
                        ),
                    )
                elif command == "key":
                    if not sys.stdin.isatty():
                        raise PilotError("interactive_hidden_input_required")
                    with warnings.catch_warnings():
                        warnings.simplefilter("error", getpass.GetPassWarning)
                        secret = getpass.getpass("OpenAI API key (hidden): ")
                    if not secret.startswith("sk-") or any(c.isspace() for c in secret):
                        raise PilotError("invalid_api_key")
                    write_bytes(PRIVATE / "api-key.txt", secret.encode())
                elif command == "run":
                    if not (PRIVATE / "sealed").is_file():
                        raise PilotError("sealed_approval_required")
                    execute(PRIVATE)
                elif command == "report":
                    print(json.dumps(evaluate(PRIVATE), indent=2))
        if command != "report":
            print(json.dumps({"command": command, "status": "complete"}))
        return 0
    except PilotError as error:
        print(json.dumps({"status": "refused", "code": str(error)}), file=sys.stderr)
        return 1
    except Exception:
        # Even unexpected filesystem/JSON/validation/provider exceptions remain private.
        print(
            '{"status":"refused","detail":"Check private pilot inputs, approval and ledger."}',
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
