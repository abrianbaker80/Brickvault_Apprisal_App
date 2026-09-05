# Originating Chat Summary

This file distills the product discussion that created BrickVault Appraisal App. It is intentionally shorter and more actionable than a verbatim transcript.

## Initial idea

Brian wants an app that can analyze Facebook Marketplace LEGO listings when the seller does not provide a set name or number. The app should inspect listing photographs, identify likely sets, and provide current value and realistic resale value before Brian makes an offer.

Brian already has OpenAI and Gemini API keys.

## Discussion of training on every LEGO set

The first idea was to train an AI using images and metadata for every released set from sources such as Rebrickable and BrickLink.

The recommended approach is instead:

- index/catalog every set,
- store reference images and metadata,
- create visual embeddings,
- retrieve the closest candidates for a Marketplace image,
- use a multimodal model to compare the strongest candidates,
- use minifigures, distinctive parts, colors, printed elements, visible text, theme, year, and inventories as supporting/contradicting evidence,
- return ranked candidates with uncertainty,
- collect Brian's corrections,
- train a specialized matcher/reranker only after enough confirmed real Marketplace examples exist.

This avoids a brittle fixed classifier with tens of thousands of classes and avoids pretending pristine catalog photos resemble messy real listings.

## Private-use decision

Brian clarified that the app will be used solely by him.

Consequences:

- no registration, billing, subscriptions, teams, or public support,
- no need for app-store distribution,
- self-hosting on Brian's home server is preferred,
- the app can learn Brian's actual resale channels, costs, margins, labor, and risk tolerance,
- a browser UI and Android companion can share the same server data.

## Facebook Marketplace capture idea

Brian asked for a smoother way to select Marketplace images, similar to Google's screen overlay/read-the-screen experience.

The desired Android experience is:

- open a Marketplace listing,
- tap a floating BrickVault control,
- capture the current Facebook window/photo,
- swipe the image carousel manually,
- capture additional photos,
- see the number of collected/unique photos,
- optionally crop or circle a particular set/object,
- extract or enter title, description, asking price, and URL,
- send one listing session to the private server,
- view a compact appraisal result or open the full app.

The application must not scrape Facebook, intercept credentials/traffic, or autonomously navigate/click/swipe. Android Share and ordinary upload remain dependable fallbacks.

## Save images for future training

Brian decided that listing photos should be saved on the server so they can later be used for training.

The recommended data design saves:

- immutable original screen captures,
- cropped listing photographs,
- object-level crops,
- thumbnails/normalized derivatives,
- listing metadata and asking price,
- AI model/provider/prompt versions,
- candidate sets and scores,
- Brian's confirmed or corrected identity,
- hard-negative candidates,
- condition/completeness notes,
- purchase price and physically verified contents,
- eventual resale proceeds, costs, profit, and time to sell.

A prediction is not training truth. Training states should include unreviewed, partially labeled, confirmed, purchase-verified, training-ready, and excluded.

Seller identity, profile photos, messages, notifications, exact addresses, and unrelated screen content should not enter training-ready exports.

## Codex implementation decision

Brian will use Codex with GPT-6 Astra to write the code and wants carefully scoped prompts plus guidance on reasoning level and chat continuity.

Recommended workflow:

- one repository/project,
- durable context in `AGENTS.md` and `docs/`,
- one Codex chat per major milestone,
- plan first for difficult work,
- Extra High reasoning for initial architecture and recognition design,
- High for substantial implementations,
- Medium for routine focused edits,
- Ultra only when stable interfaces allow genuinely independent sub-tasks.

The build should proceed through risk-controlled vertical slices rather than one prompt asking Codex to build the entire application.
