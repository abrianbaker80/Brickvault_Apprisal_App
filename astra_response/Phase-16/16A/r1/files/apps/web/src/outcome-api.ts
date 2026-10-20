import createClient from 'openapi-fetch';
import type { components, paths } from '@brickvault/contracts';
import { sessionFetch } from './session-client';

export type OutcomeActuals = components['schemas']['OutcomeActuals'];
export type OutcomeAppend = components['schemas']['OutcomeAppend'];
export type OutcomeEntry = components['schemas']['OutcomeEntry'];
export type OutcomeResponse = components['schemas']['OutcomeResponse'];
export type OutcomeMetric = components['schemas']['OutcomeComparisonMetric'];

export class OutcomeRequestError extends Error {
  constructor(
    readonly status: number,
    readonly code: string | null,
  ) {
    super(
      status === 409
        ? 'This outcome changed or the submission identity was reused. Reload before correcting.'
        : status === 404
          ? 'Saved deal or outcome entry not found.'
          : status === 422
            ? 'Check the entered outcome facts, dates, amounts and correction reason.'
            : 'Outcome service is unavailable. No write result is assumed.',
    );
  }
}
const client = () => createClient<paths>({ fetch: sessionFetch });
const options = (signal: AbortSignal) => ({
  signal,
  cache: 'no-store' as const,
  redirect: 'error' as const,
});
function fail(status: number, error: unknown): never {
  const code = (error as { error?: { code?: string } } | undefined)?.error?.code ?? null;
  throw new OutcomeRequestError(status, code);
}
export async function getOutcome(
  id: string,
  signal: AbortSignal,
  before?: number,
): Promise<OutcomeResponse> {
  const { data, error, response } = await client().GET('/api/deal-forecasts/{identifier}/outcome', {
    ...options(signal),
    params: {
      path: { identifier: id },
      query: before === undefined ? {} : { before_revision: before },
    },
  });
  if (!data) fail(response.status, error);
  return data;
}
export async function appendOutcome(
  id: string,
  body: OutcomeAppend,
  signal: AbortSignal,
): Promise<OutcomeEntry> {
  const { data, error, response } = await client().POST(
    '/api/deal-forecasts/{identifier}/outcome',
    {
      ...options(signal),
      params: { path: { identifier: id } },
      body,
    },
  );
  if (!data) fail(response.status, error);
  if (data.id !== body.id || data.revision !== body.expected_revision + 1)
    throw new Error('Uncertain outcome identity');
  return data;
}
export async function getOutcomeEntry(
  id: string,
  entry: string,
  signal: AbortSignal,
): Promise<OutcomeEntry> {
  const { data, error, response } = await client().GET(
    '/api/deal-forecasts/{identifier}/outcome/entries/{entry_id}',
    {
      ...options(signal),
      params: { path: { identifier: id, entry_id: entry } },
    },
  );
  if (!data) fail(response.status, error);
  if (data.id !== entry) throw new Error('Unexpected outcome identity');
  return data;
}
