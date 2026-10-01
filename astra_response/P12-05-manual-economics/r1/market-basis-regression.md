# Unchanged MARKET admission

SELECTED_MARKET+UNKNOWN with zero observations returns UNKNOWN, market_value null
and null expected sale/gross/net/profit/ROI. Costs/acquisition remain 25.00/105.00.
SELECTED_MARKET+SUPPORTED uses the existing exact synthetic market price 180.049,
displayed as 180.05, with unchanged exact arithmetic and rounding. MANUAL+SUPPORTED
uses 200 while retaining that separate 180.05 market value.

The 112 economics/snapshot unit tests passed, including all four NEW/USED x
SOLD/STOCK views, unsupported admission, zero prices, valid/invalid money,
ambient Decimal isolation, revision identity and exact replay. These are unchanged
source regressions, not a claim that a new repair passed. All application source files
remain identical to accepted main; no market/provider/stale-basis rules changed.
Existing service first-save expiry/basis checks and UI abort/generation behavior
were traced but their broader API/browser suites were not rerun.
