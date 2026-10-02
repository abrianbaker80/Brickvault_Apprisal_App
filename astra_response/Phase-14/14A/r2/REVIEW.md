# READY FOR PHASE 14A REVIEW

**Partial run stopped at the approved output ceiling.** Exact model `gpt-6-luna`;
amended lifetime cap USD 10.00; ten total inference attempts. Implementation base
`d839e51b65f9156e5829740c08d52b59be4c4ec4`. Phase 13 remains CLOSED;
wider Phase 14 remains IN PROGRESS.

## Observed result

- **Six live inference requests sent**, six groups/eleven approved images; **five
  groups completed**. Full seven-group/13-image sample **did not complete**.
- G06 returned incomplete: 2,048 output tokens, all reported as reasoning. The
  ledger stopped, retaining the failed attempt; **G07 was not sent**. No retry.
- Actual reported usage: **9,118 input + 5,388 total output tokens**, including
  4,403 reasoning. Cached-input/cache-write tokens were both zero.
- **Estimated cost USD 0.0036058**; actual invoice/charge amount unavailable.
  Average USD 0.00060097 per sent request/attempted group. USD 1.392216 remains
  reserved; USD 8.607784 unreserved, four lifetime inference attempts remaining.
- **Raw recognition agreement:** top-1 **3/17**, top-3 **3/17** (17.65%). Original
  independently confirmed denominators include the failed/unattempted cases.
- **Canonical resolution:** three expected set labels resolve; fourteen BrickLink
  figure labels remain unresolved. All three correct set predictions resolve.
  Exact unmapped labels remain valid for raw scoring; no equivalence is invented.

The first three groups identify their expected sets; figure predictions are omitted
in two groups and disagree in the individual-figure group. G04 yields an unscored
mixed-set abstention. G06 has no completed structured result. The MOC negative case
was not attempted. Listing text is present; this is not visual-only evidence.

## Implementation and review material

The model-wide 922,000 maximum input ceiling plus the approved maximum output and
worst applicable token rates reserves **USD 0.232036/request**, without counting
submissions or assumed cache savings. All ten reservations fit inside USD 10.00.
Raw agreement is independent of catalog resolution. The report records actual
usage, estimated cost, workload, failure/completion and effective rates separately.

- [Bounded plan](plan.md)
- [Provider/privacy/cost evidence](provider-privacy-cost.md)
- [Per-group results, usage and limitations](sample-results.md)
- [Focused validation and preservation receipt](validation.txt)
- [Literal thirteen-file inventory and hashes](changed-files.md)
- [Cumulative application patch](cumulative.patch)
- [Current pilot report](source/docs/PHASE_14A_PILOT.md)
- [Final CLI source](source/services/api/src/brickvault_api/recognition/)
- [Focused fixture tests](source/services/api/tests/unit/test_recognition_pilot.py)

Six affected fixtures passed, then one final transport check and one synthetic-ID
fixture recheck. Ruff and strict mypy passed. Source fixtures and live observations
are distinct. The patch was checked against the application base; only literal r2
review-package files are published. Previous review revisions stay intact.

## Limitations and next decision

This partial selected sample cannot qualify general recognition, minifigure variants,
quantities, condition/completeness, calibrated confidence or valuation. Catalog
resolution uses three retained accepted-catalog references; it does not claim a full
retrieval comparison. No authoritative figure crosswalk was established or written.

Review this partial result. Any continuation needs explicit approval for a manual
G06 retry with revised output/reasoning allowance and subsequent G07 dispatch. The
failed attempt remains counted/reserved. No request follows this review automatically.

Development remained stopped; recovery and private ledger/credentials are retained.
Sample hashes and protected files match. Main stays uncommitted/unpushed with an
empty index. No production, mapping/import/migration campaign, broad suites/builds,
training or Phase 15/16 work occurred. Photos, listing text, exact sample labels,
credential values and private asset paths are excluded. Two historical local asset
paths are redacted in copied documents; hashes identify local and publication bytes.
Copied application-document links resolve when the cumulative patch is applied to
the application tree; package-root review links work independently.
