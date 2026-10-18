import { StrictMode } from 'react';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { Authentication, useLogout } from './Authentication';
import { NativeShareNotice } from './NativeShareReview';
import { nativeShareSnapshot } from './native-share';
vi.mock('openapi-fetch', async (importOriginal) => {
  const original = await importOriginal<typeof import('openapi-fetch')>();
  return {
    ...original,
    default: (options?: Parameters<typeof original.default>[0]) =>
      original.default({ baseUrl: window.location.origin, ...options }),
  };
});

const native = vi.hoisted(() => ({
  authenticated: null as boolean | null,
  pending: true,
  notice: null as string | null,
  resume: () => {},
  activity: (event: { isActive: boolean }) => {
    void event;
  },
  share: () => {},
  sessions: [] as boolean[],
  read: vi.fn(() => Promise.resolve({ data: 'AP8QIA==', byteCount: 4, eof: true })),
}));
vi.mock('@capacitor/core', () => ({
  Capacitor: { isNativePlatform: () => true },
  registerPlugin: () => ({
    setSession: ({ authenticated }: { authenticated: boolean }) => {
      native.sessions.push(authenticated);
      native.authenticated = authenticated;
      if (!authenticated && native.pending) {
        native.pending = false;
        native.notice = 'SIGN_IN_AND_RESHARE';
      }
      return Promise.resolve();
    },
    getPendingShare: () =>
      Promise.resolve({
        batch:
          native.authenticated && native.pending
            ? {
                id: 'cold-batch',
                state: 'ready',
                items: [
                  {
                    id: 'one',
                    index: 0,
                    filename: 'shared-image-1.png',
                    mimeType: 'image/png',
                    byteCount: 4,
                    state: 'ready',
                    errorCode: null,
                  },
                ],
              }
            : null,
        notice: native.notice,
      }),
    readChunk: native.read,
    acknowledgeShare: () => {
      return Promise.resolve();
    },
    saveUploadContext: () => Promise.resolve(),
    saveReviewContext: () => Promise.resolve(),
    cancelShare: () => {
      native.pending = false;
      return Promise.resolve();
    },
    addListener: (_name: string, callback: () => void) => {
      native.share = callback;
      return Promise.resolve({ remove: () => Promise.resolve() });
    },
  }),
}));
vi.mock('@capacitor/app', () => ({
  App: {
    addListener: (event: string, callback: () => void) => {
      if (event === 'resume') native.resume = callback;
      else native.activity = callback;
      return Promise.resolve({ remove: () => Promise.resolve() });
    },
  },
}));
function LogoutButton() {
  const logout = useLogout();
  return (
    <>
      <NativeShareNotice />
      <button onClick={logout ?? undefined}>Synthetic logout</button>
    </>
  );
}
function deferredResponse() {
  let resolve!: (response: Response) => void;
  const promise = new Promise<Response>((done) => {
    resolve = done;
  });
  return { promise, resolve };
}
const session = {
  principal_id: 'synthetic-owner',
  csrf_token: 'synthetic-csrf',
  idle_expires_at: new Date(Date.now() + 1800000).toISOString(),
  absolute_expires_at: new Date(Date.now() + 43200000).toISOString(),
};

it('preserves cold URI admission through StrictMode and initial session checking, re-authorizes only after resume verification, and discards warm signed-out intake', async () => {
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {});
  const cold = deferredResponse();
  const resumed = deferredResponse();
  let checks = 0;
  const fetcher = vi.fn<(request: Request) => Promise<Response>>((request) => {
    if (request.method === 'POST') return Promise.resolve(new Response(null, { status: 204 }));
    checks++;
    if (checks <= 2) return cold.promise.then((response) => response.clone());
    return resumed.promise;
  });
  vi.stubGlobal('fetch', fetcher);
  const view = render(
    <StrictMode>
      <Authentication>
        <LogoutButton />
      </Authentication>
    </StrictMode>,
  );
  await act(() => Promise.resolve());
  expect(native.sessions).toEqual([]);
  expect(native.pending).toBe(true);
  expect(native.read).not.toHaveBeenCalled();
  await act(() => {
    cold.resolve(Response.json(session));
    return Promise.resolve();
  });
  await waitFor(() => expect(nativeShareSnapshot().state).toBe('ready'));
  expect(native.sessions).toEqual([true]);
  expect(native.read).toHaveBeenCalledTimes(1);

  act(() => {
    native.authenticated = null; // Native onPause invalidates admission without discarding bytes.
    native.activity({ isActive: false });
    native.activity({ isActive: true });
    native.resume();
  });
  expect(nativeShareSnapshot().verified).toBe(false);
  expect(native.sessions).toEqual([true]);
  await act(() => {
    resumed.resolve(Response.json(session));
    return Promise.resolve();
  });
  await waitFor(() => expect(native.sessions).toEqual([true, true]));
  expect(native.read).toHaveBeenCalledTimes(1); // Existing live document File remains; no re-ingestion.
  fireEvent.click(screen.getByRole('button', { name: 'Synthetic logout' }));
  await screen.findByRole('heading', { name: 'Sign in to BrickVault' });
  expect(nativeShareSnapshot().items).toEqual([]);

  act(() => {
    native.authenticated = null;
    native.pending = true; // Explicit warm Share before onResume; its session outcome is unknown.
    native.share();
    native.resume();
  });
  await screen.findByText(/Sign in, then share the images again/);
  expect(native.pending).toBe(false);
  expect(native.read).toHaveBeenCalledTimes(1);
  expect(nativeShareSnapshot().items).toEqual([]);
  view.unmount();
});
