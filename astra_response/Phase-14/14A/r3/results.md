# Original, amended and cumulative results

[Original r2 record, unchanged](../r2/REVIEW.md). Detailed original per-call evidence
remains in [r2 sample results](../r2/sample-results.md); it is reused here.

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
cache savings or releasing any original reservation. See the [provider decision](source/docs/PHASE_14A_PROVIDER_DECISION.md).

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
