# Phase 14A local recognition pilot

## One Sol model-comparison result — 2026-10-03

**READY FOR PHASE 14A MODEL-COMPARISON REVIEW.**


**One additional live inference request was sent, lifetime attempt 9; it completed.**
Both models are compared against the same eight independently confirmed identities,
with exact kind + namespace + identifier matching and unchanged rank scoring.

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

Both models omit all eight confirmed identities at top-3. Exact omitted-ID and
unmatched-ID lists remain in the protected private score review, outside this
publication. G06 labels are **not exhaustive**; unmatched proposals are not
automatically proven wrong-object identifications. Confidence remains uncalibrated.
Sol produced more proposals without improving exact agreement on this group.

## Canonical resolution is separate

Neither model resolves any G06 proposal through the retained accepted catalog
projection; all eight confirmed G06 figure labels remain canonically unresolved.
Across the original pilot, three set labels resolve and fourteen BrickLink figure
labels remain unmapped. Missing mappings do not cause the raw recognition misses.
No mapping, automatic confirmation, valuation promotion or catalog write occurred.

Luna's original whole-sample **3/17 top-1 and top-3** is unchanged, as is its r3
cumulative **3/17** (sets 3/3, figures 0/14). Sol has only this independent G06
measurement. Its answer is never combined with Luna's other answers as either
model's full-sample accuracy. This is preliminary evidence, not production qualification.

## Lifetime accounting

| Scope | Requests | Input | Output | Reasoning included | Estimated USD | Retained reservations USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Prior Luna history | 8 | 12852 | 9058 | 7202 | 0.0058142 | 1.877792 |
| Sol G06 comparison | 1 | 1248 | 4061 | 2070 | 0.043106 | 5.495760 |
| Lifetime | 9 | 14100 | 13119 | 9272 | 0.0489202 | 7.373552 |

All nine requests report usage and token partitions. Actual invoice charges are
unavailable; costs are dated token-based estimates. Sol calculation is
`(1248 × 2 + 4061 × 10) / 1000000 = USD 0.043106`; cache/write counts are zero.
Sol's one-request average/effective cost per G06 group is USD 0.043106. The mixed-model
lifetime average is approximately USD 0.005435578/request; allocation
per seven distinct groups is USD 0.006988600, including repeats. These
allocations are workload evidence, not per-image tariffs or full-model comparisons.
There are 13 unique approved images and 15 sent image inputs across all nine calls.
Unreserved allowance is **USD 2.626448**; reservations remain retained rather than
being described as actual spending. Attempt 10 and all further calls are unauthorized.

## Preserved state and limits

The eight old attempt JSON records are unchanged by field/value; 33 frozen private
files (including all 13 derivatives) and three protected files match their pre-r4
hashes. Original r2/r3 result/evaluation/publication files remain unchanged and
readable. Only G06 was resubmitted, once, with a separate linked result. Development
remains stopped and the protected recovery copy retained. Main remains at `d839e51b65f9156e5829740c08d52b59be4c4ec4`,
unpushed with empty index. No broader suite, build, database/catalog access, mapping,
production deployment, prompt tuning or later-phase work occurred. Stop for review.

### Comparison amendment and cost admission


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

**Phase 14 IN PROGRESS — two-call continuation finished; recognition qualification unestablished.**
Phase 13 remains CLOSED. This optional CLI does not alter the running application.
See [Plan 104](plans/104-recognition-quality-pilot.md) and the
[provider/privacy/cost decision](PHASE_14A_PROVIDER_DECISION.md).

## Two-call continuation result — 2026-10-02

**READY FOR PHASE 14A CONTINUATION REVIEW.** Brian accepted r2 as honest partial
pilot evidence, not completed recognition qualification. The authorized two-call
continuation is finished and stopped. Phase 14A remains open for review.

### Versioned limit amendment

`recognition-14a-limits-v1` changes only `max_output_tokens: 2048 → 16384` and the
transport deadline `60 → 180` seconds for lifetime attempts **7 (G07)** and **8 (G06)**.
Model `gpt-6-luna`, Medium reasoning, Standard processing, `store:false`, prompt,
strict recognition schema, high image detail, preprocessing, exact approved inputs,
catalog rules and scoring are unchanged. G07 went first. G06 attempt 8 links to
failed predecessor 6; no previous reasoning, output or expected labels was sent.
The original approval and G01–G05 files remain under their original parameters.

Original protocol SHA-256: `4f8f47a56907a3c7a82012f87f2c83c8ab36bc43fb56c4c441de509247adc7bc`. Amended protocol SHA-256: `1809a6dfd05299ffd4f9dd39b505311366cc22eff5d257f4d2f0e5b0ea4ebcaf`.
The private amendment binds the accepted r2 commit, original approval/ledger/attempt
prefix, frozen inputs and new protocol. The original six attempt records are preserved
exactly by JSON field/value, and all fifteen preserved r2 file hashes match.
No ledger reset, result overwrite or reservation release occurred.

### Three distinct result views

**Original protocol (r2):** six requests, five completed groups, original G06 incomplete,
G07 unattempted; raw top-1/top-3 **3/17**, cost estimate **USD 0.0036058**. This recorded
view is unchanged. Three sets matched; five confirmed figure IDs were omitted in
G02/G03, and G05 proposed a different figure ID. Eight G06 identities had no completed
answer. Original G04 was an unscored mixed-set abstention.

**Amended protocol:** exactly two additional completed requests:

| Lifetime attempt | Group | Result | Raw identity agreement | Input | Output | Reasoning within output | Estimated USD | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 7 | G07 | `custom_build`, no official identity proposed | Correct confirmed MOC outcome | 2486 | 398 | 322 | 0.0004476 | 6.160784 |
| 8 | G06 sole retry | 11 objects: 9 unknown, 2 figure proposals | 0 of 8 confirmed figure IDs at top-1/top-3 | 1248 | 3272 | 2477 | 0.0017608 | 28.857528 |

The two G06 proposals do not match any confirmed label. G06 labels are not exhaustive:
partial/combined figures remain unscored, so unmatched suggestions are not all promoted
to verified wrong-object judgments. Nine unknown objects are distinct from its earlier
processing failure. No reasoning text or private listing/figure labels is published.
Increasing output space supplied a usable answer; exact figure recognition did not improve.

**Cumulative sample coverage (mixed limits, explicitly labeled):** all **7 groups/13
approved images** now have completed structured results. Eight lifetime requests sent
**14 image inputs**, including the repeated approved G06 photo. Original G06 remains
failed and counted. Only its sole authorized retry supplies group coverage; no identity
is counted twice and no best-of-retries selection is made.

- Raw top-1/top-3 **3/17 (17.65%)** with the original independently confirmed denominator.
- Sets **3/3 exact**; minifigures **0/14 exact**. Listing text was included throughout.
- Confirmed outcomes **6/6**; G07 correctly returns a custom build. This outcome count
  does not establish exact identity accuracy. G04 identities stay unscored.
- Cumulative abstentions: 11 objects. Confidence remains uncalibrated. G06's non-exhaustive
  labels cannot support an exhaustive false-suggestion rate.
- Canonical integration remains separate: **3 expected set labels resolve; 14 figure
  labels remain unresolved**. All three correct set predictions resolve. This is a frozen
  three-reference projection, not full-catalog retrieval. No mappings/confirmations/
  valuation evidence were written. Missing mappings do not explain raw figure misses.

### Lifetime cost and workload

The conservative new reservation is
`(922000 × 0.125 × 2 + 16384 × 0.50 × 1.5) / 1000000 = USD 0.242788/request`.
Both requests were admitted within the unchanged USD 10.00 lifetime cap, without
cache savings or releasing any original reservation. See the [provider decision](PHASE_14A_PROVIDER_DECISION.md).

| Accounting scope | Requests | Input | Total output | Reasoning included | Estimated USD | Retained reservations USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Original r2 | 6 | 9118 | 5388 | 4403 | 0.0036058 | 1.392216 |
| Amended calls | 2 | 3734 | 3670 | 2799 | 0.0022084 | 0.485576 |
| Lifetime | 8 | 12852 | 9058 | 7202 | 0.0058142 | 1.877792 |

All calls reported usage, with cached/write tokens zero. **Actual invoice/billing
amount remains unavailable**. Estimates apply the dated Standard rates; reasoning
is already included in output. New requests averaged USD 0.0011042/request. Lifetime
average is USD 0.000726775/request; effective cost per distinct attempted group is
USD 0.0008306, including the failed first G06 call. Per transmitted image input is
USD 0.0004153, an allocation rather than an image-only billing rate. Unreserved
allowance is **USD 8.122208**. Two lifetime attempts remain, **neither authorized**.
No model metadata/counting call, automatic retry/fallback or result reuse was added.

### Focused validation and preserved state

Exactly three affected fixture tests passed in **2.93 seconds** (ten unrelated tests
deselected): amended reservation/output accounting, guarded two-call continuation,
and original-protocol readability. Their fixtures also exercise one uncertain first
call stopping before G06, no repeated continuation, and retained known unusable output.
Ruff lint/format and strict mypy passed for the four edited Python/test files.
No broad suites, builds, provider investigation or prior qualification were repeated.

The exact sample, privacy/account/key receipts, original approval/results/evaluation
and original request parameters are preserved. Development remains stopped and the
protected recovery remains retained; no database work occurred. Protected files
match, main is uncommitted/unpushed and its index is empty. r1/r2 remain intact;
r3 publishes the amendment, new evidence, lifetime accounting and cumulative patch.

The continuation is complete, but recognition qualification is **not** established.
Review the weak minifigure results before any separately authorized model/retrieval
comparison. No further call, tuning cycle, mapping campaign or later phase has begun.

## Current execution result — 2026-10-02 amended approval

**READY FOR PHASE 14A REVIEW — partial sample; stopped at the approved output limit.**
Brian raised the lifetime cap to **USD 10.00**, retained exact `gpt-6-luna` and ten
inference attempts, and removed the counting-endpoint prerequisite. Raw recognition
uses exact kind + namespace + identifier independently of canonical resolution.
The original seven groups/13 photos, listing texts, labels and denominators are frozen.

### Live workload and results

Six Standard Responses requests were sent once, covering six groups/11 prepared
images. Five groups completed; G06 failed and G07 was not attempted. All six calls
returned provider responses and token usage. G06 reported 2,048 output tokens,
all reasoning, and an incomplete response; it produced no completed structured
result. The ledger is stopped, the failed attempt and full reservation are retained,
and no retry or fallback was sent. Four lifetime inference attempts remain.

| Group | Images sent | Processing result | Raw top-1 / top-3 agreement | Expected canonical coverage |
| --- | ---: | --- | --- | --- |
| G01 | 2 | Completed | 1 / 1 of 1 | 1 resolved |
| G02 | 2 | Completed; figure omitted | 1 / 1 of 2 | 1 resolved, 1 unresolved |
| G03 | 2 | Completed; figures omitted | 1 / 1 of 5 | 1 resolved, 4 unresolved |
| G04 | 2 | Mixed-set abstention | Unscored; labels unconfirmed | No confirmed identity denominator |
| G05 | 2 | Completed; different figure ID proposed | 0 / 0 of 1 | 1 unresolved |
| G06 | 1 | Incomplete at output ceiling | 0 / 0 of 8 | 8 unresolved |
| G07 | 0 | Not attempted after stop | Confirmed custom-build outcome unobserved | No expected canonical identity |

**A. Raw recognition agreement:** top-1 **3/17 (17.65%)**; top-3 **3/17 (17.65%)**.
Each independently confirmed identity counts once per group. Failed/unattempted
cases remain in the original denominator; G04 tentative suggestions stay unscored.
Predeclared outcomes agree in **4/6** confirmed groups. One abstaining object and
zero incorrect suggestions at the fixed 0.8 confidence threshold were recorded;
confidence remains uncalibrated. These counts establish selected-sample behavior,
not general accuracy, completeness, quantity or condition detection.

**B. Canonical catalog resolution:** retained accepted-catalog evidence resolves
**3/17** expected labels (the three sets); all **14** BrickLink figure labels remain
unresolved. The three correctly recognized sets resolve exactly. The one different
figure candidate is unresolved in the projection. A frozen three-reference projection
reuses the previous guarded checks, so development stayed stopped. Other identifiers
outside this projection are not claimed absent from the full catalog. No mappings,
imports, aliases, valuation evidence or automatic confirmations were written.

### Cost admission and effective rate

The published model maximum input is **922,000 tokens**, including images, instructions
and schema. Reserve that full ceiling for every valid request, using the highest
input rate (cache write), long-context multipliers and the 2,048 total output ceiling:

`(922000 × 0.125 × 2 + 2048 × 0.50 × 1.5) / 1000000 = USD 0.232036/request`.

Ten such reservations total USD 2.320360, within USD 10.00. No image multiplier,
cache saving or token-counting call is assumed. Oversized input is rejected without
truncation or automatic retry. See the dated [provider decision](PHASE_14A_PROVIDER_DECISION.md).

Reported usage totals **9,118 input + 5,388 output tokens**; output includes **4,403
reasoning tokens**. Cached-input and cache-write usage were both reported as zero.
At the verified Standard global rates, estimated inference cost is **USD 0.0036058**.
This is a token-derived estimate; **no actual invoice/charge amount was supplied**.
It includes the incomplete G06 call and does not double-charge reasoning.

| Group | Input | Output | Reasoning included in output | Estimated USD | Latency seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| G01 | 2501 | 301 | 117 | 0.0004006 | 5.555832 |
| G02 | 1765 | 381 | 206 | 0.0003670 | 5.960073 |
| G03 | 1855 | 949 | 637 | 0.0006600 | 11.610445 |
| G04 | 1118 | 545 | 458 | 0.0003843 | 8.899985 |
| G05 | 631 | 1164 | 937 | 0.0006451 | 14.059835 |
| G06 | 1248 | 2048 | 2048 | 0.0011488 | 22.465451 |

Average estimated cost per sent request and per attempted image group is
**USD 0.00060097** (six requests/groups, eleven image inputs). Approximate effective
cost per sent image is USD 0.00032780; groups contain one or two photos, so this is
an allocation, not an independent per-image billing rate. Total reservations remain
**USD 1.392216**, leaving **USD 8.607784** unreserved. No allowance was reset or
released. Counting submissions, automatic retries and result reuses remain zero.
Two lifetime metadata GETs (one this continuation) sent no photos or inference prompt;
they are reported separately from the six inference requests. No counting charge arose.

### Verification, preservation and review boundary

Six directly affected fixture checks passed in 3.42 seconds; one transport/redaction
check passed in 0.69 seconds after the final diagnostic change. The unmapped-ID
fixture uses a synthetic ID for publication privacy; its focused recheck passed in 0.81 seconds. Ruff lint/format
and strict mypy passed for the six Python files. Fixtures prohibit network access;
these checks establish software behavior, separately from the live evidence above.
No broad suite, frontend/Android build or prior-phase campaign was repeated.

Existing migrations 0013–0017 and runtime grants remain accepted; retained migration
receipts report 69 table-count comparisons, 39 content digests and 56 runtime SELECT
checks passed. The protected recovery copy remains retained. Development stayed
stopped throughout this run. Prepared sample/review hashes and the three protected
file hashes match; credentials stay private, the main index is empty and main is
unpushed. Publication contains sanitized source and counts, without photos, private
listing text, figure labels, credential values or private asset filenames.

**Next decision:** review the partial result. Continuing needs explicit approval for
a manual G06 retry with a revised output/reasoning allowance and subsequent G07 call.
The failed attempt stays counted; neither retry nor parameter change was performed.
Wider Phase 14 comparisons and Phase 15/16 remain outside this execution.

## Earlier preparation and admission record

The following dated record preserves the prior USD 0.25 approval and blocked states.
The amended approval and live result above supersede those current-status claims.

## What runs

From the repository root, use the existing Python environment:

```powershell
& services/api/.venv/Scripts/python.exe -m brickvault_api.recognition --help
```

There is no default live action. Commands operate on one fixed ignored private
directory, `.local/recognition-14a/`, with owner-restricted Windows ACLs or POSIX
permissions. Inputs, credentials and results never belong in the review package.
No new dependency, HTTP API, migration, UI or production service is involved.

| Command | Behavior |
| --- | --- |
| `init` | Create protected directory and empty selection/catalog request templates; refuse existing directory |
| `prepare` | Read only explicitly selected local files; retain originals; save anonymous metadata-free copies and frozen labels |
| `subset` | Export 1–30 exact references from an accepted nonsynthetic development snapshot using existing ownership/query guards |
| `draft-approval` | Create an OFF approval draft bound to prepared inputs, subset and protocol digests |
| `check-model` | With the final private approval/project ID and local key, GET exact model metadata; send no photos or inference prompt; save key/project-bound visibility evidence |
| `seal` | Require completed Brian approval; create immutable initialization marker and durable ledger; refuse repeats |
| `key` | Accept a key through hidden terminal input and write it only to protected storage; refuse overwrite |
| `run` | Validate approval and limits; reserve before dispatch; reuse verified completed results; stop on failure or exhausted budget |
| `report` | Preserve the original-protocol counts, latency, tokens and estimated/reserved USD |
| `continue-approved` | With a recorded v1 amendment, send only G07 then one G06 retry; refuse any repeat/resume or other group |
| `continuation-report` | Separate original results, amended request accounting and cumulative sample coverage; omit private labels/content |

`subset` never starts a database. The owned development database must already be
available through the established local workflow. It cannot target production or
port 5432. Source tests have not exercised a real catalog export in this slice.

## Select and prepare the sample

After `init`, edit private `selection.json` with 6–8 groups. Example shape below is
illustrative, not an approved asset or confirmed answer. Supply an absolute local
path in the private file; never include it in review artifacts.

```json
{
  "groups": [{
    "group": "G01",
    "files": ["<operator-selected absolute local photo path>"],
    "listing_text": "",
    "independently_confirmed": false,
    "labels_exhaustive": false,
    "expected": [],
    "expected_outcome": null,
    "submission_rights_confirmed": false,
    "personal_content_removed": false
  }]
}
```

Repeat for the selected groups. Mark rights/privacy fields true only after actual
review. `expected` entries use `kind` (`set` or `minifigure`), `namespace` and exact
`identifier`, including set suffixes. Expected identities must come from independent
confirmation. `labels_exhaustive` means every distinguishable identity in the group
has been labeled; only such groups support incorrect-confident-suggestion counts.
Negative cases can use confirmed `expected_outcome` and an empty identity list.
Unconfirmed cases show behavior but establish no accuracy. Multiple photos in one
group show the same scene/objects from different views.

`prepare` refuses duplicate photos, indirect paths, network shares, unsupported or
oversized images, animation and unreviewed privacy/rights. Originals are read only.
Review the protected copies visually before the final photo approval. No automatic
personal-content detector or crop editor is supplied.

Edit private `catalog-request.json` with the accepted development `snapshot_id`
and 1–30 `identities` of the same proposal shape, including similar alternatives.
Run `subset`, then `draft-approval`. The export reuses `open_catalog` and
`resolve_identity`; it sends no catalog names, images or answer labels to OpenAI.
Unrecognized namespace/identifier proposals remain unresolved; a bare set number
does not silently acquire a suffix. A valid catalog identity does not prove a visual match.

## Approve once, execute once

Brian approved the exact `gpt-6-luna` model, $0.25 lifetime cap, ten total attempts
and standard API handling, conditional on project privacy and exact sample approval.
A fresh authenticated read confirms API sharing is disabled organization-wide,
including Brickvault. The private account receipt records this verification. The prepared sample still needs Brian's confirmation.
The official model-specific image billing bound remains unverified and blocks live
dispatch in code; see the provider decision. No model or formula substitution.

After these gates resolve, record the confirmed project ID and exact sample/protocol
digests in the protected draft, run `seal`, enter the key locally with `key`, then
`check-model`. The metadata check only proves model visibility with that key/project.
Run the selected sample once. Changing the final approval/key invalidates access
proof; reconcile it in this conversation without resetting any ledger allowance.

A failed, refused, malformed, truncated or timed-out request remains counted and
stops the sample. A lost response or process interruption retains the reservation.
Completed results are reused only after validating their stored hash, strict schema
and full request identity. The identity includes ordered transmitted image hashes,
text, model/parameters, prompt/schema/preprocessing versions and catalog subset
version. Canonical validation repeats on reuse. Reuse increments its own counter
and adds no independent accuracy measurement. Missing/corrupt results block a
repeat inference. Reuse does not invoke valuation or refresh market evidence. An uncertain attempt or stale operation lock
requires manual reconciliation in this conversation; do not delete/reset the ledger
to regain budget. Ten is an absolute ceiling including any separately approved
manual retries; 14A provides no retry command. No repeated tuning campaign is allowed.

## Results and interpretation

Every private result records model/prompt/schema versions and digests, image digests,
transformation recipe, request parameters, catalog snapshot, ranked candidates,
visual/text clues, contradictions and requested views. The ledger records latency,
available input, cached-input, cache-write, total output and included reasoning tokens,
model/dated prices, result-reuse count and token-derived estimated USD.
There is no reported invoice/billing amount. Missing usage stays unknown and retains
the full reservation. Structured candidates never write catalog mappings, training
labels, confirmations or valuation evidence.

Top-1/top-3 are counts of independently confirmed identities found among rank-1 or
rank-1–3 proposals **per group**, pooled across distinguishable objects. Each expected
identity counts at most once; this is identity recall, not quantity/object-detection
accuracy. The denominator includes all predeclared confirmed identities, including
failed/unattempted groups; completion counts are reported separately. Confidence is
uncalibrated; the fixed high-confidence threshold is 0.8. Abstentions count objects
without candidates. Unknown/custom/non-LEGO outcomes are valid processing results.

**Current live results:** 0 attempts, USD 0 spent, 13 selected photos across seven prepared groups, no observed
recognition quality or latency. The original six fixture tests validated software behavior only. The continuation
passed seven affected tests in 3.80 seconds (one unchanged canonical test deselected),
plus Ruff and strict mypy for six Python files. No live image/cost proof follows.
The actual catalog subset and inference compatibility remain unverified; see the continuation result below.

The wider Phase 14 comparison of direct recognition, retrieval alone and retrieval
plus verification remains outstanding. Embeddings/vector infrastructure requires
measured need and approval. A tiny selected sample cannot establish general accuracy.

## Sample preparation update

Seven groups/13 photos are prepared privately; original hashes are unchanged.
The local key file is present. Final sample confirmation, catalog/project checks and
verified image-token admission remain outstanding; no provider request was made.
Schema v2 increases object/expected-label limits from six to twelve to accommodate
G06's eight exact identities and three partial/combined-parts figures. Partial figures
are not promoted to exact labels. Three affected tests passed in 3.16 seconds, with
Ruff and strict mypy passing. The 2,048 output-token limit is unchanged; dense-lot
truncation remains possible and stops the run without automatic retry.


## Authorized development catch-up and cost admission — 2026-10-02

Brian separately authorized the existing forward migrations 0013–0017 on the owned
local development database only. Verified target: `127.0.0.1:55432`, database
`brickvault_dev`, expected ownership marker/owner, initial revision
`0012_product_identity_qualifiers`, and initially stopped service.

One protected, ignored custom-format PostgreSQL recovery copy was created using
the existing local PostgreSQL utility transport before migration: 2,131,671,403
bytes, SHA-256 `fd12f4332e69f1dd911d053500513b37f64beb89e9b9fe4dae9d97a688fbd049`.
`pg_dump` succeeded; `pg_restore --list` read the archive metadata successfully.
The dump, table of contents and private receipt are retained. No restore rehearsal
was performed. The established migration function applied the existing chain and
runtime grants in one transaction, reaching `0017_listing_images`.

Validation: all 69 pre-existing table counts matched, totaling 17,641,958 rows.
Full-content SHA-256 digests also matched for all 39 tables with at most 10,000
rows, including saved-work and catalog activation context. Larger catalog tables
were compared by row count, not full-content digest. Fifty-six runtime SELECT
checks passed. Existing user data was retained. No catalog import, replacement,
new migration or application-code change occurred in this continuation.

Read-only catalog admission found one accepted nonsynthetic full-catalog snapshot,
which is active. Three confirmed set identities resolve exactly. The 14 confirmed
BrickLink minifigure identifiers do not resolve as canonical identities, and this
snapshot contains zero BrickLink minifigure mappings. Those labels remain unchanged;
no mappings were guessed or written. The 20–30-reference pilot subset is not sealed.

Cost admission remains blocked independently of the database result:

- The official [image-token rules](https://developers.openai.com/api/docs/guides/images-vision)
  do not list `gpt-6-luna`; another model's multiplier was not substituted.
- The [counting guide](https://developers.openai.com/api/docs/guides/token-counting)
  and [API reference](https://developers.openai.com/api/reference/python/resources/responses/subresources/input_tokens/methods/count)
  document image inputs and structured-output configuration. They do not establish
  Luna-specific support, counting charges or endpoint-specific retention. The
  reference does not document a `store` parameter for counting.
- The current [pricing](https://developers.openai.com/api/docs/pricing) and
  [data-controls](https://developers.openai.com/api/docs/guides/your-data) pages
  did not resolve those counting-endpoint questions. No claim that counting is free
  or exempt from photo-submission handling is made.

Preflight photo submissions: **0**. Inference attempts: **0**. Reuses: **0**.
Preflight charges: **USD 0**. Inference charges: **USD 0**. No inference reservation
was admitted; the USD 0.25 total cap and ten-attempt limit remain intact.
The exact approved prepared-sample and review hashes are unchanged. The development
service was returned to its original stopped state after each bounded operation.
Protected files remain unchanged, the index is empty and main remains unpushed.
No broad tests, frontend/Android builds or production operations were run.

Remaining evidence: an authoritative Luna image-cost bound, or confirmed counting
endpoint model/billing/data-handling terms; and verified catalog identity/mapping
coverage for the selected minifigures. The pilot has not run.


## Bounded catalog-admission investigation — 2026-10-02

Cause **C, with intentional importer scope B**: the retained authoritative
Rebrickable bulk source supplies no BrickLink minifigure crosswalk. Its minifigs
archive contains 17,225 rows with `fig_num,name,num_parts,img_url`; compressed and
decompressed hashes match the accepted manifest. None of the fourteen approved
BrickLink IDs appears in any field. The accepted snapshot/source binding is
retained in the original activation receipt. This is a catalog-coverage limitation.

The [source profile](../services/api/src/brickvault_api/providers/rebrickable/records.py)
accepts those fields and ignores only the reviewed image URL. The
[candidate builder](../services/api/src/brickvault_api/catalog/builder.py) creates
direct verified mappings for the supplying Rebrickable namespace.
[Candidate validation](../services/api/src/brickvault_api/catalog/candidate_validation.py)
explicitly records external provider mappings as deferred and BrickLink as
`not_populated`. There was no retained crosswalk column or mapping dataset omitted
during import (A). The
[canonical resolver](../services/api/src/brickvault_api/catalog/repository.py)
looks up canonical identifiers; provider mapping status is a separate operation.
It is not hiding a valid existing mapping (D).

Retained BrickLink proof covers a different minifigure. One necessary, bounded
read-only development check searched the existing separate market mapping revisions
for the fourteen exact approved native IDs, including historical revisions: zero
matches. It did not repeat the accepted zero-catalog-mapping query. Ownership,
loopback target and current migration guards were used; development returned to
its initial stopped state. No database mutation occurred.

Private review manifest: `.local/recognition-14a/catalog-mapping-review-manifest.json`.
Each entry keeps the original BrickLink ID, a null canonical candidate, exact
retained source/provenance, unavailable status and the required existing review
operation. Counts among the fourteen IDs: **0 verified, 0 ambiguous, 14 unavailable**.
No visual/name/variant inference was used. Recognition and canonical mapping are
separate: the confirmed sample labels remain intact; this finding establishes no
recognition result. Samples, scoring protocol and denominators are unchanged.

Minimum correction proposal: obtain a provider-certified exact supplemental
BrickLink MINIFIG → Rebrickable minifigure crosswalk for these fourteen exact
variants, with source locators/digests and access/retention rights. No particular
unverified endpoint is claimed to supply it. Once evidence supports existing
canonical identities, reuse
[`MarketRepository.review_mapping`](../services/api/src/brickvault_api/market/repository.py)
with evidence-bound mapping revisions. A separately authorized, bounded read-only
pilot admission path must then consume exact verified current bindings; the current
CLI projects canonical identities only. The existing importer has no operation that
can create the absent crosswalk from the retained CSV. Reimporting the same source
would reproduce the gap. No accepted snapshot edit, alias fabrication, shadow catalog,
full catalog replacement or migration is proposed. Source acquisition/retention
(if needed), reviewed local mapping writes and the bounded admission-source change
need separate authorization. Nothing was applied.

Cost admission remains blocked using the documented evidence gap. Draft provider
question, **not sent**:

> For gpt-6-luna, what is the billed image-token upper bound for 1–2 JPEGs per request, each at most 1024×1024 pixels with detail=high; does POST /v1/responses/input_tokens support the exact request with developer instructions, images, structured-output schema and explicit cache breakpoint; and what counting charges and retention/data-handling rules apply, including whether store=false is supported?

Photo/counting submissions **0**; inference attempts **0**; spend **USD 0**.
The USD 0.25 lifetime cap and ten inference attempts remain intact. Recovery copy,
private credentials and existing allowance state were preserved. Protected files
are unchanged, the index is empty and main remains unpushed. No inference/counting
call, provider fetch, broad test, build, staging, commit or push occurred.


## External-evidence handoff — paused

One bounded public source-feasibility check reviewed Rebrickable's
[API documentation](https://rebrickable.com/api/v3/docs/) and its linked
[public OpenAPI schema](https://rebrickable.com/api/v3/swagger/?format=openapi).
The documentation identifies external IDs for parts; the reviewed material does
not establish an exact whole-minifigure BrickLink → Rebrickable crosswalk or
permitted coverage for the fourteen selected IDs. **No authoritative source
established.** No authenticated catalog fetch, mapping write or resolver change
occurred. Accepted local findings are reused without further qualification.

Submit the following text through the chat bubble at the bottom right of
[help.openai.com](https://help.openai.com/en/articles/6614161-how-can-i-contact-support).
The inquiry has **not been sent**:

> Subject: gpt-6-luna image-token bounds and input-token counting billing/data handling
>
> I am preparing a small private vision evaluation using only gpt-6-luna, with a $0.25 total API budget. Before submitting any images, please clarify:
>
> 1. What billed image-token formula or guaranteed upper bound applies to 1–2 metadata-free JPEGs per request, each at most 1024×1024 pixels and 1 MiB, with detail=high? Please provide an official reference explicitly applicable to gpt-6-luna.
> 2. Does POST /v1/responses/input_tokens support this model and accurately count developer instructions, base64 image inputs, a strict JSON output schema and an explicit prompt-cache breakpoint? Our planned Responses request uses reasoning.effort=medium, service_tier=default, store=false and max_output_tokens=2048. Which fields must be retained or omitted in the counting request without changing the counted input?
> 3. Is token counting free or billable? If billable, what rates, minimum charges, image charges or cache-write charges apply?
> 4. What data handling applies specifically to counting submissions: training use, abuse-monitoring retention, application-state storage, image retention and cache retention? Is store=false supported, and what retention does it control? Project data sharing is disabled.
>
> Please answer using documentation or written confirmation. This inquiry includes no images or credentials; no inference or token-counting probe has been made.

Paused pending external evidence or an explicit scope decision. Approved inputs,
labels/scoring, exact model and lifetime limits remain accepted. No photo/counting
submissions, inference attempts or spend were added.
