# Architecture

## Guiding choice

One Python/FastAPI modular monolith, one authoritative PostgreSQL database, and one primary React + Vite + TypeScript interface shared by Chrome, PWA, and an Android package. This serves the unified valuation-first product; optional later recognition supplies identities to that core.

    Chrome / installable PWA ---- shared React UI ---- /api ---- FastAPI
    Android package ------------ same React UI --------|          |
                                                                PostgreSQL
    Server core: catalog -> relationships/mappings -> market -> valuation
                 deals/settings/watchlists -> hunting -> auth/synchronization
    Later only: image ingestion -> recognition -> candidate core identities
                BlobStore, native capture extensions, reviewed training datasets

FastAPI serves the configurable static frontend build. Static hosting may later move to Caddy/reverse proxy without changing frontend API contracts. One backend owns provider calls and financial rules; there is no separate Android, web, or recognition valuation engine.

## Alternatives considered

- Next.js plus FastAPI remains a rejected architecture alternative: server rendering/SEO do not currently justify an additional application runtime.
- Django is viable, but changing the approved FastAPI/React stack has no demonstrated benefit for this correction.
- Separate valuation and recognition repositories/services would duplicate catalog/mapping synchronization or add premature service coordination; explicit modules in one repository are sufficient.
- A separate native Android implementation of core screens duplicates UI maintenance; the shared React UI with a later wrapper is preferred under D-019.
- Microservices, brokers, Kubernetes, and managed object-store infrastructure are unnecessary for the initial single-user workload.

## Repository, dependency, and development boundaries

    apps/web/                 Shared React views and API client
    apps/android/             Phase 9 wrapper; Phase 15 needed native extensions
    services/api/
      src/brickvault_api/
        api/                  HTTP/Pydantic contracts
        application/          Explicit use cases
        persistence/          SQLAlchemy transactions and repositories
        migrations/           Packaged Alembic resources; empty Phase 1 baseline
        catalog/              Phase 2 identities, relationships, mapping/import
        market/               Phase 3 evidence normalization and cache policy
        providers/            Server-side adapters introduced by actual use
        valuation/            Phase 5 pure deterministic calculations
        deals/                Phase 7 saved work and profiles
        auth/                 Phase 7 private access
        hunting/              Phase 8 versioned scores
        synchronization/      Phase 9 cache/version conflict contracts
        images/               Phase 13 only
        recognition/          Phase 14 only
        datasets/             Phase 16 only
      tests/
    packages/contracts/       Pydantic-derived OpenAPI and TypeScript
    infra/                    Separately requested local tooling; deployment later
    scripts/                  Future repeatable developer/check commands

This tree is proposed, not implemented. Create only used directories in the authorized phase. Phase 1 needs API/application/persistence boundaries, not empty future domain modules.

Use one pnpm workspace/root lockfile and one uv project/API lockfile. SQLAlchemy uses explicit synchronous transactions; block work outside the async event loop where required. Avoid generic repository frameworks or event buses. Use Alembic for reviewed migrations, never runtime create_all. Add pgvector only when a later measured retrieval use case needs it.

Local future development runs native FastAPI/Vite with isolated Compose PostgreSQL on loopback ports 55432 (development) and 55433 (test); API 8000 and Vite 5173 also bind loopback. Never connect to or modify the existing PostgreSQL service on 5432. No setup, manifests, Docker files, dependencies, or service startup is authorized by this documentation.

## Core module ownership

| Module | Authoritative responsibility | First phase |
|---|---|---|
| Catalog identity | Explicit sets/minifigures, canonical variants, names/themes | 2 |
| Set/minifigure relationships | Versioned inventory and positive quantities | 2 |
| Provider identifier mappings | Provider namespaces, provenance, review state, no arbitrary matches | 2 |
| Market observations | New/used, sold/listing side, price/sample/time/currency and permitted retention | 3 |
| Deterministic valuation | Strategies, adjusted quantities, costs, profit/ROI/max-buy under exact-decimal rules | 5 |
| Deal analysis | Inputs, adjustments, immutable calculation snapshots | 7 |
| Saved work | Saved sets, deals, target prices, URLs, notes, settings, watchlists | 7 |
| Sets to Hunt | Versioned explainable rankings and insufficient-evidence outcomes | 8 |
| Authentication/synchronization | Brian-only access, authoritative server revisions, dated client caches | 7 / 9 |
| Responsive client | Shared views; no independent provider access or money arithmetic | 1 / 6–9 |

D-025 extends catalog ownership to explicit part/color identities, full inventory choices, figure/component allocation and scoped rarity relationships; market ownership to part prices/activity and shared refresh; valuation ownership to POV, recovery, liquidity/opportunity and burden calculations; and hunting to their explainable score components. These are planned Phases 2–8 capabilities in the existing modules, not new services or Phase 1 work.

Catalog and provider mappings are shared across every use case. A set number suffix is part of identity, not text to discard. A provider's figure ID is not assumed to equal another provider's identifier. No catalog-set-only generic record substitutes for quantity-bearing figure relationships.

## API contract strategy

Every endpoint, including health, readiness, documentation, and OpenAPI, lives under /api. Generate TypeScript from Pydantic-derived OpenAPI in packages/contracts and use openapi-fetch. Contracts export without a live database or provider keys; drift checks compare regenerated output.

Vite proxies /api locally; the browser production build uses relative /api URLs. The Android package uses an explicitly configured authenticated server base plus the same /api paths; loopback on a phone is not the development PC. The base URL is not a provider credential.

Amounts are decimal strings with currency; quantities are integers. Evidence/status enums distinguish unknown, unresolved mapping, unavailable, stale, and thin data. API errors stay JSON, including unknown /api routes; static fallback never returns HTML success for missing API or static assets.

## Phase 1 API — foundation only

- GET /api/health: process liveness; no provider or production checks.
- GET /api/ready: isolated database connectivity and expected Alembic revision, with 503 on dependency/schema unavailability.
- GET /api/openapi.json: generated schema, independent of a live database.

Use the Alembic revision table to prove an empty baseline migration round-trip; no product entities are needed. The web shell displays health/readiness and useful unavailable states at desktop/mobile viewports. There are no listing, image, catalog, provider, valuation, or Android endpoints in Phase 1. [ExecPlan 000](plans/000-local-foundation.md) is the canonical approved execution plan, not implementation authorization.

Phase 1 runs only through separately authorized Slices 1A (toolchain/workspace), 1B (isolated database/API/contracts), and 1C (web shell/built serving/CI/full acceptance). Slice 1A creates no API/frontend source, migrations, Compose infrastructure, or CI. Packaged Alembic resources keep the future API distribution and readiness migration graph together. The future browser-test API uses loopback port 18000 independently of development port 8000.

The planned built shell has only the / frontend route and /assets; Swagger/ReDoc are disabled in Phase 1. Missing assets and unknown /api routes stay errors. GitHub Actions is planned in Slice 1C for Ubuntu full checks and Windows portability checks, with no live product-provider dependency. These are approved design details, not implemented or freshly version-verified behavior.

## Later core API responsibilities

| Phase | Proposed contract responsibility |
|---|---|
| 2–4 | Import/provider/feasibility commands and server services; do not expose provider credentials or claim the browser feature exists. |
| 6 | GET /api/catalog/sets?query=... provides bounded deterministic name search; GET /api/catalog/sets/resolve?set_number=... resolves suffix/variant identity or explicit ambiguity. |
| 6 | GET /api/catalog/sets/{set_id} returns set identity, versioned figure inventory/quantities, permitted image references, separate whole-set/figure new/used sold and listing observations, coverage-aware totals, and provenance/freshness. |
| 7 | POST /api/valuations evaluates a supplied set/strategy/adjustment profile using the same engine; /api/deals persists reproducible snapshots with asking price, URLs, targets, and notes. |
| 7 | /api/saved-sets, /api/watchlist, /api/settings, /api/selling-profiles, and /api/auth supply private saved workflows; precise CRUD/auth contracts are defined in that phase's ExecPlan. |
| 8 | GET /api/hunts returns versioned score snapshots, supported opportunities, explanations, and blocked/partial evidence states. |
| 9 | Revision/conditional-write and synchronization metadata support one authoritative server state and bounded dated caches. |
| 16 | Append actual purchase/resale outcomes to saved deals without changing historical estimates. |

Phase 6 detail responses cannot require a listing session or recognition run. Set detail combines market observations with the Phase 5 total/coverage rules; fee/target deal recommendations appear through the Phase 7 workflow.

## Part-out and liquidity data flow — planned Phases 2–8

Authoritative versioned set inventory resolves exact part/color/condition quantities and mutually exclusive sale allocation. Server-side providers supply normalized item-level price/activity observations to the existing PostgreSQL market store. Shared deterministic valuation functions produce four POV views, part-liquidity/opportunity and set-level results, consumed by Set Detail, saved strategy comparisons and Hunt components. No client or recognition module recalculates these values.

The initial evidence path is inventory plus item-level observations. Phase 3 verifies whether an authorized aggregate capability exists; a permitted direct result may supply additional evidence/benchmarking, but cannot erase our inclusion, provenance or coverage contract. Phase 4 compares equivalent settings with BrickLink-displayed values where authorized and practical. “BrickLink Part Out Value” naming requires demonstrated equivalence and permitted use.

### Shared observation cache and priority refresh

Phase 3 designs provider_cache_entry and durable provider_refresh_job ownership within the same backend/PostgreSQL application. Begin with a bounded worker execution mode in the modular monolith and PostgreSQL job state/leases; this plan does not add Redis, brokers, microservices or another database. Any later alternative needs measured justification and its own review. No queue/worker is implemented or started in Phase 1 or this amendment.

Set Detail reads existing permitted observations/derived snapshots and returns fresh, stale-with-refresh, partial, pending or blocked states promptly. A bounded idempotent refresh request can enqueue missing/stale keys; the user-facing detail request never waits for hundreds of synchronous provider calls. Shared keys deduplicate across searched sets, watchlists and Hunt candidates. Responses carry independent price/activity ages, coverage and refresh status, not a fresh timestamp hiding old evidence.

Cache keys include provider/type/item/color, condition, SOLD/CURRENT, region, currency, statistic/window, relevant source parameters and mapping compatibility. Apply source-specific TTL, maximum stale-display and retention limits, bounded concurrency and account quotas, Retry-After/backoff with attempt/deadline caps, negative-cache expiry and per-key/provider failure isolation. In-flight deduplication and transactional leases prevent concurrent refresh duplication; version/time checks prevent late stale results overwriting newer cache pointers. Retain immutable observations referenced by history only where rights allow.

Priority classes consider Brian's explicit search, watchlisted sets, Hunt candidates, valuable liquid lots, stale high-value observations and broader coverage. Define quotas/fairness/aging so background work cannot exhaust foreground budget or starve indefinitely. Record request reason, policy/adapter version, attempt, quota status, source observation times and outcomes without credentials/raw private payloads. Refresh failure preserves usable dated evidence within permitted limits; expired or prohibited data stays unavailable. Prices and activity can fail independently.

### Planned generated API and UI contracts

Phase 6 extends set detail or its bounded /api/catalog/sets/{set_id}/part-out resource with the minimum snapshot contract in [the part-out plan](plans/005-set-part-out-values.md). Paginated lot drill-down exposes exact identity/allocation, permitted images, source prices/activity, formula inputs and Gem/classification reasons. A bounded refresh-status/request contract may be defined in that phase using the Phase 3 service; precise routes remain a reviewed interface decision, not implemented endpoints.

The shared React Part-Out Analysis area shows the four-view matrix, recoverable gross, Liquid/Fast Cash/dead-stock, premium, concentrations, density and burden with explicit proxy/unknown/partial labels. Phase 7 /api/valuations and saved deals compare separate strategies and persist assumptions/thresholds/freshness; Phase 8 /api/hunts adds decomposable part-out/competition/rarity/liquidity components. Decimal/null-plus-state representations, server-only arithmetic, generated OpenAPI/TypeScript, revision conflicts and existing private-access/cache rules remain authoritative.

## Client, authentication, and offline boundaries

Phase 7 introduces private authentication before any non-loopback access; current loopback Phase 1 contains no authentication. Choose and review the exact browser/wrapper session mechanism in Phase 7/9, keeping provider secrets server-side and protecting state changes.

Phase 9 prefers Capacitor and packages the same React interface. Native Android code is limited to needed device extensions; overlay/Share are Phase 15. No separate catalog or financial database lives on the phone.

Initially offline mode is read-only access to explicitly cached set details, saved deals, and watchlists with visible observation/sync dates. New searches, price refresh, financial recalculation, and writes require connectivity. Do not silently queue financial writes or imply stale cache is current. Online saved edits use server revisions and explicit conflict handling rather than last-write-wins data loss. Persisted historical calculations remain labeled historical.

## Later image and recognition modules — Phases 13–16

[IMAGE_INGESTION.md](IMAGE_INGESTION.md) preserves immutable SHA-256 BlobStore bytes, separate semantic assets/lineage, listing_image_id relationships, partial success, client UUID/display_order stability, minimum-successful-receipt ordering, and recoverable receipts for successful duplicates.

Phase 13 later routes include POST/GET /api/listings, GET /api/listings/{id}, POST /api/listings/{id}/images, and controlled GET /api/images/{asset_id}/content. Optional listing-to-deal references never make direct set search depend on images. Filesystem and DB publication are not one transaction; preserve recoverable complete orphan blobs and a report-only consistency command.

Phase 14 adds analysis runs, candidate canonical identities, provider/model versions, evidence, and separate confirmation events. Retrieval uses shared catalog/mappings/reference metadata; it has no second catalog, market rules, or valuation arithmetic. Phase 15 adds separately tested native Share/capture. Phase 16 adds privacy-reviewed labels, datasets, and actual outcomes.

## Deferred gates

Provider eligibility, mapping/price coverage, current rights, quotas, and retention are unverified until [provider gates](PROVIDER_GATES.md) pass. Android packaging/physical behavior also needs its own evidence. Image retention/deletion policy is a Phase 13 release gate.

Phase 10 local security/release work does not authorize infrastructure access. Phase 11 read-only discovery and Phase 12 deployment have separate explicit approvals; neither is included in Phase 1. No public PostgreSQL exposure.
