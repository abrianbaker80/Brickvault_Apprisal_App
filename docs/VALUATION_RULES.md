# Valuation Rules

Status: authoritative planning contract under D-020; no engine or provider integration exists yet. Implement in Phase 5, expose in Phases 6–8. See [product requirements](PRODUCT_SPEC.md), [data model](DATA_MODEL.md), and [provider gates](PROVIDER_GATES.md).

## Money and rounding

Use exact decimal arithmetic on the server and PostgreSQL NUMERIC; transport amounts as decimal strings with an explicit ISO currency code. Never use binary floating-point dollars for financial calculations. Preserve source precision, and round displayed monetary amounts to the currency's minor unit using decimal ROUND_HALF_UP. Calculations retain exact decimal precision until an explicitly defined rounding boundary.

Each fee rule declares its base and whether rounding occurs per order or on the aggregate; use the same boundary in tests, snapshots, and explanations. Do not assume every currency has two decimal places. Financial truth is server-calculated; client formatting must not recalculate it.

Preserve currency on every observation, cost line, input, and result. Reject mixed-currency addition unless a recorded conversion observation supplies source/target currencies, rate, direction, provider, and timestamp. Persist that conversion and its rounding in the valuation snapshot. Phase 5 may initially support only same-currency calculations and explicitly block others.

## Market evidence

New and used remain separate. Whole-set display labels are new/sealed and used/complete only when the source evidence supports those completeness/packaging claims; a provider's generic new/used flag alone does not prove sealed or complete. Unsupported equivalence is an explicit qualification or unavailable state, never an automatic upgrade.

Sold evidence and current-listing evidence remain separate. Current asking prices are contextual supply evidence, not completed-sale values. A current/fair estimate must identify its evidence basis and statistic. No silent fallback from sold to asking data.

Every displayed sourced value preserves provider, provider item identifier/type, condition, market side, currency, observed-at time, observation window, sample count and/or quantity where available, fetched-at time, stale-after time, and freshness/coverage state. A source's unknown sample size remains unknown. Distinguish observation time from fetch time; fetching an old sample does not make it recent.

Missing data is unknown, never zero. Preserve unavailable, mapping-unresolved, stale, thin, and provider-error states distinctly. A known zero quantity, such as a verified set with no minifigures, has a known zero total; it is not missing evidence. Manual values are separately labeled, timestamped assumptions with an audit trail, never fabricated provider observations.

Provider-specific freshness and minimum-sample policies are configurable and versioned after Phase 4 feasibility evidence. Do not invent universally reliable thresholds now. A recommendation is blocked when required evidence is unavailable or mappings are unresolved; weak, stale, or incomplete evidence visibly reduces confidence and may block recommendations under the selected policy. Missing critical evidence cannot be bypassed with an unlabeled estimate.

## Minifigure identity, quantity, and condition

Use the verified catalog relationship quantity, then record the deal's actual quantity and condition per physical unit or homogeneous quantity group. Missing figures have absent quantity, not a fictional zero market price. Damaged/incomplete figures need an explicit adjusted unit-value basis or a supported replacement scenario; do not silently value them as complete.

For priced included minifigures:

    minifigure gross = sum(adjusted unit value × included quantity)

Produce separate new and used catalog totals. Deal totals additionally reflect actual missing/damaged/selected quantities. Report total applicable quantity, priced quantity, unavailable quantity, coverage percentage, top-figure concentration, and complete/partial/blocked status. Coverage = priced quantity / total applicable quantity × 100; report not applicable for a verified zero-figure set, whose total is zero and status complete.

Top-figure concentration = largest single physical figure's adjusted unit value / priced minifigure gross; it is undefined when priced gross is zero or unknown. Also expose concentration by figure identity including its quantity so repeated figures remain visible. For partial coverage, label concentration as conditional on priced items; never imply it covers unknown figures.

Show catalog quantity, absent quantity, and deal quantity separately so reducing a deal to zero figures does not imply the catalog contains none. Quantity-aware acceptance covers repeated figures and partially missing copies.

## Mutually exclusive sale strategies

Each valuation selects exactly one strategy; comparisons show separate results:

1. Sell the complete set, or an explicitly adjusted incomplete-set lot.
2. Sell selected minifigures separately and sell the remaining build.
3. Later, sell minifigures and part out individual remaining pieces.

Allocate each physical unit to at most one sale line in a strategy. Figures retained in the residual lot are not also separate figure lines. Missing units cannot produce sale proceeds. Components of a separately sold figure cannot also be priced as loose parts. Alternative strategies may reference the same inventory only because their totals are never added together.

Never calculate complete-set value + removed minifigure values + values of those same figure components as parts.

    split-sale gross =
        sum(adjusted minifigure proceeds)
        + conservative remaining-build proceeds

A remaining-build value needs an explicit basis: comparable residual-build evidence or a clearly labeled, versioned conservative assumption validated in Phase 4. Record whether instructions, box, and retained figures are included. Do not assert residual value equals whole-set price minus theoretical figure prices.

The theoretical sum of individual parts is a separate metric, not expected recoverable proceeds, until liquidity, completeness, order count, and selling-burden assumptions are supported. Full piece-level part-out is outside the initial engine. Unsupported residual proceeds block a supported split-sale recommendation; a manual scenario can remain visible as a labeled scenario.

## New and used set part-out comparison — R-11

The requested [part-out feature](plans/005-set-part-out-values.md) calculates a theoretical sum of component quantities times condition-specific unit observations, separately for new and used. Preserve exact color/variant identity, price statistic and market side, inclusion policy, currency, inventory/source versions, freshness and lot/unit coverage. A partial subtotal is not a complete total; absent required prices are unknown rather than zero. Default policy keeps minifigures assembled and excludes extras/alternates/box/instructions as detailed in that plan; unresolved required choices block completeness.

A part-out total includes each allocated physical unit once. Never add it to whole-set value or residual-build value, or add minifigures again when already included. Its theoretical nature does not authorize a profit/max-buy recommendation without separately supported sell-through, costs and selling-burden assumptions. The initial exclusion for operational individual-piece sales remains; Phases 2–6 add this comparison metric only.

## Gross proceeds and selling costs

Expected gross proceeds comprise only the sale lines in the selected strategy. Explicitly identify seller revenue such as charged shipping when included; exclude pass-through taxes that are not Brian's revenue.

Selling costs include percentage fees with their taxable/fee bases, fixed per-order fees, estimated order count, seller-paid shipping, packaging/supplies, promotions/advertising, configured labor or replacement outlays, risk reserve, and other itemized selling costs. Record expected listings/orders separately from item quantity. Do not assume all figures sell in one order.

Any outlay belongs to one cost category only. Do not deduct a replacement both as an acquisition cost and selling cost, or apply both a condition discount and replacement deduction without explaining the distinct losses. Risk reserve is an explicit cost line deducted once.

    expected net proceeds N =
        expected gross proceeds - expected selling costs

N is proceeds before acquiring the deal; it is not profit.

## Acquisition cost, profit, and ROI

Let p be purchase price and A fixed acquisition costs, including configured travel/pickup or fixed premiums. Record acquisition tax and percentage buyer premiums independently with their bases.

    total acquisition cost C(p) =
        purchase price
        + purchase-price-dependent tax or buyer premium
        + fixed acquisition costs

For the simple case where all percentage charges apply directly to purchase price, t is their combined effective rate:

    C(p) = p × (1 + t) + A
    expected profit = N - C(p)
    ROI = expected profit / C(p)

ROI is undefined when total acquisition cost is zero. Display that state explicitly, not infinity or zero. Margin percentage, if shown, has a separately named denominator and is not labeled ROI.

A missing asking price allows a supported maximum-buy calculation but leaves asking-price profit/ROI unavailable. Negative proceeds or profit remain visible; do not clamp them to zero.

## Maximum purchase price and recommendation

For N expected net proceeds, target ROI r, minimum required profit P, fixed acquisition costs A, and percentage acquisition tax/premium t applied to p:

    maximum purchase by ROI = (N / (1 + r) - A) / (1 + t)
    maximum purchase by minimum profit = (N - A - P) / (1 + t)
    recommended maximum purchase price =
        max(0, minimum of the supported maximums)

Require r >= 0, P >= 0, A >= 0, and t >= 0 for this initial purchase policy. Settings must explicitly enable/disable each constraint; the default uses both with visible user-configured targets. An unavailable enabled constraint blocks the recommendation rather than being silently omitted from "supported maximums." With neither constraint enabled, no recommendation is produced.

Keep the raw signed constraint results for explanation, then round a purchasable maximum DOWN to the currency's minor unit. Re-evaluate the actual acquisition-cost and fee rounding at that price and reduce by minor units if necessary to satisfy every enabled constraint. A negative raw cap yields a displayed maximum of zero plus "no feasible purchase at these targets"; zero must not be presented as a profitable recommendation when even a free item fails the constraints.

If tax applies to premiums, charges have thresholds/caps, or rounded tax rules make C(p) nonlinear, the simple formula is not valid as written. Model and version the actual monotone C(p), and find the greatest minor-unit purchase price satisfying N - C(p) >= P and, when C(p) > 0, (N - C(p)) / C(p) >= r. Block unsupported cost rules rather than approximating silently. Zero-cost ROI remains undefined.

## Later appraisal extensions

The originating image-assisted concept also proposed quick-sale estimates and opening offers. Preserve them as optional later appraisal extensions, not Phase 1 work or replacements for the sourcing constraints: any quick-sale discount is a labeled, supported scenario in this same engine, and an opening-offer policy is versioned, explicit, and bounded by the supported recommended maximum. Do not add a second financial engine or let a model choose the arithmetic.

## Reproducibility and acceptance examples

Persist all input/output lines, source references permitted by provider terms, source/manual distinctions, quantities, condition adjustments, currency conversions, cost bases, enabled targets, formula version, evidence-policy version, and rounding rules. A saved recommendation must reproduce exactly without refetching current prices. Resolve source-retention conflicts before promising permanent provider snapshots; see [provider gates](PROVIDER_GATES.md).

Illustrative decimal fixture, not a market claim: N = USD 180, A = USD 10, t = 0.10, r = 0.50, P = USD 40. Raw ROI cap = USD 100; raw minimum-profit cap = USD 118.1818…; recommended cap = USD 100. At p = USD 100, acquisition cost = USD 120, profit = USD 60, ROI = 50%. Raising t changes both caps and the result.

Phase 5 must test exact decimal and currency handling; both conditions and market sides; complete/missing/damaged/repeated figures; no-figure and unavailable cases; strategy allocation without double counting; negative profit; zero acquisition cost; each enabled/disabled target; variable tax/premium bases; order-count and rounding boundaries; and blocked unsupported evidence. Phase 8 additionally tests ranking determinism, tie rules, concentration, stale/thin data, and residual-estimate dependence.

Recommendations and hunt scores are deterministic, explainable, and versioned. An AI model may later suggest candidate catalog identities or describe visible condition evidence; it must never invent or alter financial arithmetic.
