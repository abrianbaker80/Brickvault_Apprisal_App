# Governing contract analysis

The accepted Plan 071 checkpoint (lines 214-215) explicitly says
PARTIAL/BLOCKED/UNKNOWN cannot gain full dependent economics, even with a manual
sale assumption. VALUATION_RULES (lines 47-48) repeats the qualified-basis rule
for exact replay. Its fee-assumption rules also preserve unsupported economics.
These are affirmative accepted semantics, not an absence of specification.

DECISIONS' exact replay contract freezes request defaults, execution/order/rounding
and one versioned implementation for public calculation and replay; new financial
behavior requires a new execution version. Plans 073 and 075 preserve admission.
Plans 076/077 add saving and explicit revisions, not a new sale-admission rule.
Plan 079 verifies/replays saved rows before presenting summaries. Plan 081 supplies
settings/profiles, excludes manual sale price from profiles and changes no formula
or snapshot schema. Phase 8 Plan 084 preserves financial versions while adding
explanatory frozen component context. Phase 9 Plans 085/086 add public shell and
read-only private document memory, with no offline calculation or financial rewrite.
DATA_MODEL and REQUIREMENTS_TRACEABILITY retain these bounded distinctions.

Runtime confirms the contract: economics_v1.py line 391 returns whenever
status is not SUPPORTED or market source is absent, before selecting MANUAL at line 394.
test_economics.py::test_non_supported_basis_never_gains_full_economics explicitly
tests MANUAL with every unsupported status. Snapshot admission tests cover both
sale modes across all four market views and statuses, retaining null full finances.
Both files passed in this review's 112-test selection.

UI confirms deliberate coupling: Deal.tsx discloses unavailable full net/profit/ROI
for unsupported market basis, and revision admission says MANUAL does not waive
evidence admission. Deal.test.tsx preserves these unavailable states. Historical
UI reads server replay projections. Client code does not calculate money.

Decision: stop on the explicit governing-contract condition. Path A is not safe.
Path B would be required for newly approved financial semantics, but it is not
implemented while this governing-contract stop applies. No accepted decision or
historical specification is rewritten. The separate product decision must define
manual arithmetic availability alongside unchanged market/physical qualifications.
