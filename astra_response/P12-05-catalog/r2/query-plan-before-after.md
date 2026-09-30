# Inventory-parts query plans — before and counterfactual evidence

The exact failing operation is `inventory_lines:parts`, sanitized SQL identity `d4665b50baf251a3f5e626d98a7a67128bba85a5d297df6cb564a9c4d98958de`. This comparison covers the full INSERT, including PostgreSQL triggers, rather than a SELECT-only proxy. First and last bounded plans passed; complete clean qualification passed.

## Baseline and complete unchanged INSERT

The isolated unmodified r6 baseline canceled this operation at **300.012128 seconds** under `statement_timeout=300000 ms`. Its estimated plan and the subsequently observed natural plan have the same 19-node shape. Relevant existing indexes are present; the inventory revision population is newly built with missing column statistics at this point. See [baseline plan](evidence/baseline-plan.json) and [baseline statistics](evidence/baseline-statistics.json).

| Plan observation | Estimate | Actual |
| --- | ---: | ---: |
| Final parts row producer | 8 rows | 1,557,375 rows |
| Intermediate part/part-color join | 2,282 rows | 51,595,923 rows |
| Revision snapshot scan | 41 rows | 47,452 rows |
| Parts staging native-key lookup | 1 row per probe | 1 row per probe, 1,557,375 loops |
| Large hash | 1 initial batch | 128 batches |
| Temporary reads / writes | — | 47,836 / 47,836 blocks |

The plan starts from a small estimated revision population, uses an indexed inventory lookup and inventory-parts lookup, then probes the staged part identity for each source line. A hash joins part-color identities on the part side before the final color restriction. That order creates large intermediate fan-out without changing the correct final parts count. The plan has no Sort, DISTINCT or Aggregate node.

The complete unchanged diagnostic INSERT used a **TEST-only 900000 ms ceiling** after the original timeout was reproduced. Its elapsed time was 415.631328 seconds and reported execution time 415.623399 seconds. The full candidate write rolled back.

| Measured timing | Seconds | Interpretation |
| --- | ---: | --- |
| Row-producing subtree | 44.825215 | Includes its joins, repeated index probes and spill. |
| ModifyTable | 275.278657 | Inclusive of producer and BEFORE-row guard time. |
| Snapshot guard | 59.234065 | Already included in ModifyTable; do not add it again. |
| Execution after ModifyTable | 140.344742 | Dominated by end-of-statement foreign-key checks. |
| Sum of ten FK trigger times | 138.416037 | Within the post-ModifyTable phase; remaining time includes execution overhead. |

The full insertion recorded 4,490,253 shared blocks read, 57,740,088 shared block hits, 22,149,424 WAL records and 5,533,152,645 WAL bytes. These totals describe this diagnostic run; they do not independently prove a particular storage bottleneck. The producer alone is substantially shorter than the complete constrained write. See [natural/counterfactual plans](evidence/probe-plans.json) and [probe summary](evidence/probe-summary.json).

## Statistics-only counterfactuals

| Isolated change | Estimated-plan change | Actual full-INSERT result |
| --- | --- | --- |
| ANALYZE revision only | Final estimate becomes 9,602; source parts are scanned and joined to part/color identities, then the existing inventory/revision indexes are used. | Timeout at 300.011897 seconds under 300000 ms. |
| ANALYZE inventory and revision | Final estimate remains 9,602; inventory and revision scans/hashes represent the 47,452-row population, with a different upstream join order. | Timeout at 300.020539 seconds under 300000 ms. |

Both counterfactuals are measurements of the complete INSERT with constraints enabled. Neither qualified the statement. Their execution followed earlier rolled-back inserts, which leave physical write bloat, and overlapped resource use from the failed-state clone. Consequently these measurements do not establish a clean relative-speed ranking, a statistics regression, or a claim that every possible statistics/query optimization has been exhausted. The source repair includes no new ANALYZE or planner setting.

## Bounded repair — source shape and measured plans

[The repaired builder](files/services/api/src/brickvault_api/catalog/builder.py) obtains the maximum staged physical row number, then executes the existing parts INSERT over disjoint predicates `row_number > lower` and `row_number <= upper`, with spans of 100,000. It changes statement extent while preserving all original joins, target columns, source flags, evidence, quantity separation and database constraints. All spans stay inside one outer construction transaction; no partial canonical candidate is committed.

The first and last bounded full-INSERT probes passed with BUFFERS/WAL/SETTINGS and actual execution of all eleven original trigger entries. No ANALYZE or timeout change was added for these probes. See [bounded plans and timings](evidence/batch-probe-summary.json).

| Metric | Unbounded natural INSERT | First bounded span | Last bounded span |
| --- | ---: | ---: | ---: |
| Data rows inserted | 1,557,375 | 99,999 | 100,000 |
| Largest emitted intermediate population | 51,595,923 | 99,999 | 100,000 |
| Captured plan nodes | 19 | 17 | 17 |
| Hash batches | 128 | 1 | 1 |
| Temp blocks read / written | 47,836 / 47,836 | 0 / 0 | 0 / 0 |
| Complete statement elapsed seconds | 415.631328 | 23.413110 | 21.765112 |
| Statement limit milliseconds | 900000, diagnostic only | 300000 | 300000 |

The first physical span includes the header position and correctly contains 99,999 data rows. The probes independently counted staged rows within each bound and required the inserted count to match. Both retain the indexed inventory/native-parts lookups but use indexed color lookups and the existing unique `(part_id,color_id)` identity index, avoiding the broad part-only fan-out. The smaller statement extent changed the selected plan without changing the original join rules or installing an index. Trigger work is fully included. Both writes rolled back and the logical failed audit/staging state remained unchanged.

These measurements compare statement extents as well as plans: they prove bounded statement margin for the tested first and last spans, not an end-to-end speedup or a guarantee for every intermediate batch. No sum of probe times is presented as a full-import estimate.

Real PostgreSQL 18 fixture execution passed twenty cases, including source-row coverage, sparse/multiline physical locators, and full candidate rollback after a first batch. [Fixture evidence](evidence/socket-recovery-tests.json) binds the current recovery/batching test bytes. [Normal package evidence](evidence/release-evidence.json) passed for the expected repaired candidate and confirms no production installation.

The repaired clean full-source import, independent semantic comparison and clean candidate-build repetition passed. [Full timing evidence](performance-evidence.md) records every named operation, row totals, observed variability and meaningful margin below the unchanged 300-second limit.

These diagnosis and full qualification results establish the narrow repair in isolation. No production ANALYZE, index change, timeout change, recovery, retry or activation was performed by this diagnosis.

Clean full-import maximum parts batch 29.471287 seconds; all named operations maximum 189.398854 seconds. Clean repeat maximum 196.324807 seconds, with matching native inventory digest set. Complete sanitized qualification plans and timing traces accompany this review.
