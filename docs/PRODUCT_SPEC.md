# Product Specification

## Product statement

BrickVault Appraisal App is a private, self-hosted assistant that turns messy LEGO resale-listing photos into an evidence-backed identification and buy/no-buy appraisal.

## Primary workflow

1. Brian creates a listing session through Android capture/share or web upload.
2. He adds one or more photos and, when available, title, description, asking price, location, and source URL.
3. The server stores immutable originals and creates safe derivatives.
4. The app detects duplicate photos and possible objects/sets within them.
5. The recognition pipeline returns ranked candidate sets and visible evidence.
6. The valuation pipeline retrieves or calculates condition-appropriate values.
7. The app displays risk, estimated value, resale scenarios, opening offer, and maximum offer.
8. Brian confirms/corrects identities and optionally records the purchase and resale outcome.

## MVP capabilities

### Listing capture and storage

- Create, edit, and archive a listing.
- Upload multiple PNG/JPEG/WebP images.
- Preserve original bytes and generate thumbnails.
- Detect exact duplicates; record relationships for derivatives.
- Store extracted or manually entered listing metadata.
- Show image upload/processing status and failures.

### Recognition

- Analyze one clearly visible set or box first.
- Return at least three candidates where possible.
- Include confidence, supporting features, contradictions, and requested follow-up views.
- Permit `unknown`, `custom build`, `mixed sets`, and `insufficient evidence` rather than forcing a set number.
- Record Brian's confirmation or correction.

### Valuation

Display separately:

- market value for an identified condition,
- quick-sale estimate,
- expected gross resale,
- expected fees/shipping/replacement costs,
- expected net resale,
- suggested opening offer,
- maximum offer,
- confidence/risk reserve and the assumptions behind it.

Valuation formulas must be deterministic, inspectable, configurable, and testable. The language model may classify evidence but must not silently invent the final arithmetic.

### History and outcomes

- Search prior appraisals.
- Record bought/not bought, purchase price, verified contents, actual sale price, costs, and time to sell.
- Compare predicted versus actual results.

### Android input

The first dependable Android input can be a share target. The intended advanced input is a user-triggered floating overlay/accessibility-assisted capture flow with a manual fallback.

## Training-data requirements

- AI predictions remain unverified until Brian confirms them.
- Confirmed object crops can be marked training-ready.
- Hard-negative candidate pairs should be retained.
- Dataset export must keep listing groups intact across train/validation/test splits.
- Training-ready exports must exclude unrelated personal or seller-identifying screen content.

## Non-goals for the first MVP

- Public users, registration, billing, subscriptions, teams, or roles.
- App Store/Play Store distribution.
- Automated Facebook crawling or unattended interaction.
- Automatic seller messaging or offer submission.
- Guaranteed set completeness from photographs.
- Recognition of every loose individual element.
- A custom-trained production model.
- Kubernetes, autoscaling, or high-availability infrastructure.
- Full accounting or inventory management.

## MVP acceptance scenario

Given five screenshots of a Marketplace listing showing one assembled official LEGO set, Brian can:

1. create a listing,
2. upload/share the screenshots,
3. see unique saved listing photos,
4. receive ranked candidate set IDs with evidence,
5. confirm the correct set,
6. see a transparent value and offer calculation,
7. reopen the appraisal later,
8. preserve the confirmed image/label pair for a future dataset.
