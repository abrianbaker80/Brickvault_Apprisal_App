"""Enumerated runtime grants shared by local proofs and production administration."""

import re

from sqlalchemy import Connection, text


def grant_runtime(connection: Connection, role: str) -> None:
    """Apply the reviewed least-privilege policy without default future-table grants."""
    if re.fullmatch(r"brickvault_[a-z][a-z0-9_]{0,50}_runtime", role) is None:
        raise ValueError("Invalid runtime role.")
    connection.execute(text(f'REVOKE ALL ON public.alembic_version FROM PUBLIC, "{role}"'))
    connection.execute(text(f'GRANT SELECT ON public.alembic_version TO "{role}"'))
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
            connection.execute(text(f'REVOKE ALL ON public."{name}" FROM PUBLIC, "{role}"'))
            if name in RUNTIME_CATALOG_TABLES:
                connection.execute(text(f'GRANT SELECT ON public."{name}" TO "{role}"'))
    from brickvault_api.market.models import (
        MARKET_TABLES,
        OPERATIONAL_TABLES,
    )

    if connection.scalar(text("SELECT to_regclass('public.auth_principal')")):
        for name, privileges in (
            ("auth_principal", "SELECT"),
            ("auth_control", "SELECT, UPDATE"),
            ("auth_session", "SELECT, INSERT, DELETE"),
        ):
            connection.execute(text(f'REVOKE ALL ON public.{name} FROM PUBLIC, "{role}"'))
            connection.execute(text(f'GRANT {privileges} ON public.{name} TO "{role}"'))
        connection.execute(
            text(f'GRANT UPDATE(last_activity_at,revoked_at) ON public.auth_session TO "{role}"')
        )

    if connection.scalar(text("SELECT to_regclass('public.deal_forecast')")):
        connection.execute(text(f'REVOKE ALL ON public.deal_forecast FROM PUBLIC, "{role}"'))
        connection.execute(
            text(f'GRANT SELECT, INSERT, UPDATE(saved_at) ON public.deal_forecast TO "{role}"')
        )
        for signature in (
            "forecast_clock()",
            "forecast_cleanup(uuid)",
            "forecast_lock_context(uuid)",
        ):
            connection.execute(text(f'GRANT EXECUTE ON FUNCTION public.{signature} TO "{role}"'))

    if connection.scalar(text("SELECT to_regclass('public.watchlist_item')")):
        connection.execute(text(f'REVOKE ALL ON public.watchlist_item FROM PUBLIC, "{role}"'))
        connection.execute(text(f'GRANT SELECT, DELETE ON public.watchlist_item TO "{role}"'))
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

    if connection.scalar(text("SELECT to_regclass('public.deal_lineage_metadata')")):
        connection.execute(
            text(f'REVOKE ALL ON public.deal_lineage_metadata FROM PUBLIC, "{role}"')
        )
        connection.execute(
            text(
                f"GRANT SELECT, INSERT(owner_id,root_forecast_id,note,source_url), "
                f'UPDATE(note,source_url,revision) ON public.deal_lineage_metadata TO "{role}"'
            )
        )

    if connection.scalar(text("SELECT to_regclass('public.hunt_run')")):
        connection.execute(text(f'REVOKE ALL ON public.hunt_run FROM PUBLIC, "{role}"'))
        connection.execute(
            text(
                f"GRANT SELECT, INSERT(id,owner_id,idempotency_key,request_digest,"
                f"run_version,sort_policy_version,default_sort_by,"
                f"default_sort_direction,settings_snapshot,candidate_count), "
                f'UPDATE(completed_at) ON public.hunt_run TO "{role}"'
            )
        )
    if connection.scalar(text("SELECT to_regclass('public.hunt_candidate')")):
        connection.execute(text(f'REVOKE ALL ON public.hunt_candidate FROM PUBLIC, "{role}"'))
        connection.execute(
            text(
                f"GRANT SELECT, INSERT(id,run_id,owner_id,candidate_position,"
                f"canonical_set_id,set_number,set_name,snapshot_version,snapshot) "
                f'ON public.hunt_candidate TO "{role}"'
            )
        )

    if connection.scalar(text("SELECT to_regclass('public.selling_profile')")):
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
            connection.execute(text(f'REVOKE ALL ON public.{table} FROM PUBLIC, "{role}"'))
            connection.execute(
                text(
                    f'GRANT SELECT, INSERT({insert_columns}), UPDATE({update_columns}) ON public.{table} TO "{role}"'
                )
            )
        connection.execute(text(f'GRANT DELETE ON public.selling_profile TO "{role}"'))

    for name in MARKET_TABLES:
        if (
            connection.scalar(
                text("SELECT to_regclass(:name)"),
                {"name": "public." + name},
            )
            is not None
        ):
            connection.execute(text(f'REVOKE ALL ON public."{name}" FROM PUBLIC, "{role}"'))
            privileges = "SELECT"
            if name in OPERATIONAL_TABLES and name != "provider_scope_state":
                privileges += ", INSERT, UPDATE"
            elif name == "market_observation":
                privileges += ", INSERT"
            connection.execute(text(f'GRANT {privileges} ON public."{name}" TO "{role}"'))
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

    if connection.scalar(text("SELECT to_regclass('public.product_refresh_operation')")):
        for name, columns in PRODUCT_COLUMNS.items():
            connection.execute(text(f'GRANT UPDATE({columns}) ON public.{name} TO "{role}"'))
        connection.execute(
            text(
                "GRANT INSERT(attempt_id,operation_id,item_type,item_no,item_name,classification,"
                "received_at,completed_at,adapter_version,normalization_version,evidence_digest,retained_until) "
                f'ON public.provider_discovery_evidence TO "{role}"'
            )
        )
        for signature in PRODUCT_FUNCTIONS:
            connection.execute(text(f'GRANT EXECUTE ON FUNCTION public.{signature} TO "{role}"'))
