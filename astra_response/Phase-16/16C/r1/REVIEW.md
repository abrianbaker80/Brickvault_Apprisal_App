# Phase 16C outcomes reporting — implementation review

**READY FOR PHASE 16C OUTCOMES REPORT IMPLEMENTATION REVIEW — 2026-11-02.**

Brian approved Plan 111's grouped decisions and bounded source/TEST implementation.
The [approved planning package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/8db34043d280bb8a13329d9c434a5c6f251d65c0/astra_response/Phase-16/16C-plan/r1/REVIEW.md)
is preserved. This r1 package publishes review evidence only; it does not publish
the implementation source to `main`.

## What is implemented

- The `/deals` report counts each owned original root once, using its latest saved
  outcome and classification from one consistent snapshot. Inclusive filters use
  the original saved UTC date; report totals are server-side and use stored,
  versioned results and immutable-original comparison eligibility.
- Only explicit latest `REAL` classifications enter real totals. Unknown,
  synthetic and excluded roots are counted separately. Known zero remains zero,
  unknown remains unavailable, losses stay negative, partial receipts remain
  separate from completed profit, and unpaid minutes are not priced.
- Root classification reads and appends use the existing append-only
  `dataset_subject_revision` ledger, ownership checks, idempotent replay,
  expected-revision conflicts and permanent synthetic provenance. The UI requires
  an explicit reason/evidence key and verifies a successful write by reading it
  back.
- The report is authenticated and no-store. The shared React UI links to saved
  deals and outcome history, and handles a stale snapshot by restarting the page
  set. OpenAPI and TypeScript are generated from the API models.

## API and schema

- `GET /api/deal-outcomes/report` accepts `from_date`, `to_date`, `offset` and
  `snapshot` query parameters.
- `GET` and CSRF-protected `POST /api/deal-forecasts/{identifier}/classification`
  read or append root-only classification history.
- Existing migration `0019_reviewed_dataset_foundation` is reused. No migration,
  new dependency, parallel classification flag or dataset permission was added.
  Listing-subject withdrawal behavior remains intact, and root-only revisions
  are excluded from the listing graph's bounded SQL query.

## Validation

Contracts, TypeScript, ESLint, Prettier, Ruff and MyPy checks passed. The API
wheel/sdist and normal Vite build passed. Five focused cases passed with owned,
disposable TEST PostgreSQL: three report/classification integration tests, the
listing graph regression and one Chromium desktop/320px flow. The browser flow
verified conflict recovery, readback, history links, date filters, missing fields,
no persistent browser storage and no provider/catalog request. It was repeated
successfully against the final production build; the runner reported no leftovers.

See [focused validation](focused-validation.json), [changed files and hashes](changed-inventory.json),
[cumulative source patch](cumulative.patch), [preservation checks](preservation.json),
[reused evidence](reused-evidence.json) and the [updated Plan 111](PLAN-111.md).
The review bundle's source hashes, patch application, link targets, JSON files and
sanitized contents were checked before publication.

## Boundaries

Local `main` remains at `e0deef0ba065d19377525a1ba36fc436ee254e6c` with the source and Plan 111 uncommitted and
unstaged. The 22 pre-existing pending paths, protected files and prior packages
remain unchanged. Only this sanitized package is intended for `astra-response`.

This is source/TEST evidence only. No production database, server, deployment,
provider/model, phone, real corpus, export, training, production smoke
classification, Android build or physical-device qualification was used. The
separate 0019 production rollout and exact-ID smoke registration remain gated;
16A and 16B stay closed, and wider Phase 16 remains open.
