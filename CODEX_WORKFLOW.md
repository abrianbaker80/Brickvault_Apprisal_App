# Codex Workflow for BrickVault Appraisal App

## Current checkpoint and next task

The approved detailed [ExecPlan 000](docs/plans/000-local-foundation.md) is the canonical Phase 1 execution plan. Slice 1A is accepted from documentation baseline cb3e4373ee02faf4a485eb451d98749090f34e17: all applicable checks pass, including 17 tests, and the reviewed local checkpoint contains exactly 27 files. The plan records the durable acceptance evidence, bounded fixes, deferred checks, and inventory. Phase 1 is not complete.

The current authorized action is **Slice 1A acceptance review, bounded correction, and conditional local commit**. Approved selections remain TypeScript 5.9.3 with openapi-typescript 7.13.0, repository-local uv 0.12.10, and ESLint 10.10.0 / @eslint/js 10.0.1 / typescript-eslint 8.69.0. Use the verified uv wrappers and repository-owned paths in local setup. The next implementation checkpoint is **separate explicit authorization for Slice 1B**; it has not started. No push or branch change is authorized.

[Prompt 01](prompts/01_scaffold_foundation.md) remains a reusable plan-only review. Its approved review has occurred; reopening that prompt still does not authorize implementation. Historical realignment checkpoint wording in product/history/security documents and dated decisions records the earlier task; current progress belongs here and in ExecPlan 000. Product and security obligations remain unchanged.

## Phase 1 execution boundaries

| Slice | Authorized scope when separately requested | Required stop |
|---|---|---|
| 1A — Toolchain and workspace | Verify stable toolchain/package compatibility; create workspace/manifests/configuration; resolve exact locks; format/lint/type/orchestration foundations; local lock checkpoint only when explicitly authorized | Report actual checks before database infrastructure, connections, application shells, or CI |
| 1B — Database, API, and contracts | Isolated PostgreSQL development/test infrastructure, guarded tooling, SQLAlchemy/Alembic, health/readiness/OpenAPI, deterministic TypeScript contracts, unit/integration checks | Report before frontend/built-serving/browser/CI completion |
| 1C — Web shell, built serving, CI, and acceptance | Responsive React status shell, Vite proxy, FastAPI static serving, browser tests, GitHub Actions, complete Phase 1 acceptance, permitted documentation | Report and stop before Phase 2 |

Each slice requires a separate explicit implementation authorization. Completing one never authorizes the next. Dependency/tool acquisition requires that slice's explicit local/network scope. No product-provider calls, home access, PWA/Android, domain workflow, or existing PostgreSQL on 5432 belongs to Phase 1.

The original Slice 1A implementation request retained working-tree changes for review. The subsequent acceptance request permits one exact-list local checkpoint only if acceptance passes, with an existing Git identity, complete staged review, and no ignored or unrelated files. Never use blanket staging or force-add ignored files; nothing may be pushed.

## Documentation-update rules during Phase 1 implementation

Read-only by default:

- AGENTS.md
- docs/ORIGINATING_CHAT_SUMMARY.md
- docs/PRODUCT_SPEC.md
- docs/VALUATION_RULES.md
- docs/SECURITY_PRIVACY.md

Change one only for a concrete verified contradiction that cannot be accurately documented elsewhere. Any proposed change must be narrow, evidence-backed, and explicitly reported; routine implementation progress does not qualify.

Normal status updates belong primarily in README.md, CODEX_WORKFLOW.md, docs/PROJECT_CONTEXT.md, docs/ROADMAP.md, docs/REQUIREMENTS_TRACEABILITY.md, docs/LOCAL_DEVELOPMENT.md, and docs/plans/000-local-foundation.md. Update docs/ARCHITECTURE.md only for verified implementation details. Keep future domain schemas and accepted historical decisions intact; record newly accepted decisions additively.

Use repository-relative paths wherever sufficient. Resolve the repository root dynamically rather than hard-coding a machine/user/checkout location. [Local development](docs/LOCAL_DEVELOPMENT.md) now records tested Slice 1A setup, final checks, deferred application acceptance, and the temporary-cache cleanup limitation. The next implementation slice is 1B only after a separate explicit request.

## Chat strategy

Use one repository and a fresh chat for each major phase; keep tightly scoped plan review and its separately authorized implementation together where practical. Each chat reads [AGENTS.md](AGENTS.md), [product spec](docs/PRODUCT_SPEC.md), [valuation rules](docs/VALUATION_RULES.md), [traceability](docs/REQUIREMENTS_TRACEABILITY.md), current decisions, roadmap, and relevant ExecPlan.

The [originating summary](docs/ORIGINATING_CHAT_SUMMARY.md) is chronological context. Historical image-first instructions and the starter ZIP never override current decisions. Preserve accepted image contracts in their later module.

## Prompt rhythm

1. Select one phase from [ROADMAP.md](docs/ROADMAP.md), and one explicitly named slice for Phase 1.
2. Establish its entry gate, scope, permitted access, and exclusions.
3. Review the self-contained ExecPlan under [.agent/PLANS.md](.agent/PLANS.md).
4. A plan-only request returns the plan in chat and stops. A documentation/local-Git request changes only its authorized Markdown and reviewed Git checkpoint.
5. Implement only the separately requested slice/phase after required access gates are satisfied.
6. Run applicable verification, inspect the full diff, and report actual evidence and limitations.
7. Stage/commit only on Brian's explicit request; never advance automatically or push implicitly.

Prompt 00 is bootstrap/revalidation. Prompt numbers 01–16 map one-to-one to roadmap phases; 1A/1B/1C are execution slices inside Phase 1, not new numbered phases/prompts. Prompts 13–16 remain optional later image work.

## Model, evidence, and special gates

Use current user-selected settings. Do not spawn subagents unless the user or applicable task instructions explicitly request delegation.

Fixtures prove behavior, not live provider entitlement, rights, or market coverage. Phase 3 resolves provider access/use constraints; Phase 4 proves representative feasibility before supported sourcing is claimed. No version or provider research was refreshed in this documentation checkpoint.

Phase 9 requires Android package/physical core-flow evidence. Phase 10 hardens a local release. Phase 11 requires explicit read-only home discovery authorization; Phase 12 requires a distinct reviewed deployment authorization. Prompt 15 cannot claim overlay/Facebook compatibility from a build.

Never broaden localhost to LAN/public access implicitly. Keep secrets out of chat/clients. Preserve unrelated uncommitted work; never use blanket stage/reset/clean to simplify a checkpoint.
