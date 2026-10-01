# Exact acceptance arithmetic and evidence scope

The request and live unavailable result are reused from P12-05 r2; no production
retry occurred. New evidence uses synthetic existing V1 capture/replay helpers.

| Output | Requested MANUAL result | Unchanged MANUAL + SUPPORTED fixture | Unchanged MANUAL + zero-observation UNKNOWN |
| --- | --- | --- | --- |
| Expected item sale | 200.00 | 200.00 | null |
| Gross proceeds | 210.00 | 210.00 | null |
| Selling costs | 25.00 | 25.00 | 25.00 |
| Net before acquisition | 185.00 | 185.00 | null |
| Total acquisition | 105.00 | 105.00 | 105.00 |
| Profit | 80.00 | 80.00 | null |
| ROI | 76.2% | 76.2% | null |

Inputs: sale 200, purchase 100, charged shipping 10, manual fees 15, paid shipping 8,
other selling costs 2, additional acquisition 5. Gross = 200 + 10; costs = 15 + 8 + 2;
net = 210 - 25; acquisition = 100 + 5; profit = 185 - 105; ROI = 80 / 105 * 100
using existing Decimal isolation and display rounding. No fixture-specific formula
was implemented. The supported fixture's separate market amount is 180.05 and
does not replace the manual 200 sale. UNKNOWN fixtures have no market observations.

[Machine-readable synthetic results](arithmetic-evidence.json) record all four
sale-mode/status cases and exact encode/decode/replay preservation. These fixtures
prove accepted V1 arithmetic and the blocker. They do not satisfy MANUAL+UNKNOWN
repair acceptance. Existing unit tests also confirm undefined ROI at zero
acquisition and sub-cent/exact-money boundaries.
