"""Connections are supplied only by explicit, guarded migration tooling."""

from alembic import context
from sqlalchemy import Connection

connection = context.config.attributes.get("connection")
if not isinstance(connection, Connection):
    raise RuntimeError("Use the guarded database migration command.")
context.configure(connection=connection, target_metadata=None, version_table_schema="public")
with context.begin_transaction():
    context.run_migrations()
