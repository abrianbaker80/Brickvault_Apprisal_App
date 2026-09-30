# P12-05 catalog importer repair — ACCEPTED / CLOSED

**Catalog importer repair ACCEPTED / CLOSED. Production catalog activation
prerequisite BLOCKED pending separately authorized production recovery/retry/activation.
P12-05 BLOCKED; Phase 12 IN PROGRESS.** Brian accepted
[r2](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/REVIEW.md) and authorized this repair closeout only.

The one local main commit is `0ea8e0e21156bebb9aa4150c270643a0a5d0d571` — **Close P12-05 catalog importer repair**,
with parent `5c673e81a4f1caa13a0909a746d6ba0fffca075e`. Main was not pushed. The index is empty;
only the three protected files remain dirty and unstaged, with their accepted
SHA-256 values unchanged. The [exact 15-file inventory](committed-files.txt),
[committed blob hashes](committed-file-sha256.json) and
[local commit receipt](local-commit.json) record the checkpoint.

Closeout verified the exact staged inventory, inspected the complete staged diff
(3,505 lines), passed `git diff --cached --check`, resolved 231 local links in the
five changed Markdown documents, verified protected hashes and audited final
HEAD/index/worktree. All ten executable/test files match accepted r2; staging
normalized the importer's CRLF line endings to LF without changing its content.
The only new changes since r2 are the five additive
[status notices](status-only-changes.patch).
[Closeout validation](closeout-validation.json) records this scope.

[Final Plan 100](Plan-100.md), [final Plan 101](Plan-101.md) and supporting
[final Plan 099 context](Plan-099.md) are copies from this local commit with only
Markdown links rewritten for standalone review. Their earlier scopes and
repository-state statements remain dated pre-closeout history beneath the current
acceptance notice. No substantive qualification, independent review or build was
rerun; accepted r2 evidence is reused below. r1 and r2 are preserved.

## Accepted repair and qualification

The exact failing operation was `inventory_lines:parts`: the production-equivalent
baseline timed out at 300.012128 seconds and the complete unchanged isolated INSERT
took 415.631328 seconds. Severe planner underestimation produced 51.6 million
intermediate rows and hash spill, with substantial index/constraint/FK costs.
The repair divides only `inventory_parts` insertion into disjoint spans of
100,000 physical row numbers, preserving original joins, identity resolution,
evidence, quantities, flags, every constraint and trigger, and one atomic candidate
construction transaction. A later batch failure rolls back the entire build.
There is no timeout increase, migration, grant change or constraint relaxation.
[Root cause](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/root-cause.md) and
[query plans](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/query-plan-before-after.md) are accepted r2 evidence.

The full retained official source passed in isolated PostgreSQL: 12 datasets,
1,898,466 staged rows, report passed, candidate validated, no activation.
Parts-batch maxima were 29.471287 seconds and 29.894506 seconds on clean repeat;
maximum named operations were 189.398854 and 196.324807 seconds. The minimum
observed margin was 103.675193 seconds under unchanged
`statement_timeout=300000` and `lock_timeout=10000` ms.
[Complete performance evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/performance-evidence.md) is reused.

Independent native identity, inventory, relationship and quantity comparisons and
semantic equivalence passed; the fingerprint matches the failed candidate.
Required known-set evidence passed: `75331-1`, The Razor Crest, exactly one set,
one inventory and four directly recorded minifigure lots.
[Semantic equivalence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/semantic-equivalence.md) is reused.

Accepted validation is 177 focused unit/wrapper tests, 20 real PostgreSQL tests,
Ruff, format, strict mypy, normal package/frontend/release checks, exact source
reconstruction and [independent review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/independent-review.md),
all PASS. These are prior r2 results, not closeout reruns.
[Validation](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/validation.txt) and
[release proof](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/package-validation.json) remain the source evidence.

## Accepted failed-state recovery design

**GUARDED RETIRE + EXPLICIT PREDECESSOR-LINKED FRESH RETRY.** Admission must first
prove the exact failed state. The original attempt remains `status=failed` and
`stage=failed`; failure category, times, counts and provenance stay truthful.
An additive versioned retirement receipt records the exact retired candidate.
Only that candidate and its staging are removed; provider/source/source-file
provenance remains. Zero canonical/publication state and a NULL generation-zero
active pointer are required. Altered, extra, validated, accepted or active state,
concurrent/competing imports and blind repeat recovery refuse.

The fresh retry requires the exact recovered predecessor, stores `predecessor_id`
and must retain the retired candidate's semantic fingerprint. Existing structural
validation and activation stay unchanged. Real PostgreSQL recovery/refusal proof
and full retained-source retirement plus repaired linked retry passed in isolation.
[Recovery design and evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/failed-state-recovery.md) are reused.
Production recovery, retry and activation were not run.

## Candidate release identity

Accepted candidate: **p12-05-catalog-repair-r1**, qualified locally/isolated only.

| Identity | Accepted value |
| --- | --- |
| Source ID | `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344` |
| Manifest SHA-256 | `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36` |
| Wheel SHA-256 | `a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6` |

These are accepted pre-closeout artifact identities, recorded in
[candidate-release.json](candidate-release.json). No artifact was rebuilt,
recalculated, installed, switched or activated in closeout.

## Production continuation boundary

**Production continuation is NOT AUTHORIZED by this closeout.** Accepted r2's final
read-only evidence reports `p12-04e-r6`, migration `0016_hunt_cached_runs`, one owner,
retention READY, 13 health checks PASS, zero failed units, unchanged timeouts and
the preserved failed catalog shape: one provider/source, one failed run, one
unvalidated candidate, 12 source files, 1,898,466 staging rows, zero canonical
catalog data/validation/accepted snapshots/activation receipts and a NULL
generation-zero active pointer. [Production evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/production-readonly-state.md)
is accepted r2 history; production was not contacted or freshly checked here.

The future sequence in final Plan 100 needs separate explicit authorization:
prepare and verify the exact repair release and detached approval beside r6;
fresh pre-recovery dual backup; one guarded retirement while r6 stays current;
switch to the repaired release; exactly one predecessor-linked fresh retry;
exact validated-candidate activation; post-activation dual backup; installed
number/name search, Set Detail and read-only Watchlist qualification. Ambiguous
acknowledgements require durable-state inspection before further action.

No VM 115, PostgreSQL, Proxmox, Google Drive/restic, Rebrickable or Gmail contact
occurred during this closeout. No tests, lint, formatter, mypy, full imports,
performance probes, EXPLAIN ANALYZE, recovery tests, package/frontend builds,
production health/database checks, recovery/retry/activation or client/device
acceptance were rerun. The only network operation is authorized Git publication
to `astra-response`. Main remains local. Remaining P12-05 gates stay BLOCKED;
Phase 12 remains IN PROGRESS; Phase 13 did not start.
