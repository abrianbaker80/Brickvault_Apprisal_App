# Production catalog import evidence

Status: **BLOCKED — PRODUCTION_CATALOG_IMPORT_DATABASE_FAILURE**.

One production import was attempted with the retained official, nonsynthetic
Rebrickable source `official-aa9a32c8fa634132b0c737680027853c`, profile
`rebrickable-bulk-v3-2d.1`, and existing importer `offline-catalog-2d.2`.
The protected manifest's raw SHA-256 is
`c4518012ab3c41da9538e08362bdb2294df9192b977496b6f18853b39da3c9ad`;
its application provenance digest is
`619af89bce55b040d2d745541793c33254e559a883b94ec6c9ab61d644e17f15`.
All twelve files passed the current parser, complete EOF, source counts and both
compressed/decompressed digest checks. Parser errors: **0**. Quarantined rows:
**0**; malformed source records are rejected by the existing importer, not silently
discarded. These results establish source integrity, not accepted catalog data.

| Dataset | Verified source and retained staging rows |
| --- | ---: |
| themes | 496 |
| colors | 275 |
| part_categories | 76 |
| parts | 64,620 |
| part_relationships | 37,394 |
| elements | 114,245 |
| sets | 28,278 |
| minifigs | 17,225 |
| inventories | 47,452 |
| inventory_parts | 1,557,375 |
| inventory_minifigs | 25,820 |
| inventory_sets | 5,210 |
| **Total** | **1,898,466** |

The import ended after **1,004.47 seconds** with durable run status/stage
`failed` and failure category `database_failure`. PostgreSQL independently
reported `canceling statement due to statement timeout`. The inherited owner
connection limits remained **300,000 ms statement timeout**, **10,000 ms lock
timeout** and **60,000 ms idle-in-transaction timeout**. No timeout was increased.
The cancellation record did not identify an operation table. The last observed
statement was an `INSERT INTO catalog_inventory_line`; the exact canceled build
step and its execution-plan cause remain unverified.

Current `catalog/builder.py` labels this family `inventory_lines:parts`,
`inventory_lines:inventory_minifigs` and `inventory_lines:inventory_sets`.
The parts producer joins staged membership to staged inventory ownership,
canonical inventory and the candidate revision, then exact staged part/color
identities and `part_color_identity`. It preserves normal versus spare quantities
and source evidence. The other producers use the same revision join and their
exact figure/set targets. No provider mapping or source redesign is implicated by
the available failure evidence.

Current `catalog/importer.py` commits provenance, staging batches and the empty
candidate record before enclosing **all candidate construction** in one separate
transaction. A construction statement failure rolls back its canonical identities,
facts, inventory and evidence together. The importer then records the failed run
outside that rolled-back transaction. Final readback confirms one provider, one
source version, twelve source files, one failed run and one unvalidated `candidate`,
with **zero canonical identities, facts, inventory lines or catalog evidence**.
All 1,898,466 staged rows and audit records remain preserved.

Candidate structural validation/report: **UNRUN**, with zero validation records.
Acceptance and activation: **UNRUN**. No import retry, cleanup or ad-hoc SQL repair
occurred. The next bounded repair requires evidence of the failing candidate SQL
operation and its plan/constraint costs under the existing limits, followed by a
reviewed root-cause correction and proportionate verification. A query-plan cause
has not been established, and another production import is not authorized by this
failed result.
