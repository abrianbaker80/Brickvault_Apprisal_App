# Codex Workflow for BrickVault Appraisal App

## Chat strategy

Use one repository, but do **not** use one endless Codex chat.

- Start a brand-new Codex chat for project bootstrap.
- Keep plan review and implementation of the same tightly scoped milestone in that chat.
- Start a new chat when beginning a new major milestone, when changing from Android to recognition/pricing work, or when the current chat has accumulated obsolete assumptions.
- Every new chat opens the same repository and reads `AGENTS.md` plus the current plan, so continuity comes from files rather than an enormous conversation.
- Keep the current ChatGPT conversation for product decisions, tradeoffs, and generation of future Codex prompts.

## Model and reasoning guidance

| Work type | Model | Reasoning | Mode |
|---|---|---:|---|
| Initial architecture and risk plan | GPT-6 Astra | Extra High | Plan |
| Cross-stack implementation milestone | GPT-6 Astra | High | Code after plan review |
| Android capture/accessibility work | GPT-6 Astra | High or Extra High | Plan first |
| Recognition/ranking design | GPT-6 Astra | Extra High | Plan first |
| Well-scoped endpoint, migration, or test | GPT-6 Astra | Medium | Code |
| Small UI adjustment | GPT-6 Astra | Light/Medium | Code |
| Difficult cross-stack debugging | GPT-6 Astra | Extra High; Max only if needed | Plan/debug |
| Independent audits after interfaces stabilize | GPT-6 Astra | Ultra selectively | Multi-agent |

### Why not Ultra at the beginning?

Ultra is best when meaningful parts can run independently. At project inception, architecture, contracts, and data semantics are tightly coupled. Parallel agents can produce competing stacks and inconsistent interfaces. Use Ultra later for bounded parallel work such as independent security, test, and accessibility reviews.

## Prompt rhythm

1. Give Codex one milestone prompt.
2. Require an ExecPlan for complex work.
3. Review the plan and correct product assumptions before implementation.
4. Tell Codex to implement only the approved plan.
5. Require tests/builds and a concise report.
6. Review the diff or use `/review` before starting the next milestone.
7. Commit a clean checkpoint.
8. Start a new chat for the next milestone.

## Usage-control rules

- Do not ask Codex to “build the entire app.”
- Avoid broad prompts such as “keep improving it.”
- Give explicit stop conditions.
- Keep each implementation prompt to one independently testable slice.
- Use Medium for routine follow-ups rather than leaving every task on Extra High.
- Do not use Max or Ultra merely because they are available.
