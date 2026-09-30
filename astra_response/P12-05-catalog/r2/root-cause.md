# Catalog importer root cause — measured diagnosis; repair qualified in isolation

The reproduced failing operation is `inventory_lines:parts`: the full parts `INSERT INTO catalog_inventory_line` in [builder.py](files/services/api/src/brickvault_api/catalog/builder.py). It exceeds the existing five-minute limit because one statement performs the complete 1,557,375-row parts write, including indexes, row guards and foreign-key checks. A badly underestimated join with intermediate fan-out and hash spill contributes additional work. These are measured costs; the repair does not infer the cause solely from production's last observed statement.

## Exact baseline reproduction

The isolated PostgreSQL 18 baseline used the installed unmodified r6 catalog modules, the unchanged twelve retained official datasets, and owner limits of `statement_timeout=300000 ms` and `lock_timeout=10000 ms`. All 1,898,466 source rows were staged. Instrumentation named each statement and captured its SQL digest; a TEST-only savepoint enabled evidence capture after cancellation without changing the importer’s outer rollback boundary.

The full import took **1,007.719 seconds** and failed at candidate-build step 147, `inventory_lines:parts`, after **300.012128 seconds**, with SQLSTATE `57014` and statement-timeout classification. The audit retained `database_failure`. There were 146 completed operations before it; the largest completed statement took 184.479999 seconds. The failed audit, candidate and staging were preserved, and candidate construction rolled back. No activation occurred. See [baseline summary](evidence/baseline-summary.json) and [baseline plan](evidence/baseline-plan.json).

The unchanged target statement has sanitized SQL identity:

`d4665b50baf251a3f5e626d98a7a67128bba85a5d297df6cb564a9c4d98958de`

This resolves the previously unproven operation identity. It is the parts statement, rather than the later `inventory_lines:inventory_minifigs` or `inventory_lines:inventory_sets` statements.

## Complete-plan observation

After reproducing the 300-second cancellation, an isolated diagnostic-only 900000 ms ceiling permitted one complete unchanged `EXPLAIN ANALYZE` INSERT, including BUFFERS, WAL, SETTINGS and triggers. All candidate writes rolled back afterward; no production setting changed. Its wall time was **415.631328 seconds** and PostgreSQL execution time was **415.623399 seconds**.

The row-producing subtree took **44.825215 seconds**. The inclusive ModifyTable node took **275.278657 seconds**, which already includes producer time and the **59.234065-second** snapshot-guard trigger. The remaining **140.344742 seconds** occurred after ModifyTable, dominated by end-of-statement foreign-key checks: their ten reported trigger times sum to **138.416037 seconds**. These overlapping timings must not be added as independent costs.

The producer created **51,595,923 intermediate rows**, against an estimate of **2,282**, before color filtering yielded the correct **1,557,375 final rows**. Its hash grew from one estimated batch to **128 batches**, with **47,836 temporary blocks read and written**. The parts staging lookup ran 1,557,375 times. The insertion emitted 22,149,424 WAL records and 5,533,152,645 WAL bytes in this diagnostic observation. The write/constraint path is the larger measured cost; the intermediate join and spill are real contributors, not evidence of duplicate final catalog lines. See [probe summary](evidence/probe-summary.json) and [probe plans](evidence/probe-plans.json).

## Root-cause questions evaluated

| Question | Evidence and conclusion |
| --- | --- |
| Missing or unsuitable index | Relevant indexes exist and match production. The plan uses revision snapshot/source, inventory primary-key, staging inventory-parts native-key and staging parts native-key indexes. A missing index is not established as the cause. A better index may alter the producer plan, but no new persistent index is justified by this evidence. |
| Join-key/index ordering | Typed joins use existing keys. The selected join order applies the color restriction after a large part-only fan-out. This is contributory; it does not explain the larger measured write/constraint cost by itself. |
| Stale or missing planner statistics | Newly built canonical inventory/revision/part-color relations lacked column statistics at this point. Revision estimates were 41 against 47,452 actual rows; source staging estimates were substantially accurate. Missing candidate-population statistics contributes to the poor plan. |
| Unnecessary repeated scans | There are 1,557,375 indexed part lookups and 47,452 inventory primary-key lookups. These repeated probes and intermediate processing are measured. No repeated full correlated scan is present in the target INSERT. |
| Correlated subquery behavior | The target parts INSERT has ordinary joins and no correlated subquery or LATERAL expression. Other builder operations have different shapes, but they are not this reproduced timeout. |
| Join/cardinality explosion | The measured 51.6-million-row intermediate is severe fan-out and underestimation. Final output still equals the parts source count; no semantic duplicate or skipped-row repair is permitted. |
| Expensive DISTINCT/GROUP/SORT | None appears in this target statement or its captured plan. Earlier builder statements use other operations, but this failure is not a DISTINCT, aggregation or sort timeout. |
| One giant safely partitionable INSERT | Confirmed: the complete 1.56-million-row constrained INSERT exceeds 300 seconds. Disjoint source-row spans can bound statement work while keeping every batch inside the existing atomic candidate transaction. This is the chosen narrow source repair. |
| Redundant identity resolution | The parts producer repeatedly resolves existing staged identities. No duplicated identity creation or incorrect mapping was found. A new identity-map architecture is not necessary for the bounded repair. |
| Constraint/index maintenance cost | Confirmed as the larger measured component: ModifyTable and end-of-statement foreign-key work greatly exceed producer time. Snapshot and foreign-key guards remain enabled; removing them is not a permissible fix. |
| Temporary-file/hash spill | Confirmed: 128 hash batches and 47,836 temporary blocks in each direction. This contributes producer overhead. No memory-setting increase is part of the repair. |
| Transaction design | The existing outer construction transaction correctly rolled back all canonical writes. Changing it to commit partial candidates would weaken correctness. The repair preserves that transaction and bounds statements within it. |
| Another measured cause | The full constrained write is larger than one accepted administration statement budget. The evidence does not isolate every residual write-path cost or prove a particular disk bottleneck; it supports bounding the complete statement rather than timing SELECT alone. |

## Statistics counterfactual and chosen repair

TEST-only revision statistics changed the plan, but the unchanged full INSERT still reached its 300-second limit at 300.011897 seconds. Refreshing both inventory and revision statistics also changed join choices but reached the limit at 300.020539 seconds. These runs followed rolled-back inserts that can leave physical heap/index bloat, and resource overlap with the failed-state clone is a comparison caveat. They are not a clean speed ranking or proof that statistics never help. They do show that statistics-only treatment did not qualify the full constrained statement in the observed environment.

The current source instead partitions only the parts insertion into disjoint **100,000-physical-row-number spans**. The same joins, targets, source locators, normal/spare quantities, flags, evidence, constraints and identity rules remain. A maximum source-row-number query bounds complete coverage, including gaps; no OFFSET pagination or selected-row limit can skip source positions. Every parts batch remains in the caller’s one candidate construction transaction. A later batch failure rolls back earlier batches and the rest of that candidate.

This repair adds no ANALYZE statement, migration, persistent index, timeout override or grant expansion. Existing statistics preparation remains. The linked failed-state recovery changes are described separately in [failed-state recovery](failed-state-recovery.md).

## Bounded probes and full qualification

The first and last 100,000-position spans passed as complete constrained INSERTs on retained TEST staging, with the unchanged 300000/10000 ms statement/lock limits and no additional statistics preparation:

| Probe | Source rows inserted | Elapsed seconds | Largest emitted plan-node population | Temporary blocks read / written |
| --- | ---: | ---: | ---: | ---: |
| First physical span | 99,999 | 23.413110 | 99,999 | 0 / 0 |
| Last physical span | 100,000 | 21.765112 | 100,000 | 0 / 0 |

The first span includes the header's physical position, so its 99,999 data rows are expected; the probe independently counted rows within each bound. Both plans contain 17 nodes and one-batch hashes. They use existing indexed color and `(part_id,color_id)` identity lookups, avoiding the natural full statement's 51,595,923-row intermediate and 128-batch spill. All eleven original trigger entries, including foreign-key checks, remain. Both probe writes rolled back, and the preserved failed audit/staging state remained unchanged. The larger observed bounded time is 23.413110 seconds, well below 300; these two probes establish margin for those spans, not yet every statement of a complete import. See [bounded full-INSERT probes](evidence/batch-probe-summary.json).

Real PostgreSQL 18 fixture execution passed **20 tests** in 43.64 seconds: seventeen recovery cases and three parts-batching cases. It used function-scoped owned databases, the matched current test bytes, no production credentials, and no TCP/provider connections. This proves focused state, coverage and rollback behavior; it does not substitute for full-source performance or semantic qualification. See [fixture results](evidence/socket-recovery-tests.json).

Normal package/release construction also passed for candidate `p12-05-catalog-repair-r1`, release source ID `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344`, manifest SHA-256 `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`. It was not installed in production. See [package evidence](evidence/release-evidence.json).

Clean full retained-source import, meaningful margin for every named operation under unchanged limits, independent semantic equivalence and clean candidate-build repetition passed. See [full performance evidence](performance-evidence.md) and [semantic equality](semantic-equivalence.md). No production retry occurred.

Clean full-import maximum parts batch 29.471287 seconds; all named operations maximum 189.398854 seconds. Clean repeat maximum 196.324807 seconds, with matching native inventory digest set. Complete sanitized qualification plans and timing traces accompany this review.
