import { OnlineOnly, useConnection } from './Connectivity';
import { useEffect, useRef, useState } from 'react';
import { historicalForecast, ForecastRequestError } from './forecast-api';
import type { HistoricalForecast } from './forecast-api';
import { FinancialPresentation, dealMoney } from './Deal';
import { humanize } from './product-copy';
import { useDraftMemory } from './Authentication';
import { draftFromHistory } from './revision-draft';
import { contextHref } from './navigation';
import { ForecastLink } from './RevisionDraftPanel';
import { LineageMetadataSection } from './LineageMetadataSection';
import { OutcomeSection } from './OutcomeSection';

const timing = (value: string | null) =>
  value ? new Date(value).toLocaleString() : 'Not recorded';

/** Historical GET is the sole data dependency; saved history has no live expiry. */
export function HistoricalForecastPage({ id }: { id: string }) {
  const connection = useConnection();
  const memory = useDraftMemory();
  const [data, setData] = useState<HistoricalForecast | null>(null);
  const [error, setError] = useState('');
  const [retry, setRetry] = useState(0);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => {
    let current = true;
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 15_000);
    setData(null);
    setError('');
    document.title = 'Saved original forecast | BrickVault';
    heading.current?.focus();
    void historicalForecast(id, controller.signal)
      .then((value) => {
        if (!current) return;
        if (controller.signal.aborted) throw new Error('Request timed out');
        setData(value);
        if (memory?.value && memory.value.number !== value.presentation.set_number) {
          memory.value = null;
          memory.forecastId = null;
        }
        document.title = `${value.presentation.set_number} · Saved ${value.record.lineage.parent_id ? 'revision' : 'original forecast'} | BrickVault`;
      })
      .catch((cause: unknown) => {
        if (current)
          setError(
            cause instanceof ForecastRequestError
              ? cause.message
              : 'The saved original could not be loaded. No financial results are displayed.',
          );
      })
      .finally(() => window.clearTimeout(timer));
    return () => {
      current = false;
      controller.abort();
      window.clearTimeout(timer);
    };
  }, [id, retry, connection.revision]);
  const result = data?.presentation;
  const assumptions = result?.assumptions;
  const isRevision = !!data?.record.lineage.parent_id;
  function edit() {
    if (!data || !memory) return;
    const result = data.presentation;
    memory.value = {
      number: result.set_number,
      draft: draftFromHistory(data),
      revision: {
        sourceId: data.record.id,
        parentId: data.record.id,
        rootId: data.record.lineage.root_id,
      },
    };
    window.history.pushState(
      {},
      '',
      contextHref(result.set_number, {
        section: 'deal',
        condition: result.condition,
        basis: result.basis,
        strategy: 'COMPLETE_SET',
      }),
    );
    window.dispatchEvent(new PopStateEvent('popstate'));
  }
  return (
    <article className="historical-forecast" aria-labelledby="forecast-title">
      <header className="set-identity">
        <p className="eyebrow">
          Private historical record{result ? ` · Set ${result.set_number}` : ''}
        </p>
        <h1 id="forecast-title" ref={heading} tabIndex={-1}>
          {isRevision ? 'Saved revision' : 'Saved original forecast'}
        </h1>
        <p>Current evidence not checked.</p>
      </header>
      {error ? (
        <div className="notice" role="alert">
          <p>{error}</p>
          <button onClick={() => setRetry((v) => v + 1)}>Retry historical load</button>
        </div>
      ) : !data ? (
        <p role="status">Loading saved original…</p>
      ) : null}
      <OnlineOnly>
        <LineageMetadataSection key={id} id={id} />
      </OnlineOnly>
      <OnlineOnly>
        <OutcomeSection key={id} id={id} />
      </OnlineOnly>
      {data && result && assumptions && (
        <>
          <nav className="forecast-lineage" aria-label="Saved forecast lineage">
            {isRevision && (
              <>
                <ForecastLink id={data.record.lineage.root_id}>Original forecast</ForecastLink>
                <ForecastLink id={data.record.lineage.parent_id!}>Parent forecast</ForecastLink>
              </>
            )}
            {data.record.lineage.latest_saved_id && data.record.lineage.latest_saved_id !== id && (
              <ForecastLink id={data.record.lineage.latest_saved_id}>
                Latest saved revision
              </ForecastLink>
            )}
          </nav>
          <p className="forecast-id">Viewing exact saved record {data.record.id}</p>
          {data.record.lineage.latest_saved_id !== id && (
            <p>
              Latest is observed navigation information. This page remains the requested saved
              record.
            </p>
          )}
          <button onClick={edit}>Edit assumptions</button>
          <p className="historical-context">
            Set {result.set_number} · {result.condition === 'N' ? 'NEW' : 'USED'} ×{' '}
            {result.basis === 'sold' ? 'SOLD' : 'STOCK'} ·{' '}
            {assumptions.sale_basis === 'MANUAL'
              ? 'Manual sale assumption'
              : 'Selected market sale assumption'}
          </p>
          {result.basis === 'stock' && (
            <p className="notice">
              Active-listing what-if: asking prices are not completed sales. This is not a
              SOLD-backed recommendation.
            </p>
          )}
          <p>
            Saved assumptions and historical qualifications, with financial results recomputed and
            verified from this exact record. An assumed purchase price is not an actual purchase;
            forecast profit is not realized profit.
          </p>
          <dl className="forecast-times">
            <div>
              <dt>Originally calculated</dt>
              <dd>{timing(data.calculated_at)}</dd>
            </div>
            <div>
              <dt>Evidence assessed</dt>
              <dd>{timing(data.assessed_at)}</dd>
            </div>
            <div>
              <dt>{isRevision ? 'Revision saved' : 'Original saved'}</dt>
              <dd>{timing(data.record.saved_at)}</dd>
            </div>
            <div>
              <dt>Original evidence eligibility deadline (historical)</dt>
              <dd>{timing(data.original_evidence_deadline)}</dd>
            </div>
          </dl>
          <p className="deal-help">
            The original evidence deadline describes the assessment then. It does not expire this
            saved record or establish current eligibility.
          </p>
          <div className="deal-columns">
            <section
              className="forecast-assumptions"
              aria-label={isRevision ? 'Saved revision assumptions' : 'Original assumptions'}
            >
              <h2>{isRevision ? 'Saved revision assumptions' : 'Original assumptions'}</h2>
              <dl className="deal-ledger">
                {(
                  [
                    ['Assumed purchase price', assumptions.purchase_price],
                    ['Manual expected sale', assumptions.manual_sale_price],
                    ['Shipping charged to buyer', assumptions.shipping_charged],
                    ['Shipping expense', assumptions.shipping_paid],
                    ['Other selling costs', assumptions.other_selling_costs],
                    ['Additional acquisition costs', assumptions.acquisition_costs],
                  ] as const
                ).map(([label, amount]) => (
                  <div key={label}>
                    <dt>{label}</dt>
                    <dd>{dealMoney(amount, result.currency)}</dd>
                  </div>
                ))}
                <div>
                  <dt>Selling fee mode</dt>
                  <dd>
                    {assumptions.selling_fee_mode === 'CALCULATED'
                      ? 'Percentage + fixed fee'
                      : 'Manual total fee'}
                  </dd>
                </div>
                {assumptions.selling_fee_mode !== 'CALCULATED' && (
                  <div>
                    <dt>Assumed manual fee</dt>
                    <dd>{dealMoney(assumptions.selling_fees, result.currency)}</dd>
                  </div>
                )}
                {'targets' in assumptions && (
                  <>
                    <div>
                      <dt>Purchase tax</dt>
                      <dd>{assumptions.purchase_tax_percent}%</dd>
                    </div>
                    <div>
                      <dt>Buyer premium</dt>
                      <dd>{assumptions.buyer_premium_percent}%</dd>
                    </div>
                    <div>
                      <dt>Target ROI</dt>
                      <dd>
                        {assumptions.targets.roi_enabled
                          ? `${assumptions.targets.roi_percent}%`
                          : 'Disabled'}
                      </dd>
                    </div>
                    <div>
                      <dt>Minimum profit</dt>
                      <dd>
                        {assumptions.targets.profit_enabled
                          ? dealMoney(assumptions.targets.minimum_profit, result.currency)
                          : 'Disabled'}
                      </dd>
                    </div>
                  </>
                )}
              </dl>
              <h3>Historical qualifications</h3>
              <p>
                {isRevision ? 'Recorded' : 'Original'} whole-set market value:{' '}
                {dealMoney(result.market_value, result.currency)}.
              </p>
              {result.market_subset_value !== null && (
                <p>
                  Original partial market subtotal:{' '}
                  {dealMoney(result.market_subset_value, result.currency)}. This is not a complete
                  market value.
                </p>
              )}
              <p>Original assertions preserved; not reassessed against current evidence.</p>
              <p>
                {result.status} · {humanize(result.evidence_quality)}
              </p>
              <p>
                Physical state: {humanize(data.qualifications.physical_state)}.{' '}
                {data.qualifications.physical_admitted
                  ? 'Admitted in the original assessment.'
                  : 'Not admitted in the original assessment.'}
              </p>
              {[...new Set([...data.qualifications.physical_reasons, ...result.reasons])].map(
                (reason) => (
                  <p key={reason}>{humanize(reason)}</p>
                ),
              )}
              {data.qualifications.synthetic_catalog && (
                <p className="synthetic-notice">Synthetic catalog data</p>
              )}
            </section>
            <section className="deal-results" aria-label="Verified historical economics">
              <h2>{isRevision ? 'Saved revision economics' : 'Original forecast economics'}</h2>
              <FinancialPresentation result={result} />
            </section>
          </div>
          <details className="forecast-provenance">
            <summary>Original record details & attribution</summary>
            <dl className="forecast-times">
              <div>
                <dt>Capture created</dt>
                <dd>{timing(data.record.created_at)}</dd>
              </div>
              <div>
                <dt>First-save deadline (historical)</dt>
                <dd>{timing(data.record.save_eligible_until)}</dd>
              </div>
              <div>
                <dt>Calculation accepted</dt>
                <dd>{timing(data.accepted_at)}</dd>
              </div>
            </dl>
            <p className="forecast-id">Record {data.record.id}</p>
            <p>
              {data.execution.snapshot} · {data.execution.calculation} · {data.execution.rounding}
            </p>
            {data.provider_attribution.map((value) => (
              <p key={value}>{value}</p>
            ))}
            <p>{data.catalog_attribution}</p>
          </details>
          <p className="deal-help">{data.trademark_notice}</p>
        </>
      )}
    </article>
  );
}
