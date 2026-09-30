# Minimal accepted r3 context

[Accepted r3 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/9f24d1e541da3b173cfe3ea7304e269f37d5c17c/astra_response/P12-05-catalog/r3/REVIEW.md), commit `9f24d1e541da3b173cfe3ea7304e269f37d5c17c`.
Catalog importer repair is **ACCEPTED / CLOSED** and main closeout is
`0ea8e0e21156bebb9aa4150c270643a0a5d0d571`. r1/r2/r3 are retained unchanged.

Accepted repair: 100,000 physical-row inventory_parts spans, unchanged constraints,
triggers, atomic build transaction, statement/lock timeouts, migration and grants.
Accepted isolated full-source evidence: 12 datasets, 1,898,466 staged rows, validated
candidate, structural PASS; parts maximum 29.471287 seconds, clean repeat 29.894506;
worst named operation 196.324807 seconds, margin at least 103.675193 under 300.
177 focused units and 20 PostgreSQL tests are accepted earlier evidence.

None of these tests/builds/isolated qualifications were rerun. They do not prove
this production continuation. The exact local artifact verification passed anew;
installation, recovery/retry/activation and installed application gates are unrun.
The approval mismatch is specific to the newly required detached identity binding.

## Historical local source references

The plan snapshots retain earlier local source references. The following files
resolve in the preserved main checkout but are absent from verified public trees.
Their links lead here for that context; their source is not newly published or
requalified by this blocker package. The exact approval validator is separately
linked to its accepted r2 published bytes.

- `docs/PHASE_2D_PROVIDER_GATE.md` — local source reference only.
- `services/api/src/brickvault_api/product.py` — local source reference only.
- `services/api/src/brickvault_api/watchlist.py` — local source reference only.
