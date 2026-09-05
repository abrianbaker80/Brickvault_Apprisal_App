# Data Model Outline

This is a conceptual model, not a final migration specification.

## Listing and capture

### `listing`

- id
- source type (`facebook_marketplace`, `manual`, `other`)
- source URL
- title
- description
- asking price and currency
- general location text
- status
- created/updated timestamps

### `capture_session`

Groups images and metadata collected during one Android/web capture flow.

- id
- listing id
- client type/version
- device/OS metadata kept to the minimum useful level
- started/completed timestamps

### `image_asset`

Represents immutable stored bytes.

- id
- SHA-256
- storage key
- MIME type
- byte count
- width/height
- asset kind
- privacy class
- created timestamp

### `image_relation`

Records lineage between assets.

- parent asset id
- child asset id
- transformation type
- crop coordinates or transformation metadata

### `listing_image`

Links an image asset to a listing/capture session with ordering and role.

### `object_region`

A selected/detected object within a listing image, with bounding geometry and an optional derived image asset.

## Analysis and recognition

### `analysis_run`

- id
- listing id
- status
- pipeline version
- requested provider strategy
- start/end timestamps
- failure details

### `provider_call_log`

- analysis run id
- provider
- model ID
- prompt/template version
- request purpose
- token/image usage and estimated cost
- latency
- success/failure metadata without secrets or image bytes

### `candidate_match`

- analysis run id
- object/listing image id
- candidate set number
- rank
- component scores (visual, text, inventory, verifier)
- final score/confidence
- evidence and contradictions

### `identity_confirmation`

An append-only event recording Brian's decision.

- target object/image/listing
- confirmed set number or special class
- confidence source (`user_confirmed`, `purchase_verified`)
- notes
- timestamp

Special classes include:

- unknown
- insufficient evidence
- custom build
- mixed sets
- non-LEGO

## Catalog and pricing

### `catalog_set`

- canonical set number
- name
- theme/subtheme
- release year
- piece count
- source mappings
- metadata provenance and update timestamp

### `reference_image`

- catalog set id
- image asset or external-reference metadata
- source and permitted-use metadata
- view type
- embedding/version status

### `image_embedding`

- image asset/reference id
- provider/model/version
- dimension
- vector
- created timestamp

### `price_snapshot`

- item/set number
- source
- condition
- region/currency
- statistic type and value
- sample count
- observed period
- fetched timestamp

## Appraisal and outcomes

### `appraisal`

- listing/analysis run id
- confirmed or assumed identity
- valuation profile/version
- market/quick-sale/gross/net estimates
- cost/risk assumptions
- opening offer
- maximum offer
- explanation snapshot

### `deal_outcome`

- listing id
- bought/not bought
- purchase price/date
- verified contents and missing items
- replacement costs
- resale channel
- gross sale, fees, shipping, other costs
- net result
- sale date/time-to-sell

## Dataset management

### `label_state`

State per image/object:

- unreviewed
- partially_labeled
- confirmed
- purchase_verified
- training_ready
- excluded

### `dataset_release`

- name/version
- selection rules
- split seed
- manifest hash
- created timestamp

### `dataset_item`

- dataset release id
- image/object asset
- label
- split
- hard-negative relationships
- provenance

All derivatives from one original listing must remain in the same split group.
