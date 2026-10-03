# Paired G06 result and lifetime accounting

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
