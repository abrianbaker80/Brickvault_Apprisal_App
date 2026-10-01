# Version, persistence and historical compatibility

| Identifier | Meaning and current use |
| --- | --- |
| whole-set-economics-v1 | Frozen financial execution: defaults, admission, formulas, order and presentation |
| whole-set-usd-rounding-v1 | Frozen exact/charge/display/feasible-cent rounding rules |
| whole-set-snapshot-v1 | Canonical exact-input/historical-assertion/expectation storage envelope |
| deal-economics-v1 / purchase-limits-v1 | Public result variants, not independent execution dispatch |

SnapshotV1 persists execution versions inside canonical_payload; no separate
relational calculation-version column is needed to persist the current version.
Capture resolves exact request, basis and historical assertions before rounding.
The SHA-256 digest includes resolved versions, request, basis, qualifications,
accepted_at and exact/presentation expectations, excluding only the digest itself.
It establishes integrity, not external authenticity or replayability by itself.

basis_revision separately hashes valuation (excluding as_of) plus selected
same-condition mapping/observation/eligibility receipts. It is stable across clock/
refresh progress but changes with relevant basis facts, even below displayed cents.
It is not a replay archive and does not replace execution-version persistence.

ForecastService._verify checks stored digest/canonical encoding and calls replay.
Historical load, saved index and revision-parent admission use this verification.
replay decodes the exact supported version tuple, recomputes solely from inputs
through calculate_v1 and compares both financial and presentation expectations.
Stored expected outputs are comparison targets, never financial inputs.

A valid existing MANUAL+UNKNOWN snapshot records null dependent finances. Moving
the V1 guard changes its recomputed expected sale/net/profit/ROI and fails the
expectation comparison, making historical reads unavailable. A digest remaining
valid cannot cure this semantic mismatch. Existing tests distinguish digest
integrity failure from valid-digest replay mismatch and reject unknown versions.

Current local version inventory: source capture/decoder/projection and Hunt
financial fields admit only whole-set-economics-v1. All four offline encoded
fixtures in arithmetic-evidence.json retain that execution version and exact
byte roundtrip/replay. Fixture records are invented, not private saved contents.
Production and development saved records were not queried; no claim is made about
their counts or absence. Prior r2 only reports an ordinary unsaved capture.

Compatibility strategy here: preserve all executable source and V1 behavior.
112 unit tests passed, including supported MARKET/MANUAL, unavailable MANUAL,
canonical bytes, original inputs, unknown-version refusal and replay isolation.
Four exact roundtrips passed with versions unchanged. No record changes version.
No migration, history rewrite or calculator dispatch change occurs.

If a later explicit contract decision approves independent MANUAL admission, freeze
V1 and add narrowly selected new execution-version capture/dispatch with old replay
retained. Current Literal models and exact-version decoder do not already admit
that version: do not rename a constant or route old records through new semantics.
This review establishes neither a substantial migration need nor a broad redesign.
