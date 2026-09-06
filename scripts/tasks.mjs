import { spawnSync } from 'node:child_process';
import { randomBytes, randomUUID } from 'node:crypto';
import {
  closeSync,
  existsSync,
  fsyncSync,
  linkSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join, resolve } from 'node:path';
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
    'uv:sync': ['sync', '--locked', '--all-groups', '--no-install-project'],
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
    if (values.get(key) !== expected)
      throw new SetupError(`Invalid ${key}: requires the approved local value.`);
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
  'packages/*/*.json',
  'docs/LOCAL_DEVELOPMENT.md',
];

/** Only real Slice 1A commands are dispatched. Later commands are absent.
 * @param {string[]} args
 * @param {string} [root]
 * @param {(message: string) => void} [log]
 */
export function dispatch(args, root = repositoryRoot(), log = console.log) {
  const [task] = args;
  if (task && ['uv:sync', 'uv:check', 'uv:cache'].includes(task)) {
    if (args.length !== 1 && !(args.length === 2 && args[1] === '--offline')) {
      throw new SetupError('uv tasks accept only the optional --offline flag.');
    }
    return runUv(task, root, args[1] === '--offline', log);
  }
  if (args.length !== 1) throw new SetupError('Expected one Slice 1A task name. See package.json.');
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
      return runChild(
        process.execPath,
        [join(root, 'node_modules/prettier/bin/prettier.cjs'), '--check', ...formatInputs],
        root,
      );
    case 'lint':
      return runChild(
        process.execPath,
        [
          join(root, 'node_modules/eslint/bin/eslint.js'),
          '--max-warnings',
          '0',
          'scripts/**/*.mjs',
          '*.config.mjs',
        ],
        root,
      );
    case 'typecheck':
      return runChild(
        process.execPath,
        [join(root, 'node_modules/typescript/bin/tsc'), '--project', 'tsconfig.tools.json'],
        root,
      );
    case 'test:unit':
      return runChild(process.execPath, ['--test', join(root, 'scripts/tasks.test.mjs')], root);
    default:
      throw new SetupError(
        'Unknown or unavailable Slice 1A task. See package.json; later slices are not implemented.',
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
