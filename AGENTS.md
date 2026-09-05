# BrickVault Appraisal App — Codex Guidance

## Product truth

- This is a private, single-user application for Brian.
- Its purpose is to analyze LEGO resale listings, identify likely official sets and minifigures, estimate current market value and realistic resale value, and recommend an opening and maximum offer.
- Initial listing source: Facebook Marketplace. The product must also support ordinary image upload and Android sharing so it is not dependent on Facebook's UI.
- The system will be self-hosted on Brian's home infrastructure. Do not deploy to, modify, restart, or administer any server unless the current task explicitly authorizes it.
- The product name is **BrickVault Appraisal App**. The repository slug is `brickvault-appraisal-app`.

## Read before complex work

Before planning or implementing a cross-cutting change, read:

1. `docs/PROJECT_CONTEXT.md`
2. `docs/ORIGINATING_CHAT_SUMMARY.md`
3. `docs/PRODUCT_SPEC.md`
4. `docs/DECISIONS.md`
5. `docs/ARCHITECTURE.md`
6. The relevant current plan under `docs/plans/`

For a complex feature, significant refactor, schema change, external integration, Android capture change, or deployment change, use an ExecPlan as defined in `.agent/PLANS.md`.

## Working method

- Work in small, reviewable vertical slices.
- Implement only the milestone requested in the current prompt. Do not silently begin later roadmap phases.
- Prefer the smallest defensible change over a broad rewrite.
- Inspect existing code and tests before editing.
- State assumptions in the plan or final report. When an assumption becomes an accepted project decision, update `docs/DECISIONS.md`.
- Keep durable requirements in repository documents rather than depending on chat memory.
- Do not fabricate successful tests, device verification, API behavior, or external service responses.
- Stop and report clearly when a step requires physical-device testing, credentials, a paid API, or access that is not present.

## Architecture guardrails

- Native Android features belong in `apps/android` using Kotlin and Jetpack Compose unless an accepted decision says otherwise.
- The browser UI belongs in `apps/web`.
- Server-side application logic, model-provider calls, image processing, catalog ingestion, valuation logic, and secrets belong in `services/api`.
- The server API is the source of truth. Android and web clients must not independently implement valuation rules or call AI/catalog/pricing providers directly.
- External providers must be behind interfaces/adapters so OpenAI, Gemini, Rebrickable, BrickLink, or future sources can be replaced or compared.
- Keep AI model IDs and provider settings configurable. Do not scatter model names throughout the codebase.
- Start without Redis, a message broker, Kubernetes, MinIO, or microservices unless measured need justifies them. Use a storage abstraction so local filesystem storage can later be replaced by S3-compatible storage.
- PostgreSQL is the planned metadata store. Use migrations for every schema change. Use pgvector only where vector retrieval is actually implemented.
- Generate or share typed API contracts rather than duplicating request/response shapes manually across clients.

## Facebook and Android boundaries

- Do not scrape Facebook, intercept traffic, reuse Facebook credentials, automate seller interactions, or build unattended browsing.
- Capture must be initiated by Brian through an explicit action.
- Restrict accessibility-assisted capture to approved package names and make the active state visibly obvious.
- Prefer Android's supported APIs. For Android 14+ evaluate window-specific screenshot capture so the app's overlay is not included in the captured image. Keep a share-target/manual-upload fallback.
- Do not claim an AccessibilityService or overlay works in Facebook until it has been tested on Brian's physical device.

## Image and training-data integrity

- Preserve original uploaded bytes as immutable assets. Never overwrite the only copy.
- Address image assets by content hash and detect exact duplicates.
- Store raw screenshots, cropped listing photos, object crops, thumbnails, and training derivatives as distinct assets with lineage.
- Separate full-screen captures that may contain personal information from sanitized LEGO-photo crops.
- A model prediction is not ground truth.
- Only Brian-confirmed labels, or labels verified after physical purchase, may become training-ready.
- Save rejected candidates as hard negatives where appropriate.
- Prevent data leakage: derivatives from one original listing must not be split across training and validation/test partitions.
- Dataset releases must be versioned and reproducible.

## Security and privacy

- Never commit API keys, tokens, passwords, cookies, seller identities, or production configuration.
- Keep OpenAI, Gemini, Rebrickable, BrickLink, and any future credentials server-side.
- Provide `.env.example` with placeholders only.
- Redact or exclude seller names, profile photos, chat messages, notifications, exact addresses, and unrelated screen content from training-ready images and exports.
- Logs must not contain image bytes, secrets, authorization headers, or unnecessary personal data.
- Any remote access design must use authenticated encrypted access. Do not expose an unauthenticated development service to the public internet.

## Quality gates

For every implementation task, run the relevant available checks before stopping:

- formatter
- linter
- static/type checks
- unit tests
- integration tests affected by the change
- build for each changed application

For UI work, verify the relevant route and responsive viewport when the environment permits. For Android work, distinguish compilation/emulator checks from physical-device verification.

Every completed task must leave:

- code in a buildable state,
- tests or a documented reason a test cannot yet exist,
- updated relevant documentation,
- no unrelated generated files,
- a concise final report listing changes, verification performed, limitations, and the next logical milestone.

## Code review rules

Flag these as high priority:

- AI guesses persisted as confirmed labels.
- Original images overwritten or deleted by derivative generation.
- API keys or provider calls in client code.
- Facebook automation or background capture without explicit user action.
- Duplicate valuation formulas in multiple clients.
- Unbounded external API calls without caching, rate handling, or cost logging.
- Database changes without migrations.
- Tests that mock away the behavior they claim to verify.
