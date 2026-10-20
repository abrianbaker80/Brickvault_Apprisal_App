import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { OutcomeSection } from './OutcomeSection';
import * as api from './outcome-api';
import type { OutcomeActuals, OutcomeEntry, OutcomeResponse, OutcomeMetric } from './outcome-api';
import { clearPrivateViews, startPrivateSession, transition } from './private-views';

vi.mock('./outcome-api', async (load) => ({
  ...(await load<typeof import('./outcome-api')>()),
  getOutcome: vi.fn(),
  appendOutcome: vi.fn(),
  getOutcomeEntry: vi.fn(),
}));
const root = '11111111-1111-4111-8111-111111111111';
const entryId = (n: number) => `22222222-2222-4222-8222-${String(n).padStart(12, '0')}`;
const empty: OutcomeResponse = {
  root_forecast_id: root,
  state: 'NOT_RECORDED',
  latest: null,
  history: [],
  next_before_revision: null,
};
function entry(revision = 1, actuals?: OutcomeActuals, id = entryId(revision)): OutcomeEntry {
  const unknown = { amount: null, reasons: ['purchase_price'] };
  const metric: OutcomeMetric = {
    state: 'UNAVAILABLE',
    actual_amount: null,
    expected_amount: null,
    reasons: ['ORIGINAL_VALUE_UNAVAILABLE'],
  };
  return {
    id,
    root_forecast_id: root,
    revision,
    recorded_at: '2026-10-20T10:00:00Z',
    correction_reason: revision > 1 ? 'Corrected actual price' : null,
    actuals: actuals ?? {
      purchase_decision: 'BOUGHT',
      currency: 'USD',
      contents_state: 'NOT_CHECKED',
      sale_status: 'NOT_SOLD',
      purchase_price: '100.00',
    },
    results: {
      calculation_version: 'outcome-calculation-v1',
      rounding_version: 'whole-set-usd-rounding-v1',
      currency: 'USD',
      state: 'NOT_SOLD',
      gross: unknown,
      selling_costs: unknown,
      net: unknown,
      acquisition: unknown,
      profit: unknown,
      days_to_sell: null,
      duration_reasons: ['SALE_NOT_COMPLETE'],
      missing_fields: ['purchase_price'],
      unpaid_own_labor_excluded: true,
      comparison: {
        original_id: root,
        original_created_at: '2026-09-12T12:00:00Z',
        meaning: 'UNAVAILABLE',
        sale: metric,
        net: metric,
        profit: metric,
      },
    },
  };
}
function recorded(value: OutcomeEntry): OutcomeResponse {
  return {
    ...empty,
    state: 'RECORDED',
    latest: value,
    history: [
      {
        id: value.id,
        revision: value.revision,
        recorded_at: value.recorded_at,
        correction_reason: value.correction_reason,
        purchase_decision: value.actuals.purchase_decision,
        sale_status: value.actuals.sale_status ?? null,
      },
    ],
  };
}
async function open() {
  render(<OutcomeSection id={root} />);
  await screen.findByRole('button', { name: /Record outcome|Correct entry/u });
}
function price(value: string) {
  fireEvent.change(screen.getByLabelText('Actual purchase price (USD)'), { target: { value } });
}

beforeEach(() => {
  vi.resetAllMocks();
  startPrivateSession('synthetic-owner', Date.now() + 600000);
  vi.mocked(api.getOutcome).mockResolvedValue(empty);
  vi.mocked(api.appendOutcome).mockImplementation((_id, body) =>
    Promise.resolve(entry(body.expected_revision + 1, body.actuals, body.id)),
  );
});

describe('Actual outcomes', () => {
  it('saves only explicitly, distinguishing unknown from a deliberate zero', async () => {
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Record outcome' }));
    expect(screen.getByLabelText('Actual purchase price (USD)')).toHaveValue('');
    expect(screen.getByLabelText('Inspected contents', { exact: true })).toHaveValue('NOT_CHECKED');
    expect(screen.getByLabelText('Sale status', { exact: true })).toHaveValue('NOT_SOLD');
    expect(api.appendOutcome).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Set actual purchase price to zero' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save outcome' }));
    await screen.findByText('Outcome revision 1 saved. Original forecast unchanged.');
    const body = vi.mocked(api.appendOutcome).mock.calls[0]![1];
    expect(body.expected_revision).toBe(0);
    expect(body.actuals.purchase_price).toBe('0');
    expect(body.actuals.shipping_paid ?? null).toBeNull();
    expect(body.actuals.forecast_preceded_purchase ?? null).toBeNull();
    expect(body).not.toHaveProperty('results');
    expect(api.appendOutcome).toHaveBeenCalledTimes(1);
  });

  it('appends a correction and opens exact prior history without changing the baseline', async () => {
    const first = entry();
    vi.mocked(api.getOutcome).mockResolvedValue(recorded(first));
    vi.mocked(api.getOutcomeEntry).mockResolvedValue(first);
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Correct entry' }));
    price('125.00');
    expect(screen.getByLabelText('Correction reason')).toBeRequired();
    fireEvent.change(screen.getByLabelText('Correction reason'), {
      target: { value: 'Receipt correction' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Save correction' }));
    await screen.findByText('Outcome revision 2 saved. Original forecast unchanged.');
    const body = vi.mocked(api.appendOutcome).mock.calls[0]![1];
    expect(body.expected_revision).toBe(1);
    expect(body.correction_reason).toBe('Receipt correction');
    expect(body.actuals.purchase_price).toBe('125.00');
    fireEvent.click(screen.getByText('Outcome history', { selector: 'summary' }));
    fireEvent.click(screen.getByRole('button', { name: 'View outcome revision 1' }));
    const old = await screen.findByRole('region', { name: 'Historical actual outcome' });
    fireEvent.click(within(old).getByText('Recorded facts', { selector: 'summary' }));
    expect(within(old).getByText('100.00')).toBeVisible();
    expect(api.getOutcomeEntry).toHaveBeenCalledWith(root, first.id, expect.any(AbortSignal));
    expect(screen.getByText(`Comparison baseline: original ${root}.`)).toBeVisible();
  });

  it('recovers a committed exact submission without sending a second write', async () => {
    vi.mocked(api.appendOutcome).mockRejectedValue(new TypeError('transport interruption'));
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Record outcome' }));
    price('100');
    fireEvent.click(screen.getByRole('button', { name: 'Save outcome' }));
    await screen.findByText(/Save status is uncertain/u);
    const body = vi.mocked(api.appendOutcome).mock.calls[0]![1];
    vi.mocked(api.getOutcomeEntry).mockResolvedValue(entry(1, body.actuals, body.id));
    vi.mocked(api.getOutcome).mockResolvedValue(recorded(entry(2)));
    expect(screen.getByLabelText('Actual purchase price (USD)')).toBeDisabled();
    expect(screen.queryByRole('button', { name: 'Retry same submission' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Check submission status' }));
    await screen.findByRole('heading', { name: 'Recorded outcome · revision 2' });
    expect(api.appendOutcome).toHaveBeenCalledTimes(1);
  });

  it('requires exact not-found recovery before an explicit identical-ID retry', async () => {
    vi.mocked(api.appendOutcome).mockRejectedValueOnce(new TypeError('lost response'));
    vi.mocked(api.getOutcomeEntry).mockRejectedValue(
      new api.OutcomeRequestError(404, 'OUTCOME_NOT_FOUND'),
    );
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Record outcome' }));
    price('95');
    fireEvent.click(screen.getByRole('button', { name: 'Save outcome' }));
    await screen.findByText(/Save status is uncertain/u);
    const body = vi.mocked(api.appendOutcome).mock.calls[0]![1];
    fireEvent.click(screen.getByRole('button', { name: 'Check submission status' }));
    const retry = await screen.findByRole('button', { name: 'Retry same submission' });
    expect(api.appendOutcome).toHaveBeenCalledTimes(1);
    fireEvent.click(retry);
    await screen.findByText('Outcome revision 1 saved. Original forecast unchanged.');
    expect(vi.mocked(api.appendOutcome).mock.calls[1]![1]).toEqual(body);
  });

  it('retains a conflicting draft and requires deliberate reload and Save', async () => {
    vi.mocked(api.getOutcome).mockResolvedValue(recorded(entry()));
    vi.mocked(api.appendOutcome).mockRejectedValueOnce(
      new api.OutcomeRequestError(409, 'OUTCOME_CONFLICT'),
    );
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Correct entry' }));
    price('90');
    fireEvent.change(screen.getByLabelText('Correction reason'), {
      target: { value: 'Actual receipt' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Save correction' }));
    await screen.findByRole('button', { name: 'Reload latest outcome' });
    expect(screen.getByLabelText('Actual purchase price (USD)')).toHaveValue('90');
    expect(screen.getByRole('button', { name: 'Save correction' })).toBeDisabled();
    vi.mocked(api.getOutcome).mockResolvedValue(recorded(entry(2)));
    fireEvent.click(screen.getByRole('button', { name: 'Reload latest outcome' }));
    await screen.findByText(/Review your retained draft/u);
    expect(screen.getByLabelText('Actual purchase price (USD)')).toHaveValue('90');
    expect(api.appendOutcome).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole('button', { name: 'Save correction' }));
    await screen.findByText('Outcome revision 3 saved. Original forecast unchanged.');
    expect(vi.mocked(api.appendOutcome).mock.calls[1]![1].expected_revision).toBe(2);
  });

  it('does not send offline and clears drafts/pending responses when the session locks', async () => {
    let resolve!: (value: OutcomeEntry) => void;
    vi.mocked(api.appendOutcome).mockImplementation(
      () =>
        new Promise((done) => {
          resolve = done;
        }),
    );
    await open();
    fireEvent.click(screen.getByRole('button', { name: 'Record outcome' }));
    price('100');
    act(() => transition('OFFLINE_CACHED'));
    expect(screen.queryByRole('button', { name: 'Save outcome' })).not.toBeInTheDocument();
    expect(api.appendOutcome).not.toHaveBeenCalled();
    act(() => transition('ONLINE_VERIFIED'));
    fireEvent.click(screen.getByRole('button', { name: 'Save outcome' }));
    await waitFor(() => expect(api.appendOutcome).toHaveBeenCalledTimes(1));
    act(() => clearPrivateViews());
    await act(async () => {
      resolve(entry());
      await Promise.resolve();
    });
    expect(screen.queryByRole('form', { name: 'Actual outcome form' })).not.toBeInTheDocument();
    expect(screen.queryByText(/revision 1 saved/u)).not.toBeInTheDocument();
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
  });
});
