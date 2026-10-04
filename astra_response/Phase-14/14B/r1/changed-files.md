# Exact changed-file inventory

Application baseline: 7149f83dd7a16092bc2dfa12cd1ab1935073f537.
Ten implementation/doc/test files remain uncommitted.

- CODEX_WORKFLOW.md
- docs/ROADMAP.md
- docs/plans/105-reference-candidate-retrieval.md
- scripts/reference_candidates.py
- services/api/src/brickvault_api/catalog/query_types.py
- services/api/src/brickvault_api/catalog/repository.py
- services/api/src/brickvault_api/catalog/search.py
- services/api/src/brickvault_api/recognition/comparison.py
- services/api/src/brickvault_api/recognition/retrieval.py
- services/api/tests/unit/test_reference_retrieval.py

See [source hashes](source-inventory.json). One historical private asset path in
the workflow snapshot is publication-only redaction; local source is unchanged.
The cumulative patch contains the exact ten-file application change.

Excluded: AGENTS.md; services/api/tests/integration/test_catalog_search.py;
services/api/tests/unit/test_catalog_parser.py. All remain unchanged and unstaged.
