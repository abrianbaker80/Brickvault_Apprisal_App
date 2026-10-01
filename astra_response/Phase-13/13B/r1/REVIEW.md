# Phase 13B — ready for review

**Phase 13A ACCEPTED / CLOSED. Phase 13B IMPLEMENTED / READY FOR REVIEW.
Phase 13 IN PROGRESS. Phase 14 NOT STARTED.**

Private Listings create/list/detail, persisted galleries, original viewing and a
two-upload queue are implemented. File identity, bytes and selected position stay
stable on retries. Successful uploads are not resent after another file fails.
No recognition, native capture, providers, source fetching or production work.

Accepted 13A source is checkpointed locally as `d14002e244434123dc68b57aefda004a00aa8e89`,
`Implement Phase 13A image ingestion backend`. Exact 24-file inventory and complete
staged changed lines match accepted r1; whitespace, 242 links and protected hashes
passed. No 13A validation reran for closeout; main was not pushed.

13B candidate baseline is that local commit; all [11 changed files](changed-files.txt)
remain uncommitted on main. Index empty; three protected files byte-identical and
unstaged. No migration, accepted generated-contract, dependency or lockfile change.
One required backend adjustment explicitly admits the two new static shell routes,
excluded from OpenAPI, after local integration exposed the missing route.

Read [Plan 103](Plan-103.md), [UI summary](ui-summary.md),
[queue/retry semantics](queue-retry-semantics.md), [focused validation](focused-validation.md)
and the [cumulative 13B patch](cumulative-13B.patch).
Exact executable source/tests and changed docs are under `files/`.
Repository-relative links in those copies retain source context. The workflow copy
redacts one unchanged historical private ZIP path; every new changed line stays
exact in the zero-context patch. The top-level plan's two reference links point
to accepted 13A r1 rather than duplicating its evidence.

Seven unique focused cases passed (six initially, then two affected after scoped
corrections). Two real browser flows and desktop/mobile smoke passed; peak uploads
two, six attempts and exactly five images/receipts after lost-result recovery.
Frontend typecheck/affected lint/format, one normal frontend build and one affected
Python module's static checks passed. Owned TEST API/database/blobs cleaned up.
No broad test campaign, backend pytest/migration tests, PWA/Android qualification,
home-server contact, release deployment or Phase 14 work occurred.

Phase 13C requires Brian's privacy/retention approval, Linux filesystem qualification,
production migration/release, database-plus-blob backup/recovery, one real production
listing/image acceptance and final Phase 13 closeout. Shipping policy stays PROPOSED.
