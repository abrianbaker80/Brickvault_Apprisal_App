# Prompt 04 — Core appraisal workflow

**Use in:** a new Codex chat after the Android and recognition spikes have documented outcomes  
**Model:** GPT-6 Astra  
**Reasoning:** High  
**Mode:** Plan first  
**Expected result:** a usable manual-upload recognition workflow

---

Create an ExecPlan and implement the smallest usable BrickVault appraisal workflow using only techniques proven by the completed foundation and recognition spikes.

The workflow must allow Brian to:

1. create or open a listing,
2. add listing title, description, asking price, URL, and multiple images,
3. start an analysis run,
4. see processing status and failures,
5. review ranked candidate sets for the listing or selected object crop,
6. see evidence, contradictions, confidence, and requested follow-up images,
7. confirm a candidate, enter a different set number, or classify the image as unknown/custom/mixed/insufficient evidence,
8. preserve the confirmation as an append-only event separate from predictions,
9. mark eligible confirmed crops with a label state suitable for future dataset review,
10. reopen the listing and see the complete audit trail.

Include a basic transparent appraisal placeholder driven by manually entered price inputs if live pricing is not implemented yet. It must clearly label manual versus sourced values and use deterministic arithmetic.

Do not implement full catalog ingestion, live pricing, polished overlay capture, custom training, or production deployment in this milestone.

Add appropriate migrations, tests, web UI states, API contracts, and documentation. Run all relevant quality gates and stop when this vertical slice is complete.
