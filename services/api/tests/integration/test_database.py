import time

import pytest
from sqlalchemy import Engine, text
from sqlalchemy.exc import DBAPIError, TimeoutError


def test_only_revision_table_and_effective_runtime_privileges(
    owner_engine: Engine, runtime_engine: Engine
) -> None:
    with owner_engine.connect() as connection:
        assert connection.scalars(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        ).all() == ["alembic_version"]
        assert (
            connection.scalar(text("SELECT version_num FROM public.alembic_version"))
            == "0001_foundation"
        )
        assert connection.scalar(text("SELECT current_setting('server_version')")).startswith(
            "18.6"
        )
    with runtime_engine.connect() as connection:
        assert (
            connection.scalar(text("SELECT version_num FROM public.alembic_version"))
            == "0001_foundation"
        )
        assert connection.execute(
            text(
                "SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication, rolbypassrls FROM pg_roles WHERE rolname=current_user"
            )
        ).one() == (False, False, False, False, False)
        for query in (
            "SELECT has_database_privilege(current_user, current_database(), 'CREATE')",
            "SELECT has_database_privilege(current_user, current_database(), 'TEMP')",
            "SELECT has_schema_privilege(current_user, 'public', 'CREATE')",
            "SELECT has_database_privilege(current_user, 'postgres', 'CONNECT')",
            "SELECT has_database_privilege(current_user, 'template1', 'CONNECT')",
            "SELECT has_table_privilege(current_user, 'public.alembic_version', 'INSERT,UPDATE,DELETE,TRUNCATE')",
        ):
            assert connection.scalar(text(query)) is False


@pytest.mark.parametrize(
    "statement",
    [
        "CREATE TABLE public.forbidden_product (id integer)",
        "CREATE TEMP TABLE forbidden_temp(id integer)",
        "UPDATE public.alembic_version SET version_num='bad'",
        "DELETE FROM public.alembic_version",
        "INSERT INTO public.alembic_version VALUES ('bad')",
        "TRUNCATE public.alembic_version",
        "ALTER TABLE public.alembic_version ADD COLUMN forbidden integer",
        "CREATE SCHEMA forbidden",
        "CREATE ROLE forbidden_role",
        "CREATE DATABASE forbidden_database",
        "GRANT brickvault_test_owner TO brickvault_test_runtime",
        "SET ROLE brickvault_test_owner",
    ],
)
def test_runtime_denied_actual_writes_and_ddl(statement: str, runtime_engine: Engine) -> None:
    with runtime_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        with pytest.raises(DBAPIError) as caught:
            connection.execute(text(statement))
        assert getattr(caught.value.orig, "sqlstate", None) == "42501"


def test_statement_and_pool_timeouts_are_bounded(runtime_engine: Engine) -> None:
    with runtime_engine.connect() as connection:
        assert connection.scalar(text("SHOW statement_timeout")) == "2s"
        started = time.monotonic()
        with pytest.raises(DBAPIError) as caught:
            connection.execute(text("SELECT pg_sleep(10)"))
        assert getattr(caught.value.orig, "sqlstate", None) == "57014"
        assert time.monotonic() - started < 4
    with runtime_engine.connect(), runtime_engine.connect():
        started = time.monotonic()
        with pytest.raises(TimeoutError), runtime_engine.connect():
            pytest.fail("Pool should be exhausted")
        assert time.monotonic() - started < 4


def test_owner_is_limited_to_database_schema(owner_engine: Engine) -> None:
    with owner_engine.connect() as connection:
        assert connection.execute(
            text(
                "SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication, rolbypassrls FROM pg_roles WHERE rolname=current_user"
            )
        ).one() == (False, False, False, False, False)
        assert (
            connection.scalar(text("SELECT has_schema_privilege(current_user, 'public', 'CREATE')"))
            is True
        )
        assert (
            connection.scalar(
                text("SELECT has_database_privilege(current_user, 'postgres', 'CONNECT')")
            )
            is False
        )


@pytest.mark.parametrize(
    "statement", ["CREATE DATABASE forbidden_owner_database", "CREATE ROLE forbidden_owner_role"]
)
def test_owner_denied_cluster_management(statement: str, owner_engine: Engine) -> None:
    with owner_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        with pytest.raises(DBAPIError) as caught:
            connection.execute(text(statement))
        assert getattr(caught.value.orig, "sqlstate", None) == "42501"


def test_default_table_privileges_do_not_grant_runtime_access(
    owner_engine: Engine, runtime_engine: Engine
) -> None:
    try:
        with owner_engine.begin() as connection:
            connection.execute(text("CREATE TABLE public.default_privilege_probe (id integer)"))
        with runtime_engine.connect() as connection:
            for privilege in (
                "SELECT",
                "INSERT",
                "UPDATE",
                "DELETE",
                "TRUNCATE",
                "REFERENCES",
                "TRIGGER",
            ):
                assert (
                    connection.scalar(
                        text(
                            "SELECT has_table_privilege(current_user, 'public.default_privilege_probe', :privilege)"
                        ),
                        {"privilege": privilege},
                    )
                    is False
                )
            with pytest.raises(DBAPIError) as caught:
                connection.execute(text("SELECT * FROM public.default_privilege_probe"))
            assert getattr(caught.value.orig, "sqlstate", None) == "42501"
    finally:
        with owner_engine.begin() as connection:
            connection.execute(text("DROP TABLE IF EXISTS public.default_privilege_probe"))
