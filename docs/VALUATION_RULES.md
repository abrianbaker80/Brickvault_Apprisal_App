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
3. Full part-out, with an explicit intact-versus-component figure policy and supported recovery/cost evidence.
4. Later selective part-out / harvest of high-value lots, only after separate residual-inventory and recovery evidence supports it.

Allocate each physical unit to at most one sale line in a strategy. Figures retained in the residual lot are not also separate figure lines. Missing units cannot produce sale proceeds. Components of a separately sold figure cannot also be priced as loose parts. Alternative strategies may reference the same inventory only because their totals are never added together.

Never calculate complete-set value + removed minifigure values + values of those same figure components as parts.

    split-sale gross =
        sum(adjusted minifigure proceeds)
        + conservative remaining-build proceeds

A remaining-build value needs an explicit basis: comparable residual-build evidence or a clearly labeled, versioned conservative assumption validated in Phase 4. Record whether instructions, box, and retained figures are included. Do not assert residual value equals whole-set price minus theoretical figure prices.

The theoretical sum of individual parts is a separate metric from expected recoverable proceeds. D-025 brings full part-out economic analysis into the Phase 5 engine subject to liquidity, completeness, order-count and burden evidence; operational individual-piece listing/fulfillment remains excluded. Unsupported residual proceeds block a supported split-sale or selective-harvest recommendation; a manual scenario can remain visible as a labeled scenario. A removed high-value part must be removed from residual-build allocation as well as its value basis; whole-set value minus theoretical removed-part prices is not a supported residual estimate.

## New and used set part-out comparison — R-11

The requested [part-out feature](plans/005-set-part-out-values.md) calculates four independent NEW/USED × SOLD/CURRENT theoretical views. Preserve exact color/variant identity, price statistic, currency, inventory/source versions, freshness and lot/unit coverage. Default policy keeps minifigures assembled and excludes optional extras, unselected alternate possibilities, box and instructions. Required alternate/matching choices must resolve to the actual selected inventory; omitting an unresolved required group cannot produce a complete result. Extra quantities remain separately recorded even when explicitly included.

A part-out total includes each allocated physical unit once. Never add it to whole-set value or residual-build value, or add minifigures again when already included. Breaking a figure into verified components replaces its intact sale line; nested subsets likewise expand or remain intact, never both. D-025 adds recoverable-gross and liquidity analysis in Phases 2–8 while preserving the exclusion for selling operations and every gross/net/acquisition/ROI/max-buy rule below.

## Part-out inputs, status and coverage — R-13/R-14

For a chosen set/inventory/allocation policy let q_i be selected sellable quantity, p_i the selected exact unit price, L the unique sellable lot count and Q the total selected sellable quantity. A unique lot groups identical canonical item/variant/color/condition and compatible sale treatment; consolidate identical selected lines deterministically while retaining regular/extra/source lineage. Keep physical piece count Q_piece separately: an intact figure is one sellable unit but can contain several physical pieces. Use verified component relationships to count those pieces once; unknown expansion leaves Q_piece unavailable. Instructions/packaging are non-piece sale lines and do not inflate Q_piece. Each numerator discloses its inclusion policy, including any non-piece value.

All metrics carry value or null, state, reason, input references, units/currency, actual time window, calculation/policy version and as-of time. Use complete/partial/blocked at result level and finite/undefined/infinite/insufficient_evidence/not_applicable as applicable at metric level; never encode nonfinite JSON numbers. A partial priced subtotal is separate from a null full theoretical total. Unresolved required identity/allocation blocks completeness and dependent recommendations.

Lot price coverage = priced lots / L; quantity price coverage = priced sellable quantity / Q. Report both as percentages and counts, including unpriced quantities and line identities. Verified empty inventory has a zero theoretical total and not-applicable coverage; unknown inventory has no known denominator. Activity coverage is per metric: lots and quantities with all required compatible activity inputs divided by selected totals. Partial field availability cannot count as complete liquidity coverage.

**Value coverage:** a full-value-weighted percentage cannot be known from only prices of the priced subset. If all selected value is known and the total is positive, coverage is 100%; with zero total it is not applicable. With missing prices, value coverage remains undefined unless independent, complete, permitted reference weights w_i exist. Then report separately labeled reference-value coverage = sum(w_i for priced lots) / sum(w_i for all selected lots), with reference basis/version, positive denominator and uncertainty; never use it to invent missing prices or label the POV complete. Do not divide a subtotal by itself to claim coverage.

Percentages of POV below require positive, complete POV. With incomplete coverage an optional conditional percentage uses the explicitly labeled priced subtotal; it is never presented as a percentage of the unknown full value. Unknown excluded value remains unquantified, accompanied by its lots/quantities. Zero and unknown denominators remain distinct.

## Theoretical and recoverable part-out value — R-11/R-12/R-15

**V-POV:** theoretical POV = sum(q_i × p_i) over the resolved selected inventory. Each of the four views uses its own prices and coverage. Reject negative quantities/prices, unsupported currency mixing and guessed identities; known zero selected quantity contributes zero without implying that a missing quote is zero. Select an explicit provider statistic, preferably a supported quantity-weighted sold statistic for a sold view; never silently replace it with simple average or current asking price.

**V-REC:** expected recoverable POV is expected recoverable **gross** for a stated horizon, strategy and selling profile. A candidate auditable model is sum(q_i × f_i × u_i), where f_i is the supported expected sold fraction in [0,1] and u_i is a supported expected realized gross unit price; consolidation may instead use nonoverlapping grouped sale lines. This defines the calculation structure, not approved f_i/u_i coefficients. Phase 4 must validate the model, horizon, liquidity/supply/occurrence inputs, stale/thin-price handling, unsold/low-value/long-tail assumptions and calibration. Missing required support yields blocked or explicitly manual scenario results, not a default haircut or market-share assumption.

List the theoretical-to-recoverable adjustments and excluded inventory with reasons. Operational capacity, fragmentation, consolidation and expected listings/orders can affect achievable gross only through supported, separately identified recovery assumptions. Fees, packaging, shipping, handling/labor, risk reserve and other selling outlays are itemized once afterward: N = recoverable gross - selling costs; profit = N - C(p). Do not call a value after fees “gross,” deduct costs twice, or equate an unsold-value adjustment with an additional identical risk deduction. Charged shipping, if modeled, is separately identified gross revenue; no invented order count.

## Part-level liquidity formulas — R-16–R-21

S is recent sold unit quantity; C is current available unit quantity; M is the positive observation duration in months; O is a supplied sale-occurrence count; q is this set's selected quantity of the exact lot. Nonnegative inputs must describe compatible provider/item/color/condition, geography and market scope. S/O describe an actual interval; C describes its own observation instant. Store both timestamps and their age/skew policy; incompatible or missing inputs yield insufficient_evidence. Never invent historical stock exposure from C.

| Formula ID / metric | Deterministic rule | Zero, missing and interpretation rules |
|---|---|---|
| L-PROXY / unit sell-through proxy | S / (S + C) | Undefined if S=C=0; S=0,C>0 gives 0 with its actual sample; S>0,C=0 gives 1 without implying guaranteed liquidity. Missing inputs are insufficient evidence. “Six-month” applies only when that actual window is six months. |
| L-VELOCITY / monthly sales velocity | V = S / M | M must be known and positive. Verified S=0 yields V=0; absent S/window yields insufficient evidence. Store actual start/end, provider duration and the versioned calendar/day-to-month convention; do not choose a six-month default. |
| L-SUPPLY / months of supply | C / V for V>0 | C>0,V=0 is infinite under observed zero demand; C=V=0 is undefined; missing inputs are insufficient evidence. A finite zero for C=0,V>0 describes no observed supply, not instant sale. |
| L-ABSORB / set-quantity absorption | q / V for V>0 | q>0,V=0 is infinite; q=V=0 is undefined; unknown V/q is insufficient evidence. Demand-equivalent months use total observed market demand, not Brian's market share. |
| L-OCCURRENCE / occurrence frequency | O / M | Preserve raw O and its provider-defined meaning. O=0 in a verified positive window is zero; missing O stays unknown. Do not infer transaction sizes, buyers, orders or store sales. |

Ratios/durations use deterministic decimal or rational arithmetic, explicit precision/rounding at display boundaries, and preserve exact numerator/denominator inputs. A provider's non-six-month interval remains non-six-month. Phase 4 must settle and version any required month-normalization convention before comparing velocities. Do not mix differing source populations or normalize unknown windows.

Absorption examples are mathematical fixtures: q=2,V=75 gives 2/75 months; q=16,V=4 gives 4 months. Neither is a liquidation promise. At set level report distributions/buckets and extrema with quantity/value coverage and weighting; do not sum per-lot times into a set sale deadline. Competing lots sell concurrently, and observed aggregate demand is not exclusively available to this seller.

## Part opportunities, liquidity subsets and exposure — R-22–R-25

**O-GEM:** show the value/demand/supply/absorption/confidence/rarity dimensions before classification. Deterministic rules must define material unit/contributed value and adequate liquidity/confidence, using verified sales, occurrences where available, competition and absorption. No threshold is fixed here. Preserve INSUFFICIENT DATA and high-value/low-liquidity cases. Rare alone and expensive alone cannot qualify. A missing occurrence field cannot be assumed sufficient if the selected policy requires it.

**V-LIQUID:** sum theoretical contributions for selected lots passing the liquidity/confidence policy. **V-FAST:** use a stricter qualifying subset of Liquid POV with either theoretical contributions or explicitly labeled conservative gross adjustments bounded by those contributions; never mix bases without disclosure. Report amounts, shares of compatible POV, qualifying lots/pieces, confidence and threshold/profile version. Fast Cash's horizon, occurrences/velocity/supply and evidence thresholds remain Phase 4 gates. Neither subset proves expected cash or a sale date.

**V-DEAD:** sum priced contributions classified as slow/dead candidates by a validated policy, using verified zero/near-zero demand, high supply/velocity ratios and occurrence evidence where supported. Stale/thin data may invalidate the classification; missing activity produces INSUFFICIENT DATA. Report slow/dead value/share, lots/pieces and threshold/version separately from unknown-activity value/share and unpriced lots. Unknown inventory is not zero-value dead stock.

Policies are configurable, immutable by version and calibrated for representative cases in Phase 4, never selected to maximize the display. Liquid, Fast Cash and dead/slow classifications share a coherent classification version; Fast Cash is nested within Liquid, while dead/slow and qualifying liquid sets are disjoint. Nonqualifying-but-not-dead inventory remains a separate category. Do not add nested Liquid/Fast Cash values to each other or add any subset to total POV.

## Concentration, break-even and operational metrics — R-26–R-34

| Formula ID / metric | Rule and required explanation |
|---|---|
| V-CONCENTRATION | Rank unique consolidated lots by q_i × p_i descending, breaking ties by stable canonical lot key. Highest lot and sums of first min(5,L) / min(10,L) lots produce top-5/top-10 values and compatible POV shares. Report policy-qualified high-value and high-liquidity contribution shares separately; preserve physical-figure and figure-identity concentration. |
| V-BREAK-EVEN | For nonnegative acquisition target A_target = C(p), take the shortest ranked lot prefix whose cumulative chosen contribution reaches A_target; report all chosen identities, lots, sellable/physical quantities, quantity and lot percentages, theoretical/recoverable contributions and confidence. View A sorts theoretical contributions; View B uses a documented Phase 4-validated value/liquidity/confidence order with stable ties. Insufficient qualifying value is “target not reached,” never a forced result. Zero target needs zero lots and does not define ROI. |
| V-BREAK-EVEN economics | A theoretical/recoverable-gross prefix measures gross acquisition-target coverage only. A supported economic break-even view must re-evaluate itemized incremental/fixed order, shipping, packaging and labor costs for that subset, so subset net >= C(p). Unknown costs/recovery block the economic claim. No lot count guarantees a sale or recovery. |
| V-PER-LOT | Expected recoverable gross / L selected unique sellable lots; unknown recovery/count yields unavailable, zero L is undefined. If only a subtotal is known, label the result conditional. |
| V-PER-PIECE | Expected recoverable gross / Q_piece selected physical pieces; unknown component count or recovery yields unavailable, zero denominator is undefined. Disclose included non-piece revenue and allow a compatible piece-only numerator as a separately named view. Never substitute lot count for pieces. |
| O-BURDEN | Preserve L, Q_piece, supportable expected listings/orders, lot value, low/high-value-lot proportions with threshold and denominator, and fragmentation. Version LOW/MEDIUM/HIGH rules only after feasibility calibration; no fabricated precise labor hours or orders-per-lot assumption. |
| O-COMPETITION | Preserve C, active inventory/lot count and seller/store count as separate supplied measures. Seller concentration requires a supplied distribution, not just total seller count. |
| O-RARITY | Count distinct canonical sets with the exact part/color in verified selected inventory relationships, scoped to catalog/version/completeness and alternate-resolution policy. Preserve first/last known appearances where available. Unresolved alternatives cannot prove presence/exclusivity; an incomplete catalog proves only known presence, never global exclusivity. |
| V-PREMIUM | POV / compatible whole-set value - 1, requiring a positive known denominator and complete compatible numerator for an unqualified premium. Match condition, SOLD/CURRENT, currency and documented statistic/window/inclusion basis. Explicitly label cross-basis or partial comparisons and exclude them from default ranking. |

Illustrative efficiency fixtures, not market evidence: recoverable gross USD 300 over 75 lots = USD 4.00/lot; over 475 lots = USD 0.63/lot at display precision. A lot prefix's coverage percentage states whether its denominator is lots, sellable units or physical pieces. Unsupported physical expansion leaves the piece percentage unavailable; listing count is not order count.

## Set aggregation and Hunt components — R-36/R-37

Each set-level snapshot groups four independent POV results, expected recoverable gross, Liquid/Fast Cash/dead-stock outputs, price/activity coverage, high-value-part/Gem counts, concentration, density, burden, distributions and confidence. Preserve selected basis and numerator/denominator per field; never blend all four values into a total. Aggregate distributions preserve infinite/unknown buckets and observed periods rather than dropping adverse lots.

Hunt components include asking price or labeled hypothetical target, whole-set/figure/POV/recoverable evidence, net/profit/ROI/max-buy, POV premium, proxy/velocity and supply/absorption distributions, Liquid share, Fast Cash, Dead-Stock Exposure, top figure/part/5/10/Gems/break-even concentration, lots/pieces/density/low-value share/orders/burden, competition, rarity and mapping/price/activity/sample/freshness confidence. Compare strategies independently. No supported combined score from theoretical POV alone; no double reward for overlapping derived measures without an explicit calibration rationale.

Phase 4 evaluates candidate normalization, thresholds, weights, sensitivity and stable tie rules on representative real sets. Phase 8 implements the reviewed deterministic decomposable policy, retaining components, versions and exclusion reasons. Do not lock arbitrary weights here; do not silently renormalize missing critical components into an apparently precise high score. Without asking price, deal profit/ROI remain unavailable unless a labeled hypothetical acquisition scenario is selected.

## Planned deterministic part-out acceptance

Phase 5 table tests must cover all formula IDs above: exact sums/currency/rounding, four-view isolation, zero/unknown/full/partial coverage and reference-weight provenance, empty inventory, repeated quantities, selected extras and alternate resolution, intact-versus-component/no-residual-double-count allocation, physical-piece versus sellable-unit counts, non-six-month windows, invalid M, S=C=0, zero demand with positive supply/quantity, missing activity, time/scope mismatch and infinite/unknown distribution buckets.

Test 100 sold units in one versus 60 occurrences, identical supply across three versus 28 sellers, high-value/low-velocity and low-value/high-velocity cases, rare/no-demand cases, threshold boundaries, fast-subset nesting and dead/unknown separation, stable top-N ties and L<5/10, target reached/not reached/zero with subset costs, density zero denominators, compatible/incompatible/zero-denominator premiums, and deterministic profile/version replay. Recovery examples must itemize gross adjustments and costs exactly once. Phase 8 tests missing critical inputs, score components/ties, correlated-metric sensitivity and immutable ranking replay. These are planned tests; this amendment implements or executes none of them.

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
