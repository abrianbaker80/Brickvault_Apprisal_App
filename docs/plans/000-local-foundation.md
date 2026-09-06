# Phase 1 — Local foundation implementation plan — ExecPlan 000

**Status:** Slice 1A ACCEPTED for the reviewed local checkpoint. Slices 1B and 1C NOT STARTED. Phase 1 is not complete.

**Date:** 2026-09-05

**Owner:** Brian

This is the canonical, self-contained Phase 1 execution plan under D-021 and D-022. It incorporates the approved in-chat plan and Brian's documentation-checkpoint refinements: portable paths, narrow documentation-update rules, and separately authorized Slices 1A, 1B, and 1C.

The documentation baseline is commit cb3e4373ee02faf4a485eb451d98749090f34e17. Brian subsequently authorized Slice 1A implementation only, including bounded official documentation/registry/package access and a repository-local uv bootstrap. The initial implementation verified a clean baseline. The subsequent acceptance-review request expects the dirty Slice 1A result and authorizes bounded corrections plus one local commit only after acceptance passes. Branch changes, push, services, containers, database connections, infrastructure, and application source remain excluded. Slices 1B and 1C still require separate requests. Historical checkpoint statements below describe their dated authorizations.

Read [workflow](../../CODEX_WORKFLOW.md), [guidance](../../AGENTS.md), [architecture](../ARCHITECTURE.md), [data model](../DATA_MODEL.md), [roadmap](../ROADMAP.md), [security/privacy](../SECURITY_PRIVACY.md), [valuation rules](../VALUATION_RULES.md), [traceability](../REQUIREMENTS_TRACEABILITY.md), and [decisions](../DECISIONS.md). [Prompt 01](../../prompts/01_scaffold_foundation.md) remains a reusable plan-only review; it is not an implementation command.

## 1. Goal and user-visible outcome

Establish the local foundation for Brian's unified LEGO sourcing and valuation application.

Brian can open a responsive React application, see whether FastAPI is running, and see whether an isolated PostgreSQL database has the expected migration revision. The same frontend build can run locally through FastAPI.

Phase 1 delivers infrastructure and application shells only. It creates no product workflow or product-domain tables. Executing each bounded slice requires its own separate explicit implementation request.

## 2. Why this work is being done now

Catalog ingestion, market-data feasibility, and deterministic valuation need reproducible development tooling, database migrations, and shared API contracts.

This phase proves those foundations without making catalog, pricing, images, or recognition prerequisites for starting the application. The authoritative order remains foundation, catalog, market integration, representative feasibility, valuation, direct search, saved workflows, hunting, shared PWA/Android, local hardening, and separately approved infrastructure work. Images and recognition remain later optional modules.

## 3. In scope

- One pnpm workspace and one uv-managed Python project.
- React/Vite responsive web shell.
- FastAPI shell with health, readiness, OpenAPI, and local static serving.
- Isolated PostgreSQL development and test instances.
- SQLAlchemy connectivity and Alembic migrations.
- Validated configuration, safe logging, and consistent API errors.
- Formatting, linting, strict typing, unit/integration/contract/browser tests.
- GitHub Actions checks without live product providers.
- Local setup, recovery, and verification documentation.

These are future implementation deliverables, not work authorized by the documentation checkpoint.

## 4. Explicit non-goals

Do not implement:

- Catalog ingestion, set/minifigure relationships, Rebrickable, BrickLink, or market-price calls.
- Valuation, set search, deal calculations, saved deals, settings workflows, authentication, or Sets to Hunt.
- Listing sessions, uploads, thumbnails, image storage, BlobStore, recognition, AI, embeddings, or training.
- PWA/offline features, Capacitor, Android applications, or native capture.
- Home-server access, Proxmox, DNS, Cloudflare, router changes, public exposure, or deployment.
- Redis, queues, workers, pgvector, MinIO, microservices, application Docker images, or unnecessary empty future modules.

Do not connect to or modify the existing PostgreSQL service on port 5432. Do not move or rename the repository. Do not push or infer staging/commit authorization from completing a slice.

## 5. Current repository state

The documentation-stage repository began at initial commit 064cfcf. The earlier image-first plan was never implemented. The valuation-first realignment, expanded implementation plan, and reviewed Markdown baseline belong to the current local documentation checkpoint.

The clean baseline had no application manifests, source directories, migrations, scripts, tests, CI workflows, runtime configuration, or runnable setup commands. Slice 1A now adds only its manifests/configuration, exact locks, checked tooling, tests, and setup documentation. It adds no application source. Preserve unrelated dirty work in every future task.

All governing documents and the approved in-chat plan were reviewed. No toolchain checks, installs, services, database connections, network requests, or implementation checks were performed during this persistence checkpoint. Its local commit hash and final Git status are reported separately rather than embedding a self-referential commit hash here.

Dated bootstrap observations from 2026-09-05 are retained only as historical context: Windows 11 x64/about 32 GB RAM; Python 3.13.12 plus managed 3.14.3; Node 24.14.0; uv 0.10.7; pnpm 11.8.0; Docker CLI present but Linux engine unavailable/stopped; PostgreSQL 18.3 client and an existing service on 5432. These are not verified current readiness or permission to operate anything.

All inventory paths and commands in this plan are relative to the repository root unless stated otherwise. Markdown links are relative to their containing document. Resolve the root dynamically; Brian's current machine, username, or checkout directory is not an architectural or execution requirement.

## 6. Decisions and assumptions

### Workspace and dependency management

Use:

- A private root pnpm workspace containing apps/web and packages/contracts.
- One root pnpm-lock.yaml; no nested JavaScript lockfiles.
- One Python project in services/api, managed by uv.
- One services/api/uv.lock and project-local services/api/.venv.
- Native local API and Vite processes; Docker Compose supplies PostgreSQL only.
- Portable Node scripts for root command orchestration and a typed Python helper for database provisioning/testing.
- No workspace task framework such as Turborepo.

Use ordinary explicit API/application/persistence modules and synchronous SQLAlchemy transactions. Keep blocking database work outside the async event loop. Do not introduce generic repository or event-bus frameworks.

Use strict TypeScript, including noUncheckedIndexedAccess and exactOptionalPropertyTypes; checked JSDoc for .mjs orchestration; strict mypy for authored Python; Ruff, ESLint, and Prettier for their respective files.

### Approved version constraints

These families derive from the planning baseline with the explicit D-023 corrections. Actual installed/resolved versions and remaining limits are recorded in section 14. PostgreSQL image selection remains deferred to Slice 1B.

| Component | Proposed constraint |
|---|---|
| Python | >=3.13,<3.14 |
| Node.js | >=24,<25 |
| pnpm | >=11,<12 |
| uv | Exactly 0.12.10, repository-local executable only |
| PostgreSQL | Supported stable 18.x |
| FastAPI | >=0.141,<0.142 |
| Pydantic | >=2.13,<2.14 |
| pydantic-settings | >=2,<3, compatible with selected Pydantic |
| SQLAlchemy | >=2.0,<2.1 |
| Alembic | >=1.19,<1.20 |
| Psycopg | >=3.3,<3.4, binary distribution for local development |
| Uvicorn | >=0.30,<1, compatible stable release |
| React / React DOM | Matching 19.2.x versions |
| Vite | >=8.2,<8.3 |
| TypeScript | >=5.9.3,<5.10; initial exact selection 5.9.3 |
| Vite React plugin | Compatible stable release within >=5,<7 |
| openapi-typescript | >=7.13,<7.14 |
| openapi-fetch | >=0.17,<0.18 |
| Vitest | >=4.1,<4.2 |
| Playwright | >=1.63,<1.64 |
| ESLint / @eslint/js / typescript-eslint | >=10.0.0,<11 / compatible 10.x / compatible 8.x; initial selections 10.10.0 / 10.0.1 / 8.69.0 |
| Prettier | 3.x |
| Ruff / mypy | Compatible stable <1 / 1.x |
| pytest / HTTPX | Compatible 9.x / >=0.28,<1 |
| Hatchling | Compatible 1.x |

Use compatible React 19 type packages, Testing Library React 16, jest-dom 6, and jsdom 26–29 for browser unit tests.

### Approved tooling corrections — 2026-09-05

These selections were persisted as approved with verification pending before installation. Approval itself is not evidence; subsequent actual results are recorded in the progress and outcome sections.

- TypeScript 5.9.3 with openapi-typescript 7.13.0 replaces the former TypeScript >=6.0,<6.1 proposal because the generator requires TypeScript ^5.x. Use one selected compiler across authored workspace packages.
- ESLint 10.10.0 with @eslint/js 10.0.1 and typescript-eslint 8.69.0 replaces ESLint 9.x, which reached end of life on 2026-08-06. Their published requirements determine compatibility; ESLint and @eslint/js patch/minor numbers need not match. Use supported flat configuration without peer overrides, warning suppression, or legacy switches.
- Bootstrap official standalone uv 0.12.10 under .local/tooling/uv/0.12.10/ after ignoring .local/. Inspect the official version/platform release metadata and verify published archive integrity before extraction/execution. An official archive or inspected version-specific installer in documented unmanaged mode is permitted. Do not modify global uv 0.10.7, PATH, profiles, registry, or execution policies.
- Invoke that local executable explicitly; missing/wrong-version tools fail with setup guidance. Enforce `[tool.uv] required-version = "==0.12.10"`. Use installed Python 3.13 only and disable automatic Python downloads. Keep all caches/environments ignored.
- Retain the intended Hatchling build backend without dummy source. Slice 1A synchronizes dependencies with `sync --project services/api --locked --all-groups --no-install-project`, then checks `lock --project services/api --check`. Application package installation/build remains mandatory after source exists; later acceptance must not substitute dependency-only synchronization.

References verified during prerequisite research: [generator peer metadata](https://registry.npmjs.org/openapi-typescript/7.13.0), [ESLint support](https://eslint.org/version-support/), [typescript-eslint support](https://typescript-eslint.io/users/dependency-versions/), and [official uv release](https://github.com/astral-sh/uv/releases/tag/0.12.10). See D-023 for the additive decision record.

During separately authorized Slice 1A, verify official support status and peer compatibility, then select and lock exact stable versions within these constraints. Record resolved versions. A nonexistent, unsupported, or incompatible branch requires a documented correction before scaffolding proceeds; do not silently adopt a different major version or prerelease.

Pin Node/Python versions in their version files, pnpm in packageManager, and uv in project/CI configuration. Verify and pin the PostgreSQL image patch/digest when its Slice 1B infrastructure is authorized; no image pull or container startup belongs to Slice 1A.

Preserve the earlier unverified patch candidates as historical planning evidence only: Python 3.13.15, Node 24.20.0 LTS, FastAPI 0.141.1, Pydantic 2.13.5, PostgreSQL 18.6, SQLAlchemy 2.0.52, Alembic 1.19.2, Psycopg 3.3.5, React 19.2.8, Vite 8.2.2, TypeScript 6.0.3, uv 0.12.10, pnpm 11.25.0, openapi-typescript 7.13.0, openapi-fetch 0.17.0, Vitest 4.1.11, and Playwright 1.63.0. These are not guaranteed releases or required patch pins.

Future official references, not accessed during persistence: [Python releases](https://www.python.org/downloads/), [Node releases](https://nodejs.org/en/about/previous-releases), [PostgreSQL support](https://www.postgresql.org/support/versioning/), [Vite releases](https://vite.dev/releases), [TypeScript releases](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html), [FastAPI version guidance](https://fastapi.tiangolo.com/deployment/versions/), [uv project layout](https://docs.astral.sh/uv/concepts/projects/layout/), and [OpenAPI TypeScript client](https://openapi-ts.dev/openapi-fetch/).

### Deferred verification commands

None of these commands were run during this checkpoint. In an authorized Windows Slice 1A run, inspect local executable availability and versions:

    Get-Command git, node, pnpm, uv, docker -ErrorAction SilentlyContinue
    node --version
    pnpm --version
    .local/tooling/uv/0.12.10/uv.exe --version
    .local/tooling/uv/0.12.10/uv.exe python list --only-installed
    docker context show
    docker context inspect

Docker context inspection reads local configuration. Do not contact its endpoint before confirming a local named pipe or Unix socket. Daemon readiness and port checks belong to separately authorized Slice 1B; do not start Docker in Slice 1A:

    docker version
    docker compose version
    docker info
    Get-NetTCPConnection -State Listen -LocalPort 8000,5173,55432,55433,18000 -ErrorAction SilentlyContinue

Authorized package verification in Slice 1A includes official release/support documentation, metadata, and constrained dependency resolution:

    pnpm view vite@8.2 engines peerDependencies --json
    pnpm view @vitejs/plugin-react@6 engines peerDependencies --json
    pnpm view typescript-eslint@8 peerDependencies --json

The plugin command checks the proposed 6.x candidate; if it is unavailable or incompatible, verify the allowed 5.x candidate before selecting it. Successful resolution alone does not establish support or security. Future Linux checks use equivalent local executable/port inspection; committed task scripts must not require PowerShell or a particular checkout path.

## 7. Data model and API/interface changes

### Exact planned file inventory

All paths below are relative to the repository root. Brace groups enumerate individual files; they are inventory notation, not shell commands. Only the Slice 1A inventory is now implemented.

Created in authorized Slice 1A:

    .gitignore
    .editorconfig
    .node-version
    .env.example
    package.json
    pnpm-workspace.yaml
    pnpm-lock.yaml
    tsconfig.base.json
    tsconfig.json
    tsconfig.tools.json
    eslint.config.mjs
    prettier.config.mjs
    .prettierignore
    scripts/tasks.mjs
    scripts/tasks.test.mjs
    apps/web/package.json
    apps/web/tsconfig.json
    packages/contracts/package.json
    packages/contracts/tsconfig.json
    services/api/.python-version
    services/api/pyproject.toml
    services/api/uv.lock
    docs/LOCAL_DEVELOPMENT.md

Create in separately authorized Slice 1B:

    infra/compose.dev.yml
    scripts/database.py
    scripts/test_database.py
    packages/contracts/openapi.json
    packages/contracts/src/index.ts
    packages/contracts/src/schema.d.ts
    services/api/alembic.ini
    services/api/src/brickvault_api/{__init__.py,main.py,settings.py,observability.py,contracts.py}
    services/api/src/brickvault_api/api/{__init__.py,health.py,errors.py}
    services/api/src/brickvault_api/application/{__init__.py,readiness.py}
    services/api/src/brickvault_api/persistence/{__init__.py,database.py}
    services/api/src/brickvault_api/migrations/env.py
    services/api/src/brickvault_api/migrations/script.py.mako
    services/api/src/brickvault_api/migrations/versions/0001_foundation.py
    services/api/tests/conftest.py
    services/api/tests/unit/{test_api.py,test_settings.py,test_contracts.py}
    services/api/tests/integration/{test_database.py,test_migrations.py}

Create in separately authorized Slice 1C:

    .github/workflows/ci.yml
    apps/web/vite.config.ts
    apps/web/index.html
    apps/web/playwright.config.ts
    apps/web/src/main.tsx
    apps/web/src/App.tsx
    apps/web/src/App.test.tsx
    apps/web/src/styles.css
    apps/web/src/api.ts
    apps/web/src/test/setup.ts
    apps/web/e2e/shell.spec.ts
    services/api/src/brickvault_api/api/static.py
    services/api/tests/unit/test_static.py

Later slices extend previously created configuration, scripts, main/API modules, tests, and setup documentation as needed within the final inventory. Keep Alembic resources inside the Python package so the built distribution carries the same migration graph used by readiness checks.

Slice 1A creates manifests/configuration but no API or frontend source shell, placeholder domain modules, generated contracts, migrations, Compose files, or CI. Retain Hatchling configuration for the intended Python package and use the explicitly authorized --no-install-project synchronization while source is absent. Verify actual package installation in Slice 1B when source exists. Do not fabricate an empty API package merely to make Slice 1A tooling pass. Typecheck applicable tooling then, and report future application checks as not yet available rather than false passes.

### Documentation-update rules during implementation

Treat these as read-only by default:

- AGENTS.md
- docs/ORIGINATING_CHAT_SUMMARY.md
- docs/PRODUCT_SPEC.md
- docs/VALUATION_RULES.md
- docs/SECURITY_PRIVACY.md

They may change only if implementation reveals a concrete verified contradiction that cannot be accurately documented elsewhere. Any such proposed change must be narrowly scoped, justified with actual evidence, and explicitly reported. Routine progress, version checks, and file-layout facts do not meet that exception. Preserve historical decisions and later image/provider contracts.

Normal Phase 1 implementation-status updates are limited primarily to:

- README.md
- CODEX_WORKFLOW.md
- docs/PROJECT_CONTEXT.md
- docs/ARCHITECTURE.md, only where verified implementation details belong
- docs/ROADMAP.md
- docs/REQUIREMENTS_TRACEABILITY.md
- docs/LOCAL_DEVELOPMENT.md
- docs/plans/000-local-foundation.md

Keep docs/DATA_MODEL.md unchanged unless a verified foundation schema-contract discrepancy needs a narrow correction; Phase 1 is not permission to redesign future product entities. Record any newly accepted decision additively, without rewriting D-001 through D-021.

These implementation-update rules do not erase historical checkpoint wording. CODEX_WORKFLOW.md and this plan carry the current checkpoint and next separately authorizable slice. Keep all repository references portable.

### Expected ignored local/generated artifacts

- Root .env.local.
- services/api/.venv/, Python caches, and services/api/dist/.
- Workspace node_modules/, apps/web/dist/, coverage, Playwright reports, and temporary test files.
- A .local/ directory for guarded runner locks and temporary validation artifacts.

No other application directories, placeholder domain modules, or tracked artifacts are planned. dev:init belongs to Slice 1A configuration/orchestration; creating local configuration does not authorize a database connection.

### Local development and built frontend

- Vite binds to 127.0.0.1:5173 with strict port selection.
- FastAPI binds to 127.0.0.1:8000.
- Browser requests use relative /api URLs.
- Vite proxies /api to FastAPI during development.
- openapi-fetch consumes generated contract types.
- Do not enable broad CORS or expose server configuration through VITE_*.

The shell contains the application name, separate API/database status indicators, loading and unavailable states, and a Retry button. It uses accessible labels and status announcements. It contains no search box, deal form, or simulated product data.

In local built-serving mode, FastAPI serves the configured build's index.html at /, build assets under /assets, and API routes under /api. Phase 1 needs only the / frontend route. Additional routes and navigation fallback belong to actual later screens. Unknown API routes and missing assets always remain errors.

Missing build output causes an explicit startup error when static mode is requested. Normal API-only development does not require a frontend build. No deployment configuration is created.

### PostgreSQL isolation and migrations

Use two independently named Compose projects:

| Purpose | Project | Host binding | Storage |
|---|---|---|---|
| Development | brickvault-appraisal-dev | 127.0.0.1:55432 | Dedicated named volume |
| Tests | brickvault-appraisal-test | 127.0.0.1:55433 | Separate named volume; disposable test databases |

Do not use explicit global container names or external volumes. Verify Docker context locality and project ownership before provisioning or stopping containers.

Development uses database brickvault_dev. Test runs create uniquely named `brickvault_test_<uuid>` databases and track their exact names for cleanup.

Use separate bootstrap, migration-owner, and runtime roles:

- Bootstrap credentials are used only by local provisioning.
- Migration owners have privileges only for their application database/schema and are not superusers.
- Runtime roles receive only connectivity/schema usage and read access needed for alembic_version in Phase 1.

Guard database tooling before opening a connection:

- Require an approved loopback hostname and expected port.
- Refuse port 5432, remote hosts, unexpected database names, and options that override host/port.
- Test commands refuse development targets.
- Cleanup requires an approved test target and a database name created by that run.

Create an empty baseline revision named 0001_foundation. Its application-schema effect is only Alembic's version bookkeeping; there are no product tables.

Clean initialization explicitly provisions roles/database, runs alembic upgrade head, and grants the runtime role its required access. Repeating initialization/migration preserves credentials and existing state.

The server never calls create_all, creates databases, or applies migrations. Autogeneration is only a draft requiring review. Retained databases use reviewed forward migrations; downgrade/re-upgrade checks run only against disposable test databases.

### Health, readiness, and OpenAPI contracts

| Endpoint | Contract |
|---|---|
| GET /api/health | 200: {"service":"brickvault-api","status":"ok"} |
| GET /api/ready | 200: {"status":"ready","database":"ok","migrations":"current"} |
| GET /api/openapi.json | 200: canonical OpenAPI JSON |

Readiness failures return HTTP 503:

    {"status":"not_ready","database":"unavailable","migrations":"not_checked"}

    {"status":"not_ready","database":"ok","migrations":"missing"}

    {"status":"not_ready","database":"ok","migrations":"mismatch"}

Readiness checks actual PostgreSQL connectivity and the installed revision against the packaged migration graph. Unknown, additional, or outdated revisions fail readiness. Unexpected database errors produce the redacted unavailable response.

Use bounded connection, pool-acquisition, and statement timeouts, initially two seconds each, without automatic retries. Liveness does not query PostgreSQL.

Disable Swagger/ReDoc routes in Phase 1, avoiding additional routes and externally hosted UI assets. All API routes, including any future API documentation routes, remain under /api.

Ordinary API errors use:

    {
      "error": {
        "code": "NOT_FOUND",
        "message": "Resource not found",
        "request_id": "server-generated-uuid"
      }
    }

Provide consistent handling for 400, 403, 404, 405, 422, and unexpected 500 responses. Never expose exception text or connection details. Each response carries X-Request-ID; health/readiness responses are not cached.

### Contract generation

Pydantic models and FastAPI route declarations are authoritative.

App construction and schema export must not open database connections or require runtime credentials. Validate runtime settings during application startup; the schema exporter does not enter that lifecycle.

Generate deterministic OpenAPI JSON and TypeScript declarations. Do not maintain duplicate response interfaces manually.

contracts:check regenerates into temporary storage and compares bytes with the committed/generated working files. It must detect drift even before initial files are committed, without rewriting them or relying on unrelated Git differences.

## 8. Implementation sequence

Each slice requires a separate explicit implementation authorization naming that slice and its permitted local dependency/network/service scope. Completing one slice never authorizes the next. Only Slice 1A has subsequent implementation authorization; the documentation baseline alone authorized none of them.

### Slice 1A — Toolchain and workspace

1. Inspect current Git changes and preserve unrelated work. Verify permitted local executable versions, official support, and package compatibility using section 6. Do not start services or contact Docker/database endpoints.
2. Create only the Slice 1A inventory: workspace/manifests/configuration, exact dependency locks, portable command foundations, and local setup documentation.
3. Resolve the Phase 1 dependency graph without implementing the later modules. Initial commands are pnpm install --strict-peer-dependencies and the explicitly invoked repository-local uv 0.12.10 with lock --project services/api. Use installed Python only, no Python downloads, and the root .local/uv-cache. Subsequent reproducibility checks use frozen/locked installation; Slice 1A sync includes --all-groups --no-install-project. Exact tested Windows commands are in LOCAL_DEVELOPMENT.md.
4. Add formatting, linting, strict typing, and orchestration foundations, including idempotent dev:init and meaningful orchestration tests. Run only checks with actual applicable files. Commands for later slices must not claim success or start work when unavailable.
5. The original implementation retained exact locks uncommitted for review. Brian's subsequent acceptance request permits one local checkpoint only after all applicable checks pass, with an explicit reviewed file list and complete staged validation. No push is authorized.
6. Report resolved versions, changed files, actual applicable checks, outstanding prerequisites, and checkpoint status. Stop before database infrastructure, migrations, API behavior, frontend source, built serving, or CI.

Slice 1A acceptance: dependency resolution and frozen/locked reproduction succeed; applicable formatting/lint/type/orchestration tests pass; version/lock evidence is recorded; no database or application shell exists. This is partial Phase 1 evidence, not final acceptance.

### Slice 1B — Database, API, and contracts

1. Require a separate explicit Slice 1B request and accepted Slice 1A evidence. Recheck relevant local Docker/port prerequisites before connecting; verify and pin the PostgreSQL image within authorized dependency access.
2. Create isolated PostgreSQL development/test infrastructure and guarded database provisioning/lifecycle tooling.
3. Add SQLAlchemy connection management, packaged Alembic tooling, and the reviewed empty baseline. Switch the existing Python project to its installable Hatchling package when the API source exists.
4. Implement runtime settings, safe logging/errors, health/readiness/OpenAPI, credential-free schema export, generated TypeScript contracts, and non-mutating drift checks.
5. Run relevant Python/tooling unit tests, real PostgreSQL integration tests, contract checks, and applicable format/lint/type checks. Verify the API package and migration resources without requiring an unbuilt frontend.
6. Update permitted documentation with actual evidence and stop with an explicit report before frontend shell, Vite proxy completion, built serving, browser checks, or CI completion.

Slice 1B acceptance: real migration/connectivity/readiness and failure tests pass; liveness/schema export remain database-independent; generated contracts are deterministic and drift is detected. Do not claim responsive UI or final Phase 1 acceptance yet.

### Slice 1C — Web shell, built serving, CI, and acceptance

1. Require a separate explicit Slice 1C request and accepted Slice 1B evidence.
2. Build the responsive React status shell and Vite /api proxy using generated contracts.
3. Add configurable FastAPI built-frontend serving with correct API/static error boundaries.
4. Add browser smoke tests and GitHub Actions without live product providers.
5. Run the entire unchanged Phase 1 acceptance sequence in section 9, including real database failures, built serving, responsive Chromium, and Windows/local evidence.
6. Update only permitted documentation with actual results and limitations. Inspect status and the complete diff; report every changed file. Stop before Phase 2 and without an implicit commit or push.

The three slices change execution boundaries, not final Phase 1 acceptance. A slice report must distinguish checks passed, checks unavailable because their slice is not yet implemented, and genuine blockers. Do not write placeholder product code or weaken acceptance to make an earlier slice appear complete.

## 9. Validation and acceptance criteria

### Documentation-only checkpoint checks

Before the authorized documentation commit, inspect Git status, all tracked differences and new Markdown content, local Markdown links, portable paths, 14 required plan sections, Phase 0–16 roadmap/prompt alignment, slice authorization gates, historical decisions, and preserved later image contracts. Verify no non-document worktree change and existing Git identity before staging literal reviewed paths. Inspect the full staged diff and file list before the one local commit; never push.

No command in the implementation sections below was run during this checkpoint.

### Required future command contract

| Command | Required behavior |
|---|---|
| pnpm dev:init | Create missing ignored local configuration with generated local credentials; preserve existing files |
| pnpm db:up | Start and provision only the development Compose project |
| pnpm db:migrate | Explicitly upgrade the guarded development database |
| pnpm db:status | Report current/expected development migration revision |
| pnpm db:stop | Stop this project's development/test services without deleting volumes |
| pnpm dev:api | Run API-only development mode on loopback |
| pnpm dev:web | Run Vite on loopback with its /api proxy |
| pnpm contracts:generate | Deliberately regenerate OpenAPI and TypeScript files |
| pnpm contracts:check | Detect contract drift without modifying source/generated files |
| pnpm format:check | Check authored Python, frontend, scripts, and configuration formatting |
| pnpm lint | Run Ruff and ESLint |
| pnpm typecheck | Run strict mypy and TypeScript checks |
| pnpm test:unit | Run Python, Vitest, and Node orchestration unit tests without PostgreSQL |
| pnpm test:integration | Manage guarded disposable databases and run real PostgreSQL tests |
| pnpm build | Build API wheel/sdist and Vite assets; verify packaged migration resources |
| pnpm test:e2e | Run Chromium against the built frontend served by FastAPI |
| pnpm serve | Serve an existing frontend build locally through FastAPI |

Integration and browser runners acquire an exclusive test-run lock, manage only the dedicated test project, and clean up databases/processes they created. They do not silently attach to an already-running application.

The browser runner binds its API to 127.0.0.1:18000, separate from interactive development. Future pnpm build/test:unit completion across applications is a Slice 1C gate; earlier slice reports identify only their actually available subchecks.

### Exact future full acceptance sequence — Slice 1C

After locks exist and local prerequisites are available, Slice 1B must first extend uv:sync to install
the real application (remove --no-install-project) and verify installation. The future sequence below
requires that change; the current Slice 1A dependency-only command cannot pass full application acceptance.
Retain its absolute cache/environment/temporary paths and local uv version guard:

    pnpm install --frozen-lockfile --strict-peer-dependencies
    pnpm uv:sync

    pnpm dev:init
    pnpm dev:init

    pnpm contracts:check
    pnpm format:check
    pnpm lint
    pnpm typecheck
    pnpm test:unit

    pnpm db:up
    pnpm db:migrate
    pnpm db:migrate
    pnpm db:status

    pnpm test:integration
    pnpm build

    pnpm --filter @brickvault/web exec playwright install chromium
    pnpm test:e2e

Run interactive development in separate terminals:

    pnpm dev:api

    pnpm dev:web

For built-serving verification, stop the development API first, then run:

    pnpm serve

Finally, stop project services without removing data:

    pnpm db:stop

Frozen installs verify previously generated locks; they cannot bootstrap nonexistent locks. The uv runner resolves the explicit local executable for its platform. Full Slice 1C synchronization must omit --no-install-project: actual application installation must then pass. None of these future commands broadens the currently authorized slice.

### Required test scenarios

#### Configuration and tooling

- Repeating dev:init leaves existing configuration byte-for-byte unchanged.
- Invalid configuration fails with the field name and safe explanation, without displaying its value.
- Wrong database host, port, name, or cleanup target is rejected before connecting.
- Port conflicts fail explicitly without killing another process or selecting an undocumented alternative port.

#### Database and migrations

- A fresh database upgrades to 0001_foundation.
- Repeated upgrade is harmless.
- The only application-schema table is alembic_version.
- A disposable database can downgrade to base and upgrade again.
- Runtime credentials can read migration state but cannot create application tables.
- Missing and incorrect revisions produce the specified 503 responses.
- A stopped dedicated test PostgreSQL service produces readiness 503 while liveness remains 200; the test runner restores the service it controls.

#### API and contracts

- Health and OpenAPI export work with no database connection and no provider credentials.
- Generated OpenAPI and TypeScript are deterministic.
- Deliberately stale generated content in an isolated temporary test copy makes contracts:check fail.
- Unknown /api routes return JSON 404, unsupported methods return JSON 405, and unexpected errors return redacted JSON 500.
- Request IDs correlate responses and logs without reflecting arbitrary incoming identifiers.

#### Frontend and static serving

- Built frontend passes at 1440 × 900 and 390 × 844.
- No horizontal overflow; keyboard access and visible focus work.
- Loading, ready, database unavailable, and network-error states are distinguishable.
- Retry recovers after the underlying service recovers.
- Database-status evidence uses real API/PostgreSQL behavior; browser interception is reserved for a transport-failure scenario.
- Direct navigation and reload at / work.
- Missing assets return 404; /api errors never return frontend HTML.
- Requests for .env, source files, traversal paths, and files outside the build directory do not disclose content.
- Browser application requests remain local; no CDN fonts/scripts or external providers are used.

#### Build and documentation

- All quality commands exit successfully.
- API artifacts include required migration resources.
- Frontend output contains no generated credential sentinel.
- Windows local startup/migration/static serving is verified.
- Record a manual Chrome check when Chrome is available; Chromium automation is reported separately.
- Setup documentation reproduces tested commands and explains preserved volumes and failure recovery.

Use real PostgreSQL for persistence behavior. Do not mock away the dependency or migration behavior claimed by an integration test. Use deterministic synchronization where concurrency is exercised.

### CI — Slice 1C

Use GitHub Actions because the configured repository remote is GitHub. Reading local remote configuration does not require remote access.

Run on pushes and pull requests with read-only repository permissions:

- Ubuntu 24.04: frozen installs, contract/format/lint/type/unit checks, real PostgreSQL integration tests, builds, and Chromium smoke tests.
- Windows 2022: frozen installs, contract/format/lint/type/unit checks, and builds to catch path and command portability problems.

Ubuntu installs Chromium and required OS libraries with:

    pnpm --filter @brickvault/web exec playwright install --with-deps chromium

Use the same root commands as local development. CI dependency downloads are distinct from product-provider integration: no provider credentials, live catalog/market calls, remote databases, or home infrastructure are required.

Pin reviewed actions to immutable commits during authorized Slice 1C. Upload failure reports only after excluding private configuration. Cleanup runs even when tests fail. Creating a workflow locally does not authorize pushing or remotely dispatching it; distinguish local validation from an actual hosted CI result.

## 10. Security, privacy, and data-integrity considerations

Use one ignored root .env.local, generated by dev:init; .env.example contains placeholders only.

Define typed settings for development/test mode, runtime and migration database URLs, local provisioning credentials, log level, API port, static-serving enablement, and build directory.

The bind address is fixed to loopback in Phase 1. Default API port is 8000; the owned browser-test process uses 18000. Static paths resolve to an explicit absolute directory at runtime and cannot expose the repository root. Runtime path resolution does not hard-code a checkout location in documentation or source.

Reject malformed values and unrecognized project-prefixed settings. Existing invalid credentials are reported, never silently regenerated. Provisioning settings are passed only to database tooling; frontend commands do not receive generated database secrets.

Validate Host and supplied Origin headers against local application addresses. Do not add permissive CORS. Authentication remains excluded, so these commands must not expose an unauthenticated non-loopback service.

Use standard-library structured JSON logging with timestamp/severity, server-generated request ID, HTTP method and matched route, response status/duration, and safe internal error category.

Do not log raw query strings, request bodies, authorization headers, database URLs, credential values, or unrestricted exception representations. Unknown routes use a generic route label rather than arbitrary path contents. No provider or production credentials are needed.

## 11. Failure modes, rollback, and recovery

- Missing/incompatible toolchain: stop at verification and report the exact conflict; do not substitute a different architecture. Install/update only within a separately authorized implementation slice's scope.
- Unavailable Docker engine: report the blocked local prerequisite; never substitute the existing PostgreSQL service or home server.
- Port conflict: preserve the occupying process and report the conflict.
- Existing configuration mismatch: preserve the file and explain the corrective local action without requesting secrets in chat.
- Migration mismatch/failure: remain not-ready; do not migrate during startup or reset retained data. Repair through a reviewed forward change.
- Contract drift: fix Pydantic/schema declarations or deliberately regenerate contracts; never bypass the check.
- Missing static build: fail static-mode startup with a safe setup error.
- Interrupted tests: clean up only recorded disposable databases and owned processes. Preserve development volumes.
- Blocked verification: report the slice and Phase 1 as incomplete, with the failed command and limitation; do not claim acceptance or begin the next slice.

Do not use broad reset, restore, clean, volume deletion, or unrelated process termination to make checks pass.

## 12. Progress log

- [x] 2026-09-05 — Read guidance, product documents/prompts, and product-scope audit; preserve historical decisions and later image contracts.
- [x] 2026-09-05 — Rebase the unexecuted image-first foundation to the unified valuation-first scope.
- [x] 2026-09-05 — Complete the in-chat Phase 1 plan-only review; Brian approves persistence with portable paths, documentation-update restrictions, and separate slices.
- [x] 2026-09-05 — Persist the approved detailed plan as this canonical ExecPlan. Documentation/local Git only; implementation remains unstarted.
- [x] 2026-09-05 — Receive explicit Slice 1A authorization and bounded TypeScript, local uv, and ESLint corrections; verify the required clean baseline before edits.
- [x] 2026-09-05 — Persist approved tooling corrections before installation. Installation and validation remain pending at this checkpoint.
- [x] 2026-09-05 — Create Slice 1A manifests/configuration, exact locks, local uv bootstrap, portable tooling and private initializer; no application source.
- [x] 2026-09-05 — Strict initial/frozen pnpm installation, local uv lock/locked dependency sync/check, unchanged-lock reproduction, format/lint/strict tooling types, and 13 Node tests pass; document corrected development failures and deferred checks.
- [x] 2026-09-05 — Run real dev:init twice with byte preservation, inspect secret/ignore/scope evidence and documentation; retain all Slice 1A work uncommitted for review. Stop before Slice 1B.
- [x] 2026-09-05 — Acceptance review verifies the required HEAD, empty index, four modified documents and 23 new files; reviews every authored file, tracked diff, and both complete lock structures. Correct cwd-dependent uv destinations and normalized configuration URLs; record reproducible regression evidence below.
- [x] 2026-09-05 — All applicable acceptance checks pass: frozen/locked offline reproduction, unchanged locks, formatting/lint/strict tooling types, 17 tests, private configuration preservation/redaction, ignore/credential scans, internal links, and diff checks. Local checkpoint is authorized after the required staged review; no Slice 1B work follows.
- [ ] Obtain separate explicit Slice 1B implementation authorization; execute only its bounded scope, report actual evidence, and stop.
- [ ] Obtain separate explicit Slice 1C implementation authorization; execute its scope and full Phase 1 acceptance, report, and stop before Phase 2.

The completed documentation-baseline checkbox remains historical. Slice 1A checkboxes record only the local tooling evidence below, not application acceptance or hosted CI results.

## 13. Open questions or physical-device/manual checks

The architecture and scope are decision-complete for review. No provider, Android, financial-default, or home-server decision is needed for Phase 1.

Remaining verification gates, not unresolved product choices:

- Availability and compatibility of proposed dependency branches.
- Access to a usable local Docker Linux engine in Slice 1B.
- Availability of the declared loopback ports.
- Correct Windows command, migration, and static-serving behavior.
- GitHub-hosted CI availability for this repository; a local workflow is not a hosted run.

Defaults are one pnpm workspace, one uv project, synchronous SQLAlchemy, separate development/test PostgreSQL projects, packaged Alembic resources, generated contracts, and GitHub Actions.

If verification invalidates a proposed branch or environment assumption, document the evidence and bounded correction before continuing. Do not expand Phase 1 to compensate. No physical Android test is needed for this shell.

## 14. Outcome and follow-up

The complete approved Phase 1 plan is persisted with portable repository paths and three separately authorized slices. Useful historical observations and references remain explicitly dated and unverified. The earlier image contract remains in [IMAGE_INGESTION.md](../IMAGE_INGESTION.md); recognition and capture remain later enhancements.

Phase 1 is complete only when all declared files exist, all required checks pass with recorded evidence, permitted documentation reflects the implemented foundation, and the final diff contains only authorized Phase 1 work plus preserved pre-existing changes.

Each slice report lists changed files, actual commands/results, unresolved limitations, and confirmation that existing PostgreSQL and production infrastructure were untouched. Completing any slice does not authorize another slice, staging/commit, push, or Phase 2.

### Slice 1A actual outcome — 2026-09-05 session

Starting HEAD was cb3e4373ee02faf4a485eb451d98749090f34e17 with clean index/worktree and the current directory confirmed as repository root. The complete Slice 1A inventory above now exists, including tsconfig.json to expose the tools project to typescript-eslint's supported project service. README.md, CODEX_WORKFLOW.md, this plan, and the additive D-023 decision entry are the only previously tracked modifications; roadmap, product, architecture, security, valuation, and earlier decision history remain unchanged.

Verified installed runtimes/tools: Git 2.54.0.windows.1, Node 24.14.0, pnpm 11.8.0, Python 3.13.12, repository-local uv 0.12.10. Read-only Docker CLI/Compose checks reported 29.2.1 / 5.0.2; desktop-linux resolves to a local named pipe and all five planned ports were free. Docker daemon readiness was not tested. Node 24 LTS/Python 3.13 family support and direct dependency requirements were researched through official documentation/registries.

Exact JavaScript direct selections: TypeScript 5.9.3 in root/web/contracts; eslint 10.10.0; @eslint/js 10.0.1; typescript-eslint 8.69.0; prettier 3.9.6; @types/node 24.13.3; react/react-dom 19.2.8; @types/react 19.2.18; @types/react-dom 19.2.7; vite 8.2.2; @vitejs/plugin-react 6.1.1; openapi-typescript 7.13.0; openapi-fetch 0.17.0; vitest 4.1.11; @playwright/test 1.63.0; @testing-library/react 16.3.3; @testing-library/dom 10.4.1; @testing-library/jest-dom 6.9.1; jsdom 29.1.1. Initial pnpm installation added 236 packages. No peer overrides, warning suppression, or second compiler were used.

Exact Python selections: fastapi 0.141.1; pydantic 2.13.5; pydantic-settings 2.15.0; sqlalchemy 2.0.52; alembic 1.19.2; psycopg/psycopg-binary 3.3.5; uvicorn 0.52.4; hatchling 1.32.0; ruff 0.16.6; mypy 1.20.2; pytest 9.1.1; httpx 0.28.1. uv.lock contains 41 records including the root project; 40 dependencies were synchronized without installing the application. Registry sources are PyPI only. Hatchling remains configured for the later real package.

The official uv Windows x64 archive SHA-256 f65744f94072152b1f86ba2aace4d01f1124d9a8ecb235805039e3718c36cac2 matched both published release digest and .sha256 asset. Explicit local invocation reported uv 0.12.10 (3c979abda 2026-09-04 x86_64-pc-windows-msvc). Global uv 0.10.7 was not replaced; executable hashes matched before/after. No PATH, registry, profile, global Git, Docker, or persistent execution-policy changes occurred.

Passed commands: pnpm install --strict-peer-dependencies; pnpm install --frozen-lockfile --strict-peer-dependencies; explicit local uv lock, sync --locked --all-groups --no-install-project, and lock --check; pnpm toolchain:check; pnpm dev:init twice; pnpm format:check; pnpm lint; pnpm typecheck; pnpm test:unit (13/13). Repeat installs/sync preserved both locks byte-for-byte. Lock SHA-256 values: pnpm-lock.yaml a047dd02498b1b68113bca873167a388eb2b66d1c0e8e0724920128dd6ee6be7; services/api/uv.lock 4fd75352f5d49ad72a30db22afba686d35c764b1ac56944e07c7e88af06f08bc. See [local setup](../LOCAL_DEVELOPMENT.md) for commands, exact argument boundaries, and test details.

The tests cover process exit status, shell-free argument/path handling, task dispatch/failure, valid and invalid configuration preservation/redaction, Git ignore refusal with an unchanged index, local uv resolution, and lint configuration coverage. An unused-variable stdin probe triggers @typescript-eslint/no-unused-vars and CLI exit 1 with no parser error. Project service corrected the earlier explicit-project optimization that read disk content instead of stdin. Formatting covers all new supported tooling/configuration inputs; modified historical Markdown receives diff/link/consistency review without broad reformatting. Ruff/mypy were installed and version-checked, but substantive Python checks are deferred because no authored Python source exists.

Initial development failures were corrected: uv's unsupported default-index key became a supported [[tool.uv.index]] entry; the cache path was corrected for cwd-relative resolution; Node tests now await registration; typed lint uses project service. Initial invalid settings caused ordinary downloads into the existing user cache. A small cache was also created at Downloads/.local/uv-cache before the relative path was corrected. Automatic approval review rejected relocating/removing that temporary cache with "blocked by policy"; it remains untouched. All final setup/reproduction commands use ignored repository .local/uv-cache. This is a recorded cleanup limitation, not an alternative toolchain or global configuration change.

Ignored repository artifacts are .env.local (generated local values never printed), root/workspace node_modules, services/api/.venv, and .local tooling/archive/integrity metadata/caches/disposable test directories/validation records. No application source, provider calls, database connections, services, containers, migrations, Compose, generated API contracts, CI, PWA, Android, images, recognition, or deployment exists. Linux/macOS execution, Windows cross-user ACL hardening, application installation/builds, real PostgreSQL and browser acceptance remain unverified/deferred.

That implementation session ended with an uncommitted review checkpoint. Its original next action was review; the subsequent acceptance record below supersedes its checkpoint status. Slice 1B — isolated database, API, and contracts — requires separate explicit authorization and refreshed Docker/port gates. Phase 1 remains incomplete.

### Slice 1A acceptance review — 2026-09-05 local / 2026-09-06 UTC

Entry gate passed: existing intended checkout, HEAD cb3e4373ee02faf4a485eb451d98749090f34e17,
empty index, and exactly four tracked document modifications plus 23 new files. No unrelated change
was found. No reset, branch/worktree change, relocation, or dependency version change was made.

The complete reviewed checkpoint inventory is the following 27 files. Generated locks were parsed
in full and checked against manifests, package records, dependency edges, sources, and integrity data;
all new authored files and the complete tracked modifications were read.

| Group | Exact reviewed files |
|---|---|
| Existing documents (4) | CODEX_WORKFLOW.md; README.md; docs/DECISIONS.md; docs/plans/000-local-foundation.md |
| New root configuration (12) | .editorconfig; .env.example; .gitignore; .node-version; .prettierignore; eslint.config.mjs; package.json; pnpm-workspace.yaml; prettier.config.mjs; tsconfig.base.json; tsconfig.json; tsconfig.tools.json |
| New locks (2) | pnpm-lock.yaml; services/api/uv.lock |
| New workspace manifests/configuration (6) | apps/web/package.json; apps/web/tsconfig.json; packages/contracts/package.json; packages/contracts/tsconfig.json; services/api/.python-version; services/api/pyproject.toml |
| New tooling and setup (3) | scripts/tasks.mjs; scripts/tasks.test.mjs; docs/LOCAL_DEVELOPMENT.md |

Findings and bounded corrections:

1. The reviewed services/api/pyproject.toml line 44 and original local setup commands selected
   `.local/uv-cache` relative to the caller, without a guarded shared invocation or an explicit
   environment destination. Read-only real-uv `cache dir` probes using the original --project and
   --cache-dir arguments resolved to root/.local/uv-cache from root but services/api/.local/uv-cache
   from the API directory. They created no cache. Existing tests never exercised effective uv paths.
   [uvInvocation](../../scripts/tasks.mjs) now derives absolute project/cache/environment/temp paths
   from the runner module, checks the local uv version, and rejects unsupported cwd before writes.
   The existing dispatcher provides only uv:sync, uv:check, and uv:cache with optional --offline;
   inherited uv overrides cannot redirect them. No package versions changed. Setup and the future
   full-acceptance instructions use this same runner instead of raw relative-path commands.
2. The original validateConfig URL checks (scripts/tasks.mjs lines 151–170 before corrections)
   accepted trailing whitespace and an embedded hostname tab because URL parsing normalized them.
   The extended invalid-existing-file test failed with `Missing expected exception` before the fix.
   Comparing parsed href with the original value now rejects normalization before field checks.
   The regression passes, preserves invalid bytes, and excludes credentials/input values from errors.

Cache regression evidence: three path tests plus a uv child-failure test bring the suite from 13 to 17
tests. They use the actual
installed uv offline, the actual sync/check arguments and child environment, and root/API invocations
in this checkout with spaces. Cache queries share all actual common options (only the operation and
unsupported cache-query interpreter option differ); actual sync/check commands also run unchanged.
Tests pin the API environment and check its Python sys.prefix, override inherited UV_* and temp
destinations with targets confined to ignored fixtures, and verify those unwanted paths stay absent.
Unsupported cwd/flags fail with exit 1 before creating any files. Test fixtures remain in ignored
.local/tests; uv temporary files stay in .local/tmp. Windows path tests are not Linux execution.
The child-failure test copies the existing runner and local uv into a disposable in-repository fixture,
feeds uv invalid fixture configuration, and proves its nonzero exit status survives while the
diagnostic sentinel is redacted. No fixture is staged or committed.

Commands and results recorded during acceptance:

| Check | Actual result |
|---|---|
| pnpm install --frozen-lockfile --strict-peer-dependencies --offline | Passed, all three workspace projects already up to date; strict peers/engines retained |
| pnpm uv:sync --offline | Passed; --locked --all-groups --no-install-project with installed Python only; 40 distributions, no brickvault-api package installed |
| pnpm uv:check --offline; pnpm uv:cache --offline | Passed; unchanged lock and absolute root/.local/uv-cache |
| node ../../scripts/tasks.mjs uv:sync / uv:check / uv:cache --offline from services/api (three separate commands) | Passed with the same cache/environment; real uv tests also cover these exact argument forms |
| pnpm toolchain:check and installed package metadata | Passed; Node 24.14.0, pnpm 11.8.0, Python 3.13.12, local uv 0.12.10, TypeScript 5.9.3 in all three packages, ESLint 10.10.0, typescript-eslint 8.69.0, Ruff 0.16.6, mypy 1.20.2 |
| Complete lock/manifests inspection | Passed; pnpm 261 package records and 261 snapshots, three importers, one TypeScript compiler, SHA-512 integrity on every package; uv 41 records and 176 SHA-256 official PyPI artifacts; exact direct requirements and Hatchling match |
| Original pnpm test:unit | Passed 13/13; no effective-cache regression existed |
| Extended invalid-configuration regression before/after correction | Failed for the expected missing rejection, then passed with unchanged invalid bytes and redacted errors |
| pnpm format:check; pnpm lint; pnpm typecheck; pnpm test:unit | Passed; 17/17 tests, zero skipped/deferred tests inside the applicable suite. ESLint negative input exits 1 for @typescript-eslint/no-unused-vars with no fatal parser error |
| Real root dev:init twice | Passed; existing private configuration preserved byte-for-byte without printing values |
| Ignore/credential/documentation/diff checks | Passed; 19 ignore probes, .env.example remains trackable, no private files tracked, no actual generated private values or credential patterns in the 27 reviewed files, 35 Markdown documents/187 local file links/one anchor checked, git diff --check clean |
| Staged review and git diff --cached --check | Passed; exactly 27 normal files (23 additions, four document modifications), all staged blob IDs match reviewed content, full staged patch scanned with no credentials/ignored/unrelated files, historical decisions preserved; repeated after this final evidence update |

Both lock SHA-256 values remain unchanged from the reviewed input: pnpm
`a047dd02498b1b68113bca873167a388eb2b66d1c0e8e0724920128dd6ee6be7`; uv
`4fd75352f5d49ad72a30db22afba686d35c764b1ac56944e07c7e88af06f08bc`.

The original incident remains recorded: early implementation wrote into the existing user uv cache
and created Downloads/.local/uv-cache. Automatic approval review rejected relocating/removing the
latter with "blocked by policy". Acceptance did not inspect, delete, relocate, clean, or otherwise
modify that leftover directory, and did not retry the rejected operation. Its cleanup remains
unresolved; it is not used by the verified commands and is not itself an acceptance blocker.

Deferred: substantive Python application checks and installation/builds, React/contracts compilation,
generated OpenAPI/contracts, API/frontend builds, real PostgreSQL/migrations/integration tests,
Docker daemon readiness, service/port readiness, browser/Chrome/responsive acceptance, CI execution,
Linux/macOS execution, Windows cross-user ACL hardening, and all Android/physical-device evidence.
There is no application source, database tooling, Compose, migration, CI workflow, provider/AI call,
service/container start, database connection (including 5432), home-infrastructure access, or deployment.
All acceptance dependency commands used offline caches; no fresh dependency research or upgrade ran.

Acceptance status: **PASSED**; no unresolved correctness, security, reproducibility, or scope finding
blocks Slice 1A. All 27 files are reviewed and all applicable checks passed before staging.
Existing Git user.name and user.email are configured; no identity or global setting was changed.
The requested commit message is `chore: complete phase 1a tooling and workspace foundation`.
The local checkpoint contains this acceptance record; its resulting commit hash and final Git status
are reported after Git returns, avoiding a self-referential hash in the commit. No failed hook is bypassed.
No push is authorized. Next checkpoint: **separate explicit Slice 1B authorization**. Slice 1B and
Slice 1C remain NOT STARTED; Phase 1 is incomplete.
