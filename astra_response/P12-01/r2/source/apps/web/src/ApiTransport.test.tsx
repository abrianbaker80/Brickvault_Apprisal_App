import { afterEach, expect, it, vi } from 'vitest';
import { apiDestination, apiFetch } from './api-transport';
import { sessionFetch, configureSession } from './session-client';

afterEach(() => vi.unstubAllEnvs());
it('ordinary browser and PWA retain same-origin credentials and no-store', async () => {
  const fetcher = vi.fn().mockResolvedValue(new Response());
  vi.stubGlobal('fetch', fetcher);
  await apiFetch(new Request('/api/auth/login', { method: 'POST', body: 'sentinel' }));
  const request = fetcher.mock.calls[0]![0] as Request;
  expect(request.url).toBe(window.location.origin + '/api/auth/login');
  expect(request.credentials).toBe('same-origin');
  expect(request.cache).toBe('no-store');
  expect(request.redirect).toBe('error');
  expect(request.method).toBe('POST');
  expect(await request.text()).toBe('sentinel');
});
it('qualification accepts only the exact document and API origins', () => {
  vi.stubEnv('MODE', 'android-qualification');
  expect(
    apiDestination(
      'https://localhost/api/auth/session',
      'https://localhost',
      'android-qualification',
    ),
  ).toEqual({
    url: 'https://localhost:18443/api/auth/session',
    credentials: 'include',
  });
  expect(() =>
    apiDestination(
      'http://localhost/api/auth/session',
      'http://localhost',
      'android-qualification',
    ),
  ).toThrow();
  expect(() =>
    apiDestination('https://localhost:443/api/a', 'https://localhost:444', 'android-qualification'),
  ).toThrow();
});
it('production Android uses only the exact same-site HTTPS API destination', () => {
  expect(
    apiDestination(
      'https://android.app.example.test/api/auth/session',
      'https://android.app.example.test',
      'android-production',
      'https://app.example.test',
    ),
  ).toEqual({ url: 'https://app.example.test/api/auth/session', credentials: 'include' });
  for (const apiOrigin of [
    undefined,
    'http://app.example.test',
    'https://localhost:18443',
    'https://app.example.test:443',
  ]) {
    expect(() =>
      apiDestination(
        'https://android.app.example.test/api/a',
        'https://android.app.example.test',
        'android-production',
        apiOrigin,
      ),
    ).toThrow();
  }
  expect(() =>
    apiDestination(
      'https://localhost/api/a',
      'https://localhost',
      'android-production',
      'https://app.example.test',
    ),
  ).toThrow();
  expect(() =>
    apiDestination(
      'https://localhost/api/a',
      'https://localhost',
      'android-qualification',
      'https://app.example.test',
    ),
  ).toThrow();
});
it.each([
  'https://evil.example/api/a',
  'https://localhost:18443/api/a',
  'https://localhost.evil.example/api/a',
  'http://127.0.0.1:5173/not-api',
  'http://127.0.0.1:5173/api/a#fragment',
])('refuses credential forwarding to %s before fetch', async (url) => {
  const fetcher = vi.fn();
  vi.stubGlobal('fetch', fetcher);
  configureSession(
    'secret-csrf',
    () => {},
    () => {},
  );
  expect(() => apiFetch(new Request(url))).toThrow();
  await expect(sessionFetch(new Request(url, { method: 'POST' }))).rejects.toThrow();
  expect(fetcher).not.toHaveBeenCalled();
});

it('refuses URL credentials before Request construction', () => {
  expect(() => apiDestination('http://user:pass@127.0.0.1:5173/api/a')).toThrow();
});

it('qualification preserves mutation body, headers and cancellation over HTTPS', async () => {
  vi.stubEnv('MODE', 'android-qualification');
  vi.stubGlobal('window', {
    location: { origin: 'https://localhost', href: 'https://localhost/' },
  });
  const fetcher = vi.fn().mockResolvedValue(new Response());
  vi.stubGlobal('fetch', fetcher);
  const controller = new AbortController();
  await apiFetch(
    new Request('https://localhost/api/watchlist', {
      method: 'POST',
      body: '{"value":1}',
      headers: { 'X-CSRF-Token': 'synthetic' },
      signal: controller.signal,
    }),
  );
  const request = fetcher.mock.calls[0]![0] as Request;
  expect(request.url).toBe('https://localhost:18443/api/watchlist');
  expect(request.credentials).toBe('include');
  expect(request.method).toBe('POST');
  expect(request.headers.get('X-CSRF-Token')).toBe('synthetic');
  expect(await request.text()).toBe('{"value":1}');
  controller.abort();
  expect(request.signal.aborted).toBe(true);
});
