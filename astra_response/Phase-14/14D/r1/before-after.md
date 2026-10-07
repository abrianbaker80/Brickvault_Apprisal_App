# Phase 14D before/after structural diagnostic — 2026-10-06

**Disposition: STILL NOT USEFUL.** The correction was designed after the accepted
14C misses; this is not an independent benchmark. All three known sets remain
outside their set top-eight. Kind starvation was removed but was insufficient
to recover these candidates. Deterministic description retrieval is not worth
further optimization on this evidence; image-driven retrieval is the next separate
decision. No image-driven implementation, research or paid request starts here.

## Controlled change

The existing scored/sorted pool is partitioned by candidate kind. Each kind gets
its own limit (eight); both are produced for every query, without a target-kind
argument or ground-truth label. The scorer selects the relevant bucket afterwards.
Matched terms, weights, exact-name bonus, tie key, per-term/type limit 100, corpus,
references and exact canonical resolution are unchanged. Static syntax-tree checks
verify the scoring/search prefix and six query/reference/resolution helper functions.

The comparison renderer has Set candidates and Minifigure candidates sections
with rank restarting within each. Kind no-match states are explicit. Legacy saved
combined results remain readable; new flat matches are a union for note-key lookup,
not a shared rank. HTML section/CSP behavior was checked in a synthetic fixture.

## Aggregate comparison

| Metric | Accepted 14C combined shortlist | 14D correct-kind bucket |
|---|---:|---:|
| Scoreable | 4 | 4 |
| Corpus/mapping unavailable | 13 | 13 |
| Exact top-1 | 0/4 | 0/4 |
| Exact top-3 | 0/4 | 0/4 |
| Exact top-8 | 1/4 | 1/4 |
| Mean reciprocal rank@8 | 0.035714 | 0.035714 |
| Known-set top-8 | 0/3 | 0/3 |
| Curated figure rank | 7 | 7 |
| No-match | 0/4 | 0/4 |
| Overall search saturation | 4/4 | 4/4 |
| Average overall candidate pool | 946.75 | 946.75 |
| Correct-kind average pool | not separately retained | 466.75 |

Rank absent from top eight is not a known full-pool rank. Thirteen unavailable
identities remain outside ranking metrics. All fourteen original figure labels
remain canonically unmapped, including the curated external key that is scoreable
for raw retrieval. These are separate coverage questions, not guessed equivalences.

## Previously scoreable cases

Private query text/figure IDs are omitted. The before column preserves accepted
14C scores directly; no old run was repeated or rescored.

| Case / group | Kind | Old rank | New bucket rank | Old top-1/3/8 | New top-1/3/8 | New kind pool | Overall pool | Truncated | Bucket photos | Correct returned photo |
|---|---|---|---|---|---|---:|---:|---|---:|---|
| C01 / G01 | set | >8 | >8 | no/no/no | no/no/no | 347 | 741 | yes | 0 | not returned |
| C02 / G02 | set | >8 | >8 | no/no/no | no/no/no | 395 | 882 | yes | 0 | not returned |
| C04 / G03 | set | >8 | >8 | no/no/no | no/no/no | 387 | 876 | yes | 0 | not returned |
| C09 / G05 | minifigure | 7 | 7 | no/no/yes | no/no/yes | 738 | 1288 | yes | 2 | yes |

## Both buckets, independently returned

| Frozen query code | Set pool | Set returned | Set state | Figure pool | Figure returned | Figure state | Overall pool | Overall truncated |
|---|---:|---:|---|---:|---:|---|---:|---|
| Q01 | 347 | 8 | shortlist | 394 | 8 | shortlist | 741 | yes |
| Q02 | 395 | 8 | shortlist | 487 | 8 | shortlist | 882 | yes |
| Q03 | 387 | 8 | shortlist | 489 | 8 | shortlist | 876 | yes |
| Q04 | 550 | 8 | shortlist | 738 | 8 | shortlist | 1288 | yes |

There are 64 exposed candidates across all eight buckets, including two approved
reference photos (2/64). Within the four relevant-kind scoring buckets, reference
coverage is 2/32, unchanged from the old combined case shortlists. The one returned
correct key has a reference photo and remains external/unresolved. Bucket pool counts
sum to the original overall pools. Saturation is retained as an overall flag; it does
not establish complete search coverage within either kind.

## Limits and preservation

Four scoreable cases, with no new examples. G05 references were curated around a
known identity; the single figure hit supports no production-quality conclusion.
Concealed-head uniqueness is unestablished and photographic darkness is not proof
of a variant distinction. No image-only/general recognition, full reference coverage,
complete crosswalk, production confirmation or valuation is established.

Original 14C inputs were read directly, neither edited nor regenerated. Separate
query/truth hashes match both runs. The original 14C public-result bytes are copied
exactly into results-before-14c.json; accepted r1 and all earlier review trees are
preserved. Private labels, photos, queries, asset paths, credentials and ledger stay local.

One 14D run completed through the existing owned read-only development lifecycle,
stopped before/after. Three focused fixtures and affected static checks passed; no
old suite, browser smoke, broad checks, builds, database mutation or provider calls.
Main stays unpushed with nine uncommitted 14D files and empty index. STOP for review.
