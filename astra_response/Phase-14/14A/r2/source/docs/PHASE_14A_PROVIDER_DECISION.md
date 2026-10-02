# Phase 14A provider, privacy and cost decision

## Current approved admission — 2026-10-02

Brian superseded the USD 0.25 lifetime cap with **USD 10.00**, retaining ten total
inference attempts, exact `gpt-6-luna`, the exact approved sample and standard API
handling. Counting-endpoint clarification is no longer a prerequisite. No counting
request or photo preflight was made. The six-request partial run stopped at G06;
see the [pilot result](PHASE_14A_PILOT.md#current-execution-result--2026-10-02-amended-approval).

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

## Earlier provider decision (superseded status)

The following preserves the earlier cap and admission pause. Current authority and
execution evidence are above; the historical blocking language is no longer current.

**2026-10-02 continuation: Brian approved GPT-6 Luna, USD 0.25 total and ten total
inference attempts. Sharing is verified and the sample is prepared. Live execution is blocked on final
sample confirmation, catalog/project verification and the image-token bound.** This replaces the earlier GPT-4.1 mini proposal;
the published r1 package preserves that historical proposal. No fallback is allowed.

## Verified model and request

The exact API ID is `gpt-6-luna`. Official documentation lists image input,
structured output, Responses, and prompt caching. The implementation selects
Responses with `reasoning.effort: medium`, `service_tier: default` (Standard),
`store: false`, and `max_output_tokens: 2048`. Temperature is omitted. No tools,
background calls, SDK retries, warming calls or fallback are enabled. API project
access is still unverified; public documentation cannot establish entitlement.
[Model](https://developers.openai.com/api/docs/models/gpt-6-luna),
[migration parameters](https://developers.openai.com/api/docs/guides/latest-model),
[structured output](https://developers.openai.com/api/docs/guides/structured-outputs).

## Actual account observation

After Brian saved the change, a fresh authenticated read confirmed API input/output,
Playground feedback and evaluation/fine-tuning sharing all disabled organization-wide,
including Brickvault. The private account-review receipt records the selected project
and verification time. The earlier all-project opt-in is historical. The agent changed
no account setting. A local API key file is now present; no key value was displayed.

Brian accepted standard abuse monitoring of up to 30 days and applicable safety/legal
exceptions. `store=false` is not zero retention and does not disable prompt caching.
The approved [image policy](IMAGE_PRIVACY_POLICY.md) remains unchanged.
[Official data controls](https://developers.openai.com/api/docs/guides/your-data).

## Stable prefix and caching

Official GPT-5.6-and-later controls support explicit cache boundaries. The request
uses `prompt_cache_options: {mode: explicit, ttl: 30m}` and a breakpoint at the end
of the stable developer instructions. The output schema is stable; changing photos
and sanitized listing text follow the boundary and are not written to the prompt
cache. No filler is added to reach the 1,024-token cache threshold. No cache hit or
savings are promised. The 30-minute TTL is a minimum; documented encrypted KV-cache
retention can extend to 24 hours. The prefix contains general instructions, without
sample photos, listing text, labels, filenames, timestamps or unique identifiers.
[Cache controls and pricing](https://developers.openai.com/api/docs/guides/prompt-caching).

## Dated prices and unresolved admission bound

Official Standard prices checked 2026-10-02, USD per million tokens:

| Ordinary input | Cached input | Cache write | Total output |
| --- | --- | --- | --- |
| 0.10 | 0.01 | 0.125 | 0.50 |

Cache writes replace ordinary input pricing; they are not additive. Reasoning is
included in total output and the 2,048-token output ceiling. Above 272,000 input
tokens, input/cache rates double and output is multiplied by 1.5. This pilot uses
the global endpoint and Standard processing, with no regional or Fast premium.
[Pricing](https://developers.openai.com/api/docs/pricing).

**The official image sizing/multiplier table and interactive image-cost calculator
omit GPT-6 Luna.** No verified per-image upper bound has been established for the
approved 1024-square derivatives. The earlier model's multiplier and $0.02 reservation
are removed. `input_token_bound` explicitly refuses live dispatch until that provider
fact is resolved; there is no CLI bypass. Tests inject a fixture bound and cannot
establish real image cost. This is an unresolved gate, not a completed live integration.
[Image billing rules](https://developers.openai.com/api/docs/guides/images-vision),
[official calculator](https://developers.openai.com/api/docs/guides/image-cost-calculator).
The documented token-count endpoint could count images, but its billing/privacy
basis was not sufficiently verified here; no extra photo request was added.

Once an input bound is verified, admission computes its worst-case cache-write cost
plus maximum output, with applicable long-context multipliers and no cache hit.
The existing ledger reserves that amount durably before dispatch. All reservations
remain encumbered, including successful, failed, uncertain and interrupted calls.
It rejects a request that would exceed the lifetime $0.25 or ten-attempt ceiling.
Reported token partitions produce a separate labeled cost estimate; missing cache
details use the highest input rate, and missing usage remains unknown. No invoice
cost is invented or reasoning charged twice.

## Approved limits and remaining setup

6–8 groups, 1–2 photos each; originals at most 25 MiB; metadata-free JPEG copies at
most 1024×1024 and 1 MiB; optional sanitized text at most 1,000 UTF-8 bytes; 2,048
maximum total output tokens; 60-second deadline. Originals remain unchanged.
Visible personal information requires separate review/removal. Expected identities
and revealing filenames never enter the provider request. No photo-folder scans.

Seven groups and 13 selected photos are prepared privately for final sample review.
All original hashes match their pre-preparation hashes. Metadata-free derivatives
passed the existing size/format checks. A local review document lists each exact copy,
listing text and expected labels. G04 tentative identities remain unscored; G06 has
eight exact labels plus separate partial/combined-parts notes. Schema v2 supports up
to 12 objects/labels, with the same 2,048 total output-token ceiling. Dense lots may
still exhaust the output budget; an incomplete response stops the pilot without retry.
The selected catalog subset, project/model access and image billing bound still need
verification. No final sample approval or inference is inferred from data collection.

**Current totals: zero live attempts, zero result reuses, USD 0 spent/reserved;
USD 0.25 and ten attempts remain.** Seven groups/13 photos are prepared and the local
key file is present. Published r1 remains historical; update after live gates resolve.


## Approved sample and preflight result

Brian explicitly approved the seven prepared groups/13 photos and listing texts,
conditional on the remaining checks. The private sample approval binds prepared.json
and the review document by SHA-256. A project-scoped model metadata GET succeeded:
`gpt-6-luna` is visible to the supplied key. This is not image/schema inference proof.
No photos or inference prompt were sent; attempts/spend/reuses remain zero.

The owned loopback development database at 127.0.0.1:55432 was stopped. It was started
for read-only diagnosis and restored to stopped. Ownership matched. Its installed
revision is `0012_product_identity_qualifiers`; this checkout requires
`0017_listing_images`. The catalog guard correctly refuses access. Applying existing
migrations 0013 through 0017 would change the development schema and is pending
Brian's authorization; no migration, catalog import or production access occurred.
The model-specific image-token billing bound remains unverified after a focused
refresh of official documentation; no fallback or cost-gate bypass is enabled.


The authorized development catch-up through 0017 passed. The accepted catalog
resolves the three confirmed sets but has no BrickLink minifigure mappings for the
14 confirmed figure IDs. Token-counting billing/model/data-handling terms remain
unconfirmed; no counting submission was made. See the existing
[pilot report](PHASE_14A_PILOT.md#authorized-development-catch-up-and-cost-admission--2026-10-02)
for the recovery, migration, preservation and cost-admission evidence.
