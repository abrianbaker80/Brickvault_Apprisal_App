"""One owned local PostgreSQL proof of the production-style runtime contract."""

import json
import logging
import secrets
from uuid import uuid4

import psycopg
from brickvault_api.auth import AuthService
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.main import create_app
from brickvault_api.observability import SafeFormatter
from brickvault_api.persistence.database import create_database_engine
from brickvault_api.settings import RuntimeSettings
from database import (
    LOCAL,
    ROOT,
    DatabaseError,
    Instance,
    database_marker,
    instance,
    migrate,
    runner_lock,
    write_record,
)
from fastapi.testclient import TestClient
from psycopg import sql
from pydantic import SecretStr
from sqlalchemy import text

ORIGIN = "https://app.example.test"
NATIVE_ORIGIN = "https://android.app.example.test"
PROXY = "b" * 64  # Synthetic proof value; never a deployment secret.


def targets(
    stem: str, database: str, owner_password: str, runtime_password: str
) -> tuple[str, str]:
    base = f"@127.0.0.1:55433/{database}"
    return (
        f"postgresql+psycopg://brickvault_{stem}_owner:{owner_password}{base}",
        f"postgresql+psycopg://brickvault_{stem}_runtime:{runtime_password}{base}",
    )


def provision_proof_database(
    owned: Instance,
    database: str,
    owner_role: str,
    runtime_role: str,
    owner_password: str,
    runtime_password: str,
    marker: str,
    role_marker: str,
) -> None:
    with owned.bootstrap() as connection, connection.transaction():
        for role, password in (
            (owner_role, owner_password),
            (runtime_role, runtime_password),
        ):
            if connection.execute(
                "SELECT 1 FROM pg_roles WHERE rolname=%s", (role,)
            ).fetchone():
                raise DatabaseError("Production proof role already exists.")
            connection.execute(
                sql.SQL(
                    "CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE "
                    "NOREPLICATION NOBYPASSRLS PASSWORD {}"
                ).format(sql.Identifier(role), sql.Literal(password))
            )
            connection.execute(
                sql.SQL("COMMENT ON ROLE {} IS {}").format(
                    sql.Identifier(role), sql.Literal(role_marker)
                )
            )
    with owned.bootstrap() as connection:
        if connection.execute(
            "SELECT 1 FROM pg_database WHERE datname=%s", (database,)
        ).fetchone():
            raise DatabaseError("Production proof database already exists.")
        connection.execute(
            sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0").format(
                sql.Identifier(database), sql.Identifier(owner_role)
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
                sql.Identifier(database), sql.Identifier(runtime_role)
            )
        )


def cleanup_proof_database(
    owned: Instance,
    database: str,
    owner_role: str,
    runtime_role: str,
    marker: str,
    role_marker: str,
) -> None:
    with owned.bootstrap() as connection:
        row = connection.execute(
            "SELECT shobj_description(oid,'pg_database'),pg_get_userbyid(datdba) "
            "FROM pg_database WHERE datname=%s",
            (database,),
        ).fetchone()
        if row is not None:
            if row != (marker, owner_role):
                raise DatabaseError(
                    "Production proof database ownership changed; cleanup refused."
                )
            connection.execute(
                sql.SQL("DROP DATABASE {} WITH (FORCE)").format(
                    sql.Identifier(database)
                )
            )
        for role in (runtime_role, owner_role):
            record = connection.execute(
                "SELECT shobj_description(oid,'pg_authid') FROM pg_roles WHERE rolname=%s",
                (role,),
            ).fetchone()
            if record is not None:
                if record != (role_marker,):
                    raise DatabaseError(
                        "Production proof role ownership changed; cleanup refused."
                    )
                connection.execute(sql.SQL("DROP ROLE {}").format(sql.Identifier(role)))


def http_proof(owner_url: str, runtime_url: str, marker: str) -> None:
    owner = CatalogDatabase(owner_url, "production", marker, role="owner")
    runtime = CatalogDatabase(runtime_url, "production", marker, role="runtime")
    password = secrets.token_urlsafe(32)
    AuthService(owner).provision(password)
    with runtime.connect() as connection:
        identity = connection.execute("SELECT current_user").fetchone()
        assert identity is not None
        role = identity["current_user"]
        assert role.endswith("_runtime")
        privilege = connection.execute(
            "SELECT has_database_privilege(current_user,current_database(),'CREATE') AS allowed"
        ).fetchone()
        assert privilege is not None and not privilege["allowed"]
        try:
            connection.execute("CREATE TABLE public.proof_forbidden(id integer)")
        except psycopg.errors.InsufficientPrivilege:
            pass
        else:
            raise AssertionError("Runtime role gained DDL privilege")
    settings = RuntimeSettings(
        purpose="production",
        port=8600,
        database_url=SecretStr(runtime_url),
        database_ownership_marker=SecretStr(marker),
        production_origin=ORIGIN,
        proxy_shared_secret=SecretStr(PROXY),
        static_enabled=True,
        web_build_dir=str((ROOT / "apps/web/dist").resolve()),
    )
    settings.target()
    request_logger = logging.getLogger("brickvault.requests")
    prior_level = request_logger.level
    records: list[logging.LogRecord] = []

    class Capture(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    handler = Capture()
    request_logger.addHandler(handler)
    request_logger.setLevel(logging.INFO)
    application = create_app(settings)
    try:
        with TestClient(application, base_url="http://app.example.test") as client:
            proxy = {"X-BrickVault-Proxy": PROXY}
            assert client.get("/api/health").status_code == 403
            assert (
                client.get(
                    "/api/health", headers={"X-Forwarded-Proto": "https"}
                ).status_code
                == 403
            )
            assert (
                client.get(
                    "/api/health",
                    headers={
                        **proxy,
                        "Host": "evil.example.test",
                        "X-Forwarded-Host": "app.example.test",
                    },
                ).status_code
                == 400
            )
            assert (
                client.get(
                    "/api/health",
                    headers={
                        **proxy,
                        "Origin": "https://evil.example.test",
                        "X-Forwarded-Proto": "https",
                    },
                ).status_code
                == 403
            )
            assert (
                client.get(
                    "/api/health", headers={**proxy, "Origin": ORIGIN}
                ).status_code
                == 200
            )
            preflight = client.options(
                "/api/auth/login",
                headers={
                    **proxy,
                    "Origin": NATIVE_ORIGIN,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type,x-brickvault-login",
                },
            )
            assert preflight.status_code == 204
            assert preflight.headers["access-control-allow-origin"] == NATIVE_ORIGIN
            assert (
                client.post(
                    "/api/auth/login", json={"password": password}, headers=proxy
                ).status_code
                == 403
            )
            login = client.post(
                "/api/auth/login",
                json={"password": password},
                headers={**proxy, "Origin": ORIGIN, "X-BrickVault-Login": "1"},
            )
            assert login.status_code == 200
            assert all(
                "Secure" in header
                and "HttpOnly" in header
                and "SameSite=strict" in header
                for header in login.headers.get_list("set-cookie")
            )
            session = login.cookies.get("bva_session")
            csrf_cookie = login.cookies.get("bva_csrf")
            csrf = login.json()["csrf_token"]
            assert session and csrf_cookie and csrf
            cookies = {
                **proxy,
                "Cookie": f"bva_session={session}; bva_csrf={csrf_cookie}",
            }
            ready = client.get("/api/ready", headers=cookies)
            assert ready.status_code == 200 and ready.json()["migrations"] == "current"
            assert ready.headers["cache-control"] == "no-store"
            assert (
                client.post(
                    "/api/auth/logout", headers={**cookies, "Origin": ORIGIN}
                ).status_code
                == 403
            )
            assert (
                client.post(
                    "/api/auth/logout",
                    headers={
                        **cookies,
                        "Origin": "https://evil.example.test",
                        "X-CSRF-Token": csrf,
                    },
                ).status_code
                == 403
            )
            assert client.get("/api/missing", headers=cookies).status_code == 404
            page = client.get("/", headers=proxy)
            assert page.status_code == 200
            assert all(
                value not in page.content
                for value in (
                    password.encode(),
                    session.encode(),
                    csrf.encode(),
                    runtime_url.encode(),
                    PROXY.encode(),
                )
            )
            assert (
                client.post(
                    "/api/auth/logout",
                    headers={**cookies, "Origin": ORIGIN, "X-CSRF-Token": csrf},
                ).status_code
                == 204
            )
            native_login = client.post(
                "/api/auth/login",
                json={"password": password},
                headers={**proxy, "Origin": NATIVE_ORIGIN, "X-BrickVault-Login": "1"},
            )
            assert native_login.status_code == 200
            assert native_login.headers["access-control-allow-origin"] == NATIVE_ORIGIN
            assert native_login.headers["access-control-allow-credentials"] == "true"
            assert all(
                "Secure" in header
                for header in native_login.headers.get_list("set-cookie")
            )
            native_session = native_login.cookies.get("bva_session")
            native_csrf_cookie = native_login.cookies.get("bva_csrf")
            native_csrf = native_login.json()["csrf_token"]
            assert native_session and native_csrf_cookie and native_csrf
            native_cookies = {
                **proxy,
                "Cookie": f"bva_session={native_session}; bva_csrf={native_csrf_cookie}",
                "Origin": NATIVE_ORIGIN,
            }
            native_state = client.get("/api/auth/session", headers=native_cookies)
            assert native_state.status_code == 200
            assert native_state.headers["access-control-allow-origin"] == NATIVE_ORIGIN
            assert native_state.headers["cache-control"] == "no-store"
            for content, _media in application.state.build.values():
                assert all(
                    value not in content
                    for value in (
                        password.encode(),
                        session.encode(),
                        native_session.encode(),
                        csrf.encode(),
                        native_csrf.encode(),
                        runtime_url.encode(),
                        PROXY.encode(),
                    )
                )
            assert (
                client.post(
                    "/api/auth/logout",
                    headers={**native_cookies, "X-CSRF-Token": native_csrf},
                ).status_code
                == 204
            )
    finally:
        request_logger.removeHandler(handler)
        request_logger.setLevel(prior_level)
    formatted = "\n".join(SafeFormatter().format(record) for record in records)
    assert all(
        value not in formatted
        for value in (
            password,
            session,
            native_session,
            csrf,
            native_csrf,
            runtime_url,
            PROXY,
        )
    )


def main() -> None:
    with runner_lock():
        owned = instance("test")
        run_id = uuid4().hex
        stem = "p12" + run_id[:16]
        database = "brickvault_" + stem
        owner_role, runtime_role = (
            f"brickvault_{stem}_owner",
            f"brickvault_{stem}_runtime",
        )
        owner_password, runtime_password = secrets.token_hex(32), secrets.token_hex(32)
        owner_url, runtime_url = targets(
            stem, database, owner_password, runtime_password
        )
        marker = database_marker(owned, run_id)
        role_marker = database_marker(owned, run_id + ":role")
        journal = LOCAL / "runs" / f"{run_id}-production.json"
        before = owned.verify(required=False)
        running_before = bool(before and before["State"]["Running"])
        record: dict[str, object] = {
            "run_id": run_id,
            "purpose": "disposable-production-style-proof",
            "database": database,
            "roles": [owner_role, runtime_role],
            "running_before": running_before,
            "status": "starting",
            "leftovers": [],
        }
        write_record(journal, record)
        leftovers: list[str] = []
        try:
            owned.up()
            provision_proof_database(
                owned,
                database,
                owner_role,
                runtime_role,
                owner_password,
                runtime_password,
                marker,
                role_marker,
            )
            record["status"] = "migrating"
            write_record(journal, record)
            engine = create_database_engine(owner_url, "production", "owner")
            try:
                with engine.begin() as connection:
                    connection.execute(text("REVOKE ALL ON SCHEMA public FROM PUBLIC"))
                    connection.execute(
                        text(f'GRANT USAGE ON SCHEMA public TO "{runtime_role}"')
                    )
            finally:
                engine.dispose()
            migrate(
                owned, database, run_id=run_id, proof_targets=(owner_url, runtime_url)
            )
            record["status"] = "testing"
            write_record(journal, record)
            http_proof(owner_url, runtime_url, marker)
            record["status"] = "passed"
        except BaseException:
            record["status"] = "failed_or_interrupted"
            raise
        finally:
            try:
                owned.up()
                cleanup_proof_database(
                    owned, database, owner_role, runtime_role, marker, role_marker
                )
            except (DatabaseError, OSError, psycopg.Error):
                leftovers.append("recorded-proof-database-or-roles")
            try:
                if not running_before:
                    owned.stop()
            except (DatabaseError, OSError, psycopg.Error):
                leftovers.append("owned-test-service-state")
            record["leftovers"] = leftovers
            write_record(journal, record)
            print(
                json.dumps(
                    {
                        "proof_status": record["status"],
                        "leftovers": leftovers,
                        "ledger": str(journal.relative_to(ROOT)),
                    }
                )
            )
        if leftovers:
            raise DatabaseError(
                "Owned proof cleanup incomplete; inspect the exact private ledger."
            )


if __name__ == "__main__":
    main()
