"""Optional private listings and immutable image ingestion receipts."""

from brickvault_api.migrations.catalog_ddl import execute_resource

revision = "0017_listing_images"
down_revision = "0016_hunt_cached_runs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    execute_resource("0017_listing_images_up.sql")


def downgrade() -> None:
    execute_resource("0017_listing_images_down.sql")
