# Phase 14A local recognition pilot

**READY FOR PHASE 14A REVIEW — live approval/setup pending. Phase 14 IN PROGRESS.**
Phase 13 remains CLOSED. This optional CLI does not alter the running application.
See [Plan 104](plans/104-recognition-quality-pilot.md) and the
[provider/privacy/cost decision](PHASE_14A_PROVIDER_DECISION.md).

## What runs

From the repository root, use the existing Python environment:

```powershell
& services/api/.venv/Scripts/python.exe -m brickvault_api.recognition --help
```

There is no default live action. Commands operate on one fixed ignored private
directory, `.local/recognition-14a/`, with owner-restricted Windows ACLs or POSIX
permissions. Inputs, credentials and results never belong in the review package.
No new dependency, HTTP API, migration, UI or production service is involved.

| Command | Behavior |
| --- | --- |
| `init` | Create protected directory and empty selection/catalog request templates; refuse existing directory |
| `prepare` | Read only explicitly selected local files; retain originals; save anonymous metadata-free copies and frozen labels |
| `subset` | Export 20–30 exact references from an accepted nonsynthetic development snapshot using existing ownership/query guards |
| `draft-approval` | Create an OFF approval draft bound to prepared inputs, subset and protocol digests |
| `seal` | Require completed Brian approval; create immutable initialization marker and durable ledger; refuse repeats |
| `key` | Accept a key through hidden terminal input and write it only to protected storage; refuse overwrite |
| `run` | Validate approval and limits; reserve before dispatch; run each group at most once; stop on failure |
| `report` | Print counts, latency, tokens and estimated/reserved USD; exclude photos, clues, IDs, filenames and listing text |

`subset` never starts a database. The owned development database must already be
available through the established local workflow. It cannot target production or
port 5432. Source tests have not exercised a real catalog export in this slice.

## Select and prepare the sample

After `init`, edit private `selection.json` with 6–8 groups. Example shape below is
illustrative, not an approved asset or confirmed answer. Supply an absolute local
path in the private file; never include it in review artifacts.

```json
{
  "groups": [{
    "group": "G01",
    "files": ["<operator-selected absolute local photo path>"],
    "listing_text": "",
    "independently_confirmed": false,
    "labels_exhaustive": false,
    "expected": [],
    "expected_outcome": null,
    "submission_rights_confirmed": false,
    "personal_content_removed": false
  }]
}
```

Repeat for the selected groups. Mark rights/privacy fields true only after actual
review. `expected` entries use `kind` (`set` or `minifigure`), `namespace` and exact
`identifier`, including set suffixes. Expected identities must come from independent
confirmation. `labels_exhaustive` means every distinguishable identity in the group
has been labeled; only such groups support incorrect-confident-suggestion counts.
Negative cases can use confirmed `expected_outcome` and an empty identity list.
Unconfirmed cases show behavior but establish no accuracy. Multiple photos in one
group show the same scene/objects from different views.

`prepare` refuses duplicate photos, indirect paths, network shares, unsupported or
oversized images, animation and unreviewed privacy/rights. Originals are read only.
Review the protected copies visually before the final photo approval. No automatic
personal-content detector or crop editor is supplied.

Edit private `catalog-request.json` with the accepted development `snapshot_id`
and 20–30 `identities` of the same proposal shape, including similar alternatives.
Run `subset`, then `draft-approval`. The export reuses `open_catalog` and
`resolve_identity`; it sends no catalog names, images or answer labels to OpenAI.
Unrecognized namespace/identifier proposals remain unresolved; a bare set number
does not silently acquire a suffix. A valid catalog identity does not prove a visual match.

## Approve once, execute once

The combined provider/budget/photo request is pending in this conversation. After
Brian's approval, record it in the protected draft, confirming the exact digests,
cap, data-sharing status and expiration. Run `seal`; enter the key locally with `key`;
then run `run` once. Live access/entitlement is still unverified until an authorized
request succeeds. No authenticated entitlement probe is hidden in setup.

A failed, refused, malformed, truncated or timed-out request remains counted and
stops the sample. A lost response or process interruption retains the reservation.
Completed groups are skipped on rerun. An uncertain attempt or stale operation lock
requires manual reconciliation in this conversation; do not delete/reset the ledger
to regain budget. Ten is an absolute ceiling including any separately approved
manual retries; 14A provides no retry command. No repeated tuning campaign is allowed.

## Results and interpretation

Every private result records model/prompt/schema versions and digests, image digests,
transformation recipe, request parameters, catalog snapshot, ranked candidates,
visual/text clues, contradictions and requested views. The ledger records latency,
reported input/output tokens where available and token-derived estimated USD.
There is no reported invoice/billing amount. Missing usage stays unknown and retains
the full reservation. Structured candidates never write catalog mappings, training
labels, confirmations or valuation evidence.

Top-1/top-3 are counts of independently confirmed identities found among rank-1 or
rank-1–3 proposals **per group**, pooled across distinguishable objects. Each expected
identity counts at most once; this is identity recall, not quantity/object-detection
accuracy. The denominator includes all predeclared confirmed identities, including
failed/unattempted groups; completion counts are reported separately. Confidence is
uncalibrated; the fixed high-confidence threshold is 0.8. Abstentions count objects
without candidates. Unknown/custom/non-LEGO outcomes are valid processing results.

**Current live results:** 0 attempts, USD 0 spent, 0 selected photos, no observed
recognition quality or latency. Six fixture tests validate software behavior only.
The actual catalog subset and live schema/account compatibility remain unverified.

The wider Phase 14 comparison of direct recognition, retrieval alone and retrieval
plus verification remains outstanding. Embeddings/vector infrastructure requires
measured need and approval. A tiny selected sample cannot establish general accuracy.
