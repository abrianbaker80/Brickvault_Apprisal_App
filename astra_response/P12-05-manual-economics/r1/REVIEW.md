# P12-05 manual economics r1: contract and replay review

**BLOCKED — governing contract forbids MANUAL economics independent of market
admission. No executable repair is implemented. P12-05 remains BLOCKED at Gate 5;
Phase 12 remains IN PROGRESS.**

The requested MANUAL + UNKNOWN arithmetic conflicts with the explicit accepted
Phase 7A2/7B contract. Changing the V1 guard would also change valid historical
recomputation. Brian's explicit governing-contract stop condition therefore applies
before implementing either an in-place correction or a new execution version.
This is not a claim that a larger schema redesign is unavoidable.

[Contract analysis](contract-analysis.md), [version/replay compatibility](version-replay-compatibility.md),
[admission and response semantics](manual-admission.md), and [bounded repair plan](repair-plan.md)
record the findings and the specific decision needed for future work.

Focused diagnostic validation passed: 112 economics/snapshot unit tests, four
offline synthetic capture/replay cases, and two real PostgreSQL cleanup tests in
owned disposable TEST databases. These confirm unchanged V1, not the requested
new admission behavior. [Arithmetic](arithmetic-evidence.md),
[MARKET regression](market-basis-regression.md), [cleanup](forecast-cleanup.md),
and [validation](validation.txt) distinguish each evidence scope.

Only Plan 102 and a minimal Plan 099 note were changed in this slice. The existing
P12-05 blocker documents and three protected dirty files were preserved; accepted
hashes match, main HEAD is unchanged and its index remains empty.
[Changed files](changed-files.txt), [exact changed documentation ZIP](changed-documents.zip),
[document hashes](document-hashes.json), and [cumulative patch](cumulative.patch)
make the stopped result reviewable. The cumulative patch also carries the preexisting
workflow/roadmap/Plan 099 blocker edits; it excludes protected modifications.

Accepted baseline: `e64f2d812bf90255005c88e8d1f68b4c8ab0d7af`.
Parent review publication: `15c403c3d4cc8b7eadbb233ea9af13032a7e4b39`.
[Minimal prior blocker context](p12-05-r2-context.md) reuses that publication.
Catalog importer repair and catalog activation remain ACCEPTED / CLOSED.

Production was not accessed: no owner login, preview retry, residual cleanup,
deployment, restart, database change, release pointer, backup or later acceptance
gate. Accepted production release context remains `p12-05-catalog-repair-r1`;
it was not freshly inspected. There is no candidate application release, migration
or new dependency. Main was not committed or pushed.
