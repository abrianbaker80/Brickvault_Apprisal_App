import createClient from 'openapi-fetch';
import type { components, paths } from '@brickvault/contracts';
import { sessionFetch } from './session-client';

export type Listing = components['schemas']['ListingResponse'];
export type ListingDetail = components['schemas']['ListingDetail'];
export type ListingCreate = components['schemas']['ListingCreate'];
export type UploadResult = components['schemas']['UploadResult'];
export type PrivacyElevation =
  paths['/api/listings/{listing_id}/images']['post']['requestBody']['content']['multipart/form-data']['privacy_elevation'];
const client = () => createClient<paths>({ fetch: sessionFetch });

export class ListingRequestError extends Error {
  constructor(
    message: string,
    readonly uncertain = false,
  ) {
    super(message);
  }
}
const options = (signal: AbortSignal) => ({ signal, cache: 'no-store' as const });
export function uploadFailure(id: string, filename: string, code: string): UploadResult {
  const message =
    code === 'DISPLAY_ORDER_CONFLICT'
      ? 'Another upload claimed this position. Refresh positions, remove this failed item, then select it again.'
      : code === 'UPLOAD_ID_CONFLICT'
        ? 'This upload identity conflicts with a saved submission. Remove it and select the file again.'
        : code === 'REQUEST_TOO_LARGE' || code === 'IMAGE_TOO_LARGE'
          ? 'The image exceeds the upload limits (25 MiB, 40 megapixels, 16,000 pixels per side).'
          : code === 'TRANSPORT_ERROR'
            ? 'The result was not confirmed. Retry this same file to recover its saved result.'
            : 'This image could not be uploaded. Use a valid single-frame JPEG, PNG or WebP, or retry when the service is available.';
  return {
    client_upload_id: id,
    filename,
    status: 'failed',
    listing_image_id: null,
    error: { code, message },
  };
}

function check<T>({ data, response }: { data?: T; response: Response }): T {
  if (data !== undefined) return data;
  throw new ListingRequestError(
    response.status === 422
      ? 'Check the URL, currency and asking price. Your entered values are retained.'
      : response.status === 404
        ? 'Listing not found.'
        : 'The listing request could not be completed. Refresh to check the saved state.',
    response.status >= 500,
  );
}
export async function listingList(offset: number, signal: AbortSignal) {
  return check(
    await client().GET('/api/listings', {
      ...options(signal),
      params: { query: { offset, limit: 12 } },
    }),
  );
}
export async function listingDetail(id: string, signal: AbortSignal) {
  return check(
    await client().GET('/api/listings/{listing_id}', {
      ...options(signal),
      params: { path: { listing_id: id } },
    }),
  );
}
export async function createListing(body: ListingCreate, signal: AbortSignal) {
  return check(await client().POST('/api/listings', { ...options(signal), body }));
}
export async function uploadImage(
  listingId: string,
  file: File,
  id: string,
  order: number,
  signal: AbortSignal,
  privacyElevation?: PrivacyElevation,
): Promise<UploadResult> {
  try {
    const result = await client().POST('/api/listings/{listing_id}/images', {
      ...options(signal),
      params: { path: { listing_id: listingId } },
      body: {
        file: '',
        client_upload_id: id,
        display_order: order,
        ...(privacyElevation ? { privacy_elevation: privacyElevation } : {}),
      },
      bodySerializer: () => {
        const form = new FormData();
        form.append('file', file, file.name);
        form.append('client_upload_id', id);
        form.append('display_order', String(order));
        if (privacyElevation) form.append('privacy_elevation', privacyElevation);
        return form;
      },
    });
    if (result.data && result.data.status !== 'failed') return result.data;
    const error: unknown = result.error ?? result.data;
    const problem = error as { error?: { code?: string } } | undefined;
    return uploadFailure(id, file.name, problem?.error?.code ?? `HTTP_${result.response.status}`);
  } catch {
    return uploadFailure(id, file.name, 'TRANSPORT_ERROR');
  }
}
export async function imageContent(id: string, signal: AbortSignal): Promise<Blob> {
  return check(
    await client().GET('/api/images/{asset_id}/content', {
      ...options(signal),
      params: { path: { asset_id: id } },
      parseAs: 'blob',
    }),
  );
}
