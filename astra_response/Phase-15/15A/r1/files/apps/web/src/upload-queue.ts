import { uploadImage, uploadFailure } from './listings-api';
import type { PrivacyElevation, UploadResult } from './listings-api';

export type QueueItem = {
  id: string;
  file: File;
  order: number;
  state: 'queued' | 'uploading' | UploadResult['status'];
  result: UploadResult | null;
  privacyElevation?: PrivacyElevation;
};
type Sender = typeof uploadImage;

/** Document-memory queue. Selection owns identity/order; completion never reallocates. */
export class UploadQueue {
  private items: QueueItem[] = [];
  private listeners = new Set<() => void>();
  private next = 0;
  private active = 0;
  private enabled = true;
  private disposed = false;
  private controller = new AbortController();
  constructor(
    private listing: string,
    private onSuccess: () => void,
    private send: Sender = uploadImage,
    private dispatchAllowed: () => boolean = () => true,
  ) {}
  snapshot = () => this.items;
  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
  nextPosition = () => this.next;
  refreshPositions(serverNext: number) {
    this.next = Math.max(this.next, serverNext);
    this.emit();
  }
  select(files: File[], serverNext: number, privacyElevation?: PrivacyElevation) {
    if (this.disposed) return;
    this.next = Math.max(this.next, serverNext);
    if (this.next + files.length > 2147483647) throw new Error('No upload positions remain.');
    for (const file of files) {
      if (this.next > 2147483646) throw new Error('No upload positions remain.');
      this.items.push({
        id: crypto.randomUUID(),
        file,
        order: this.next++,
        state: 'queued',
        result: null,
        privacyElevation,
      });
    }
    this.emit();
    this.pump();
  }
  retry(id: string) {
    const item = this.items.find((v) => v.id === id);
    if (
      !item ||
      item.state !== 'failed' ||
      this.disposed ||
      ['DISPLAY_ORDER_CONFLICT', 'UPLOAD_ID_CONFLICT'].includes(item.result?.error?.code ?? '')
    )
      return;
    item.state = 'queued';
    item.result = null;
    this.emit();
    this.pump();
  }
  restore(
    items: { id: string; file: File; order: number }[],
    serverNext: number,
    privacyElevation?: PrivacyElevation,
  ) {
    if (this.disposed || this.items.length || items.length > 8)
      throw new Error('The saved live queue cannot be restored.');
    const ids = new Set<string>();
    const orders = new Set<number>();
    for (const item of items) {
      if (
        !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(item.id) ||
        !Number.isInteger(item.order) ||
        item.order < 0 ||
        item.order > 2147483646 ||
        ids.has(item.id) ||
        orders.has(item.order)
      )
        throw new Error('The saved live queue has invalid identities or positions.');
      ids.add(item.id);
      orders.add(item.order);
    }
    this.next = Math.max(serverNext, ...items.map((item) => item.order + 1));
    this.items = items.map((item) => ({
      ...item,
      state: 'failed',
      result: uploadFailure(item.id, item.file.name, 'TRANSPORT_ERROR'),
      privacyElevation,
    }));
    this.emit();
    // Prior responses are uncertain after document recreation. Explicit retry
    // recovers the same server receipt; restoration never starts HTTP writes.
  }
  remove(id: string) {
    this.items = this.items.filter((v) => v.id !== id || v.state !== 'failed');
    this.emit();
  }
  setEnabled(enabled: boolean) {
    this.enabled = enabled;
    this.pump();
  }
  dispose() {
    this.disposed = true;
    this.controller.abort();
    this.items = [];
    this.emit();
    this.listeners.clear();
  }
  private emit() {
    this.items = [...this.items];
    for (const listener of this.listeners) listener();
  }
  private pump() {
    if (this.disposed || !this.enabled || !this.dispatchAllowed()) return;
    while (this.active < 2) {
      if (!this.enabled || !this.dispatchAllowed()) return;
      const item = this.items.find((v) => v.state === 'queued');
      if (!item) return;
      item.state = 'uploading';
      this.active++;
      this.emit();
      void this.dispatch(item);
    }
  }
  private async dispatch(item: QueueItem) {
    let result: UploadResult;
    try {
      result = await this.send(
        this.listing,
        item.file,
        item.id,
        item.order,
        this.controller.signal,
        item.privacyElevation,
      );
    } catch {
      result = uploadFailure(item.id, item.file.name, 'TRANSPORT_ERROR');
    }
    this.active--;
    if (this.disposed) return;
    item.result = result;
    item.state = result.status;
    this.emit();
    if (result.status !== 'failed') this.onSuccess();
    this.pump();
  }
}
