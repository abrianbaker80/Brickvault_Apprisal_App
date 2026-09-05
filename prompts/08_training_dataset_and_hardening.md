# Prompt 08 — Dataset export, outcomes, and hardening

**Use in:** a new Codex chat after the daily-use appraisal flow is stable  
**Model:** GPT-6 Astra  
**Reasoning:** High; Ultra may be used only for independent audits  
**Mode:** Plan first  
**Expected result:** reproducible datasets, actual-outcome tracking, and a deployable system

---

Plan and implement dataset/versioning, deal-outcome tracking, backup/restore verification, and security hardening.

Dataset requirements:

- Review queue for unreviewed/partially labeled/confirmed/purchase-verified images and object crops.
- Explicit training-ready/excluded decision.
- Versioned dataset releases with immutable manifests and hashes.
- Group-safe train/validation/test splits so no listing or source-image derivatives cross splits.
- Positive pairs, hard negatives, special classes, and provenance.
- Sanitized export that excludes seller-identifying and unrelated screen content.
- Reproducible export CLI with a dry run and summary report.

Outcome requirements:

- bought/not bought,
- purchase price/date,
- physically verified sets/minifigures/missing items,
- replacement and labor costs,
- sale channel/date/gross/fees/shipping/net,
- time to sell,
- predicted versus actual error reporting.

Hardening requirements:

- threat-model review,
- provider secret and logging audit,
- upload/image parser abuse tests,
- database/blob consistency checker,
- backup and restore procedure tested on a disposable environment,
- dependency/security scanning,
- home-server deployment plan with rollback, but no production deployment unless the prompt explicitly authorizes it.

Independent Ultra subagents may review security, data leakage, and test coverage in parallel only after the main implementation is stable. Reconcile their findings into one prioritized report. Stop after the milestone and do not train a custom model yet.
