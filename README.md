# BrickVault Appraisal App

One private, self-hosted LEGO sourcing and appraisal platform for Brian. Start with a set number (including 75331-1) or name, inspect new/used whole-set and minifigure values, calculate profit/ROI and maximum buy, save deals and watchlists, and find supported opportunities in Sets to Hunt.

Marketplace screenshots and recognition are later optional inputs into the same catalog and valuation core. Direct lookup works with every image feature disabled.

## Current checkpoint

The approved Phase 1 implementation plan is persisted in [ExecPlan 000](docs/plans/000-local-foundation.md) as part of the valuation-first documentation baseline. Phase 1 has not started. The next action eligible for separate explicit implementation authorization is **Slice 1A — toolchain and workspace only**.

Phase 1 has three bounded slices: 1A toolchain/workspace; 1B isolated database, API, and contracts; 1C web shell, built serving, CI, and full acceptance. Each requires its own explicit request and ends with a report. [Prompt 01](prompts/01_scaffold_foundation.md) remains a reusable plan-only review, not an implementation command.

No application directories, manifests, dependencies, migrations, runtime configuration, CI workflows, or runnable setup commands exist yet. This checkpoint authorizes documentation and one reviewed local Git commit only; it authorizes no installs, services, database connections, network/server access, implementation, or push. Follow [workflow guidance](CODEX_WORKFLOW.md) for slice authorization and narrow documentation-update rules.

## Product and architecture

- React + Vite + TypeScript supplies one primary interface for responsive Chrome, the installable PWA, and Android packaging (Capacitor preferred, subject to its later spike).
- FastAPI serves the production static build and all API routes under /api; one PostgreSQL database is authoritative.
- Server-side catalog/provider adapters and exact-decimal deterministic valuation serve every client.
- Sold evidence and current listings, new and used, and whole-set versus split-sale strategies remain distinct.
- Missing prices are unknown; quantities, provenance, freshness, profit, ROI, and maximum-buy constraints are explicit.
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
    infra/              Later requested local dependencies; deployment separate
    scripts/            Future local development and validation commands
    docs/               Requirements, architecture, rules, plans
    prompts/            Contiguous Phase 0–16 tasks
    .agent/PLANS.md      ExecPlan requirements

Use pnpm for web/contracts and uv for Python. Create only modules needed by the authorized phase. The starter ZIP is historical material: do not extract it over the repository or treat it as active instructions.
