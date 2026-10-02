# Phase 14A provider, privacy and cost decision

**2026-10-02: proposed; Brian's combined live approval remains pending.**
No API key was found in the process environment or conventional repository env
files. Presence checks exposed no values. No account entitlement, sharing settings
or special retention arrangement has been verified. No authenticated call was made.
Brian replied that he would return to the bundled request; that is not approval.

## One recommended model

Use OpenAI `gpt-4.1-mini-2025-04-14`, a pinned model supporting image input and
strict structured output. Current standard token rates are USD 0.40/million input
and USD 1.60/million output. Its small cost and non-reasoning output make it suitable
for an initial direct multimodal baseline; suitability for LEGO remains unmeasured.
[Official model and pricing](https://developers.openai.com/api/docs/models/gpt-4.1-mini).
[Structured output contract](https://developers.openai.com/api/docs/guides/structured-outputs).

Gemini `gemini-2.5-flash` also documents image input and structured output. Current
standard rates are USD 0.30/million text/image/video input and USD 2.50/million output,
including thinking. Paid-service data handling depends on the actual project's
billing state. This comparison selects only OpenAI; no Gemini adapter is implemented.
[Model](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash),
[structured output](https://ai.google.dev/gemini-api/docs/structured-output),
[pricing](https://ai.google.dev/gemini-api/docs/pricing).

## Account and photo treatment

For the selected OpenAI API endpoint, training is off by default unless the customer
opts in. Standard abuse-monitoring retention can last up to 30 days. `store:false`
avoids optional stored completions; it does not eliminate abuse monitoring. Image
safety review and legal exceptions can retain content. No Zero Data Retention
entitlement is assumed. Brian must confirm the selected project's voluntary data
sharing is disabled and accept this handling before the approval file can be sealed.
[OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data).

For comparison, Gemini paid services do not use prompts/responses for product
improvement, but retain logs for a limited abuse-prevention period. The paid API
treatment requires an active billing account on the project; free-service treatment
can differ, including product improvement and human review.
[Gemini terms](https://ai.google.dev/gemini-api/terms).

Only explicitly selected, rights-cleared photos and sanitized optional listing text
may be submitted. Display rights for catalog images do not authorize AI submission.
The existing [approved image policy](IMAGE_PRIVACY_POLICY.md) is unchanged. This
proposal grants no permission for other assets or future use. Original bytes remain
unchanged; metadata-free copies are made locally. Brian must inspect visible personal
content and supply sanitized crops where needed; metadata stripping does not remove
faces, messages or addresses embedded in pixels.

## Proposed spending and input limits

| Limit | Enforced value |
| --- | --- |
| Whole pilot | USD 0.25 cap, separately approved; at most 10 attempts |
| Per attempt reservation | USD 0.02, retained even on failure or interruption |
| Sample | 6–8 selected groups; 1–2 photos per group |
| Original file | At most 25 MiB; existing decoder format/pixel/frame guards |
| Transmitted copy | JPEG, at most 1024×1024 and 1 MiB per image |
| Listing text | At most 1,000 UTF-8 bytes |
| Prompt/schema/evidence | At most 16,000 UTF-8 bytes, excluding image data |
| HTTP request / response | At most 3 MiB / 256 KiB |
| Output | At most 2,048 tokens, one completion |
| Timeout | 60-second wall deadline, including DNS/TLS wait |
| Repeats | Zero automatic retries or model fallback; completed groups skipped |

The image accounting uses 32-pixel patches and the documented 1.62 multiplier:
two 1024-square images cost at most 3,318 input tokens. Treating every allowed text
byte as a token and adding 4,096 framing tokens gives a conservative estimate:
`(16000 + 3318 + 4096) × 0.40 / 1000000 + 2048 × 1.60 / 1000000 = $0.0126424`.
The larger $0.02 reservation covers each request. Ten reservations total $0.20;
admission also enforces Brian's actual approved cap. Six to eight initial requests
reserve $0.12–$0.16. These are usage estimates, not invoice totals or tax estimates.
Reported tokens produce a separate USD estimate without assuming cache discounts.
[Image token calculation](https://developers.openai.com/api/docs/guides/images-vision).

## Combined decision still required

Approve the exact provider/model, dollar cap, limits and account handling; select
exact files for the sample below with submission rights and privacy review; identify
confirmed expected identities; choose an existing key entered through local hidden
input or secure creation of a new key. Never send the key in chat or argv.
The protected approval binds sample, catalog subset and protocol SHA-256 digests.
Code cannot verify a human authorization independently: the approval record is
written only after Brian gives it. Documentation or stored credentials alone do not
authorize live use. Recheck current pricing before a later authorization.

| Group | Requested photo category |
| --- | --- |
| G01 | Clear complete set |
| G02–G03 | Two similar-looking alternatives |
| G04 | Incomplete or partly obscured build |
| G05 | Minifigure |
| G06 | Mixed lot |
| G07 | Insufficient evidence, custom build or non-LEGO negative |
| G08 | Optional additional negative or difficult example |

No files have been selected, scanned or transmitted. The relevant approximately
25 catalog identities will be selected with these examples, including alternatives,
then projected read-only from the existing accepted development catalog.
