# Prompt 01 — Implement the storage foundation

**Use in:** the same Codex chat as Prompt 00, after reviewing/accepting the ExecPlan  
**Model:** GPT-6 Astra  
**Reasoning:** High  
**Mode:** Code  
**Expected result:** one working end-to-end storage vertical slice

---

Implement only the approved Phase 1 portion of `docs/plans/000-foundation-and-risk-spikes.md`.

The completed slice must let me:

1. start the development environment from documented commands,
2. create a listing in the browser,
3. upload several PNG/JPEG/WebP images,
4. preserve the original uploaded bytes immutably in the configured local BlobStore,
5. store image metadata and listing relationships in PostgreSQL,
6. detect exact duplicate uploads by SHA-256 without treating duplicates as independent physical blobs,
7. generate and display thumbnails as separate derived assets with lineage,
8. reopen the listing and see its metadata and images.

Requirements:

- Follow `AGENTS.md` and the accepted plan exactly.
- Use migrations; do not rely on automatic schema creation at runtime.
- Validate actual image decoding, MIME type, upload size, and pixel dimensions.
- Make file/database failure behavior transactional or recoverable; document any unavoidable orphan scenario and provide a safe reconciliation command or plan.
- Keep original files immutable.
- Add `.env.example` with placeholders only.
- Do not implement AI, embeddings, LEGO catalog ingestion, pricing, Android code, authentication, remote deployment, queues, MinIO, or background workers.
- Keep the UI functional and clean, but do not spend this milestone on visual polish.
- Add unit and integration tests for hashing/deduplication, upload validation, asset lineage, and listing retrieval.
- Add a lightweight end-to-end or browser test if the selected stack supports it without disproportionate setup.
- Update README/setup documentation and the ExecPlan progress/outcome sections.

Verification:

- Run formatters, linters, type checks, tests, migrations, and builds for every changed component.
- Start the complete local stack and perform one real upload through the UI/API if the environment permits.
- Do not claim a manual test occurred if it did not.

Stop after Phase 1 is complete. Do not begin the Android or recognition spikes. In the final report include changed files, commands run and results, manual verification performed, known limitations, and the recommended next prompt.
