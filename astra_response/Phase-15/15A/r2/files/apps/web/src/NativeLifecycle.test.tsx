import { act, render, screen, waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { Authentication } from './Authentication';
import { connectionSnapshot } from './private-views';
import { PwaUpdate } from './PwaUpdate';
import { observeNativeResume } from './native-lifecycle';
vi.mock('openapi-fetch', async (importOriginal) => {
  const original = await importOriginal<typeof import('openapi-fetch')>();
  return {
    ...original,
    default: (options?: Parameters<typeof original.default>[0]) =>
      original.default({ baseUrl: window.location.origin, ...options }),
  };
});
const native = vi.hoisted(() => ({ resume: () => {}, remove: vi.fn(), enabled: true }));
vi.mock('@capacitor/core', () => ({
  Capacitor: { isNativePlatform: () => native.enabled },
  registerPlugin: () => ({
    setSession: () => Promise.resolve(),
    getPendingShare: () => Promise.resolve({ batch: null, notice: null }),
    addListener: () => Promise.resolve({ remove: () => Promise.resolve() }),
  }),
}));
vi.mock('@capacitor/app', () => ({
  App: {
    addListener: vi.fn((event: string, callback: () => void) => {
      if (event === 'appStateChange') return Promise.resolve({ remove: () => Promise.resolve() });
      expect(event).toBe('resume');
      native.resume = callback;
      return Promise.resolve({ remove: native.remove });
    }),
  },
}));
it('native resume enters checking, passively verifies, and never retries a mutation', async () => {
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {});
  const session = {
    principal_id: 'synthetic',
    csrf_token: 'synthetic',
    idle_expires_at: new Date(Date.now() + 1800000).toISOString(),
    absolute_expires_at: new Date(Date.now() + 43200000).toISOString(),
  };
  let resolve!: (response: Response) => void;
  const fetcher = vi
    .fn<(request: Request) => Promise<Response>>()
    .mockResolvedValueOnce(Response.json(session))
    .mockImplementation(
      () =>
        new Promise<Response>((done) => {
          resolve = done;
        }),
    );
  vi.stubGlobal('fetch', fetcher);
  const view = render(
    <Authentication>
      <p>Private sentinel</p>
    </Authentication>,
  );
  expect(await screen.findByText('Private sentinel')).toBeVisible();
  act(() => native.resume());
  expect(connectionSnapshot().state).toBe('CHECKING_CONNECTION');
  act(() => native.resume());
  expect(fetcher).toHaveBeenCalledTimes(2);
  await act(() => {
    resolve(Response.json(session));
    return Promise.resolve();
  });
  await waitFor(() => expect(connectionSnapshot().state).toBe('ONLINE_VERIFIED'));
  for (const [request] of fetcher.mock.calls) {
    expect(request.method).toBe('GET');
    expect(request.url).toContain('/api/auth/session');
    expect(request.cache).toBe('no-store');
  }
  view.unmount();
  expect(native.remove).toHaveBeenCalledTimes(1);
  native.resume();
  expect(fetcher).toHaveBeenCalledTimes(2);
});
it('browser does not subscribe to native resume', () => {
  native.enabled = false;
  const verify = vi.fn();
  const dispose = observeNativeResume(verify, vi.fn());
  dispose();
  expect(verify).not.toHaveBeenCalled();
  native.enabled = true;
});

it.each([false, true])(
  'PWA worker registration respects actual native platform (%s)',
  async (isNative) => {
    native.enabled = isNative;
    vi.stubEnv('PROD', true);
    const registration = { addEventListener: vi.fn(), removeEventListener: vi.fn() };
    const register = vi.fn().mockResolvedValue(registration);
    vi.stubGlobal('navigator', {
      serviceWorker: { register, addEventListener: vi.fn(), removeEventListener: vi.fn() },
    });
    const view = render(<PwaUpdate />);
    await act(() => Promise.resolve());
    expect(register).toHaveBeenCalledTimes(isNative ? 0 : 1);
    view.unmount();
    vi.unstubAllEnvs();
    native.enabled = true;
  },
);
