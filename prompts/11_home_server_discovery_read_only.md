# Prompt 11 — Read-only home-server discovery

**Mode:** Plan first; explicitly authorized read-only execution only

**Expected result:** A read-only report identifies actual infrastructure constraints and a proposed deployment boundary without making changes.

## Instructions

Read AGENTS.md, CODEX_WORKFLOW.md, the product specification, valuation rules, data model, decisions, traceability, roadmap, and relevant ExecPlans. Use current checked-out documents, never the historical starter ZIP. PLAN FIRST until Brian explicitly authorizes the named read-only discovery targets. Then use only permitted read operations; no writes, installs, restarts, DNS changes, state-changing probes, or secret dumping. Record observed infrastructure, unknowns, backup/rollback constraints, proposed isolation, and questions for a later deployment plan. Report only unless a separate request explicitly permits saving Markdown; never make remote changes.

## Inputs

Completed local release evidence and Brian's separate explicit authorization naming discovery targets/access.

## Scope

Read-only discovery of actual Proxmox, networking, storage, proxy/tunnel, backup, monitoring, and rollback constraints; document facts and unknowns.

## Exclusions

Any remote/local configuration mutation, installs, service starts/restarts, deployments, database writes, DNS/Cloudflare/router changes, staging, and commits. No staging or commits unless Brian explicitly requests them. No later phase begins automatically.

## Acceptance evidence

A read-only report identifies actual infrastructure constraints and a proposed deployment boundary without making changes.

Distinguish observations from assumptions and record that every operation was read-only.

## Gate and access

Separate explicit discovery authorization is mandatory before any connection; discovery permission is never deployment permission.

Only explicitly authorized home/network/control-plane read access; no credentials in chat or broad exploratory target discovery.

## Stop condition

Stop after the authorized read-only report. Do not deploy or change infrastructure.

[Roadmap](../docs/ROADMAP.md) · [Product](../docs/PRODUCT_SPEC.md) · [Traceability](../docs/REQUIREMENTS_TRACEABILITY.md)
