# Prompt 05 — Catalog ingestion and scalable retrieval

**Use in:** a new Codex chat after the recognition approach has passed its spike criteria  
**Model:** GPT-6 Astra  
**Reasoning:** High/Extra High  
**Mode:** Plan first  
**Expected result:** repeatable catalog import and incremental visual retrieval

---

Plan and implement the LEGO catalog and reference-image ingestion milestone.

Requirements:

- Consult current official Rebrickable, BrickLink, provider, and image-source documentation/terms before coding.
- Prefer official bulk downloads/APIs and incremental synchronization; do not scrape HTML pages.
- Record source, source identifier, import version/date, licensing/provenance notes, and mappings between canonical set identifiers.
- Import set metadata, theme/year/piece count, inventories/minifigures where useful, and approved reference-image metadata/assets.
- Make imports resumable and idempotent.
- Validate and quarantine malformed records rather than silently dropping them.
- Generate configurable Gemini multimodal embeddings in batches, record embedding model/version/dimension, and support incremental re-embedding.
- Implement pgvector similarity search with filters and deterministic tie handling.
- Add cache/rate-limit/retry behavior and cost reporting.
- Provide CLI commands and an admin/status page showing catalog counts, failures, embedding coverage, and last sync.
- Add integration tests with small fixtures and at least one documented live smoke-test path when credentials are present.

Do not add pricing, custom model training, or Facebook automation. Stop after catalog retrieval is reliable and documented.
