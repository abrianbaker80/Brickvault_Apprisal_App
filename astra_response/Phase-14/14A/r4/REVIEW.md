# READY FOR PHASE 14A MODEL-COMPARISON REVIEW

**One authorized Sol request completed; exact G06 agreement did not improve.**
G06 attempt 9 (`gpt-6.1-sol`) is paired with Luna attempt 8 under the same exact
approved input and protocol. [Accepted r3](../r3/REVIEW.md) remains unchanged.
Application baseline `d839e51b65f9156e5829740c08d52b59be4c4ec4`; comparison baseline `c89583e40eb1c62620c1162bd1ac0c23bbf51c56`.

| G06 measurement | Luna attempt 8 | Sol attempt 9 |
| --- | ---: | ---: |
| Completed | Yes | Yes |
| Exact top-1 / top-3 | 0/8 / 0/8 | 0/8 / 0/8 |
| Confirmed identities omitted from all three ranks | 8 | 8 |
| Objects / abstentions | 11 / 9 | 11 / 3 |
| Distinct unmatched proposals | 2 | 8 |
| Reported input tokens | 1248 | 1248 |
| Reported output tokens | 3272 | 4061 |
| Reasoning tokens, included in output | 2477 | 2070 |
| Cached input / cache writes | 0 / 0 | 0 / 0 |
| Latency, seconds | 28.857528 | 90.569283 |
| Token-estimated USD | 0.0017608 | 0.043106 |
| Retained reservation USD | 0.242788 | 5.495760 |

Both omit all eight confirmed labels. G06 labels are not exhaustive; unmatched
proposals are not automatically proven wrong-object identifications. Exact identity
lists remain private. Canonical G06 recognition/resolution is separate: no proposal
resolves through the accepted projection, and figure mappings remain unresolved.
No mapping, automatic confirmation or valuation promotion was made.

Luna's original and cumulative whole-sample **3/17** remain unchanged. Sol's single
G06 answer is not spliced into either model's full-sample accuracy. Listing evidence
was included. This comparison is preliminary, not production qualification.

## Lifetime and limits

**9 lifetime inference requests**, 14100 input / 13119 output tokens,
including 9272 reasoning tokens. Token-estimated lifetime cost
**USD 0.0489202**; actual invoice charges unavailable. All old reservations retained:
**USD 7.373552** encumbered, **USD 2.626448** unreserved under USD 10.
Attempt 10 is unauthorized. One metadata GET was added; no token counting/access
inference probe, retry, fallback or other model/sample change occurred.

## Review package

- [Model comparison amendment and Sol pricing admission](model-comparison-amendment.md)
- [Paired results, usage, latency, costs and lifetime accounting](results.md)
- [Three focused checks and targeted static verification](validation.txt)
- [Exact changed-file inventory and hashes](changed-files.md)
- [Changes against accepted r3](amendment.patch)
- [Cumulative application patch against the local baseline](cumulative.patch)
- [Existing Phase 14A report](source/docs/PHASE_14A_PILOT.md)
- [Adapter, one-call guard and distinct scoring source](source/services/api/src/brickvault_api/recognition/pilot.py)

11 files change from r3; 13 form the cumulative delivery.
All eight prior attempt records, saved results, parameters, usage, hashes and
reservations are preserved. Thirty-three private file hashes and three protected
files match. Source changes are uncommitted in main, index empty, main unpushed.
Development stays stopped and recovery retained. Only this sanitized r4 package
is published on astra-response; r1-r3 are preserved. No private photos, labels,
listing text, credentials, asset paths or reasoning text are included.

**Stop for review. No further calls, tuning, comparison, production or later phase.**
