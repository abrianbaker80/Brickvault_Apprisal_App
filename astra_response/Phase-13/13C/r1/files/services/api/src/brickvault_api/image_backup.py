"""Paused, snapshot-bound image capture and strictly checked disposable extraction."""

import hashlib
import io
import json
import os
import signal
import stat
import subprocess
import sys
import tarfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, text

from brickvault_api.images.storage import FilesystemBlobStore, key_for

STATE = Path("/run/brickvault-image-capture")
JOURNAL = STATE / "pause.json"
UNITS = ("brickvault-health.timer", "brickvault-health-deep.timer", "brickvault-api.service")
IMAGE_TABLES = (
    "listing",
    "blob",
    "image_asset",
    "image_relation",
    "listing_image",
    "upload_receipt",
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()


def security_inventory(connection: Connection) -> dict[str, Any]:
    queries = {
        "roles": "SELECT rolname,rolsuper,rolinherit,rolcreaterole,rolcreatedb,rolcanlogin,rolreplication,rolbypassrls,rolconnlimit,rolvaliduntil FROM pg_roles WHERE rolname IN ('brickvault_appraisal_prod_owner','brickvault_appraisal_prod_runtime') ORDER BY rolname",
        "memberships": "SELECT roleid::regrole::text AS role,member::regrole::text AS member,admin_option FROM pg_auth_members WHERE roleid IN (SELECT oid FROM pg_roles WHERE rolname IN ('brickvault_appraisal_prod_owner','brickvault_appraisal_prod_runtime')) OR member IN (SELECT oid FROM pg_roles WHERE rolname IN ('brickvault_appraisal_prod_owner','brickvault_appraisal_prod_runtime')) ORDER BY 1,2",
        "database": "SELECT datname,pg_get_userbyid(datdba) AS owner,coalesce(datacl,acldefault('d',datdba))::text AS acl FROM pg_database WHERE datname=current_database()",
        "schemas": "SELECT nspname,pg_get_userbyid(nspowner) AS owner,coalesce(nspacl,acldefault('n',nspowner))::text AS acl FROM pg_namespace WHERE nspname='public' ORDER BY 1",
        "columns": "SELECT c.relname,a.attname,a.attacl::text AS acl FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND a.attacl IS NOT NULL ORDER BY 1,2",
        "functions": "SELECT p.proname,pg_get_function_identity_arguments(p.oid) AS args,pg_get_userbyid(p.proowner) AS owner,coalesce(p.proacl,acldefault('f',p.proowner))::text AS acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' ORDER BY 1,2",
        "defaults": "SELECT pg_get_userbyid(defaclrole) AS role,defaclobjtype,defaclacl::text AS acl FROM pg_default_acl ORDER BY 1,2,3",
    }
    result = {}
    for name, query in queries.items():
        rows = [dict(r) for r in connection.execute(text(query)).mappings()]
        for row in rows:
            if "acl" in row:
                row["acl"] = sorted(row["acl"].strip("{}").split(","))
        result[name] = rows
    return result


def database_inventory(connection: Connection) -> dict[str, Any]:
    tables = (
        connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        )
        .scalars()
        .all()
    )
    counts = {
        name: connection.scalar(
            text('SELECT count(*) FROM public."' + name.replace('"', '""') + '"')
        )
        for name in tables
    }
    rows = {
        name: [
            dict(r)
            for r in connection.execute(text(f"SELECT * FROM public.{name} ORDER BY id")).mappings()
        ]
        for name in IMAGE_TABLES
    }
    objects = [
        dict(r)
        for r in connection.execute(
            text(
                "SELECT c.relname,c.relkind,pg_get_userbyid(c.relowner) AS owner,"
                "coalesce(c.relacl,acldefault(CASE WHEN c.relkind='S' THEN 'S'::\"char\" ELSE 'r'::\"char\" END,c.relowner))::text AS acl "
                "FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='public' ORDER BY c.relname,c.relkind"
            )
        ).mappings()
    ]
    for row in objects:
        row["acl"] = sorted(row["acl"].strip("{}").split(","))
    return {
        "counts": counts,
        "security": security_inventory(connection),
        "context": {
            name: hashlib.sha256(
                canonical(
                    [
                        dict(r)
                        for r in connection.execute(
                            text(f"SELECT * FROM public.{name} t ORDER BY row_to_json(t)::text")
                        ).mappings()
                    ]
                )
            ).hexdigest()
            for name in (
                "catalog_active_snapshot",
                "catalog_activation",
                "catalog_import_run",
                "auth_principal",
                "application_settings",
                "watchlist_item",
            )
        },
        "image_tables": {
            name: hashlib.sha256(canonical(values)).hexdigest() for name, values in rows.items()
        },
        "objects": objects,
        "blobs": [{k: r[k] for k in ("sha256", "storage_key", "byte_count")} for r in rows["blob"]],
    }


def configured_root() -> Path:
    from brickvault_api import production_admin as admin

    raw = admin._protected_file(Path("/etc/brickvault/api.env")).decode()
    values = [
        line.split("=", 1)[1]
        for line in raw.splitlines()
        if line.startswith("BVA_IMAGE_BLOB_ROOT=")
    ]
    if len(values) != 1 or not values[0].startswith("/"):
        raise ValueError("Private image root is absent.")
    root = Path(values[0])
    if root != root.resolve(strict=True) or not root.is_dir():
        raise ValueError("Private image root is unsafe.")
    for forbidden in (Path("/var/lib/postgresql/18/main"), Path("/opt/brickvault")):
        if root.is_relative_to(forbidden):
            raise ValueError("Private image root overlaps protected storage.")
    info = root.stat()
    if stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError("Private image root permissions differ.")
    return root


def systemctl(*arguments: str) -> str:
    r = subprocess.run(
        ["/usr/bin/systemctl", *arguments], capture_output=True, timeout=180, check=False
    )
    if r.returncode:
        raise RuntimeError("Image capture service control failed.")
    return r.stdout.decode().strip()


def resume() -> None:
    if not JOURNAL.exists():
        return
    from brickvault_api import production_admin as admin

    value = dict(admin._parse_json(admin._protected_file(JOURNAL)))
    if (
        set(value) != {"pid", "active"}
        or type(value["pid"]) is not int
        or type(value["active"]) is not list
    ):
        raise ValueError("Invalid image pause journal.")
    if len(value["active"]) != len(set(value["active"])) or any(
        u not in UNITS for u in value["active"]
    ):
        raise ValueError("Invalid image pause units.")
    if value["pid"] != os.getpid() and Path(f"/proc/{value['pid']}").exists():
        raise ValueError("Image capture is still running.")
    for unit in reversed(value["active"]):
        systemctl("start", unit)
    JOURNAL.unlink()


@contextmanager
def maintenance_pause() -> Iterator[None]:
    from brickvault_api import production_admin as admin

    admin._require_root()
    STATE.mkdir(mode=0o700, exist_ok=True)
    info = STATE.lstat()
    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != 0
        or stat.S_IMODE(info.st_mode) != 0o700
        or JOURNAL.exists()
    ):
        raise ValueError("Image capture state needs operator review.")
    for unit in ("brickvault-health.service", "brickvault-health-deep.service"):
        if systemctl("show", unit, "--property=ActiveState", "--value") not in (
            "inactive",
            "failed",
        ):
            raise ValueError("Health operation conflicts with image capture.")
    active = []
    for unit in UNITS:
        state = systemctl("show", unit, "--property=ActiveState", "--value")
        if state not in ("active", "inactive"):
            raise ValueError("Service transition conflicts with image capture.")
        if state == "active":
            active.append(unit)
    fd = os.open(JOURNAL, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as output:
        output.write(canonical({"pid": os.getpid(), "active": active}))
        output.flush()
        os.fsync(output.fileno())
    previous = signal.getsignal(signal.SIGTERM)

    def interrupted(_signal: int, _frame: Any) -> None:
        raise InterruptedError("Image capture interrupted.")

    signal.signal(signal.SIGTERM, interrupted)
    try:
        for unit in active:
            systemctl("stop", unit)
        if systemctl("show", "brickvault-api.service", "--property=MainPID", "--value") != "0":
            raise ValueError("Image uploads have not settled.")
        yield
    finally:
        signal.signal(signal.SIGTERM, previous)
        resume()


def validate_inventory(value: Any) -> list[dict[str, Any]]:
    if (
        type(value) is not dict
        or set(value) != {"schema", "revisions", "database"}
        or value["schema"] != 1
        or value["revisions"] != ["0017_listing_images"]
    ):
        raise ValueError("Invalid image inventory format.")
    database = value["database"]
    if (
        type(database) is not dict
        or set(database) != {"counts", "image_tables", "objects", "blobs", "security", "context"}
        or type(database["blobs"]) is not list
    ):
        raise ValueError("Invalid image inventory.")
    rows = database["blobs"]
    seen = set()
    for row in rows:
        if (
            type(row) is not dict
            or set(row) != {"sha256", "storage_key", "byte_count"}
            or type(row["byte_count"]) is not int
            or row["byte_count"] <= 0
        ):
            raise ValueError("Invalid inventory blob.")
        if (
            type(row["sha256"]) is not str
            or row["storage_key"] != key_for(row["sha256"])
            or row["sha256"] in seen
        ):
            raise ValueError("Invalid inventory key.")
        seen.add(row["sha256"])
    return rows


def write_archive(inventory: Path, root: Path) -> None:
    raw = inventory.read_bytes()
    rows = validate_inventory(json.loads(raw))
    store = FilesystemBlobStore(root)
    with tarfile.open(fileobj=sys.stdout.buffer, mode="w|") as archive:
        member = tarfile.TarInfo("inventory.json")
        member.size = len(raw)
        member.mode = 0o600
        archive.addfile(member, io.BytesIO(raw))
        for row in rows:
            verified = store.stat(row["sha256"])
            if verified.byte_count != row["byte_count"]:
                raise ValueError("Inventory bytes differ.")
            member = tarfile.TarInfo(row["storage_key"])
            member.size = verified.byte_count
            member.mode = 0o600
            with store.read(row["sha256"]) as source:
                archive.addfile(member, source)


def extract_archive(archive_path: Path, destination: Path) -> dict[str, Any]:
    # Destination must be newly task-owned; no production default or overwrite mode.
    if (
        not destination.is_absolute()
        or destination.exists()
        or destination != destination.parent.resolve() / destination.name
    ):
        raise ValueError("Recovery destination must be new and absolute.")
    if any(
        destination.is_relative_to(p)
        for p in (Path("/var/lib/postgresql"), Path("/opt/brickvault"))
    ):
        raise ValueError("Recovery destination overlaps production.")
    destination.mkdir(mode=0o700)
    with tarfile.open(archive_path, mode="r|") as archive:
        member = archive.next()
        if (
            member is None
            or member.name != "inventory.json"
            or not member.isfile()
            or member.size > 16 * 1024**2
        ):
            raise ValueError("Recovery inventory is absent.")
        source = archive.extractfile(member)
        assert source is not None
        value = json.loads(source.read())
        rows = {r["storage_key"]: r for r in validate_inventory(value)}
        seen: set[str] = set()
        while (member := archive.next()) is not None:
            if (
                not member.isfile()
                or member.name not in rows
                or member.name in seen
                or member.size != rows[member.name]["byte_count"]
            ):
                raise ValueError("Unexpected recovery archive member.")
            path = destination / member.name
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            source = archive.extractfile(member)
            assert source is not None
            digest = hashlib.sha256()
            with path.open("xb") as output:
                os.chmod(path, 0o600)
                while chunk := source.read(1024 * 1024):
                    digest.update(chunk)
                    output.write(chunk)
            if digest.hexdigest() != rows[member.name]["sha256"]:
                raise ValueError("Recovery blob digest differs.")
            seen.add(member.name)
        if seen != set(rows):
            raise ValueError("Recovery archive is incomplete.")
    return value


def main() -> int:
    try:
        if sys.argv[1:] == ["resume"]:
            resume()
        elif len(sys.argv) == 4 and sys.argv[1] == "archive":
            write_archive(Path(sys.argv[2]), Path(sys.argv[3]))
        else:
            raise ValueError("Invalid image backup command.")
    except Exception:  # noqa: BLE001 - private metadata is never logged.
        print("IMAGE_BACKUP_FAILED", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
