from importlib.resources import files

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, create_engine

from brickvault_api.settings import Purpose, Role, validate_target


def migration_config() -> Config:
    config = Config()
    location = str(files("brickvault_api").joinpath("migrations"))
    # ConfigParser interprets percent signs; package paths are literal filesystem data.
    config.set_main_option("script_location", location.replace("%", "%%"))
    return config


def expected_revisions() -> tuple[str, ...]:
    return tuple(sorted(ScriptDirectory.from_config(migration_config()).get_heads()))


def create_database_engine(value: str, purpose: Purpose, role: Role = "runtime") -> Engine:
    target = validate_target(value, purpose, role)
    return create_engine(
        target,
        pool_size=2,
        max_overflow=0,
        pool_timeout=2,
        pool_pre_ping=False,
        hide_parameters=True,
        connect_args={
            "connect_timeout": 2,
            "options": "-c statement_timeout=2000 -c lock_timeout=2000",
            "sslmode": "disable",
            "gssencmode": "disable",
            "application_name": "brickvault-api",
        },
    )
