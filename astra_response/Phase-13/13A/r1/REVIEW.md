# Phase 13A — listing/image backend foundation r1

**READY FOR PHASE 13A REVIEW. Phase 13A IMPLEMENTED / READY FOR REVIEW.
Phase 13 IN PROGRESS. Phase 14 NOT STARTED.** Phase 12 remains ACCEPTED / CLOSED.

Source baseline: main `653fae52ef5cb852985e2c36039b20523776f3b9`; main remains uncommitted/unpushed with empty index.
The three protected dirty files remain byte-preserved and unstaged. This slice
implements the authorized local backend foundation only, with no production access.

- [Plan 103](Plan-103.md) and [proposed shipping policy](proposed-privacy-policy.md).
- [Architecture/data model](architecture-data-model.md) and [migration](migration.md).
- [Upload/receipt/order semantics](upload-semantics.md), [blob/thumbnail semantics](blob-thumbnail-semantics.md),
  and [report-only consistency](consistency-check.md).
- [Focused validation](validation.txt), [exact changed-file inventory](changed-files.txt),
  [cumulative patch](cumulative.patch) and [source-copy hashes](source-inventory.json).

Twenty-four changed files are copied under `files/`. Executable source, tests,
generated contracts, lock/config and new documents are exact. The workflow review
copy redacts one **unchanged historical** workstation ZIP path; its new status
lines and every other changed line remain exact in the cumulative patch. Top-level
Plan/policy copies adapt relative links. The preserved contract reference renders
repository-only link targets as code; its governing text is unchanged.
No private images or production data.

Fourteen focused cases passed, then eight affected cases passed after narrow
response/JSON-null constraint corrections. Ruff/format on 14 changed Python files,
mypy on 13 affected source files and generated-contract verification pass. Both
disposable PostgreSQL runs cleaned up completely. No broad suites or frontend/production release builds ran.

Deferred: polished browser upload UI (13B), shipping policy approval, Linux deployment
filesystem qualification and DB-plus-blob backup design. No provider/AI/recognition,
Android, crop, deletion/retention automation, production deployment or main commit.
