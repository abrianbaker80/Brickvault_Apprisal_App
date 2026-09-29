"""Guarded, interactive administration of the dedicated production database.

The protected input and recovery receipt are deliberately absent from a new
installation. Provisioning and migration are explicit later operations.
"""

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import sys
import warnings
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, NoReturn

import psycopg
from alembic import command
from psycopg import sql
from psycopg.rows import dict_row
from sqlalchemy import Connection, text

from brickvault_api.auth import AuthService, password_valid
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.persistence.database import (
    create_database_engine,
    expected_revisions,
    migration_config,
)
from brickvault_api.persistence.runtime_grants import grant_runtime
from brickvault_api.settings import reject_pg_environment, validate_target

DATABASE = "brickvault_appraisal_prod"
OWNER = "brickvault_appraisal_prod_owner"
RUNTIME = "brickvault_appraisal_prod_runtime"
CONFIG_PATH = Path("/etc/brickvault/production-admin.json")
SOCKET = "/var/run/postgresql"
PORT = 5432
MARKER = re.compile(r"brickvault-appraisal:[a-f0-9]{32}:[a-f0-9]{32}\Z")
SNAPSHOT = re.compile(r"[a-f0-9]{64}\Z")
_CREDENTIAL_LOGGING = {
    "log_statement": "none",
    "log_min_error_statement": "panic",
    "log_min_messages": "panic",
    "log_min_duration_statement": "-1",
    "log_min_duration_sample": "-1",
    "log_transaction_sample_rate": "0",
    "log_statement_sample_rate": "0",
    "log_duration": "off",
    "log_parameter_max_length": "0",
    "log_parameter_max_length_on_error": "0",
    "log_error_verbosity": "terse",
    "debug_print_parse": "off",
    "debug_print_rewritten": "off",
    "debug_print_plan": "off",
    "track_activities": "off",
    "log_statement_stats": "off",
    "log_parser_stats": "off",
    "log_planner_stats": "off",
    "log_executor_stats": "off",
}


class AdminError(RuntimeError):
    """Safe failure category; the CLI never prints underlying driver exceptions."""


@dataclass(frozen=True)
class AdminConfig:
    owner_url: str = field(repr=False)
    runtime_url: str = field(repr=False)
    marker: str = field(repr=False)


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AdminError("Duplicate protected configuration key.")
        result[key] = value
    return result


def _parse_json(raw: bytes) -> Mapping[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_object_pairs)
    except (UnicodeError, ValueError) as exc:
        raise AdminError("Invalid protected JSON.") from exc
    if type(value) is not dict:
        raise AdminError("Protected input must be an object.")
    return value


def parse_config(raw: bytes) -> AdminConfig:
    """Validate exact production identity before any connection or mutation."""
    value = _parse_json(raw)
    if set(value) != {"purpose", "database", "owner_url", "runtime_url", "ownership_marker"}:
        raise AdminError("Unexpected production configuration fields.")
    if value["purpose"] != "production" or value["database"] != DATABASE:
        raise AdminError("Incorrect production purpose or database.")
    if any(type(value[key]) is not str for key in ("owner_url", "runtime_url", "ownership_marker")):
        raise AdminError("Invalid production descriptor type.")
    owner = validate_target(value["owner_url"], "production", "owner")
    runtime = validate_target(value["runtime_url"], "production", "runtime")
    if (
        owner.username != OWNER
        or runtime.username != RUNTIME
        or owner.database != DATABASE
        or runtime.database != DATABASE
        or owner.port != PORT
        or runtime.port != PORT
        or owner.password == runtime.password
        or MARKER.fullmatch(value["ownership_marker"]) is None
    ):
        raise AdminError("Production database identity does not match the approved contract.")
    return AdminConfig(value["owner_url"], value["runtime_url"], value["ownership_marker"])


def _protected_file(path: Path) -> bytes:
    """Read one root-owned regular file without following a final-component symlink."""
    get_euid = getattr(os, "geteuid", None)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    closexec = getattr(os, "O_CLOEXEC", 0)
    if (
        not path.is_absolute()
        or os.name != "posix"
        or get_euid is None
        or get_euid() != 0
        or not nofollow
    ):
        raise AdminError("Root and an absolute protected input path are required.")
    for parent in (path.parent, *path.parent.parents):
        status = parent.lstat()
        if not stat.S_ISDIR(status.st_mode) or status.st_uid != 0 or status.st_mode & 0o022:
            raise AdminError("Protected input directory is unsafe.")
    descriptor = os.open(path, os.O_RDONLY | nofollow | closexec)
    try:
        status = os.fstat(descriptor)
        if (
            not stat.S_ISREG(status.st_mode)
            or status.st_uid != 0
            or stat.S_IMODE(status.st_mode) not in (0o400, 0o600)
            or status.st_size > 16 * 1024
        ):
            raise AdminError("Protected input file is unsafe.")
        with os.fdopen(descriptor, "rb", closefd=False) as source:
            content = source.read(16 * 1024 + 1)
            if len(content) > 16 * 1024:
                raise AdminError("Protected input file is too large.")
            return content
    finally:
        os.close(descriptor)


def _load_config(path: Path) -> AdminConfig:
    reject_pg_environment()
    if any(key.startswith("BVA_") for key in os.environ):
        raise AdminError("Runtime environment must not enter administration.")
    return parse_config(_protected_file(path))


def _role_marker(config: AdminConfig) -> str:
    return config.marker + ":role"


def _require_root() -> None:
    get_euid = getattr(os, "geteuid", None)
    if os.name != "posix" or get_euid is None or get_euid() != 0:
        raise AdminError("Production peer maintenance requires OS root.")


@contextmanager
def _maintenance() -> Iterator[psycopg.Connection[dict[str, Any]]]:
    """Use only the reviewed root-to-postgres peer map and local Unix socket."""
    reject_pg_environment()
    _require_root()
    with psycopg.connect(
        host=SOCKET,
        port=PORT,
        dbname="postgres",
        user="postgres",
        row_factory=dict_row,
        autocommit=True,
        connect_timeout=2,
        sslmode="disable",
        gssencmode="disable",
        application_name="brickvault-production-admin",
    ) as connection:
        row = connection.execute(
            "SELECT current_user AS role, session_user AS login, "
            "current_database() AS database, inet_server_addr() IS NULL AS socket, "
            "current_setting('server_version_num')::integer AS version, "
            "current_setting('listen_addresses') AS listen, "
            "current_setting('port')::integer AS port, "
            "pg_is_in_recovery() AS recovery"
        ).fetchone()
        validate_maintenance_session(row)
        yield connection


def validate_maintenance_session(
    row: Mapping[str, Any] | None, expected_database: str = "postgres"
) -> None:
    if (
        row is None
        or row.get("role") != "postgres"
        or row.get("login") != "postgres"
        or row.get("database") != expected_database
        or row.get("socket") is not True
        or row.get("listen") != "127.0.0.1"
        or row.get("port") != PORT
        or row.get("recovery") is not False
        or type(row.get("version")) is not int
        or not 180000 <= row["version"] < 190000
    ):
        raise AdminError("Maintenance session is not the approved local PostgreSQL 18 cluster.")


def _credential_session_guard(connection: psycopg.Connection[dict[str, Any]]) -> int:
    """Refuse credential SQL unless this session cannot expose statements in normal logs.

    PostgreSQL 18 documents both statement logging and error-statement logging
    as possible secret disclosures. Client-generated SCRAM still carries a
    verifier in SQL, so disable all standard statement and query observability
    paths before sending it, then read back the effective settings.
    """
    preloads = connection.execute(
        "SELECT current_setting('shared_preload_libraries') AS shared,"
        "current_setting('session_preload_libraries') AS session,"
        "current_setting('local_preload_libraries') AS local"
    ).fetchone()
    if preloads != {"shared": "", "session": "", "local": ""}:
        raise AdminError(
            "Unreviewed PostgreSQL preload library prevents credential administration."
        )
    for name, value in _CREDENTIAL_LOGGING.items():
        connection.execute(sql.SQL("SET {} = {}").format(sql.Identifier(name), sql.Literal(value)))
    _verify_credential_logging(connection)
    password_settings = connection.execute(
        "SELECT current_setting('password_encryption') AS encryption,"
        "current_setting('scram_iterations')::integer AS iterations"
    ).fetchone()
    if (
        password_settings is None
        or password_settings["encryption"] != "scram-sha-256"
        or type(password_settings["iterations"]) is not int
        or not 4096 <= password_settings["iterations"] <= 1000000
    ):
        raise AdminError("PostgreSQL SCRAM settings are outside the reviewed range.")
    return password_settings["iterations"]


def _verify_credential_logging(connection: psycopg.Connection[dict[str, Any]]) -> None:
    settings = connection.execute(
        "SELECT name,setting FROM pg_settings WHERE name = ANY(%s)",
        (list(_CREDENTIAL_LOGGING),),
    ).fetchall()
    effective = {row["name"]: row["setting"].lower() for row in settings}
    if effective != _CREDENTIAL_LOGGING:
        raise AdminError("Credential-session logging controls did not take effect.")


def _scram_verifier(password: str, iterations: int, salt: bytes) -> str:
    """Build PostgreSQL's RFC 5803 SCRAM-SHA-256 secret on the client.

    Production passwords are canonical ASCII hex, so SASLprep is the identity
    transformation. The cleartext password never enters a SQL statement.
    """
    if (
        re.fullmatch(r"[a-f0-9]{64}", password) is None
        or not 4096 <= iterations <= 1000000
        or len(salt) != 16
    ):
        raise AdminError("Invalid SCRAM credential input.")
    salted = hashlib.pbkdf2_hmac("sha256", password.encode("ascii"), salt, iterations)
    client_key = hmac.new(salted, b"Client Key", hashlib.sha256).digest()
    stored_key = hashlib.sha256(client_key).digest()
    server_key = hmac.new(salted, b"Server Key", hashlib.sha256).digest()
    salt64 = base64.b64encode(salt).decode("ascii")
    stored64 = base64.b64encode(stored_key).decode("ascii")
    server64 = base64.b64encode(server_key).decode("ascii")
    return f"SCRAM-SHA-256${iterations}:{salt64}${stored64}:{server64}"


def _snapshot(
    connection: psycopg.Connection[dict[str, Any]], config: AdminConfig
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    roles = connection.execute(
        "SELECT rolname,rolcanlogin,rolsuper,rolcreatedb,rolcreaterole,"
        "rolreplication,rolbypassrls,shobj_description(oid,'pg_authid') AS marker "
        "FROM pg_roles WHERE rolname IN (%s,%s) ORDER BY rolname",
        (OWNER, RUNTIME),
    ).fetchall()
    database = connection.execute(
        "SELECT datname,pg_get_userbyid(datdba) AS owner,"
        "shobj_description(oid,'pg_database') AS marker,datacl,datdba "
        "FROM pg_database WHERE datname=%s",
        (DATABASE,),
    ).fetchone()
    return roles, database


def _require_provisioned(
    connection: psycopg.Connection[dict[str, Any]], config: AdminConfig
) -> None:
    roles, database = _snapshot(connection, config)
    if len(roles) != 2 or database is None:
        raise AdminError("Production database and both roles must already exist.")
    if database["owner"] != OWNER or database["marker"] != config.marker:
        raise AdminError("Production database owner or marker differs.")
    for role in roles:
        if (
            role["rolname"] not in (OWNER, RUNTIME)
            or not role["rolcanlogin"]
            or any(
                role[name]
                for name in (
                    "rolsuper",
                    "rolcreatedb",
                    "rolcreaterole",
                    "rolreplication",
                    "rolbypassrls",
                )
            )
            or role["marker"] != _role_marker(config)
        ):
            raise AdminError("Production role ownership or privilege differs.")
    membership = connection.execute(
        "SELECT EXISTS(SELECT 1 FROM pg_auth_members WHERE "
        "member IN (SELECT oid FROM pg_roles WHERE rolname IN (%s,%s)) "
        "OR roleid IN (SELECT oid FROM pg_roles WHERE rolname IN (%s,%s)))",
        (OWNER, RUNTIME, OWNER, RUNTIME),
    ).fetchone()
    if membership is None or bool(next(iter(membership.values()))):
        raise AdminError("Production roles have unexpected membership.")
    privileges = connection.execute(
        "SELECT has_database_privilege(%s,%s,'CONNECT') AS connect,"
        "has_database_privilege(%s,%s,'CREATE') AS create,"
        "has_database_privilege(%s,%s,'TEMPORARY') AS temporary,"
        "EXISTS(SELECT 1 FROM aclexplode(coalesce(datacl,acldefault('d',datdba))) "
        "WHERE grantee=0) AS public_access FROM pg_database WHERE datname=%s",
        (RUNTIME, DATABASE, RUNTIME, DATABASE, RUNTIME, DATABASE, DATABASE),
    ).fetchone()
    if privileges != {
        "connect": True,
        "create": False,
        "temporary": False,
        "public_access": False,
    }:
        raise AdminError("Production database grants differ from the approved contract.")


@contextmanager
def _owner_connection(config: AdminConfig) -> Iterator[Connection]:
    engine = create_database_engine(config.owner_url, "production", "owner")
    try:
        with engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        "SELECT current_user AS role,current_database() AS database,"
                        "shobj_description(oid,'pg_database') AS marker,"
                        "pg_get_userbyid(datdba) AS owner "
                        "FROM pg_database WHERE datname=current_database()"
                    )
                )
                .mappings()
                .one()
            )
            if dict(row) != {
                "role": OWNER,
                "database": DATABASE,
                "marker": config.marker,
                "owner": OWNER,
            }:
                raise AdminError("Owner connection does not match production ownership.")
            yield connection
    finally:
        engine.dispose()


class _GuardedOwnerDatabase(CatalogDatabase):
    """Run account creation as effective owner under a protected peer session."""

    def connect(self) -> CatalogConnection:
        reject_pg_environment()
        _require_root()
        connection: CatalogConnection = psycopg.connect(
            host=SOCKET,
            port=PORT,
            dbname=DATABASE,
            user="postgres",
            row_factory=dict_row,
            autocommit=True,
            connect_timeout=2,
            sslmode="disable",
            gssencmode="disable",
            application_name="brickvault-production-admin-bootstrap",
        )
        try:
            row = connection.execute(
                "SELECT current_user AS role,session_user AS login,"
                "current_database() AS database,inet_server_addr() IS NULL AS socket,"
                "current_setting('server_version_num')::integer AS version,"
                "current_setting('listen_addresses') AS listen,"
                "current_setting('port')::integer AS port,"
                "pg_is_in_recovery() AS recovery,"
                "shobj_description(oid,'pg_database') AS marker,"
                "pg_get_userbyid(datdba) AS owner "
                "FROM pg_database WHERE datname=current_database()"
            ).fetchone()
            validate_maintenance_session(row, DATABASE)
            if row is None or row["marker"] != self.ownership_marker or row["owner"] != OWNER:
                raise AdminError("Guarded owner session targets unexpected ownership.")
            _credential_session_guard(connection)
            connection.execute(sql.SQL("SET ROLE {}").format(sql.Identifier(OWNER)))
            identity = connection.execute(
                "SELECT current_user AS role,session_user AS login,current_database() AS database"
            ).fetchone()
            if identity != {"role": OWNER, "login": "postgres", "database": DATABASE}:
                raise AdminError("Guarded owner role switch failed.")
            _verify_credential_logging(connection)
            revisions = connection.execute(
                "SELECT version_num FROM public.alembic_version"
            ).fetchall()
            if sorted(item["version_num"] for item in revisions) != list(expected_revisions()):
                raise AdminError("Guarded owner session requires the packaged migration head.")
            return connection
        except BaseException:
            connection.close()
            raise


def _schema_guard(connection: Connection) -> None:
    row = (
        connection.execute(
            text(
                "SELECT has_schema_privilege(:role,'public','USAGE') AS usage,"
                "has_schema_privilege(:role,'public','CREATE') AS create,"
                "EXISTS(SELECT 1 FROM pg_namespace n,"
                "LATERAL aclexplode(coalesce(n.nspacl,acldefault('n',n.nspowner))) a "
                "WHERE n.nspname='public' AND a.grantee=0) AS public_access"
            ),
            {"role": RUNTIME},
        )
        .mappings()
        .one()
    )
    if dict(row) != {"usage": True, "create": False, "public_access": False}:
        raise AdminError("Production schema grants differ from the approved contract.")


def _runtime_identity(config: AdminConfig) -> None:
    """Check the protected runtime descriptor before migrations can change data."""
    target = validate_target(config.runtime_url, "production", "runtime")
    with psycopg.connect(
        host=target.host,
        port=target.port,
        dbname=target.database,
        user=target.username,
        password=target.password,
        row_factory=dict_row,
        autocommit=True,
        connect_timeout=2,
        sslmode="disable",
        gssencmode="disable",
        application_name="brickvault-production-admin-preflight",
    ) as connection:
        row = connection.execute(
            "SELECT current_user AS role,current_database() AS database,"
            "shobj_description(oid,'pg_database') AS marker,"
            "pg_get_userbyid(datdba) AS owner "
            "FROM pg_database WHERE datname=current_database()"
        ).fetchone()
        if row != {
            "role": RUNTIME,
            "database": DATABASE,
            "marker": config.marker,
            "owner": OWNER,
        }:
            raise AdminError("Runtime connection does not match production ownership.")


def _revisions(connection: Connection) -> tuple[str, ...]:
    if connection.scalar(text("SELECT to_regclass('public.alembic_version')")) is None:
        return ()
    values = tuple(
        sorted(connection.scalars(text("SELECT version_num FROM public.alembic_version")))
    )
    from alembic.script import ScriptDirectory

    known = {
        script.revision
        for script in ScriptDirectory.from_config(migration_config()).walk_revisions()
    }
    if len(values) > 1 or any(value not in known for value in values):
        raise AdminError("Migration state is ambiguous or outside the packaged graph.")
    return values


def _recovery_proof(path: Path, config: AdminConfig, revisions: tuple[str, ...] | None) -> None:
    """Gate mutations on an operator-verified dual-copy receipt bound to this DB."""
    value = _parse_json(_protected_file(path))
    if (
        set(value)
        != {
            "purpose",
            "database",
            "ownership_marker",
            "revisions_at_backup",
            "proxmox_snapshot",
            "drive_snapshot",
            "verified_at_utc",
        }
        or any(
            type(value[key]) is not str
            for key in (
                "purpose",
                "database",
                "ownership_marker",
                "proxmox_snapshot",
                "drive_snapshot",
                "verified_at_utc",
            )
        )
        or type(value["revisions_at_backup"]) is not list
    ):
        raise AdminError("Recovery receipt shape is invalid.")
    if (
        value["purpose"] != "production"
        or value["database"] != DATABASE
        or value["ownership_marker"] != config.marker
        or any(type(item) is not str for item in value["revisions_at_backup"])
        or (revisions is not None and tuple(value["revisions_at_backup"]) != revisions)
        or SNAPSHOT.fullmatch(value["proxmox_snapshot"]) is None
        or SNAPSHOT.fullmatch(value["drive_snapshot"]) is None
        or value["proxmox_snapshot"] == value["drive_snapshot"]
    ):
        raise AdminError("Recovery receipt does not match the target and copies.")
    try:
        stamp = datetime.fromisoformat(value["verified_at_utc"])
    except ValueError as exc:
        raise AdminError("Recovery receipt time is invalid.") from exc
    now = datetime.now(UTC)
    if (
        stamp.tzinfo is None
        or stamp.utcoffset() != timedelta(0)
        or not now - timedelta(hours=24) <= stamp <= now
    ):
        raise AdminError("Recovery receipt is missing, stale or future-dated.")


def preflight(config: AdminConfig) -> str:
    with _maintenance() as maintenance:
        roles, database = _snapshot(maintenance, config)
        if not roles and database is None:
            return "Approved production names are unused; database creation may be reviewed."
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as owner:
        _schema_guard(owner)
        _revisions(owner)
    _runtime_identity(config)
    return "Production database ownership and configuration are recognized."


def provision_db(config: AdminConfig) -> None:
    """Create only unused approved names; partial failures require manual review."""
    with _maintenance() as maintenance:
        roles, database = _snapshot(maintenance, config)
        if roles or database is not None:
            raise AdminError("Provisioning refuses existing or partial production state.")
        owner = validate_target(config.owner_url, "production", "owner")
        runtime = validate_target(config.runtime_url, "production", "runtime")
        iterations = _credential_session_guard(maintenance)
        with maintenance.transaction():
            for role, password in ((OWNER, owner.password), (RUNTIME, runtime.password)):
                if password is None:
                    raise AdminError("Production role credential is missing.")
                verifier = _scram_verifier(password, iterations, secrets.token_bytes(16))
                maintenance.execute(
                    sql.SQL(
                        "CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE "
                        "NOREPLICATION NOBYPASSRLS PASSWORD {}"
                    ).format(sql.Identifier(role), sql.Literal(verifier))
                )
                maintenance.execute(
                    sql.SQL("COMMENT ON ROLE {} IS {}").format(
                        sql.Identifier(role), sql.Literal(_role_marker(config))
                    )
                )
        maintenance.execute(
            sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0").format(
                sql.Identifier(DATABASE), sql.Identifier(OWNER)
            )
        )
        maintenance.execute(
            sql.SQL("COMMENT ON DATABASE {} IS {}").format(
                sql.Identifier(DATABASE), sql.Literal(config.marker)
            )
        )
        maintenance.execute(
            sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(sql.Identifier(DATABASE))
        )
        maintenance.execute(
            sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                sql.Identifier(DATABASE), sql.Identifier(RUNTIME)
            )
        )
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as connection:
        connection.execute(text("REVOKE ALL ON SCHEMA public FROM PUBLIC"))
        connection.execute(text(f'GRANT USAGE ON SCHEMA public TO "{RUNTIME}"'))
        _schema_guard(connection)
    _runtime_identity(config)


def migrate(config: AdminConfig, receipt: Path) -> None:
    with _maintenance() as maintenance:
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as owner:
        _schema_guard(owner)
        _runtime_identity(config)
        before = _revisions(owner)
        if before == expected_revisions():
            raise AdminError("Migration is already current; no operation was performed.")
        _recovery_proof(receipt, config, before)
        alembic = migration_config()
        alembic.attributes["connection"] = owner
        command.upgrade(alembic, "head")
        if _revisions(owner) != expected_revisions():
            raise AdminError("Migration did not reach the packaged head.")


def grant_runtime_role(config: AdminConfig, receipt: Path) -> None:
    with _maintenance() as maintenance:
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as owner:
        _schema_guard(owner)
        if _revisions(owner) != expected_revisions():
            raise AdminError("Runtime grants require the packaged migration head.")
        _recovery_proof(receipt, config, None)
        grant_runtime(owner, RUNTIME)


def _runtime_guard(config: AdminConfig) -> None:
    database = CatalogDatabase(config.runtime_url, "production", config.marker, "runtime")
    with database.connect() as connection:
        row = connection.execute(
            "SELECT has_schema_privilege(current_user,'public','CREATE') AS schema_create,"
            "has_database_privilege(current_user,current_database(),'CREATE') AS db_create,"
            "has_database_privilege(current_user,current_database(),'TEMPORARY') AS temporary,"
            "has_table_privilege(current_user,'public.alembic_version','SELECT') AS revision_read,"
            "has_table_privilege(current_user,'public.alembic_version','UPDATE') AS revision_write,"
            "has_table_privilege(current_user,'public.auth_principal','SELECT') AS principal_read,"
            "has_table_privilege(current_user,'public.auth_principal','INSERT') AS principal_write"
        ).fetchone()
        if row != {
            "schema_create": False,
            "db_create": False,
            "temporary": False,
            "revision_read": True,
            "revision_write": False,
            "principal_read": True,
            "principal_write": False,
        }:
            raise AdminError("Runtime privileges differ from the approved minimum checks.")


def bootstrap_owner(config: AdminConfig, receipt: Path) -> None:
    with _maintenance() as maintenance:
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as owner:
        _schema_guard(owner)
        if _revisions(owner) != expected_revisions():
            raise AdminError("Owner bootstrap requires the packaged migration head.")
        _recovery_proof(receipt, config, None)
        if owner.scalar(text("SELECT count(*) FROM public.auth_principal")) != 0:
            raise AdminError("Owner account already exists; bootstrap refuses repetition.")
    _runtime_guard(config)
    if not sys.stdin.isatty():
        raise AdminError("Owner bootstrap requires a local interactive TTY.")
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        password = getpass.getpass("New owner password: ")
        confirmation = getpass.getpass("Repeat owner password: ")
    if not password_valid(password) or password != confirmation:
        raise AdminError("Owner password length or confirmation is invalid.")
    database = _GuardedOwnerDatabase(config.owner_url, "production", config.marker, "owner")
    AuthService(database).provision(password)


def verify(config: AdminConfig) -> None:
    with _maintenance() as maintenance:
        _require_provisioned(maintenance, config)
    with _owner_connection(config) as owner:
        _schema_guard(owner)
        if _revisions(owner) != expected_revisions():
            raise AdminError("Packaged migration head is not current.")
        if owner.scalar(text("SELECT count(*) FROM public.auth_principal")) != 1:
            raise AdminError("Expected exactly one private owner account.")
    _runtime_guard(config)


class _SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise AdminError("Invalid administration command or options.")


def main(argv: list[str] | None = None) -> int:
    parser = _SafeParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--config", type=Path, default=CONFIG_PATH, help="root-owned local descriptor"
    )
    commands = parser.add_subparsers(dest="command", required=True, parser_class=_SafeParser)
    for name in (
        "preflight",
        "provision-db",
        "migrate",
        "grant-runtime",
        "bootstrap-owner",
        "verify",
    ):
        command_parser = commands.add_parser(name, allow_abbrev=False)
        if name in ("migrate", "grant-runtime", "bootstrap-owner"):
            command_parser.add_argument("--recovery-proof", required=True, type=Path)
    try:
        options = parser.parse_args(argv)
        config = _load_config(options.config)
        match options.command:
            case "preflight":
                print(preflight(config))
            case "provision-db":
                provision_db(config)
                print(
                    "Production database and roles provisioned; review backup gates before migration."
                )
            case "migrate":
                migrate(config, options.recovery_proof)
                print("Packaged production migrations reached the current head.")
            case "grant-runtime":
                grant_runtime_role(config, options.recovery_proof)
                print("Enumerated runtime grants applied.")
            case "bootstrap-owner":
                bootstrap_owner(config, options.recovery_proof)
                print("Private owner account created.")
            case "verify":
                verify(config)
                print("Production ownership, migration, account and core grants verified.")
        return 0
    except Exception:  # noqa: BLE001 - never print driver, parser, file or credential details.
        print("Production administration refused; inspect protected local state.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
