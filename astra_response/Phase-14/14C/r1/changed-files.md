# Exact Phase 14C inventory

Six files relative to the accepted local 14B checkpoint; no retriever changes.

- `CODEX_WORKFLOW.md`
- `docs/ROADMAP.md`
- `docs/plans/106-retrieval-quality-gate.md`
- `scripts/evaluate_retrieval.py`
- `services/api/src/brickvault_api/recognition/evaluation.py`
- `services/api/tests/unit/test_retrieval_evaluation.py`

Protected and unstaged: AGENTS.md; services/api/tests/integration/test_catalog_search.py; services/api/tests/unit/test_catalog_parser.py. All remain byte-for-byte unchanged.

Local source stays intact. The publication workflow snapshot alone redacts one historical private asset path. The patch is cumulative from 44a1e15bc0d45f996d3eb6898534cd2f202ca275 and passes reverse apply-check; it is not applied.
