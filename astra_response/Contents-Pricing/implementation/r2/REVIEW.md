# Selected contents pricing — corrected implementation r2

**READY FOR SELECTED CONTENTS PRICING CORRECTED IMPLEMENTATION REVIEW**

November 17, 2026. Targeted correction within approved Plan 112. Application main
remains `97130dac80e3351af62ea8d2168c62fefcaae133`, uncommitted and unpushed with an
empty index. This publication contains review artifacts only; r1 is preserved.

## Correction

`ContentsService.confirm_selected()` previously checked for a receipt only before
reconstructing the plan. A duplicate could miss that receipt, then see cache/job drift
after the original confirmation committed and progressed, incorrectly returning
`REPLAN_REQUIRED`. A barrier-controlled PostgreSQL regression reproduced this before
the fix, extending the reviewer's earlier in-memory reproduction.

The service now follows the existing whole-set recovery pattern: after a
`ProductRefreshError` in new confirmation/revalidation, it rechecks the exact durable
receipt. A shared helper verifies normalized contents selection during both initial
and late recovery. Existing scope, set, key, digest and creation-time checks remain;
signature validation stays outside the late-recovery handler.

An exact retry returns the original operation whether progressed or terminal. Changed
selection remains `IDEMPOTENCY_CONFLICT`; mismatched receipt, invalid signature and
genuine drift remain errors. Receipt recovery performs reads only: no new operation,
provider request, quota reset, altered signed plan or lookup of the newest set operation.
The mapped-only 0 identity / 4 price / 2 retry limits are unchanged.

## Evidence and scope

Nine focused PostgreSQL cases have passing evidence across the bounded runs. Final
five-case barrier suite: 5 passed in 26.08s, with original-ID recovery, one operation,
no additional provider attempts and unchanged full operation/view/accounting state.
Four directly affected replay/drift controls passed in the preceding run. Python lint,
formatting and service typing pass. API-only packaging passes; wheel, sdist and
independently installed wheel contain the exact corrected service bytes.

Only three of the 32 implementation paths changed: `contents.py`, its existing
integration test file, and Plan 112. All other 29 hashes match r1. Reuse unchanged r1
request-cap, migration/grants, financial/evidence, UI/browser and recovery evidence.
No web build/browser rerun, migration, full test campaign, phone, provider, production,
backup/restore or deployment work was performed.

Artifacts: [small correction diff](r1-to-r2.patch), [cumulative patch against main](implementation.patch),
[exact inventory/hashes](inventory.json), [updated Plan 112](plan.md),
[focused checks and reused evidence](VALIDATION.md), [package checksums](PACKAGE_SHA256SUMS.txt).
The cumulative patch excludes all pre-existing pending work. Both patches were applied
in isolated verification directories and their postimages compared with final source.

All 22 pre-existing pending/protected paths, stopped capture work and prior publications
remain preserved. No application-source commit. Real mapping availability/rights/account
state and live use remain unverified; fourteen unresolved figure mappings are not
assumed fixed. No mapping onboarding, discovery or later economics work. Stop for review.
