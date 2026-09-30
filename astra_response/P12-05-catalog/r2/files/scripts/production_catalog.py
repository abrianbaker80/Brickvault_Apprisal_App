"""Root-only, source-bound production catalog retirement, retry and activation.

Run with the exact reviewed repair-release interpreter. Retirement requires the
predecessor to remain current; retry and activation require the repaired release.
"""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn
from urllib.parse import urlsplit
from uuid import UUID

from brickvault_api import production_admin as admin
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.catalog.fingerprint import IMPORTER_VERSION
from brickvault_api.catalog.importer import import_source
from brickvault_api.catalog.models import CATALOG_TABLES
from brickvault_api.catalog.ownership import import_lock
from brickvault_api.catalog.promotion import activate
from brickvault_api.catalog.recovery import (
    admit_retry,
    failed_run,
    metadata_guard,
    recover_failed,
)
from brickvault_api.persistence.database import expected_revisions
from brickvault_api.providers.rebrickable.parser import Parser
from brickvault_api.providers.rebrickable.source import (
    Manifest,
    SourceArea,
    digest,
    load_manifest,
)
from psycopg import sql

APPROVAL = Path("/etc/brickvault/production-catalog.json")
REPAIR_APPROVAL = Path("/etc/brickvault/production-catalog-repair.json")
SOURCE_ROOT = Path("/var/lib/brickvault-catalog-source")
MANIFEST = SOURCE_ROOT / "manifest.json"
OPERATIONS_LOCK = Path("/run/brickvault-backup-retention.lock")
RELEASE = Path("/opt/brickvault/releases/p12-05-catalog-repair-r1")
PREDECESSOR_RELEASE = Path("/opt/brickvault/releases/p12-04e-r6")
PREDECESSOR_MANIFEST_SHA256 = (
    "9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d"
)
SOURCE_VERSION = "official-aa9a32c8fa634132b0c737680027853c"
SOURCE_MANIFEST_SHA256 = (
    "c4518012ab3c41da9538e08362bdb2294df9192b977496b6f18853b39da3c9ad"
)
SOURCE_PROVENANCE_SHA256 = (
    "619af89bce55b040d2d745541793c33254e559a883b94ec6c9ab61d644e17f15"
)
KNOWN_SET = "75331-1"
CONFLICT_UNITS = (
    "brickvault-backup.service",
    "brickvault-retention.service",
    "certbot.service",
    "apt-daily.service",
    "apt-daily-upgrade.service",
    "brickvault-python-version.service",
    "brickvault-health.service",
    "brickvault-health-deep.service",
)


@dataclass(frozen=True)
class ApprovedSource:
    area: SourceArea
    manifest: Manifest
    paths: dict[str, Path]


def approve(raw: bytes, manifest: Manifest, manifest_raw: bytes) -> None:
    value = admin._parse_json(raw)
    fields = {
        "purpose",
        "database",
        "provider",
        "synthetic",
        "scope",
        "source_version",
        "manifest_sha256",
        "provenance_sha256",
        "importer_version",
        "permitted_use_reference",
        "rights_limitations",
        "classification",
        "known_set",
    }
    if set(value) != fields:
        raise admin.AdminError("Unexpected source approval fields.")
    fixed = {
        "purpose": "production",
        "database": admin.DATABASE,
        "provider": "rebrickable",
        "synthetic": False,
        "scope": "full-catalog",
        "source_version": manifest.source_version,
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "provenance_sha256": digest(manifest.provenance()),
        "importer_version": IMPORTER_VERSION,
        "classification": "official-nonsynthetic",
        "known_set": KNOWN_SET,
    }
    if any(
        value[key] != expected or type(value[key]) is not type(expected)
        for key, expected in fixed.items()
    ):
        raise admin.AdminError("Source approval does not match the exact manifest.")
    reference = value["permitted_use_reference"]
    limitations = value["rights_limitations"]
    if not isinstance(reference, str) or len(reference) > 2048:
        raise admin.AdminError("Official rights reference is required.")
    url = urlsplit(reference)
    if (
        (url.scheme, url.netloc, url.path)
        not in {
            ("https", "rebrickable.com", "/downloads/"),
            ("https", "rebrickable.com", "/terms/"),
        }
        or url.query
        or url.fragment
    ):
        raise admin.AdminError("Unreviewed rights reference.")
    if (
        type(limitations) is not list
        or not 1 <= len(limitations) <= 10
        or any(
            type(item) is not str
            or not 1 <= len(item) <= 512
            or any(ord(char) < 32 for char in item)
            for item in limitations
        )
    ):
        raise admin.AdminError("Explicit bounded rights limitations are required.")
    if (
        manifest.synthetic
        or manifest.provider != "rebrickable"
        or manifest.scope != "full-catalog"
        or manifest.profile_version != "rebrickable-bulk-v3-2d.1"
        or not manifest.source_version.startswith("official-")
        or any(
            word in manifest.source_version.lower()
            for word in ("fixture", "synthetic", "test")
        )
        or manifest.acquisition_method != "offline-approved-acquisition"
        or any(
            source.source_url is None or source.downloaded_at is None
            for source in manifest.files
        )
    ):
        raise admin.AdminError(
            "Only approved official nonsynthetic bulk sources are supported."
        )


def protected_source_file(path: Path) -> None:
    for parent in (path.parent, *path.parent.parents):
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise admin.AdminError("Unsafe source directory.")
    info = path.lstat()
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != 0
        or info.st_nlink != 1
        or stat.S_IMODE(info.st_mode) not in (0o400, 0o600)
    ):
        raise admin.AdminError("Unsafe protected source file.")


def load_source() -> ApprovedSource:
    admin._require_root()
    protected_source_file(APPROVAL)
    approval_raw = admin._protected_file(APPROVAL)
    protected_source_file(MANIFEST)
    manifest_raw = admin._protected_file(MANIFEST)
    area = SourceArea(SOURCE_ROOT)
    manifest, paths = load_manifest(area, str(MANIFEST))
    approve(approval_raw, manifest, manifest_raw)
    for path in paths.values():
        protected_source_file(path)
    return ApprovedSource(area, manifest, paths)


def parse_source(source: ApprovedSource) -> dict[str, int]:
    counts = {}
    known = 0
    for item in source.manifest.files:
        parser = Parser(source.area, item, source.paths[item.dataset], synthetic=False)
        for row in parser.rows():
            if item.dataset == "sets" and row.values["set_num"] == KNOWN_SET:
                known += 1
        if not parser.complete:
            raise admin.AdminError("Source parsing did not reach verified EOF.")
        counts[item.dataset] = parser.count
    if known != 1 or counts["sets"] == 0:
        raise admin.AdminError("Required exact known set is absent or ambiguous.")
    return counts


@contextmanager
def operations_lock() -> Iterator[None]:
    import fcntl

    descriptor = os.open(OPERATIONS_LOCK, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != 0
            or info.st_nlink != 1
            or stat.S_IMODE(info.st_mode) != 0o600
        ):
            raise admin.AdminError("Unsafe operations lock.")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(descriptor)


def approve_repair_release(raw: bytes, manifest: Manifest, manifest_raw: bytes) -> str:
    """The post-build release digest is detached from the package it approves."""
    value = admin._parse_json(raw)
    fixed = {
        "purpose": "production",
        "database": admin.DATABASE,
        "release_id": RELEASE.name,
        "predecessor_release_id": PREDECESSOR_RELEASE.name,
        "predecessor_release_manifest_sha256": PREDECESSOR_MANIFEST_SHA256,
        "source_version": SOURCE_VERSION,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "source_provenance_sha256": SOURCE_PROVENANCE_SHA256,
        "migration_head": "0016_hunt_cached_runs",
    }
    if set(value) != {*fixed, "release_manifest_sha256"} or any(
        type(value[key]) is not str or value[key] != expected
        for key, expected in fixed.items()
    ):
        raise admin.AdminError("Repair approval authority does not match.")
    reviewed = value["release_manifest_sha256"]
    if (
        type(reviewed) is not str
        or len(reviewed) != 64
        or any(char not in "0123456789abcdef" for char in reviewed)
        or manifest.source_version != SOURCE_VERSION
        or digest(manifest.provenance()) != SOURCE_PROVENANCE_SHA256
        or hashlib.sha256(manifest_raw).hexdigest() != SOURCE_MANIFEST_SHA256
    ):
        raise admin.AdminError("Repair approval source or release digest differs.")
    return reviewed


def operations_guard(command: str, source: ApprovedSource) -> None:
    protected_source_file(REPAIR_APPROVAL)
    reviewed = approve_repair_release(
        admin._protected_file(REPAIR_APPROVAL),
        source.manifest,
        admin._protected_file(MANIFEST),
    )
    current = Path("/opt/brickvault/current").resolve(strict=True)
    expected_current = PREDECESSOR_RELEASE if command == "recover-failed" else RELEASE
    if (
        current != expected_current
        or Path(sys.prefix).resolve(strict=True) != RELEASE / "api/venv"
        or expected_revisions() != ("0016_hunt_cached_runs",)
        or hashlib.sha256((RELEASE / "manifest.json").read_bytes()).hexdigest()
        != reviewed
        or (
            command == "recover-failed"
            and hashlib.sha256(
                (PREDECESSOR_RELEASE / "manifest.json").read_bytes()
            ).hexdigest()
            != PREDECESSOR_MANIFEST_SHA256
        )
    ):
        raise admin.AdminError("Installed release or migration contract changed.")
    for unit in CONFLICT_UNITS:
        result = subprocess.run(
            ["/usr/bin/systemctl", "show", "--property=ActiveState", "--value", unit],
            capture_output=True,
            timeout=10,
            check=False,
        )
        if result.returncode or result.stdout.strip() != b"inactive":
            raise admin.AdminError("Conflicting or ambiguous maintenance job.")


def table_counts(connection: CatalogConnection) -> dict[str, int]:
    counts = {}
    for name in CATALOG_TABLES:
        row = connection.execute(
            sql.SQL("SELECT count(*) AS n FROM public.{}").format(sql.Identifier(name))
        ).fetchone()
        if row is None:
            raise admin.AdminError("Catalog counts unavailable.")
        counts[name] = row["n"]
    return counts


def require_empty(counts: dict[str, int]) -> None:
    if any(counts.values()):
        raise admin.AdminError("First import requires wholly empty catalog history.")


def candidate_guard(
    connection: CatalogConnection,
    source: ApprovedSource,
    snapshot: UUID,
    receipt: UUID | None = None,
) -> dict[str, Any]:
    counts = table_counts(connection)
    expected = {
        "catalog_provider": 1,
        "catalog_source_version": 1,
        "catalog_source_file": 12,
        "catalog_import_run": counts["catalog_import_run"],
        "catalog_snapshot": 1,
        "catalog_snapshot_validation": 1,
        "catalog_active_snapshot": 1,
    }
    if (
        counts["catalog_import_run"] not in (1, 2)
        or any(counts[name] != n for name, n in expected.items())
        or counts["catalog_set_fact"] < 1
    ):
        raise admin.AdminError("Partial or competing catalog state.")
    row = connection.execute(
        """SELECT s.state,s.source_version_id,s.validation_digest,s.semantic_fingerprint,v.manifest_digest,v.synthetic,
        v.source_metadata->>'source_version' AS source_version,p.code,r.status,r.stage,r.counts,
        a.snapshot_id,a.generation,a.activation_id,s.scope,r.predecessor_id,r.id AS run_id
        FROM catalog_snapshot s JOIN catalog_source_version v ON v.id=s.source_version_id
        JOIN catalog_provider p ON p.id=v.provider_id JOIN catalog_import_run r ON r.id=s.import_run_id
        JOIN catalog_active_snapshot a ON a.provider_id=p.id AND a.scope=s.scope WHERE s.id=%s""",
        (snapshot,),
    ).fetchone()
    if (
        row is None
        or row["code"] != "rebrickable"
        or row["synthetic"] is not False
        or row["scope"] != source.manifest.scope
        or row["manifest_digest"] != digest(source.manifest.provenance())
        or row["source_version"] != source.manifest.source_version
        or row["status"] != "succeeded"
    ):
        raise admin.AdminError("Candidate does not match the approved source.")
    predecessor = row.get("predecessor_id")
    if predecessor is None:
        if counts["catalog_import_run"] != 1:
            raise admin.AdminError("Unbound competing import history.")
    else:
        if counts["catalog_import_run"] != 2:
            raise admin.AdminError("Retry history is not exact.")
        prior = failed_run(
            connection, row["source_version_id"], predecessor, source.manifest
        )
        retired = metadata_guard(prior, source.manifest)
        if row["semantic_fingerprint"] != retired["candidate"]["semantic_fingerprint"]:
            raise admin.AdminError(
                "Retry fingerprint does not match the retired source."
            )
        for dataset in source.paths:
            old = connection.execute(
                sql.SQL("SELECT count(*) AS n FROM public.{} WHERE run_id=%s").format(
                    sql.Identifier("catalog_stage_" + dataset)
                ),
                (predecessor,),
            ).fetchone()
            if old is None or old["n"] != 0:
                raise admin.AdminError("Retired staging unexpectedly remains.")
    fresh = (
        row["state"],
        row["stage"],
        row["snapshot_id"],
        row["generation"],
        row["activation_id"],
    )
    if fresh != ("validated", "validated", None, 0, None):
        if (
            receipt is None
            or fresh != ("accepted", "accepted", snapshot, 1, receipt)
            or counts["catalog_activation"] != 1
        ):
            raise admin.AdminError("Unexpected activation state or receipt.")
    elif counts["catalog_activation"]:
        raise admin.AdminError("Unexpected activation history.")
    return row


def execute(
    command: str,
    snapshot: UUID | None = None,
    receipt: UUID | None = None,
    run: UUID | None = None,
    candidate: UUID | None = None,
    predecessor: UUID | None = None,
) -> dict[str, Any]:
    if command not in (
        "preflight",
        "import",
        "activate",
        "recover-failed",
        "retry-import",
    ):
        raise admin.AdminError("Unreviewed catalog command.")
    config = admin._load_config(admin.CONFIG_PATH)
    source = load_source()
    with operations_lock():
        operations_guard(command, source)
        admin.verify(config)
        database = CatalogDatabase(
            config.owner_url, "production", config.marker, "owner"
        )
        with database.connect() as connection:
            if command in ("preflight", "import"):
                require_empty(table_counts(connection))
            elif command == "activate" and snapshot is not None:
                candidate_guard(connection, source, snapshot, receipt)
            elif command not in ("recover-failed", "retry-import"):
                raise admin.AdminError("Exact candidate and receipt are required.")
        if command == "recover-failed":
            if run is None or candidate is None:
                raise admin.AdminError(
                    "Exact failed attempt and candidate are required."
                )
            return recover_failed(
                database, source.manifest, parse_source(source), run, candidate
            )
        if command == "retry-import":
            if predecessor is None:
                raise admin.AdminError("Exact recovered predecessor is required.")
            # The importer repeats admission inside its exclusive provider lock.
            # This early check avoids reparsing when retirement has not occurred.
            with (
                database.connect() as connection,
                import_lock(connection, "rebrickable"),
                connection.transaction(),
            ):
                admit_retry(connection, source.manifest, predecessor)
            source_counts = parse_source(source)
            report = import_source(
                database, source.area, str(MANIFEST), predecessor_id=predecessor
            )
            if (
                report.get("state") != "passed"
                or report.get("dataset_counts") != source_counts
            ):
                raise admin.AdminError(
                    "Retry did not produce a validated exact source."
                )
            with database.connect() as connection:
                candidate_guard(connection, source, UUID(report["candidate_snapshot"]))
            return report
        if command in ("preflight", "import"):
            counts = parse_source(source)
            if command == "preflight":
                return {
                    "state": "preflight_passed",
                    "dataset_counts": counts,
                    "manifest_digest": digest(source.manifest.provenance()),
                }
            report = import_source(database, source.area, str(MANIFEST))
            if (
                report.get("state") != "passed"
                or report.get("dataset_counts") != counts
            ):
                raise admin.AdminError(
                    "Import did not produce a fully validated exact source."
                )
            candidate = UUID(report["candidate_snapshot"])
            with database.connect() as connection:
                candidate_guard(connection, source, candidate)
            return report
        if snapshot is None or receipt is None:
            raise admin.AdminError("Exact candidate and receipt are required.")
        result = activate(database, snapshot, None, 0, receipt)
        with database.connect() as connection:
            candidate_guard(connection, source, snapshot, receipt)
        admin.verify(config)
        return result


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise admin.AdminError("Invalid catalog administration arguments.")


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(
        dest="command", required=True, parser_class=SafeParser
    )
    commands.add_parser("preflight", allow_abbrev=False)
    commands.add_parser("import", allow_abbrev=False)
    activation = commands.add_parser("activate", allow_abbrev=False)
    activation.add_argument("--snapshot", required=True, type=UUID)
    activation.add_argument("--receipt", required=True, type=UUID)
    recovery = commands.add_parser("recover-failed", allow_abbrev=False)
    recovery.add_argument("--run", required=True, type=UUID)
    recovery.add_argument("--candidate", required=True, type=UUID)
    retry = commands.add_parser("retry-import", allow_abbrev=False)
    retry.add_argument("--predecessor", required=True, type=UUID)
    try:
        options = parser.parse_args(argv)
        result = execute(
            options.command,
            getattr(options, "snapshot", None),
            getattr(options, "receipt", None),
            getattr(options, "run", None),
            getattr(options, "candidate", None),
            getattr(options, "predecessor", None),
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception:  # noqa: BLE001 - paths, source rows and underlying driver errors stay private.
        print(
            "Production catalog operation refused; inspect protected local state.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print("Production catalog operation interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
