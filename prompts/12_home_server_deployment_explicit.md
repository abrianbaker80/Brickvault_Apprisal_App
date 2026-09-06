# Prompt 12 — Approved home-server deployment

**Mode:** Plan first; distinct explicit deployment authorization required

**Expected result:** The approved subdomain passes authenticated HTTPS, backup/restore, monitoring, and rollback checks, and PostgreSQL is never publicly exposed.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. If a reviewed concrete deployment plan and distinct execution approval are absent, remain plan-only and do not connect. The plan must name artifacts, hosts, storage/database isolation, hostname, approved network/DNS/proxy/tunnel actions, private auth/TLS, backup, observability, rollback triggers, and validation. After explicit authorization execute only that scope; discovery permission is insufficient. Never expose PostgreSQL or modify unrelated services.

## Inputs

Phase 11 actual findings, local release artifacts, reviewed deployment/backup/rollback plan, exact approved hostname and targets, and distinct explicit execution authorization.

## Scope

Execute only the approved deployment steps and validate private application operation under the selected abrianbaker.com subdomain.

## Exclusions

Unapproved host/network/DNS changes, public PostgreSQL, unrelated systems, recognition scope, and implicit staging/commits. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

The approved subdomain passes authenticated HTTPS, backup/restore, monitoring, and rollback checks, and PostgreSQL is never publicly exposed.

Record actual relevant checks, commands/results, and limitations; distinguish fixtures, live calls, builds, browser checks, and physical-device evidence. Do not fabricate unavailable verification.

## Gate and access

Do not connect or execute without both reviewed concrete plan and separate deployment approval; DNS/tunnel/router changes must be explicitly included in that plan's authorization.

Only specifically approved production/home/DNS/control-plane actions; stop at a changed target or material discovery mismatch before broadening scope.

## Stop condition

Stop after the explicitly approved deployment and its validation, or report the blocking prerequisite without unauthorized action.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
