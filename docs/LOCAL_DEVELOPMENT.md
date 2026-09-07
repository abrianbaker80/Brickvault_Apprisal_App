# Local development — Phase 1 foundation

Slice 1A is accepted at 150caf77820d09c60d028eeeba5b1b4317e11539. Slice 1B supplies
isolated PostgreSQL, API-only serving, migrations and generated contracts. See
[ExecPlan 000](plans/000-local-foundation.md) for actual acceptance evidence and
[workflow](../CODEX_WORKFLOW.md) for authorization. Slice 1C frontend/static/browser/CI
work remains unstarted.

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
There is no frontend build, static serving, Swagger, ReDoc or permissive CORS.

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
and contracts. Acceptance checks comprise 19 Node tests, 55 Python unit tests and
28 real PostgreSQL integration tests. Both visible warnings originate in transitive
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
services/api/dist and .local/package-check. Aggregate frontend build remains Slice 1C.

## Remaining boundaries

This is Windows/backend acceptance only. No frontend/static/browser/CI, Linux/macOS
execution, PWA/Android, physical-device, authentication, provider-account or deployment
acceptance is claimed. Part-out values were added only to their later
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
