# CONTENTS PRICING TWO-TARGET MAPPING ADMISSION — COMPLETE

On 2026-11-17 at 14:17:23 UTC, both authorized component mappings were reviewed and
newly admitted in one production transaction. **Two created; zero reused.** Durable
readback confirms exactly one open verified current-source mapping for each target.

| Representative direct occurrence | Reviewed provider binding | New mapping revision | Eligibility |
| --- | --- | --- | --- |
| `21333-1`: whole Rebrickable `fig-012609`, Vincent van Gogh, regular quantity 1 / extra 0 | BrickLink `MINIFIG idea106`, provider color absent | `a136912a-069e-4ea2-8817-d0a9dae641f2` | PASS |
| `10016-1`: Rebrickable part `3001`, White `15`, regular quantity 2 / extra 0 | BrickLink `PART 3001`, White `1`, via element `300101` | `874d6fbf-81c1-4016-a950-685e3bbfe255` | PASS |

The exact production canonical IDs, direct occurrences, revision IDs and evidence
bindings are in [binding-lineage.json](binding-lineage.json) and
[admission.json](admission.json). Rebrickable color `15` and BrickLink color `1` remain
distinct namespaces. No other component, color, set or variant was admitted.

## Evidence and review

The unchanged retained Phase 3B accounting proof has SHA-256
`1db3445152faae8a7024195f8d6f716600fc375dd60a1d1da9af55e52a61d29d`.
Its manifest digest, selection bindings and both reviews passed the existing
`ProofBudget`/identity-review validators. Whole-figure ITEM and intact-parent SUBSETS
evidence supports the figure; ELEMENT, ITEM, COLOR and KNOWN_COLORS evidence supports
the exact part/color. The original proof still has 19 attempts, with no new attempt.

Six retained compressed source files passed their compressed/decompressed hashes;
six selected source rows matched production values and row digests. This includes
both direct occurrences, figure/part facts, element association and known White color.
Current parent membership remains one whole regular figure, with no alternative.
The physical part/color admission predicate also passed before either write.

Original provider evidence remains dated **2026-09-11**. New timestamps denote the
**2026-11-17 current binding review**, not a new identity fetch. Old snapshot/canonical
UUIDs remain in lineage and were not copied into production bindings. The immutable
mapping evidence references bind both the original proof digest and the exact lineage
artifact digest `0b01449dd5e95b79f85e46035f95e8fde364508c5bf4c4075c655b602afb591b`.

Accepted minimal identity metadata satisfies the existing review validators; they do
not require the intentionally unretained raw responses. Policy `market-v1` is unchanged:
30-day operational-metadata retention and 90-day closed/unreferenced-mapping retention
do not impose a new expiry on these open reviewed identity bindings. No price freshness,
current provider identity response or broader retention permission is claimed.

## Production admission and readback

The established VM115 endpoint reported `brickvault-appraisal`, release
`phase16c-outcomes-production-r2`, installed package/database head
`0019_reviewed_dataset_foundation`. Both mappings bind accepted active generation 1,
snapshot `9ba3056b-690d-4686-bd96-109981f696ea`, source
`cdf842d4-c525-4324-a990-55cbfaedaa4a`.

The installed `_GuardedOwnerDatabase` retained root-peer, ownership, credential-logging
and packaged-head checks. Both candidates and conflicts were checked before writing.
The outer transaction held provider/advisory locks and shared catalog/default-revision
locks; a transaction-scoped connection adapter let the unchanged
`MarketRepository.review_mapping` calls use nested savepoints. The normal API gained
no mapping privileges. No direct-SQL mapping insert, override or 0020 function was used.

Accepted offline custody was reused. The existing protected dual-backup receipt from
2026-11-17 10:08:38 UTC passed receipt/repository-identity validation for current schema
0019 and was less than 24 hours old. No backup, restore, proof generation or repository
requalification was initiated; no provider credentials were loaded.

Production writes: **2 mapping inserts; 0 updates; 0 deletes; 0 other database rows**.
Before/after counts and complete-row fingerprints preserve the existing SET mapping,
policy/scope, cache, observations, jobs, fetch/discovery/budget history, refresh
operations/views, forecast, outcome and classification records. Catalog evidence was
read and locked, never changed. A new guarded read-only transaction verified both
committed mappings and unchanged unrelated fingerprints.

| Record class | Before | After | Added |
| --- | ---: | ---: | ---: |
| Market mappings | 1 | 3 | 2 |
| Provider attempts | 5 | 5 | 0 |
| Price observations | 4 | 4 | 0 |
| Refresh operations | 1 | 1 | 0 |

**BrickLink/Rebrickable/AI calls: zero.** No remaining evidence prerequisite blocks
these two admitted mappings. Current external account access and prices remain
unverified; broader contents coverage and the separate fourteen-figure gap are unchanged.
No deployment occurred. Later USED/SOLD refreshes still require separately approved
deployment and Brian's confirmation of the deployed feature's actual displayed plans.

## Preservation and stop boundary

[Plan 112 was appended](plan-note.md) and remains uncommitted. Local main stays
`f79e94092d272a050ced989eb1761b34320bdd28`, unpushed, with an empty index. All 22
pre-existing pending paths, 59 baseline files, the three protected files, prior
publications and original private evidence remain unchanged. Private admission
receipts and lineage are retained. See [preservation.json](preservation.json).

Validation was limited to existing admission rules and exact production readback.
No application edits, tests, builds, dependencies, services, migration, maintenance,
APK/phone, dataset or later economics work occurred. Capture remains stopped.
This isolated sanitized package is the only commit/push authorized by this task.
