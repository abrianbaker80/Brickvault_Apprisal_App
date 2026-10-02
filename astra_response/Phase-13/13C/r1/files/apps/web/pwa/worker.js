/* RELEASE and RESOURCES are generated from the exact public build bytes. */
const PREFIX = 'brickvault-public-shell-';
const CACHE = PREFIX + RELEASE;
const UUID = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}';
function navigation(path) {
  return (
    ['/', '/deals', '/watchlist', '/settings', '/hunt', '/listings'].includes(path) ||
    /^\/sets\/[A-Za-z0-9][A-Za-z0-9._+-]{0,255}$/.test(path) ||
    new RegExp(`^/(deals|hunt|listings)/${UUID}$`).test(path)
  );
}
self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      // Validate the entire release before publishing any resource. Never cache a
      // login redirect, private response or HTML returned in place of an asset.
      const responses = await Promise.all(
        Object.entries(RESOURCES).map(async ([path, digest]) => {
          const response = await fetch(path, {
            credentials: 'omit',
            cache: 'no-store',
            redirect: 'error',
          });
          if (!response.ok || response.headers.get('cache-control')?.includes('no-store'))
            throw new Error('Public shell unavailable');
          const hash = await crypto.subtle.digest('SHA-256', await response.clone().arrayBuffer());
          const actual = Array.from(new Uint8Array(hash), (b) =>
            b.toString(16).padStart(2, '0'),
          ).join('');
          if (actual !== digest) throw new Error('Mixed shell release');
          return [path, response];
        }),
      );
      try {
        const cache = await caches.open(CACHE);
        for (const [path, response] of responses) await cache.put(path, response);
      } catch (error) {
        await caches.delete(CACHE);
        throw error;
      }
    })(),
  );
});
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      for (const key of await caches.keys()) {
        if (key !== CACHE && /^brickvault-public-shell-[a-f0-9]{64}$/.test(key))
          await caches.delete(key);
      }
      await self.clients.claim();
    })(),
  );
});
self.addEventListener('message', (event) => {
  if (event.data !== 'ACTIVATE_PUBLIC_SHELL' || !event.source) return;
  event.waitUntil(
    (async () => {
      const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
      // An update must not take another open workspace through a version change.
      if (windows.length !== 1 || windows[0].id !== event.source.id) {
        event.source.postMessage('PUBLIC_SHELL_OTHER_TABS');
        return;
      }
      await self.skipWaiting();
    })(),
  );
});
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (
    request.method !== 'GET' ||
    url.origin !== self.location.origin ||
    url.pathname === '/api' ||
    url.pathname.startsWith('/api/')
  )
    return;
  const key =
    request.mode === 'navigate' && navigation(url.pathname)
      ? '/'
      : !url.search && Object.hasOwn(RESOURCES, url.pathname)
        ? url.pathname
        : null;
  if (!key) return;
  // No runtime cache writes and no network fallback mixing releases. API and
  // external traffic are never intercepted. Only the generic entry is retained.
  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE);
      return (
        (await cache.match(key)) ??
        new Response('Public shell unavailable. Reconnect and reload.', {
          status: 503,
          headers: { 'Content-Type': 'text/plain', 'Cache-Control': 'no-store' },
        })
      );
    })(),
  );
});
