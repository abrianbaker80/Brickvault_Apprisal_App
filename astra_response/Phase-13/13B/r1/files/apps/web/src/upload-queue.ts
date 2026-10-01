import { uploadImage, uploadFailure } from './listings-api';
import type { UploadResult } from './listings-api';

export type QueueItem = {
  id: string;
  file: File;
  order: number;
  state: 'queued' | 'uploading' | UploadResult['status'];
  result: UploadResult | null;
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
  select(files: File[], serverNext: number) {
    if (this.disposed) return;
    this.next = Math.max(this.next, serverNext);
    for (const file of files) {
      if (this.next > 2147483646) throw new Error('No upload positions remain.');
      this.items.push({
        id: crypto.randomUUID(),
        file,
        order: this.next++,
        state: 'queued',
        result: null,
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
    this.listeners.clear();
  }
  private emit() {
    this.items = [...this.items];
    for (const listener of this.listeners) listener();
  }
  private pump() {
    if (this.disposed || !this.enabled) return;
    while (this.active < 2) {
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
