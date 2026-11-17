# Selected contents pricing — implementation review r1

**READY FOR SELECTED CONTENTS PRICING IMPLEMENTATION REVIEW**

Approved Plan 112 is implemented in the local working tree on main
`97130dac80e3351af62ea8d2168c62fefcaae133`. This branch contains only a sanitized
review package. Application source and Plan 112 remain uncommitted; main was not pushed.
Approval source: planning publication `dfc602030615923dd43903b31e0dac633d344a83`
and Brian's explicit implementation authorization.

## Working workflow

The Contents route reads revision-pinned direct catalog occurrences, preserving exact
figure/part-color identity, regular quantities and extras. Select up to four targets /
32 occurrences and independent New/Used × Sold/Active views. Review the signed plan,
confirm, inspect per-target/view progress and item evidence, reload or explicitly resume.
Eight cold requests are refused; two selected cold views use two initials and allow at
most two shared retries. No-FETCH plans authorize zero attempts. Identity requests are
always zero. There is no truncation, refill or chained batch.

Missing/conflicting mappings stay visible and blocked. Exact verified mappings are
revalidated against catalog source, revision and part color. Unit amounts share the
existing Decimal evidence rules and effective policy deadlines; empty is not zero.
Refresh state and retained evidence are separate. Catalog quantities do not verify
physical lot completeness, and this slice adds no component subtotal or sale economics.

## Schema/API and recovery

One additive migration, `0020_contents_market_refresh`, extends the existing operation,
cache/job/attempt framework with CONTENTS scope, a target table and per-target view
binding keys. SET v1 constraints and 4/4/2/10 limits retain explicit scope branches;
contents roots use 0/4/2/6. Runtime grants, package/table inventories, retention and
exact-head/backup compatibility are included. Downgrade refuses contents history.

Added six authenticated route shapes: Contents GET, plan POST, confirmation POST,
active GET, status GET and resume POST. Contracts are generated. Read/plan/status never
dispatch or load provider credentials. Signed plans bind selection, quantities, mappings,
policy and exact cache/job generations. REUSE/JOIN cannot silently become FETCH.

Duplicate confirmation recovers the same durable receipt. Resume reconciles first;
completed views remain complete and uncertain sends remain charged. Joined jobs retain
their original owner/accounting. Explicit reconciliation closes invalid/expired saved
contents operations without cancelling another owner's work; a new plan is required
for replacement work. Terminal replay never reopens quota.

## Evidence and review

- 22 selected PostgreSQL cases have passing evidence (15 new contents, seven legacy SET).
- 122 focused unit cases; 22 Contents/whole-set UI cases; affected lint/types/format and
  generated-contract checks pass.
- Normal API wheel/sdist, independent installed-wheel migration/schema verification and
  web build pass. A later checkbox layout correction required only web rebuild/browser
  recheck; final output privacy/inventory validation passes.
- Real TEST API + synthetic provider browser workflow passes at desktop 1440px and
  narrow 390px: over-cap refusal, mixed selection, partial completion, reload without
  dispatch, explicit resume and independent unit evidence. No page errors/overflow.
- One independent read-only review identified two presentation/freshness defects; both
  were corrected. Focused regressions also corrected a legacy SQL scope-name collision.

See [validation and reused evidence](VALIDATION.md), [updated Plan 112](plan.md),
[exact inventory](inventory.json), [cumulative patch](implementation.patch),
[desktop screenshot](browser-desktop.png) and [narrow screenshot](browser-narrow.png).
Screenshots contain synthetic data only; sticky navigation is captured at the scroll
position by the full-page screenshot, not a separate duplicate navigation element.

The patch excludes all 22 pre-existing pending paths; their bytes and the original
publication files were preserved. Tests/builds used that preserved working-tree context.
The patch itself is checked against the stated main base, with LF-normalized postimages
verified against the inventory. No unrelated staging/reset/stash/cleanup occurred.

## Limits and requested disposition

SOURCE/TEST completion only. Real mapping availability, rights/account state, deployment
and live provider use are unverified. The fourteen unresolved figure mappings are not
assumed fixed. No server/phone access, production migration, provider/model call,
capture restart, dataset/training work, APK or deployment occurred. Every-item coverage,
nested/alternative selection, missing/damaged edits and deferred sale economics remain open.

Review this implementation. Do not deploy, start a live refresh or begin another slice.
