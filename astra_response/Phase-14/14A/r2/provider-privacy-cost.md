# Approved provider, privacy and cost controls

## Current approved admission — 2026-10-02

Brian superseded the USD 0.25 lifetime cap with **USD 10.00**, retaining ten total
inference attempts, exact `gpt-6-luna`, the exact approved sample and standard API
handling. Counting-endpoint clarification is no longer a prerequisite. No counting
request or photo preflight was made. The six-request partial run stopped at G06;
see the [pilot result](sample-results.md).

### Conservative reservation

The official [model specification](https://developers.openai.com/api/docs/models/gpt-6-luna)
checked on 2026-10-02 publishes **922,000 maximum input tokens**. Every accepted
request is reserved at that entire input ceiling, including images, instructions
and strict schema. This does not infer an undocumented per-image multiplier.
Oversized requests are rejected; truncation, tools, automatic retries and fallback
are absent. The [pricing](https://developers.openai.com/api/docs/pricing) rates are
USD 0.10 ordinary input, 0.01 cached input, 0.125 cache write and 0.50 output per
million tokens. Above 272,000 input tokens, input/cache rates double and output
rates multiply by 1.5. Standard global processing is explicitly selected.

Worst case, without cache savings:
`(922000 × 0.125 × 2 + 2048 × 0.50 × 1.5) / 1000000 = USD 0.232036/request`.
All ten attempts would reserve USD 2.320360. Durable reservations precede dispatch,
remain encumbered for success/failure/interruption and stop the next request if its
reservation would exceed USD 10.00. The revised approval was sealed once; no
ledger reset occurred. All six sent calls reported token partitions. Their estimated
cost is USD 0.0036058, separate from USD 1.392216 in retained reservations. Actual
invoice/billing cost is unavailable. Reasoning is included in output, not added twice.

### Privacy and request evidence

The approved metadata-free derivatives and sanitized text were sent anonymously,
with `detail:high`, `store:false`, no tools and no expected labels/catalog payload.
Project sharing remains verified disabled. The existing explicit prompt-cache
boundary includes only stable developer instructions; dynamic photos/text are after
it. The approved Standard handling, up-to-30-day abuse monitoring, applicable image
safety/legal exceptions and documented cache retention remain in force. `store:false`
does not promise zero retention. [Data controls](https://developers.openai.com/api/docs/guides/your-data),
[cache controls](https://developers.openai.com/api/docs/guides/prompt-caching).
A fresh metadata GET passed; the six Responses requests establish actual model/schema
processing for this workload. No support inquiry was sent by the agent.

The image-token formula and counting billing/retention questions remain unanswered,
but they do not block this approved model-ceiling reservation method. No source
mapping question was reopened. Raw agreement includes exact unmapped BrickLink IDs;
canonical resolution stays separate and cannot promote a prediction to truth/value.
