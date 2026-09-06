# BrickVault Codex Execution Plans

An ExecPlan is a living, self-contained design and implementation document that another developer or Codex session can follow using only the repository and the plan.

## When an ExecPlan is required

Use an ExecPlan for:

- a new application or major feature,
- changes spanning Android, web, API, and/or database boundaries,
- database schema or migration work,
- external AI/catalog/pricing integrations,
- the recognition pipeline,
- security or privacy-sensitive behavior,
- deployment and infrastructure changes,
- a refactor likely to take more than one focused coding session.

A tiny, well-contained bug fix does not need a new plan unless the current prompt requests one.

## Plan location and naming

Store plans in `docs/plans/` with a numeric prefix and descriptive slug, for example:

```text
docs/plans/000-local-foundation.md
docs/plans/150-android-capture-spike.md
```

## Required sections

Each plan must include:

1. **Goal and user-visible outcome**
2. **Why this work is being done now**
3. **In scope**
4. **Explicit non-goals**
5. **Current repository state**
6. **Decisions and assumptions**
7. **Data model and API/interface changes**
8. **Implementation sequence** with small checkpoints
9. **Validation and acceptance criteria**
10. **Security, privacy, and data-integrity considerations**
11. **Failure modes, rollback, and recovery**
12. **Progress log** with dated checkboxes
13. **Open questions or physical-device/manual checks**
14. **Outcome and follow-up** completed at the end

## Plan quality rules

- Be specific enough that a new session can continue without relying on chat history.
- Name files, modules, routes, commands, schemas, and test cases when known.
- Explain unfamiliar terms the first time they appear.
- Resolve ordinary implementation details in the plan instead of leaving a cloud of vague questions.
- Clearly mark assumptions that require Brian's decision.
- Do not turn a plan into a sprawling wish list. Keep it bounded to the requested milestone.
- Update the plan as implementation reveals facts. Do not preserve a known-wrong plan merely because it was written first.
- If the prompt says **plan only**, stop before modifying application code.

## Product and phase alignment

Read [requirements traceability](../docs/REQUIREMENTS_TRACEABILITY.md) and [valuation rules](../docs/VALUATION_RULES.md) when planning core work. Keep each ExecPlan bounded to its requested roadmap phase. The Phase 1 foundation has no product workflow; image/capture plans are later modules under D-018/D-021. Historical plan examples do not authorize a phase.
