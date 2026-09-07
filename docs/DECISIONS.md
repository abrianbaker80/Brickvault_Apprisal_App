# Project Decisions

This file preserves durable decision history. The original D-001 through D-017 text below records earlier approvals, not an instruction to revive superseded scope. Current applicability is determined by the additive D-018 through D-021 decisions. References to image-first Phase 1 or the former plan path in historical entries are superseded as stated below.

## Accepted

### D-001 — Private single-user product

The application is built solely for Brian. No public registration, billing, team roles, or app-store distribution is required.

### D-002 — Self-hosted source of truth

Images, labels, appraisals, and provider credentials will be controlled by Brian's server. Clients call the server rather than external providers directly.

### D-003 — Save training-useful data from the beginning

The MVP must preserve immutable originals, useful crops, prediction history, and Brian's corrections. Dataset labeling is part of the product, not an afterthought.

### D-004 — Human confirmation separates prediction from truth

An AI result cannot automatically become a verified training label.

### D-005 — Retrieval and verification precede custom training

Index reference images and metadata, retrieve candidates, and use multimodal verification before investing in a custom model.

### D-006 — Explicit user-triggered Facebook capture only

Do not scrape, intercept, or autonomously navigate Facebook. Brian triggers each capture/session.

### D-007 — Keep ordinary uploads and Android Share as fallbacks

The app must remain usable when the overlay/accessibility path breaks or Facebook changes its UI.

### D-008 — Risk-first development

Prove the image-storage path, Android capture feasibility, and recognition quality in isolated milestones before building the complete workflow.

## Accepted foundation decisions — 2026-09-05

Brian approved these decisions during architecture review and the documentation checkpoint. Their implementation is a separate task. D-001 through D-008 above retain their original text.

### D-009 — React + Vite + TypeScript browser UI

Use React + Vite + TypeScript in `apps/web`. This supersedes browser framework proposal P-002. Keep the frontend cleanly separated from the server and its static host.

### D-010 — FastAPI production static serving

FastAPI is the API and production application server and serves the frontend's static build from a configurable directory. Static serving can later move to Caddy or another reverse proxy without rewriting the frontend. No production deployment is authorized by this decision.

### D-011 — API namespace and generated contracts

All server API routes use `/api`, including health, readiness, and OpenAPI. Clients use the same server contract; the web build uses relative `/api` URLs and a Vite development proxy. Generate TypeScript from Pydantic-derived OpenAPI in `packages/contracts` and use `openapi-fetch`. API errors must not become frontend HTML responses.

### D-012 — Independent partial-success uploads

Send one image per multipart request. Each file has its own result and transaction. Preserve successful uploads when another fails; allow retrying/removing a failed file without re-uploading successes. Successful images may proceed to analysis in later milestones despite other failures. Phase 1 adds no analysis.

### D-013 — Idempotent per-file retries and successful duplicate receipts

Assign a client upload UUID before dispatch. The request includes intended `display_order`; retries preserve the UUID, bytes, and position. Every successful result, including an exact duplicate, creates or reuses a durable receipt. Replay returns the stored result and relationship without additional records. A committed UUID reused with different bytes or order yields `UPLOAD_ID_CONFLICT`. Store successful receipts and any relationship/order changes in one transaction.

### D-014 — Listing-image identifier

The per-file result field is `listing_image_id`. It identifies the listing-to-image relationship; it is distinct from the original asset ID, thumbnail asset ID, and physical blob hash. Return it for both successful new and duplicate uploads, and use null for failures.

### D-015 — Deterministic persisted image ordering

Assign consecutive intended `display_order` values in client selection order before uploads begin, using the server receipt high-water mark and outstanding local queue positions. Retry the same position. Persist each receipt's intended position and each unique listing image's minimum successful receipt position. This handles duplicates arriving out of order without making the final display order depend on request completion or commit order.

Enforce unique `(listing_id, client_upload_id)` and `(listing_id, display_order)` on receipts, plus unique original and position per listing-image relationship. Return `DISPLAY_ORDER_CONFLICT` for another UUID claiming an owned position; do not silently reassign it. Removing/reselecting only the failed file after refreshing positions is a new submission with a new UUID, not an ordinary retry. Gaps and duplicate receipt positions remain accounted for by the high-water mark. ExecPlan 000 defines the exact transaction and acceptance scenarios.

### D-016 — Foundation architecture and scope

Use a Python/FastAPI modular monolith, PostgreSQL with SQLAlchemy/Alembic migrations, and immutable content-addressed filesystem blobs behind a `BlobStore` interface. Separate physical blobs from semantic image assets, lineage, listing relationships, and receipts. Use uv for Python and pnpm for web/contracts. No runtime schema creation, queues, background workers, MinIO, AI, Android, authentication, or remote deployment in Phase 1. Development is loopback-only and uses isolated PostgreSQL instances.

This adopts proposals P-001 and P-005. P-004 is adopted as PostgreSQL now, pgvector only when retrieval is implemented. P-003 remains the accepted future direction: native Kotlin/Jetpack Compose Android, with exact toolchain and physical-device feasibility established in its own milestone.

### D-017 — Documentation checkpoint and historical starter

The active sources of truth are checked-out guidance, current documents, and `docs/plans/000-foundation-and-risk-spikes.md`. The starter ZIP is historical material and is not restored or consulted as active instructions. A documentation checkpoint does not authorize implementation, dependency installation, service startup, home-server access, or a Git commit. Start Phase 1 only after a separate explicit implementation request.

## Accepted realignment decisions — 2026-09-05

### D-018 — One unified valuation-first product

Brian establishes one private LEGO sourcing and appraisal platform. Deterministic catalog identity, set/minifigure quantities, provider mappings, market observations, valuation, saved work, and Sets to Hunt form the foundational core. Direct suffixed set-number/name search must work with every image feature disabled.

This supersedes D-008 only with respect to development sequencing: image storage, Android capture, and recognition move to Phase 13 onward rather than gate the sourcing MVP. Its rationale for bounded, evidence-backed risk work remains; the early risks are now provider mappings, rights, coverage, and deterministic financial correctness.

D-003's "from the beginning" scope starts when image ingestion is implemented, not in the catalog/valuation foundation. Its original retention rationale remains, subject to an explicit privacy/retention/deletion policy before that later feature ships. D-005's retrieval-before-custom-training rule applies within the later recognition module, not before deterministic sourcing.

D-001, D-002, D-004, D-006, and D-007 remain substantively applicable; image-specific obligations take effect in their later module. Recognition returns candidate canonical identities into the same catalog/relationships/mappings/market/valuation core and owns no duplicate catalog or financial engine.

### D-019 — Shared React interface for Chrome, PWA, and Android

Use the same primary React + Vite + TypeScript application for responsive Chrome, an installable PWA, and an Android package, preferably through Capacitor unless a documented Phase 9 spike proves a better choice. All share one FastAPI API, user data, and authoritative PostgreSQL database.

This supersedes D-016's reference to P-003 as a native Kotlin/Compose core-client direction. Native code may extend apps/android later for genuinely required Share/overlay behavior; it does not reimplement core screens, provider calls, or valuation rules. Packaging and physical-device compatibility remain unverified.

Initial offline behavior is read-only access to permitted, explicitly dated cached views. Fresh search, recalculation, and writes require the backend; online edits use server revisions and explicit conflicts. Client caches are not authoritative databases.

### D-020 — Authoritative financial, identity, and evidence rules

Adopt [VALUATION_RULES.md](VALUATION_RULES.md) and [DATA_MODEL.md](DATA_MODEL.md): exact decimal money, explicit currencies/conversions, quantity-bearing set/minifigure relationships, verified provider-scoped mappings, separate new/used and sold/listing evidence, and missing data as unknown.

Sale strategies cannot double-count physical figures/builds/components. Define gross/selling/net proceeds, acquisition-dependent costs, profit, ROI with zero-cost undefined state, target-ROI and minimum-profit maximums, conservative rounding/clamps, and deterministic versioned explanations. Missing required evidence blocks recommendations.

Phase 4 representative feasibility must establish supported sourcing evidence before confidence is claimed. Provider access/rights/retention, live coverage, and device behavior remain future gates; documented endpoints or fixtures do not prove them.

### D-021 — Rebased foundation and preserved later contracts

Replace the unexecuted image-first ExecPlan 000 with [000-local-foundation.md](plans/000-local-foundation.md), covering only local web/API shells, isolated PostgreSQL, migration tooling, generated health/readiness contracts, checks, and setup documentation. It has no product tables or image/listing/provider routes.

D-009 React/Vite, D-010 FastAPI static serving, and D-011 /api/generated contracts remain active. D-016's modular monolith, PostgreSQL/Alembic, uv/pnpm, loopback isolation, and no unnecessary infrastructure remain active; image/BlobStore work moves out of Phase 1.

D-012 through D-015 remain accepted upload semantics for Phase 13: independent partial success, listing_image_id, stable client UUID/position retries, deterministic persisted minimum-receipt ordering, and durable successful-duplicate receipts. Historical references to Phase 1 in those entries no longer assign their implementation phase. The complete preserved contract is [IMAGE_INGESTION.md](IMAGE_INGESTION.md).

D-017's stop/authorization and historical-ZIP boundaries remain active; its former plan path is historical and replaced by the link above. The current checkpoint is documentation realignment. After Brian reviews it, the next action is Prompt 01 in Plan mode; implementation still requires a separate explicit request.

The roadmap and prompts now align one-to-one from 00 through 16. Phase 10 hardens only a local release; Phase 11 requires separate read-only home discovery authorization; Phase 12 requires a reviewed plan and distinct deployment approval. No current server/DNS/production access, application implementation, dependency change, staging, or commit is authorized.

## Accepted documentation baseline refinement — 2026-09-05

### D-022 — Canonical Phase 1 plan, portable paths, and bounded execution

Persist the approved detailed [ExecPlan 000](plans/000-local-foundation.md) as the canonical Phase 1 execution plan. D-001 through D-021 retain their original text and accepted historical meaning; earlier current-checkpoint sentences describe their dated approvals rather than the latest task state.

Use repository-relative paths wherever sufficient; no machine, username, or checkout location is an architectural requirement. Phase 1 has three separately authorized slices: 1A toolchain/workspace and exact locks; 1B isolated PostgreSQL, SQLAlchemy/Alembic, API and generated contracts; 1C responsive web shell, built serving, CI and complete acceptance. Completing one slice never authorizes the next. The split does not weaken final acceptance or add product-domain, image, provider, PWA/Android, or deployment work.

The Slice 1A plan includes an exact-lock local checkpoint only under an explicit slice execution/local-Git request. The present checkpoint authorizes documentation and one reviewed local baseline commit only, with no push; it authorizes no implementation, installs, services, database connections, networks, or infrastructure access.

During Phase 1 implementation, AGENTS.md, ORIGINATING_CHAT_SUMMARY.md, PRODUCT_SPEC.md, VALUATION_RULES.md, and SECURITY_PRIVACY.md are read-only by default. Change one only for a concrete verified contradiction that cannot be accurately documented elsewhere; propose a narrow evidence-backed change and report it explicitly. Normal progress belongs in the current workflow/setup/plan/roadmap/traceability documents listed in ExecPlan 000, with architecture edits limited to verified details.

[CODEX_WORKFLOW.md](../CODEX_WORKFLOW.md) and ExecPlan 000 carry current checkpoint and slice status. Prompt 01 remains reusable plan-only review; the next separately authorizable implementation action is Slice 1A only.

### D-023 — Approved Slice 1A tooling corrections — 2026-09-05

Brian authorizes TypeScript >=5.9.3,<5.10, initially 5.9.3, with openapi-typescript 7.13.0; this supersedes the incompatible TypeScript 6 proposal. ESLint >=10.0.0,<11, initially 10.10.0, with @eslint/js 10.0.1 and typescript-eslint 8.69.0 replaces the end-of-life ESLint 9 proposal. Select one workspace compiler and preserve strict peer checks, supported flat configuration, and stable supported direct dependencies.

Official standalone uv 0.12.10 may be installed under ignored .local/tooling/uv/0.12.10/ with published artifact integrity verification. Invoke it explicitly and enforce its exact version. Global uv 0.10.7 and system/user configuration remain untouched; no automatic Python downloads are permitted. Retain Hatchling and use --no-install-project only for Slice 1A dependency synchronization, with actual application installation/build required once source exists.

Persist these approvals even if subsequent installation is blocked; approvals are not test evidence. Slice 1A alone is authorized, with working-tree changes retained for review and no staging/commit, application source, services, databases, infrastructure, or automatic advancement. D-001 through D-022 retain their historical meaning.

### D-024 — New and used set part-out values — 2026-09-06

Brian requests separate new/used set part-out values in the sourcing product. Add the feature through Phases 2–6 under [the part-out plan](plans/005-set-part-out-values.md): quantity/color-aware inventory, verified component pricing, feasibility, deterministic aggregation, and set-detail display. These are theoretical component totals with evidence and coverage, distinct from supported net proceeds/profit/max-buy. Assembled figures and their components cannot both count. Operational individual-piece selling remains outside the initial scope.

Public BrickLink documentation describes subset inventories and per-item guides; aggregate API availability, live account access, rights, coverage and website-calculator parity remain unverified. No provider calls or Phase 1 feature implementation is authorized by this planning addition. D-001 through D-023 retain their history.
