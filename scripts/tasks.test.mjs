import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { join, resolve, sep } from 'node:path';
import { test } from 'node:test';
import { pathToFileURL } from 'node:url';
import { ESLint } from 'eslint';
import {
  dispatch,
  initializeConfig,
  localUvPath,
  repositoryRoot,
  requireLocalUv,
  runChild,
  SetupError,
  uvInvocation,
  validateConfig,
} from './tasks.mjs';

const root = repositoryRoot();
const scratch = join(root, '.local', 'tests');
mkdirSync(scratch, { recursive: true });

/** @param {import('node:test').TestContext} t */
function fixture(t) {
  const directory = mkdtempSync(join(scratch, 'tooling spaces '));
  t.after(() => {
    assert.ok(resolve(directory).startsWith(resolve(scratch) + sep));
    rmSync(directory, { recursive: true, force: true });
  });
  const git = spawnSync('git', ['init', '--quiet', directory], {
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.equal(git.status, 0);
  writeFileSync(join(directory, '.gitignore'), '.env\n.env.*\n!.env.example\n.local/\n');
  return directory;
}

/** @param {string} directory @param {string[]} args */
function cli(directory, args) {
  return spawnSync(process.execPath, [join(root, 'scripts/tasks.mjs'), ...args], {
    cwd: directory,
    encoding: 'utf8',
    windowsHide: true,
  });
}

await test('module paths resolve independently of cwd, spaces and URL escaping', () => {
  const pretendRoot = join(root, '.local', 'space # percent %');
  assert.equal(
    repositoryRoot(pathToFileURL(join(pretendRoot, 'scripts/tasks.mjs')).href),
    pretendRoot,
  );
  assert.equal(
    localUvPath(pretendRoot, 'win32'),
    join(pretendRoot, '.local/tooling/uv/0.12.10/uv.exe'),
  );
  assert.equal(
    localUvPath(pretendRoot, 'linux'),
    join(pretendRoot, '.local/tooling/uv/0.12.10/uv'),
  );
});

await test('unknown, missing, later and excess task arguments fail without echoing input', () => {
  for (const args of [[], ['db:up'], ['secret-sentinel'], ['lint', 'secret-sentinel']]) {
    assert.throws(() => dispatch(args), SetupError);
    const result = cli(join(root, 'apps/web'), args);
    assert.equal(result.status, 1);
    assert.doesNotMatch(result.stderr + result.stdout, /secret-sentinel/u);
  }
});

await test('runner preserves actual child exit codes and arguments containing shell characters', (t) => {
  const directory = fixture(t);
  const argument = 'a space & literal $() `quote`';
  assert.equal(
    runChild(
      process.execPath,
      [
        '-e',
        'process.exit(process.argv[1] === "a space & literal $() `quote`" ? 23 : 24)',
        argument,
      ],
      directory,
      'pipe',
    ),
    23,
  );
  assert.equal(runChild(process.execPath, ['-e', 'process.exit(0)'], directory, 'pipe'), 0);
  assert.throws(
    () => runChild(join(directory, 'absent-program'), [], directory, 'pipe'),
    /Unable to start/u,
  );
});

await test('dispatch propagates failure from the selected child tool', (t) => {
  const directory = fixture(t);
  const bin = join(directory, 'node_modules/typescript/bin');
  mkdirSync(bin, { recursive: true });
  writeFileSync(join(bin, 'tsc'), 'process.exit(27);\n');
  assert.equal(dispatch(['typecheck'], directory), 27);
});

await test('initializer creates valid private configuration, preserves bytes and redacts logs', (t) => {
  const directory = fixture(t);
  /** @type {string[]} */
  const messages = [];
  assert.equal(
    dispatch(['dev:init'], directory, (message) => messages.push(message)),
    0,
  );
  const filename = join(directory, '.env.local');
  const before = readFileSync(filename);
  validateConfig(before.toString('utf8'));
  assert.equal(
    dispatch(['dev:init'], directory, (message) => messages.push(message)),
    0,
  );
  assert.deepEqual(readFileSync(filename), before);
  assert.match(messages.join('\n'), /created.*redacted[\s\S]*preserved.*redacted/u);
  assert.doesNotMatch(messages.join('\n'), /[a-f0-9]{64}|postgresql|PASSWORD=/u);
  assert.deepEqual(
    readdirSync(directory).filter((name) => name.startsWith('.env.')),
    ['.env.local'],
  );
});

await test('valid existing custom values and CRLF comments survive byte-for-byte', (t) => {
  const directory = fixture(t);
  initializeConfig(directory);
  const filename = join(directory, '.env.local');
  const customized = (
    readFileSync(filename, 'utf8').replace('BVA_LOG_LEVEL=INFO', 'BVA_LOG_LEVEL=DEBUG') +
    '# retained comment\n'
  ).replaceAll('\n', '\r\n');
  writeFileSync(filename, customized);
  assert.equal(initializeConfig(directory), 'preserved');
  assert.deepEqual(readFileSync(filename), Buffer.from(customized));
});

await test('invalid existing local values fail safely and never regenerate', (t) => {
  const directory = fixture(t);
  initializeConfig(directory);
  const filename = join(directory, '.env.local');
  const valid = readFileSync(filename, 'utf8');
  const invalidCases = [
    valid.replace('BVA_API_PORT=8000', 'BVA_API_PORT=secret-sentinel'),
    valid.replace('@127.0.0.1:55432', '@remote.invalid:55432'),
    valid.replace(':55432/', ':5432/'),
    valid.replace('/brickvault_dev\n', '/brickvault_dev \n'),
    valid.replace('@127.0.0.1:55432', '@127.0.0.\t1:55432'),
    valid.replace('/brickvault_dev\n', '/brickvault_dev?host=remote.invalid\n'),
    valid.replace('BVA_LOG_LEVEL=INFO\n', ''),
    valid + 'BVA_LOG_LEVEL=ERROR\n',
    valid + 'VITE_DATABASE_URL=secret-sentinel\n',
    valid + 'secret-sentinel\n',
  ];
  for (const invalid of invalidCases) {
    writeFileSync(filename, invalid);
    assert.throws(
      () => initializeConfig(directory),
      (error) => {
        assert.ok(error instanceof SetupError);
        assert.doesNotMatch(error.message, /secret-sentinel|remote\.invalid|[a-f0-9]{64}/u);
        return true;
      },
    );
    assert.deepEqual(readFileSync(filename), Buffer.from(invalid));
  }
});

await test('private-file guard refuses missing ignore rules before creating configuration', (t) => {
  const directory = fixture(t);
  writeFileSync(join(directory, '.gitignore'), '');
  assert.throws(() => initializeConfig(directory), /must be ignored/u);
  assert.equal(existsSync(join(directory, '.env.local')), false);
});

await test('Git refuses a normal dry-run add of generated configuration; index remains empty', (t) => {
  const directory = fixture(t);
  initializeConfig(directory);
  const result = spawnSync('git', ['add', '--dry-run', '--', '.env.local'], {
    cwd: directory,
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /ignored/u);
  const index = spawnSync('git', ['ls-files'], {
    cwd: directory,
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.equal(index.status, 0);
  assert.equal(index.stdout, '');
});

await test('initializer rejects a directory where the private file belongs', (t) => {
  const directory = fixture(t);
  mkdirSync(join(directory, '.env.local'));
  assert.throws(() => initializeConfig(directory), /ordinary file/u);
});

await test('local uv resolver refuses missing and non-executable paths without global fallback', (t) => {
  const directory = fixture(t);
  assert.throws(() => requireLocalUv(directory), /repository-local uv 0\.12\.10/u);
  const executable = localUvPath(directory);
  mkdirSync(executable, { recursive: true });
  assert.throws(() => requireLocalUv(directory), /global uv is not used/u);
});

await test('installed local uv passes its exact version check', () => {
  assert.equal(requireLocalUv(root), localUvPath(root));
});

await test('real uv resolves the same absolute cache with the sync/check arguments and environment', (t) => {
  const directory = fixture(t);
  const unwanted = join(directory, 'unwanted destinations');
  const environment = {
    ...process.env,
    UV_CACHE_DIR: join(unwanted, 'cache'),
    UV_PROJECT_ENVIRONMENT: join(unwanted, 'environment'),
    UV_NO_CACHE: 'true',
    UV_CONFIG_FILE: join(unwanted, 'uv.toml'),
    TEMP: unwanted,
    Temp: unwanted,
    TMPDIR: unwanted,
  };
  for (const cwd of [root, join(root, 'services/api')]) {
    for (const task of ['uv:sync', 'uv:check']) {
      const invocation = uvInvocation(task, root, true, cwd, environment);
      assert.equal(invocation.executable, localUvPath(root));
      assert.equal(invocation.options.cwd, root);
      assert.equal(invocation.options.env.UV_PROJECT_ENVIRONMENT, join(root, 'services/api/.venv'));
      for (const key of ['TMP', 'TEMP', 'TMPDIR']) {
        assert.equal(invocation.options.env[key], join(root, '.local/tmp'));
      }
      assert.equal(invocation.options.env.UV_NO_CACHE, undefined);
      // Keep all actual common arguments and the actual child environment; only
      // replace the operation to ask uv itself for its effective destination.
      const common = invocation.args.slice(invocation.args.indexOf('--directory'));
      const pythonIndex = common.indexOf('--python');
      common.splice(pythonIndex, 2); // cache dir does not accept an interpreter option.
      const result = spawnSync(
        invocation.executable,
        ['cache', 'dir', ...common],
        invocation.options,
      );
      assert.equal(result.status, 0, 'uv cache inspection must succeed');
      assert.equal(result.stdout.trim(), join(root, '.local/uv-cache'));
    }
  }
  assert.equal(existsSync(unwanted), false);
});

await test('documented offline uv commands work from root and API despite inherited destination overrides', (t) => {
  const directory = fixture(t);
  const unwanted = join(directory, 'unwanted destinations');
  for (const cwd of [root, join(root, 'services/api')]) {
    for (const task of ['uv:sync', 'uv:check', 'uv:cache']) {
      const result = spawnSync(
        process.execPath,
        [join(root, 'scripts/tasks.mjs'), task, '--offline'],
        {
          cwd,
          encoding: 'utf8',
          windowsHide: true,
          env: {
            ...process.env,
            UV_CACHE_DIR: join(unwanted, 'cache'),
            UV_PROJECT_ENVIRONMENT: join(unwanted, 'environment'),
            UV_NO_CACHE: 'true',
            UV_CONFIG_FILE: join(unwanted, 'uv.toml'),
            TEMP: unwanted,
            TMP: unwanted,
            TMPDIR: unwanted,
          },
        },
      );
      assert.equal(result.status, 0, `${task} must succeed from ${cwd}; output redacted`);
      if (task === 'uv:cache') assert.equal(result.stdout.trim(), join(root, '.local/uv-cache'));
    }
  }
  assert.equal(existsSync(unwanted), false);
  assert.equal(existsSync(join(root, 'services/api/.local/uv-cache')), false);
  const python = join(
    root,
    'services/api/.venv',
    process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python',
  );
  const result = spawnSync(python, ['-c', 'import sys; print(sys.prefix)'], {
    cwd: root,
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.equal(result.status, 0);
  assert.equal(resolve(result.stdout.trim()), join(root, 'services/api/.venv'));
});

await test('uv rejects unsupported working directories and flags before creating files', (t) => {
  const directory = fixture(t);
  const before = readdirSync(directory, { recursive: true });
  for (const task of ['uv:sync', 'uv:check', 'uv:cache']) {
    const result = cli(directory, [task, '--offline']);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /repository root or services\/api/u);
    const badFlag = cli(root, [task, '--cache-dir=secret-sentinel']);
    assert.equal(badFlag.status, 1);
    assert.doesNotMatch(badFlag.stderr + badFlag.stdout, /secret-sentinel/u);
  }
  assert.deepEqual(readdirSync(directory, { recursive: true }), before);
});

await test('uv child failures retain their exit status and redact diagnostic values', (t) => {
  const directory = fixture(t);
  const executable = localUvPath(directory);
  mkdirSync(resolve(executable, '..'), { recursive: true });
  copyFileSync(localUvPath(root), executable);
  mkdirSync(join(directory, 'scripts'));
  copyFileSync(join(root, 'scripts/tasks.mjs'), join(directory, 'scripts/tasks.mjs'));
  mkdirSync(join(directory, 'services/api'), { recursive: true });
  copyFileSync(
    join(root, 'services/api/.python-version'),
    join(directory, 'services/api/.python-version'),
  );
  writeFileSync(join(directory, 'services/api/pyproject.toml'), 'secret-sentinel = [\n');
  const invocation = uvInvocation('uv:check', directory, true, directory);
  const child = spawnSync(executable, invocation.args, invocation.options);
  assert.notEqual(child.status, 0);
  assert.match(child.stderr, /secret-sentinel/u); // Only captured fixture data; never print it.
  const result = spawnSync(process.execPath, ['scripts/tasks.mjs', 'uv:check', '--offline'], {
    cwd: directory,
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.equal(result.status, child.status);
  assert.match(result.stdout, /failed.*tool output redacted/u);
  assert.doesNotMatch(result.stdout + result.stderr, /secret-sentinel/u);
});

await test('ESLint config covers every authored mjs file and detects an actual unused variable', async () => {
  const eslint = new ESLint({ cwd: root });
  for (const filename of [
    'scripts/tasks.mjs',
    'scripts/tasks.test.mjs',
    'eslint.config.mjs',
    'prettier.config.mjs',
  ]) {
    assert.equal(await eslint.isPathIgnored(join(root, filename)), false);
  }
  const results = await eslint.lintText('const unusedSliceOneProbe = 1;\n', {
    filePath: 'scripts/tasks.mjs',
  });
  assert.ok(
    results.some((result) =>
      result.messages.some(
        (message) => message.ruleId === '@typescript-eslint/no-unused-vars' && !message.fatal,
      ),
    ),
  );
  const child = spawnSync(
    process.execPath,
    [
      join(root, 'node_modules/eslint/bin/eslint.js'),
      '--stdin',
      '--stdin-filename',
      'scripts/tasks.mjs',
      '--format',
      'json',
    ],
    {
      cwd: root,
      input: 'const unusedSliceOneProbe = 1;\n',
      encoding: 'utf8',
      windowsHide: true,
    },
  );
  assert.equal(child.status, 1);
  assert.match(child.stdout, /"ruleId":"@typescript-eslint\/no-unused-vars"/u);
  assert.doesNotMatch(child.stdout, /"fatal":true/u);
});
