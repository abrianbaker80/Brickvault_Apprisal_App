# Migration 0017_listing_images

Forward parent: 0016_hunt_cached_runs. Adds exactly six tables, supporting unique
indexes/typed/composite FKs, immutability and deferred receipt/hash/order checks.
Existing Phase 12 tables are not altered. Runtime grants are explicitly enumerated.
Packaged frozen up/down SQL follows the existing Alembic convention; runtime startup
never creates schema. The reverse migration drops only these six tables/functions.

Owned disposable PostgreSQL 18 proves fresh -> head, 0016 -> 0017 preserving auth
control data, and a single empty-table 0017 -> 0016 -> 0017 smoke. No large downgrade
campaign. Both test runs report passed/no leftover databases, and restore the prior
stopped state of the owned local TEST instance. No production migration or connection.
