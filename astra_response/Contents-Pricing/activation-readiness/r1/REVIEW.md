# CONTENTS PRICING LIVE-MAPPING READINESS — BLOCKED

Read-only observation: 2026-11-17, 13:48–13:52 UTC. Selected contents pricing remains
SOURCE/TEST ACCEPTED / CLOSED at local main `f79e94092d272a050ced989eb1761b34320bdd28`.
This result does not reopen implementation qualification or authorize deployment.

## Actual production baseline

The established host-key-checked VM115 administrative endpoint reports hostname
`brickvault-appraisal`, active release `phase16c-outcomes-production-r2`, source commit
`50f66837addf77ddd1c1a69eed0a873c17163a81`, Python 3.13.18 and database schema
`0019_reviewed_dataset_foundation`. The API service is active. No hypervisor operation
was performed. The release and schema remained unchanged at the final read.

The active real Rebrickable full-catalog snapshot is accepted generation 1:
`9ba3056b-690d-4686-bd96-109981f696ea`, source
`cdf842d4-c525-4324-a990-55cbfaedaa4a`. It contains 28,278 set facts and selected set
inventories, and 17,225 figure facts. The latter is not the direct-occurrence denominator.

## Eligibility

| Type | Production market mapping rows, all history | Eligible mappings / distinct targets / direct occurrences | Supported distinct targets / direct occurrences, including extras |
| --- | ---: | ---: | ---: |
| Whole MINIFIG | 0 | 0 / 0 / 0 | 16,780 / 23,441 |
| Exact PART/color | 0 | 0 / 0 / 0 | 70,012 / 1,335,651 |

Regular-only denominators are 16,780 / 23,441 for figures and 69,789 / 1,234,732 for
parts. Part rows before the known-color gate are 79,412 distinct targets / 1,345,859
occurrences; 10,208 occurrences have unknown color semantics. No direct rows in these
two types belong to matching choices. Counts are rows and distinct identities, **not
piece quantities**. The only market mapping is one open verified SET mapping; there
are no component rows to classify as closed, rejected, ambiguous or wrong-snapshot.

`10350-1` has eight direct figure occurrences / eight targets and 882 part occurrences /
767 targets, with zero eligible occurrences. No eligible real-set example exists.
Current catalog associations are solely Rebrickable: 17,225 figure, 64,620 part and
275 color associations marked verified; element associations are 109,293 verified and
4,952 unresolved. These are not verified BrickLink market mappings. The fourteen
historically unresolved figures are not the catalog-wide denominator and remain outside
the two-candidate proposal below.

## One next action: bounded mapping onboarding first

Separately authorize reviewed admission of **two exact production mapping revisions**
using the already-held Phase 3B identity evidence and the current source bindings:

| Type | Current direct occurrence | Retained provider identity | Provisional later view |
| --- | --- | --- | --- |
| MINIFIG | `21333-1`: Rebrickable `fig-012609`, Vincent van Gogh; regular quantity 1, extra 0; sole intact figure, no alternative | BrickLink `MINIFIG idea106`, no color | USED / SOLD |
| PART/color | `10016-1`: Rebrickable `3001`, White `15`; regular quantity 2, extra 0; element `300101` | BrickLink `PART 3001`, White `1` | USED / SOLD |

These are **onboarding candidates, not ready targets**. Their current canonical,
revision, occurrence and source-evidence UUIDs are in [evidence.json](evidence.json).
The retained review uniquely corroborated parent membership for the whole figure and
element, item, color and known-color evidence for the part. The five relevant retained
source-file digests match production; current figure membership and element association
also agree. This supports a narrow admission proposal without new crosswalk research.

The old proof snapshot `243ee681-2c7d-4cfc-b7f1-204577fa93ba` and its canonical UUIDs
are different. Explicitly review and bind production snapshot/source, canonical IDs,
evidence references and exact provider color through the existing
`MarketRepository.review_mapping` operation. Do not copy old UUIDs or automatically
promote raw catalog associations. Retained metadata is available; original raw provider
responses were intentionally not retained. For these two identities the gap is reviewed
production admission/binding, not absent authoritative identity evidence. The separate
fourteen-figure crosswalk gap remains an authoritative-evidence prerequisite.

Only after admission would a separately approved deployment, including migration 0020,
make a live check possible. The provisional scope is two separate per-set plans, one
target and one view each: at most two initial price requests, zero identity requests,
and at most two retries **per plan** (four across both if fully consumed). Actual cache
and join state can reduce dispatch. This estimate is not an executable confirmation
plan or dispatch authorization. Brian must separately confirm each deployed feature's
actual displayed plan within its accepted limits.

## Access uncertainty and boundaries

Runtime configuration and the BrickLink credential file are present as regular mode-0600
files. Only file metadata was read; provider secret contents were not loaded. The local
BrickLink scope is not suspended and has policy `market-v1`. Four retained successful
SET fetches last finished 2026-10-19 20:21:53 UTC. These facts do not establish current
credentials, component access, registered-IP validity, external quota or prices.

No provider/model requests, database writes, migrations, service changes, maintenance,
backup, deployment, phone work, application changes, tests or builds occurred.
All 22 pre-existing pending paths and 59 baseline files, including the three protected
files and prior evidence, remain byte-identical. Main remains unpushed at `f79e940…`,
with an empty index. Only the additive [Plan 112 note](plan-note.md) is newly dirty;
it remains uncommitted. Capture stays stopped.

## Method and supporting evidence

Three guarded owner connections verified production ownership and used explicit
read-only, repeatable-read transactions; statement timeouts were 10–30 seconds and
lock timeout 2 seconds. Queries used existing 0019 tables, aggregate counts and bounded
result sets, not 0020 functions or application startup. See [exact SELECT queries](queries.sql).

Eligibility follows the accepted projection and planner: current accepted active
snapshot/source; selected default set revision; direct exact canonical target; no
matching choice; known part color; positive regular quantity unless extras are selected;
exactly one open verified BrickLink mapping across all snapshot/source candidates;
then matching snapshot/source and whole MINIFIG/no provider color or exact PART,
canonical part/color and non-null provider color. Variants and namespaces are preserved.
Nothing is inferred from a name match, component of a figure or raw provider association.

[Evidence](evidence.json) contains only catalog identities, aggregates, digests and safe
metadata. [Preservation](preservation.json) records the local checks. This package is
the only authorized commit/push; no main-source checkpoint or later work is included.
