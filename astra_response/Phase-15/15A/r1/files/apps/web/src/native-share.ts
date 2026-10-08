import { App } from '@capacitor/app';
import { Capacitor, registerPlugin, type PluginListenerHandle } from '@capacitor/core';

export type NativeShareItem = {
  id: string;
  index: number;
  filename: string;
  mimeType: string | null;
  byteCount: number;
  state: 'pending' | 'ready' | 'failed';
  errorCode: string | null;
};
export type NativeShareBatch = {
  id: string;
  state: 'reading' | 'ready';
  items: NativeShareItem[];
  queueContext?: NativeShareQueueContext | null;
  reviewContext?: NativeShareReviewContext | null;
  handedOff?: boolean;
};
export type NativeShareQueueContext = {
  listingId: string;
  items: { itemId: string; clientUploadId: string; displayOrder: number }[];
};
export type NativeShareReviewContext = { selectedItemIds: string[]; creationUncertain: boolean };
export interface NativeSharePort {
  setSession: (options: { authenticated: boolean }) => Promise<void>;
  getPendingShare: () => Promise<{ batch: NativeShareBatch | null; notice: string | null }>;
  readChunk: (options: {
    batchId: string;
    itemId: string;
    offset: number;
    length: number;
  }) => Promise<{ data: string; byteCount: number; eof: boolean }>;
  acknowledgeShare: (options: { batchId: string }) => Promise<void>;
  saveUploadContext: (options: NativeShareQueueContext & { batchId: string }) => Promise<void>;
  saveReviewContext: (options: NativeShareReviewContext & { batchId: string }) => Promise<void>;
  cancelShare: (options: { batchId?: string }) => Promise<void>;
  addListener: (event: 'shareAvailable', listener: () => void) => Promise<PluginListenerHandle>;
}
export type SharedImage = {
  id: string;
  index: number;
  filename: string;
  file: File | null;
  errorCode: string | null;
};
export type NativeShareSnapshot = {
  batchId: string | null;
  state: 'idle' | 'reading' | 'ready';
  items: SharedImage[];
  notice: string | null;
  foreground: boolean;
  verified: boolean;
  queueContext: NativeShareQueueContext | null;
  reviewContext: NativeShareReviewContext | null;
};
const CHUNK_BYTES = 256 * 1024;
const ITEM_BYTES = 25 * 1024 * 1024;
const BATCH_BYTES = 50 * 1024 * 1024;
const IMAGE_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);
const interrupted = () => new DOMException('Share intake paused', 'AbortError');

/** Volatile intake only. A bridge event never creates a listing or dispatches an upload. */
export class NativeShareIntake {
  private value: NativeShareSnapshot = {
    batchId: null,
    state: 'idle',
    items: [],
    notice: null,
    foreground: true,
    verified: false,
    queueContext: null,
    reviewContext: null,
  };
  private listeners = new Set<() => void>();
  private authenticated = false;
  private verified = false;
  private generation = 0;
  private pulling = false;
  private again = false;
  private sessionWork: Promise<void> = Promise.resolve();
  constructor(private port: NativeSharePort) {}
  snapshot = () => this.value;
  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
  private publish(change: Partial<NativeShareSnapshot>) {
    this.value = { ...this.value, ...change };
    this.listeners.forEach((listener) => listener());
  }
  setForeground(foreground: boolean) {
    if (!foreground) {
      this.generation++;
      this.verified = false;
    }
    this.publish({ foreground, verified: this.verified });
    if (foreground) void this.pull();
  }
  setVerified(verified: boolean) {
    this.verified = verified;
    this.publish({ verified });
    if (!verified) this.generation++;
    else void this.pull();
  }
  setAuthenticated(authenticated: boolean) {
    this.authenticated = authenticated;
    this.verified = authenticated;
    this.generation++;
    const generation = this.generation;
    if (!authenticated)
      this.publish({
        batchId: null,
        state: 'idle',
        items: [],
        notice: null,
        verified: false,
        queueContext: null,
        reviewContext: null,
      });
    else this.publish({ verified: true });
    // Preserve call order so a delayed true cannot restore intake after logout.
    this.sessionWork = this.sessionWork
      .catch(() => {})
      .then(async () => {
        if (authenticated && !this.admitted(generation)) return;
        await this.port.setSession({ authenticated });
      });
    void this.sessionWork.then(
      () => this.pull(),
      () => {
        if (generation !== this.generation) return;
        this.publish({ batchId: null, state: 'idle', items: [], notice: 'SHARE_UNAVAILABLE' });
      },
    );
  }
  async cancel() {
    this.generation++;
    this.publish({
      batchId: null,
      state: 'idle',
      items: [],
      notice: null,
      queueContext: null,
      reviewContext: null,
    });
    try {
      await this.port.cancelShare({});
    } catch {
      this.publish({ notice: 'SHARE_UNAVAILABLE' });
    }
  }
  detach() {
    this.authenticated = false;
    this.verified = false;
    this.generation++;
    this.publish({
      batchId: null,
      state: 'idle',
      items: [],
      notice: null,
      verified: false,
      queueContext: null,
      reviewContext: null,
    });
  }
  async saveUploadContext(context: NativeShareQueueContext) {
    const batchId = this.value.batchId;
    const previous = this.value.queueContext;
    if (!batchId || !this.admitted(this.generation)) throw interrupted();
    await this.port.saveUploadContext({ batchId, ...context });
    if (this.value.batchId === batchId && this.authenticated)
      this.publish({
        queueContext: context,
        reviewContext: previous
          ? this.value.reviewContext
          : {
              selectedItemIds: context.items.map((item) => item.itemId),
              creationUncertain: false,
            },
      });
  }
  async saveReviewContext(context: NativeShareReviewContext) {
    const batchId = this.value.batchId;
    if (!batchId || !this.admitted(this.generation)) throw interrupted();
    await this.port.saveReviewContext({ batchId, ...context });
    if (this.value.batchId === batchId && this.authenticated) {
      const selected = new Set(context.selectedItemIds);
      const bound = new Set(this.value.queueContext?.items.map((item) => item.itemId));
      this.publish({
        reviewContext: context,
        items: this.value.items.map((item) =>
          bound.has(item.id) && !selected.has(item.id)
            ? { ...item, file: null, errorCode: 'SHARE_REMOVED' }
            : item,
        ),
      });
    }
  }
  private admitted(generation: number) {
    return (
      generation === this.generation && this.authenticated && this.verified && this.value.foreground
    );
  }
  async pull() {
    if (this.pulling) {
      this.again = true;
      return;
    }
    this.pulling = true;
    const generation = this.generation;
    try {
      await this.sessionWork;
      const pending = await this.port.getPendingShare();
      if (generation !== this.generation) return;
      if (pending.notice) this.publish({ notice: pending.notice });
      const batch = pending.batch;
      if (!batch || !this.admitted(generation)) return;
      if (this.value.state === 'ready') {
        if (this.value.batchId !== batch.id) {
          await this.port.cancelShare({ batchId: batch.id });
          this.publish({ notice: 'SHARE_BUSY' });
        }
        return;
      }
      if (batch.items.length > 9 || batch.items.some((item, index) => item.index !== index))
        throw new Error('Invalid bounded Share metadata');
      this.publish({ batchId: batch.id, state: 'reading', items: [] });
      if (batch.state === 'reading') return;
      let total = 0;
      const items: SharedImage[] = [];
      for (const item of batch.items) {
        if (!this.admitted(generation)) throw interrupted();
        let file: File | null = null;
        let errorCode = item.errorCode;
        if (item.state === 'ready') {
          try {
            if (
              item.index >= 8 ||
              !Number.isSafeInteger(item.byteCount) ||
              item.byteCount <= 0 ||
              item.byteCount > ITEM_BYTES ||
              !IMAGE_TYPES.has(item.mimeType ?? '') ||
              total + item.byteCount > BATCH_BYTES
            )
              throw new Error('Invalid Share bounds');
            total += item.byteCount;
            const parts: ArrayBuffer[] = [];
            for (let offset = 0; offset < item.byteCount;) {
              if (!this.admitted(generation)) throw interrupted();
              const length = Math.min(CHUNK_BYTES, item.byteCount - offset);
              const chunk = await this.port.readChunk({
                batchId: batch.id,
                itemId: item.id,
                offset,
                length,
              });
              if (!this.admitted(generation)) throw interrupted();
              if (chunk.data.length > Math.ceil(CHUNK_BYTES / 3) * 4)
                throw new Error('Oversized chunk');
              const bytes = Uint8Array.from(atob(chunk.data), (character) =>
                character.charCodeAt(0),
              );
              if (
                chunk.byteCount !== length ||
                bytes.length !== length ||
                chunk.eof !== (offset + length === item.byteCount)
              )
                throw new Error('Invalid chunk');
              parts.push(bytes.buffer);
              offset += length;
            }
            file = new File(parts, item.filename, { type: item.mimeType! });
          } catch (error) {
            if (
              !this.admitted(generation) ||
              (error instanceof DOMException && error.name === 'AbortError')
            )
              throw interrupted();
            errorCode = 'SHARE_TRANSFER_FAILED';
          }
        } else if (!errorCode) errorCode = 'SHARE_TRANSFER_FAILED';
        items.push({ id: item.id, index: item.index, filename: item.filename, file, errorCode });
      }
      if (!this.admitted(generation)) throw interrupted();
      // Native retains its bounded process-memory snapshot until clear/logout,
      // so a recreated document can recover the same original bytes and identity.
      this.publish({
        state: 'ready',
        items,
        queueContext: batch.queueContext ?? null,
        reviewContext: batch.reviewContext ?? null,
      });
      await this.port.acknowledgeShare({ batchId: batch.id });
    } catch (error) {
      if (
        generation === this.generation &&
        !(error instanceof DOMException && error.name === 'AbortError')
      )
        if (this.value.state === 'ready') this.publish({ notice: 'SHARE_ACK_UNCONFIRMED' });
        else this.publish({ state: 'idle', batchId: null, items: [], notice: 'SHARE_UNAVAILABLE' });
    } finally {
      this.pulling = false;
      if (this.again) {
        this.again = false;
        void this.pull();
      }
    }
  }
}

let port: NativeSharePort | undefined;
let intake: NativeShareIntake | undefined;
let boundaries = 0;
const idle: NativeShareSnapshot = {
  batchId: null,
  state: 'idle',
  items: [],
  notice: null,
  foreground: true,
  verified: true,
  queueContext: null,
  reviewContext: null,
};
function nativeIntake() {
  if (!Capacitor.isNativePlatform()) return null;
  port ??= registerPlugin<NativeSharePort>('BrickVaultShare');
  intake ??= new NativeShareIntake(port);
  return intake;
}
export const nativeShareSnapshot = () => intake?.snapshot() ?? idle;
export const subscribeNativeShare = (listener: () => void) =>
  nativeIntake()?.subscribe(listener) ?? (() => {});
export const setNativeShareAuthenticated = (authenticated: boolean) =>
  nativeIntake()?.setAuthenticated(authenticated);
// Native onPause invalidates admission. A successful passive recheck must explicitly
// re-authorize the bridge; visibility alone never resumes URI/chunk reads.
export const setNativeShareVerified = (verified: boolean) => {
  const service = nativeIntake();
  if (verified) service?.setAuthenticated(true);
  else service?.setVerified(false);
};
export const cancelNativeShare = () => nativeIntake()?.cancel() ?? Promise.resolve();
export const saveNativeShareUploadContext = (context: NativeShareQueueContext) => {
  const service = nativeIntake();
  return service
    ? service.saveUploadContext(context)
    : Promise.reject(new Error('Native Share unavailable'));
};
export const saveNativeShareReviewContext = (context: NativeShareReviewContext) => {
  const service = nativeIntake();
  return service
    ? service.saveReviewContext(context)
    : Promise.reject(new Error('Native Share unavailable'));
};

export function initializeNativeShare() {
  const service = nativeIntake();
  if (!service || !port) return () => {};
  boundaries++;
  let disposed = false;
  let nativeActive = true;
  const handles: PluginListenerHandle[] = [];
  const register = (promise: Promise<PluginListenerHandle>) => {
    void promise.then(
      (handle) => {
        if (disposed) void handle.remove();
        else handles.push(handle);
      },
      () => {
        if (!disposed) service.setVerified(false);
      },
    );
  };
  register(
    port.addListener('shareAvailable', () => {
      if (!disposed) void service.pull();
    }),
  );
  register(
    App.addListener('appStateChange', ({ isActive }) => {
      nativeActive = isActive;
      if (!disposed) service.setForeground(nativeActive && document.visibilityState !== 'hidden');
    }),
  );
  const visibility = () =>
    service.setForeground(nativeActive && document.visibilityState !== 'hidden');
  document.addEventListener('visibilitychange', visibility);
  // Pulling before session outcome reads only neutral metadata/notice; native retains cold URIs.
  void service.pull();
  return () => {
    disposed = true;
    document.removeEventListener('visibilitychange', visibility);
    handles.forEach((handle) => {
      void handle.remove();
    });
    boundaries--;
    // StrictMode performs setup/cleanup/setup before the initial session outcome.
    // Clear on a real boundary removal, without discarding a legitimate cold Share.
    void Promise.resolve().then(() => {
      if (boundaries === 0) service.detach();
    });
  };
}
