# ExecPlan 101 — Catalog importer performance repair

## Goal and user-visible outcome

Identify and correct the exact full-source candidate-build bottleneck under the
unchanged 300-second statement limit. Prove the repair and a truthful, deterministic
failed-state recovery/retry lifecycle in isolated real PostgreSQL 18. This is
source and isolated qualification only; the production catalog remains unavailable.
**Catalog importer repair IMPLEMENTED / READY FOR REVIEW. Catalog prerequisite BLOCKED pending repair review; P12-05 BLOCKED; Phase 12 IN PROGRESS.**

## Why now

[Plan 100](100-production-catalog-activation.md) and its accepted
[r1 blocker](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/99bc5225686c42905930df545f8fc58d6b1a11ff/astra_response/P12-05-catalog/r1/REVIEW.md)
preserve the failed first production import. PostgreSQL confirmed statement timeout,
but the exact canceled operation and execution-plan cause were unqualified. Brian
explicitly authorized this bounded repair and isolated recovery proof on 2026-09-30.

## In scope

Read-only production diagnosis; named-statement mapping; isolated faithful baseline;
measured narrow performance correction; isolated full official-source qualification;
semantic equivalence; guarded recovery/retry source implementation and tests; normal
package/release qualification; sanitized r2 review publication.

## Explicit non-goals

No production ANALYZE, schema/index change, cleanup, recovery, retry, activation,
timeout increase, repaired release installation/switch, backup or retention operation.
No market acquisition, credentials, image bytes, Phase 13 or remaining Plan 099
browser/PWA/Android/rollback/cold-start gates. No main staging, commit or push.

## Current repository state

Main remains at `5c673e81a4f1caa13a0909a746d6ba0fffca075e`, index empty. Preserve
the six existing uncommitted r1 files: CODEX_WORKFLOW, ROADMAP, Plans 099/100 and
production_catalog wrapper/tests. The three protected dirty files retain Plan 100's
accepted SHA-256 values and remain byte-identical and unstaged.
Production remains r6, migration `0016_hunt_cached_runs`, one owner. Its exact
preserved state is one provider/source/failed run/unvalidated candidate, twelve
source files, 1,898,466 staging rows, zero canonical data/validation/acceptance/
activation and a NULL generation-zero active pointer.

## Decisions and assumptions

Use the exact retained official source already verified by r1; no acquisition or
rights expansion. Use installed PostgreSQL 18 on the same VM with a separate
task-owned data directory, database and Unix socket, no TCP listener and no
production credentials. Match production planner/resource settings where practical
and record differences. Existing BuildSteps/BuildInspector supply named timings,
rowcounts and query fingerprints without baseline code changes.

The isolated baseline identifies `inventory_lines:parts` as the canceled operation.
Its full INSERT cost, including indexes and constraints, exceeds the session's
five-minute limit. Missing revision statistics and a large join intermediate
contribute, but analyzing revision/inventory tables alone did not qualify the
operation. Bound the part INSERT by physical source-row ranges, retaining the
same outer candidate transaction, SQL relationships and constraint enforcement.

## Data model and API/interface changes

No public API, persistent schema, migration or runtime privilege change is required.
The recovery is guarded retire plus fresh retry: preserve failed audit
status/reason/provenance, record retired empty candidate metadata durably, remove
only its staging/candidate, and link a new run through existing predecessor_id.
Do not reopen or rewrite the failed run as successful. Existing counts metadata
holds an additive versioned retirement receipt; the existing immutable predecessor
column links a fresh attempt. PostgreSQL proof must precede review-ready status.

## Implementation sequence

1. Verify checkout/protected state; map current builder and transaction boundaries.
2. Capture production state/settings/schema/statistics using bounded read-only work.
3. Create task-owned socket-only PostgreSQL 18 and migrate current packaged schema.
4. Run unmodified full-source baseline at statement_timeout=300000/lock_timeout=10000;
   capture exact failing operation and sanitized transient-state plan.
5. Measure the cause in isolated rollback probes; diagnostic timeout expansion is
   allowed only there if essential to complete EXPLAIN ANALYZE.
6. Implement the smallest measured repair and focused regression checks.
7. Implement exact guarded recovery and explicit retry admission with truthful audit;
   test refusal cases and concurrency/transaction boundaries on real PostgreSQL.
8. Exercise recovery on the exact isolated failed shape, then one repaired full-source
   import under unchanged limits; prove every build statement has substantial margin.
9. Repeat the formerly slow build portion if needed; verify independently derived
   semantic counts, known-set relationships and deterministic fingerprints.
10. Run affected pytest/Ruff/format/strict mypy and normal package/release checks.
11. Stop/remove only task-owned isolated cluster artifacts; production final read-only
    equality/health/timeout checks; document and publish exact cumulative r2 package.

## Validation and acceptance criteria

Baseline must identify the exact failed named statement and explain production's
failure using data/plan/settings evidence. Repaired qualification must parse/stage
all 1,898,466 rows, build atomically and pass structural validation at unchanged
300-second limits with useful margin. Preserve source counts, exact suffix/name,
`75331-1` inventory and four direct minifigure lots, normal/spare separation,
distinct nested targets, canonical uniqueness, independent line counts and
deterministic semantic fingerprint behavior. Focused fixture tests complement
full-source evidence; they do not replace it.

Recovery must admit only the exact source-bound terminal failed state, preserve
audit, refuse any wrong source/count/canonical/validated/accepted/active/receipt/
competing state, refuse blind repetition, and establish deterministic fresh retry.
The new import must link to its failed predecessor and validate without stale
staging/candidate collisions. Production's failed state must remain unchanged.

## Security, privacy and data integrity

Production diagnostics run inside READ ONLY transactions with bounded timeouts;
EXPLAIN has no ANALYZE there. Never expose production secrets, markers, account
identities, private source locations, recovery IDs or private network identifiers.
Isolated plans can contain ephemeral UUID parameters; sanitize these before
publication. Keep raw source/plan state ignored and root-protected. Archive bytes
stay outside static content; no source rows enter telemetry or review output.

## Failure modes, rollback and recovery

Stop if the exact operation/cause cannot be established, repaired statements remain
near the timeout, semantics diverge, audit preservation is impossible, or a broad
redesign/correctness weakening is required. No timeout-only workaround. Isolated
diagnostic probes always roll back candidate writes and restore qualification
limits. Cluster cleanup verifies its exact task-owned path and identity first;
never target production data or credentials. Production recovery requires later
explicit authorization after r2 review.

## Progress log

- [x] 2026-09-30: Read repair authorization, verified accepted main HEAD/empty index,
  protected hashes and unchanged r1 dirty work; mapped existing telemetry hooks.
- [x] Read-only production configuration and preserved-state evidence: unchanged
  failed catalog state, all 13 health checks PASS, retention READY, failed units 0,
  owner timeouts 300000/10000 ms; accepted security and operational hashes match.
- [x] Disposable PostgreSQL 18.6 initialized with production UTF8/locale and
  planner settings, packaged migration head 0016, different task data/socket,
  no TCP listener and no production credentials in the importer connection.
- [x] Unmodified installed-r6 baseline: `inventory_lines:parts`, SQLSTATE 57014,
  statement timeout at 300.012128 seconds; total import 1007.719 seconds.
  All twelve datasets and 1,898,466 staged rows remain after atomic build rollback.
- [x] Full isolated INSERT EXPLAIN ANALYZE/BUFFERS/WAL/SETTINGS: 415.631328 seconds;
  51,595,923-row intermediate and 128 hash batches. Revision-only and revision plus
  inventory ANALYZE probes still time out at 300 seconds. Later probes have aborted
  write bloat and shared-host load, so they are insufficient qualification evidence.
- [x] Parts INSERT bounded to 100,000 physical row-number spans, same atomic build.
  First/last full-cost probes: 23.413110/21.765112 seconds at unchanged limits.
  Focused checks: 177 unit tests, Ruff/format/strict Linux-target mypy on ten files,
  20 real PostgreSQL 18 recovery/batching tests including sparse multiline locators,
  empty interior batches and rollback after the first batch.
- [x] Guarded failed-state recovery/retry source and focused real PostgreSQL proof.
  Full retained-source retirement and the explicitly linked retry also passed.
- [x] Full official-source qualification under unchanged limits with timing margin.
- [x] Semantic equivalence, repeat probe and package/release qualification.
- [x] Isolated cleanup, final production read-only equality and sanitized r2 review.

## Open questions and manual checks

No new provider access or owner login is needed. No migration is needed for this
repair. Future production continuation must separately
authorize backup if needed, recovery, repaired release/migration deployment, one
retry, activation, post-activation backup and search/detail qualification. Those
actions are not executable permission from this plan or its review publication.

## Outcome and follow-up

Source repair and isolated qualification are complete and ready for independent review.
Keep the live failed import untouched; Plan 099 remains blocked pending acceptance
and separately authorized production recovery, retry and activation.

### Existing transaction and statement map

`import_manifest` holds the provider's exclusive import advisory lock across the
attempt. Source headers and a new audit run commit first. Each dataset COPY commits
in batches of 10,000 rows, followed by an explicit staging-table ANALYZE. Bundle
checks and the sorted typed-row fingerprint run in their own transaction. The
candidate shell and building-stage audit transition then commit before construction.

All `build_candidate` writes share one transaction: the `evidence_conflict`,
`evidence_reconcile`, `evidence_insert` and changed-dataset `evidence_statistics`
steps; provider/canonical identity conflict, reconciliation, insertion and mapping
steps; facts and aliases; part/color construction; `inventories` and
`inventory_revisions`; `inventory_part_line_extent`, `inventory_lines:parts` and
its numbered batches, `inventory_lines:inventory_minifigs`
and `inventory_lines:inventory_sets`; `inventory_line_build_statistics`; streamed
inventory digest construction; `inventory_revision_statistics`; default inventories,
expansion bindings, elements and part relationships. A failed statement rolls back
that entire construction transaction, preserving the committed candidate shell and
staging. The failure audit is recorded afterward without marking the attempt successful.

On successful construction, a separate committed `inventory_line_statistics`
transaction prepares structural validation. Validation locks the candidate for
update, then commits its report, validated state and terminal success together.
Neither import nor validation activates a snapshot. Existing named `BuildSteps`
telemetry measures SQL/stream work and exposes sanitized SQL fingerprints without
source rows. Exact observed operation names, timings and plan evidence will complete
this map after baseline and repaired qualification.


### Qualified repair outcome, 2026-09-30

The full unchanged official source passed one normal repaired import on isolated
PostgreSQL 18.6 with statement_timeout=300000 and lock_timeout=10000 ms:
12 datasets, 1,898,466 staged rows, report passed, candidate validated, no activation.
Total retry import 1319.802 seconds; 16 parts batches, maximum
29.471287 seconds. Maximum named SQL/stream operation in full qualification:
189.398854 seconds. Clean candidate-build repeat:
933.770152 seconds overall, maximum named operation
196.324807 seconds. Worst observed margin below
300 seconds is 103.675193 seconds (34.56 percent). Timings
include complete writes/constraints; digest stream time overlaps its separately
timed COPY suboperations and is not additive independent SQL time.

Independent CSV-to-canonical equality passed all native identities/suffixes,
inventory owners/versions and source-line target/quantity tuples. Canonical counts:
110,970 core identities, 272,667 provider identities, 1,898,466 evidence rows,
47,452 inventory revisions and 1,588,405 lines. Exact 75331-1 is The Razor Crest,
one inventory, four direct minifigure lots; native figure quantities match.
Fingerprint `8f37571222fb078a2f75927ee1c58a7c3a90994bb24bee269270f784ebd48395` equals the unmodified failed candidate.
Native inventory digest set `cde10b1d49881bbea1006885a580bef4887119ae51fd05f9799807fb9eaf7a60` is identical
in a clean rebuild. No migration, new ANALYZE or timeout configuration change.

Guarded retirement passed against the exact full-source failed shape, preserving
historical status/stage/reason/provenance/times/counts except additive retirement
metadata. Explicit linked retry validated without stale staging/candidate collision
or active pointer. Twenty PostgreSQL tests passed: seventeen recovery/lifecycle
cases and three batching cases. Focused unit suite 177 PASS; Ruff/format and strict
Linux-target mypy on ten files PASS; normal wheel/sdist/frontend/release proof PASS.
The production wrapper's authority, fixed configuration, release bridge and
dispatch have source/unit evidence. Real PostgreSQL and full-source proof execute
the shared recovery/admission/importer core on owned TEST databases; they do not
execute the production CLI against its live fixed configuration or qualify a
deployed repair release.

Expected future release `p12-05-catalog-repair-r1`, source ID
`33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344`, manifest SHA-256
`02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`. Production is not installed or switched to it.
Final production read-only checks: exact r6/0016, one owner, retention READY,
all thirteen health checks PASS, zero failed units/running imports, unchanged
failed audit/candidate/full staging and NULL generation-zero pointer, identical
security/operations fingerprints and unchanged 300000/10000 ms limits. No production
cleanup/recovery/retry/activation/ANALYZE/schema/index/timeout/package/service/backup
or retention mutation occurred. Owned isolated databases and cluster were removed;
protected evidence and retained source preserved.

R2 publication must include full sanitized EXPLAIN JSON, complete named timing
traces and verified source reconstruction from accepted main. Main HEAD/index and
all three protected hashes remain unchanged; final reconstruction and publication
checks are recorded at the review boundary. Publication on astra-response is
review evidence, not production authorization.
[Plan 100](100-production-catalog-activation.md) records the concrete
separately authorizable release bridge and recovery/retry/activation continuation.
Catalog prerequisite and P12-05 remain BLOCKED; Phase 12 IN PROGRESS.
