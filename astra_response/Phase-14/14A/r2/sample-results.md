# Sanitized Phase 14A live results

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
truncation or automatic retry. See the dated [provider decision](provider-privacy-cost.md).

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
