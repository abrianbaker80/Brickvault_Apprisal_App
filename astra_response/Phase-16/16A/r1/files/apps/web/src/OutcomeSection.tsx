import { useEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useConnection } from './Connectivity';
import { connectionSnapshot, privateEpoch } from './private-views';
import { appendOutcome, getOutcome, getOutcomeEntry, OutcomeRequestError } from './outcome-api';
import type {
  OutcomeActuals,
  OutcomeAppend,
  OutcomeEntry,
  OutcomeMetric,
  OutcomeResponse,
} from './outcome-api';
import './outcomes.css';

const moneyFields = [
  ['purchase_price', 'Actual purchase price'],
  ['acquisition_extra_costs', 'Actual acquisition extras'],
  ['replacement_costs', 'Replacement costs'],
  ['labor_costs', 'Paid labor costs'],
  ['item_sale_proceeds', 'Item sale proceeds'],
  ['shipping_charged', 'Shipping received from buyer'],
  ['selling_fees', 'Selling fees'],
  ['shipping_paid', 'Shipping paid'],
  ['other_selling_costs', 'Other selling costs'],
] as const;
const labels: Record<string, string> = Object.fromEntries(moneyFields);
Object.assign(labels, {
  purchase_decision: 'Purchase decision',
  acquired_on: 'Acquisition date',
  currency: 'Currency',
  contents_state: 'Inspected contents',
  contents_checked_on: 'Inspection date',
  contents_note: 'Contents note',
  forecast_preceded_purchase: 'Original forecast preceded purchase',
  labor_minutes: 'Own labor minutes',
  sale_status: 'Sale status',
  sale_strategy: 'Sale strategy',
  sale_condition: 'Sale condition',
  sale_channel: 'Sale channel',
  sold_on: 'Final sale date',
});
const words = (value: string) => value.replaceAll('_', ' ').toLowerCase();
const money = (value: string | null | undefined) => (value == null ? 'Unknown' : `$${value} USD`);
const explain = (reasons: string[] | undefined) =>
  (reasons ?? []).map((r) => labels[r] ?? words(r)).join('; ');
const blank = (): OutcomeActuals => ({
  purchase_decision: 'BOUGHT',
  currency: 'USD',
  contents_state: 'NOT_CHECKED',
  sale_status: 'NOT_SOLD',
});

function Metric({ name, value }: { name: string; value: OutcomeMetric }) {
  return (
    <div className="outcome-metric">
      <h4>{name}</h4>
      <p>
        Actual: {money(value.actual_amount)} · Original: {money(value.expected_amount)}
      </p>
      {value.state === 'COMPARABLE' ? (
        <p>
          Actual minus original: <strong>{money(value.error_amount)}</strong>
        </p>
      ) : (
        <p>
          {words(value.state)}: {explain(value.reasons)}
        </p>
      )}
    </div>
  );
}

function OutcomeReadout({
  entry,
  historical = false,
}: {
  entry: OutcomeEntry;
  historical?: boolean;
}) {
  const result = entry.results;
  const comparison = result.comparison;
  return (
    <section
      className="outcome-readout"
      aria-label={historical ? 'Historical actual outcome' : 'Recorded actual outcome'}
    >
      <h3>
        {historical ? 'Historical' : 'Recorded'} outcome · revision {entry.revision}
      </h3>
      <p>
        {words(result.state)} · Recorded {new Date(entry.recorded_at).toLocaleString()}
      </p>
      {entry.correction_reason && <p>Correction: {entry.correction_reason}</p>}
      {result.state === 'PARTIALLY_SOLD' && (
        <p>Cumulative receipts and costs to date; this is not final profit.</p>
      )}
      <dl className="outcome-totals">
        {(
          [
            ['gross', 'Gross received'],
            ['selling_costs', 'Recorded selling/preparation costs'],
            ['net', 'Net after recorded selling/preparation costs'],
            ['acquisition', 'Total acquisition'],
            ['profit', 'Actual profit'],
          ] as const
        ).map(([key, label]) => (
          <div key={key}>
            <dt>{label}</dt>
            <dd>
              {money(result[key].amount)}
              {result[key].amount == null && <small>{explain(result[key].reasons)}</small>}
            </dd>
          </div>
        ))}
        <div>
          <dt>Days to sell</dt>
          <dd>
            {result.days_to_sell ?? 'Unknown'}
            {result.days_to_sell == null && <small>{explain(result.duration_reasons)}</small>}
          </dd>
        </div>
        <div>
          <dt>Own labor</dt>
          <dd>
            {entry.actuals.labor_minutes == null
              ? 'Unknown'
              : `${entry.actuals.labor_minutes} minutes`}
          </dd>
        </div>
      </dl>
      <p>Actual profit is after recorded monetary costs; unpaid own labor is excluded.</p>
      {!!result.missing_fields?.length && (
        <p>Incomplete facts: {explain(result.missing_fields)}.</p>
      )}
      <details>
        <summary>Recorded facts</summary>
        <dl className="outcome-totals">
          {Object.entries(labels).map(([key, label]) => {
            const value = entry.actuals[key as keyof OutcomeActuals];
            return (
              <div key={key}>
                <dt>{label}</dt>
                <dd>
                  {value == null
                    ? 'Unknown'
                    : typeof value === 'boolean'
                      ? value
                        ? 'Yes'
                        : 'No'
                      : String(value)}
                </dd>
              </div>
            );
          })}
        </dl>
      </details>
      <details className="outcome-comparison">
        <summary>Comparison with original forecast</summary>
        <p>
          Baseline: original {comparison.original_id}. Later forecast revisions do not replace it.
        </p>
        <p>
          {comparison.meaning === 'ASSUMPTION_COMPARISON'
            ? 'Manual assumption comparison, not provider forecast accuracy.'
            : words(comparison.meaning)}
        </p>
        <p>
          Acquisition basis: actual {money(comparison.actual_acquisition)}; original{' '}
          {money(comparison.original_acquisition)}.
        </p>
        <Metric name="Item sale" value={comparison.sale} />
        <Metric name="Net" value={comparison.net} />
        <Metric name="Profit" value={comparison.profit} />
      </details>
    </section>
  );
}

export function OutcomeSection({ id }: { id: string }) {
  const connection = useConnection();
  const [data, setData] = useState<OutcomeResponse | null>(null);
  const [draft, setDraft] = useState<OutcomeActuals | null>(null);
  const [expected, setExpected] = useState(0);
  const [reason, setReason] = useState('');
  const [historical, setHistorical] = useState<OutcomeEntry | null>(null);
  const [pending, setPending] = useState<OutcomeAppend | null>(null);
  const [retryAllowed, setRetryAllowed] = useState(false);
  const [conflict, setConflict] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [reload, setReload] = useState(0);
  const generation = useRef(0);
  const mounted = useRef(false);
  const locked = useRef(false);
  const operation = useRef<AbortController | null>(null);
  const online = connection.state === 'ONLINE_VERIFIED';

  useEffect(() => {
    mounted.current = true;
    const ticket = ++generation.current;
    const epoch = privateEpoch();
    const controller = new AbortController();
    operation.current = controller;
    setBusy(true);
    locked.current = true;
    setError('');
    void getOutcome(id, AbortSignal.any([controller.signal, AbortSignal.timeout(15000)]))
      .then((value) => {
        if (mounted.current && ticket === generation.current && epoch === privateEpoch())
          setData(value);
      })
      .catch(() => {
        if (mounted.current && ticket === generation.current && epoch === privateEpoch())
          setError('Actual outcome could not be loaded. The saved forecast is unchanged.');
      })
      .finally(() => {
        if (ticket === generation.current) {
          locked.current = false;
          if (mounted.current) setBusy(false);
        }
      });
    return () => {
      mounted.current = false;
      ++generation.current;
      controller.abort();
      operation.current?.abort();
      locked.current = false;
    };
  }, [id, reload, connection.revision]);

  useEffect(() => {
    if (connection.state === 'LOCKED' || connection.state === 'PUBLIC_OFFLINE_SHELL') {
      ++generation.current;
      operation.current?.abort();
      locked.current = false;
      setData(null);
      setDraft(null);
      setHistorical(null);
      setPending(null);
      setReason('');
      setExpected(0);
      setRetryAllowed(false);
      setConflict(false);
      setError('');
      setMessage('');
      setBusy(false);
    }
  }, [connection.state]);

  type Valid = () => boolean;
  async function act(work: (signal: AbortSignal, valid: Valid) => Promise<void>) {
    if (locked.current || connectionSnapshot().state !== 'ONLINE_VERIFIED') return;
    locked.current = true;
    setBusy(true);
    setError('');
    setMessage('');
    const ticket = ++generation.current;
    const epoch = privateEpoch();
    const controller = new AbortController();
    operation.current = controller;
    const valid = () =>
      mounted.current && ticket === generation.current && epoch === privateEpoch();
    try {
      await work(AbortSignal.any([controller.signal, AbortSignal.timeout(15000)]), valid);
    } finally {
      if (ticket === generation.current) {
        locked.current = false;
        if (mounted.current) setBusy(false);
      }
    }
  }

  function observed(entry: OutcomeEntry) {
    setPending(null);
    setRetryAllowed(false);
    setDraft(null);
    setReason('');
    setConflict(false);
    setData((current) =>
      current
        ? {
            ...current,
            state: 'RECORDED',
            latest:
              !current.latest || entry.revision > current.latest.revision ? entry : current.latest,
            history: [
              {
                id: entry.id,
                revision: entry.revision,
                recorded_at: entry.recorded_at,
                correction_reason: entry.correction_reason,
                purchase_decision: entry.actuals.purchase_decision,
                sale_status: entry.actuals.sale_status ?? null,
              },
              ...current.history.filter((item) => item.id !== entry.id),
            ].sort((a, b) => b.revision - a.revision),
          }
        : current,
    );
    setMessage(`Outcome revision ${entry.revision} saved. Original forecast unchanged.`);
  }

  async function send(body: OutcomeAppend, signal: AbortSignal, valid: Valid) {
    try {
      const entry = await appendOutcome(id, body, signal);
      if (valid()) observed(entry);
    } catch (cause) {
      if (!valid()) return;
      if (cause instanceof OutcomeRequestError && [404, 409, 422].includes(cause.status)) {
        setPending(null);
        setRetryAllowed(false);
        setConflict(cause.status === 409);
        setError(
          cause.code === 'OUTCOME_INVALID_CHRONOLOGY'
            ? 'The original forecast is later than the acquisition date. Correct the date or the before-purchase confirmation.'
            : cause.message,
        );
      } else {
        setRetryAllowed(false);
        setError(
          'Save status is uncertain. Check the exact submission before retrying; no automatic write will occur.',
        );
      }
    }
  }

  function save(event: FormEvent) {
    event.preventDefault();
    if (!draft || !data || pending || conflict) return;
    const body: OutcomeAppend = {
      id: crypto.randomUUID(),
      expected_revision: expected,
      actuals: draft,
      correction_reason: reason.trim() || null,
    };
    void act(async (signal, valid) => {
      setPending(body);
      setRetryAllowed(false);
      await send(body, signal, valid);
    });
  }

  function recover() {
    if (!pending || !data) return;
    const body = pending;
    void act(async (signal, valid) => {
      try {
        const entry = await getOutcomeEntry(id, body.id, signal);
        if (entry.root_forecast_id !== data.root_forecast_id) throw new Error('Unexpected root');
        if (!valid()) return;
        observed(entry);
        try {
          const latest = await getOutcome(id, signal);
          if (valid()) setData(latest);
        } catch {
          if (valid())
            setMessage(
              `Recovered revision ${entry.revision}. Reload to check for later corrections.`,
            );
        }
      } catch (cause) {
        if (!valid()) return;
        if (
          cause instanceof OutcomeRequestError &&
          cause.status === 404 &&
          cause.code === 'OUTCOME_NOT_FOUND'
        ) {
          setRetryAllowed(true);
          setMessage(
            'Exact submission was not found. An explicit retry will reuse its same identity and facts.',
          );
        } else
          setError(
            'Recovery could not be verified. Keep this page open and check again; no retry was sent.',
          );
      }
    });
  }

  function latest() {
    void act(async (signal, valid) => {
      try {
        const value = await getOutcome(id, signal);
        if (!valid()) return;
        setData(value);
        setExpected(value.latest?.revision ?? 0);
        setConflict(false);
        setMessage(
          'Latest revision loaded. Review your retained draft before deliberately saving.',
        );
      } catch {
        if (valid()) setError('Latest outcome could not be read. Your draft is retained.');
      }
    });
  }

  function history(entry: string) {
    void act(async (signal, valid) => {
      try {
        const value = await getOutcomeEntry(id, entry, signal);
        if (valid()) setHistorical(value);
      } catch {
        if (valid()) setError('Historical outcome could not be loaded.');
      }
    });
  }

  function moreHistory() {
    if (!data?.next_before_revision) return;
    const before = data.next_before_revision;
    void act(async (signal, valid) => {
      try {
        const page = await getOutcome(id, signal, before);
        if (!valid()) return;
        setData((current) =>
          current
            ? {
                ...page,
                history: [
                  ...current.history,
                  ...page.history.filter(
                    (item) => !current.history.some((old) => old.id === item.id),
                  ),
                ],
              }
            : page,
        );
      } catch {
        if (valid()) setError('More history could not be loaded.');
      }
    });
  }

  function field<K extends keyof OutcomeActuals>(key: K, value: OutcomeActuals[K]) {
    setDraft((current) => (current ? { ...current, [key]: value } : current));
  }
  function startEdit() {
    setDraft(data?.latest ? { ...data.latest.actuals } : blank());
    setExpected(data?.latest?.revision ?? 0);
    setReason('');
    setError('');
    setMessage('');
    setConflict(false);
    setHistorical(null);
  }

  return (
    <section className="outcome-section" aria-labelledby="actual-outcome-title">
      <h2 id="actual-outcome-title">Actual outcome</h2>
      <p>
        Private recorded facts for one purchase in this saved-deal lineage. Corrections retain
        history; forecasts are not rewritten.
      </p>
      {!online && (
        <p role="status">Verified connectivity is required. No offline outcome writes.</p>
      )}
      {busy && <p role="status">Working on actual outcome…</p>}
      {error && <p role="alert">{error}</p>}
      {message && <p role="status">{message}</p>}
      {!data && !busy && online && (
        <button type="button" onClick={() => setReload((value) => value + 1)}>
          Reload outcome
        </button>
      )}
      {data && online && (
        <>
          <p className="outcome-baseline">Comparison baseline: original {data.root_forecast_id}.</p>
          {data.latest ? (
            <OutcomeReadout entry={data.latest} />
          ) : (
            <p>No actual outcome recorded.</p>
          )}
          {!draft && !pending && (
            <button type="button" disabled={busy} onClick={startEdit}>
              {data.latest ? 'Correct entry' : 'Record outcome'}
            </button>
          )}
          {draft && (
            <form onSubmit={save} aria-label="Actual outcome form">
              <fieldset disabled={busy || !!pending}>
                <legend>{expected ? `Correct revision ${expected}` : 'Record actual facts'}</legend>
                <label>
                  Purchase decision
                  <select
                    aria-label="Purchase decision"
                    value={draft.purchase_decision}
                    onChange={(event) =>
                      setDraft(
                        event.target.value === 'NOT_BOUGHT'
                          ? {
                              purchase_decision: 'NOT_BOUGHT',
                              currency: 'USD',
                              contents_state: 'NOT_CHECKED',
                            }
                          : blank(),
                      )
                    }
                  >
                    <option value="BOUGHT">Bought</option>
                    <option value="NOT_BOUGHT">Not bought</option>
                  </select>
                </label>
                {draft.purchase_decision === 'BOUGHT' && (
                  <>
                    <p>
                      Blank amounts mean unknown. Use “None / 0” only for a cost or receipt you know
                      is zero. USD only.
                    </p>
                    <div className="outcome-fields">
                      <label>
                        Acquisition date
                        <input
                          type="date"
                          value={draft.acquired_on ?? ''}
                          onChange={(event) => field('acquired_on', event.target.value || null)}
                        />
                      </label>
                      <label>
                        Inspected contents
                        <select
                          aria-label="Inspected contents"
                          value={draft.contents_state ?? 'NOT_CHECKED'}
                          onChange={(event) =>
                            field(
                              'contents_state',
                              event.target.value as OutcomeActuals['contents_state'],
                            )
                          }
                        >
                          <option value="NOT_CHECKED">Not checked</option>
                          <option value="CONFIRMED_MATCH">
                            Confirmed match to this one-set forecast
                          </option>
                          <option value="CONFIRMED_DIFFERENT">Confirmed different</option>
                        </select>
                      </label>
                      <label>
                        Inspection date
                        <input
                          type="date"
                          value={draft.contents_checked_on ?? ''}
                          onChange={(event) =>
                            field('contents_checked_on', event.target.value || null)
                          }
                        />
                      </label>
                      <label>
                        Contents note
                        <textarea
                          maxLength={1000}
                          value={draft.contents_note ?? ''}
                          onChange={(event) => field('contents_note', event.target.value || null)}
                        />
                      </label>
                      <label>
                        Original forecast preceded purchase
                        <select
                          aria-label="Original forecast preceded purchase"
                          value={
                            draft.forecast_preceded_purchase == null
                              ? ''
                              : String(draft.forecast_preceded_purchase)
                          }
                          onChange={(event) =>
                            field(
                              'forecast_preceded_purchase',
                              event.target.value === '' ? null : event.target.value === 'true',
                            )
                          }
                        >
                          <option value="">Unknown</option>
                          <option value="true">Yes</option>
                          <option value="false">No</option>
                        </select>
                      </label>
                      <label>
                        Own labor minutes
                        <input
                          type="number"
                          min="0"
                          step="1"
                          max="2147483647"
                          value={draft.labor_minutes ?? ''}
                          onChange={(event) =>
                            field(
                              'labor_minutes',
                              event.target.value === '' ? null : Number(event.target.value),
                            )
                          }
                        />
                      </label>
                      <label>
                        Sale status
                        <select
                          aria-label="Sale status"
                          value={draft.sale_status ?? 'NOT_SOLD'}
                          onChange={(event) => {
                            const value = event.target.value as NonNullable<
                              OutcomeActuals['sale_status']
                            >;
                            setDraft((current) =>
                              current
                                ? {
                                    ...current,
                                    sale_status: value,
                                    ...(value !== 'COMPLETE' ? { sold_on: null } : {}),
                                    ...(value === 'NOT_SOLD'
                                      ? { item_sale_proceeds: null, shipping_charged: null }
                                      : {}),
                                  }
                                : current,
                            );
                          }}
                        >
                          <option value="NOT_SOLD">Not sold</option>
                          <option value="PARTIALLY_SOLD">Partially sold — totals to date</option>
                          <option value="COMPLETE">Complete — all sold and finally settled</option>
                        </select>
                      </label>
                      <label>
                        Sale strategy
                        <select
                          aria-label="Sale strategy"
                          value={draft.sale_strategy ?? ''}
                          onChange={(event) =>
                            field(
                              'sale_strategy',
                              (event.target.value || null) as OutcomeActuals['sale_strategy'],
                            )
                          }
                        >
                          <option value="">Unknown</option>
                          <option value="COMPLETE_SET">Complete set</option>
                          <option value="OTHER">Other strategy</option>
                        </select>
                      </label>
                      <label>
                        Sale condition
                        <select
                          aria-label="Sale condition"
                          value={draft.sale_condition ?? 'UNKNOWN'}
                          onChange={(event) =>
                            field(
                              'sale_condition',
                              event.target.value as OutcomeActuals['sale_condition'],
                            )
                          }
                        >
                          <option value="UNKNOWN">Unknown</option>
                          <option value="N">New</option>
                          <option value="U">Used</option>
                        </select>
                      </label>
                      <label>
                        Sale channel
                        <input
                          maxLength={80}
                          value={draft.sale_channel ?? ''}
                          onChange={(event) => field('sale_channel', event.target.value || null)}
                        />
                      </label>
                      {draft.sale_status === 'COMPLETE' && (
                        <label>
                          Final sale date
                          <input
                            type="date"
                            value={draft.sold_on ?? ''}
                            onChange={(event) => field('sold_on', event.target.value || null)}
                          />
                        </label>
                      )}
                    </div>
                    <p>
                      Dates are calendar dates. Before-purchase checks use the original forecast’s
                      UTC date; same-day ordering needs your confirmation.
                    </p>
                    <div className="outcome-fields">
                      {moneyFields.map(([key, label]) => {
                        const inactive =
                          draft.sale_status === 'NOT_SOLD' &&
                          (key === 'item_sale_proceeds' || key === 'shipping_charged');
                        return (
                          <div className="outcome-money" key={key}>
                            <label htmlFor={`outcome-${key}`}>{label} (USD)</label>
                            <input
                              id={`outcome-${key}`}
                              type="text"
                              inputMode="decimal"
                              autoComplete="off"
                              pattern="(0|[1-9][0-9]{0,11})(\.[0-9]{1,2})?"
                              value={draft[key] ?? ''}
                              disabled={inactive}
                              onChange={(event) => field(key, event.target.value || null)}
                            />
                            <button
                              type="button"
                              disabled={inactive}
                              aria-label={`Set ${label.toLowerCase()} to zero`}
                              onClick={() => field(key, '0')}
                            >
                              None / 0
                            </button>
                          </div>
                        );
                      })}
                    </div>
                    <p>
                      Item proceeds exclude buyer shipping and pass-through tax. Enter final settled
                      gross amounts after refunds, not marketplace net payouts. Acquisition extras
                      include tax/premium/pickup once; other selling costs exclude replacement and
                      paid labor entered separately. Own time is not priced automatically.
                    </p>
                  </>
                )}
                {expected > 0 && (
                  <label>
                    Correction reason
                    <textarea
                      required
                      maxLength={500}
                      value={reason}
                      onChange={(event) => setReason(event.target.value)}
                    />
                  </label>
                )}
                <div className="outcome-actions">
                  <button type="submit" disabled={conflict}>
                    {expected ? 'Save correction' : 'Save outcome'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setDraft(null);
                      setReason('');
                      setError('');
                      setConflict(false);
                    }}
                  >
                    Cancel outcome edit
                  </button>
                </div>
              </fieldset>
            </form>
          )}
          {conflict && (
            <button type="button" disabled={busy} onClick={latest}>
              Reload latest outcome
            </button>
          )}
          {pending && (
            <div className="notice">
              <p>
                Submission pending recovery. Your exact facts and submission identity are held only
                on this page.
              </p>
              <button type="button" disabled={busy} onClick={recover}>
                Check submission status
              </button>
              {retryAllowed && (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => void act((signal, valid) => send(pending, signal, valid))}
                >
                  Retry same submission
                </button>
              )}
            </div>
          )}
          {!!data.history.length && (
            <details>
              <summary>Outcome history</summary>
              <ul>
                {data.history.map((item) => (
                  <li key={item.id}>
                    <button type="button" disabled={busy} onClick={() => history(item.id)}>
                      View outcome revision {item.revision}
                    </button>{' '}
                    · {new Date(item.recorded_at).toLocaleString()}
                    {item.correction_reason ? ` · ${item.correction_reason}` : ''}
                  </li>
                ))}
              </ul>
              {data.next_before_revision && (
                <button type="button" disabled={busy} onClick={moreHistory}>
                  More outcome history
                </button>
              )}
            </details>
          )}
          {historical && (
            <>
              <OutcomeReadout entry={historical} historical />
              <button type="button" onClick={() => setHistorical(null)}>
                Close historical outcome
              </button>
            </>
          )}
        </>
      )}
    </section>
  );
}
