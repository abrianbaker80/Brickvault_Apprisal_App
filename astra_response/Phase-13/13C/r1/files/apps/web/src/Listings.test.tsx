import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import App from './App';
import { ListingDetailPage } from './ListingsPage';
import * as api from './listings-api';
import type { ListingDetail, UploadResult } from './listings-api';
import { UploadQueue } from './upload-queue';
import { configureSession } from './session-client';

const id = '11111111-1111-4111-8111-111111111111';
const detail: ListingDetail = {
  id,
  title: 'Private find',
  description: 'Three photos',
  source_type: 'manual',
  source_url: null,
  asking_price: '0.00',
  currency: 'USD',
  created_at: '2026-10-01T00:00:00Z',
  updated_at: '2026-10-01T00:00:00Z',
  images: [],
  next_display_order: 0,
};
const file = (name: string) => new File(['same bytes'], name, { type: 'image/png' });
const success = (
  uploadId: string,
  filename: string,
  status: 'uploaded' | 'duplicate' = 'uploaded',
): UploadResult => ({
  client_upload_id: uploadId,
  filename,
  status,
  listing_image_id: id,
  error: null,
});
function deferred() {
  let resolve!: (value: UploadResult) => void;
  const promise = new Promise<UploadResult>((r) => {
    resolve = r;
  });
  return { promise, resolve };
}
beforeEach(() => {
  window.history.replaceState({}, '', '/listings');
  configureSession(
    null,
    () => {},
    () => {},
  );
});

it('creates through generated metadata and renders list/detail without treating zero as missing', async () => {
  vi.spyOn(api, 'listingList').mockResolvedValue({ items: [detail], next_offset: null });
  vi.spyOn(api, 'listingDetail').mockResolvedValue(detail);
  const create = vi.spyOn(api, 'createListing').mockResolvedValue(detail);
  render(<App />);
  expect(await screen.findByRole('heading', { name: 'Private find' })).toBeVisible();
  expect(screen.getByRole('link', { name: 'Marketplace Listings' })).toHaveAttribute(
    'aria-current',
    'page',
  );
  expect(screen.getByText(/Nothing publishes to Facebook, eBay, Poshmark/)).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Add Marketplace Listing' }));
  expect(screen.getByLabelText('Currency')).toHaveValue('USD');
  fireEvent.change(screen.getByLabelText('Title (optional)'), { target: { value: 'New listing' } });
  fireEvent.change(screen.getByLabelText('Asking price (optional)'), { target: { value: '0' } });
  fireEvent.click(screen.getByRole('button', { name: 'Save listing' }));
  await waitFor(() => expect(create).toHaveBeenCalled());
  expect(create.mock.calls[0]?.[0]).toMatchObject({
    title: 'New listing',
    asking_price: '0',
    currency: 'USD',
    source_url: null,
  });
  expect(await screen.findByRole('heading', { name: 'Photos · 0' })).toBeVisible();
  expect(screen.getByText('manual · USD 0.00')).toBeVisible();
});

it('assigns stable identities and positions on selection and never reuses failed/removed positions', async () => {
  const send = vi
    .fn<typeof api.uploadImage>()
    .mockImplementation((_listing, f, uuid) =>
      Promise.resolve(api.uploadFailure(uuid, f.name, 'INVALID_IMAGE')),
    );
  const queue = new UploadQueue(id, () => {}, send);
  queue.setEnabled(false);
  queue.select([file('a.png'), file('b.png')], 5);
  const before = queue.snapshot().map((v) => ({ id: v.id, order: v.order }));
  expect(before.map((v) => v.order)).toEqual([5, 6]);
  expect(new Set(before.map((v) => v.id)).size).toBe(2);
  queue.refreshPositions(0);
  queue.setEnabled(true);
  await waitFor(() => expect(queue.snapshot().every((v) => v.state === 'failed')).toBe(true));
  queue.remove(before[0]!.id);
  queue.select([file('c.png')], 1);
  expect(queue.snapshot().map((v) => v.order)).toEqual([6, 7]);
  expect(queue.nextPosition()).toBe(8);
  expect(queue.snapshot()[0]!.id).toBe(before[1]!.id);
  queue.dispose();
});

it('keeps at most two uploads in flight and starts the third only after a completion', async () => {
  const pending = [deferred(), deferred(), deferred()];
  const send = vi
    .fn<typeof api.uploadImage>()
    .mockImplementation(() => pending[send.mock.calls.length - 1]!.promise);
  const queue = new UploadQueue(id, () => {}, send);
  queue.select([file('a.png'), file('b.png'), file('c.png')], 0);
  expect(send).toHaveBeenCalledTimes(2);
  expect(queue.snapshot().map((v) => v.state)).toEqual(['uploading', 'uploading', 'queued']);
  pending[1]!.resolve(success(queue.snapshot()[1]!.id, 'b.png'));
  await waitFor(() => expect(send).toHaveBeenCalledTimes(3));
  expect(queue.snapshot().filter((v) => v.state === 'uploading')).toHaveLength(2);
  queue.dispose();
});

it('preserves successful/duplicate items during partial failure and retries only the same UUID/file/position', async () => {
  const done = vi.fn();
  let attempts = 0;
  const send = vi.fn<typeof api.uploadImage>().mockImplementation((_listing, f, uuid) => {
    if (f.name === 'b.png' && attempts++ === 0)
      return Promise.resolve(api.uploadFailure(uuid, f.name, 'TRANSPORT_ERROR'));
    return Promise.resolve(success(uuid, f.name, f.name === 'copy.png' ? 'duplicate' : 'uploaded'));
  });
  const queue = new UploadQueue(id, done, send);
  const b = file('b.png');
  queue.select([file('a.png'), b, file('copy.png')], 0);
  await waitFor(() =>
    expect(queue.snapshot().map((v) => v.state)).toEqual(['uploaded', 'failed', 'duplicate']),
  );
  const original = send.mock.calls[1]!;
  queue.retry(queue.snapshot()[1]!.id);
  await waitFor(() => expect(queue.snapshot()[1]!.state).toBe('uploaded'));
  expect(send).toHaveBeenCalledTimes(4);
  expect(send.mock.calls[3]!.slice(0, 4)).toEqual(original.slice(0, 4));
  expect(send.mock.calls[3]![1]).toBe(b);
  expect(done).toHaveBeenCalledTimes(3);
  queue.dispose();
});

it('blocks conflict retries and requires refresh/remove/reselect with a new identity above the high-water mark', async () => {
  const send = vi
    .fn<typeof api.uploadImage>()
    .mockImplementation((_listing, f, uuid, order) =>
      Promise.resolve(
        api.uploadFailure(
          uuid,
          f.name,
          order === 0 ? 'DISPLAY_ORDER_CONFLICT' : 'UPLOAD_ID_CONFLICT',
        ),
      ),
    );
  const queue = new UploadQueue(id, () => {}, send);
  queue.select([file('a.png'), file('b.png')], 0);
  await waitFor(() => expect(queue.snapshot().every((v) => v.state === 'failed')).toBe(true));
  const uuid = queue.snapshot()[0]!.id;
  for (const item of queue.snapshot()) queue.retry(item.id);
  expect(send).toHaveBeenCalledTimes(2);
  queue.refreshPositions(9);
  queue.remove(uuid);
  queue.select([file('a.png')], 9);
  expect(queue.snapshot().at(-1)?.order).toBe(9);
  expect(queue.snapshot().at(-1)?.id).not.toBe(uuid);
  queue.dispose();
});

it('normalizes early JSON and transport failures with known identity and sends actual multipart via the session client', async () => {
  const fetchMock = vi
    .fn<typeof fetch>()
    .mockResolvedValueOnce(
      new Response(JSON.stringify({ error: { code: 'DISPLAY_ORDER_CONFLICT' } }), {
        status: 409,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    .mockRejectedValueOnce(new TypeError('lost response'));
  vi.stubGlobal('fetch', fetchMock);
  configureSession(
    'csrf-test',
    () => {},
    () => {},
  );
  const f = file('a.png');
  const signal = new AbortController().signal;
  expect((await api.uploadImage(id, f, id, 4, signal)).error?.code).toBe('DISPLAY_ORDER_CONFLICT');
  const request = fetchMock.mock.calls[0]![0] as Request;
  expect(request.headers.get('X-CSRF-Token')).toBe('csrf-test');
  expect(request.headers.get('Content-Type')).toContain('multipart/form-data; boundary=');
  expect(request.credentials).toBe('same-origin');
  const multipart = await request.clone().text();
  expect(multipart).toContain('name="client_upload_id"');
  expect(multipart).toContain(id);
  expect(multipart).toContain('name="display_order"');
  // Native Node Request and jsdom File are different realms; real browser flows qualify file bytes.
  expect(multipart).toContain('name="file"');
  const failed = await api.uploadImage(id, f, id, 4, signal);
  expect(failed).toMatchObject({
    client_upload_id: id,
    filename: 'a.png',
    status: 'failed',
    error: { code: 'TRANSPORT_ERROR' },
  });
});

it('shows a readable conflict without a misleading retry, and lets Brian remove that failed queue item', async () => {
  vi.spyOn(api, 'listingDetail').mockResolvedValue(detail);
  vi.spyOn(api, 'uploadImage').mockImplementation((_listing, f, uuid) =>
    Promise.resolve(api.uploadFailure(uuid, f.name, 'DISPLAY_ORDER_CONFLICT')),
  );
  render(<ListingDetailPage id={id} />);
  await screen.findByRole('heading', { name: 'Photos · 0' });
  await act(async () => {
    fireEvent.change(screen.getByLabelText('Choose photos'), {
      target: { files: [file('conflict.png')] },
    });
    await Promise.resolve();
  });
  expect(await screen.findByText(/Another upload claimed this position/)).toBeVisible();
  expect(screen.queryByRole('button', { name: 'Retry conflict.png' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Remove failed conflict.png' }));
  expect(screen.getByText('Next available upload position: 1')).toBeVisible();
  expect(screen.queryByText('conflict.png')).not.toBeInTheDocument();
});
