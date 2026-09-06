# BrickVault Appraisal App — Codex Guidance

## Product truth

- One private application for Brian: a deliberately unified LEGO sourcing and appraisal platform with a deterministic valuation-first MVP.
- Direct set-number (including suffixed variants) and name search, whole-set new/used evidence, every included minifigure and quantity, individual/totals pricing, deal math, saved work, and Sets to Hunt are core requirements.
- Chrome, PWA, and Android use one primary React UI, one FastAPI backend, and one authoritative PostgreSQL database.
- Marketplace photos, listing sessions, recognition, overlays, and training data are later optional modules. Direct lookup must work when all image features are disabled.
- The product name is BrickVault Appraisal App; repository slug is brickvault-appraisal-app.
- Eventual home hosting and an approved abrianbaker.com subdomain confer no present authorization to access or modify any server, Proxmox, router, DNS, Cloudflare, or production system.
- Checked-out guidance is current. The starter ZIP is historical; never restore it over the repository.

## Read before complex work

Read [project context](docs/PROJECT_CONTEXT.md), [originating history](docs/ORIGINATING_CHAT_SUMMARY.md), [product specification](docs/PRODUCT_SPEC.md), [valuation rules](docs/VALUATION_RULES.md), [traceability](docs/REQUIREMENTS_TRACEABILITY.md), [decisions](docs/DECISIONS.md), [architecture](docs/ARCHITECTURE.md), [data model](docs/DATA_MODEL.md), [roadmap](docs/ROADMAP.md), and the relevant plan.

Use an ExecPlan under [.agent/PLANS.md](.agent/PLANS.md) for complex features, cross-stack work, migrations, integrations, capture, security, or deployment. The current [ExecPlan 000](docs/plans/000-local-foundation.md) covers only the local foundation.

## Working method and authorization

- Work in small reviewable vertical slices and implement only the explicitly requested milestone.
- Current checkpoint and the next separately authorizable slice are recorded in [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md) and [ExecPlan 000](docs/plans/000-local-foundation.md). Phase 1 uses separate explicit authorizations for Slices 1A, 1B, and 1C; completing one never starts the next. [Prompt 01](prompts/01_scaffold_foundation.md) remains plan-only.
- Plan approval, persistence, or a mode change does not authorize code, dependencies, service startup, network/provider calls, server access, staging, or a commit.
- Never stage or commit unless Brian explicitly requests it. Preserve unrelated dirty work.
- Inspect existing code/tests before future edits; diagnose root causes and use proportionate verification rather than presenting workarounds as solutions.
- Keep durable requirements here, not only in chat. Record accepted changes additively in decisions.
- Distinguish fixtures, live provider evidence, builds, emulator results, and physical-device verification; never fabricate any of them.
- Stop at missing required account access, rights, paid-call authorization, device evidence, or infrastructure approval. Do not request secrets in chat.
- This documentation task installs nothing. General advice to install missing tools does not override a task's explicit no-install boundary.

## Architecture guardrails

- React + Vite + TypeScript belongs in apps/web; the same primary interface is packaged for Chrome/PWA/Android. Capacitor is preferred for Phase 9 pending a documented spike.
- apps/android holds the later wrapper and genuinely needed native extensions; Kotlin/Compose is not a second implementation of the core UI.
- FastAPI serves the configurable production static build and all routes under /api. Vite proxies /api locally; unknown API routes must remain JSON errors, not frontend HTML.
- services/api owns catalog identity, set/minifigure relationships, provider mappings, market evidence, valuation, deals, settings/watchlists, hunting, authentication, and synchronization.
- Clients never call catalog/pricing/AI providers directly or independently implement financial rules.
- Use explicit server-side provider adapters; keep provider/model IDs configurable. Later recognition returns candidate canonical identities to the same core, with no separate catalog or valuation engine.
- PostgreSQL is authoritative. Use reviewed Alembic migrations for every schema change, never runtime create_all.
- Generate OpenAPI from Pydantic and TypeScript in packages/contracts; use openapi-fetch. No manually duplicated contract shapes.
- Use uv for Python and pnpm for web/contracts. Start without Redis, brokers, Kubernetes, MinIO, or microservices. Add pgvector only in a measured later retrieval feature.
- Later image bytes use a replaceable BlobStore abstraction; it is not part of Phase 1.

## Financial and provider invariants

- [VALUATION_RULES.md](docs/VALUATION_RULES.md) is authoritative: exact decimal money, explicit currency, documented conversions and rounding.
- New/used and sold/current-listing evidence stay separate. Do not infer sealed/complete condition from an unsupported provider flag.
- Missing price or mapping is unknown, never zero or an arbitrary first match. Include provider-scoped IDs, source versions, quantities, review states, periods, sample information, and freshness.
- Preserve quantity-aware figure totals and missing/damaged adjustments; mutually exclusive sale strategies cannot double-count figures, residual builds, or components.
- Net proceeds precede acquisition cost; profit subtracts acquisition cost; ROI uses acquisition cost and is undefined at zero.
- Account for purchase-dependent tax/premiums in both target-ROI and minimum-profit maximum-buy constraints. Recommendations are deterministic, explainable, versioned, and blocked for missing required evidence.
- Provider access does not establish display, cache, image, training, or historical-retention rights. Follow [provider gates](docs/PROVIDER_GATES.md); bounded retries, quota handling, provenance, and honest unavailable states are required.
- Catalog/market feasibility precedes the engine and direct-search product; recognition never gates them.

## Later image integrity — Phases 13–16 only

- Follow [IMAGE_INGESTION.md](docs/IMAGE_INGESTION.md); none of this is a Phase 1 requirement.
- Preserve immutable originals, SHA-256 exact deduplication, distinct assets/derivative lineage, and explicit privacy classes.
- Upload independently with partial success. Results use listing_image_id for the listing-to-image relationship, not an asset.
- Assign client upload UUID and display_order before dispatch; retries preserve UUID, bytes, and position.
- Persist deterministic ordering from minimum successful receipt positions, with database uniqueness constraints and explicit conflicts.
- Every successful new or duplicate submission creates or reuses a durable receipt; replay recovers lost responses without extra records.
- Approve image retention/deletion policy before shipping. A model prediction is not ground truth; only Brian-confirmed or purchase-verified, privacy-reviewed labels may become training-ready.
- Keep rejected candidates as appropriate hard negatives; keep all connected listing/source derivatives, including shared exact originals, in the same dataset split.

## Later Facebook and Android capture boundaries

- Never scrape Facebook or other sources, intercept traffic/credentials, automate seller interactions, or browse/capture unattended.
- Brian explicitly triggers each capture. Show active status, restrict supported package names, and keep Share/manual-upload fallbacks.
- Use supported APIs; platform documentation is not proof of Facebook compatibility. Physical-device verification is required for Phase 15.
- Native share/overlay code extends the shared app; it does not duplicate catalog, price, or offer logic.

## Security and scope boundaries

- Provider credentials stay server-side; never commit secrets, cookies, seller identities, or production configuration. Future .env.example contains placeholders only.
- Exclude secrets, image bytes, unnecessary listing text, authorization headers, and private filenames from logs.
- Phase 1 is unauthenticated and loopback-only; use isolated local development/test PostgreSQL and do not connect to or modify the existing service on 5432.
- Add private authentication in Phase 7 before any non-loopback exposure, with explicit network scope approval; do not expose an unauthenticated development service.
- Phase 11 is separately authorized read-only discovery. Phase 12 requires a reviewed plan and distinct deployment approval. PostgreSQL is never public.
- Later screenshots may contain names, profile images, locations, messages, and notifications; apply retention, access, redaction, and deletion rules before that feature ships.
- Read [SECURITY_PRIVACY.md](docs/SECURITY_PRIVACY.md) for current and later-module obligations.

## Quality gates and review priorities

For implementation, run relevant formatter, linter, type/static checks, unit/integration tests, and builds. Verify changed UI routes at responsive viewports; distinguish Android builds from physical tests. Use real PostgreSQL for persistence behavior and deterministic barriers for concurrency tests.

For documentation-only tasks, inspect the complete diff including new documents, resolve local Markdown links, check roadmap/prompt/traceability consistency, preserve historical decisions, and confirm no non-document changes. Do not install dependencies or start services for documentation checks.

Flag incorrect money/ROI/max-buy math, double counting, missing data treated as zero, guessed provider mappings, unsupported rights/coverage claims, duplicated client arithmetic, predictions promoted to truth, lost originals/receipts, unstable image order, migration omissions, secret exposure, unauthorized infrastructure work, and tests that mock away the behavior being claimed.

Report changes, actual validation, limitations, and the next authorized milestone; stop there.
