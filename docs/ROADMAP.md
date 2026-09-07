# Valuation-First Roadmap

## Status and phase map

Current checkpoint: Slices 1A and 1B are accepted; [ExecPlan 000](plans/000-local-foundation.md) records the reviewed local foundation evidence. Slice 1C is not started and Phase 1 is incomplete. The next authorized action is the separately approved Part-Out Value + liquidity documentation amendment; it is not performed by the Slice 1B acceptance task. One unified platform uses the deterministic core first; recognition is an optional Phase 14 input. Prompt 01 remains PLAN ONLY when reused. No phase entry or completed slice itself authorizes implementation, network access, service startup, staging, a commit, or a push.

Each roadmap phase maps to exactly one numbered prompt. Prompts 13–16 refine the later image extension; they do not displace Phases 1–12. Inputs and gates must be satisfied before advancing.

| Phase | Name | Prompt |
|---|---|---|
| 0 | Bootstrap and plan | [00_bootstrap_plan.md](../prompts/00_bootstrap_plan.md) |
| 1 | Repository and local foundation | [01_scaffold_foundation.md](../prompts/01_scaffold_foundation.md) |
| 2 | Catalog and set/minifigure relationships | [02_catalog_and_relationships.md](../prompts/02_catalog_and_relationships.md) |
| 3 | Market-price provider integration | [03_market_price_provider.md](../prompts/03_market_price_provider.md) |
| 4 | Representative-set feasibility gate | [04_feasibility_gate.md](../prompts/04_feasibility_gate.md) |
| 5 | Deterministic valuation engine | [05_valuation_engine.md](../prompts/05_valuation_engine.md) |
| 6 | Set search and detail vertical slice | [06_set_search_and_detail.md](../prompts/06_set_search_and_detail.md) |
| 7 | Deal calculator and saved work | [07_deal_calculator_and_saved_work.md](../prompts/07_deal_calculator_and_saved_work.md) |
| 8 | Sets to Hunt | [08_sets_to_hunt.md](../prompts/08_sets_to_hunt.md) |
| 9 | PWA, offline behavior, and Android core app | [09_pwa_and_android.md](../prompts/09_pwa_and_android.md) |
| 10 | Local release and security hardening | [10_release_and_security_hardening.md](../prompts/10_release_and_security_hardening.md) |
| 11 | Read-only home-server discovery | [11_home_server_discovery_read_only.md](../prompts/11_home_server_discovery_read_only.md) |
| 12 | Approved home-server deployment | [12_home_server_deployment_explicit.md](../prompts/12_home_server_deployment_explicit.md) |
| 13 | Marketplace image ingestion | [13_marketplace_image_ingestion.md](../prompts/13_marketplace_image_ingestion.md) |
| 14 | Recognition quality spike | [14_recognition_spike.md](../prompts/14_recognition_spike.md) |
| 15 | Android share and overlay capture | [15_android_capture_overlay.md](../prompts/15_android_capture_overlay.md) |
| 16 | Training datasets, outcomes, and recognition hardening | [16_training_dataset_and_hardening.md](../prompts/16_training_dataset_and_hardening.md) |

## Phase 0 — Bootstrap and plan

- **Inputs:** Authoritative product definition, current guidance, decision history, and the product-scope audit.
- **Scope:** Read/revalidate the unified product and bounded Phase 1 ExecPlan; keep valuation-first ordering and historical decisions explicit.
- **Exclusions:** Application implementation, installations, services, provider/network calls, infrastructure access, and staging/commits.
- **Acceptance:** The in-chat plan preserves the ten requirements and defines only the local foundation, with reviewable assumptions and a stop before edits or implementation.
- **Gate:** The reviewed documentation baseline is the Phase 0 checkpoint; subsequent revalidation is plan-only unless Brian separately requests Markdown/local-Git work.
- **Access and evidence:** Local read-only files only; no network, devices, or servers.

## Phase 1 — Repository and local foundation

- **Inputs:** Approved product/architecture and canonical [ExecPlan 000](plans/000-local-foundation.md); a separate explicit implementation request for the selected slice.
- **Scope:** React/Vite responsive shell, FastAPI shell, isolated PostgreSQL, SQLAlchemy/Alembic empty baseline, health/readiness/OpenAPI and generated TypeScript contracts, strict checks, provider-free CI, and local setup documentation.
- **Exclusions:** Catalog imports/providers/prices/valuation/search/deals/authentication/Sets to Hunt, listings/images/recognition, PWA/Android, and home-server/deployment work.
- **Acceptance:** The implemented local web shell and API run against an isolated migrated database with reproducible contract/format/lint/type/unit/integration/build checks, CI definitions, and built-serving desktop/mobile browser evidence. No product tables or external providers are required.
- **Gate:** Each of Slices 1A, 1B, and 1C requires separate explicit implementation authorization and ends with a report; completion does not authorize the next slice. Prompt 01 is reusable plan-only review. Slice 1B acceptance authorizes only its bounded corrections and conditional local checkpoint; it does not begin Slice 1C.
- **Access and evidence:** Slice 1A may verify/install local toolchains and resolve packages only under its explicit dependency/network scope, with no services/database work. Slice 1B separately authorizes isolated local database/API work. Slice 1C separately authorizes web/CI/local acceptance. Never contact product providers, existing PostgreSQL on 5432, or home infrastructure.

### Slice 1A — Toolchain and workspace

Verify supported toolchains/compatibility; create workspace/manifests/configuration and exact locks; add format/lint/type/orchestration foundations; resolve and commit locks only under the slice's explicit local-Git authorization. Report applicable checks and stop before database or application-shell work.

### Slice 1B — Database, API, and contracts

After separate authorization, add isolated development/test PostgreSQL, guarded tooling, SQLAlchemy/Alembic, health/readiness/OpenAPI, deterministic TypeScript contracts, and real unit/integration/contract checks. Report and stop before frontend/built-serving/browser/CI completion.

### Slice 1C — Web shell, built serving, CI, and acceptance

After separate authorization, add React status UI, Vite proxy, FastAPI built serving, browser smoke tests, and GitHub Actions. Run every full Phase 1 acceptance criterion, update permitted documentation, report, and stop before Phase 2. The slice split does not weaken final acceptance.

## Phase 2 — Catalog and set/minifigure relationships

R-11 addition: [set part-out plan](plans/005-set-part-out-values.md) adds versioned component/color quantities and exact provider mappings here, component guides in Phase 3, coverage/website comparison in Phase 4, separate new/used decimal aggregation in Phase 5, and set-detail display in Phase 6. It is a theoretical sourcing metric; existing exclusions for full piece-by-piece sales operations and treating theoretical totals as cash remain. No Phase 1 work is added.

- **Inputs:** Completed local foundation; explicit identity/quantity contracts and permitted local catalog fixtures.
- **Scope:** Repeatable imports of sets, suffixed-number normalization, names/themes, minifigures, versioned quantity relationships, provider-scoped mappings, provenance, and source versions.
- **Exclusions:** Pricing/valuation implementation, browser search/detail workflow, image ingestion, embeddings, recognition, scraping, and infrastructure changes.
- **Acceptance:** Verified fixtures resolve representative numbers/names and return every included minifigure with correct quantities, including duplicates and variants, while ambiguous mappings and malformed data remain explicit.
- **Gate:** Review import/source-use rights before source data is used; no arbitrary suffix stripping or first-match mapping; fixtures do not establish provider access.
- **Access and evidence:** Local fixtures suffice for implementation checks; live catalog/download requests require separately authorized network access and verified source permissions.

## Phase 3 — Market-price provider integration

- **Inputs:** Verified canonical identities/relationships and mappings; provider-gate checklist and permitted fixtures.
- **Scope:** Server-side adapters/cache for sets and minifigures, separate new/used and sold/current-listing evidence, exact amounts/currencies, observation/sample times/quantities, and explicit unavailable/stale/thin states.
- **Exclusions:** Scraping, guessed mappings, browser/Android secrets, valuation UI, recognition, unlimited retention assumptions, and infrastructure administration.
- **Acceptance:** Authorized provider calls or labeled recorded fixtures produce normalized provenance-rich observations without guessing mappings, conflating conditions/market sides, or treating missing prices as zero.
- **Gate:** Verify current official authentication/eligibility, rights/display/cache/retention, quotas/cost, and outbound-IP requirements before live calls or provider-content persistence; missing permissions block that path.
- **Access and evidence:** Network/provider access is required for live proof and must be explicitly authorized; recorded-fixture checks remain distinguishable and cannot certify live access.

## Phase 4 — Representative-set feasibility gate

- **Inputs:** Catalog/mapping versions, normalized market adapter, permitted observations, and a documented representative sample.
- **Scope:** Evaluate modern/retired, zero/one/many/repeated figures, one valuable dominant figure, suffixed variants, unresolved mappings, missing prices, stale/thin evidence, and supported residual-build assumptions.
- **Exclusions:** Recognition benchmarks, scaling imports instead of evaluating coverage, fabricated provider access/rights, product UI expansion, and production access.
- **Acceptance:** A reproducible report demonstrates usable whole-set and minifigure new/used evidence coverage, documents every gap and request/display/retention constraint, and states whether deterministic sourcing is supported, partial, or blocked.
- **Gate:** No live rights/account/coverage claim before this gate actually runs; fixture-only evidence cannot pass live-product feasibility, and critical unsupported mappings/evidence block advancement to supported recommendations.
- **Access and evidence:** Live feasibility requires authorized provider/network access and Brian review; offline fixtures can rehearse the report only, with live gates explicitly unresolved.

## Phase 5 — Deterministic valuation engine

- **Inputs:** Phase 4 feasibility outcome, exact valuation rules, verified representative fixtures, and supported evidence policies.
- **Scope:** Implement pure server-side arithmetic and serializable versioned input/output snapshots for quantities, strategies, adjustments, costs, profit/ROI, both maximum-buy constraints, and blocked/partial results.
- **Exclusions:** UI financial logic, live provider calls required by unit tests, image/AI work, full individual-piece part-out, automatic purchasing, and production access.
- **Acceptance:** Table-driven tests reproduce every displayed calculation for complete, missing, damaged, repeated, unavailable, and variable-tax/premium cases without double-counting minifigures or costs.
- **Gate:** Review formula/rounding/constraint examples and unsupported-evidence behavior before exposing recommendations; preserve rights-compliant reproducibility.
- **Access and evidence:** Local deterministic fixtures; dependency access only if separately authorized for implementation, no product-provider or server access needed.

## Phase 6 — Set search and detail vertical slice

- **Inputs:** Verified catalog/market contracts, passed feasibility gate, and tested valuation totals/coverage functions.
- **Scope:** Direct suffixed-number/name search and a set-detail API/React page with whole-set and minifigure new/used values, quantities/totals, permitted images/references, separate market sides, provenance, and unavailable states.
- **Exclusions:** Listing sessions, user image uploads, recognition, separate client formulas, saved-deal editing, and deployment.
- **Acceptance:** Brian enters a set number or name without images, resolves the correct variant, and sees whole-set values plus every included minifigure, quantities, individual values, quantity-aware totals, provenance/freshness, and explicit missing-data indicators.
- **Gate:** Browser/API acceptance must cover ambiguity, no-figure, repeated-figure, and unavailable-price cases with image modules disabled.
- **Access and evidence:** Local fixtures/cached permitted evidence for tests; any live refresh remains within the already verified and explicitly authorized provider scope.

## Phase 7 — Deal calculator and saved work

- **Inputs:** Direct set detail and tested valuation engine; reviewed private authentication and persistence design.
- **Scope:** Asking price, actual contents/condition, build/instructions/box adjustments, selling profiles and costs, proceeds/profit/ROI/max buy, saved sets/deals/notes/watchlists/targets/settings, and Brian-only authentication.
- **Exclusions:** Recognition/capture, new arithmetic in clients, offline writes, seller automation, provider-rights bypass, and production work.
- **Acceptance:** A saved deal survives reload and every recommendation reproduces from visible inputs, persisted assumptions, and versioned output, with authenticated access, missing/damaged adjustments, and saved targets/notes/watchlists.
- **Gate:** Review authentication and source-retention compatibility before persistent private workflows or any approved non-loopback access; revision conflicts cannot silently overwrite saved work.
- **Access and evidence:** Local private tests first; no LAN/public binding change or home access without explicit scope, and provider access remains separately bounded.

## Phase 8 — Sets to Hunt

- **Inputs:** Supported market/valuation snapshots, saved targets/profiles, feasibility policies, and deterministic sample opportunities.
- **Scope:** Versioned ranking/explanations using profit/ROI/max buy, figure-value coverage, sales activity/freshness/confidence, top-figure concentration, residual-estimate dependence, listings/orders, and operational burden.
- **Exclusions:** Scraping for deals, automatic purchases/contact, invented asking prices, theoretical part-out cash, recognition, and production access.
- **Acceptance:** Reproducible results identify supported split-sale opportunities and explain every score, with insufficient/stale evidence reducing confidence or blocking ranking instead of producing false precision.
- **Gate:** Test ties, missing/thin/stale prices, concentration, residual assumptions, and selling burden; disclose a hypothetical acquisition assumption when no asking price exists.
- **Access and evidence:** Local fixture/cached snapshot evaluation; separately authorized provider refresh only under established quotas/rights.

## Phase 9 — PWA, offline behavior, and Android core app

- **Inputs:** Private sourcing workflows, shared React UI/API, versioned saved work, and an authorized Android packaging test environment.
- **Scope:** Installable PWA and preferably Capacitor Android package of the same UI, private auth, dated read-only caches, explicit offline states, and server-revision synchronization.
- **Exclusions:** Separate native core UI/database/valuation engine, offline financial recalculation/writes, overlay/capture/Share implementation, and home deployment.
- **Acceptance:** Chrome/PWA and Android support set search/detail, deal analysis, saved work, and watchlists through one backend/database, and cached information is dated without representing stale prices as current.
- **Gate:** Document the packaging spike and any justified alternative; test physical Android core workflows and auth/cache expiry/sync conflicts separately from compilation.
- **Access and evidence:** Authorized local SDK/dependency acquisition and physical Android device testing; device-to-API networking needs explicit secure scope, not home-server access.

## Phase 10 — Local release and security hardening

- **Inputs:** Feature-complete core web/PWA/Android, auth, migrations, versioned data, and disposable local release fixtures.
- **Scope:** Local release packaging, security/auth/secret review, migration/rollback checks, backup/restore rehearsal, observability, and release/check documentation.
- **Exclusions:** Home-server discovery, Proxmox/router/DNS/Cloudflare changes, public exposure, production deployment, and image modules.
- **Acceptance:** The locally packaged application passes security, authentication, secret handling, migrations, disposable backup/restore, observability, and release checks without touching production infrastructure.
- **Gate:** Record actual check results and unresolved release blockers; local readiness is not deployment authorization.
- **Access and evidence:** Local/disposable services only; security-feed/dependency network access requires explicit task scope, and Android release checks distinguish physical evidence.

## Phase 11 — Read-only home-server discovery

- **Inputs:** Completed local release evidence and Brian's separate explicit authorization naming discovery targets/access.
- **Scope:** Read-only discovery of actual Proxmox, networking, storage, proxy/tunnel, backup, monitoring, and rollback constraints; document facts and unknowns.
- **Exclusions:** Any remote/local configuration mutation, installs, service starts/restarts, deployments, database writes, DNS/Cloudflare/router changes, staging, and commits.
- **Acceptance:** A read-only report identifies actual infrastructure constraints and a proposed deployment boundary without making changes.
- **Gate:** Separate explicit discovery authorization is mandatory before any connection; discovery permission is never deployment permission.
- **Access and evidence:** Only explicitly authorized home/network/control-plane read access; no credentials in chat or broad exploratory target discovery.

## Phase 12 — Approved home-server deployment

- **Inputs:** Phase 11 actual findings, local release artifacts, reviewed deployment/backup/rollback plan, exact approved hostname and targets, and distinct explicit execution authorization.
- **Scope:** Execute only the approved deployment steps and validate private application operation under the selected abrianbaker.com subdomain.
- **Exclusions:** Unapproved host/network/DNS changes, public PostgreSQL, unrelated systems, recognition scope, and implicit staging/commits.
- **Acceptance:** The approved subdomain passes authenticated HTTPS, backup/restore, monitoring, and rollback checks, and PostgreSQL is never publicly exposed.
- **Gate:** Do not connect or execute without both reviewed concrete plan and separate deployment approval; DNS/tunnel/router changes must be explicitly included in that plan's authorization.
- **Access and evidence:** Only specifically approved production/home/DNS/control-plane actions; stop at a changed target or material discovery mismatch before broadening scope.

## Phase 13 — Marketplace image ingestion

- **Inputs:** Proven deterministic core, separately requested image ExecPlan, and reviewed image privacy/retention/deletion policy.
- **Scope:** Optional listing metadata/session workflow, multi-file upload, immutable originals, exact dedupe, thumbnails/lineage, listing_image_id, independent partial success, stable UUID/display_order, duplicate receipts, and report-only consistency checking.
- **Exclusions:** Recognition/model calls, new catalogs/pricing/offer formulas, native capture, near-duplicate/crop polish, training exports, automatic deletion, and infrastructure changes.
- **Acceptance:** Images attach to optional listings without affecting direct lookup, original bytes/lineage survive restart, and real concurrency/failure tests prove deterministic order and recoverable successful-duplicate receipts.
- **Gate:** Apply IMAGE_INGESTION.md and approve explicit retention/deletion/privacy policy before shipping; current documentation never authorizes image handling or production deployment.
- **Access and evidence:** Local authorized image fixtures and isolated services; no source-URL fetching or provider calls, and production rollout remains separately authorized.

## Phase 14 — Recognition quality spike

- **Inputs:** Proven core/image ingestion, rights-cleared catalog references, separately confirmed listing examples, and approved provider/spending scope.
- **Scope:** Candidate set/minifigure identities using shared catalog/mappings, server-side OpenAI/Gemini adapters, text clues, retrieval/verification comparison, analysis provenance, and separate corrections.
- **Exclusions:** A parallel catalog/mapping/valuation engine, model-invented finance, custom training, full catalog/vector infrastructure without evidence, Android capture, and deployment.
- **Acceptance:** A repeatable small-catalog evaluation measures identification/retrieval/unknown/cost/latency behavior and routes candidate canonical identities into the same core while direct set search works with recognition disabled.
- **Gate:** Verify current model/account/image-use/retention/cost conditions before live calls; fixture results are not paid-provider benchmarks or confirmed labels.
- **Access and evidence:** Explicitly authorized paid/provider network scope for live evidence; no claims of live accuracy from synthetic fixtures.

## Phase 15 — Android share and overlay capture

- **Inputs:** Working shared-UI Android core, proven image API, recognition findings, approved retention policy, and Brian's physical-device details.
- **Scope:** Needed native Share extension and isolated visible user-triggered allowlisted capture spike; only after device proof, manual multi-photo review/crop/order and result handoff with robust partial retries.
- **Exclusions:** A second native core app, automatic browsing/swipes/clicks, Facebook traffic/credential interception, unattended capture, independent valuation, and unapproved infrastructure access.
- **Acceptance:** Physical-device evidence proves supported Share/capture flows and fallback/permission/failure behavior while the same core UI/API/data and direct lookup remain usable when capture is disabled.
- **Gate:** Separate spike results from polished follow-on work; do not claim Facebook compatibility from an APK/emulator or move past a failed device gate.
- **Access and evidence:** Explicitly authorized Android SDK/device tests and supported-API research; any secure device/backend networking is scoped separately from production administration.

## Phase 16 — Training datasets, outcomes, and recognition hardening

- **Inputs:** Proven deterministic app and optional image/capture flows, reviewed labels/privacy policy, and preserved valuation histories.
- **Scope:** Append purchase/resale outcomes, forecast-versus-actual reports, reviewed label states, sanitized versioned exports, hard negatives, connected-source-safe splits, image security/recovery and backup regression.
- **Exclusions:** Custom model training, automatic promotion of predictions, provider-rights assumptions, deleting originals outside policy, duplicated valuation rules, and unapproved production operations.
- **Acceptance:** Actual outcomes append without rewriting forecasts, and a reproducible sanitized dataset/export plus regression evidence preserves confirmed-label provenance, connected-source split integrity, receipts/order, and recoverable data.
- **Gate:** Verify export/source rights and every training-ready confirmation/privacy decision; physical capture limitations remain explicit and custom training needs a new request.
- **Access and evidence:** Local/disposable export and backup checks; private data/provider/device/production access only when separately authorized for the exact check.

## Shared acceptance authority

Use [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [VALUATION_RULES.md](VALUATION_RULES.md), [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md), [PROVIDER_GATES.md](PROVIDER_GATES.md), and [SECURITY_PRIVACY.md](SECURITY_PRIVACY.md). Product phases remain planned; foundation evidence is limited to the accepted slices recorded in ExecPlan 000. Dated research and fixtures do not constitute provider or physical-device proof.
