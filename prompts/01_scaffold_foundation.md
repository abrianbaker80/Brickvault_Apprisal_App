# Prompt 01 — Repository and local foundation

**Mode:** Plan only

**Expected result:** An in-chat review of the canonical approved Phase 1 plan; no file or runtime changes

## Instructions

This prompt is PLAN ONLY, including in a mode that permits edits. Read AGENTS.md, CODEX_WORKFLOW.md, README.md, .agent/PLANS.md, product/context/history/decision/architecture/data-model/valuation/security/traceability documents, the roadmap, and docs/plans/000-local-foundation.md. The approved detailed plan has been persisted; review it against current repository facts without implementing it.

Return a self-contained in-chat plan with exact future file/command contracts, unchanged final acceptance, and separate Slice 1A/1B/1C authorization and stop boundaries. Keep paths portable and apply the plan's narrow implementation documentation-update rules. Do not modify files, scaffold, install/update dependencies, create manifests/locks/migrations/containers/configuration/CI, start services, open database connections, call providers/network resources, access infrastructure, stage, or commit.

Future commands are contracts, not existing commands to execute. Installed toolchain/version/port checks belong only to their separately authorized implementation slice.

## Inputs

Approved product/architecture and canonical [ExecPlan 000](../docs/plans/000-local-foundation.md); current documentation baseline and explicit task boundaries.

## Scope

Review React/Vite responsive shell, FastAPI, isolated PostgreSQL, SQLAlchemy/Alembic empty baseline, health/readiness/OpenAPI and generated TypeScript contracts, strict checks, provider-free CI, and local setup documentation.

## Exclusions

Catalog imports/providers/pricing/valuation/set search/deals/authentication/Sets to Hunt, listing/image/recognition work, PWA/Android, home infrastructure, deployment, and all implementation or Git mutations in this plan-only prompt.

## Acceptance evidence

The future complete Phase 1 shell/API uses an isolated migrated database and passes contract/format/lint/type/unit/integration/build and built-serving desktop/mobile browser checks, with provider-free CI definitions and reproducible local setup. No product tables or external providers are needed.

The canonical plan's final acceptance is unchanged by the slice split. No application check is claimed by this review.

## Gate and access

The approved plan-only review has occurred. Reusing this prompt remains offline and read-only. A separate explicit implementation request must name one slice:

- **Slice 1A — Toolchain and workspace:** verify compatible stable toolchains; workspace/manifests/configuration, exact locks, and format/lint/type/orchestration foundations; explicitly authorized local lock checkpoint; report and stop before database or application shells.
- **Slice 1B — Database, API, and contracts:** isolated PostgreSQL, guarded tooling, SQLAlchemy/Alembic, health/readiness/OpenAPI, generated contracts and relevant real tests; report and stop before frontend and CI completion.
- **Slice 1C — Web shell, built serving, CI, and acceptance:** React shell, Vite proxy, FastAPI static serving, browser tests, GitHub Actions, all final acceptance, permitted documentation; report and stop before Phase 2.

Completing one slice does not authorize the next. The next separately authorizable action is Slice 1A only; the documentation baseline commit is not implementation authorization. No product-provider calls, existing PostgreSQL on 5432, or home/production access belongs to any slice.

## Stop condition

Return the in-chat plan and stop without edits or implementation. Do not interpret this prompt, approval, persistence, or a mode change as a slice execution request.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
