# Local development

## Phase 7B-1 authentication — accepted source checkpoint, 2026-09-17

The current source requires migration 0009 for protected operations. This task does
**not** apply it to brickvault_dev or provision Brian. Until a separately authorized
development migration and owner bootstrap, the updated application fails closed.

After that authorization, use the normal guarded migration procedure, then run
`pnpm auth:bootstrap` in a local interactive terminal. It verifies existing owner,
instance, target and migration identity before hidden password entry/confirmation.
It neither starts nor migrates PostgreSQL and has no password argument/env option.
The bootstrap refuses an existing principal. `pnpm auth:reset` requires that principal,
keeps its identity, changes its verifier and revokes every session atomically.
Choose Brian's password locally; never put it in chat, shell history or .env files.
Hidden-input fallback is rejected. These commands have not been run for Brian.

The existing loopback launcher explicitly enables the HTTP cookie exception;
direct environment startup defaults BVA_AUTH_ALLOW_LOOPBACK_HTTP to false and accepts
only literal true/false. HTTPS requires Secure cookies; proxy trust/bind/Host restrictions
remain unchanged. This is not network-exposure authorization. Readiness and live schema
now require login; `pnpm contracts:generate` still exports offline without credentials.

`pnpm build` then `pnpm test:e2e` uses the guarded TEST runner: one disposable migrated
database, synthetic account, reserved loopback API port and the real built app. Tests
use real authentication while existing product fixtures remain synthetic. The runner
cleans its exact database/processes and restores prior TEST service state; it does not
attach to a development server. Passwords/cookies never enter persisted browser state
or frontend configuration. See [ExecPlan 074](plans/074-brian-only-authentication.md)
for session activity rules, qualified evidence and source-checkpoint acceptance.
Operational setup remains unauthorized; 7B-2 is next and not authorized.

## Phase 6B implementation boundary — 2026-09-14

The new complete-set refresh UI/API requires the accepted migration 0008. This task
does not migrate `brickvault_dev` or activate live provider work. Default launchers
leave refresh unavailable until explicitly configured. After review/checkpoint and
separate real-product acceptance authorization, the owned API launcher supports
`services/api/.venv/Scripts/python.exe scripts/serve_api.py --static --market-account-scope <existing-approved-account-UUID>`.
This verifies the existing development instance and uses the existing server-side
credential location; it does not provision/migrate or load provider credentials at
startup. Do not place account settings in Vite or browser configuration. The optional
UUID must match the account of the existing cache and provider credentials.

Read-only planning shows the request estimate before Refresh now. Status and Resume
recover unfinished durable operations after reload; Resume preserves the same root
and allowance. All-current confirmation uses zero provider requests. The first real
development migration and button click are still pending. See
[market operations](MARKET_OPERATIONS.md#phase-6b-public-complete-set-refresh--2026-09-14)
and [ExecPlan 060](plans/060-product-surface.md#phase-6b-public-workflow-implementation--2026-09-14).

## Current Phase 6A startup and product checks — 2026-09-13

Use the existing configured, migrated, owned local database: `pnpm.cmd db:up`, then
`pnpm.cmd dev:api` and `pnpm.cmd dev:web` in separate terminals. Open
[the local app](http://127.0.0.1:5173/) or [41802-1](http://127.0.0.1:5173/sets/41802-1).
The loopback API uses 8000; Vite proxies `/api`. No new migration or dependency is
required. The API launcher verifies ownership and passes its marker internally;
it does not provision/migrate. Search supports numbers, variants and multiword names.
Appraisal reads existing eligible cached evidence without provider credentials or
refresh. Missing pricing remains unavailable; service failures offer safe retry.

`pnpm.cmd test:e2e` now runs four deterministic product cases using synthetic HTTP
fixtures and its own Vite server. Stop an existing 5173 server first. It needs no
database or provider configuration. Real database GET/immutability coverage lives
in `services/api/tests/integration/test_product.py`. Older shell-browser procedures
below are historical, not the current product test command.

Independent review reproduced the legacy port-18000 failure, then corrected the
owned TEST helper to bind port 0 and hold the assigned socket through Windows
process spawn. The wrapper records the actual port, checks health/readiness/schema
and request boundaries, joins its owned child, and restores TEST state. It now exits
successfully. Normal environment-based startup retains 8000 (development) and
18000 (test); ephemeral injection belongs to the owned test helper. No Windows
reservation or production network setting changes. [ExecPlan 060](plans/060-product-surface.md)
records independent acceptance, the reviewed inventory and cleanup.

**Phase 3C offline accepted — 2026-09-12 UTC:** F5 is corrected and deterministic PostgreSQL regressions pass. [ExecPlan 030, section 18](plans/030-market-provider.md#18-independent-phase-3c-offline-acceptance--2026-09-12-utc) preserves the finding and records final verification and the reviewed 32-file checkpoint scope. Phase 3 is complete locally; Phase 4 requires separate authorization. Historical checkpoints below remain dated evidence.

**Current checkpoint — 2026-09-11:** Phase 2 is locally accepted: official development generation 1, cached no-op and history preservation verified, cleanup correction tested, and all 61 intended files independently reviewed. This acceptance does not establish deployment or the deferred product capabilities. See [ExecPlan 020](plans/020-catalog-foundation.md). Phase 3 is not started.

Dated execution records below preserve historical outcomes and then-applicable authorization; their pending or blocked states do not supersede this checkpoint.

## Historical Phase 2D observation correction and fourth-run stop — 2026-09-10 local

**Historical Phase 2D outcome — 2026-09-10 local: BLOCKED at a different development SQL timeout.** The requested observation timeout is proven and corrected by in-transaction candidate color-fact analysis. An independent matching retained-state probe changes SELECT from a 300-second timeout to 0.820762 seconds and full rollback INSERT to 57.537484 seconds; corrected retained official acceptance inserts 1,557,375 observations in 55.291041 seconds and passes 72 pre/postactivation cases plus no-op. All 264 Python units, 22 Node tests, 11 React tests, 196 PostgreSQL tests, six browser cases and build/contracts/package gates pass. Authorized fourth NEW development run `bcf21407-15ab-44bb-b358-17f600282599` instead times out earlier at step 16 `evidence_conflict:elements` in 300.004024 seconds (57014); its cause is not yet proven. Construction rolls back before the corrected observation step, validation, benchmark or activation. Read-only verification confirms zero candidate facts/validation, official generation 0/no receipts, unchanged two synthetic snapshots/four receipts/generation 4, and all three prior failed histories/staging unchanged. A fourth terminal failed run is retained. The accepted Windows publisher, migration 0005, existing indexes and 300-second limit remain unchanged. No fifth import, provider call, staging cleanup, Git checkpoint or Phase 3 work occurs. See the [current 42-item report](PHASE_2D_OBSERVATIONS.md). Earlier stops below remain historical evidence.

Reports may be read during operations. Windows replacement conflicts receive bounded atomic retries; exhausted auxiliary publication emits independent safe diagnostics. Invalid content and final acceptance evidence remain strict. Consult durable DB state/receipts rather than replaying SQL based on a stale report. All four failed development runs are terminal; preserve their staging and do not rerun the one-shot development helper. The observation correction passes retained disposable acceptance. The fourth attempt stops earlier at evidence_conflict:elements. Diagnose that new timeout with faithful retained-state prerequisites before any separately authorized new import; never resume a terminal run.

## Historical Phase 2D retained-history diagnosis — 2026-09-09

The previous official development build failed after 503.785 seconds at the
existing 300-second statement limit. Its terminal run, unvalidated candidate,
retained staging and synthetic generation-4 history are preserved. Existing
migration 0005 is already applied in development; this diagnosis creates no
migration, index, timeout increase or server configuration change.

The authorized comparison uses separate owned disposable test databases:
`pnpm catalog:smoke -- --source <cached-manifest> --diagnose-build`, with
`--retained-history` for two accepted synthetic snapshots and four activations.
Plans, statement timings and exact-backend activity remain under ignored
`.local/catalog/rebrickable`. Each database is removed only after its durable
report is written, and the owned container's original running state is restored.
No data download is part of these commands. See [diagnostic operation and
privacy details](CATALOG_IMPORT.md#candidate-construction-diagnostics--authorized-2026-09-09).

All SQL diagnosis gates passed before development was inspected. Its new import
passed the former timeout operation, then stopped at progress-report publication
after successful SQL. Both failed runs, candidates, exact old staging and synthetic
generation-4 history remain preserved; no official activation occurred. At that checkpoint the next
correction concerned atomic Windows report publication, with a sharing regression
and safe failure metadata. Neither terminal run may resume. See the [historical
32-item blocker and sizing evidence](PHASE_2D_BUILD_DIAGNOSTICS.md).

## Slice 2C queries — 2026-09-09

The packaged head is `0005_catalog_search_indexes`: five revisions, eight frozen SQL resources,
53 catalog tables, no new extension or runtime privilege. The two new indexes support normalized
exact/prefix names and PostgreSQL `simple` full-text matching. Accepted migrations 0001–0004 remain
unchanged. [Query semantics and validation commands](CATALOG_IMPORT.md) describe the read-only
snapshot boundary, modes, limits and benchmark manifests; [ExecPlan 020](plans/020-catalog-foundation.md)
records actual verification and the separately approved migration extension.

Use `pnpm catalog:validate -- --snapshot <accepted-synthetic-snapshot-uuid> --manifest
services/api/tests/fixtures/catalog/synthetic/benchmark-import-smoke.json` as one command against an
already running/migrated owned development database. It never starts, migrates or activates anything.
The deeper `benchmark.json` expectations belong to the explicitly authored relational test fixture,
not the retained bulk-import development state. All implementation tests use disposable databases;
no development migration or history reset is part of this implementation run. A later development
smoke needs its normal explicitly authorized setup at the current package head first.

The dated 2B/2A/Phase 1 entries below preserve their earlier heads and counts. Their use of "current"
is historical. Full Phase 2/provider acceptance, market data and deployment are still unverified.

## Slice 2B offline operations — 2026-09-08

Current packaged Alembic head: `0004_catalog_staging`; 0001–0003 remain unchanged. Migration 0004 adds fifteen tables (53 total), with runtime SELECT limited to 41 non-staging tables. Use the existing guarded `pnpm db:up` / `pnpm db:migrate` only for explicitly authorized local setup, then `pnpm catalog:import -- --source <manifest>`, `pnpm catalog:status`, and explicit `pnpm catalog:activate` with snapshot, expected active snapshot/generation and receipt UUID. Commands never start/reset/migrate databases themselves. [Complete command examples and recovery](CATALOG_IMPORT.md), [manifest/profile rules](CATALOG_SOURCES.md), and [validation/cleanup evidence](plans/020-catalog-foundation.md) are authoritative.

Wheel/sdist checks verify all four revisions, six frozen SQL resources, provider/import modules and 53-table metadata independently from the source checkout. Tests/fixtures/private configuration stay excluded. The Phase 1/2A sections below preserve historical counts and scope; 2B completion does not claim new UI, provider or physical-device acceptance.

## Slice 2A catalog foundation — 2026-09-07

The current packaged Alembic head is `0003_catalog_inventory`: unchanged empty `0001_foundation`, then `0002_catalog_identity` (29 tables) and `0003_catalog_inventory` (nine tables). [ExecPlan 020](plans/020-catalog-foundation.md) records the design and verification. Existing `pnpm db:migrate` performs guarded forward migration when explicitly invoked; application startup never migrates. This slice tested only runner-owned disposable databases, preserving development data and named volumes.

Runtime has enumerated SELECT grants on the 38 catalog tables plus Alembic bookkeeping; no writes, DDL, temporary tables, activation or owner-role access. Default privileges remain restrictive. Existing integration/unit commands discover the new tests; no catalog command, parser, staging, provider credential or source archive is needed. Wheel/sdist builds include frozen migration SQL and the typed package; tests/fixtures are excluded from distributions. The independently installed wheel verifies three revisions and SQL resources without database/provider access. Both locks and dependency versions remain unchanged.

Independent local 2A acceptance passed on 2026-09-08 after correcting source-freeze isolation: 106 real PostgreSQL tests, 98 Python/21 Node/11 React unit tests, API smoke, contracts, quality checks and package/frontend builds passed. Full findings and cleanup are recorded in ExecPlan 020. No frontend behavior changed, so no new browser acceptance is claimed. The Phase 1 sections below preserve their historical counts and baseline-only schema description; current catalog status is recorded here and in ExecPlan 020. Phase 2B is not started.

Slice 1A is accepted at 150caf77820d09c60d028eeeba5b1b4317e11539. Slice 1B supplies
isolated PostgreSQL, API-only serving, migrations and generated contracts. See
[ExecPlan 000](plans/000-local-foundation.md) for actual acceptance evidence and
[workflow](../CODEX_WORKFLOW.md) for authorization. Independent Phase 1 local acceptance
passed on Windows on 2026-09-07 for the authorized local completion checkpoint.
Hosted CI execution and home-server/production deployment are separate, unverified boundaries.

## Prerequisites and locked setup

Use the accepted Node 24.14.0, pnpm 11.8.0, installed Python 3.13.12 and repository-local
uv 0.12.10. Direct application versions and both exact lockfiles are unchanged from
Slice 1A. Do not use global uv or the abandoned outside-repository cache.

From the repository root, run each command separately and stop on failure:

    pnpm install --frozen-lockfile --strict-peer-dependencies
    pnpm toolchain:check
    pnpm uv:sync
    pnpm uv:check
    pnpm uv:cache
    pnpm dev:init

uv:sync now performs normal --locked --all-groups project installation, including
brickvault-api. It no longer uses --no-install-project. uv commands accept optional
--offline and are also supported as `node ../../scripts/tasks.mjs uv:sync` (or uv:check,
uv:cache) from services/api. The existing runner preserves absolute project/environment,
.local/uv-cache and .local/tmp destinations, rejects unsupported working directories
and overrides, and verifies the explicit local executable. No automatic Python
downloads or dependency upgrades occur.

dev:init validates and preserves existing private bytes, including generated passwords.
Do not overwrite .env.local to solve a connection failure. It is ignored, as are .local
ownership receipts, test ledgers, caches and package-verification environments. Preserve
.env.local and .local/database ownership records with retained database volumes. A moved
checkout or missing ownership receipt requires explicit review; tooling never adopts
an existing resource from its name alone.

## Docker and PostgreSQL

The helper verifies effective context/environment locality before daemon calls and pins
that context for the operation. Docker/Compose overrides fail with setup guidance.
Only a local named pipe or Unix socket and Linux engine are accepted. Do not select a
remote context or connect to host PostgreSQL on 5432.

The initial missing named pipe was repaired using Docker's supported
`docker desktop start --timeout 45` under Brian's task-specific expanded local repair
authorization. No reinstall, reset, Windows change, data deletion or reboot was needed.
The resume inspection found an external upgrade to Desktop 4.89.0.238018 / Engine
29.7.2 / Compose 5.5.0; this task did not perform that upgrade. Existing Akaunting
containers are paused and an unrelated container is running; preserve those states.
Future machine repair still needs applicable authorization.

Pinned official image:

    docker.io/library/postgres:18.6-bookworm@sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af

It was verified against official PostgreSQL support information, Docker official-image
metadata and the registry manifest, then pulled by digest. On a new authorized machine,
pull that exact reference before db:up; the helper uses --pull never. The default
PGDATA is /var/lib/postgresql/18/docker and volumes mount at /var/lib/postgresql.
See the [official image documentation](https://github.com/docker-library/docs/blob/master/postgres/README.md#pgdata).

| Purpose     | Compose project           | Host publication | Named volume                   | Application database                  |
| ----------- | ------------------------- | ---------------- | ------------------------------ | ------------------------------------- |
| Development | brickvault-appraisal-dev  | 127.0.0.1:55432  | brickvault-appraisal-dev_data  | brickvault_dev                        |
| Integration | brickvault-appraisal-test | 127.0.0.1:55433  | brickvault-appraisal-test_data | brickvault_test_ followed by UUID hex |

Each project uses its own bridge network and normal container port 5432. Every host
publication is explicitly loopback. There are no global container names, host-directory
mounts, external volumes, privileged containers or socket mounts. An internal-only
network was tested and rejected during implementation because it produced no effective
host publication; only that run-owned container/network was replaced, with its volume
preserved. The helper now verifies actual running-container publication as well as
configured ports, ownership labels, source Compose path, image, mounts and network.

## Database commands

    pnpm db:up
    pnpm db:migrate
    pnpm db:status

db:up explicitly starts/provisions the development service. db:migrate explicitly applies
the packaged Alembic graph and runtime read grant. Run them in this order; db:up alone
does not claim migrations are current. Repeating provisioning and migrations preserves
passwords and database identity. The only application-schema table is alembic_version,
at revision 0001_foundation.

Bootstrap credentials are used only by guarded administration. Migration owners are
nonsuperusers without database/role-management privileges. Runtime roles receive
CONNECT, schema USAGE and SELECT on alembic_version, with no DDL, temporary-table or
revision-write privileges. PUBLIC grants on the application and maintenance databases
are restricted and tested on the owned instance. App startup/readiness never provisions,
grants or migrates.

Connections require canonical 127.0.0.1 URLs, the purpose-specific port/database/role,
and generated passwords. Whitespace normalization, query options, remote/ambiguous
hosts, port 5432 and inherited PG* settings are rejected before connection. Test
templates in .env.local cannot themselves become connection targets.

    pnpm test:integration

The integration runner holds an OS-backed exclusive lock, creates UUID databases,
records resources under .local/database/runs, migrates and tests against real PostgreSQL,
runs a temporary API on 127.0.0.1:18000, and cleans only its recorded, ownership-verified
databases. It restores the owned test service after the intentional outage, then returns
that service to its prior running/stopped state. Development data and named volumes
remain intact. Injected test-failure and interruption cases also exercise real database
cleanup. A forced OS process kill or machine failure cannot guarantee cleanup; consult
the exact ledger before any recovery and never delete databases by prefix alone.

To stop both owned services without deleting volumes:

    pnpm db:stop

No command prunes, uses down -v, kills a port owner, changes ports silently, or adopts
unknown resources. Paused/restarting or mismatched project resources require inspection.
Do not print Compose configuration, container environment or private connection strings.

## API-only development

    pnpm dev:api

The process stays attached to its launcher on Windows, validates local runtime settings,
and serves only 127.0.0.1:8000. Ctrl+C stops it. Port conflicts fail; no process is killed
and no alternate port is selected. Only selected runtime settings reach the server.
This command does not serve the frontend. Swagger, ReDoc and permissive CORS remain disabled.
Use the explicit built-serving command below when a frontend build exists.

| Route                 | Success                                                |
| --------------------- | ------------------------------------------------------ |
| GET /api/health       | 200, service brickvault-api and status ok; no DB query |
| GET /api/ready        | 200, status ready / database ok / migrations current   |
| GET /api/openapi.json | 200, canonical generated schema                        |

Readiness returns 503 for database unavailable/not_checked, or database ok with migrations
missing/mismatch. It compares exact installed revisions with the packaged graph.
Connectivity, statement and pool acquisition timeouts are two seconds each, without
application retries; these individual bounds are not a two-second total request SLA.
Synchronous database checks execute outside the async event loop. Lifespan disposes the
engine; database failure does not prevent liveness.

Host must match localhost or 127.0.0.1 with the active API port. A supplied Origin must
be an exact HTTP local application origin on 8000, 5173 or 18000. Unknown routes,
invalid requests/methods and unexpected errors return redacted JSON. Responses receive
server-generated X-Request-ID and no-store; logs exclude queries, bodies, arbitrary
incoming IDs, credentials and raw exceptions.

## Contracts and quality checks

    pnpm contracts:generate
    pnpm contracts:check
    pnpm format:check
    pnpm lint
    pnpm typecheck
    pnpm test:unit
    pnpm build:api

FastAPI/Pydantic is authoritative. Generation exports without .env.local, credentials,
DB connections or a running server. The already-pinned openapi-typescript CLI produces
schema.d.ts; index.ts exports its types. contracts:check generates in ignored .local
storage, compares bytes and never rewrites expected files. It detects drift before
initial Git commit. Isolated fixtures prove a nonzero drift result without damaging
real generated files. Root, services/api and packages/contracts are supported working
directories; invoke the root runner by its relative path from a package.

Formatting, linting and strict typing cover authored Node tooling, Python source/tests,
contracts, React, Vite and browser tests. Slice 1C checks comprise 21 Node tests,
70 Python unit/tooling tests, 11 React tests, 28 real PostgreSQL integration tests
and six Chromium scenarios. Both visible Python warnings originate in transitive
Starlette 1.6.0: its TestClient fallback to the approved direct HTTPX 0.28.1 dependency,
and its use of AnyIO 4.15.1's deprecated BlockingPortal alias. Application code does not
use that alias. Switching to httpx2 would introduce an unapproved dependency family;
upstream changes remain deferred. No warning is suppressed and no package was upgraded.

build:api uses installed pinned Hatchling to create the API wheel/sdist, checks packaged
migration resources, installs the wheel in an independent ignored environment using
repository-local uv and exact uv.lock-derived constraints, then verifies import, migration
graph and credential-free export outside repository source paths. File URIs preserve
spaces in constraint/artifact paths. Official PyPI downloads are used for missing cached
locked artifacts; no new dependency versions are resolved. Artifacts stay in
services/api/dist and .local/package-check. The aggregate build below includes this same check.

## Web development and built serving

After `pnpm db:up` and `pnpm db:migrate`, use separate terminals:

    pnpm dev:api
    pnpm dev:web

Open http://127.0.0.1:5173. Vite binds strictly to 127.0.0.1:5173 and proxies relative
/api requests to 127.0.0.1:8000, with no broad CORS. An occupied port fails without
killing its owner or selecting another port. Frontend tooling does not load dotenv
files and receives only an allowlist of OS/runtime environment settings.

Stop the development processes with Ctrl+C before built serving on API port 8000:

    pnpm build
    pnpm serve

Open http://127.0.0.1:8000. The foundation shell displays separate API and database
status, announced loading/ready/unavailable states and a keyboard-operable Retry
button. Readiness failure (503) differs from transport failure with unknown database
state. Requests time out after ten seconds; Retry checks both endpoints again.
The shell has no product workflow, fabricated product data or remote assets.

`pnpm build` builds/verifies the API wheel/sdist and Vite output, checks all published
frontend bytes against actual generated private values and the CI credential sentinel,
and rejects extra root files or source maps. No dependency version changes are needed.
The build does not deploy anything and API startup never invokes pnpm or migrations.

`pnpm serve` explicitly enables static mode, resolving BVA_WEB_BUILD_DIR from private
configuration (default apps/web/dist) to an absolute directory. A relative custom
directory resolves against the repository; an explicit absolute dedicated directory
is also supported. Preserve other configuration fields. API-only mode still works
without a build. Missing or unsafe output produces a setup failure recommending
`pnpm build`; it never silently starts an empty frontend.

The dedicated build root contains only index.html and a flat assets directory with
ordinary JS/CSS files. Static validation rejects hidden/source/extra files, symlinks,
Windows junctions, hard links and builds exceeding 32 MiB or 100 files. Startup reads
a fixed snapshot, checking opened file identity; HTTP requests perform exact lookups
without filesystem traversal. Only / and /assets filenames are served. Missing assets,
unknown /api routes and arbitrary future browser routes return JSON errors. Rebuild
and restart serving to publish a new snapshot; do not write secrets into a build.

## Browser acceptance and CI

    pnpm --filter @brickvault/web exec playwright install chromium
    pnpm test:e2e

The browser runner acquires the same exclusive lock as integration/database commands.
It uses only the ownership-verified test Compose project, a recorded disposable
database and an API on 127.0.0.1:18000. It reserves that socket before spawning the
actual serving process and keeps its process handle; it never attaches by matching
an HTTP response on an already occupied port. Chromium cannot start through the
bare Playwright config without the run-owned coordinator capability.

A temporary loopback test coordinator accepts authenticated stop/start/hold/release
commands from the Node test worker. Its per-run capability never enters the browser
application. A real PostgreSQL table lock coordinates loading; a real stopped test
service proves outage/recovery. Only the deliberate transport-failure case intercepts
browser requests. Tests cover desktop 1440×900, mobile 390×844, overflow, keyboard focus,
reload, local-only requests, JSON boundaries and sensitive-path probes. Screenshots
contain only the foundation shell and remain ignored under apps/web/test-results.

The runner stops its API/coordinator/browser processes, cleans exact recorded databases,
restores the test service's prior running state and preserves named volumes. Failure
and interruption paths retain a safe ledger under .local/database/runs; forceful OS
termination/power loss can still require manual inspection of that exact ledger.
Never recover resources by name prefix or kill a port occupant.

The separate manual check used installed Chrome 152.0.7977.76, with visual inspection
at both requested sizes, Tab focus, real not-ready communication and Retry recovery.
This is distinct from automated Playwright Chromium 153.0.8010.12.

[CI](../.github/workflows/ci.yml) runs on push/pull_request with contents: read and
immutable reviewed action commits. Ubuntu 24.04 runs frozen installs, all quality and
contract checks, real PostgreSQL integration, builds and Chromium with --with-deps.
Windows 2022 runs frozen installs, contracts, formatting/lint/typing/unit checks and
builds without Docker integration. No artifacts/private logs or caches are uploaded;
database cleanup runs after failures once initialization succeeded.

`python scripts/bootstrap_uv.py` supplies the same approved repository-local uv 0.12.10
on Windows/Linux x64 with fixed official archive SHA-256 verification. It preserves
an existing valid executable and changes no global tools. Local workflow validation
used official Actionlint 1.7.12 in ignored .local/tooling; pins and action input schemas
were checked against official tagged commits. A valid workflow is not a hosted run.

At the end of local work:

    pnpm db:stop

Stop the application terminals too. This preserves .env.local, ownership receipts,
named database volumes, unrelated Docker resources and Docker Desktop.

## Remaining boundaries

Phase 1 local Windows acceptance passed. Remote Ubuntu/Windows GitHub CI execution
is DEFERRED because nothing was pushed. Existing Ubuntu WSL discovery found Node
22.22.1 and no Python 3.13 executable; no Linux application checks, distribution/toolchain
installation or upgrades were performed. No Linux/macOS runtime, PWA/Android,
physical-device, authentication, provider-account or deployment acceptance is claimed.
Part-out values were added only to their later
[product plan](plans/005-set-part-out-values.md).

The previously rejected abandoned-cache cleanup remains untouched. Original Slice 1A
bootstrap incidents, acceptance details and immutable lock hashes are retained in
ExecPlan 000. No global uv, host PostgreSQL, home-server or production changes are part
of this work.

## Repository-local uv bootstrap

Use the existing approved runtimes. Missing prerequisites must be resolved within explicit task
authorization; do not install or update global tools. Start in the repository root.

The [official uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)
permits direct [release archives](https://github.com/astral-sh/uv/releases/tag/0.12.10). This session
used the Windows x64 MSVC archive, not an installer. No PATH/profile/registry changes were needed.

The following reproduces that bootstrap in PowerShell after .gitignore exists. It stops on an
unexpected existing download and verifies both published integrity sources before extraction:

```powershell
$ErrorActionPreference = 'Stop'
$repoRoot = (git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Run from the existing repository root' }
$repoRoot = [System.IO.Path]::GetFullPath($repoRoot)
if ((Get-Location).ProviderPath -ne $repoRoot) { throw 'Run bootstrap from the repository root' }
$manifest = Get-Content -LiteralPath (Join-Path $repoRoot 'package.json') -Raw | ConvertFrom-Json
if ($manifest.name -ne 'brickvault-appraisal-app') { throw 'Unexpected repository' }
git check-ignore .local/tooling/uv/0.12.10/uv.exe
if ($LASTEXITCODE -ne 0) { throw 'Local tools must be ignored first' }
$uvDirectory = Join-Path $repoRoot '.local/tooling/uv/0.12.10'
$localUv = Join-Path $uvDirectory 'uv.exe'
if (-not (Test-Path -LiteralPath $localUv)) {
  $release = Invoke-RestMethod 'https://api.github.com/repos/astral-sh/uv/releases/tags/0.12.10'
  if ($release.tag_name -ne '0.12.10' -or $release.prerelease -or $release.draft) {
    throw 'Unexpected uv release'
  }
  $asset = $release.assets | Where-Object name -eq 'uv-x86_64-pc-windows-msvc.zip'
  $checksum = $release.assets | Where-Object name -eq 'uv-x86_64-pc-windows-msvc.zip.sha256'
  if (-not $asset -or -not $checksum) { throw 'Expected release assets are missing' }
  $archive = Join-Path $uvDirectory $asset.name
  if (Test-Path -LiteralPath $archive) { throw 'Inspect existing archive before retrying' }
  New-Item -ItemType Directory -Path $uvDirectory -Force | Out-Null
  Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $archive
  $checksumFile = Join-Path $uvDirectory $checksum.name
  Invoke-WebRequest -Uri $checksum.browser_download_url -OutFile $checksumFile
  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash.ToLowerInvariant()
  $published = ((Get-Content -LiteralPath $checksumFile -Raw).Trim() -split '\s+')[0]
  if ($asset.digest -ne "sha256:$actual" -or $published -ne $actual) {
    throw 'uv archive integrity mismatch'
  }
  Expand-Archive -LiteralPath $archive -DestinationPath $uvDirectory
}
& $localUv --version
if ($LASTEXITCODE -ne 0) { throw 'uv executable verification failed' }
node scripts/tasks.mjs toolchain:check
if ($LASTEXITCODE -ne 0) { throw 'Local toolchain check failed' }
```

The downloaded archive SHA-256 was
`f65744f94072152b1f86ba2aace4d01f1124d9a8ecb235805039e3718c36cac2`, matching both GitHub's release-asset
digest and the official .sha256 asset. The extracted executable reported
`uv 0.12.10 (3c979abda 2026-09-04 x86_64-pc-windows-msvc)`.

On another supported platform, select and verify its official 0.12.10 archive and place the standalone
`uv` executable at .local/tooling/uv/0.12.10/uv. The runner resolves platform filenames without a shell;
actual Linux/macOS installation and execution were not tested in this session. Do not reuse the
Windows archive or claim cross-platform execution evidence from path tests.
