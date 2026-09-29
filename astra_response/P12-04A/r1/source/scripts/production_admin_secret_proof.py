"""Explicit local PostgreSQL 18 proof of credential SQL and logging controls.

Run with the API virtualenv's Python. This creates one uniquely owned Docker
container from the already cached, repository-pinned image and removes only
that container. It never connects to a production server or an existing test
database. Only sanitized proof results are written under .local.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import socket
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import psycopg
from brickvault_api import production_admin as admin
from brickvault_api.auth import PASSWORDS
from brickvault_api.settings import reject_pg_environment
from database import IMAGE, ROOT, local_context
from psycopg import sql
from psycopg.rows import dict_row


class ProofError(RuntimeError):
    """Failure messages must never contain SQL, logs, passwords or verifiers."""


def _docker(context: str, *args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["docker", "--context", context, *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        check=False,
    )
    if result.returncode:
        raise ProofError("Local Docker operation failed; output withheld.")
    return result.stdout + result.stderr


def _port() -> int:
    for candidate in range(55434, 55444):
        try:
            with socket.socket() as probe:
                if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                    probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                probe.bind(("127.0.0.1", candidate))
                return candidate
        except OSError:
            continue
    raise ProofError("No approved disposable loopback port is free.")


def _owned(context: str, name: str, owner: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = json.loads(
        _docker(context, "container", "inspect", name)
    )
    if (
        len(rows) != 1
        or rows[0]["Name"] != "/" + name
        or rows[0]["Config"]["Labels"].get("app.brickvault.secret-proof") != owner
        or rows[0]["Config"]["Image"] != IMAGE
        or any(item.get("Type") == "volume" for item in rows[0]["Mounts"])
    ):
        raise ProofError("Disposable container ownership differs; cleanup refused.")
    return rows[0]


def _connect(port: int, user: str, password: str | None = None) -> Any:
    return psycopg.connect(
        host="127.0.0.1",
        port=port,
        dbname="postgres",
        user=user,
        password=password,
        autocommit=True,
        row_factory=dict_row,
        connect_timeout=2,
        sslmode="disable",
        gssencmode="disable",
    )


def _expect_error(
    connection: Any, statement: Any, code: str, params: Any = None
) -> None:
    try:
        connection.execute(statement, params)
    except psycopg.Error as error:
        if error.sqlstate != code:
            raise ProofError(
                "SQL failure did not have the expected category."
            ) from None
    else:
        raise ProofError("Expected SQL failure did not occur.")


def prove() -> Path:
    reject_pg_environment()
    context = local_context()
    image = json.loads(_docker(context, "image", "inspect", IMAGE))[0]
    if image["Os"] != "linux" or IMAGE.split("@", 1)[1] not in image["RepoDigests"][0]:
        raise ProofError("Cached PostgreSQL image identity differs.")
    run_id = uuid4().hex
    name = "bva-secret-proof-" + run_id
    bootstrap = "proof_bootstrap_" + run_id[:12]
    login = "proof_login_" + run_id[:12]
    owner_role = "proof_owner_" + run_id[:12]
    port = _port()
    receipt = ROOT / ".local" / "p12-04a-secret-proof" / run_id / "result.json"
    receipt.parent.mkdir(parents=True, exist_ok=False)
    result: dict[str, Any] = {
        "run_id": run_id,
        "started_at_utc": datetime.now(UTC).isoformat(),
        "image": IMAGE,
        "target": "new disposable local container; loopback only",
        "port": port,
        "production_access": False,
        "status": "FAILED",
        "checks": [],
        "container_removed": False,
    }
    created = False
    primary_error: BaseException | None = None
    sensitive: list[str] = []
    controls = ["SAFE_SQL_CONTROL_" + run_id, "SAFE_ERROR_CONTROL_" + run_id]
    try:
        _docker(
            context,
            "run",
            "--detach",
            "--pull",
            "never",
            "--name",
            name,
            "--label",
            "app.brickvault.secret-proof=" + run_id,
            "--restart",
            "no",
            "--memory",
            "512m",
            "--cpus",
            "1",
            "--tmpfs",
            "/var/lib/postgresql:rw,nosuid,nodev,size=384m",
            "--publish",
            f"127.0.0.1:{port}:5432",
            "--env",
            "POSTGRES_USER=" + bootstrap,
            "--env",
            "POSTGRES_DB=postgres",
            "--env",
            "POSTGRES_HOST_AUTH_METHOD=trust",
            IMAGE,
            "postgres",
            "-c",
            "shared_buffers=32MB",
            "-c",
            "log_statement=all",
            "-c",
            "log_min_error_statement=error",
            "-c",
            "log_min_messages=warning",
            "-c",
            "log_error_verbosity=verbose",
            "-c",
            "log_min_duration_statement=0",
            "-c",
            "log_min_duration_sample=0",
            "-c",
            "log_statement_sample_rate=1",
            "-c",
            "log_transaction_sample_rate=1",
            "-c",
            "log_duration=on",
            "-c",
            "log_parameter_max_length=-1",
            "-c",
            "log_parameter_max_length_on_error=-1",
            "-c",
            "debug_print_parse=on",
            "-c",
            "debug_print_rewritten=on",
            "-c",
            "debug_print_plan=on",
        )
        created = True
        item = _owned(context, name, run_id)
        if item["HostConfig"]["PortBindings"] != {
            "5432/tcp": [{"HostIp": "127.0.0.1", "HostPort": str(port)}]
        }:
            raise ProofError("Disposable container is not exclusively loopback-bound.")
        deadline = time.monotonic() + 45
        while True:
            try:
                connection = _connect(port, bootstrap)
                break
            except psycopg.OperationalError:
                if time.monotonic() >= deadline:
                    raise ProofError(
                        "Disposable PostgreSQL did not become ready."
                    ) from None
                time.sleep(0.5)
        with connection:
            identity = connection.execute(
                "SELECT current_setting('server_version_num')::integer AS version,"
                "current_setting('data_directory') AS data,current_user AS role"
            ).fetchone()
            if (
                identity["version"] != 180006
                or identity["role"] != bootstrap
                or identity["data"] != "/var/lib/postgresql/18/docker"
            ):
                raise ProofError("Disposable PostgreSQL identity differs.")
            result["postgres_version_num"] = identity["version"]
            # Trust is confined to the synthetic bootstrap identity. All new
            # login roles must complete SCRAM; no real credential is involved.
            hba = (
                "local all all trust\n"
                f"host all {bootstrap} 0.0.0.0/0 trust\n"
                "host all all 0.0.0.0/0 scram-sha-256\n"
            )
            _docker(
                context,
                "exec",
                "--interactive",
                name,
                "sh",
                "-c",
                'cat > "$PGDATA/pg_hba.conf"',
                input_text=hba,
            )
            connection.execute("SELECT pg_reload_conf()")
            rules = connection.execute(
                "SELECT auth_method FROM pg_hba_file_rules WHERE type='host' ORDER BY rule_number"
            ).fetchall()
            if rules != [{"auth_method": "trust"}, {"auth_method": "scram-sha-256"}]:
                raise ProofError("SCRAM host authentication rule differs.")
            connection.execute(
                sql.SQL("SELECT {}::text").format(sql.Literal(controls[0]))
            )
            _expect_error(
                connection,
                sql.SQL("SELECT {}::integer").format(sql.Literal(controls[1])),
                "22P02",
            )
            iterations = admin._credential_session_guard(connection)
            password = secrets.token_hex(32)
            verifier = admin._scram_verifier(
                password, iterations, secrets.token_bytes(16)
            )
            account_password = secrets.token_urlsafe(32)
            account_hash = PASSWORDS.hash(account_password)
            sensitive.extend((password, verifier, account_password, account_hash))
            statement = sql.SQL(
                "CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE "
                "NOREPLICATION NOBYPASSRLS PASSWORD {}"
            ).format(sql.Identifier(login), sql.Literal(verifier))
            connection.execute(statement)
            _expect_error(connection, statement, "42710")
            result["checks"].append("credential_guard_and_role_success_duplicate_error")
            with _connect(port, login, password) as authenticated:
                if authenticated.execute("SELECT current_user AS role").fetchone() != {
                    "role": login
                }:
                    raise ProofError("SCRAM authenticated an unexpected role.")
            incorrect = secrets.token_hex(32)
            sensitive.append(incorrect)
            try:
                wrong_connection = _connect(port, login, incorrect)
            except psycopg.OperationalError:
                # A successful connection immediately afterwards distinguishes
                # authentication refusal from a general outage.
                with _connect(port, login, password) as authenticated:
                    authenticated.execute("SELECT 1")
            else:
                wrong_connection.close()
                raise ProofError("Incorrect SCRAM password was accepted.")
            result["checks"].append(
                "scram_correct_password_success_incorrect_password_refused"
            )
            connection.execute(
                sql.SQL("CREATE ROLE {} NOLOGIN").format(sql.Identifier(owner_role))
            )
            connection.execute(
                "CREATE TABLE public.credential_proof(id integer PRIMARY KEY, "
                "password_hash text NOT NULL CHECK (password_hash LIKE '$argon2id$%'))"
            )
            connection.execute(
                sql.SQL("ALTER TABLE public.credential_proof OWNER TO {}").format(
                    sql.Identifier(owner_role)
                )
            )
            connection.execute(
                sql.SQL("SET ROLE {}").format(sql.Identifier(owner_role))
            )
            admin._verify_credential_logging(connection)
            if connection.execute("SELECT current_user AS role").fetchone() != {
                "role": owner_role
            }:
                raise ProofError("Guarded role switch failed.")
            insert = (
                "INSERT INTO public.credential_proof(id,password_hash) VALUES (%s,%s)"
            )
            connection.execute(insert, (1, account_hash))
            _expect_error(connection, insert, "23505", (1, account_hash))
            result["checks"].append("owner_role_guard_and_hash_insert_success_error")
    except BaseException as error:  # noqa: BLE001 - clean up on interruption without exposing driver details.
        primary_error = error
        result["failure_category"] = type(error).__name__
    finally:
        try:
            if created:
                item = _owned(context, name, run_id)
                _docker(context, "stop", "--time", "10", item["Id"])
                logs = _docker(context, "logs", item["Id"])
                result["log_bytes"] = len(logs.encode("utf-8"))
                result["log_sha256"] = hashlib.sha256(logs.encode("utf-8")).hexdigest()
                result["control_markers_present"] = all(
                    value in logs for value in controls
                )
                result["sensitive_values_scanned"] = len(sensitive)
                result["sensitive_log_matches"] = sum(
                    value in logs for value in sensitive
                )
                if primary_error is None and (
                    not result["control_markers_present"]
                    or len(sensitive) != 5
                    or result["sensitive_log_matches"] != 0
                ):
                    primary_error = ProofError(
                        "Log control or credential redaction proof failed."
                    )
                    result["failure_category"] = "LogVerificationFailure"
                _owned(context, name, run_id)
                _docker(context, "rm", item["Id"])
                result["container_removed"] = True
        except BaseException as error:  # noqa: BLE001 - retain a sanitized cleanup receipt on every failure.
            result["cleanup_failure_category"] = type(error).__name__
            if primary_error is None:
                primary_error = error
        result["finished_at_utc"] = datetime.now(UTC).isoformat()
        if primary_error is None and result["container_removed"]:
            result["status"] = "PASS"
        receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if primary_error is not None:
        raise ProofError(
            "Disposable credential proof failed; inspect the sanitized receipt."
        ) from None
    return receipt


if __name__ == "__main__":
    try:
        report = prove()
    except Exception:  # noqa: BLE001 - driver errors can contain synthetic credentials.
        print(
            "Disposable credential proof failed; sensitive details withheld.",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    print(
        f"PASS: disposable PostgreSQL credential/log proof; {report.relative_to(ROOT)}"
    )
