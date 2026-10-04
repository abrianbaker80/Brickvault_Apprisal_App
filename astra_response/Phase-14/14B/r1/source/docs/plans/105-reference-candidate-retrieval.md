# Plan 105 — Phase 14B local candidate retrieval foundation

## Goal and user-visible outcome

Explicitly selected photos plus a short visible description produce a deterministic
candidate shortlist, a private offline HTML comparison and optional separate operator
notes. This is description-assisted retrieval. Image-only retrieval and fresh AI
verification are deferred.

## Why now

Phase 14A is closed as accepted feasibility evidence. Exact minifigure recognition
remains unqualified for production. A reviewable local matching baseline is useful
before any new model work. Wider Phase 14 remains IN PROGRESS.

## In scope

- Existing catalog set search and a small snapshot-scoped minifigure name helper.
- Three corrected, approved reference photographs and retained provenance/licenses,
  indexed privately under .local/recognition-14b.
- scripts/reference_candidates.py: compare, interactive review and reopen.
- Self-contained reports with embedded raster bytes, source credits, ranking reasons,
  missing views and explicit canonical-resolution state.

## Explicit non-goals

No provider/model/counting/embedding calls, downloads, new dependencies, image-only
matching, new catalog/crosswalk, mapping writes, migrations, production UI/deployment
or Phase 15/16. Ten consumed 14A attempts, ledger and reservations stay unchanged.

## Current repository state

Main baseline: 7149f83dd7a16092bc2dfa12cd1ab1935073f537. Accepted 14A r6:
2c71ad336424c8d4e7af6e8ed15279371afab578. Implementation remains uncommitted,
main unpushed and index empty. The three protected files remain unchanged/unstaged.

## Decisions and assumptions

- Registry entries are reference evidence, not independent canonical catalog records.
  Documentary photo-to-ID association does not verify concealed components.
- Query fields are positively selected. Expected labels, candidate IDs, revealing
  filenames and reviewer conclusions are excluded; selected text containing catalog
  IDs or paths is refused. Operator descriptions must independently describe visible
  evidence. Prior visual/text clues require explicit object/field/clue selection.
- Up to twelve unique text terms query set and figure names independently, with at
  most 100 results per term/type. Any saturated term result is marked truncated.
- Exact token overlap: name weight 3, visible/source-feature weight 2, exact name
  phrase bonus 6. Stable ties use exact kind/namespace/identifier. Scores are not
  calibrated confidence, visual compatibility or identity proof.
- Native accepted catalog identities are separate from external reference identifiers.
  Canonical projection reuses exact namespace/identifier resolution; there is no new
  provider crosswalk. The fourteen known missing mappings remain unresolved.
- Reference photos selected around a known example demonstrate software behavior,
  not independent retrieval accuracy or the broader 25–100-set evaluation.

## Data model and interface changes

FigureMatch plus PinnedCatalog.search_minifigures reuse existing name predicates and
accepted snapshot guards. New local retrieval/comparison models keep candidate,
canonical identity, source/reference evidence and operator assertion separate.
No HTTP contract or database schema changes.

Registry records retain names/features with source basis, exact whole-figure keys,
image hashes/paths, view coverage, source URLs and permission/attribution evidence.
Comparison JSON/HTML and append-only notes are protected local files. No original
prediction, confirmed label, reference record or scoring result is overwritten.

## Implementation sequence

1. Verify baseline/protected state and derive the small reference-only index.
2. Add read-only figure text querying, deterministic ranking and private rendering.
3. Add explicit provisional/compatible/none/insufficient/operator-known review notes.
4. Run six focused synthetic cases, targeted static checks and one local smoke.
5. Publish sanitized review evidence on astra-response; leave main uncommitted.

## Validation and acceptance

Six cases cover ranking/ties/no-match, missing images/exact namespace separation,
query leakage prevention, append-only ambiguous notes/operator assertions, escaped
offline rendering/input integrity and bounded snapshot-scoped figure queries.
One smoke uses retained references and an independently supplied visible description:
query, actual owned development catalog, shortlist, browser comparison, save/reopen
private note. This demonstrates the workflow without an accuracy benchmark.

## Security, privacy and integrity

Only explicit image paths are read. Reports embed bytes and escape private text;
CSP disables scripts, connections, external resources, forms and base URLs.
Attribution stays with images. No remote images load on opening a report.
Existing protected-file helpers enforce private ACLs and exclusive local writes.
No private images, query text, operator notes, credentials or asset paths are published.

Development access uses the established ownership/loopback/service guards, runtime
role, accepted nonsynthetic snapshot, 0017 schema and read-only transaction. Only an
existing service may start; its original stopped/running state is restored in finally.
No provisioning, grants, import, backup, migration or database mutation occurs.

## Failure modes, rollback and recovery

Missing permitted photos remain explicit coverage gaps. No-match and saturated
catalog term results are distinct. Changed image/permission bytes, invalid query or
note association fail closed. A partial private report can be inspected locally;
original evidence remains intact. Removing this uncommitted slice requires Brian's
separate instruction; no cleanup of unrelated work is automatic.

## Progress log

- [x] 2026-10-04: Scope and baseline verified; initial retrieval/comparison implementation.
- [x] Six synthetic cases passed (1.53 seconds); changed-file Ruff and strict mypy
  passed for seven Python files.
- [x] One real local catalog smoke produced eight candidates from a bounded pool of
  1,012. Two shortlisted entries had approved photographs; six had no reference
  image. Term-result caps were reached, so coverage is explicitly truncated.
- [x] Installed Edge loaded four embedded images and the separate saved/reopened
  insufficient-evidence note with zero external requests. Development returned to
  its original stopped state.
- [x] Windows report-directory creation was corrected to use the established private
  ACL helper after the initial note guard refused that new directory. The same report
  was retained; no second catalog query or source-evidence rewrite was needed.
- [x] Sanitized r1 review package prepared for astra-response; publication receipt
  is returned with the review link. Main remains uncommitted.

## Open questions and manual checks

Additional view coverage, image-driven retrieval and any fresh AI-verification scope
need separate decisions. No further reference sourcing is included here.

## Outcome and follow-up

READY FOR PHASE 14B FOUNDATION REVIEW after the affected checks and local smoke.
Three source-associated, CC BY 2.0 front photographs are available; all lack exposed
heads/rear views and verified canonical mappings. The selected clue came from one
explicitly selected retained visual-clue field; prior IDs, labels and answers were
excluded. This and the preselected references demonstrate behavior, not independent
retrieval accuracy. The saved note is a software smoke example, not Brian's identity
confirmation.

No production recognition capability or full Phase 14 completion is claimed.
Phase 14A scores, ten consumed attempts and retained reservations remain closed and
unchanged. New provider calls/spend: zero. Image-driven retrieval, more independently
selected evaluation coverage and any fresh AI-verification scope remain separate work.
