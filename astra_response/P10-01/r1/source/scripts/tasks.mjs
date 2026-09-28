import { spawnSync } from 'node:child_process';
import { randomBytes, randomUUID } from 'node:crypto';
import {
  closeSync,
  existsSync,
  fsyncSync,
  linkSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  openSync,
  readFileSync,
  readdirSync,
  realpathSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export const UV_VERSION = '0.12.10';

/** @param {string} [moduleUrl] */
export function repositoryRoot(moduleUrl = import.meta.url) {
  return resolve(dirname(fileURLToPath(moduleUrl)), '..');
}

export class SetupError extends Error {}

/** @param {unknown} error @param {string} code */
function hasCode(error, code) {
  return error instanceof Error && 'code' in error && error.code === code;
}

/**
 * Run argument arrays directly, without a shell or dotenv loading.
 * @param {string} executable
 * @param {string[]} args
 * @param {string} root
 * @param {'inherit' | 'pipe'} [stdio]
 */
export function runChild(executable, args, root, stdio = 'inherit') {
  const child = spawnSync(executable, args, { cwd: root, stdio, windowsHide: true });
  if (child.error) throw new SetupError('Unable to start the required tool. Check local setup.');
  return child.status ?? 1;
}

/** @param {string} root @param {NodeJS.Platform} [platform] */
export function localUvPath(root, platform = process.platform) {
  return join(root, '.local', 'tooling', 'uv', UV_VERSION, platform === 'win32' ? 'uv.exe' : 'uv');
}

/** @param {string} root */
export function requireLocalUv(root) {
  const executable = localUvPath(root);
  const message =
    'Install repository-local uv 0.12.10 using docs/LOCAL_DEVELOPMENT.md; global uv is not used.';
  if (!existsSync(executable)) throw new SetupError(message);
  const result = spawnSync(executable, ['--version'], {
    cwd: root,
    encoding: 'utf8',
    windowsHide: true,
  });
  if (result.error || result.status !== 0 || !/^uv 0\.12\.10(?:\s|$)/u.test(result.stdout)) {
    throw new SetupError(message);
  }
  return executable;
}

/** Build the same absolute paths and environment for every supported uv command.
 * @param {string} task
 * @param {string} root
 * @param {boolean} offline
 * @param {string} [cwd]
 * @param {NodeJS.ProcessEnv} [environment]
 */
export function uvInvocation(task, root, offline, cwd = process.cwd(), environment = process.env) {
  root = resolve(root);
  const project = join(root, 'services/api');
  if (![root, project].includes(resolve(cwd))) {
    throw new SetupError('Run uv tasks from the repository root or services/api.');
  }
  /** @type {Record<string, string[]>} */
  const commands = {
    'uv:sync': ['sync', '--locked', '--all-groups'],
    'uv:check': ['lock', '--check'],
    'uv:cache': ['cache', 'dir'],
  };
  const command = commands[task];
  if (!command) throw new SetupError('Unknown Slice 1A uv task.');
  const executable = requireLocalUv(root);
  const python = readFileSync(join(project, '.python-version'), 'utf8').trim();
  if (!/^3\.13\.\d+$/u.test(python)) throw new SetupError('Expected a pinned Python 3.13 version.');
  // Do not inherit uv destination/index/config overrides or an activated environment.
  const env = Object.fromEntries(
    Object.entries(environment).filter(
      ([key]) => !/^(?:UV_|VIRTUAL_ENV$|CONDA_PREFIX$|TMP$|TEMP$|TMPDIR$)/iu.test(key),
    ),
  );
  const temporary = join(root, '.local/tmp');
  Object.assign(env, {
    UV_PROJECT_ENVIRONMENT: join(project, '.venv'),
    TMP: temporary,
    TEMP: temporary,
    TMPDIR: temporary,
  });
  return {
    executable,
    args: [
      ...command,
      '--directory',
      root,
      '--project',
      project,
      '--cache-dir',
      join(root, '.local/uv-cache'),
      '--no-python-downloads',
      '--no-managed-python',
      ...(task === 'uv:cache' ? [] : ['--python', python]),
      ...(offline ? ['--offline'] : []),
    ],
    options: { cwd: root, env, encoding: /** @type {const} */ ('utf8'), windowsHide: true },
    temporary,
  };
}

/** @param {string} task @param {string} root @param {boolean} offline
 * @param {(message: string) => void} log
 */
function runUv(task, root, offline, log) {
  const invocation = uvInvocation(task, root, offline);
  requirePrivateConfig(root);
  const ignored = spawnSync('git', ['check-ignore', '--quiet', '--', '.local/tmp/probe'], {
    cwd: root,
    windowsHide: true,
    stdio: 'pipe',
  });
  if (ignored.error || ignored.status !== 0) throw new SetupError('Local tooling must be ignored.');
  mkdirSync(invocation.temporary, { recursive: true });
  const result = spawnSync(invocation.executable, invocation.args, invocation.options);
  if (result.error) throw new SetupError('Unable to start repository-local uv.');
  const status = result.status ?? 1;
  if (status !== 0)
    log(`${task} failed (exit ${status}); tool output redacted. Check local setup.`);
  else log(task === 'uv:cache' ? result.stdout.trim() : `${task} completed successfully.`);
  return status;
}

/** Refuse tracked/unignored private configuration before reading or generating it.
 * @param {string} root
 */
export function requirePrivateConfig(root) {
  const options = { cwd: root, encoding: /** @type {const} */ ('utf8'), windowsHide: true };
  const tracked = spawnSync('git', ['ls-files', '--error-unmatch', '--', '.env.local'], options);
  if (tracked.error || tracked.status !== 1) {
    throw new SetupError(
      'Local configuration must be untracked; inspect the Git index before continuing.',
    );
  }
  const ignored = spawnSync('git', ['check-ignore', '--quiet', '--', '.env.local'], options);
  if (ignored.error || ignored.status !== 0) {
    throw new SetupError('Local configuration must be ignored by Git before initialization.');
  }
}

/** Verify ignored local storage and its effective ancestry before any new writes.
 * @param {string} root @param {string} directory
 */
export function requireLocalStorage(root, directory) {
  const local = resolve(root, '.local');
  if (directory !== local && !resolve(directory).startsWith(local + sep)) {
    throw new SetupError('Temporary storage must remain inside repository .local.');
  }
  const ignored = spawnSync('git', ['check-ignore', '--quiet', '--', '.local/probe'], {
    cwd: root,
    stdio: 'pipe',
    windowsHide: true,
  });
  if (ignored.status !== 0) throw new SetupError('Repository local storage must be ignored.');
  let ancestor = resolve(directory);
  while (!existsSync(ancestor)) ancestor = dirname(ancestor);
  const realRoot = realpathSync(root);
  const realAncestor = realpathSync(ancestor);
  if (realAncestor !== realRoot && !realAncestor.startsWith(realRoot + sep)) {
    throw new SetupError('Repository local storage must not redirect outside the checkout.');
  }
}

const fixedValues = {
  BVA_MODE: 'development',
  BVA_BIND_HOST: '127.0.0.1',
  BVA_API_PORT: '8000',
  BVA_WEB_PORT: '5173',
  BVA_TEST_API_PORT: '18000',
  BVA_STATIC_ENABLED: 'false',
  BVA_WEB_BUILD_DIR: 'apps/web/dist',
};

const passwordKeys = ['BVA_DEV_BOOTSTRAP_PASSWORD', 'BVA_TEST_BOOTSTRAP_PASSWORD'];
const urlSpecs = {
  BVA_DEV_OWNER_DATABASE_URL: ['brickvault_dev_owner', '55432', 'brickvault_dev'],
  BVA_DEV_RUNTIME_DATABASE_URL: ['brickvault_dev_runtime', '55432', 'brickvault_dev'],
  BVA_TEST_OWNER_DATABASE_URL: ['brickvault_test_owner', '55433', 'brickvault_test'],
  BVA_TEST_RUNTIME_DATABASE_URL: ['brickvault_test_runtime', '55433', 'brickvault_test'],
};
const allowedKeys = new Set([
  ...Object.keys(fixedValues),
  'BVA_LOG_LEVEL',
  ...passwordKeys,
  ...Object.keys(urlSpecs),
]);
const passwordPattern = /^[a-f0-9]{64}$/u;

/** Strict, deliberately non-shell .env syntax; errors never contain input values.
 * @param {string} text
 */
export function validateConfig(text) {
  /** @type {Map<string, string>} */
  const values = new Map();
  for (const [index, line] of text.split(/\r?\n/u).entries()) {
    if (line.trim() === '' || line.trimStart().startsWith('#')) continue;
    const match = /^([A-Z][A-Z0-9_]*)=([^\r\n]*)$/u.exec(line);
    const key = match?.[1];
    const value = match?.[2];
    if (!key || value === undefined || !allowedKeys.has(key) || values.has(key)) {
      throw new SetupError(
        `Invalid local configuration syntax, unknown or duplicate field at line ${index + 1}.`,
      );
    }
    values.set(key, value);
  }
  for (const key of allowedKeys) {
    if (!values.has(key)) throw new SetupError(`Missing local configuration field: ${key}.`);
  }
  for (const [key, expected] of Object.entries(fixedValues)) {
    if (key === 'BVA_WEB_BUILD_DIR') continue; // Validated when explicit static serving loads the build.
    if (values.get(key) !== expected)
      throw new SetupError(`Invalid ${key}: requires the approved local value.`);
  }
  const buildDirectory = values.get('BVA_WEB_BUILD_DIR') ?? '';
  if (
    !buildDirectory.trim() ||
    [...buildDirectory].some((character) => character.charCodeAt(0) < 32)
  ) {
    throw new SetupError('Invalid BVA_WEB_BUILD_DIR: expected a dedicated build directory.');
  }
  if (!['DEBUG', 'INFO', 'WARNING', 'ERROR'].includes(values.get('BVA_LOG_LEVEL') ?? '')) {
    throw new SetupError('Invalid BVA_LOG_LEVEL: unsupported log level.');
  }
  for (const key of passwordKeys) {
    if (!passwordPattern.test(values.get(key) ?? ''))
      throw new SetupError(`Invalid ${key}: expected a generated local password.`);
  }
  for (const [key, [username, port, database]] of Object.entries(urlSpecs)) {
    let url;
    try {
      url = new URL(values.get(key) ?? '');
    } catch {
      throw new SetupError(`Invalid ${key}: malformed local database URL.`);
    }
    if (
      url.href !== values.get(key) ||
      url.protocol !== 'postgresql+psycopg:' ||
      url.hostname !== '127.0.0.1' ||
      url.port !== port ||
      url.username !== username ||
      url.pathname !== `/${database}` ||
      url.search ||
      url.hash ||
      !passwordPattern.test(url.password)
    ) {
      throw new SetupError(
        `Invalid ${key}: requires the approved loopback database, port, role and local password.`,
      );
    }
  }
}

function newConfig() {
  /** @type {Record<string, string>} */
  const values = { ...fixedValues, BVA_LOG_LEVEL: 'INFO' };
  for (const key of passwordKeys) values[key] = randomBytes(32).toString('hex');
  for (const [key, [username, port, database]] of Object.entries(urlSpecs)) {
    values[key] =
      `postgresql+psycopg://${username}:${randomBytes(32).toString('hex')}@127.0.0.1:${port}/${database}`;
  }
  return (
    '# Private local development only. Never commit or share this file.\n' +
    Object.entries(values)
      .map(([key, value]) => `${key}=${value}\n`)
      .join('')
  );
}

/** @param {string} filename */
function readExistingConfig(filename) {
  const info = lstatSync(filename);
  if (!info.isFile() || info.isSymbolicLink())
    throw new SetupError('Local configuration must be an ordinary file.');
  if (info.size > 16384) throw new SetupError('Local configuration exceeds the supported size.');
  validateConfig(readFileSync(filename, 'utf8'));
}

/** Publish a complete file exclusively; a competing initializer never overwrites it.
 * @param {string} root
 * @returns {'created' | 'preserved'}
 */
export function initializeConfig(root) {
  requirePrivateConfig(root);
  const filename = join(root, '.env.local');
  try {
    readExistingConfig(filename);
    return 'preserved';
  } catch (error) {
    if (!hasCode(error, 'ENOENT')) throw error;
  }
  const content = newConfig();
  validateConfig(content);
  const temporary = join(root, `.env.local.${randomUUID()}.tmp`);
  const descriptor = openSync(temporary, 'wx', 0o600);
  try {
    try {
      writeFileSync(descriptor, content, 'utf8');
      fsyncSync(descriptor);
    } finally {
      closeSync(descriptor);
    }
    try {
      linkSync(temporary, filename);
      return 'created';
    } catch (error) {
      if (!hasCode(error, 'EEXIST')) throw error;
      readExistingConfig(filename);
      return 'preserved';
    }
  } finally {
    unlinkSync(temporary);
  }
}

const formatInputs = [
  'package.json',
  'pnpm-workspace.yaml',
  'tsconfig*.json',
  '*.config.mjs',
  'scripts/**/*.mjs',
  'apps/*/*.json',
  'apps/web/**/*.{ts,tsx,css,html}',
  '.github/workflows/*.yml',
  'packages/*/*.json',
  'packages/contracts/src/index.ts',
  'infra/*.yml',
  'docs/LOCAL_DEVELOPMENT.md',
];

/** @param {string} root */
export function pythonPath(root) {
  return join(
    root,
    'services/api/.venv',
    process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python',
  );
}

/** Keep Python caches/temp artifacts inside the repository without uv or dotenv loading.
 * @param {string} root
 */
export function pythonEnvironment(root) {
  const temporary = join(root, '.local/tmp');
  requireLocalStorage(root, temporary);
  mkdirSync(temporary, { recursive: true });
  return {
    ...Object.fromEntries(
      Object.entries(process.env).filter(
        ([key]) => !/^(?:PYTHON|VIRTUAL_ENV$|CONDA_PREFIX$|TMP$|TEMP$|TMPDIR$)/iu.test(key),
      ),
    ),
    PYTHONNOUSERSITE: '1',
    PYTHONUTF8: '1',
    TMP: temporary,
    TEMP: temporary,
    TMPDIR: temporary,
    MYPY_CACHE_DIR: join(root, '.local/mypy-cache'),
    RUFF_CACHE_DIR: join(root, '.local/ruff-cache'),
  };
}

/** @param {string} root @param {string[]} args */
function runPython(root, args) {
  const child = spawnSync(pythonPath(root), args, {
    cwd: root,
    env: pythonEnvironment(root),
    stdio: 'inherit',
    windowsHide: true,
  });
  if (child.error) throw new SetupError('Python project environment unavailable; run uv:sync.');
  return child.status ?? 1;
}

/** @param {string} root @param {boolean} check @param {string} [expectedDirectory] */
export function contractsTask(root, check, expectedDirectory = join(root, 'packages/contracts')) {
  if (
    ![root, join(root, 'services/api'), join(root, 'packages/contracts')].includes(
      resolve(process.cwd()),
    )
  ) {
    throw new SetupError('Run contract tasks from root, services/api, or packages/contracts.');
  }
  requirePrivateConfig(root);
  const temporaryRoot = join(root, '.local/contracts');
  requireLocalStorage(root, temporaryRoot);
  mkdirSync(temporaryRoot, { recursive: true });
  const temporary = mkdtempSync(join(temporaryRoot, 'generate-'));
  const openapi = join(temporary, 'openapi.json');
  const schema = join(temporary, 'schema.d.ts');
  const env = Object.fromEntries(
    Object.entries(pythonEnvironment(root)).filter(([key]) => !/^(?:BVA_|PG)/iu.test(key)),
  );
  const exported = spawnSync(pythonPath(root), ['-m', 'brickvault_api.contracts'], {
    cwd: root,
    env,
    encoding: 'utf8',
    windowsHide: true,
  });
  if (exported.error || exported.status !== 0)
    throw new SetupError('Schema export failed; diagnostics redacted.');
  writeFileSync(openapi, exported.stdout, 'utf8');
  const generated = spawnSync(
    process.execPath,
    [
      join(root, 'packages/contracts/node_modules/openapi-typescript/bin/cli.js'),
      openapi,
      '--output',
      schema,
    ],
    { cwd: root, env, stdio: 'pipe', windowsHide: true },
  );
  const result = generated.status ?? 1;
  if (result !== 0) return result;
  /** @type {[string, string][]} */
  const outputs = [
    [openapi, join(expectedDirectory, 'openapi.json')],
    [schema, join(expectedDirectory, 'src/schema.d.ts')],
  ];
  for (const [generated, expected] of outputs) {
    const bytes = readFileSync(generated);
    if (check) {
      if (!existsSync(expected) || !readFileSync(expected).equals(bytes)) return 1;
    } else {
      mkdirSync(dirname(expected), { recursive: true });
      writeFileSync(expected, bytes);
    }
  }
  return 0;
}

/** Only minimal OS/runtime settings reach frontend processes. No dotenv or secrets.
 * @param {NodeJS.ProcessEnv} [environment]
 */
export function frontendEnvironment(environment = process.env) {
  return Object.fromEntries(
    Object.entries(environment).filter(([key]) =>
      /^(?:PATH|PATHEXT|SYSTEMROOT|WINDIR|COMSPEC|TEMP|TMP|TMPDIR|HOME|USERPROFILE|LOCALAPPDATA|APPDATA|CI|TERM|NO_COLOR|FORCE_COLOR)$/iu.test(
        key,
      ),
    ),
  );
}

/** @param {string} root @param {'dev' | 'build' | 'unit'} task */
function webTask(root, task) {
  const web = join(root, 'apps/web');
  // Vite empties only its normal build output; reject redirected output first.
  for (const directory of [web, join(web, 'dist')]) {
    if (
      existsSync(directory) &&
      (lstatSync(directory).isSymbolicLink() ||
        !realpathSync(directory).startsWith(realpathSync(root) + sep))
    ) {
      throw new SetupError('Frontend paths must remain inside the repository.');
    }
  }
  const child = spawnSync(
    process.execPath,
    [
      join(
        web,
        task === 'unit' ? 'node_modules/vitest/vitest.mjs' : 'node_modules/vite/bin/vite.js',
      ),
      ...(task === 'unit' ? ['run'] : task === 'build' ? ['build'] : []),
    ],
    { cwd: web, env: frontendEnvironment(), stdio: 'inherit', windowsHide: true },
  );
  if (child.error) throw new SetupError('Frontend tool unavailable; run the frozen pnpm install.');
  return child.status ?? 1;
}

/** Verify every published byte against actual private values and a build sentinel.
 * @param {string} root @param {string} [directory]
 */
export function verifyFrontend(root, directory = join(root, 'apps/web/dist')) {
  initializeConfig(root);
  const pwa = ['icon-192.png', 'icon-512.png', 'manifest.webmanifest', 'sw.js'];
  if (!lstatSync(directory).isDirectory())
    throw new SetupError('Frontend build contains an unsafe directory.');
  const entryNames = readdirSync(directory).sort();
  const entries = entryNames.join(',');
  if (!['assets,index.html', ['assets', 'index.html', ...pwa].sort().join(',')].includes(entries)) {
    throw new SetupError('Frontend build contains unexpected public files.');
  }
  const assetDirectory = join(directory, 'assets');
  if (!lstatSync(assetDirectory).isDirectory())
    throw new SetupError('Frontend build contains an unsafe directory.');
  const assets = readdirSync(assetDirectory);
  if (assets.some((name) => !/^[A-Za-z0-9_-]+\.(?:js|css)$/u.test(name)))
    throw new SetupError('Frontend build contains an unsupported asset name.');
  const outputs = [
    join(directory, 'index.html'),
    ...pwa.filter((name) => entryNames.includes(name)).map((name) => join(directory, name)),
    ...assets.map((name) => join(assetDirectory, name)),
  ];
  const realDirectory = realpathSync(directory);
  for (const filename of outputs) {
    const info = lstatSync(filename);
    if (
      !info.isFile() ||
      info.nlink !== 1 ||
      !realpathSync(filename).startsWith(realDirectory + sep)
    )
      throw new SetupError('Frontend output contains an unsafe path.');
  }
  const privateValues =
    readFileSync(join(root, '.env.local'), 'utf8').match(/[a-f0-9]{64}/gu) ?? [];
  const forbidden = [
    ...privateValues,
    'BVA_BUILD_CREDENTIAL_SENTINEL_1C',
    'postgresql+psycopg://',
    'BVA_DEV_RUNTIME_DATABASE_URL',
  ];
  if (outputs.length < 3 || !readFileSync(outputs[0] ?? '', 'utf8').includes('/assets/'))
    throw new SetupError('Frontend build output is incomplete.');
  for (const filename of outputs) {
    const bytes = readFileSync(filename);
    if (forbidden.some((value) => bytes.includes(value)) || filename.endsWith('.map'))
      throw new SetupError('Frontend output contains private configuration or source maps.');
  }
}

/** Dispatch the complete Phase 1 root command contract.
 * @param {string[]} args
 * @param {string} [root]
 * @param {(message: string) => void} [log]
 */
export function dispatch(args, root = repositoryRoot(), log = console.log) {
  const [task] = args;
  if (task === 'catalog:smoke') {
    if (![root, join(root, 'services/api')].includes(resolve(process.cwd())))
      throw new SetupError('Run catalog tasks from root or services/api.');
    const rest = args[1] === '--' ? args.slice(2) : args.slice(1);
    return runPython(root, [join(root, 'scripts/catalog_smoke.py'), ...rest]);
  }
  if (task === 'catalog:download') {
    if (args.length !== 1 || ![root, join(root, 'services/api')].includes(resolve(process.cwd())))
      throw new SetupError('Run catalog:download without arguments from root or services/api.');
    return runPython(root, [join(root, 'scripts/download_catalog.py')]);
  }
  if (
    task &&
    ['catalog:import', 'catalog:activate', 'catalog:status', 'catalog:validate'].includes(task)
  ) {
    if (![root, join(root, 'services/api')].includes(resolve(process.cwd())))
      throw new SetupError('Run catalog tasks from root or services/api.');
    const rest = args[1] === '--' ? args.slice(2) : args.slice(1);
    return runPython(root, [join(root, 'scripts/catalog.py'), task, ...rest]);
  }
  if (task && ['uv:sync', 'uv:check', 'uv:cache'].includes(task)) {
    if (args.length !== 1 && !(args.length === 2 && args[1] === '--offline')) {
      throw new SetupError('uv tasks accept only the optional --offline flag.');
    }
    return runUv(task, root, args[1] === '--offline', log);
  }
  if (args.length !== 1)
    throw new SetupError('Expected one foundation task name. See package.json.');
  switch (task) {
    case 'dev:init':
      log(`Local configuration ${initializeConfig(root)}; values redacted.`);
      return 0;
    case 'toolchain:check': {
      if (!process.versions.node.startsWith('24.')) throw new SetupError('Node.js 24 is required.');
      const uv = requireLocalUv(root);
      requirePrivateConfig(root);
      return runChild(uv, ['--version'], root);
    }
    case 'format:check':
      return (
        runChild(
          process.execPath,
          [join(root, 'node_modules/prettier/bin/prettier.cjs'), '--check', ...formatInputs],
          root,
        ) ||
        runPython(root, [
          '-m',
          'ruff',
          'format',
          '--check',
          'services/api/src',
          'services/api/tests',
          'scripts',
        ])
      );
    case 'lint':
      return (
        runChild(
          process.execPath,
          [
            join(root, 'node_modules/eslint/bin/eslint.js'),
            '--max-warnings',
            '0',
            'scripts/**/*.mjs',
            '*.config.mjs',
            'apps/web/**/*.ts',
            'apps/web/**/*.tsx',
          ],
          root,
        ) ||
        runPython(root, [
          '-m',
          'ruff',
          'check',
          '--config',
          'services/api/pyproject.toml',
          'services/api/src',
          'services/api/tests',
          'scripts',
        ])
      );
    case 'typecheck':
      return (
        runChild(
          process.execPath,
          [join(root, 'node_modules/typescript/bin/tsc'), '--project', 'apps/web/tsconfig.json'],
          root,
        ) ||
        runChild(
          process.execPath,
          [join(root, 'node_modules/typescript/bin/tsc'), '--project', 'tsconfig.tools.json'],
          root,
        ) ||
        runChild(
          process.execPath,
          [
            join(root, 'node_modules/typescript/bin/tsc'),
            '--project',
            'packages/contracts/tsconfig.json',
          ],
          root,
        ) ||
        runPython(root, [
          '-m',
          'mypy',
          '--config-file',
          'services/api/pyproject.toml',
          'services/api/src',
          'services/api/tests',
          'scripts',
        ])
      );
    case 'test:unit':
      return (
        webTask(root, 'unit') ||
        runChild(
          process.execPath,
          [
            '--test',
            join(root, 'scripts/tasks.test.mjs'),
            join(root, 'scripts/frontend_artifact.test.mjs'),
          ],
          root,
        ) ||
        runPython(root, [
          '-m',
          'pytest',
          '-c',
          'services/api/pyproject.toml',
          'services/api/tests/unit',
          'scripts/test_database.py',
          'scripts/test_auth_admin.py',
        ])
      );
    case 'db:up':
    case 'db:migrate':
    case 'db:status':
    case 'db:stop':
    case 'test:integration':
      if (![root, join(root, 'services/api')].includes(resolve(process.cwd())))
        throw new SetupError('Run database tasks from root or services/api.');
      return runPython(root, [join(root, 'scripts/database.py'), task]);
    case 'dev:api':
      return runPython(root, [join(root, 'scripts/serve_api.py')]);
    case 'auth:bootstrap':
    case 'auth:reset':
      return runPython(root, [
        join(root, 'scripts/auth_admin.py'),
        task === 'auth:bootstrap' ? 'bootstrap' : 'reset',
      ]);
    case 'dev:web':
      return webTask(root, 'dev');
    case 'serve':
      return runPython(root, [join(root, 'scripts/serve_api.py'), '--static']);
    case 'test:e2e':
      return runPython(root, [join(root, 'scripts/browser_runner.py')]);
    case 'build': {
      const status =
        runPython(root, [join(root, 'scripts/package_api.py')]) || webTask(root, 'build');
      if (status) return status;
      verifyFrontend(root);
      log('API package and frontend build verified; no private configuration in browser output.');
      return 0;
    }
    case 'contracts:generate':
    case 'contracts:check': {
      const status = contractsTask(root, task === 'contracts:check');
      log(
        status === 0
          ? `${task} passed.`
          : `${task} failed: generated contract drift or generator failure.`,
      );
      return status;
    }
    case 'build:api':
      return runPython(root, [join(root, 'scripts/package_api.py')]);
    default:
      throw new SetupError(
        'Unknown or unavailable foundation task. See package.json; later slices are not implemented.',
      );
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    process.exitCode = dispatch(process.argv.slice(2));
  } catch (error) {
    console.error(
      error instanceof SetupError
        ? error.message
        : 'Tooling failed; local values and error details are redacted.',
    );
    process.exitCode = 1;
  }
}
