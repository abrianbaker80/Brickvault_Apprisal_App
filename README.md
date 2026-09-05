# BrickVault Appraisal App

Private, self-hosted software for analyzing LEGO listings—initially Facebook Marketplace listings—from screenshots or Android screen capture, identifying likely sets, estimating current market and resale value, and calculating a rational offer.

The originating chat has been distilled into `docs/ORIGINATING_CHAT_SUMMARY.md` so Codex receives the decisions without carrying a bloated transcript.

This starter package is intentionally **documentation-first**. It gives Codex durable project context and a sequence of narrowly scoped prompts. It does not contain production application code yet.

## Product principles

- Single-user: built specifically for Brian, not as a public SaaS product.
- Private and self-hosted: API keys, listing history, images, and training data stay under Brian's control.
- Risk-first: prove Android capture and LEGO recognition before investing in the complete app.
- Dataset-first: retain useful listing photos and verified labels from the first working build.
- Retrieval before training: index the LEGO catalog and retrieve candidates before considering a custom recognition model.
- Human-confirmed truth: an AI prediction is never treated as a verified training label until Brian confirms it.

## Recommended repository shape

```text
apps/
  web/                  Browser UI
  android/              Native Android capture/share client
services/
  api/                  Python API and application logic
packages/
  contracts/            Generated/shared API contracts when useful
infra/                   Local development and deployment files
docs/                    Product, architecture, decisions, and plans
.agent/PLANS.md          Rules for Codex execution plans
AGENTS.md                Persistent Codex project guidance
```

The exact framework versions and a few implementation choices must be validated by Codex against current official documentation before scaffolding.

## How to begin in Codex

1. Create a new local folder or repository named `brickvault-appraisal-app`.
2. Copy this starter package into the repository root.
3. Open that folder in Codex.
4. Start a **new Codex chat** with GPT-6 Astra, Extra High reasoning, and Plan mode.
5. Paste `prompts/00_bootstrap_plan.md`.
6. Review the plan before allowing implementation.
7. Continue with `prompts/01_scaffold_foundation.md` in the same chat only after the plan is accepted.
8. Run the recognition spike next; it tests the core product premise before the advanced Android overlay.
9. Then run the Android capture spike and continue with one fresh Codex chat per later milestone, always in the same repository.

See `CODEX_WORKFLOW.md` for the model, reasoning, and chat strategy.
