# One authorized Sol comparison — 2026-10-03

Brian authorized only lifetime attempt **9**, G06 with requested model ID
`gpt-6.1-sol`, paired with Luna's completed attempt **8**. Accepted r3 publication:
`c89583e40eb1c62620c1162bd1ac0c23bbf51c56`. Application baseline: `d839e51b65f9156e5829740c08d52b59be4c4ec4`.
The private `recognition-14a-sol-v1` amendment binds that history, original approval,
first eight attempt records, frozen prepared inputs, prior result and exact request.
Attempt 10 remains unauthorized. The original Luna approval/protocol is preserved.

The model ID is the sole request-body change. Exact approved transmitted G06 image
bytes and sanitized text, developer instructions, strict schema, preprocessing,
`detail:high`, Medium reasoning, `max_output_tokens:16384`, 180-second deadline,
`service_tier:default`, `store:false`, and explicit developer-only cache boundary
with 30m TTL remain unchanged. No tools, browsing, old answers/reasoning, expected
labels, filenames or catalog references were sent. No inference access probe or
token-counting request occurred. One project-bound model metadata GET passed before
dispatch; the completed structured result confirms this configuration for this call.

## Sol-specific admission

Official [Sol specification](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
and [Standard pricing](https://developers.openai.com/api/docs/pricing), checked
2026-10-03: per million tokens, USD 2 input, 0.10 cached input, 2.50 cache write,
10 output. Above 272,000 input tokens, input/cache rates double and output is USD 15.
The published context window is 1,050,000; maximum output is 128,000. Admission
conservatively reserves the entire context ceiling as input, including images,
instructions/framing/schema, **plus** the approved 16,384 output allowance. This
over-reserves shared context and assumes no cache discount or image multiplier.

`(1050000 × 5.00 + 16384 × 15.00) / 1000000 = USD 5.495760`.
Previous reservations USD 1.877792 remain encumbered. Total USD 7.373552 stays
within the unchanged USD 10 lifetime cap. Standard global `api.openai.com` processing
has no regional/fast surcharge. Cache writes use the highest applicable input rate;
reasoning is already within output. [Cache rules](https://developers.openai.com/api/docs/guides/prompt-caching)
support explicit breakpoints and 30m TTL for this generation. Existing standard
retention acceptance and disabled project sharing remain in force; `store:false`
does not promise zero retention.

Reservation is durable before dispatch; any failed/interrupted/uncertain request
consumes attempt 9. Repeat dispatch is refused. No retry, fallback, reset, credits,
auto-recharge, database/catalog work or broader evaluation is authorized.
