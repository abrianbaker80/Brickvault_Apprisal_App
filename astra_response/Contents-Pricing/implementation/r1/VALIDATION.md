# Focused SOURCE/TEST validation

All provider responses are authored fixtures. PostgreSQL databases were created and
removed by the repository's exclusive owned TEST runner (loopback 55433); no existing
5432 service, production data or external provider was accessed. No dependencies added.

## Passing evidence

| Check | Result and evidence |
| --- | --- |
| Contents + seven selected legacy PostgreSQL cases | Combined run: 21 passed; one HTTP fixture failed. Ledger `e05143c6d03b49dfae95556b9ddba34e`. All other cases reused unchanged. |
| Corrected HTTP read/plan fixture | Passed with initial browser workflow; 2 passed. Ledger `b141278f1f6542beafb13cf5e2709872`. Thus all 22 selected database cases have passing evidence; no claim of a single 22/22 run. |
| Final mixed desktop/narrow browser | 1 passed, 15.00s. Ledger `be101d8cd73d4ce48694852b5e58f058`. Corrected checkbox layout; zero page errors, no horizontal overflow, checkbox width <=20px. |
| Focused Python units | `test_valuation.py`, `test_product_refresh.py`, `test_outcome_backup_compatibility.py`: 122 passed, 0.83s. Includes 0020 supported-head case. |
| React | `ContentsPricing.test.tsx`, `MarketRefresh.test.tsx`: 22 passed, 5.04s. Final markup-only label wrapper is additionally exercised by final browser check. |
| Python static | Ruff lint/format; strict mypy on 15 affected source files: passed. |
| Web static/contracts | Affected ESLint; web and contracts TypeScript; `node scripts/tasks.mjs contracts:check`: passed. |
| Normal build | `node scripts/tasks.mjs build`: API wheel/sdist, independent installed-wheel import/migration graph/credential-free schema and web production build passed. Package check ID `5cbaf4e7bceb42669476aafa4ceabc6d`. |
| Layout-only rebuild | Existing Vite production build and exported `verifyFrontend` privacy/output inventory check passed; API package evidence unaffected. |
| Preservation/patch | Main HEAD/index and protected baseline hashes checked; cumulative allowlisted patch checked against base and normalized postimages verified. |

The selected database cases exercise mixed targets, regular/extras deduplication,
independent views, eight-request refusal, unsupported alternatives/descendants and
wrong revision, unresolved mapping without discovery, joined ownership/zero allowance,
barrier-based duplicate confirmation, mapping/cache drift, terminal replay, restart with
uncertain sends, four initials/two retries/no seventh, stricter account policy, expiry
reconciliation, empty/stale evidence, tightened freshness, physical aggregate gates,
runtime privileges, legacy history-preserving migration round-trip and guarded downgrade,
target retention, and read/plan immutability across all market tables.

Legacy selections: existing_mapping_four_views; confirmation_concurrency_conflicts_and_restart;
joined_generation_keeps_attempt_owner; partial_price_resume_keeps_generation_lineage;
product_shared_retry_exhaustion; product_revoked_mapping_and_policy_drift_stop_dispatch;
product_privileges_immutable_authorization_and_job_binding, in `test_product_refresh.py`.

The browser fixture is explicitly selected via
`services/api/tests/integration/contents_browser_fixture.py`, invoking the installed
Playwright Chromium runner `apps/web/e2e/contents-acceptance.mjs` against its own loopback
FastAPI server. Authentication is real with a random ephemeral TEST password passed only
through the child process environment. It is not a production application entrypoint.
Every listed runner ledger reports no leftovers and preserved volumes; owned servers stop.

## Corrections and reused evidence

Development failures were resolved: SQL identifier qualification; runtime grants after
recreating migration objects; shared hook error messages; effective freshness; inventory
wording; reconciliation-method name collision; Windows event-loop loopback allowance in
the HTTP test guard; inherited checkbox width. The fixture still forbids external network,
provider credential loading and the protected local database ports. Existing deprecation
and pytest assertion-rewrite warnings are not new dependency requirements.

Reused without broad repetition: existing catalog/provider mapping constraints and
adapter normalization; reviewed quota/attempt ledger and generation fencing; accepted
physical/financial arithmetic (also covered by the focused valuation unit file); existing
auth/origin/CSRF machinery; prior Phase 16C release/phone/provider evidence recorded in
Plan 112. Historical release evidence is not current activation or provider qualification.

No full historical suite, backup/restore campaign, APK/device test, live provider check,
deployment or financial calibration was performed. Performance of very large inventories
and broader mapping onboarding are not qualified by the small synthetic workflow.

Generated-contract semantic comparison also confirmed every pre-existing path/schema unchanged; five URL paths and eleven schemas were added. Package SHA-256 sums refer to published Git blob bytes (LF text), before checkout line-ending conversions.
