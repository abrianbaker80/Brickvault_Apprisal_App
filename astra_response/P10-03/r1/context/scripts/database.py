"""Owned local Compose instances and explicit database operations. No import-time I/O."""

import json
import os
import re
import socket
import subprocess
import sys
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import psycopg
from alembic import command
from brickvault_api.application.readiness import Ready, check_readiness
from brickvault_api.persistence.database import (
    create_database_engine,
    expected_revisions,
    migration_config,
)
from brickvault_api.publication import publish_json
from brickvault_api.settings import (
    TEST_DATABASE,
    ConfigurationError,
    Purpose,
    Role,
    reject_pg_environment,
    validate_target,
)
from psycopg import sql
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local" / "database"
IMAGE = "docker.io/library/postgres:18.6-bookworm@sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af"
OWNER_LABEL = "app.brickvault.owner"


class DatabaseError(RuntimeError):
    """Safe operator-facing error."""


def run(
    args: list[str], *, env: Mapping[str, str] | None = None, timeout: int = 60
) -> str:
    try:
        result = subprocess.run(
            args,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise DatabaseError(
            "Local command unavailable or timed out; output redacted."
        ) from None
    if result.returncode:
        raise DatabaseError(
            f"Local command failed (exit {result.returncode}); output redacted."
        )
    return result.stdout


def private_path(path: Path) -> None:
    if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
        raise DatabaseError(
            "Private path must remain an ordinary repository-owned path."
        )
    relative = str(path.relative_to(ROOT))
    run(["git", "check-ignore", "--quiet", "--", relative])
    if run(["git", "ls-files", "--", relative]).strip():
        raise DatabaseError("Private data must not be tracked.")


def write_record(path: Path, value: dict[str, Any]) -> None:
    private_path(path)
    publish_json(ROOT, path, value, run_id=value.get("run_id"))


@contextmanager
def runner_lock(name: str = "runner") -> Iterator[None]:
    path = LOCAL / f"{name}.lock"
    private_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise DatabaseError(
                "Another database runner holds the exclusive lock."
            ) from None
        try:
            yield
        finally:
            stream.seek(0)
            if sys.platform == "win32":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def load_config() -> dict[str, str]:
    path = ROOT / ".env.local"
    private_path(path)
    if not path.is_file() or path.stat().st_size > 16384:
        raise ConfigurationError(
            "Run dev:init to establish valid private local configuration."
        )
    if any(key.startswith("BVA_") for key in os.environ):
        raise ConfigurationError(
            "Database tooling refuses inherited application overrides."
        )
    # Reuse the accepted initializer's full validation, without emitting private values.
    run(
        [
            "node",
            "--input-type=module",
            "-e",
            "import {initializeConfig} from './scripts/tasks.mjs'; initializeConfig(process.cwd());",
        ]
    )
    return dict(
        line.split("=", 1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line and not line.lstrip().startswith("#")
    )


def require_free_port(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        if sys.platform == "win32":
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            raise DatabaseError(
                "Required loopback port is occupied; preserve its process."
            ) from None


def local_context() -> str:
    if any(
        key.upper().startswith(("DOCKER_", "COMPOSE_")) and value
        for key, value in os.environ.items()
    ):
        raise DatabaseError(
            "Docker/Compose overrides require explicit locality review."
        )
    context = run(["docker", "context", "show"]).strip()
    endpoint = run(
        [
            "docker",
            "context",
            "inspect",
            context,
            "--format",
            "{{.Endpoints.docker.Host}}",
        ]
    ).strip()
    local_pipe = endpoint in (
        "npipe:////./pipe/dockerDesktopLinuxEngine",
        "npipe:////./pipe/docker_engine",
    )
    local_socket = endpoint.startswith("unix:///") and ".." not in endpoint.split("/")
    if not (local_pipe or local_socket):
        raise DatabaseError(
            "Docker endpoint is not a verified local named pipe or Unix socket."
        )
    if (
        run(["docker", "--context", context, "info", "--format", "{{.OSType}}"]).strip()
        != "linux"
    ):
        raise DatabaseError("A local Docker Linux engine is required.")
    run(["docker", "--context", context, "compose", "version"])
    return context


@dataclass
class Instance:
    purpose: Purpose
    config: dict[str, str] = field(repr=False)
    context: str
    owner: str

    @property
    def short(self) -> str:
        return "dev" if self.purpose == "development" else "test"

    @property
    def project(self) -> str:
        return f"brickvault-appraisal-{self.short}"

    @property
    def port(self) -> int:
        return 55432 if self.purpose == "development" else 55433

    def docker(self, *args: str) -> str:
        return run(["docker", "--context", self.context, *args])

    def inspect(self, kind: str, identifier: str) -> dict[str, Any]:
        return cast(
            list[dict[str, Any]], json.loads(self.docker(kind, "inspect", identifier))
        )[0]

    def inventory(self) -> tuple[list[str], list[str], list[str]]:
        inventories = [
            self.docker(*args).splitlines()
            for args in (
                (
                    "container",
                    "ls",
                    "-aq",
                    "--filter",
                    f"label=com.docker.compose.project={self.project}",
                ),
                (
                    "volume",
                    "ls",
                    "-q",
                    "--filter",
                    f"label=com.docker.compose.project={self.project}",
                ),
                (
                    "network",
                    "ls",
                    "-q",
                    "--filter",
                    f"label=com.docker.compose.project={self.project}",
                ),
            )
        ]
        return inventories[0], inventories[1], inventories[2]

    def verify(self, *, required: bool = True) -> dict[str, Any] | None:
        containers, volumes, networks = self.inventory()
        # Names are checked as well as labels, so an unlabelled collision cannot be adopted.
        named = self.docker("container", "ls", "-a", "--format", "{{.ID}}|{{.Names}}")
        if any(
            name.startswith(self.project + "-")
            and identifier not in [c[:12] for c in containers]
            for identifier, name in (line.split("|", 1) for line in named.splitlines())
        ):
            raise DatabaseError("Unexpected container name collision.")
        for kind, expected, owned in (
            ("volume", f"{self.project}_data", volumes),
            ("network", f"{self.project}_default", networks),
        ):
            names = self.docker(kind, "ls", "--format", "{{.Name}}").splitlines()
            if expected in names and not owned:
                raise DatabaseError("Unexpected unowned resource name collision.")
        if len(containers) > 1 or len(volumes) > 1 or len(networks) > 1:
            raise DatabaseError("Unexpected resources in the intended Compose project.")
        for kind, identifiers, logical in (
            ("volume", volumes, "data"),
            ("network", networks, "default"),
            ("container", containers, "postgres"),
        ):
            for identifier in identifiers:
                item = self.inspect(kind, identifier)
                labels = (
                    item["Config"]["Labels"] if kind == "container" else item["Labels"]
                )
                if (
                    not labels
                    or labels.get(OWNER_LABEL) != self.owner
                    or labels.get("com.docker.compose.project") != self.project
                ):
                    raise DatabaseError(
                        "Compose resource ownership does not match this checkout's receipt."
                    )
                label_key = "service" if kind == "container" else kind
                if labels.get(f"com.docker.compose.{label_key}") != logical:
                    raise DatabaseError("Unexpected Compose resource identity.")
                if kind != "container" and item["Name"] != f"{self.project}_{logical}":
                    raise DatabaseError("Unexpected resource name.")
                if kind == "network" and (
                    item["Internal"] or item["Driver"] != "bridge"
                ):
                    raise DatabaseError("Unexpected database network configuration.")
                if kind == "volume" and (
                    item["Driver"] != "local" or item.get("Options")
                ):
                    raise DatabaseError("Unexpected database volume configuration.")
        if not containers:
            if required:
                raise DatabaseError(
                    "Owned database service is absent; run db:up first."
                )
            return None
        item = self.inspect("container", containers[0])
        labels = item["Config"]["Labels"]
        configured_file = str(ROOT / "infra" / "compose.dev.yml")
        if (
            Path(labels.get("com.docker.compose.project.config_files", "")).resolve()
            != Path(configured_file).resolve()
        ):
            raise DatabaseError(
                "Container was not created from this checkout's Compose file."
            )
        expected_bind = {
            "5432/tcp": [{"HostIp": "127.0.0.1", "HostPort": str(self.port)}]
        }
        if item["State"].get("Paused") or item["State"].get("Restarting"):
            raise DatabaseError(
                "Owned service is paused or restarting; preserve its current state."
            )
        if (
            item["State"]["Running"]
            and item["NetworkSettings"]["Ports"] != expected_bind
        ):
            raise DatabaseError(
                "Owned service has no effective approved loopback port publication."
            )
        mounts = item["Mounts"]
        if (
            item["Config"]["Image"] != IMAGE
            or item["HostConfig"]["PortBindings"] != expected_bind
            or item["HostConfig"]["Privileged"]
            or item["HostConfig"].get("Binds")
            not in (None, [], [f"{self.project}_data:/var/lib/postgresql:rw"])
            or len(mounts) != 1
            or mounts[0]["Type"] != "volume"
            or mounts[0]["Name"] != f"{self.project}_data"
            or mounts[0]["Destination"] != "/var/lib/postgresql"
            or set(item["NetworkSettings"]["Networks"]) != {f"{self.project}_default"}
        ):
            raise DatabaseError(
                "Owned container configuration differs from the approved isolation contract."
            )
        environment = dict(entry.split("=", 1) for entry in item["Config"]["Env"])
        if (
            environment.get("PGDATA") != "/var/lib/postgresql/18/docker"
            or environment.get("POSTGRES_USER") != "brickvault_bootstrap"
            or environment.get("POSTGRES_PASSWORD")
            != self.config[f"BVA_{self.short.upper()}_BOOTSTRAP_PASSWORD"]
        ):
            raise DatabaseError(
                "Owned container settings or preserved credentials differ; refusing replacement."
            )
        return item

    def up(self) -> bool:
        before = self.verify(required=False)
        if before and before["State"]["Running"]:
            return False
        require_free_port(self.port)
        environment = {
            **os.environ,
            "BVA_DATABASE_PORT": str(self.port),
            "BVA_DATABASE_OWNER": self.owner,
            "BVA_DATABASE_BOOTSTRAP_PASSWORD": self.config[
                f"BVA_{self.short.upper()}_BOOTSTRAP_PASSWORD"
            ],
        }
        run(
            [
                "docker",
                "--context",
                self.context,
                "compose",
                "--project-name",
                self.project,
                "--file",
                str(ROOT / "infra" / "compose.dev.yml"),
                "--env-file",
                os.devnull,
                "up",
                "--detach",
                "--no-recreate",
                "--pull",
                "never",
                "--wait",
                "--wait-timeout",
                "45",
                "postgres",
            ],
            env=environment,
        )
        self.verify()
        return True

    def stop(self) -> None:
        item = self.verify(required=False)
        if item and item["State"]["Running"]:
            self.docker("stop", "--time", "10", item["Id"])

    def target(self, database: str, role: Role) -> str:
        template = self.config[f"BVA_{self.short.upper()}_{role.upper()}_DATABASE_URL"]
        original = validate_target(template, self.purpose, role, config_template=True)
        result = original.set(database=database).render_as_string(hide_password=False)
        validate_target(result, self.purpose, role)
        return result

    def bootstrap(self) -> psycopg.Connection[tuple[Any, ...]]:
        self.verify()
        reject_pg_environment()
        return psycopg.connect(
            host="127.0.0.1",
            port=self.port,
            dbname="postgres",
            user="brickvault_bootstrap",
            password=self.config[f"BVA_{self.short.upper()}_BOOTSTRAP_PASSWORD"],
            autocommit=True,
            connect_timeout=2,
            options="-c statement_timeout=2000 -c lock_timeout=2000",
            sslmode="disable",
            gssencmode="disable",
        )


def instance(purpose: Purpose) -> Instance:
    configured = load_config()
    context = local_context()
    path = LOCAL / f"{purpose}.json"
    private_path(path)
    if path.exists():
        record = json.loads(path.read_text())
        if (
            record.get("root") != str(ROOT)
            or re.fullmatch(r"[a-f0-9]{32}", record.get("owner", "")) is None
        ):
            raise DatabaseError("Invalid local resource ownership receipt.")
        owner = str(record["owner"])
    else:
        owner = uuid4().hex
        candidate = Instance(purpose, configured, context, owner)
        candidate.verify(required=False)
        write_record(path, {"root": str(ROOT), "owner": owner})
    return Instance(purpose, configured, context, owner)


def database_marker(instance: Instance, run_id: str) -> str:
    return f"brickvault-appraisal:{instance.owner}:{run_id}"


def provision(instance: Instance, database: str, run_id: str) -> None:
    owner_url = validate_target(
        instance.target(database, "owner"), instance.purpose, "owner"
    )
    runtime_url = validate_target(
        instance.target(database, "runtime"), instance.purpose, "runtime"
    )
    marker = database_marker(instance, run_id)
    with instance.bootstrap() as connection:
        for target in (owner_url, runtime_url):
            role = target.username
            existing = connection.execute(
                "SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication, rolbypassrls, shobj_description(oid, 'pg_authid') FROM pg_roles WHERE rolname=%s",
                (role,),
            ).fetchone()
            if existing:
                if any(existing[:5]) or existing[5] != database_marker(
                    instance, "role"
                ):
                    raise DatabaseError(
                        "Existing role does not match its ownership and privilege contract."
                    )
                if connection.execute(
                    "SELECT 1 FROM pg_auth_members WHERE member=(SELECT oid FROM pg_roles WHERE rolname=%s)",
                    (role,),
                ).fetchone():
                    raise DatabaseError("Unexpected inherited role membership.")
            else:
                connection.execute(
                    sql.SQL(
                        "CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD {}"
                    ).format(sql.Identifier(role or ""), sql.Literal(target.password))
                )
                connection.execute(
                    sql.SQL("COMMENT ON ROLE {} IS {}").format(
                        sql.Identifier(role or ""),
                        sql.Literal(database_marker(instance, "role")),
                    )
                )
        existing_db = connection.execute(
            "SELECT pg_get_userbyid(datdba), shobj_description(oid, 'pg_database') FROM pg_database WHERE datname=%s",
            (database,),
        ).fetchone()
        if existing_db:
            if existing_db != (owner_url.username, marker):
                raise DatabaseError(
                    "Existing database is not owned by this provisioning operation."
                )
        else:
            connection.execute(
                sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0").format(
                    sql.Identifier(database), sql.Identifier(owner_url.username or "")
                )
            )
            connection.execute(
                sql.SQL("COMMENT ON DATABASE {} IS {}").format(
                    sql.Identifier(database), sql.Literal(marker)
                )
            )
        connection.execute(
            sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(
                sql.Identifier(database)
            )
        )
        connection.execute(
            sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                sql.Identifier(database), sql.Identifier(runtime_url.username or "")
            )
        )
        # PUBLIC's default CONNECT/TEMP on maintenance/template databases is not runtime access.
        for maintenance in ("postgres", "template1"):
            connection.execute(
                sql.SQL("REVOKE ALL ON DATABASE {} FROM PUBLIC").format(
                    sql.Identifier(maintenance)
                )
            )
    engine = create_database_engine(
        instance.target(database, "owner"), instance.purpose, "owner"
    )
    try:
        with engine.begin() as connection:
            connection.execute(text("REVOKE ALL ON SCHEMA public FROM PUBLIC"))
            # Role names have already passed an exact allowlist; no arbitrary SQL identifiers.
            connection.execute(
                text(f'GRANT USAGE ON SCHEMA public TO "{runtime_url.username}"')
            )
    finally:
        engine.dispose()


def migrate(
    instance: Instance,
    database: str,
    *,
    downgrade: bool = False,
    run_id: str = "development",
    revision: str = "head",
) -> None:
    instance.verify()
    if revision != "head" and (
        instance.purpose != "test"
        or TEST_DATABASE.fullmatch(database) is None
        or revision
        not in (
            "0001_foundation",
            "0002_catalog_identity",
            "0003_catalog_inventory",
            "0004_catalog_staging",
        )
    ):
        raise DatabaseError(
            "Explicit migration boundaries require a disposable test database."
        )
    if downgrade and (
        instance.purpose != "test" or TEST_DATABASE.fullmatch(database) is None
    ):
        raise DatabaseError(
            "Destructive migrations require a disposable test database."
        )
    with instance.bootstrap() as maintenance:
        row = maintenance.execute(
            "SELECT shobj_description(oid, 'pg_database'), pg_get_userbyid(datdba) FROM pg_database WHERE datname=%s",
            (database,),
        ).fetchone()
        expected_owner = (
            "brickvault_dev_owner"
            if instance.purpose == "development"
            else "brickvault_test_owner"
        )
        if row != (database_marker(instance, run_id), expected_owner):
            raise DatabaseError("Migration requires verified database ownership.")
    engine = create_database_engine(
        instance.target(database, "owner"), instance.purpose, "owner"
    )
    try:
        with engine.begin() as connection:
            config = migration_config()
            config.attributes["connection"] = connection
            if downgrade:
                command.downgrade(config, "base")
            else:
                command.upgrade(config, revision)
                role = validate_target(
                    instance.target(database, "runtime"), instance.purpose, "runtime"
                ).username
                connection.execute(
                    text(f'REVOKE ALL ON public.alembic_version FROM PUBLIC, "{role}"')
                )
                connection.execute(
                    text(f'GRANT SELECT ON public.alembic_version TO "{role}"')
                )
                from brickvault_api.catalog.models import (
                    CATALOG_TABLES,
                    RUNTIME_CATALOG_TABLES,
                )

                # Enumerated catalog objects only. Future tables get no default grant.
                for name in CATALOG_TABLES:
                    if (
                        connection.scalar(
                            text("SELECT to_regclass(:name)"),
                            {"name": "public." + name},
                        )
                        is not None
                    ):
                        connection.execute(
                            text(f'REVOKE ALL ON public."{name}" FROM PUBLIC, "{role}"')
                        )
                        if name in RUNTIME_CATALOG_TABLES:
                            connection.execute(
                                text(f'GRANT SELECT ON public."{name}" TO "{role}"')
                            )
                from brickvault_api.market.models import (
                    MARKET_TABLES,
                    OPERATIONAL_TABLES,
                )

                if connection.scalar(
                    text("SELECT to_regclass('public.auth_principal')")
                ):
                    for name, privileges in (
                        ("auth_principal", "SELECT"),
                        ("auth_control", "SELECT, UPDATE"),
                        ("auth_session", "SELECT, INSERT, DELETE"),
                    ):
                        connection.execute(
                            text(f'REVOKE ALL ON public.{name} FROM PUBLIC, "{role}"')
                        )
                        connection.execute(
                            text(f'GRANT {privileges} ON public.{name} TO "{role}"')
                        )
                    connection.execute(
                        text(
                            f'GRANT UPDATE(last_activity_at,revoked_at) ON public.auth_session TO "{role}"'
                        )
                    )

                if connection.scalar(
                    text("SELECT to_regclass('public.deal_forecast')")
                ):
                    connection.execute(
                        text(
                            f'REVOKE ALL ON public.deal_forecast FROM PUBLIC, "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f'GRANT SELECT, INSERT, UPDATE(saved_at) ON public.deal_forecast TO "{role}"'
                        )
                    )
                    for signature in (
                        "forecast_clock()",
                        "forecast_cleanup(uuid)",
                        "forecast_lock_context(uuid)",
                    ):
                        connection.execute(
                            text(
                                f'GRANT EXECUTE ON FUNCTION public.{signature} TO "{role}"'
                            )
                        )

                if connection.scalar(
                    text("SELECT to_regclass('public.watchlist_item')")
                ):
                    connection.execute(
                        text(
                            f'REVOKE ALL ON public.watchlist_item FROM PUBLIC, "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f'GRANT SELECT, DELETE ON public.watchlist_item TO "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f"GRANT INSERT(id,owner_id,canonical_set_id,set_number,target_purchase_price) "
                            f'ON public.watchlist_item TO "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f"GRANT UPDATE(target_purchase_price,note,revision) "
                            f'ON public.watchlist_item TO "{role}"'
                        )
                    )

                if connection.scalar(
                    text("SELECT to_regclass('public.deal_lineage_metadata')")
                ):
                    connection.execute(
                        text(
                            f'REVOKE ALL ON public.deal_lineage_metadata FROM PUBLIC, "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f"GRANT SELECT, INSERT(owner_id,root_forecast_id,note,source_url), "
                            f'UPDATE(note,source_url,revision) ON public.deal_lineage_metadata TO "{role}"'
                        )
                    )

                if connection.scalar(text("SELECT to_regclass('public.hunt_run')")):
                    connection.execute(
                        text(f'REVOKE ALL ON public.hunt_run FROM PUBLIC, "{role}"')
                    )
                    connection.execute(
                        text(
                            f"GRANT SELECT, INSERT(id,owner_id,idempotency_key,request_digest,"
                            f"run_version,sort_policy_version,default_sort_by,"
                            f"default_sort_direction,settings_snapshot,candidate_count), "
                            f'UPDATE(completed_at) ON public.hunt_run TO "{role}"'
                        )
                    )
                if connection.scalar(
                    text("SELECT to_regclass('public.hunt_candidate')")
                ):
                    connection.execute(
                        text(
                            f'REVOKE ALL ON public.hunt_candidate FROM PUBLIC, "{role}"'
                        )
                    )
                    connection.execute(
                        text(
                            f"GRANT SELECT, INSERT(id,run_id,owner_id,candidate_position,"
                            f"canonical_set_id,set_number,set_name,snapshot_version,snapshot) "
                            f'ON public.hunt_candidate TO "{role}"'
                        )
                    )

                if connection.scalar(
                    text("SELECT to_regclass('public.selling_profile')")
                ):
                    for table, insert_columns, update_columns in (
                        (
                            "selling_profile",
                            "id,owner_id,name,assumptions",
                            "name,assumptions,revision",
                        ),
                        (
                            "application_settings",
                            "id,owner_id,default_profile_id,defaults",
                            "default_profile_id,defaults,revision",
                        ),
                    ):
                        connection.execute(
                            text(f'REVOKE ALL ON public.{table} FROM PUBLIC, "{role}"')
                        )
                        connection.execute(
                            text(
                                f'GRANT SELECT, INSERT({insert_columns}), UPDATE({update_columns}) ON public.{table} TO "{role}"'
                            )
                        )
                    connection.execute(
                        text(f'GRANT DELETE ON public.selling_profile TO "{role}"')
                    )

                for name in MARKET_TABLES:
                    if (
                        connection.scalar(
                            text("SELECT to_regclass(:name)"),
                            {"name": "public." + name},
                        )
                        is not None
                    ):
                        connection.execute(
                            text(f'REVOKE ALL ON public."{name}" FROM PUBLIC, "{role}"')
                        )
                        privileges = "SELECT"
                        if (
                            name in OPERATIONAL_TABLES
                            and name != "provider_scope_state"
                        ):
                            privileges += ", INSERT, UPDATE"
                        elif name == "market_observation":
                            privileges += ", INSERT"
                        connection.execute(
                            text(f'GRANT {privileges} ON public."{name}" TO "{role}"')
                        )
                        if name == "provider_scope_state":
                            connection.execute(
                                text(
                                    f'GRANT UPDATE(suspended,next_dispatch_at,lease_owner,lease_token,lease_until) ON public.provider_scope_state TO "{role}"'
                                )
                            )
                from brickvault_api.market.product_refresh_models import (
                    PRODUCT_COLUMNS,
                    PRODUCT_FUNCTIONS,
                )

                if connection.scalar(
                    text("SELECT to_regclass('public.product_refresh_operation')")
                ):
                    for name, columns in PRODUCT_COLUMNS.items():
                        connection.execute(
                            text(
                                f'GRANT UPDATE({columns}) ON public.{name} TO "{role}"'
                            )
                        )
                    connection.execute(
                        text(
                            "GRANT INSERT(attempt_id,operation_id,item_type,item_no,item_name,classification,"
                            "received_at,completed_at,adapter_version,normalization_version,evidence_digest,retained_until) "
                            f'ON public.provider_discovery_evidence TO "{role}"'
                        )
                    )
                    for signature in PRODUCT_FUNCTIONS:
                        connection.execute(
                            text(
                                f'GRANT EXECUTE ON FUNCTION public.{signature} TO "{role}"'
                            )
                        )
    finally:
        engine.dispose()


def cleanup_database(
    instance: Instance, database: str, run_id: str, recorded: list[str]
) -> bool:
    if (
        instance.purpose != "test"
        or TEST_DATABASE.fullmatch(database) is None
        or database not in recorded
    ):
        raise DatabaseError(
            "Cleanup requires an exact run-recorded disposable test database."
        )
    with instance.bootstrap() as connection:
        row = connection.execute(
            "SELECT shobj_description(oid, 'pg_database'), pg_get_userbyid(datdba) FROM pg_database WHERE datname=%s",
            (database,),
        ).fetchone()
        if row is None:
            return False
        if row != (database_marker(instance, run_id), "brickvault_test_owner"):
            raise DatabaseError("Database cleanup ownership check failed.")
        connection.execute(
            sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(database))
        )
    return True


def main(task: str) -> None:
    with runner_lock():
        if task == "test:integration":
            from integration_runner import integration

            integration(instance("test"))
            return
        dev = instance("development")
        if task == "db:up":
            dev.up()
            provision(dev, "brickvault_dev", "development")
        elif task == "db:migrate":
            migrate(dev, "brickvault_dev")
        elif task == "db:status":
            dev.verify()
            engine = create_database_engine(
                dev.target("brickvault_dev", "runtime"), "development"
            )
            try:
                state = check_readiness(engine)
                print(
                    json.dumps(
                        {
                            "project": dev.project,
                            "expected": expected_revisions(),
                            **state.model_dump(),
                        }
                    )
                )
                if not isinstance(state, Ready):
                    raise DatabaseError("Development database is not ready.")
            finally:
                engine.dispose()
        elif task == "db:stop":
            test = instance("test")
            dev.verify(required=False)
            test.verify(required=False)
            dev.stop()
            test.stop()
        else:
            raise DatabaseError("Unknown database command.")
        print(f"{task} completed; named volumes preserved.")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise DatabaseError("Expected one database command.")
        main(sys.argv[1])
    except (DatabaseError, ConfigurationError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except (Exception, KeyboardInterrupt):  # noqa: BLE001 -- redact last-resort private driver errors
        print(
            "Database command failed or interrupted; private output redacted. Inspect owned-resource status.",
            file=sys.stderr,
        )
        sys.exit(1)
