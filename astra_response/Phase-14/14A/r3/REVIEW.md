# READY FOR PHASE 14A CONTINUATION REVIEW

**The two authorized requests completed; exact minifigure recognition remains weak.**
Brian accepted [r2](../r2/REVIEW.md) as partial evidence, not completed qualification.
Phase 14A remains open for review; no later phase or model comparison is started.
Application baseline `d839e51b65f9156e5829740c08d52b59be4c4ec4`; prior publication `108f7f6d65a38ebead7701d3c0f7f2d62ed3b5ab`.

## Distinct views

| View | Processing | Raw exact agreement | Estimated USD |
| --- | --- | --- | ---: |
| Original r2 protocol, unchanged | 6 requests; 5 groups completed; G06 incomplete | Top-1/top-3 3/17 | 0.0036058 |
| Amended calls | G07 first, then sole G06 retry; both completed | G07 correct custom_build; G06 0/8 confirmed IDs | 0.0022084 |
| Cumulative sample coverage, mixed output limits | 8 lifetime requests; all 7 groups/13 approved images processed | Top-1/top-3 3/17 (17.65%) | 0.0058142 |

Original G06 remains failed/counts toward cost and attempts. Its sole retry supplies
coverage; no best-of selection or double-counted labels. G01–G05 and original r2
files/usage/hashes are unchanged. Two lifetime attempts remain, neither authorized.

**Sets: 3/3 exact. Minifigures: 0/14 exact.** Five figure IDs were omitted in completed
original set groups; the individual-figure case proposed a different ID. The G06
retry returned nine unknown objects and two IDs matching none of its eight confirmed
labels. Its labels are not exhaustive; partial/combined figures remain unscored.
G04 remains an unscored mixed-set abstention. G07 correctly returned custom_build.
Listing text was included; this is not visual-only evidence or general qualification.

Canonical integration is separate: three expected set labels resolve, fourteen
figure labels remain unmapped. The raw misses are not caused by that mapping gap.
No guessed mapping, valuation promotion, confirmation or catalog write occurred.

## Accounting and bounds

Only new attempts 7/8 use **16384 output tokens / 180 seconds**. Model `gpt-6-luna`,
Medium reasoning, prompt/schema, inputs, detail/preprocessing and privacy stay fixed.
**12852 input + 9058 output tokens** reported lifetime; output includes **7202 reasoning**.
Cached/write usage zero. Invoice cost unavailable; USD 0.0058142 is an estimate.
Average USD 0.000726775/request; effective USD 0.0008306/distinct group including retry.
Retained reservations **USD 1.877792**, unreserved **USD 8.122208**, within USD 10.00.
Fourteen image inputs were sent across eight calls, with the original approved G06
photo repeated once. No new counting/metadata probe, automatic retry/fallback or extra call.

## Review material

- [Approved amendment, protocol and retry linkage](amendment.md)
- [Per-request results and cumulative accounting](results.md)
- [Three affected checks, static checks and reused evidence](validation.txt)
- [Exact changed-file inventory and hashes](changed-files.md)
- [Amendment patch against r2](amendment.patch)
- [Cumulative application patch](cumulative.patch)
- [Existing pilot report](source/docs/PHASE_14A_PILOT.md)
- [Guarded CLI/accounting source](source/services/api/src/brickvault_api/recognition/pilot.py)
- [Existing fixtures plus three targeted checks](source/services/api/tests/unit/test_recognition_pilot.py)

The three affected tests pass (2.93s), plus Ruff/strict mypy for four edited files.
Earlier qualification is reused. Original six attempt records/results remain intact;
new files and a versioned amendment preserve each request's parameters/history.
Eleven files change from r2; thirteen form the cumulative delivery. Two historical
private local paths are redacted in publication copies. Copied application-document
links resolve after applying the cumulative patch; package-root review links work.

Development remains stopped; recovery and protected/private files are preserved.
Main is uncommitted/unpushed with empty index. Only this sanitized r3 package is
published; r1/r2 are unchanged. No database work, builds, production, mapping writes,
training, new model or expanded evaluation was done. Photos/listing text/expected
figure labels/credentials/private asset paths/reasoning text are excluded.

**Stop for recognition-quality review.** Increasing capacity completed G06 without
improving exact figure agreement. Do not close 14A or claim recognition qualification.
