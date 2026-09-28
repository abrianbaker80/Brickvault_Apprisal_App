# P10-03 r2 — local packaged-release readiness

**Verdict: READY FOR PHASE 10 CLOSEOUT REVIEW.** This bounded local smoke and the accepted earlier evidence support the existing Phase 10 local gates. P10-03 is implemented for review; Phase 10 remains IN PROGRESS. No deployment or Phase 11 work is authorized or claimed. This revision supersedes r1 only to correct a transcribed protected-file SHA-256 in the report; the task patch, source and validation results are unchanged.

## Scope and implementation state

- Starting and final implementation checkout: `main` at `6b844b757ec2df2dd3ebcdbc32f2e6ccbf7ddb19`; the implementation index was empty before and after. No application commit or push occurred.
- Initial working tree: only three pre-existing protected modifications. Final working tree: those three plus the nine uncommitted P10-03 files listed below. Build output, isolated package check and local run ledger remain ignored.
- Protected files stayed unstaged and match their recorded SHA-256 values: `AGENTS.md` (`f0a354ed80f631910f4cdcb64729209ef4758de441f3eaaf509da49395f969b4`), `services/api/tests/integration/test_catalog_search.py` (`d06965d560361a06b7a33647efa5b9b34829f8c34d5d912226d9cd5b3645abf7`), `services/api/tests/unit/test_catalog_parser.py` (`0251b5c358cd37de9e07e2cbdfb44913752cade7050d9eb1b3a885f57d27a041`).
- Remote `main` remained at `5c57731c7e15abdae5d6d1e5a35e46e602bc3618` when packaging began; the implementation baseline is not remotely available. `base/` includes exact original versions of the three changed tracked tooling/entrypoint files. Historical `CODEX_WORKFLOW.md`, `LOCAL_DEVELOPMENT.md` and roadmap baselines are omitted for privacy/size; their complete task hunks remain in `changes.patch`. This is the documentation reconstruction gap for reviewers without the local baseline.

## Exact changed-file inventory

| Repository path | Substantive reason |
| --- | --- |
| `scripts/packaged_release_smoke.py` | Guard one selected isolated wheel install; start its installed API in Python isolated mode with an owned loopback socket, disposable TEST database and exact worker handle; verify the HTTP flow and safe logs; restore prior TEST state. |
| `scripts/test_packaged_release_smoke.py` | Five focused receipt/import refusal and Windows-separator cases. |
| `scripts/package_api.py` | Print the new package-check receipt path after the existing offline locked install succeeds, so the exact build is selected. |
| `scripts/tasks.mjs`, `package.json` | Add the root-only `test:packaged-release` command with one explicit receipt argument. |
| `docs/LOCAL_DEVELOPMENT.md` | Record the repeatable local command, ownership/cleanup behavior and evidence limits. |
| `docs/plans/089-local-packaged-release-readiness.md` | Bounded ExecPlan, progress, results and Phase 10 requirement-to-evidence reconciliation. |
| `docs/ROADMAP.md` | Correct the current Phase 10 status to IN PROGRESS while preserving Phase 9 closure and later phase boundaries. |
| `CODEX_WORKFLOW.md` | Add only the current P10-03 implemented-for-review note, preserving standing rules and historical entries. |

`changes.patch` is the complete nine-file cumulative unified diff against the stated implementation baseline, including all new files. `source/` holds complete final versions of all changed implementation/test/entrypoint files. `context/` contains only the unchanged owned database, API app and static-loader contracts needed to evaluate the runner. No private configuration, dump, credential, verifier, cookie, token, actual record, APK, dataset or raw log is included.

## Existing Phase 10 requirement-to-evidence table

| Requirement | Accepted evidence reused | P10-03 evidence | Remaining local gap |
| --- | --- | --- | --- |
| Release packaging | P10-01 frontend verifier regressions; existing offline locked package checks. | One normal `pnpm build` passed wheel/sdist and isolated-install probes plus Vite production build. The HTTP process imported from the selected venv `Lib/site-packages`, and served the exact built shell and referenced JS/CSS assets. | None for local packaging. No Android rebuild or deployment. |
| Authentication, security and secrets | Accepted Phase 7B expiry/revocation, rotation, CSRF, privileges and log tests; Phase 9 physical TLS/cookie, expiry/offline/privacy/sync evidence; P10-01 asset/private-value checks. | Packaged HTTP checked pre-login denial, login, CSRF refusal and Settings update/readback, logout denial, three static-root exclusions, no-store private responses and absence of TEST secret values in public bytes/logs. | None for these bounded local checks; no comprehensive security or dependency audit is claimed. |
| Migration and recovery | Accepted Phase 8 current-head `0016_hunt_cached_runs` TEST selection included downgrade/re-upgrade, mismatch and downgrade-refusal tests; earlier owned outage/recovery evidence. | One new TEST database migrated to current head; installed runtime-role HTTP readiness returned current migrations and database OK. | None for local migration checks; no development/production rollback operation was run. |
| Backup and restore | Accepted P10-02 real custom dump/restore of two owned TEST databases, focused readback, eight guards and exact cleanup. | Reused without repeating the recovery rehearsal. | None for the disposable proof. Production retention, off-host backup and disaster recovery remain unqualified. |
| Observability and release operation | Accepted foundation request-ID, safe JSON logs/errors, Host/Origin and owned cleanup evidence. | Nineteen safe structured request events, unknown `/api` JSON error, exact child/database cleanup, restored TEST state and local run instructions. | None for local operation; centralized monitoring/deployment is later scope. |

## Actual validation and limitations

- **New local results:** One successful Windows `pnpm build` using Node 24.14.0, pnpm 11.8.0, Python 3.13.12 and repository-local uv 0.12.10. It installed the locked wheel offline into a new isolated venv and built the normal web/PWA output. One successful packaged HTTP smoke passed **18 checks**, including two referenced assets and three static-root probes; **19** safe request log events were found. The package import resolved under the selected venv, never `services/api/src`. One exact disposable database was removed, the API worker/listener stopped, prior TEST service state was restored and the ledger reported **zero leftovers**.
- **New focused tooling checks:** Five guard tests, changed-file Ruff check/format, strict mypy, targeted Prettier/ESLint, new-link checks and complete task patch whitespace check passed. `validation.txt` records exact commands and the routine failed smoke attempts with their cleanup outcomes.
- **Reused evidence:** P10-01 six frontend verifier tests, P10-02 one real restore proof and eight guard tests, accepted Phase 7B authentication/integration and Phase 8 migration selection, accepted Phase 9 physical Android qualification and foundation local error/log evidence. None was rerun here.
- The Windows venv launcher and installed Python worker have distinct PIDs. The final runner retains an OS handle to the exact installed worker and verifies listener closure; the successful run exercised that path. Earlier in-scope attempts refused a Windows receipt separator mismatch and a relative private-path mismatch before provisioning; a PID-identity attempt created one TEST database but removed it and restored the service. The final smoke reused the single successful build.
- This is synthetic local readiness. It does not establish full security audit, production disaster recovery, role/config backup, data-volume recovery, off-host retention, live providers, deployment or another physical Android run.

**Decision requested from ChatGPT:** Review whether the existing Phase 10 local requirements are sufficiently supported for closeout. Keep Phase 10 open until that review and separate acceptance; do not begin Phase 11.