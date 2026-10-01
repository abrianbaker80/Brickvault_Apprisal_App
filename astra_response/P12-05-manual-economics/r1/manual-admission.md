# MANUAL admission and honest qualifications

Sale modes are exactly MANUAL and SELECTED_MARKET. MANUAL requires an explicit
nonnegative bounded decimal money string, including valid zero; a manual price is
forbidden in SELECTED_MARKET. Fee mode is a separate MANUAL/CALCULATED choice.
Invalid, missing, negative and unsupported money validation remains unchanged.

Request.assumptions records MANUAL provenance. DealSummary carries valuation
status/reasons/evidence_quality and separate market_value/market_subset_value/
expected_sale/financial fields. It has no independently named calculation-
availability status. Although nullable amounts can physically contain numbers
with UNKNOWN, accepted V1/UI semantics explicitly prohibit full dependent finances
for that status. Filling them without changing the governing semantics is unsafe.

The desired future behavior is arithmetic from an explicit assumption while market
evidence/status/reasons stay UNKNOWN, without treating the assumption as provider
evidence or bypassing physical/basis/expiry safeguards. Existing fields offer
some representation, but this slice cannot declare their meaning changed.
The specific blocker is the governing contract, not a proven need for a new enum
or larger database/schema redesign.

Exact admission change: none. MANUAL+UNKNOWN remains unavailable in current V1;
MANUAL+SUPPORTED uses the manual amount, independent of the supported market amount.
SELECTED_MARKET admission remains unchanged. No provider lookup/dispatch was added
or used; offline fixtures deny network access. No UI/API/generated-contract changes
or request-lifecycle changes occur.
