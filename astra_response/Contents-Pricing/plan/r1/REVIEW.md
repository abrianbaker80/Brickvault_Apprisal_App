# Contents pricing plan review

**READY FOR CONTENTS PRICING PLAN REVIEW** — November 16, 2026.

[ExecPlan 112](PLAN.md) proposes one bounded delivery for selected verified
minifigures and exact part/color items in the existing set appraisal workflow.
This is planning only; implementation and live activation are not authorized.

## Actual gap and recommendation

The backend already prices MINIFIG and PART/color identities, stores exact-view
evidence and feeds eligible cached evidence to the existing valuation engine.
Contents lacks selectable item-level evidence, and public refresh models/SQL are
hard-coded to one SET mapping and four views. Blocked physical inventories remain
blocked even after item prices become available.

Deliver both mapped component types together: inspect recorded contents, select
up to four targets and independent New/Used × Sold/Active views, review a bounded
request plan, confirm, then inspect results and explicit resume/recovery. Allow
at most four new price requests plus two retries, zero identity requests and six
total attempts. More cached views may be reused; an over-cap selection is refused
without silent truncation or automatic batching.

Reuse the existing adapter, mapping revisions, cache/observations, worker, attempt
ledger, quota policy, signed confirmation and durable recovery. Proposed changes
are a paged Contents evidence projection, selection/plan/progress UI, generated
contracts and one additive `0020_contents_market_refresh` migration extending the
existing operation framework. Its affected grants, retention, packaging, schema
inventory, backup-format admission and health implications are included in the plan.

## Decisions and dependencies

Approve or revise one grouped scope: mapped-only support for both types, the
selection/request ceiling, direct recorded inventory scope and additive migration.
The first delivery creates no mappings. Source-backed part element/color review and
authoritative whole-figure crosswalk onboarding remain explicit later contents scope.
Plan 105's fourteen unresolved minifigure mappings are not assumed fixed. Current
live mapping coverage, account permissions and activation were not checked.

No missing-item editor, replacement costs, split-sale/part-out economics, labor/
recovery model, ROI expansion, economic break-even lots, Hunt change or frozen
forecast recalculation is included. Deferred Economics requirements remain outstanding.
This work has no new numbered phase and is not Phase 16D.

## Review evidence and preserved state

Source authority is local main `97130dac80e3351af62ea8d2168c62fefcaae133`.
The accepted closeout remains
[`2520e2a8` / Phase 16C production r4](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/2520e2a8e0b41e690c1f59db5183f288108d76fd/astra_response/Phase-16/16C-production/r4/REVIEW.md).
Phase 16C remains ACCEPTED / CLOSED. Recorded release/schema identities are
`phase16c-outcomes-production-r2` / `0019_reviewed_dataset_foundation`; this package
does not reverify live state or perform another closeout.

Independent planning review found no material correction required. Its limitation
is explicit: fixture/source completion cannot establish real mapping coverage or
provider readiness. Future checks cover exact identities/colors/quantities, bounded
planning and zero pre-confirm dispatch, deduplication, partial/resume recovery,
evidence/coverage, migration/grants/package compatibility and unchanged whole-set
refresh. One workflow at desktop and narrow viewport suffices; no unrelated campaign.

See [documentation inventory](documentation-inventory.json) and
[documentation and preservation checks](documentation-checks.json). This package
contains only four sanitized planning files. All 22 pre-existing pending paths,
three expressly protected files and 33 prior local publication files were checked
byte-for-byte. The original main index is empty; main and remote main remain
unchanged. The local ExecPlan remains uncommitted. Prior publication history is
preserved through an additive child commit on astra-response.

No tests/builds/installations, source/migration/contract/dependency edits, credential
reads, database/service startup, provider/model calls, production/phone access,
private corpus/export/training, backup-history investigation or deployment occurred.
The only network activity for this task was authorized Git review publication.

**Stop for plan approval.** No implementation, capture restart, deployment or later
economics work follows this publication. Any eventual live provider check requires
separate approval against the actual displayed request plan.
