# Local development — Slice 1A

Slice 1A provides the workspace, locked dependencies, configuration initializer, and checked tooling.
There is no application to start yet. Slice 1B requires separate authorization for isolated database,
API, and contract work; Slice 1C adds the frontend and full acceptance. See [ExecPlan 000](plans/000-local-foundation.md)
and [workflow](../CODEX_WORKFLOW.md). The acceptance-review request authorizes one local checkpoint
only after all applicable checks pass; it authorizes no push or Slice 1B work.

## Verified prerequisites

Verified on Windows x64 during the 2026-09-05 Slice 1A session (UTC continued into September 6):

| Tool                 | Version          | Selection                                                     |
| -------------------- | ---------------- | ------------------------------------------------------------- |
| Git                  | 2.54.0.windows.1 | Existing installation                                         |
| Node.js              | 24.14.0          | Existing Node 24 LTS; pinned in .node-version                 |
| pnpm                 | 11.8.0           | Existing installation; pinned in packageManager               |
| Python               | 3.13.12          | Existing installation; pinned in services/api/.python-version |
| uv                   | 0.12.10          | Explicit repository-local executable                          |
| Docker CLI / Compose | 29.2.1 / 5.0.2   | Versions/context inspected only                               |

Global uv 0.10.7 remains unchanged, verified by version and matching SHA-256 before/after. No Python
runtime was downloaded. Node 24 and Python 3.13 family support was checked against official
[Node](https://nodejs.org/en/about/previous-releases) and [Python](https://devguide.python.org/versions/)
documentation; this is not a complete security certification of installed runtime patches.

Docker's desktop-linux context targets the local named pipe `npipe:////./pipe/dockerDesktopLinuxEngine`,
with no Docker host/context/TLS environment overrides. Its daemon was not contacted and its readiness
remains deferred. Ports 8000, 5173, 55432, 55433, and 18000 had no listeners during inspection; recheck
before any later authorized service work. Never connect to or modify existing PostgreSQL on 5432.

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

## Locked dependency setup

Run initial JavaScript installation from the repository root. Python commands select the installed
version pinned in services/api/.python-version (3.13.12), disable managed Python and downloads, and
version-check the explicit repository-local uv 0.12.10 executable. Never invoke bare global uv.

```powershell
python --version
node scripts/tasks.mjs toolchain:check
pnpm install --frozen-lockfile --strict-peer-dependencies
pnpm uv:sync
pnpm uv:check
pnpm uv:cache
```

Stop on a failing command; do not continue a setup sequence after an error. For a cached acceptance
run, append `--offline` to installation and each uv command; these exact offline commands passed.
If a locked artifact is unavailable, report that failure before using authorized official artifact
access. Initial lock creation is historical; these commands never update either lock.
Do not run broad updates. The root pnpm-lock.yaml and services/api/uv.lock are the only dependency
locks. A workspace link connects web and contracts, without advertising nonexistent generated exports.

The pnpm configuration enables strict peers, disables automatic peer installation, and enforces
engines. Only esbuild's declared dependency build is allowed; this is not application build evidence.
Its store/cache are under ignored .local. The uv runner uses its module URL to find the repository;
it supplies absolute --directory, --project, and --cache-dir arguments, pins UV_PROJECT_ENVIRONMENT
to services/api/.venv, and uses .local/tmp for TMP/TEMP/TMPDIR. It removes inherited UV_* overrides
and active-environment hints before passing those explicit settings. It does not load .env.local.
The pyproject no longer supplies a misleading cwd-relative cache default. Raw uv dependency commands
are unsupported; use these wrappers so cache, environment, and temporary paths stay identical.

From services/api the equivalent supported commands are:

```powershell
node ../../scripts/tasks.mjs uv:sync --offline
node ../../scripts/tasks.mjs uv:check --offline
node ../../scripts/tasks.mjs uv:cache --offline
```

uv tasks invoked from any other directory fail before creating files. Arguments other than the
optional --offline flag are rejected. uv:sync passes --locked --all-groups --no-install-project;
uv:check passes lock --check. Both use the pinned installed Python and the same path/environment
configuration as uv:cache. Child failures return nonzero with redacted output; inspect pinned runtime,
cache availability, and manifest/lock consistency privately, without copying raw errors into chat.

Hatchling remains the intended build backend. **Slice 1A tests dependency resolution and environment
synchronization only.** No application package is installed by --no-install-project. Once source
exists, Slice 1B must test actual application installation; later build/full acceptance must not retain
dependency-only installation as a substitute. Run installed Python tooling directly from
services/api/.venv rather than an implicit package-installing uv run.

## Exact direct dependencies

| JavaScript package                            | Version                           |
| --------------------------------------------- | --------------------------------- |
| TypeScript                                    | 5.9.3 in root, web, and contracts |
| ESLint / @eslint/js / typescript-eslint       | 10.10.0 / 10.0.1 / 8.69.0         |
| Prettier / @types/node                        | 3.9.6 / 24.13.3                   |
| React / React DOM                             | 19.2.8 / 19.2.8                   |
| @types/react / @types/react-dom               | 19.2.18 / 19.2.7                  |
| Vite / @vitejs/plugin-react                   | 8.2.2 / 6.1.1                     |
| openapi-typescript / openapi-fetch            | 7.13.0 / 0.17.0                   |
| Vitest / @playwright/test                     | 4.1.11 / 1.63.0                   |
| @testing-library/react / @testing-library/dom | 16.3.3 / 10.4.1                   |
| @testing-library/jest-dom / jsdom             | 6.9.1 / 29.1.1                    |

| Python package                         | Version                                        |
| -------------------------------------- | ---------------------------------------------- |
| FastAPI / Pydantic / pydantic-settings | 0.141.1 / 2.13.5 / 2.15.0                      |
| SQLAlchemy / Alembic                   | 2.0.52 / 1.19.2                                |
| Psycopg / psycopg-binary               | 3.3.5 / 3.3.5                                  |
| Uvicorn                                | 0.52.4                                         |
| Hatchling                              | 1.32.0, including the build-system requirement |
| Ruff / mypy                            | 0.16.6 / 1.20.2                                |
| pytest / HTTPX                         | 9.1.1 / 0.28.1                                 |

TypeScript 6 was superseded because openapi-typescript 7.13.0 requires ^5.x. ESLint 9 was superseded
because that family is EOL. See [D-023](DECISIONS.md#d-023--approved-slice-1a-tooling-corrections--2026-09-05).
Selected registry engines, peers, stable/nondeprecated status, Python requirements, and the Windows
CPython 3.13 Psycopg binary wheel were inspected before scaffolding. Strict installation then passed.
No overrides, package extensions, peer bypasses, prereleases, or second TypeScript compiler were used.

## Implemented commands

| Root command         | Actual Slice 1A behavior                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------ |
| pnpm dev:init        | Atomically create missing ignored local configuration, or validate/preserve existing bytes |
| pnpm toolchain:check | Check Node 24, exact explicit local uv, and private configuration Git guard                |
| pnpm uv:sync         | Synchronize locked Python dependencies and all groups without installing the application   |
| pnpm uv:check        | Check uv lock consistency without updating it                                              |
| pnpm uv:cache        | Report the effective absolute repository uv cache through the same runner                  |
| pnpm format:check    | Prettier check of new tooling/configuration and this setup document                        |
| pnpm lint            | ESLint 10 flat configuration over all authored .mjs tooling/configuration files            |
| pnpm typecheck       | Strict TypeScript checking of authored .mjs with checked JSDoc                             |
| pnpm test:unit       | Node tooling tests; no database or application package                                     |

The runner derives the root from its module URL, passes argument arrays without a shell, preserves
child failure exit codes, and never loads .env.local into child environments. Unknown/later commands
fail explicitly; db, application, contract, browser, and build commands are absent.

The root tsconfig.json exposes the tooling project to the supported typescript-eslint project service,
so typed linting reads supplied editor/stdin content. The initial explicit-project CLI optimization
read the disk file instead of the negative test's stdin text; project service corrected that behavior.
No lint rule, type check, or warning was suppressed. The test checks both the expected unused-variable
rule and CLI exit 1, rejecting parser errors as evidence.

The frontend/contracts tsconfigs establish later strict compiler settings but have no source inputs
yet. Ruff/mypy/pytest configuration is present in pyproject.toml. Their substantive Python checks,
React/contracts compilation, and app builds are deferred, not successful empty checks. Existing
historical Markdown is reviewed for links/consistency without broad automatic reformatting.

## Private configuration and tests

.env.example contains placeholders only. Run `pnpm dev:init` twice; the second invocation validates
and preserves the existing file byte-for-byte. Values are never printed. The initializer creates
separate random local bootstrap/owner/runtime credentials for future dev/test infrastructure, fixed
loopback settings and planned ports. Test database URLs describe the future isolated test base;
Slice 1B must implement uniquely named per-run databases and connection guards before using them.

Invalid/missing/duplicate/unknown settings are reported safely and never overwritten. Remote hosts,
5432, URL options, URL normalization (including hidden whitespace), frontend VITE_* configuration,
and unexpected paths are rejected. To repair an
invalid file, edit the named field privately using the documented local contract; do not paste values
into chat or silently regenerate credentials. Keep existing comments and valid log-level changes.

The file is written with restrictive POSIX mode where supported and published with an exclusive hard
link only after a complete flushed write. Existing files, including a competing initializer's output,
are never replaced. Windows inherited ACLs are not modified; cross-user ACL hardening was not tested.
The Git guard refuses tracked or unignored .env.local; Git itself also refuses a normal dry-run add.
An explicit forced Git add can bypass ignore rules, so never force-add private configuration.

Tests use ignored .local/tests disposable Git repositories and fake child-tool fixtures. uv path
regressions also run the installed uv offline against the real dependency-only environment from root
and services/api, including inherited destination overrides confined to ignored fixtures. They check
effective cache paths with the actual command arguments/environment, environment sys.prefix, spaces
in checkout paths, and rejection before writes from unsupported directories. No fixture
commit or staging is performed; the only add invocation is --dry-run against an ignored file. They
verify actual process status, unknown commands, path handling, configuration idempotency and invalid
data preservation, safe messages, Git refusal, local uv checks, and ESLint negative behavior.

## Validation evidence and limitations

Initial strict pnpm resolution installed 236 packages. Frozen installation passed. uv locked 41 records
including the root project and synchronized 40 dependencies without installing the application.
Corrected uv index configuration, locking, locked sync, and consistency checks completed without
configuration warnings. Installed ESLint 10.10.0, TypeScript 5.9.3 across the workspace, local uv
0.12.10, Python 3.13.12, Ruff 0.16.6, and mypy 1.20.2 were directly checked.

The first development pass identified and corrected an invalid uv index-setting key, a relative cache
path, unawaited test registration, and stdin typed-lint behavior. These initial failures are not
counted as passes. Final command results and lock hashes are recorded in the ExecPlan.

An initial invalid uv setting caused ordinary downloads to use the existing user uv cache. The first
valid cache setting also created a small cache at Downloads/.local/uv-cache before its path was
corrected. Automatic approval review rejected relocating/removing that temporary outside-repository
cache with "blocked by policy"; it remains untouched. The final configuration and repeated checks use
the ignored repository .local/uv-cache. Global uv executable/version and global configuration were
not changed. No cleanup of unrelated caches is authorized.

Only official runtime/framework documentation, npm/PyPI metadata/artifacts, and the official Astral uv
GitHub release/asset hosts were accessed. There were no provider/AI/remote database/home-server calls,
database connections, service/container starts, application source, migrations, Compose, CI, PWA,
Android, image, or deployment work. Browser binaries were not downloaded.

The acceptance review adds cache/environment path regressions and rejects normalized database URLs;
its durable commands/results and checkpoint inventory are in ExecPlan 000. Stop before Slice 1B;
completing this setup grants no permission
to start a database, application, or another phase.
