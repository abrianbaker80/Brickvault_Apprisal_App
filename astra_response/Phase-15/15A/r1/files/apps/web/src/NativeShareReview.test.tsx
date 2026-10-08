import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { NativeShareReview } from './NativeShareReview';
import type { NativeShareSnapshot } from './native-share';
import * as api from './listings-api';
import type { ListingDetail } from './listings-api';
import { transition } from './private-views';

const shared = vi.hoisted(() => ({
  value: null as NativeShareSnapshot | null,
  listeners: new Set<() => void>(),
  cancel: vi.fn(),
  contextGate: null as Promise<void> | null,
  contexts: [] as import('./native-share').NativeShareQueueContext[],
}));
vi.mock('./native-share', () => ({
  nativeShareSnapshot: () => shared.value,
  subscribeNativeShare: (listener: () => void) => {
    shared.listeners.add(listener);
    return () => {
      shared.listeners.delete(listener);
    };
  },
  cancelNativeShare: () => {
    shared.cancel();
    shared.value = { ...shared.value!, batchId: null, state: 'idle', items: [] };
    shared.listeners.forEach((listener) => listener());
    return Promise.resolve();
  },
  saveNativeShareUploadContext: (context: import('./native-share').NativeShareQueueContext) => {
    shared.contexts.push(context);
    return (shared.contextGate ?? Promise.resolve()).then(() => {
      shared.value = {
        ...shared.value!,
        queueContext: context,
        reviewContext: {
          selectedItemIds: context.items.map((item) => item.itemId),
          creationUncertain: false,
        },
      };
      shared.listeners.forEach((listener) => listener());
    });
  },
  saveNativeShareReviewContext: (context: import('./native-share').NativeShareReviewContext) => {
    const bound = new Set(shared.value!.queueContext?.items.map((item) => item.itemId));
    shared.value = {
      ...shared.value!,
      reviewContext: context,
      items: shared.value!.items.map((item) =>
        bound.has(item.id) && !context.selectedItemIds.includes(item.id)
          ? { ...item, file: null, errorCode: 'SHARE_REMOVED' }
          : item,
      ),
    };
    shared.listeners.forEach((listener) => listener());
    return Promise.resolve();
  },
}));
const detail: ListingDetail = {
  id: 'listing',
  title: 'Photo-source listing',
  description: null,
  source_type: 'seller_photo',
  source_url: null,
  asking_price: null,
  currency: 'USD',
  created_at: '2026-10-07T00:00:00Z',
  updated_at: '2026-10-07T00:00:00Z',
  images: [],
  next_display_order: 5,
};
const originalUrl = URL;
const revoke = vi.fn();
beforeEach(() => {
  vi.restoreAllMocks();
  shared.cancel.mockClear();
  shared.contextGate = null;
  shared.contexts = [];
  revoke.mockClear();
  transition('ONLINE_VERIFIED');
  shared.value = {
    batchId: 'batch',
    state: 'ready',
    notice: null,
    foreground: true,
    verified: true,
    queueContext: null,
    reviewContext: null,
    items: [
      {
        id: 'one',
        index: 0,
        filename: 'shared-image-1.png',
        file: new File(['first original'], 'shared-image-1.png', { type: 'image/png' }),
        errorCode: null,
      },
      {
        id: 'two',
        index: 1,
        filename: 'shared-image-2.png',
        file: new File(['second original'], 'shared-image-2.png', { type: 'image/png' }),
        errorCode: null,
      },
      {
        id: 'bad',
        index: 2,
        filename: 'shared-image-3.bin',
        file: null,
        errorCode: 'URI_UNREADABLE',
      },
    ],
  };
  vi.stubGlobal(
    'URL',
    class extends originalUrl {
      static override createObjectURL = vi.fn(() => 'blob:synthetic-preview');
      static override revokeObjectURL = revoke;
    },
  );
  vi.spyOn(api, 'listingList').mockResolvedValue({ items: [detail], next_offset: null });
  vi.spyOn(api, 'listingDetail').mockResolvedValue(detail);
});

it('requires explicit review and existing destination before uploads, preserves order and elevated privacy, and releases previews on cancel', async () => {
  const create = vi.spyOn(api, 'createListing');
  const upload = vi.spyOn(api, 'uploadImage').mockImplementation((_listing, file, id) =>
    Promise.resolve({
      client_upload_id: id,
      filename: file.name,
      listing_image_id: 'relationship',
      status: 'uploaded',
      error: null,
    }),
  );
  const files = shared.value!.items.slice(0, 2).map((item) => item.file);
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  expect(create).not.toHaveBeenCalled();
  expect(upload).not.toHaveBeenCalled();
  expect(screen.getByText(/Source identity is unknown/)).toBeVisible();
  expect(screen.getByText(/access was unavailable or revoked/)).toBeVisible();
  fireEvent.change(screen.getByLabelText('Saved listing for shared images'), {
    target: { value: detail.id },
  });
  expect(upload).not.toHaveBeenCalled();
  fireEvent.click(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  );
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(2));
  expect(upload.mock.calls.map((call) => call[1])).toEqual(files);
  expect(upload.mock.calls.map((call) => call[3])).toEqual([5, 6]);
  expect(new Set(upload.mock.calls.map((call) => call[2])).size).toBe(2);
  expect(upload.mock.calls.every((call) => call[5] === 'restricted')).toBe(true);
  expect(create).not.toHaveBeenCalled();
  await waitFor(() => expect(revoke).toHaveBeenCalledTimes(2));
  fireEvent.click(screen.getByRole('button', { name: 'Clear this live Share queue' }));
  expect(shared.cancel).toHaveBeenCalledTimes(1);
  expect(screen.queryByRole('heading', { name: 'Review shared images' })).not.toBeInTheDocument();
});

it('creates a new optional listing only after explicit Save and keeps creation uncertainty out of blind retries', async () => {
  const create = vi.spyOn(api, 'createListing').mockImplementation(() => {
    expect(shared.value?.reviewContext).toEqual({
      selectedItemIds: ['one', 'two'],
      creationUncertain: true,
    });
    return Promise.reject(new TypeError('lost response'));
  });
  const upload = vi.spyOn(api, 'uploadImage');
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  fireEvent.change(screen.getByLabelText('Share destination'), { target: { value: 'new' } });
  expect(create).not.toHaveBeenCalled();
  fireEvent.change(screen.getByLabelText('Title (optional)'), {
    target: { value: 'Chosen new listing' },
  });
  fireEvent.click(
    screen.getByRole('button', { name: 'Save new listing and upload reviewed images' }),
  );
  await screen.findByText(/Listing creation was not confirmed/);
  expect(create).toHaveBeenCalledTimes(1);
  expect(create.mock.calls[0]![0]).toMatchObject({
    title: 'Chosen new listing',
    source_type: 'manual',
    currency: 'USD',
  });
  expect(
    screen.queryByRole('option', { name: 'Create a new Marketplace Listing' }),
  ).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Refresh saved listings' }));
  await waitFor(() => expect(api.listingList).toHaveBeenCalledTimes(3));
  expect(create).toHaveBeenCalledTimes(1);
  expect(upload).not.toHaveBeenCalled();
});

it('keeps Share selection independent and sends only explicitly included images', async () => {
  const upload = vi
    .spyOn(api, 'uploadImage')
    .mockImplementation((_listing, file, id) =>
      Promise.resolve(api.uploadFailure(id, file.name, 'TRANSPORT_ERROR')),
    );
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  fireEvent.click(screen.getByRole('checkbox', { name: 'Include image 1' }));
  await waitFor(() =>
    expect(screen.getByRole('checkbox', { name: 'Include image 1' })).not.toBeChecked(),
  );
  fireEvent.change(screen.getByLabelText('Saved listing for shared images'), {
    target: { value: detail.id },
  });
  fireEvent.click(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  );
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(1));
  const original = upload.mock.calls[0]!;
  expect(original[1]).toBe(shared.value!.items[1]!.file);
  expect(original[3]).toBe(5);
  fireEvent.click(await screen.findByRole('button', { name: 'Retry shared-image-2.png' }));
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(2));
  expect(upload.mock.calls[1]!.slice(0, 4)).toEqual(original.slice(0, 4));
  expect(upload.mock.calls[1]![5]).toBe('restricted');
});

it('disables saving in background or while verifying and clears unsaved previews when session expires', async () => {
  const upload = vi.spyOn(api, 'uploadImage');
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  act(() => {
    shared.value = { ...shared.value!, foreground: false, verified: false };
    shared.listeners.forEach((listener) => listener());
  });
  expect(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  ).toBeDisabled();
  act(() => {
    shared.value = { ...shared.value!, foreground: true };
    shared.listeners.forEach((listener) => listener());
  });
  expect(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  ).toBeDisabled();
  expect(upload).not.toHaveBeenCalled();
  act(() => {
    shared.value = {
      ...shared.value!,
      batchId: null,
      items: [],
      state: 'idle',
      notice: 'SIGN_IN_AND_RESHARE',
    };
    shared.listeners.forEach((listener) => listener());
  });
  expect(revoke).toHaveBeenCalledTimes(2);
  expect(screen.getByText(/No images are retained through sign-in/)).toBeVisible();
});

it('checkpoints the chosen destination and allocated identities before any HTTP upload dispatch', async () => {
  let release!: () => void;
  shared.contextGate = new Promise<void>((resolve) => {
    release = resolve;
  });
  const upload = vi
    .spyOn(api, 'uploadImage')
    .mockImplementation((_listing, file, id) =>
      Promise.resolve(api.uploadFailure(id, file.name, 'TRANSPORT_ERROR')),
    );
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  fireEvent.change(screen.getByLabelText('Saved listing for shared images'), {
    target: { value: detail.id },
  });
  fireEvent.click(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  );
  await screen.findByRole('button', { name: 'Confirm this live queue before uploading' });
  expect(shared.contexts).toHaveLength(1);
  expect(shared.contexts[0]!.listingId).toBe(detail.id);
  expect(shared.contexts[0]!.items.map((item) => [item.itemId, item.displayOrder])).toEqual([
    ['one', 5],
    ['two', 6],
  ]);
  expect(upload).not.toHaveBeenCalled();
  await act(() => {
    release();
    return Promise.resolve();
  });
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(2));
  expect(upload.mock.calls.map((call) => call[2])).toEqual(
    shared.contexts[0]!.items.map((item) => item.clientUploadId),
  );
});

it('restores a same-process queue after authenticated listing readback and retries only explicitly with the original identity', async () => {
  const id = '11111111-1111-4111-8111-111111111111';
  shared.value = {
    ...shared.value!,
    reviewContext: { selectedItemIds: ['two'], creationUncertain: false },
    queueContext: {
      listingId: detail.id,
      items: [{ itemId: 'two', clientUploadId: id, displayOrder: 7 }],
    },
  };
  const upload = vi
    .spyOn(api, 'uploadImage')
    .mockImplementation((_listing, file, uuid) =>
      Promise.resolve(api.uploadFailure(uuid, file.name, 'TRANSPORT_ERROR')),
    );
  const create = vi.spyOn(api, 'createListing');
  render(<NativeShareReview />);
  await screen.findByText(/Recovered this live process queue/);
  expect(api.listingDetail).toHaveBeenCalledWith(detail.id, expect.any(AbortSignal));
  expect(upload).not.toHaveBeenCalled();
  expect(create).not.toHaveBeenCalled();
  expect(screen.queryByText('shared-image-1.png')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Retry shared-image-2.png' }));
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(1));
  expect(upload.mock.calls[0]!.slice(0, 4)).toEqual([
    detail.id,
    shared.value.items[1]!.file,
    id,
    7,
  ]);
  expect(upload.mock.calls[0]![5]).toBe('restricted');
});

it('restores deselection and a creation-uncertain checkpoint without allowing another implicit or blind creation', async () => {
  shared.value = {
    ...shared.value!,
    reviewContext: { selectedItemIds: ['two'], creationUncertain: true },
  };
  const create = vi.spyOn(api, 'createListing');
  const upload = vi.spyOn(api, 'uploadImage');
  render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  expect(screen.getByRole('checkbox', { name: 'Include image 1' })).not.toBeChecked();
  expect(screen.getByRole('checkbox', { name: 'Include image 2' })).toBeChecked();
  expect(screen.getByRole('checkbox', { name: 'Include image 2' })).toBeDisabled();
  expect(
    screen.queryByRole('option', { name: 'Create a new Marketplace Listing' }),
  ).not.toBeInTheDocument();
  expect(screen.getByLabelText('Saved listing for shared images')).toHaveValue('');
  expect(create).not.toHaveBeenCalled();
  expect(upload).not.toHaveBeenCalled();
});

it('retires one failed image independently and restores only remaining immutable identities, including an empty retired queue', async () => {
  const upload = vi
    .spyOn(api, 'uploadImage')
    .mockImplementation((_listing, file, id) =>
      Promise.resolve(api.uploadFailure(id, file.name, 'DISPLAY_ORDER_CONFLICT')),
    );
  let view = render(<NativeShareReview />);
  await screen.findByRole('option', { name: /Photo-source listing/ });
  fireEvent.change(screen.getByLabelText('Saved listing for shared images'), {
    target: { value: detail.id },
  });
  fireEvent.click(
    screen.getByRole('button', { name: 'Upload reviewed images to selected listing' }),
  );
  fireEvent.click(await screen.findByRole('button', { name: 'Remove failed shared-image-1.png' }));
  await waitFor(() => expect(screen.queryByText('shared-image-1.png')).not.toBeInTheDocument());
  expect(shared.value!.items[0]!.file).toBeNull();
  expect(shared.value!.reviewContext?.selectedItemIds).toEqual(['two']);
  const context = shared.value!.queueContext!;
  expect(context.items).toHaveLength(2); // Immutable identity bindings remain; mask retires bytes.
  vi.mocked(api.listingDetail).mockResolvedValue({ ...detail, next_display_order: 0 });
  view.unmount();
  view = render(<NativeShareReview />);
  await screen.findByText(/Recovered this live process queue/);
  expect(screen.getByText('Next available upload position: 7')).toBeVisible();
  expect(upload).toHaveBeenCalledTimes(2);
  expect(screen.queryByText('shared-image-1.png')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Retry shared-image-2.png' }));
  await waitFor(() => expect(upload).toHaveBeenCalledTimes(3));
  expect(upload.mock.calls[2]![2]).toBe(context.items[1]!.clientUploadId);
  expect(upload.mock.calls[2]![3]).toBe(context.items[1]!.displayOrder);
  fireEvent.click(await screen.findByRole('button', { name: 'Remove failed shared-image-2.png' }));
  await waitFor(() => expect(screen.queryByText('shared-image-2.png')).not.toBeInTheDocument());
  expect(shared.value!.reviewContext?.selectedItemIds).toEqual([]);
  view.unmount();
  view = render(<NativeShareReview />);
  await screen.findByText(/Recovered this live process queue/);
  expect(screen.queryByRole('button', { name: /^Retry / })).not.toBeInTheDocument();
  expect(screen.queryByRole('button', { name: /^Remove failed / })).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Clear this live Share queue' })).toBeEnabled();
  expect(screen.getByText('Next available upload position: 7')).toBeVisible();
  expect(upload).toHaveBeenCalledTimes(3);
  view.unmount();
});
