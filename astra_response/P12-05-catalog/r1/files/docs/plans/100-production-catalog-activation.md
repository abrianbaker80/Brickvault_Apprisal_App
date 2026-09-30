# ExecPlan 100 — Production catalog activation prerequisite

## Goal and user-visible outcome

Activate exactly one accepted nonsynthetic Rebrickable catalog through the
existing importer and atomic activation path. Enable exact suffixed set search,
deterministic name search, Set Detail and Watchlist target resolution.
**Prerequisite BLOCKED — production import exceeded the existing statement
timeout. P12-05 BLOCKED; Phase 12 IN PROGRESS.** No snapshot was accepted or
activated. This plan records the stopped attempt and the separate repair gate.

## Why now

[Plan 099](099-phase-12-production-acceptance.md) established a healthy production
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
2026-09-09, recorded in [the provider gate](../PHASE_2D_PROVIDER_GATE.md) and
[D-030](../DECISIONS.md), only for the same retained source. This is not a claim
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
