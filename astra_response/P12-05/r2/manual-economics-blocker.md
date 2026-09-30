# Gate 5 manual Deal Economics blocker

The actual production UI sent one POST to `/api/sets/75331-1/forecast-preview`.
The server received MANUAL sale basis and manual_sale_price=200. HTTP 200 returned
UNKNOWN; this is a server calculation result, not a transport, TLS or UI-input failure.

| Input | Value (USD) |
| --- | --- |
| Purchase | 100 |
| Manual item sale | 200 |
| Shipping charged | 10 |
| Selling fee | 15 |
| Shipping paid | 8 |
| Other selling costs | 2 |
| Fixed acquisition cost | 5 |

| Result | Stated manual-assumption arithmetic | Actual server result |
| --- | --- | --- |
| Item sale | 200.00 | null |
| Gross proceeds | 210.00 | null |
| Selling costs | 25.00 | 25.00 |
| Net proceeds before acquisition | 185.00 | null |
| Total acquisition | 105.00 | 105.00 |
| Profit | 80.00 | null |
| ROI | 76.2% | null |

The provider market remains UNKNOWN with reasons accepted_strategy_physical_assessment
and missing_or_incompatible_or_ambiguous_mapping. Those facts must remain honest;
manual arithmetic is an assumption and must not turn them into provider evidence.

## Bounded root-cause diagnosis

`services/api/src/brickvault_api/economics_v1.py:391` returns before the
MANUAL sale selection at line 394:

```python
if value.status != Status.SUPPORTED or source is None:
    return CalculationV1(exact=facts, presentation=result)
# ...
sale = manual if request.sale_basis == "MANUAL" else source
```

The checked-out source equals the accepted release wheel member byte-for-byte
after line-ending normalization. Accepted wheel SHA-256:
`a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6`.
This is local accepted-artifact corroboration; no fresh installed-file SSH check
was run. The live response independently confirms the matching admission behavior.

The current immutable v1 calculation intentionally enforces supported market
admission even for MANUAL. The new acceptance request expects manual assumption
economics while market data is unavailable; that contract mismatch is material.
No retry, patch, market activation or workaround was performed. A separate repair
must review admission semantics, qualifications, snapshot/calculation versions and
saved-history replay compatibility before implementation or deployment.

One UNSAVED/PENDING forecast capture was created by this ordinary calculation.
It was never saved. Its deletion guard prevents deletion before eligibility expiry;
normal owner cleanup is invoked by a later preview. [Residual/cleanup](cleanup-logout.md).
