# P10-01 — Frontend release-artifact verification

## Scope and verdict

**PASS for this bounded source fix; Phase 10 remains OPEN.** The frontend
verifier now rejects unsupported asset names, linked build/assets directories,
and non-regular or hard-linked artifact files before it reads artifact bytes.
The runtime loader in `context/services/api/src/brickvault_api/api/static.py`
is unchanged. This package requests review of the source fix and its focused
Windows checks, not full release or runtime-loader parity.

## Implementation baseline and working tree

- Starting and final implementation checkout: `main` at
  `fff17f21c8cecf0303b075430c98471217f2b8ed`; HEAD was not advanced.
- Starting state: empty implementation index; only three pre-existing modified
  protected files: `AGENTS.md`,
  `services/api/tests/integration/test_catalog_search.py`, and
  `services/api/tests/unit/test_catalog_parser.py`.
- Final state: empty implementation index; the same protected modifications
  plus task edits to `CODEX_WORKFLOW.md` and `scripts/tasks.mjs`, and
  untracked `scripts/frontend_artifact.test.mjs`. The protected files retain
  their supplied SHA-256 values and remain unstaged.
- Published `main` was `5c57731c7e15abdae5d6d1e5a35e46e602bc3618`
  when checked, behind the implementation baseline. `base/` contains the
  original `scripts/tasks.mjs` needed to inspect the code change without
  local implementation history. The full original `CODEX_WORKFLOW.md` is
  excluded because it contains historical private local filenames; its
  complete task edit remains in `changes.patch`. This leaves a
  full-document reconstruction gap for that documentation file.

## Exact task changes

| Repository file | Rationale |
| --- | --- |
| `scripts/tasks.mjs` | Check build/assets directory types, flat JS/CSS asset names, and every output file's regular-file and single-link status before reading artifact bytes; preserve private-value/sentinel scanning; register the focused tests with `test:unit`. |
| `scripts/frontend_artifact.test.mjs` | Six independently runnable Node tests cover normal web/PWA acceptance, private bytes, asset names, linked directories, non-regular files, and hard links. |
| `CODEX_WORKFLOW.md` | Add the authorized concise standing reporting/publication rules and current Phase 10 P10-01 note without altering historical entries. |

`changes.patch` is the complete task-scoped unified diff against the stated
implementation baseline, including the new test file. `source/` contains
the final full implementation/test files. The unchanged runtime loader is in
`context/`. No protected or pre-existing unrelated edits are included.

## Invariants, evidence, and limits

The verifier retains its exact top-level web/PWA file-set acceptance, existing
private configuration and sentinel checks, and source-map rejection. Its flat
asset-name check matches the runtime loader's JS/CSS allowlist. All output
paths are checked before the first artifact read. The fix does not add the
runtime loader's full size/count/ancestry and file-identity controls.

New local checks on Windows with Node 24.14.0 and pnpm 11.8.0: six focused
tests passed; targeted Prettier, ESLint, and `git diff --check` passed.
`validation.txt` records the exact commands, initial same-scope corrections,
and skipped broader checks. User-supplied prior Linux/Node 22 evidence states
six focused tests passed after the candidate fix and four failed on the
original verifier. That historical reproduction was not rerun. The named
patch and validation text were not available as standalone files; a supplied
changed-files archive was inspected as a source reference. Its results are not
presented as independently verified local validation.

No unit suite, build, Android/device test, service, database, provider call,
dependency installation, deployment, or application-code commit was run.

## Decision requested from ChatGPT

Review and accept or request a focused correction to P10-01 using this package.
Keep Phase 10 open for separately authorized release work.
