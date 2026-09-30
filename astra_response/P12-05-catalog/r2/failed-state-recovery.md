# Guarded failed-state recovery and explicit retry — PASS in isolation

The implemented strategy is **guarded retirement followed by one explicit fresh retry**. Production recovery, retry, deployment and activation remain unauthorized in this repair slice. Isolated PostgreSQL 18 admission, audit preservation, refusal cases, full-source retirement and repaired linked retry passed. Production remains unchanged.

## Why retirement was chosen

A guarded resume would reuse the failed run for new construction. The existing importer creates a new attempt, and the historical run must retain its failed status, stage, failure category and original times. Reusing that attempt would blur its audit meaning and require a larger state-model change.

The existing schema already permits deleting a snapshot only while it is a candidate, updating an import run's counts metadata, and recording an immutable predecessor when inserting a new import run. Import-run deletion is prohibited. These rules support a smaller retire-and-fresh-retry implementation without a migration or grant change.

## Exact admission and atomic retirement

The library entry point is `recover_failed` in `services/api/src/brickvault_api/catalog/recovery.py`. It accepts a database context, reviewed manifest, independently verified dataset counts, and the exact failed run and candidate identifiers. It accepts no SQL or table-name arguments.

The database context must be owner-role production or an owned TEST context. The production wrapper additionally loads the existing protected administration configuration and runs its database identity, ownership marker, migration and role verification. It keeps the existing owner connection and timeout limits.

Before any retirement mutation, the library proves:

- One nonsynthetic Rebrickable source and provider, the approved full-catalog scope, and manifest provenance identical to the supplied manifest.
- Exactly twelve source files with the expected dataset names, dual digests, byte sizes, headers, encoding and source URLs.
- Exactly one original failed run, with failed stage, `database_failure`, matching parser/importer/application versions, no predecessor, and its original twelve dataset counts.
- Exactly one candidate bound to that run and source, still unvalidated, with no validation digest.
- Zero canonical identities, facts, inventories, lines, evidence, validation reports and activation receipts; one empty active pointer at generation zero.
- Every staging table's total equals its verified source count. Every staged row also belongs to the exact failed run, source and corresponding source file; matching global totals alone are insufficient.
- The candidate fingerprint equals the semantic fingerprint recomputed from its retained staging.
- No competing import holds the existing exclusive provider advisory lock.

Fixed-table counts fail closed on any additional catalog history or row. Retirement holds the exclusive provider lock and one database transaction, and locks the failed run and candidate for update. The transaction appends recovery metadata, deletes only that run's twelve staging populations and its empty candidate, then verifies the exact resulting retry state. Any refusal or database error rolls back all retirement writes.

## Truthful durable audit

The failed run retains its status, stage, failure category, start and finish times, source/version provenance, and original dataset counts. Only its counts JSON gains a versioned retirement receipt containing:

- The retired candidate's identity, semantic fingerprint, source, scope and creation time.
- The approved source version and manifest provenance digest.
- The exact retired staging counts and UTC recovery time.

Receipt validation requires the exact metadata shape, valid identities and fingerprint, UTC-aware times, candidate creation within the original run interval, and recovery no earlier than the original finish. The failed run is never marked successful or interrupted. Provider, source and source-file records remain. The retired state is deliberately unsuitable for blind repeat recovery.

## Fresh retry and activation

`admit_retry` validates the exact recovered predecessor and empty retry state. The production wrapper checks admission before reparsing. The importer repeats admission inside its exclusive provider lock and the same transaction that inserts the new attempt with its immutable predecessor. Explicit retries do not run the ordinary interrupted-run reconciliation first, so an unexpected running attempt is refused without changing its audit.

After fresh staging, `require_retry_fingerprint` requires the new semantic fingerprint to match the retired candidate before canonical construction. An importer-version or semantic divergence fails early and remains a truthful failed new attempt. The existing atomic candidate build, structural validation and explicit activation remain in use.

The wrapper accepts two-run activation history only when the successful candidate links to the exact recovered predecessor, the fingerprint matches, and the predecessor's staging is absent. It preserves the original exact-candidate, generation-zero compare-and-swap and receipt-recovery checks. Additional attempts, competing candidates, unbound history or retained old staging refuse.

## Release bridge and future authorization order

`scripts/production_catalog.py` uses the exact prepared `p12-05-catalog-repair-r1` release interpreter. A protected root-owned detached repair approval binds the reviewed repaired manifest digest, fixed release and predecessor identities, accepted predecessor manifest, database, migration and exact source raw/provenance digests. Keeping the final package digest outside its own package avoids a circular manifest dependency. The existing source-rights approval, protected-source checks, root requirement, maintenance flock, conflicting-service checks and redacted errors remain.

Future continuation must be separately reviewed and authorized in this order:

1. Prepare and verify the exact repaired release beside the accepted release; preparation does not switch the current runtime.
2. Take the required pre-recovery backup.
3. Run guarded retirement with the repaired candidate interpreter while exact `p12-04e-r6` remains current. The wrapper verifies both candidate and predecessor manifests.
4. Deploy by switching to the exact repaired release after recovery; apply a migration only if a separately reviewed repair requires one. This recovery implementation adds none.
5. Perform exactly one explicit predecessor-bound production retry. The wrapper requires the repaired release to be current.
6. Activate only the resulting fully validated exact candidate with the reviewed receipt; then perform the separately authorized post-activation backup and product qualification.

No step in that sequence has been executed against production in this repair slice.

## Validation status

The production wrapper's authority, protected approvals, release bridge, administration verification, maintenance lock and command dispatch are covered by source review and focused unit checks. The isolated PostgreSQL tests and full retained-source qualification use the shared recovery, retry-admission and importer transaction core on positively owned TEST databases. They do not execute or qualify the production CLI against its fixed production paths/configuration, and they do not qualify a deployed repaired release.

Focused final unit checks: **177 passed**. Real PostgreSQL checks: **20 passed** (17 recovery/lifecycle and 3 batching cases). Focused Ruff, format and strict Linux mypy checks passed. The integration test source covers full audit preservation, complete catalog-state equality after refusals, changed stored staging counts, unexpected canonical/evidence rows, wrong source/candidate/file bindings, validated and accepted candidates, valid activation receipts and active pointers, competing runs, a held import lock, malformed receipts, repeat recovery/retry, and actual importer-version divergence before candidate construction.

Activation-receipt refusal has its own count-gate coverage in `test_any_unexpected_catalog_row_refuses_retirement[catalog_activation]` and `test_recovered_retry_state_rejects_candidate_staging_or_extra_attempt[catalog_activation]`. The PostgreSQL recovery/retry integration test creates a real valid activation receipt and generation-one active pointer, requires recovery refusal, and compares every catalog row before and afterward. Receipt and pointer commit together under the existing database consistency triggers; a committed receipt with an empty pointer would be an invalid fixture. This separates the direct receipt-count guard from the valid persisted publication-state proof.

Full retained-source retirement passed in 51.039 seconds, preserving every failed audit field except additive counts metadata and preserving the original dataset counts. The subsequent normal predecessor-linked full-source import passed structural validation and reached validated candidate under 300000/10000 ms limits. The final read-only production check confirms unchanged failed state, r6, migration, security/operations and timeout policy. No production recovery or retry ran. See [retirement](evidence/full-source-recovery.json), [qualification](evidence/qualified-summary.json) and [PostgreSQL refusal cases](evidence/socket-recovery-tests.json).
