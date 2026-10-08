import { waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { NativeShareIntake } from './native-share';
import type { NativeShareBatch, NativeSharePort } from './native-share';
import { UploadQueue } from './upload-queue';
import { uploadFailure } from './listings-api';
import type { uploadImage, UploadResult } from './listings-api';

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((done) => {
    resolve = done;
  });
  return { resolve, promise };
}
function fixture(bytes = Uint8Array.from([0, 255, 16, 32])) {
  let batch: NativeShareBatch | null = {
    id: 'batch',
    state: 'ready',
    items: [
      {
        id: 'item',
        index: 0,
        filename: 'shared-image-1.png',
        mimeType: 'image/png',
        byteCount: bytes.length,
        state: 'ready',
        errorCode: null,
      },
    ],
  };
  let notice: string | null = null;
  const port: NativeSharePort = {
    setSession: vi.fn<NativeSharePort['setSession']>(({ authenticated }) => {
      if (!authenticated) {
        batch = null;
        notice = 'SIGN_IN_AND_RESHARE';
      }
      return Promise.resolve();
    }),
    getPendingShare: vi.fn<NativeSharePort['getPendingShare']>(() =>
      Promise.resolve({ batch, notice }),
    ),
    readChunk: vi.fn<NativeSharePort['readChunk']>(({ offset, length }) =>
      Promise.resolve({
        data: btoa(
          Array.from(bytes.slice(offset, offset + length), (byte) =>
            String.fromCharCode(byte),
          ).join(''),
        ),
        byteCount: length,
        eof: offset + length === bytes.length,
      }),
    ),
    acknowledgeShare: vi.fn<NativeSharePort['acknowledgeShare']>(() => {
      return Promise.resolve();
    }),
    saveUploadContext: vi.fn<NativeSharePort['saveUploadContext']>(({ listingId, items }) => {
      if (batch)
        batch = {
          ...batch,
          queueContext: { listingId, items },
          reviewContext: {
            selectedItemIds: items.map((item) => item.itemId),
            creationUncertain: false,
          },
        };
      return Promise.resolve();
    }),
    saveReviewContext: vi.fn<NativeSharePort['saveReviewContext']>(
      ({ selectedItemIds, creationUncertain }) => {
        if (batch) batch = { ...batch, reviewContext: { selectedItemIds, creationUncertain } };
        return Promise.resolve();
      },
    ),
    cancelShare: vi.fn<NativeSharePort['cancelShare']>(() => {
      batch = null;
      return Promise.resolve();
    }),
    addListener: vi.fn<NativeSharePort['addListener']>(() =>
      Promise.resolve({ remove: () => Promise.resolve() }),
    ),
  };
  return {
    port,
    service: new NativeShareIntake(port),
    setBatch: (value: NativeShareBatch) => {
      batch = value;
    },
  };
}
function fileBytes(file: File) {
  return new Promise<Uint8Array>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(new Uint8Array(reader.result as ArrayBuffer));
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

it('keeps cold Share unread until the authentication outcome and transfers exact bytes sequentially in bounded chunks', async () => {
  const bytes = Uint8Array.from({ length: 262149 }, (_, index) => index % 256);
  const { port, service } = fixture(bytes);
  await service.pull();
  expect(port.readChunk).not.toHaveBeenCalled();
  expect(service.snapshot().items).toEqual([]);
  service.setAuthenticated(true);
  await waitFor(() => expect(service.snapshot().state).toBe('ready'));
  expect(vi.mocked(port.readChunk).mock.calls.map(([request]) => request.length)).toEqual([
    262144, 5,
  ]);
  expect(vi.mocked(port.readChunk).mock.calls.map(([request]) => request.offset)).toEqual([
    0, 262144,
  ]);
  expect(await fileBytes(service.snapshot().items[0]!.file!)).toEqual(bytes);
  expect(port.acknowledgeShare).toHaveBeenCalledWith({ batchId: 'batch' });
  await service.pull();
  expect(port.readChunk).toHaveBeenCalledTimes(2);
});

it('discards late chunks after backgrounding and requires verified session admission before hydration resumes', async () => {
  const { port, service } = fixture();
  const pending = deferred<Awaited<ReturnType<NativeSharePort['readChunk']>>>();
  vi.mocked(port.readChunk).mockReturnValueOnce(pending.promise);
  service.setAuthenticated(true);
  await waitFor(() => expect(port.readChunk).toHaveBeenCalledTimes(1));
  service.setForeground(false);
  pending.resolve({ data: 'AP8QIA==', byteCount: 4, eof: true });
  await service.pull();
  await waitFor(() => expect(service.snapshot().foreground).toBe(false));
  expect(service.snapshot().items).toEqual([]);
  expect(port.acknowledgeShare).not.toHaveBeenCalled();
  service.setForeground(true);
  await service.pull();
  expect(port.readChunk).toHaveBeenCalledTimes(1);
  service.setAuthenticated(true);
  await waitFor(() => expect(service.snapshot().state).toBe('ready'));
  expect(port.readChunk).toHaveBeenCalledTimes(2);
  expect(port.setSession).toHaveBeenLastCalledWith({ authenticated: true });
});

it('clears volatile images on logout and cannot promote an in-flight response to review after expiry', async () => {
  const { port, service } = fixture();
  const pending = deferred<Awaited<ReturnType<NativeSharePort['readChunk']>>>();
  vi.mocked(port.readChunk).mockReturnValueOnce(pending.promise);
  service.setAuthenticated(true);
  await waitFor(() => expect(port.readChunk).toHaveBeenCalled());
  service.setAuthenticated(false);
  pending.resolve({ data: 'AP8QIA==', byteCount: 4, eof: true });
  await waitFor(() => expect(service.snapshot().notice).toBe('SIGN_IN_AND_RESHARE'));
  expect(service.snapshot()).toMatchObject({
    batchId: null,
    state: 'idle',
    items: [],
    verified: false,
  });
  expect(port.acknowledgeShare).not.toHaveBeenCalled();
});

it('preserves successful entries and received order when another entry or bridge chunk fails', async () => {
  const { port, service, setBatch } = fixture();
  setBatch({
    id: 'batch',
    state: 'ready',
    items: [
      {
        id: 'a',
        index: 0,
        filename: 'shared-image-1.png',
        mimeType: 'image/png',
        byteCount: 4,
        state: 'ready',
        errorCode: null,
      },
      {
        id: 'bad',
        index: 1,
        filename: 'shared-image-2.bin',
        mimeType: null,
        byteCount: 0,
        state: 'failed',
        errorCode: 'URI_UNREADABLE',
      },
      {
        id: 'c',
        index: 2,
        filename: 'shared-image-3.png',
        mimeType: 'image/png',
        byteCount: 4,
        state: 'ready',
        errorCode: null,
      },
    ],
  });
  vi.mocked(port.readChunk)
    .mockResolvedValueOnce({ data: 'AP8QIA==', byteCount: 4, eof: true })
    .mockResolvedValueOnce({ data: 'AP8=', byteCount: 2, eof: true });
  service.setAuthenticated(true);
  await waitFor(() => expect(service.snapshot().state).toBe('ready'));
  expect(service.snapshot().items.map((item) => [item.index, item.errorCode, !!item.file])).toEqual(
    [
      [0, null, true],
      [1, 'URI_UNREADABLE', false],
      [2, 'SHARE_TRANSFER_FAILED', false],
    ],
  );
  expect(port.acknowledgeShare).toHaveBeenCalledTimes(1);
});

it('refuses oversized bridge metadata before reading bytes and refuses a new batch while review remains open', async () => {
  const { port, service, setBatch } = fixture();
  service.setAuthenticated(true);
  await waitFor(() => expect(service.snapshot().state).toBe('ready'));
  setBatch({ id: 'next', state: 'ready', items: [] });
  await service.pull();
  expect(service.snapshot().batchId).toBe('batch');
  expect(service.snapshot().notice).toBe('SHARE_BUSY');
  expect(port.cancelShare).toHaveBeenCalledWith({ batchId: 'next' });
  await service.cancel();
  expect(service.snapshot().items).toEqual([]);
  setBatch({
    id: 'huge',
    state: 'ready',
    items: Array.from({ length: 10 }, (_, index) => ({
      id: String(index),
      index,
      filename: 'shared.bin',
      mimeType: null,
      byteCount: 0,
      state: 'failed',
      errorCode: 'ITEM_COUNT_LIMIT',
    })),
  });
  await service.pull();
  expect(service.snapshot().notice).toBe('SHARE_UNAVAILABLE');
  expect(port.readChunk).toHaveBeenCalledTimes(1);
});

it('keeps restricted privacy, original File, UUID and order on uncertain retry, pauses dispatch, and releases queue references on disposal', async () => {
  const pending = deferred<UploadResult>();
  const send = vi
    .fn<typeof uploadImage>()
    .mockReturnValueOnce(pending.promise)
    .mockImplementation((_listing, file, id) =>
      Promise.resolve(uploadFailure(id, file.name, 'TRANSPORT_ERROR')),
    );
  const queue = new UploadQueue('listing', () => {}, send);
  const files = [new File(['a'], 'a.png'), new File(['b'], 'b.png'), new File(['c'], 'c.png')];
  queue.select(files, 7, 'restricted');
  expect(send).toHaveBeenCalledTimes(2);
  const first = queue.snapshot()[0]!;
  queue.setEnabled(false);
  pending.resolve(uploadFailure(first.id, first.file.name, 'TRANSPORT_ERROR'));
  await waitFor(() => expect(first.state).toBe('failed'));
  expect(send).toHaveBeenCalledTimes(2);
  queue.retry(first.id);
  expect(send).toHaveBeenCalledTimes(2);
  queue.setEnabled(true);
  await waitFor(() => expect(send).toHaveBeenCalledTimes(4));
  expect(send.mock.calls[2]!.slice(0, 4)).toEqual(send.mock.calls[0]!.slice(0, 4));
  expect(send.mock.calls[2]![1]).toBe(files[0]);
  expect(send.mock.calls.every((call) => call[5] === 'restricted')).toBe(true);
  queue.dispose();
  expect(queue.snapshot()).toEqual([]);
  expect(send.mock.calls[0]![4].aborted).toBe(true);
});

it('checks current admission synchronously when a request completes before React can apply its pause effect', async () => {
  let admitted = true;
  const pending = [deferred<UploadResult>(), deferred<UploadResult>(), deferred<UploadResult>()];
  const send = vi
    .fn<typeof uploadImage>()
    .mockImplementation(() => pending[send.mock.calls.length - 1]!.promise);
  const queue = new UploadQueue(
    'listing',
    () => {},
    send,
    () => admitted,
  );
  queue.select(
    [new File(['a'], 'a.png'), new File(['b'], 'b.png'), new File(['c'], 'c.png')],
    0,
    'restricted',
  );
  expect(send).toHaveBeenCalledTimes(2);
  admitted = false; // Native state changes; queue.setEnabled effect has not run yet.
  const first = queue.snapshot()[0]!;
  pending[0]!.resolve(uploadFailure(first.id, first.file.name, 'TRANSPORT_ERROR'));
  await waitFor(() => expect(first.state).toBe('failed'));
  expect(send).toHaveBeenCalledTimes(2);
  expect(queue.snapshot()[2]!.state).toBe('queued');
  admitted = true;
  queue.setEnabled(true);
  expect(send).toHaveBeenCalledTimes(3);
  queue.dispose();
});

it('rehydrates bounded originals and exact queue identity after same-process document detachment without automatic upload', async () => {
  const { port, service } = fixture();
  service.setAuthenticated(true);
  await waitFor(() => expect(service.snapshot().state).toBe('ready'));
  const selected = service.snapshot().items[0]!;
  await service.saveReviewContext({ selectedItemIds: [selected.id], creationUncertain: true });
  const id = crypto.randomUUID();
  await service.saveUploadContext({
    listingId: 'listing',
    items: [{ itemId: selected.id, clientUploadId: id, displayOrder: 7 }],
  });
  service.detach();
  expect(service.snapshot().items).toEqual([]);
  expect(port.setSession).not.toHaveBeenCalledWith({ authenticated: false });
  const recreated = new NativeShareIntake(port);
  await recreated.pull();
  expect(recreated.snapshot().items).toEqual([]);
  recreated.setAuthenticated(true);
  await waitFor(() => expect(recreated.snapshot().state).toBe('ready'));
  expect(recreated.snapshot().reviewContext).toEqual({
    selectedItemIds: [selected.id],
    creationUncertain: false,
  });
  const context = recreated.snapshot().queueContext!;
  expect(context).toEqual({
    listingId: 'listing',
    items: [{ itemId: selected.id, clientUploadId: id, displayOrder: 7 }],
  });
  const send = vi
    .fn<typeof uploadImage>()
    .mockImplementation((_listing, file, uuid) =>
      Promise.resolve(uploadFailure(uuid, file.name, 'TRANSPORT_ERROR')),
    );
  const queue = new UploadQueue(context.listingId, () => {}, send);
  const restoredFile = recreated.snapshot().items[0]!.file!;
  queue.restore([{ id, order: 7, file: restoredFile }], 14, 'restricted');
  expect(send).not.toHaveBeenCalled();
  expect(queue.snapshot()[0]).toMatchObject({
    id,
    order: 7,
    state: 'failed',
    result: { error: { code: 'TRANSPORT_ERROR' } },
  });
  expect(queue.nextPosition()).toBe(14);
  queue.retry(id);
  await waitFor(() => expect(send).toHaveBeenCalledTimes(1));
  expect(send.mock.calls[0]!.slice(0, 4)).toEqual(['listing', restoredFile, id, 7]);
  expect(send.mock.calls[0]![5]).toBe('restricted');
  expect(await fileBytes(restoredFile)).toEqual(await fileBytes(selected.file!));
  queue.dispose();
});

it('skips stale queued authenticated admission after backgrounding while ordered signed-out cleanup still executes', async () => {
  const { port, service } = fixture();
  const pending = deferred<void>();
  vi.mocked(port.setSession).mockReturnValueOnce(pending.promise);
  service.setAuthenticated(true);
  await waitFor(() => expect(port.setSession).toHaveBeenCalledTimes(1));
  service.setAuthenticated(true); // Queued behind the first bridge response.
  service.setForeground(false);
  pending.resolve();
  await service.pull();
  await waitFor(() => expect(service.snapshot().verified).toBe(false));
  expect(port.setSession).toHaveBeenCalledTimes(1);
  expect(port.readChunk).not.toHaveBeenCalled();
  service.setAuthenticated(false);
  await waitFor(() => expect(port.setSession).toHaveBeenLastCalledWith({ authenticated: false }));
  expect(service.snapshot().items).toEqual([]);
});
