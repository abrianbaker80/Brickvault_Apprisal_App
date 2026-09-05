# Risk-First Roadmap

## Phase 0 — Bootstrap and architecture validation

Deliverables:

- accepted architecture and repository layout,
- ExecPlan for the foundation and risk spikes,
- toolchain/version choices based on current official docs,
- clear acceptance tests and stop conditions.

No product code yet.

## Phase 1 — Foundation vertical slice

Build only enough to prove durable storage:

- PostgreSQL schema/migrations,
- listing creation,
- multi-image upload,
- immutable content-addressed storage,
- exact deduplication,
- thumbnails,
- simple web listing/detail pages,
- tests and local startup documentation.

No AI and no Facebook capture yet.

## Phase 2 — Recognition quality spike

Use a small controlled catalog and a repeatable evaluation harness:

- provider abstractions for OpenAI and Gemini,
- multimodal embedding experiment,
- small reference-image index,
- text clue extraction,
- candidate retrieval and verifier,
- structured output and persisted analysis run,
- evaluation on confirmed sample listings,
- accuracy/cost/latency comparison.

Do not ingest every LEGO set until this proves the approach.

## Phase 3 — Android capture feasibility spike

Prove on a real device:

- Android Share Target into an existing/new listing,
- explicit floating capture control,
- supported screenshot path on Brian's Android version,
- capture without including the BrickVault overlay when possible,
- secure upload to the Phase 1 API,
- manual test checklist and known limitations.

Do not build carousel automation, OCR, or polished UX yet.

## Phase 4 — Core appraisal MVP

Join the proven pieces:

- listing analysis workflow,
- ranked candidates and evidence,
- confirmation/correction UI,
- deterministic valuation inputs and placeholder/manual pricing,
- history and reopening appraisals,
- label states and training-ready decisions.

## Phase 5 — Catalog ingestion and full retrieval

- Rebrickable catalog/inventory import,
- reference image provenance,
- stable multimodal embeddings,
- pgvector search,
- incremental update jobs,
- candidate ranking and cache strategy.

## Phase 6 — Pricing and offer engine

- BrickLink and approved additional price sources,
- snapshot history and caching,
- condition/completeness adjustments,
- resale-channel profiles,
- opening/max offer formulas,
- explanation and unit-test matrix.

## Phase 7 — Polished Android overlay workflow

- multi-photo capture session,
- duplicate/near-duplicate detection,
- crop/circle selection,
- extracted listing text,
- review before upload/analyze,
- compact result overlay and full-app handoff.

## Phase 8 — Outcomes, datasets, and hardening

- purchase/resale outcomes,
- prediction-versus-actual reporting,
- versioned dataset export,
- hard-negative export,
- group-safe train/validation/test splits,
- backup/restore test,
- security and privacy review,
- deployment plan for the home server.
