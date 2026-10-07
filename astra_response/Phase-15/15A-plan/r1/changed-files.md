# Exact planning inventory

Local main stays at `e9c7d1f14ccfdf8784a9d4402a2fc0641184dab9`; no staging/commit.
Only these seven files were changed/added by this task:

| Path | Action | Purpose |
|---|---|---|
| `docs/plans/108-phase-15-android-share-capture.md` | New | Share-first ExecPlan with preflight, API/privacy gap, physical gates and separate capture/polish approvals |
| `CODEX_WORKFLOW.md` | Modified | Dated planning-only checkpoint; previous history preserved |
| `docs/ROADMAP.md` | Modified | Current Phase 15 15A/15B/15C progression and approval gates |
| `docs/PROVIDER_GATES.md` | Modified | Known/unknown device facts, mechanism/allowlist and network gates |
| `docs/REQUIREMENTS_TRACEABILITY.md` | Modified | Planning trace without claiming new qualification |
| `docs/SECURITY_PRIVACY.md` | Modified | Correct stale unresolved-policy claim; link accepted policy and proposed custody |
| `prompts/15_android_capture_overlay.md` | Modified | Explicitly separate first Share slice, later capture and later polish |

`files/` contains the exact proposed Plan 108 at its repository-relative path.
`planning.patch` contains only the six tracked documentation changes plus new Plan 108.
The six existing documents are represented by their complete changed hunks; unrelated
historical content/private local paths are not republished. Repository Markdown targets
were checked in the actual checkout; Plan 108 uses explicit source paths and official links.
Supporting package documents are REVIEW.md, architecture-and-share.md,
device-and-gates.md, android-api-findings.md, this changed-files.md and validation.md.
No implementation or protected-file patch/copy is published.

Pre-existing protected dirty files, untouched/unstaged:

- `AGENTS.md`
- `services/api/tests/integration/test_catalog_search.py`
- `services/api/tests/unit/test_catalog_parser.py`

All earlier review trees, including accepted Phase-14/closeout/r1, remain unchanged.
