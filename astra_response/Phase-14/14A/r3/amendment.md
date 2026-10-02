# Approved versioned request-limit amendment

Brian accepted r2 at `108f7f6d65a38ebead7701d3c0f7f2d62ed3b5ab` as valid partial evidence without closing 14A.
`recognition-14a-limits-v1` authorizes **exactly two fresh calls**, completed in order:

| Lifetime attempt | Group | Authorization | Maximum output | Deadline |
| --- | --- | --- | ---: | ---: |
| 7 | G07 | Previously unattempted case, once | 16384 | 180 seconds |
| 8 | G06 | Sole manual retry, linked to failed attempt 6 | 16384 | 180 seconds |

Keep `gpt-6-luna`, Medium reasoning, Standard/default, `store:false`, exact photos/texts,
prompt, strict schema, high image detail/resolution, preprocessing, catalog rules and
scoring. Only output allowance and deadline change. No previous reasoning, answers
or expected labels are supplied as input. G01–G05 are never resent or overwritten.
Original protocol SHA-256: `4f8f47a56907a3c7a82012f87f2c83c8ab36bc43fb56c4c441de509247adc7bc`.
Amended protocol SHA-256: `1809a6dfd05299ffd4f9dd39b505311366cc22eff5d257f4d2f0e5b0ea4ebcaf`.

The owner-protected immutable amendment binds the original approval/ledger, frozen
input digests and original six records. Its two new attempts carry the amended
protocol and request limits, distinct output filenames and G06 predecessor link.
The original ledger stop remains set; only this explicit path can make those calls.
It refuses any repeat/resume or extra group. A new privacy/authentication/accounting/
budget or uncertain transport failure stops dispatch. Known unusable output is kept,
not retried. No framework, database operation or new model/provider path was added.

The USD 10.00 lifetime cap and ten-attempt ceiling remain. The two unused attempts
are **not authorized**. Admission uses the previously verified full model input bound,
922,000, highest input/cache-write rates, long-context multipliers and new output limit:
`(922000 × 0.125 × 2 + 16384 × 0.50 × 1.5) / 1000000 = USD 0.242788/request`.
No counting call/cache-saving assumption or old reservation release was used.
Retained lifetime reservations are USD 1.877792. Standard privacy/data-sharing checks
and prior data-handling acceptance remain intact.

The original G06 stays failed/counted. Cumulative coverage takes only the sole retry;
no best-of answer or duplicated expected identity count. Original results, amended
results and cumulative coverage are explicitly separated in [results](results.md).
[Original provider evidence](../r2/provider-privacy-cost.md) is reused; [current source
decision](source/docs/PHASE_14A_PROVIDER_DECISION.md) records the amended limits.
Stop for quality review; no parameter tuning or model comparison is authorized.
