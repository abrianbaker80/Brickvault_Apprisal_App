# BrickVault Appraisal App

One private, self-hosted LEGO sourcing and appraisal platform for Brian. The planned core starts with a set number (including 75331-1) or name, compares whole-set/minifigure values and four-view Part-Out Value with part-level liquidity, evaluates strategy profit/ROI/maximum buy, saves deals/watchlists and explains supported Sets-to-Hunt opportunities.

Marketplace screenshots and recognition are later optional inputs into the same catalog and valuation core. Direct lookup works with every image feature disabled.

## Current checkpoint

The approved Phase 1 implementation plan and actual validation evidence are recorded in [ExecPlan 000](docs/plans/000-local-foundation.md). Slice 1A is accepted at 150caf77820d09c60d028eeeba5b1b4317e11539; Slice 1B is accepted and locally committed at d79395223b5d6fedf78e01dabd3202b5526211eb. Phase 1 is incomplete; Slice 1C is not started. The subsequent D-025 Part-Out Value/liquidity amendment changes planning only and passes independent acceptance for one local documentation checkpoint.

Phase 1 has three bounded slices: 1A toolchain/workspace; 1B isolated database, API, and contracts; 1C web shell, built serving, CI, and full acceptance. Each requires its own explicit request and ends with a report. [Prompt 01](prompts/01_scaffold_foundation.md) remains a reusable plan-only review, not an implementation command.

The accepted tooling selections and exact locks remain unchanged. After the local documentation checkpoint, the exact next action is **Phase 1 Slice 1C — web shell, local built serving, browser tests, CI, and complete Phase 1 acceptance.** Its implementation requires a separate explicit request. Follow [workflow guidance](CODEX_WORKFLOW.md); this review authorizes only the documentation checkpoint, with no push or automatic Slice 1C/Phase 2 start.

Use [local development](docs/LOCAL_DEVELOPMENT.md) for locked setup, db:up/db:migrate/db:status/db:stop, dev:api, contract generation, unit/integration checks and API packaging. Backend verification uses real PostgreSQL. Frontend builds, static serving, browser checks and CI remain Slice 1C.

## Product and architecture

- React + Vite + TypeScript supplies one primary interface for responsive Chrome, the installable PWA, and Android packaging (Capacitor preferred, subject to its later spike).
- FastAPI serves the production static build and all API routes under /api; one PostgreSQL database is authoritative.
- Server-side catalog/provider adapters and exact-decimal deterministic valuation serve every client.
- Sold evidence and current listings, new and used, and whole-set versus split-sale strategies remain distinct.
- Missing prices are unknown; quantities, provenance, freshness, profit, ROI, and maximum-buy constraints are explicit.
- [Part-Out Value and liquidity intelligence](docs/plans/005-set-part-out-values.md) spans Phases 2–8: separate NEW/USED × SOLD/CURRENT, supported recoverable gross, Gems, Liquid POV, Fast Cash, Dead-Stock Exposure, concentration/break-even/density/burden, shared refresh and explainable Hunt components. Theoretical value, gross, net and profit stay separate; no sale guarantee or numerical threshold is implied.
- Recognition, image storage, overlays, and training retention are later modules; AI predictions are never confirmed labels.
- Home-server discovery and deployment are separate, explicitly authorized phases.

## Read and continue

1. Read [AGENTS.md](AGENTS.md), [project context](docs/PROJECT_CONTEXT.md), and [product specification](docs/PRODUCT_SPEC.md).
2. Use [valuation rules](docs/VALUATION_RULES.md) and [traceability](docs/REQUIREMENTS_TRACEABILITY.md) to verify product scope.
3. Follow [architecture](docs/ARCHITECTURE.md), [data model](docs/DATA_MODEL.md), [decisions](docs/DECISIONS.md), and [roadmap](docs/ROADMAP.md).
4. Review [ExecPlan 000](docs/plans/000-local-foundation.md), then run only the separately requested prompt under [workflow guidance](CODEX_WORKFLOW.md).
5. Later-module details are preserved in [image ingestion](docs/IMAGE_INGESTION.md) and [provider gates](docs/PROVIDER_GATES.md).

## Planned repository shape

    apps/web/           Shared React UI: Chrome, PWA, Android web assets
    apps/android/       Later Android wrapper and needed native extensions
    services/api/       FastAPI and shared catalog/market/valuation domain
    packages/contracts/ Generated OpenAPI and TypeScript contracts
    infra/              Isolated local PostgreSQL Compose; deployment separate
    scripts/            Guarded local development and validation commands
    docs/               Requirements, architecture, rules, plans
    prompts/            Contiguous Phase 0–16 tasks
    .agent/PLANS.md      ExecPlan requirements

Use pnpm for web/contracts and uv for Python. Create only modules needed by the authorized phase. The starter ZIP is historical material: do not extract it over the repository or treat it as active instructions.
