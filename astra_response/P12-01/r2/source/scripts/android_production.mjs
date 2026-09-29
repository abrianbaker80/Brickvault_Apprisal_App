/** Build one reviewed Android web bundle and copy only its matching Capacitor config. */
import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { frontendEnvironment, verifyFrontend } from './tasks.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const origin = process.env.BVA_ANDROID_PRODUCTION_ORIGIN;

if (
  origin === undefined ||
  !/^https:\/\/(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z](?:[a-z0-9-]*[a-z0-9])?$/.test(origin) ||
  origin.endsWith('.localhost') ||
  process.env.BVA_ANDROID_MODE !== undefined ||
  process.env.VITE_BVA_PRODUCTION_ORIGIN !== undefined
) {
  throw new Error('An explicit approved Android HTTPS origin is required');
}

const safe = frontendEnvironment();
const web = join(root, 'apps/web');
const android = join(root, 'apps/android');

/** @param {string} cwd @param {string} script @param {string[]} args @param {NodeJS.ProcessEnv} environment */
function run(cwd, script, args, environment) {
  const result = spawnSync(process.execPath, [script, ...args], {
    cwd,
    env: environment,
    stdio: 'inherit',
    windowsHide: true,
  });
  if (result.error || result.status !== 0) throw new Error('Android production packaging failed');
}

run(web, join(web, 'node_modules/vite/bin/vite.js'), ['build', '--mode', 'android-production'], {
  ...safe,
  VITE_BVA_PRODUCTION_ORIGIN: origin,
});
verifyFrontend(root);
const assets = join(web, 'dist/assets');
const js = readdirSync(assets)
  .filter((name) => name.endsWith('.js'))
  .map((name) => readFileSync(join(assets, name), 'utf8'))
  .join('');
if (!js.includes(origin) || js.includes('https://localhost:18443')) {
  throw new Error('Android production frontend contains an unsafe transport');
}

run(android, join(android, 'node_modules/@capacitor/cli/bin/capacitor'), ['copy', 'android'], {
  ...safe,
  BVA_ANDROID_MODE: 'production',
  BVA_ANDROID_PRODUCTION_ORIGIN: origin,
});
/** @type {unknown} */
const parsed = JSON.parse(
  readFileSync(join(android, 'android/app/src/main/assets/capacitor.config.json'), 'utf8'),
);
const copied =
  /** @type {{server?: {hostname?: unknown, androidScheme?: unknown, cleartext?: unknown, url?: unknown, allowNavigation?: unknown}, plugins?: {CapacitorHttp?: {enabled?: unknown}, CapacitorCookies?: {enabled?: unknown}}}} */ (
    parsed
  );
const expectedHost = 'android.' + new URL(origin).hostname;
if (
  copied.server?.hostname !== expectedHost ||
  copied.server?.androidScheme !== 'https' ||
  copied.server?.cleartext !== false ||
  copied.server?.url !== undefined ||
  copied.server?.allowNavigation !== undefined ||
  copied.plugins?.CapacitorHttp?.enabled !== false ||
  copied.plugins?.CapacitorCookies?.enabled !== false
) {
  throw new Error('Copied Android production configuration does not match the approved origin');
}
const trust = readFileSync(
  join(android, 'android/app/src/main/res/xml/network_security_config.xml'),
  'utf8',
);
if (
  !trust.includes('certificates src="system"') ||
  trust.includes('@raw/qualification_certificate')
) {
  throw new Error('Android production trust configuration is unsafe');
}
console.log('Android production web/config bundle verified; no APK built.');
