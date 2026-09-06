# Security, Privacy, and Data Integrity

## Current scope and authorization

This is one private application for Brian. The current task is documentation realignment only: no application/configuration changes, installs, services, external calls/network resources, staging, or commits.

No home-server, Proxmox, networking/router, DNS, Cloudflare, or production access is authorized. Phase 10 is local hardening. Phase 11 requires separate read-only discovery approval; Phase 12 requires a reviewed deployment plan and distinct execution approval. Never expose PostgreSQL publicly.

## Local and private application access

Phase 1 has no authentication, runs only on loopback, and uses isolated development/test PostgreSQL on 55432/55433. Do not connect to or modify the existing service on 5432. Local dependency installation/startup belongs only to a later explicitly authorized implementation task.

Phase 7 adds Brian-only authentication before non-loopback access. Review session expiry/revocation, password or credential verifier storage, CSRF where applicable, Host/Origin checks, rate handling, and wrapper/browser session behavior. A private LAN is not a substitute for authenticated encrypted access.

FastAPI serves the static build from a separate configurable directory. Unknown /api routes are JSON errors. Configuration, source files, future blobs, and secrets must not be statically served. Avoid permissive CORS and implicit server-binding changes.

## Provider secrets, access, and provenance

All catalog, market, and later AI calls/credentials stay in the server. None may reach React, PWA caches, Android bundles, generated contracts, URLs, or logs. A future .env.example contains placeholders only; local secrets/configuration and private fixtures are ignored. Do not ask Brian to paste secrets into chat.

[PROVIDER_GATES.md](PROVIDER_GATES.md) separates dated research, fixtures, and actual authorized evidence. Verify current access, official API use, display/cache/retention rights, quotas, and cost before calls or durable source-content storage. Never scrape or infer rights from private use.

Preserve provider-scoped mapping provenance, review state, condition, sold/current-listing side, currency, period/time, sample information, and freshness. Missing prices and unresolved mappings are unknown, not zero or guessed identities. Permit source snapshots only under verified rights, while preserving reproducible valuation requirements; report and block incompatible integrations.

## Financial and saved-data integrity

Use exact decimal money, explicit currency/conversion observations, versioned formulas, item allocations, and cost bases under [VALUATION_RULES.md](VALUATION_RULES.md). Prevent duplicate physical proceeds/costs. Retain immutable calculation history and manual overrides with audit provenance.

Saved URLs are metadata only; never fetch a Marketplace page. Render names/notes as text, reject unsafe URL schemes, and avoid unnecessary seller-personal details. Apply migrations, transaction boundaries, revision checks, and appropriately isolated tests.

Logs contain request IDs, useful error codes, duration, and bounded operational counts; exclude credentials, authorization headers, raw provider payloads, unnecessary personal text, and future image bytes/filenames.

## PWA and Android cache privacy — Phase 9

One backend/database is authoritative. Cache only permitted content, show observation/sync dates, and enforce provider freshness/retention rules on local replicas too. Initial offline behavior is read-only; do not pretend cached prices are current or silently queue financial changes.

Review logout/session-expiry cache clearing or locking, sensitive saved notes on shared devices, native credential storage, server URL validation, and synchronization conflicts. Android core-flow/device tests are separate from later overlay feasibility.

## Local release and eventual deployment

Phase 10 tests private authentication, secret handling, migrations, backup/restore on disposable local data, observability, dependency/release checks, and rollback rehearsal. It does not access production. Later backups include all required database data and, only once images exist, consistent blob storage.

Phase 11 discovers actual infrastructure read-only with explicit authorization. Phase 12 validates the approved hostname, TLS/authentication, private database exposure, monitoring, backup/restore, and rollback under its separate authorization.

## Later image privacy and retention gate — Phase 13 onward

Training/image retention begins when image ingestion is implemented, not during catalog/valuation foundation. Listing screenshots may contain seller names, profile photos, locations/addresses, messages, notifications, and unrelated personal content.

Before image ingestion ships, establish an explicit policy covering purpose, image classes, access, retention duration, manual deletion and any future automatic deletion, backups/exports, and recovery. Raw screen captures are the most restricted; cropped LEGO photos and confirmed object crops still need visible-content privacy review. The policy is currently unresolved and blocks that later feature's release.

Preserve immutable original bytes while retained, exact hashes, distinct derivatives, crop/transform lineage, and correct relationship/receipt semantics under [IMAGE_INGESTION.md](IMAGE_INGESTION.md). Immutability prevents accidental overwrite, not intentionally authorized policy deletion. No automatic deletion is authorized by the current plan.

Decode and validate real formats, size/dimensions, and malicious inputs. Store blobs outside static roots. Publish complete immutable bytes before committing metadata, receipt, relationship, and deterministic order changes; failures may leave recoverable unreferenced blobs, never false successes. Consistency checking is report-only.

## Later capture, AI, and training safeguards — Phases 14–16

Every capture is an explicit Brian action, visibly enabled and restricted to intended packages where supported. No Facebook scraping, traffic/credential interception, automatic swipes/clicks, background collection, or seller automation. Share/manual upload remain fallbacks. Device testing is required; official API documentation and APK builds do not prove Facebook compatibility.

Submit only the necessary permitted image/context to server-side OpenAI/Gemini adapters; verify provider data-use/retention settings in that phase. Record model/prompt/version/cost metadata without raw secret-bearing payloads.

Predictions remain unverified until separate Brian confirmation or purchase verification. Training-ready status additionally requires privacy review. Sanitize seller/notification/unrelated screen content before export; preserve rejected candidates as appropriate hard negatives.

Version datasets and keep all connected listing/source derivatives, including shared exact originals, in one partition. Original, crop, prediction, correction, outcome, and export lineage must remain reconstructible under the approved retention policy.
