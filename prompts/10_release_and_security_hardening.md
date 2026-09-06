# Prompt 10 — Local release and security hardening

**Mode:** Plan first; implement only on a separate explicit request

**Expected result:** The locally packaged application passes security, authentication, secret handling, migrations, disposable backup/restore, observability, and release checks without touching production infrastructure.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. Use disposable local data for upgrade/recovery, backup/restore, session expiry/revocation, secret/static-root exposure, logs, error handling, and release smoke checks. Record actual outputs and unresolved blockers. Security scanning that requires network access needs explicit task scope. Do not interpret a deployable artifact as permission to connect to any production system.

## Inputs

Feature-complete core web/PWA/Android, auth, migrations, versioned data, and disposable local release fixtures.

## Scope

Local release packaging, security/auth/secret review, migration/rollback checks, backup/restore rehearsal, observability, and release/check documentation.

## Exclusions

Home-server discovery, Proxmox/router/DNS/Cloudflare changes, public exposure, production deployment, and image modules. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

The locally packaged application passes security, authentication, secret handling, migrations, disposable backup/restore, observability, and release checks without touching production infrastructure.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Record actual check results and unresolved release blockers; local readiness is not deployment authorization.

Local/disposable services only; security-feed/dependency network access requires explicit task scope, and Android release checks distinguish physical evidence.

## Stop condition

Stop after this requested milestone and its reviewable evidence; update relevant Markdown only within the task's authorization and do not begin another phase.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
