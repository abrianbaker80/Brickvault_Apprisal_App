# Phase 14B r1 — local candidate retrieval foundation

**READY FOR PHASE 14B FOUNDATION REVIEW**

Selected local photos plus an operator description or explicitly selected retained
visual/text clue now produce a ranked shortlist, offline comparison report and
separate private operator notes. This is description-assisted retrieval; image-only
retrieval and fresh AI verification remain deferred.

## What works and what was exercised

- Deterministic name/feature matching with matched terms, ranking weights, stable
  ties and no-match behavior; existing catalog set search plus a small read-only
  minifigure helper. Catalog candidates are not restricted to the three references.
- Three corrected licensed front-reference photographs, with retained image/license
  hashes, attribution and documentary identity provenance. Exposed heads/rear views
  and canonical mappings remain unavailable.
- Six focused synthetic cases passed, plus changed-file lint and strict types.
  One actual local catalog/browser/note smoke returned eight candidates: two with
  reference photos and six without. Its 1,012-candidate pool is explicitly truncated.
- Installed Edge rendered all four embedded images and the saved/reopened private
  insufficient-evidence note with zero external requests. The note is a software
  demonstration, not Brian's confirmation. Development returned to stopped.

These preselected references demonstrate software behavior, not independent
retrieval accuracy. Retrieval scores, compatibility, unique identity, operator
assertions and canonical resolution remain separate. No production confirmation,
new mapping or valuation follows. Phase 14A scores and its ten-attempt ledger remain
closed and unchanged; new provider calls/spend are zero. Wider Phase 14 is IN PROGRESS.

## Review package

- [Plan 105](source/docs/plans/105-reference-candidate-retrieval.md)
- [CLI workflow example](workflow-example.md)
- [Retrieval, ambiguity and coverage](retrieval-ambiguity-coverage.md)
- [Focused validation and preservation](validation.txt)
- [Exact ten-file inventory](changed-files.md) and [hashes](source-inventory.json)
- [Cumulative patch](cumulative.patch) and changed source/tests/docs under source/
- [Accepted 14A r6](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/2c71ad336424c8d4e7af6e8ed15279371afab578/astra_response/Phase-14/14A/r6/REVIEW.md)

Application main stays at 7149f83dd7a16092bc2dfa12cd1ab1935073f537, uncommitted
for this slice and unpushed, with empty index. Three protected files remain byte-for-byte
unchanged/unstaged; all previous Phase 14A review trees are preserved. Public snapshots
exclude private photos, query text, operator notes, credentials and asset paths.
No inference, metadata/counting calls, model download, broad suite, build, deployment
or later-phase work occurred.
