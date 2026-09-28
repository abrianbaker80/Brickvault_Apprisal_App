import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  linkSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  renameSync,
  rmSync,
  rmdirSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import { join, resolve, sep } from 'node:path';
import { test } from 'node:test';
import { initializeConfig, repositoryRoot, verifyFrontend } from './tasks.mjs';

const scratch = join(repositoryRoot(), '.local', 'tests');

/** @param {import('node:test').TestContext} t */
function fixture(t) {
  mkdirSync(scratch, { recursive: true });
  const root = mkdtempSync(join(scratch, 'frontend artifact '));
  t.after(() => {
    assert.ok(resolve(root).startsWith(resolve(scratch) + sep));
    rmSync(root, { recursive: true, force: true });
  });
  const git = spawnSync('git', ['init', '--quiet', root], {
    encoding: 'utf8',
    windowsHide: true,
  });
  assert.equal(git.status, 0);
  writeFileSync(join(root, '.gitignore'), '.env\n.env.*\n!.env.example\n.local/\n');
  initializeConfig(root);
  const build = join(root, 'apps/web/dist');
  const assets = join(build, 'assets');
  mkdirSync(assets, { recursive: true });
  writeFileSync(join(build, 'index.html'), '<script src="/assets/app.js"></script>');
  writeFileSync(join(assets, 'app.js'), 'console.log("public");');
  writeFileSync(join(assets, 'app.css'), 'body { color: black; }');
  return { root, build, assets };
}

await test('ordinary web and PWA builds pass, while private bytes still fail', (t) => {
  const { root, build, assets } = fixture(t);
  verifyFrontend(root, build);
  for (const name of ['sw.js', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png']) {
    writeFileSync(join(build, name), 'public');
  }
  verifyFrontend(root, build);
  const privateValue = readFileSync(join(root, '.env.local'), 'utf8').match(/[a-f0-9]{64}/u)?.[0];
  assert.ok(privateValue);
  writeFileSync(join(assets, 'app.js'), privateValue);
  assert.throws(() => verifyFrontend(root, build), /private configuration/u);
  writeFileSync(join(assets, 'app.js'), 'console.log("public");');
  writeFileSync(join(build, 'sw.js'), 'BVA_BUILD_CREDENTIAL_SENTINEL_1C');
  assert.throws(() => verifyFrontend(root, build), /private configuration/u);
});

await test('asset names outside flat JS/CSS allowlist fail', (t) => {
  const { root, build, assets } = fixture(t);
  for (const name of ['app.txt', 'app.js.map', 'caps.JS', 'app.js.extra']) {
    const path = join(assets, name);
    writeFileSync(path, 'public');
    assert.throws(() => verifyFrontend(root, build), /unsupported asset name/u);
    unlinkSync(path);
  }
});

await test('linked build directory fails', (t) => {
  const { root, build } = fixture(t);
  const original = join(root, 'apps/web/dist-original');
  renameSync(build, original);
  symlinkSync(original, build, process.platform === 'win32' ? 'junction' : 'dir');
  assert.throws(() => verifyFrontend(root, build), /unsafe directory/u);
});

await test('linked assets directory fails', (t) => {
  const { root, build, assets } = fixture(t);
  const original = join(root, 'assets-original');
  renameSync(assets, original);
  symlinkSync(original, assets, process.platform === 'win32' ? 'junction' : 'dir');
  assert.throws(() => verifyFrontend(root, build), /unsafe directory/u);
});

await test('non-regular entry and asset files fail before content reads', (t) => {
  const { root, build, assets } = fixture(t);
  const index = join(build, 'index.html');
  unlinkSync(index);
  mkdirSync(index);
  assert.throws(() => verifyFrontend(root, build), /unsafe path/u);
  rmdirSync(index);
  writeFileSync(index, '<script src="/assets/app.js"></script>');
  const asset = join(assets, 'app.js');
  unlinkSync(asset);
  mkdirSync(asset);
  assert.throws(() => verifyFrontend(root, build), /unsafe path/u);
});

await test('hard-linked entry, asset and PWA files fail', (t) => {
  const { root, build, assets } = fixture(t);
  const index = join(build, 'index.html');
  const linkedIndex = join(root, 'linked-index.html');
  linkSync(index, linkedIndex);
  assert.throws(() => verifyFrontend(root, build), /unsafe path/u);
  unlinkSync(linkedIndex);
  const asset = join(assets, 'app.js');
  linkSync(asset, join(root, 'linked-app.js'));
  assert.throws(() => verifyFrontend(root, build), /unsafe path/u);
  unlinkSync(join(root, 'linked-app.js'));
  for (const name of ['sw.js', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png']) {
    writeFileSync(join(build, name), 'public');
  }
  linkSync(join(build, 'sw.js'), join(root, 'linked-sw.js'));
  assert.throws(() => verifyFrontend(root, build), /unsafe path/u);
});
