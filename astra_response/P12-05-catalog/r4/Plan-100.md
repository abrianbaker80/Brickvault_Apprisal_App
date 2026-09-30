# ExecPlan 100 — Production catalog activation prerequisite

## Production continuation stopped before mutation, 2026-09-30

**BLOCKED — Step 4 detached repair approval cannot bind the failed run/candidate.
Catalog importer repair remains ACCEPTED / CLOSED. Production catalog activation
prerequisite BLOCKED; P12-05 BLOCKED; Phase 12 IN PROGRESS.**

Minimum live admission and exact failed-state admission passed. The exact retained
`p12-05-catalog-repair-r1` bundle passed manifest/source/wheel verification without
a rebuild. During preparation, inspection of the accepted
[approval validator](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/files/scripts/production_catalog.py#L231-L260) found only ten allowed fields: database,
purpose, repair/predecessor releases and manifests, source version/raw/provenance
digests, and migration head. It has no failed-run or candidate identity fields and
rejects extra fields. The continuation's Step 4 explicitly requires those identities
to be bound by that detached approval. Exact IDs supplied to a command are a
different binding mechanism and do not satisfy this required approval contract.

The continuation explicitly prohibits a new repair or improvised production fix.
No alternate approval, schema extension, wrapper patch or substitute artifact was
used. This conflict was discovered before the first production mutation; the
sequence stopped before Step 3's pre-recovery backup. Backups performed by normal
scheduled operations outside this slice are not counted as authorized slice runs.

| Gate | Result in this continuation |
| --- | --- |
| Exact retained artifact | PASS: release `p12-05-catalog-repair-r1`; manifest `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`; source ID `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344`; wheel `a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6` |
| Minimum live admission | PASS: expected VM 115, r6 current, revision 0016, admin/one owner, 13 health checks, retention READY, zero failed units/jobs/imports, trusted private HTTPS and loopback exposure |
| Storage headroom | PASS: 123,552,899,072 bytes free on database volume; database 3,140,015,807 bytes; release volume 20,942,417,920 bytes free |
| Exact failed-state admission | PASS: one provider/source/failed run/candidate, 12 files, exact 1,898,466 staging rows; audit/provenance/fingerprint unchanged; no canonical/validation/activation data; NULL active snapshot, generation 0 |
| Detached approval identity binding | BLOCKED: accepted validator has no failed-run/candidate fields and rejects additions |
| Pre-recovery backup | UNRUN: zero slice backup invocations |
| Repair installation / wrapper deployment / approval creation | UNRUN; local bundle verification alone passed |
| Guarded retirement / switch / one linked retry | UNRUN: zero invocations; the one authorized retry remains unused |
| Production statement timing / fingerprint continuity / structural validation | UNRUN: no production retry observation; accepted isolated evidence is unchanged |
| Activation / generation-one active catalog | UNRUN; active snapshot remains NULL, generation 0 |
| Installed number/name/detail/Watchlist/market behavior qualification | UNRUN; source-known set remains `75331-1`, The Razor Crest; no production application result claimed |
| Post-activation backup | UNRUN: zero slice backup invocations |
| Blocked-state preservation check | PASS: r6, original failed audit/candidate/source/files/counts/security/listeners/timeouts unchanged; all 13 health checks and active/enabled operational timers pass |

VM 115 already had eight CPUs and 16,384 MiB RAM at live admission. No allocation,
startup, PostgreSQL configuration, timeout, migration, grant, market-provider,
owner-state, client/device or Phase 13 changes were made. `statement_timeout`
remains 300,000 ms and `lock_timeout` 10,000 ms. Market observations remain zero.
WAN-forwarding inspection was not repeated after the stop; no fresh WAN gate is
claimed. Private IDs and protected configuration remain outside review evidence.

Only Plans 099/100/101 are changed on main. Main remains at
`0ea8e0e21156bebb9aa4150c270643a0a5d0d571`, index empty; all three protected dirty files retain their accepted
hashes and remain unstaged. The sanitized r4 publication includes the specific
approval contract proof and labels all downstream gates unrun. A separately
reviewed resolution of this approval-contract discrepancy is required before
production mutation. No repair or remaining P12-05 client gate starts here.

Earlier sections below retain dated implementation, authorization and evidence
history; this stopped-continuation status is current.

## Authorized catalog production continuation, 2026-09-30

Brian explicitly authorizes the accepted exact-artifact deployment, guarded
retirement of the preserved failed candidate, exactly one predecessor-linked
fresh retry, separate validated-snapshot activation, one pre-recovery and one
post-activation dual backup, and bounded installed search/detail/Watchlist
resolution. The catalog importer repair remains ACCEPTED / CLOSED. Catalog
activation production qualification is STOPPED / BLOCKED; P12-05 remains BLOCKED and
Phase 12 IN PROGRESS. This authorization supersedes the earlier production
continuation boundary below for this exact sequence only.

Main remains at `0ea8e0e21156bebb9aa4150c270643a0a5d0d571`, with an empty index
and the three protected files byte-identical and unstaged. Reuse accepted r2/r3
repair qualification. No rebuild, new repair, second retry, timeout/resource/
schema/grant change, manual production ANALYZE, market activation, client/device
acceptance, rollback/cold-start rehearsal or Phase 13 work is authorized.
Any stated stop condition preserves durable evidence and stops the sequence.
Sanitized stopped-continuation gate results are recorded above for catalog r4;
private identifiers and configuration stay in protected local production state.

## Accepted repair closeout, 2026-09-30

**Catalog importer repair ACCEPTED / CLOSED. Production catalog activation
prerequisite BLOCKED pending separately authorized production recovery/retry/activation.
P12-05 BLOCKED; Phase 12 IN PROGRESS.** Brian accepted the
[r2 repair package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/REVIEW.md)
and authorized only the exact 15-file local closeout checkpoint and r3 publication.
Reuse accepted r2 qualification; this closeout performs no live connections,
tests, builds, production recovery/retry/activation or candidate release install.
Remaining P12-05 client/device gates stay blocked. The implementation scopes,
repository snapshots and review-ready statements below are dated pre-closeout history.

## Goal and user-visible outcome

Activate exactly one accepted nonsynthetic Rebrickable catalog through the
existing importer and atomic activation path. Enable exact suffixed set search,
deterministic name search, Set Detail and Watchlist target resolution.
**Prerequisite BLOCKED — production import exceeded the existing statement
timeout. P12-05 BLOCKED; Phase 12 IN PROGRESS.** No snapshot was accepted or
activated. This plan records the stopped attempt and the separate repair gate.

## Why now

[Plan 099](Plan-099.md) established a healthy production
database and independent Google Drive restore, but zero catalog sets or active
snapshots. Brian separately authorized this catalog-only prerequisite on
2026-09-30. This is data activation, not a corruption, restore or schema repair.

## In scope

Verify retained official source and its demonstrated rights; add the smallest
guarded production invocation if required; verify live safety; take one normal
dual backup before import; parse, validate and activate one immutable snapshot;
qualify installed services; take one normal dual backup afterward; publish a
sanitized review package on `astra-response`.

## Explicit non-goals

No market credentials, price guides, provider dispatch, synthetic production
fixtures, image copying, migrations, database reset, runtime permission changes,
retention apply/prune, Phase 13, main commit/push, or remaining P12-05 browser,
PWA, Android, rollback, cold-start and full owner workflow gates.

## Current repository state

Branch `main`; HEAD `5c673e81a4f1caa13a0909a746d6ba0fffca075e`; empty index.
Pre-existing CODEX_WORKFLOW, ROADMAP and untracked Plan 099 record the blocker.
Protected dirty files verified against Plan 099 on entry:

| File | SHA-256 |
| --- | --- |
| AGENTS.md | F0A354ED80F631910F4CDCB64729209EF4758DE441F3EAAF509DA49395F969B4 |
| services/api/tests/integration/test_catalog_search.py | D06965D560361A06B7A33647EFA5B9B34829F8C34D5D912226D9CD5B3645ABF7 |
| services/api/tests/unit/test_catalog_parser.py | 0251B5C358CD37DE9E07E2CBDFB44913752CADE7050D9EB1B3A885F57D27A041 |

These remain byte-identical and unstaged throughout.

## Decisions and assumptions

Prefer retained accepted official source. The retained manifest declares provider
`rebrickable`, scope `full-catalog`, synthetic false, profile
`rebrickable-bulk-v3-2d.1`, and original acquisition on 2026-09-09. Revalidate all
twelve gzip datasets with the current parser, original acquisition receipt and
compressed/decompressed hashes before production mutation.

Use the original user-supplied first-party Downloads/Terms evidence from
2026-09-09, recorded in [the provider gate](r3-context.md#historical-local-source-references) and
[D-030](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/5c57731c7e15abdae5d6d1e5a35e46e602bc3618/docs/DECISIONS.md), only for the same retained source. This is not a claim
of newly verified provider policy. Metadata use requires Rebrickable attribution;
full-source redistribution and AI training remain excluded. Existing catalog
image references may remain under that evidence; no image bytes are acquired.

## Data model and API/interface changes

No schema or public API changes. `scripts/catalog.py` is development-only.
Any new root-only wrapper must load the existing protected production-admin
configuration, verify exact database/roles/marker/migration/one owner, require a
protected digest-bound official manifest and rights descriptor, reject all
partial or competing catalog state, and delegate all catalog mutations to the
existing `import_source` and `activate` functions. Preserve the immutable r6
release and runtime grants.

## Implementation sequence

1. Establish protected checkout and existing catalog/operations contracts.
2. Verify retained acquisition/rights, twelve source files, exact set suffix and
   required relationships; prepare protected manifest/approval evidence.
3. Implement and test the bounded production wrapper only if necessary.
4. Verify live r6, admin, services/listeners, owner/roles/revision, retention and
   conflicting jobs. Record protected comparison evidence.
5. Run exactly one normal dual pre-import backup with all receipt checks.
6. Import with existing staging, strict parsing, structural/candidate validation;
   require passed report. Activate using generation-0 compare-and-swap and a
   durable caller receipt. Inspect state after any ambiguous acknowledgement.
7. Qualify installed runtime search/detail and read-only Watchlist resolver;
   compare security state and preserve honest missing prices.
8. Run exactly one normal dual post-activation backup; inspect source counts and
   accepted snapshot identity alongside its protected receipt.
9. Update minimum status references; inspect cumulative diff/links/redaction;
   independently review and publish the r1 package without staging main.

## Validation and acceptance criteria

Use current parser validation of the exact source and focused wrapper pytest,
Ruff, format and strict mypy if source changes. No broad catalog suite reruns.
Require one nonsynthetic accepted active Rebrickable snapshot, one provider/source
version, positive set count, successful terminal import with no blocking errors,
exact `75331-1`, deterministic actual-name search, Set Detail provenance, honest
inventory/market state and Watchlist target resolution. Require live security and
operations checks plus both dual backup receipts. A full owner Watchlist add/read
test remains P12-05 when public authentication would require owner login.

## Security, privacy and data integrity

Source archives remain protected and outside web roots. Credentials, markers,
account identities, private source paths, recovery IDs and private IP/MAC values
never appear in review output. Root source files are digest verified and frozen
against change. Malformed/ambiguous source rows block import; they are not silently
discarded. Preserve provenance and unknown physical completeness/market evidence.

## Failure modes, rollback and recovery

Stop on rights/integrity failure, unsafe production state, import validation
failure, competing active pointers, failed qualification or failed backup. Never
retry a possibly committed import/activation blindly; inspect durable run and
activation receipt first. Preserve failed audit/staging state. No ad hoc SQL row
insertion, database reset, retention or automated rollback is authorized here.
The pre-import dual backup is the recovery point; restoration needs its own
reviewed execution when required.

## Progress log

- [x] 2026-09-30: Verified main HEAD, empty index and protected hashes; inspected
  current importer, manifest, acceptance/activation and production operations.
- [x] Located original retained official manifest and user-supplied rights evidence.
- [x] Current parser/receipt/source integrity and known-set preflight: all twelve
  datasets, 1,898,466 rows, original receipt and dual hashes passed; `75331-1`
  has one inventory and four directly recorded figure lots.
- [x] Guarded wrapper: 44 focused tests, Ruff, format and strict mypy targeting
  Linux passed on Windows (`--platform linux --follow-imports=silent`).
  Server preflight correctly rejected an application-owned source parent before
  database mutation. Dedicated root-owned source placement preserves all source
  bytes and runtime ownership; corrected server preflight passed.
- [x] Fresh live safety gate and exactly one pre-import dual backup passed: all
  three artifacts, six encrypted readbacks, both repository checks and protected
  receipt. A prior helper refusal occurred before any backup attempt; fresh
  read-only backup preconditions passed before the sole actual backup.
- [ ] Successful import and exactly one accepted activation.
- [x] Read-only stopped-state check: unchanged security and operations baselines,
  production-admin PASS, all 13 light checks PASS, retention READY, idle conflicting
  jobs and zero failed units. Runtime number and actual-name searches still return
  `catalog_unavailable`; successful search/detail/Watchlist qualification is UNRUN.
- [ ] Exactly one post-activation dual backup and catalog source-state evidence.
- [x] Terminal failed import inspected without retry, cleanup or activation.
- [ ] Documentation, independent review and sanitized r1 publication.

### Retained source and failed import evidence

Option 1 passed for the unchanged official nonsynthetic full-catalog source
`official-aa9a32c8fa634132b0c737680027853c`. Acquisition was
2026-09-09T21:48:35.294084Z through 21:48:39.552697Z; no separate provider
release timestamp was supplied. Importer version is `offline-catalog-2d.2`.

| Evidence | SHA-256 |
| --- | --- |
| Original manifest bytes | c4518012ab3c41da9538e08362bdb2294df9192b977496b6f18853b39da3c9ad |
| Manifest provenance | 619af89bce55b040d2d745541793c33254e559a883b94ec6c9ab61d644e17f15 |
| Original acquisition receipt | b2131cf8b57bedc1d12f72a9eddc531272a40ca5c6225699c08950943b436510 |
| Dated first-party rights input | b0fd9663b79acd0adb4e3a47f39436b7ab2123fe4b3033a33512f9af40264ec3 |

Current parser validation found zero parser errors and discarded no rows. The
existing importer has no quarantine table; blocking source errors stop import.
One database failure occurred during canonical build, before structural snapshot
validation. The sole import ran about 1,004 seconds and terminated with
`status=failed`, `stage=failed`, `failure_category=database_failure`.
PostgreSQL logged a correlated statement-timeout cancellation; the unchanged
owner connection limit is five minutes. Its last observed active query inserted
`catalog_inventory_line` rows. The exact query-plan/resource cause has not been
qualified; increasing the timeout is not a demonstrated root-cause repair.

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
| Total | 1,898,466 |

These are staging counts, not accepted imported catalog counts. The build
transaction rolled back: all canonical catalog identities, facts, inventory lines
and evidence have zero rows. One provider, source version, import audit and
unvalidated candidate snapshot remain, with twelve source files and the complete
staging dataset. The active-pointer row has null snapshot/activation and generation
zero. There are zero accepted snapshots, validation reports and activation receipts.
No failed-state cleanup or import/activation retry occurred.

### Qualification and recovery limits

The retained source contains exact `75331-1`, actual name `The Razor Crest`, one
inventory and four directly recorded minifigure lots. Installed production number
and actual-name searches still return `catalog_unavailable`. Set Detail and
Watchlist resolution could not pass and remain UNRUN; no owner session or temporary
Watchlist row was created. Market observations remain zero and no provider was
dispatched. Successful unavailable-price behavior is unqualified here; the
accepted manual sale-assumption path remains the later P12-05 economics path.

The sole pre-import dual backup passed for all three artifacts, six encrypted
readbacks, both repository checks and protected receipt. It represents the empty
pre-import catalog. Post-activation backup and its nonempty-catalog receipt checks
are UNRUN because activation never occurred. No second restore, retention apply,
prune, schema change, service restart or release update was performed. Source
archives remain protected outside the immutable web root; no provider credential,
image bytes or bulk source content entered the review package or client assets.

## Open questions and manual checks

No owner login is required for read-only Watchlist resolution. If retained source
cannot demonstrate rights, use current official-source verification under the
request's Option 2; stop on missing approved credential or unresolved rights.
Do not ask for credentials in chat. Full owner/browser/device acceptance stays
in Plan 099 after this prerequisite is accepted.

## Outcome and follow-up

**BLOCKED — production catalog import statement timeout.** The guarded invocation
and source preflight are implemented, but the production catalog prerequisite is
not IMPLEMENTED / READY FOR REVIEW as a successful activation. Publish its blocker
evidence under `astra_response/P12-05-catalog/r1/` on `astra-response`.

The next separately authorized work is a narrow importer performance diagnosis
and root-cause correction using isolated real PostgreSQL and the retained source,
with a reviewed policy for the preserved failed candidate/staging before any new
production attempt. Do not change timeout limits, redesign the importer or retry
production under this completed stopped slice. Main remains uncommitted and
unstaged; protected files remain unchanged. Resume Plan 099 only after successful
catalog activation and its prerequisite acceptance. P12-05 remains BLOCKED and
Phase 12 IN PROGRESS; no Phase 13 work began.


### Isolated importer repair qualification, 2026-09-30

Brian separately authorized [Plan 101](Plan-101.md)
for source repair and isolated PostgreSQL proof. The unmodified full-source
baseline identified inventory_lines:parts at 300.012128 seconds; a complete
isolated diagnostic INSERT took 415.631328 seconds, with 51.6 million intermediate
rows/hash spill and dominant constrained-write cost. Statistics alone did not
qualify it. The narrow same-transaction 100,000-physical-row span repair removed
the measured fan-out/spill in bounded plans while retaining all constraints and
catalog semantics; no migration or timeout change is needed.

One full retained-source linked retry passed: all 1,898,466 source rows, report
passed, candidate validated, parts batch maximum 29.471287 seconds, all named
operation maximum 189.398854 seconds. Clean
candidate-build repeat maximum 196.324807
seconds, identical native inventory digest set. Independent source/canonical
identity, suffix, quantities, inventory and nested-target equality passed;
75331-1/The Razor Crest/one inventory/four direct figure lots passed.
Guarded full failed-shape retirement and explicit predecessor-linked fresh retry
passed in isolation, preserving truthful original audit. Focused checks: 177 unit
and 20 real PostgreSQL tests, Ruff/format/strict mypy, normal package/release PASS.

**Catalog importer repair IMPLEMENTED / READY FOR REVIEW. Catalog prerequisite
BLOCKED pending ChatGPT acceptance and separately authorized production
continuation; P12-05 BLOCKED; Phase 12 IN PROGRESS.** Production remains exact r6,
0016, one owner, retention READY, zero failed units and unchanged failed
audit/candidate/staging, with no active catalog and unchanged 300000/10000 ms.
No production recovery/retry/activation or repaired release deployment occurred.
The accepted stopped-attempt history above remains intact; isolated proof does
not qualify installed catalog search/detail or the remaining Plan 099 gates.

## Source interface and audit addition

The repair adds `services/api/src/brickvault_api/catalog/recovery.py` and state-specific `recover-failed` and `retry-import` commands to `scripts/production_catalog.py`. The importer accepts an optional predecessor only for explicit linked retry. No public product API or recovery schema migration is introduced.

Choose guarded retire-and-fresh-retry rather than resuming the failed run. Existing triggers permit deletion of an unvalidated candidate and updates to counts metadata, while preserving failed-run provenance and prohibiting its deletion. Recovery atomically records the retired candidate/fingerprint and exact staging counts, deletes only the empty candidate and its exact run staging, and retains failed status/stage/reason/start/finish and original counts. A new attempt inserts its immutable predecessor; it does not rewrite the original failure as success.

Admission requires the exact one-provider/source/failed-run/candidate shape, twelve digest-bound source files and independently verified staging counts, zero canonical/fact/inventory/evidence/validation/activation rows, and an empty generation-zero pointer. Provider lock, row locks and one transaction cover retirement. Retry admission is repeated under the provider lock before new audit writes. Its fresh staged fingerprint must match the preserved candidate before build. Changed state, competing attempts and repeat recovery/retry refuse.

Wrapper authority, fixed protected configuration, release binding and dispatch have source/unit evidence. Real PostgreSQL and full-source proof execute the shared `recover_failed`, `admit_retry` and `import_source` transaction core on positively owned TEST databases; they do not execute the production wrapper against its fixed live paths or qualify a deployed repaired release. Production administration and installed product qualification remain distinct future gates.

## Exact release bridge

The root administration wrapper must use the exact prepared `p12-05-catalog-repair-r1` interpreter and reviewed release manifest. A root-protected detached repair approval supplies the final manifest digest after build and binds the following fixed contract:

- Production purpose and database.
- Repaired release identity and reviewed repaired manifest digest.
- Accepted `p12-04e-r6` predecessor identity and manifest digest.
- Exact approved retained source version and raw/provenance digests.
- Existing migration head `0016_hunt_cached_runs`.

The wrapper verifies existing production-admin identity/ownership/roles, root source and approval protection, official nonsynthetic source and rights binding, the shared maintenance flock, conflicting jobs and redacted failures. Owner connection grants and timeouts remain unchanged. Preparing a release beside the current release supplies the recovery library before deployment; it does not switch the runtime. This avoids loading repair code into an unreviewed old environment and avoids embedding the package's own final digest inside its manifest.

For `recover-failed`, current must remain exact r6 and both predecessor/candidate manifests must match. For `retry-import` and `activate`, current and interpreter must be the exact repaired release. Do not weaken those gates to run against an arbitrary release or source.

## Future separately authorized continuation

After accepted r2 repair review, obtain the distinct production continuation authorization. Its reviewed sequence is:

1. Prepare and verify the exact repaired release and detached approval beside r6; preserve the current runtime and grants.
2. Confirm the unchanged failed state and operations baseline; take the required pre-recovery dual backup.
3. Execute `recover-failed` once with the exact reviewed failed-run/candidate identities while r6 remains current. Inspect the truthful recovery metadata and deterministic empty retry state.
4. Switch production to the exact repaired release. This recovery implementation requires no migration; any independently needed migration must be explicitly reviewed and authorized before production application.
5. Execute exactly one `retry-import` with the reviewed predecessor. Require the unchanged source counts, matching semantic fingerprint, successful atomic construction and passed structural validation.
6. Activate only that exact validated candidate with generation-zero compare-and-swap and the reviewed caller receipt. Recover an ambiguous acknowledgement by reading durable state rather than blindly resending.
7. Take the separately authorized post-activation dual backup and qualify installed exact-number/name search, Set Detail and read-only Watchlist resolution.

If recovery acknowledgement is ambiguous, inspect the preserved failed run's retirement metadata and exact catalog state before any further action. If a retry fails, retain its truthful new audit/staging and stop for review; the one-predecessor recovery path deliberately refuses an additional blind attempt. Product/device gates and Phase 13 remain outside this sequence.
