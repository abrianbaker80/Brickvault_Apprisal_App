import { createContext, useContext, useEffect, useRef, useState } from 'react';
import type { FormEvent, ReactNode } from 'react';
import createClient from 'openapi-fetch';
import { apiFetch } from './api-transport';
import { observeNativeResume } from './native-lifecycle';
import {
  initializeNativeShare,
  setNativeShareAuthenticated,
  setNativeShareVerified,
} from './native-share';
import { NativeShareNotice } from './NativeShareReview';
import type { components, paths } from '@brickvault/contracts';
import { AppShell } from './AppShell';
import { cancelSessionRequests, configureSession, rereadVisibleViews } from './session-client';
import {
  clearPrivateViews,
  connectionSnapshot,
  privateDeadline,
  privateSessionValid,
  startPrivateSession,
  transition,
  transportFailure,
} from './private-views';
import { useConnection } from './Connectivity';
import type { RevisionContext } from './revision-draft';
import type { HuntRunCreate } from './hunt-api';

type Session = components['schemas']['SessionState'];
type Draft = Record<string, string>;
export type DraftMemory = {
  value: {
    number: string;
    draft: Draft;
    defaultsPending?: boolean;
    revision?: RevisionContext;
  } | null;
  forecastId: string | null;
  ownerId: string | null;
  huntAttempt: { ownerId: string; fingerprint: string; request: HuntRunCreate } | null;
  huntRecoveryReady: boolean;
};
const DraftContext = createContext<DraftMemory | null>(null);
export const DraftMemoryProvider = DraftContext.Provider;
const LogoutContext = createContext<(() => void) | null>(null);
export const useDraftMemory = () => useContext(DraftContext);
export const useLogout = () => useContext(LogoutContext);
const client = createClient<paths>({ fetch: apiFetch });

export function Authentication({ children }: { children: ReactNode }) {
  const connection = useConnection();
  const [session, setSession] = useState<Session | null>(null);
  const [checking, setChecking] = useState(true);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [password, setPassword] = useState('');
  const [logoutPending, setLogoutPending] = useState(false);
  const [unavailable, setUnavailable] = useState(false);
  const draft = useRef<DraftMemory>({
    value: null,
    forecastId: null,
    ownerId: null,
    huntAttempt: null,
    huntRecoveryReady: false,
  });
  const owner = useRef<string | null>(null);
  const current = useRef<Session | null>(null);
  const locked = useRef(true);
  const sessionKnown = useRef(false);
  const generation = useRef(0);
  const channel = useRef<BroadcastChannel | null>(null);
  const expiryTimer = useRef<number | undefined>(undefined);
  const input = useRef<HTMLInputElement>(null);

  function lock(explicit = false) {
    sessionKnown.current = true;
    setNativeShareAuthenticated(false);
    clearPrivateViews();
    setUnavailable(false);
    locked.current = true;
    generation.current++;
    window.clearTimeout(expiryTimer.current);
    configureSession(
      null,
      () => {},
      () => {},
    );
    if (explicit) {
      draft.current.value = null;
      draft.current.forecastId = null;
      draft.current.huntAttempt = null;
      draft.current.huntRecoveryReady = false;
      draft.current.ownerId = null;
      owner.current = null;
    } else if (draft.current.huntAttempt) {
      draft.current.huntRecoveryReady = true;
    }
    setSession(null);
    setChecking(false);
    setBusy(false);
    setPassword('');
    setMessage(
      explicit
        ? 'Signed out.'
        : draft.current.huntAttempt
          ? 'Your session is locked. Sign in to review or retry the saved Hunt request. It remains only in this tab.'
          : draft.current.value
            ? 'Your session is locked. Sign in to continue. Unsaved assumptions remain only in this tab.'
            : 'Sign in to continue.',
    );
    document.title = 'Sign in | BrickVault';
  }

  function schedule(idle: string, absolute: string) {
    // Responses can arrive out of order. A passive read taken before a concurrent
    // user request must not undo that request's later inactivity deadline.
    const idleDeadline = Math.max(
      Date.parse(idle),
      Date.parse(current.current?.idle_expires_at ?? idle),
    );
    const until = Math.min(idleDeadline, Date.parse(absolute));
    privateDeadline(until);
    window.clearTimeout(expiryTimer.current);
    if (!Number.isFinite(until) || until <= Date.now()) {
      lock();
      return;
    }
    if (current.current)
      current.current = {
        ...current.current,
        idle_expires_at: new Date(until).toISOString(),
        absolute_expires_at: absolute,
      };
    expiryTimer.current = window.setTimeout(() => lock(), until - Date.now());
  }

  function accept(value: Session) {
    sessionKnown.current = true;
    setUnavailable(false);
    locked.current = false;
    if (owner.current !== value.principal_id) {
      draft.current.value = null;
      draft.current.forecastId = null;
      draft.current.huntAttempt = null;
      draft.current.huntRecoveryReady = false;
    }
    if (draft.current.huntAttempt?.ownerId !== value.principal_id) {
      draft.current.huntAttempt = null;
      draft.current.huntRecoveryReady = false;
    }
    owner.current = value.principal_id;
    draft.current.ownerId = value.principal_id;
    current.current = value;
    startPrivateSession(
      value.principal_id,
      Math.min(Date.parse(value.idle_expires_at), Date.parse(value.absolute_expires_at)),
    );
    setSession(value);
    setChecking(false);
    setBusy(false);
    setMessage('');
    setLogoutPending(false);
    configureSession(value.csrf_token, () => lock(), schedule, transportLost);
    schedule(value.idle_expires_at, value.absolute_expires_at);
    if (!locked.current) setNativeShareAuthenticated(true);
  }

  function transportLost() {
    setNativeShareVerified(false);
    if (!locked.current && privateSessionValid()) {
      cancelSessionRequests();
      transition('OFFLINE_CACHED', true);
    } else {
      lock();
      transition('PUBLIC_OFFLINE_SHELL');
      setUnavailable(true);
    }
  }

  async function check(initial = false) {
    if (!initial && connectionSnapshot().state === 'CHECKING_CONNECTION') return;
    const attempt = ++generation.current;
    if (!initial) {
      setNativeShareVerified(false);
      transition('CHECKING_CONNECTION');
      cancelSessionRequests();
    }
    try {
      const { data, response } = await client.GET('/api/auth/session', {
        cache: 'no-store',
        redirect: 'error',
        signal: AbortSignal.timeout(10000),
      });
      if (attempt !== generation.current) return;
      if (!data) {
        lock();
        if (response.status !== 401)
          setMessage('Session verification failed. The service returned an error. Try again.');
      } else if (initial) accept(data);
      else if (
        current.current?.csrf_token === data.csrf_token &&
        current.current.principal_id === data.principal_id
      ) {
        schedule(data.idle_expires_at, data.absolute_expires_at);
        if (locked.current || attempt !== generation.current) return;
        await rereadVisibleViews();
        if (attempt === generation.current && !locked.current && privateSessionValid()) {
          transition('ONLINE_VERIFIED', true);
          setNativeShareVerified(true);
        }
      } else lock();
    } catch (error) {
      if (attempt === generation.current) {
        if (!initial && transportFailure(error) && !locked.current && privateSessionValid()) {
          transition('OFFLINE_CACHED', true);
          return;
        }
        lock();
        if (transportFailure(error)) transition('PUBLIC_OFFLINE_SHELL');
        setUnavailable(transportFailure(error));
        setMessage(
          transportFailure(error)
            ? 'Connect to sign in. Private records are unavailable until your session can be verified.'
            : 'Session verification failed. The service returned an invalid response. Try again.',
        );
      }
    }
  }

  useEffect(() => {
    const stopShare = initializeNativeShare();
    void check(true);
    const verify = () => {
      if (locked.current) {
        // Warm Share can launch a signed-out app after native onPause invalidated
        // its admission. Resolve that outcome again without retaining through login.
        // The first cold session check is still unknown and must keep its URI refs.
        if (sessionKnown.current) setNativeShareAuthenticated(false);
        return;
      }
      if (
        current.current &&
        Math.min(
          Date.parse(current.current.idle_expires_at),
          Date.parse(current.current.absolute_expires_at),
        ) <= Date.now()
      )
        lock();
      else void check();
    };
    const stopNative = observeNativeResume(verify, () => lock());
    const focus = () => {
      if (document.visibilityState !== 'hidden') verify();
    };
    const visibility = () => {
      if (document.visibilityState === 'visible') focus();
    };
    window.addEventListener('focus', focus);
    window.addEventListener('pageshow', focus);
    window.addEventListener('online', focus);
    window.addEventListener('offline', focus);
    document.addEventListener('visibilitychange', visibility);
    if (typeof BroadcastChannel !== 'undefined') {
      channel.current = new BroadcastChannel('brickvault-session');
      channel.current.onmessage = (event: MessageEvent<unknown>) => {
        if (event.data === 'logout') {
          current.current = null;
          lock(true);
        }
      };
    }
    return () => {
      stopNative();
      stopShare();
      generation.current++;
      window.clearTimeout(expiryTimer.current);
      configureSession(
        null,
        () => {},
        () => {},
      );
      clearPrivateViews();
      window.removeEventListener('focus', focus);
      window.removeEventListener('pageshow', focus);
      window.removeEventListener('online', focus);
      window.removeEventListener('offline', focus);
      document.removeEventListener('visibilitychange', visibility);
      channel.current?.close();
    };
    // The boundary owns one document lifetime; callbacks read current refs.
  }, []);

  useEffect(() => {
    if (!session && !checking) {
      input.current?.focus();
      window.scrollTo(0, 0);
    }
  }, [session, checking]);

  async function login(event: FormEvent) {
    event.preventDefault();
    const attempt = ++generation.current;
    setBusy(true);
    setUnavailable(false);
    setMessage('');
    const submitted = password;
    setPassword('');
    try {
      const { data, response } = await client.POST('/api/auth/login', {
        body: { password: submitted },
        headers: { 'X-BrickVault-Login': '1' },
        cache: 'no-store',
        redirect: 'error',
        signal: AbortSignal.timeout(10000),
      });
      if (attempt !== generation.current) return;
      if (data) accept(data);
      else {
        setBusy(false);
        setMessage(
          response.status === 429
            ? 'Too many sign-in attempts. Try again in five minutes.'
            : 'Sign-in failed. Check your password and local service, then try again.',
        );
      }
    } catch (error) {
      if (attempt === generation.current) {
        setBusy(false);
        setUnavailable(transportFailure(error));
        setMessage(
          transportFailure(error)
            ? 'Connect to sign in. Sign-in could not be confirmed.'
            : 'Sign-in could not be completed. Try again.',
        );
      }
    }
  }

  async function logout() {
    const csrf = current.current?.csrf_token;
    lock(true);
    setLogoutPending(true);
    channel.current?.postMessage('logout');
    const attempt = generation.current;
    try {
      const { response } = await client.POST('/api/auth/logout', {
        headers: { 'X-CSRF-Token': csrf ?? '' },
        cache: 'no-store',
        redirect: 'error',
        signal: AbortSignal.timeout(10000),
      });
      if (attempt !== generation.current) return;
      if (response.status === 204 || response.status === 401) {
        current.current = null;
        setLogoutPending(false);
      } else setMessage('Views are locked, but server sign-out was not confirmed. Retry sign out.');
    } catch {
      if (attempt === generation.current)
        setMessage('Views are locked, but server sign-out was not confirmed. Retry sign out.');
    }
  }

  if (session)
    return (
      <DraftContext.Provider value={draft.current}>
        <LogoutContext.Provider value={() => void logout()}>
          {connection.state !== 'ONLINE_VERIFIED' && (
            <aside className="connectivity-banner" aria-label="Connection status">
              <strong>
                {connection.state === 'CHECKING_CONNECTION'
                  ? 'Checking connection…'
                  : 'Offline — cached views only'}
              </strong>
              <p>
                Read-only until your session is verified. Changes and calculations are unavailable.
                Offline viewing ends at the last confirmed session deadline.
              </p>
              <button
                disabled={connection.state === 'CHECKING_CONNECTION'}
                onClick={() => void check()}
              >
                Check connection
              </button>
            </aside>
          )}
          {children}
        </LogoutContext.Provider>
      </DraftContext.Provider>
    );
  return (
    <AppShell scout={false} navigate={(event) => event.preventDefault()} search={null}>
      <section className="auth-panel" aria-labelledby="auth-title">
        <p className="eyebrow">Private workspace</p>
        <h1 id="auth-title">{unavailable ? 'Connection unavailable' : 'Sign in to BrickVault'}</h1>
        {checking ? (
          <p role="status">Checking your session…</p>
        ) : (
          <>
            <p>Brian’s personal LEGO appraisal workspace.</p>
            {message && <p role="status">{message}</p>}
            <NativeShareNotice />
            {logoutPending ? (
              <button onClick={() => void logout()}>Retry sign out</button>
            ) : unavailable ? (
              <button
                onClick={() => {
                  setChecking(true);
                  void check(true);
                }}
              >
                Check connection
              </button>
            ) : (
              <form onSubmit={(event) => void login(event)}>
                <label htmlFor="auth-password">Password</label>
                <input
                  ref={input}
                  id="auth-password"
                  type="password"
                  autoComplete="current-password"
                  required
                  maxLength={256}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  disabled={busy}
                />
                <button type="submit" disabled={busy}>
                  {busy ? 'Signing in…' : 'Sign in'}
                </button>
              </form>
            )}
          </>
        )}
      </section>
    </AppShell>
  );
}
