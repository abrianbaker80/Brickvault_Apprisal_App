"""Append-only actual outcomes for an existing saved forecast lineage."""

from brickvault_api.migrations.catalog_ddl import execute_resource

revision = "0018_deal_outcome_revisions"
down_revision = "0017_listing_images"
branch_labels = None
depends_on = None


def upgrade() -> None:
    execute_resource("0018_deal_outcome_revisions_up.sql")


def downgrade() -> None:
    execute_resource("0018_deal_outcome_revisions_down.sql")
