# Project Context

## Owner and audience

The sole user and product owner is Brian. This is a private tool, not a public product, marketplace service, or subscription application.

## Problem

Facebook Marketplace LEGO listings frequently omit set names and set numbers. Photos may show assembled builds, partial builds, boxes, manuals, minifigures, mixed lots, or loose pieces. Brian wants to identify likely sets before making an offer and understand:

- current fair market value,
- realistic resale value,
- likely net proceeds,
- completeness and identification risk,
- an opening offer,
- a maximum rational offer.

## Desired experience

While viewing a Facebook Marketplace listing on Android, Brian should eventually be able to tap a floating BrickVault control, collect the visible listing photos and useful text, and send them to the self-hosted server for analysis. The experience should resemble a private LEGO-focused screen-understanding overlay.

The app must also support:

- selecting multiple screenshots from the phone,
- Android Share into BrickVault,
- browser upload from Chrome/desktop,
- manual correction of price/title/description,
- manual selection or cropping of an object in a crowded photo.

## Recognition approach

The initial system should not train one fixed classifier with one class for every LEGO set. Instead it should:

1. maintain a local catalog of official sets and metadata,
2. create searchable visual/reference representations,
3. retrieve a manageable list of candidate sets,
4. use OpenAI and/or Gemini as candidate analyzers/verifiers,
5. cross-check visible minifigures, distinctive parts, colors, text, and inventories,
6. return ranked candidates with evidence and uncertainty,
7. let Brian confirm, correct, or reject the result.

A custom matching/reranking model may be trained later from confirmed real-world examples.

## Data collection for future training

Photos must be retained from the first working version in a structured way. Each listing should be able to hold:

- original full-screen captures,
- cropped listing photos,
- selected object crops,
- thumbnails and normalized derivatives,
- listing title, description, asking price, URL, and capture date,
- AI provider/model and prompt version,
- ranked candidates and scores,
- Brian's confirmed identity or correction,
- condition/completeness notes,
- purchase decision and purchase price,
- physically verified contents after purchase,
- eventual resale result and time to sell.

Training status should distinguish unreviewed, partially labeled, confirmed, purchase-verified, and training-ready examples.

## Current credentials and likely sources

Brian has OpenAI and Gemini API keys. Additional integrations are expected later for LEGO catalog data and pricing, likely including Rebrickable and BrickLink, but Codex must consult current official documentation and terms when implementing those integrations.

## Hosting

The eventual service will run on Brian's home server and may use a subdomain of `abrianbaker.com`. Local development and proof-of-concept work come first. No production deployment is authorized merely by this document.

## Future possibilities

- Link appraisals to Brian's LEGO sorter after purchase.
- Use actual parts found by the sorter to update set probabilities and completeness.
- Learn personalized resale adjustments from Brian's own purchase and sales outcomes.
- Identify listings where minifigure value or part-out value exceeds complete-set resale value.
