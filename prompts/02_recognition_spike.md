# Prompt 02 — Recognition quality spike

**Use in:** a new Codex chat after the foundation is stable  
**Model:** GPT-6 Astra  
**Reasoning:** Extra High for planning, High for implementation  
**Mode:** Plan first  
**Expected result:** measured evidence that the recognition architecture works on a small catalog

---

Plan and implement a bounded LEGO recognition quality spike. Read `AGENTS.md`, product documents, the current API architecture, and completed plans first.

The goal is not to ingest every LEGO set or claim production accuracy. The goal is to build a repeatable evaluation harness and determine whether candidate retrieval plus multimodal verification is promising.

Scope:

1. Add provider interfaces for OpenAI vision/reasoning and Gemini vision/embedding calls. Keep model IDs configurable and all calls server-side.
2. Add a small fixture/reference catalog—roughly 25 to 100 deliberately similar and dissimilar sets—using legally appropriate local test fixtures or metadata. Do not bulk scrape websites.
3. Implement Gemini multimodal image embeddings through the current official API and store/search them in the existing architecture. Use pgvector only if justified by the accepted plan; a deterministic in-memory/brute-force index is acceptable for this tiny spike if it simplifies measurement.
4. Implement text clue extraction from supplied listing title/description and visible image text where supported.
5. Retrieve top candidate sets, then send a limited candidate packet to a configurable multimodal verifier. The verifier must return strict structured output containing rank, confidence, supporting evidence, contradictions, and requested additional views.
6. Persist the analysis run, provider/model/template versions, candidate scores, latency, and estimated usage/cost without storing secrets or giant raw provider payloads.
7. Create a CLI or test command that evaluates a labeled fixture set and reports at minimum top-1 accuracy, top-3 recall, unknown handling, average latency, and estimated cost by strategy/provider.
8. Compare at least these strategies:
   - direct multimodal identification without retrieval,
   - embedding retrieval alone,
   - retrieval plus verifier.
9. Surface one simple results view in the existing web listing page, but keep UI effort minimal.

Data integrity:

- Predictions remain unverified.
- Store user confirmation separately.
- Include unknown/insufficient-evidence outcomes.
- Ensure fixture derivatives from the same source do not leak across evaluation splits.

Boundaries:

- No full Rebrickable import.
- No custom model training.
- No pricing or offer engine.
- No invented benchmark claims.
- If live API keys are unavailable, implement and test the provider contracts with recorded/synthetic fixtures, then clearly list the live commands Brian must run; do not report live results.

Before stopping, run the complete evaluation available in the environment and make a recommendation: continue with this architecture, revise it, or abandon a weak approach. Include evidence, not vibes.
