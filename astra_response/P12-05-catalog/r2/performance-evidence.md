# Full retained-source performance — PASS

The unmodified installed-r6 baseline failed in `inventory_lines:parts` at 300.012128 seconds; total attempt 1007.719 seconds. The complete isolated diagnostic INSERT required 415.631328 seconds at a TEST-only 900000 ms observation ceiling. No diagnostic timeout expansion was active in either repaired qualification.

One complete repaired predecessor-linked import parsed and staged all twelve datasets, **1,898,466 rows**, on a fresh marked PostgreSQL 18.6 TEST database with the normal packaged migration `0016_hunt_cached_runs`. Its initial state was a binary copy of the exact isolated failed audit/candidate/staging shape, with no canonical rows or aborted canonical heap/index bloat copied. Guarded retirement passed, then normal source parsing/staging, atomic candidate construction and structural validation completed. Report state is **passed**, candidate **validated**, activation absent. Total import time: **1319.802 seconds**. Recovery is separately timed at 51.039 seconds.

The repaired parts operation consists of sixteen physical row-number spans of at most 100,000. First-data/header offsets and the shorter last span preserve all 1,557,375 rows. Maximum part batch: **29.471287 seconds**; cumulative part batch time: 404.220506 seconds. Batching bounds individual statements; cumulative build work remains substantial and is reported separately.

| Qualification | Maximum named operation, seconds | Part-batch maximum, seconds |
| --- | ---: | ---: |
| Full normal retained-source retry | 189.398854 | 29.471287 |
| Clean repeated candidate-build portion | 196.324807 | 29.894506 |

Across these two clean construction observations, the worst named operation retains **103.675193 seconds (34.56%)** margin below 300 seconds. The formerly failing statement has far greater margin. This is observed same-host variability, not a guarantee for arbitrary source growth or hardware. The hard statement and lock limits remain 300000/10000 ms; no statement or lock timeout occurred.

The repeat used a newly migrated TEST database and binary-copied only verified source headers and typed staging, with fresh audit/candidate shells and empty canonical tables. It did not repeat the end-to-end CSV import. Construction took 933.770152 seconds. All candidate writes rolled back, the exact test database was removed, and its native inventory digest set matched the qualified result.

| Longest full-import named operations | Rows | Seconds |
| --- | ---: | ---: |
| candidate_build / part_color_observations:inventory_parts | 1557375 | 189.398854 |
| candidate_build / evidence_insert:inventory_parts | 1557375 | 126.617931 |
| candidate_build / inventory_digest_stream | 1635857 | 40.095728 |
| candidate_build / inventory_lines:parts:batch:9 | 100000 | 29.471287 |
| candidate_build / inventory_lines:parts:batch:15 | 100000 | 28.906307 |
| candidate_build / inventory_lines:parts:batch:11 | 100000 | 28.214946 |
| candidate_build / inventory_lines:parts:batch:13 | 100000 | 28.038126 |
| candidate_build / inventory_lines:parts:batch:14 | 100000 | 27.753850 |

Complete named SQL/stream operation timings, rowcounts, starts/finishes and fingerprints are in [qualification](evidence/qualified-summary.json), [complete build trace](evidence/qualified-events-trace.json), [repeat](evidence/confirm-summary.json) and [repeat trace](evidence/confirm-events-trace.json). The digest stream includes client iteration and its separately timed COPY suboperations; these overlapping measures must not be added as independent SQL time. Every underlying statement still uses the unchanged server ceiling.
