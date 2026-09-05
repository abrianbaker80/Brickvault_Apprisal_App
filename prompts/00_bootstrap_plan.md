# Prompt 00 — Bootstrap and plan

**Use in:** a brand-new Codex chat opened at the repository root  
**Model:** GPT-6 Astra  
**Reasoning:** Extra High  
**Mode:** Plan  
**Expected result:** architecture validation and an ExecPlan only; no application code

---

We are starting the BrickVault Appraisal App. Read every repository-level guidance and product document before doing anything, especially `AGENTS.md`, `.agent/PLANS.md`, and all files under `docs/`.

Your goal in this task is to validate and tighten the architecture, then create a self-contained ExecPlan for Phase 0 and Phase 1. Do **not** scaffold or implement application code yet.

Product facts that must remain true:

- This is a private, single-user, self-hosted app for Brian.
- It analyzes LEGO resale-listing photos, initially from Facebook Marketplace.
- It must eventually provide ranked set candidates, current/fair value, realistic resale value, net value, opening offer, and maximum offer.
- Android should eventually support a Google-like user-triggered overlay/screen-capture experience, but ordinary upload and Android Share are required fallbacks.
- Original images, useful crops, model predictions, Brian's corrections, and later deal outcomes must be preserved for future training.
- AI predictions must never be silently promoted to confirmed labels.
- We will use OpenAI and Gemini through server-side adapters.
- We prefer retrieval plus multimodal verification before custom model training.
- Do not scrape or automate Facebook.

Perform these planning actions:

1. Inspect the empty/planning-stage repository and the local development environment without modifying anything outside the repo.
2. Challenge the proposed modular-monolith architecture in `docs/ARCHITECTURE.md`. Compare realistic alternatives, but optimize for one developer, one user, a home server, maintainability, and future computer-vision/model experimentation.
3. Validate current stable toolchain choices using official documentation where available. Avoid unnecessary bleeding-edge dependencies.
4. Decide and document the proposed repository layout, dependency managers, local-development approach, image-storage abstraction, migration strategy, and API contract strategy.
5. Design Phase 1 as the smallest real vertical slice: create a listing, upload multiple images, preserve immutable originals, exact-deduplicate, generate thumbnails, persist metadata, and view the listing in the web UI. No AI and no Android implementation in Phase 1.
6. Identify the technical risks and define isolated follow-on spikes for LEGO recognition and Android capture. At a planning level, verify the current official availability, authentication requirements, and obvious constraints for likely Rebrickable and BrickLink catalog/pricing integrations; do not implement them yet.
7. Create `docs/plans/000-foundation-and-risk-spikes.md` following `.agent/PLANS.md`.
8. Update `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, or `docs/ROADMAP.md` only when the planning work reveals a concrete improvement. Preserve the product decisions already marked accepted.
9. Provide exact acceptance criteria, commands to validate Phase 1, and a list of any assumptions Brian should review.

Boundaries:

- Do not create app scaffolding, migrations, Docker files, source code, or generated lockfiles in this task.
- Do not add credentials or request that secrets be pasted into chat.
- Do not expand Phase 1 into recognition, pricing, Android, deployment, or custom training.
- Prefer a decisive recommendation over presenting many unresolved options.

Before stopping, inspect the diff to ensure it contains documentation/planning changes only. Then report:

- recommended architecture,
- important changes from the starting proposal,
- assumptions needing Brian's decision,
- the exact next prompt/task to implement Phase 1.
