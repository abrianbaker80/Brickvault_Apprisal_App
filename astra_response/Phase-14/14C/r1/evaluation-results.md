# Frozen retrieval evaluation — 2026-10-06

**Disposition: NOT USEFUL on this sample.** The three correct set keys were absent
from top eight; all 24 entries in those three shortlists were minifigures. Broad
name matching across both kinds and saturated term searches do not give a useful
set shortlist here. Deterministic ties remain unchanged. The sole exact-key hit
was the curated G05 external reference at rank 7. No weights/search changes followed.

## Sample and integrity

Four visible-description queries were frozen before ranked results. Query bytes/hash
and confirmed-label bytes/hash were retained separately; both hashes remained unchanged.
Queries used visible colors/object/build details, excluding names/IDs, listing and
placard text, prior predictions, filenames and reviewer conclusions. Ground truth never
entered retrieval. Availability used the exact accepted snapshot or reference key.

The scored sample is smaller than the suggested 6–10: three reusable confirmed set
examples and one figure identity present in the curated reference corpus. No added
catalog example with independent visible evidence was manufactured. The 13 unavailable
figure labels were audited for coverage and were not dispatched as ranking queries.
G04 has no confirmed identity; G07 is a custom-build outcome. Neither supplies an
identity-retrieval denominator. This is a small feasibility result, not a benchmark.

## Aggregate

| Metric | Result |
|---|---:|
| Scoreable / corpus-unscoreable | 4 / 13 |
| Exact top-1 | 0/4 |
| Exact top-3 | 0/4 |
| Exact top-8 | 1/4 (25%) |
| Mean reciprocal rank at 8 | 1/28 = 0.035714 |
| No-match | 0/4 |
| Average candidate-pool size | 946.75 |
| Saturated/truncated searches | 4/4 (100%) |
| Shortlisted entries with approved photo | 2/32 (6.25%) |
| Returned correct keys with approved photo | 1/1 |

Pool sizes include both catalog kinds plus the three external references. Term/type
limits are 100; marked saturation does not reveal full-corpus rank. RR@8 is zero when
the target is outside the retained shortlist. No-match means an empty shortlist; a
populated irrelevant shortlist remains an exact-key miss. Missing mappings are unknown.

## Per-case results

Private figure IDs and query text are omitted. A dash is unavailable; `>8` means
absent from the retained shortlist, not a known full-pool rank.

| Case | Group | Kind / identity state | Status | Rank | Top-1/3/8 | RR@8 | Pool | Truncated | Shortlist photos | Target photo |
|---|---|---|---|---|---|---:|---:|---|---:|---|
| C01 | G01 | set / catalog_native | scoreable | >8 | no/no/no | 0.000000 | 741 | yes | 0 | not returned |
| C02 | G02 | set / catalog_native | scoreable | >8 | no/no/no | 0.000000 | 882 | yes | 0 | not returned |
| C03 | G02 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C04 | G03 | set / catalog_native | scoreable | >8 | no/no/no | 0.000000 | 876 | yes | 0 | not returned |
| C05 | G03 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C06 | G03 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C07 | G03 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C08 | G03 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C09 | G05 | minifigure / external_unresolved | scoreable | 7 | no/no/yes | 0.142857 | 1288 | yes | 2 | yes |
| C10 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C11 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C12 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C13 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C14 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C15 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C16 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |
| C17 | G06 | figure / unavailable | corpus/mapping unavailable | — | — | — | — | — | — | — |

## Interpretation and preserved boundaries

Only one of fourteen confirmed figure keys exists in this retrieval corpus, as a
curated external reference. All fourteen remain canonically unmapped. That difference
allows one raw external-ID retrieval score without fabricating a crosswalk. The three
native expected sets remain accepted catalog identities despite retrieval misses.

The references were chosen around a known G05 example; their inclusion is not
independent reference-retrieval coverage. A/B concealed heads remain indistinguishable
in the evaluation views; photographic darkness does not prove different parts.

This evaluates description-assisted retrieval only: no image-only/general recognition,
minifigure production accuracy, full reference coverage, complete crosswalk or AI
verification accuracy is established. Existing 14A scores, ledger and reservations
are unchanged. No production confirmation, mapping or valuation follows.

One evaluation and three harness fixtures; no 14B foundation rerun, provider calls,
paid inference, metadata/counting probes, embeddings, new references, browser smoke,
builds, migration/import or production work. Development returned to stopped.
Main is unpushed; 14C changes remain uncommitted and its index empty.
