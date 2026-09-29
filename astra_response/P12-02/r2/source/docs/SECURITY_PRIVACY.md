# Security, Privacy, and Data Integrity

## Phase 9 security qualification closed — 2026-09-26

Phase 9 is **CLOSED** with the final physical evidence recorded in
[ExecPlan 088](plans/088-android-https-auth-source.md). The accepted run retained
direct TLS, exact Host/Origin and credentialed CORS, normal authentication and
CSRF enforcement, `no-store` private responses, passive session timing,
read-only disconnected state, explicit session verification before private
resume, and fresh-process privacy. All five market-evidence expiry profiles
followed server deadlines without cache revival. The held Watchlist response
committed exactly one revision-1 row; the client did not replay it and
reconciled by authoritative readback. No live provider was configured or
contacted.

Cleanup removed the reverse rule, qualification app/trust, owned TEST listener
and disposable database; port 18443 is clear. The ignored evidence and local
TEST certificate/key remain only for audit. Phase 10 is **NEXT / NOT STARTED**.

## Historical Phase 9 physical USB HTTPS qualification — 2026-09-23

The separately authorized physical pass in [ExecPlan 088](plans/088-android-https-auth-source.md)
PASSED on the unchanged debug APK. Its app-scoped public localhost certificate
enabled direct TEST TLS over `adb reverse` without a system phone certificate,
cleartext, proxy or relaxed Host/Origin/CORS policy. The phone completed private
login/session, a CSRF-protected settings save and logout; both session deadlines
were exposed with no-store responses. Passive resume did not renew last activity.
On disconnect, the Watchlist was dated and read-only, writes were unavailable,
and reconnect required explicit session verification. A fresh disconnected
process showed only the public shell, with no recovered private view. No live
provider was configured or contacted.

Cleanup removed the reverse rule and debug app (including app-scoped trust),
temporary Windows PEM/key and disposable TEST database. The certificate's
thumbprint was absent from the six checked CurrentUser/LocalMachine Root, CA
and TrustedPeople stores; no owned TEST listener or container remained running.
Phase 9 remains OPEN only under its existing physical Android core-workflow and
expiry/conflict [roadmap gate](ROADMAP.md#phase-9--pwa-offline-behavior-and-android-core-app).
Earlier source-only and physical-not-started status below is historical.

## Phase 9 Slice 3B source qualification - 2026-09-23

Brian authorized the implementation and source checks in [ExecPlan 088](plans/088-android-https-auth-source.md).
**Slice 3B is CLOSED for its accepted local source checkpoint; Slice 3A is
CLOSED; Phase 9 remains OPEN.** Brian authorized the reviewed 33-file local
commit from `bd6a97f49ab1d08e8b6debab09e5338558285eb8`, subject
`Complete Phase 9 Slice 3B secure Android transport qualification`. This
supersedes earlier source-review and unauthorized status.

An explicit qualification build uses `https://localhost` to
`https://localhost:18443`, exact credentialed CORS and owned TEST direct TLS.
Normal browser/PWA builds remain same-origin. Existing cookies, CSRF, session
limits and private document-memory policy remain authoritative. Official native
resume verification is passive; backup/device transfer are excluded, and extra
localhost trust is an explicit debug-only public-certificate input.

Trusted Chromium with real disposable PostgreSQL and Android debug packaging
passed. This is not WebView/device proof. Brian manually removed the temporary
Windows TEST trust certificate; six trust stores and owned TEST resources were
verified clear. The plan records the exact cleanup and source evidence.
Final physical-device qualification remains NOT STARTED and separately authorized.
No phone, ADB, LAN, provider, development database/service, deployment
or push occurred. This acceptance closes only the Slice 3B source checkpoint.

## Phase 9 Slice 2 authorized — 2026-09-23

**Slice 2 IN PROGRESS.** [ExecPlan 086](plans/086-private-memory-reconnect.md) implements dated
read-only document-memory views and safe reconnect. Brian authorized implementation,
focused validation and owned TEST services; stop for technical/visual review,
without staging or commit. Slice 1 and Phases 7B/7C/8 remain CLOSED. Phase 9 remains
IN PROGRESS; Slice 3 is not started. Earlier Slice 2 prohibitions are historical.

Private data never persists across reload/restart. Only previously authenticated
reads may fall back, within the last confirmed session deadline. Offline use and
passive checks never renew activity. An offline client cannot discover remote
revocation immediately; expiry/logout/principal replacement clear memory.
Reconnect verifies first, rereads visible resources, preserves drafts and never
retries writes or dispatches providers. Watchlist uncertain target/removal writes
require explicit authoritative read-back. No migration, durable private store,
generic sync or offline economics. R-07/R-09/R-36 retain their remaining scope;
Phase 16 and Deferred Economics are unchanged. No development DB/site, provider,
network exposure, Android or deployment work.

## Phase 9 Slice 1 accepted source checkpoint — 2026-09-23

**Slice 1 ACCEPTED / CLOSED FOR ITS SOURCE CHECKPOINT; Phase 9 IN PROGRESS.**
[ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md) records Brian's
technical/visual acceptance and authorized local commit. Public shell alone may
persist; API/auth/private responses remain no-store and outside worker caches.
Offline restart restores no private records. Updates are explicit and preserve
active drafts until Brian chooses reload. No migration; head remains
`0016_hunt_cached_runs`. Capacitor 8.5.2 generation/sync is source feasibility only;
no native/device/deployment acceptance or network/authentication relaxation.

Brian confirmed he accidentally closed both development processes: the listener
incident is resolved, no tooling defect is implicated, and no restart/investigation
is needed. Prior separate validation selections and initial corrections stand.
Slice 2 is next, NOT STARTED / NOT AUTHORIZED; Slice 3 remains later and unstarted.
No private durable store, offline writes, generic sync or provider/background
refresh. R-07/R-36 remain partial; Phase 16 and Deferred Economics boundaries
are unchanged. Earlier Slice 1 in-progress/review-pending statements are historical.

**Phase 9 Slice 1 policy, 2026-09-23:**
[ExecPlan 085](plans/085-public-pwa-capacitor-feasibility.md) permits durable public
shell assets only. APIs/auth/private/provider responses remain no-store and never
enter worker caches. No private IndexedDB/localStorage/sessionStorage or durable
identity/drafts. Fresh offline reload requires connectivity/sign-in. Updates are
explicit and do not automatically reload another workspace. Current session,
logout/reset, CSRF, Host/Origin and network boundaries remain authoritative.
Later read-only document-memory viewing through the last confirmed session
deadline is approved policy for Slice 2, not implemented behavior in Slice 1.

**Checkpoint 2 now authorized:** [ExecPlan 076](plans/076-save-original-forecast.md) records acceptance of
checkpoint 1 for onward integration and bounded API/replay implementation. Earlier
checkpoint-1-only stops below are historical. UI, deployment and commit remain
unauthorized; 7B-3 is IN PROGRESS.

**Current checkpoint authorization:** [ExecPlan 076](plans/076-save-original-forecast.md) authorizes only
7B-3 checkpoint 1, backend Persistence and Save Authority, with synthetic TEST
validation and technical review. Earlier planning-only boundaries below are historical
for this authorization. 7B-3 remains in progress; API/UI and commit are not authorized.

**Private historical snapshots — 2026-09-17:** The [owner decision](DECISIONS.md#phase-7b-3-owner-retention-and-historical-display-authorization--2026-09-17)
clears the project retention/historical-display gate for the authorized private
scope, superseding older unresolved saved-evidence gates below. Authentication,
CSRF, attribution and logging/privacy boundaries remain intact. Public sharing,
raw-response/image/member-data archives and new backup/export systems are excluded.
Only decision documentation and 7B-3 planning are authorized in this run.

## Phase 7B-1 current implementation boundary — 2026-09-17

Brian authorized only [authentication implementation and TEST acceptance](plans/074-brian-only-authentication.md).
This supersedes older documentation-only/no-auth statements below for this slice.
One local principal; no signup, default credentials, auto-bootstrap or auth bypass.
Owner-only interactive bootstrap/reset refuse unavailable hidden input, unowned
targets, missing migrations and incorrect existing account state. Passwords are
12–256 characters; Argon2id uses 64 MiB, three passes, parallelism four, a 16-byte
salt and 32-byte verifier. Five failed attempts within five minutes impose a
five-minute shared cooldown; there is no IP/proxy-header trust for rate handling.

Random opaque session/CSRF secrets are stored only as hashes in PostgreSQL. Cookies
are HttpOnly, host-only, SameSite=Strict, path=/; HTTPS cookies require Secure.
The HTTP exception is off by default and explicitly enabled only by guarded
loopback development/TEST launchers. Existing hosts, ports and disabled proxy trust
remain; allowed Origin scheme must match the direct request scheme. All authenticated
mutations require the matching X-CSRF-Token plus an allowed Origin. Login requires
an allowed Origin and X-BrickVault-Login header. No permissive CORS is added.

All product, refresh, readiness and schema routes fail closed before protected work.
Only non-sensitive liveness, login and public bootstrap assets remain accessible.
Thirty-minute idle and twelve-hour absolute limits are validated server defaults;
search, appraisal, economics and explicit refresh plan/confirm/Resume are activity.
Background status/rejoin polls and passive session/readiness/schema reads do not renew.
Singleton locking serializes revocation and activity; reset revokes every session.
Already admitted bounded refresh work may finish without new provider admission.

Expiry aborts requests/unmounts private views, clears derived output/confirmations,
and keeps only entered Deal assumptions in this document for the same principal.
Explicit logout clears assumptions and broadcasts logout to other tabs. Focus and
visibility revalidate passively. Failed logout leaves views locked with an explicit
retry; it does not falsely claim server revocation. No secret/product state is written
to localStorage, sessionStorage, URLs, logs or acceptance artifacts. HttpOnly cookies
are the intentional browser session mechanism. No service worker/offline cache is added.

Only isolated TEST databases and synthetic accounts have execution authorization.
No actual account setup, development migration, TLS infrastructure, non-loopback
exposure or deployment is authorized. Wrapper/physical-device and deployment acceptance
remain later work. Saved evidence permission is still unresolved, not prohibited.

## Current scope and authorization

This is one private application for Brian. Earlier documentation-only task boundaries below are historical; Phase 11 P11-01 is accepted in [ExecPlan 090](plans/090-home-infrastructure-discovery.md). Phase 12 P12-01 is governed by [ExecPlan 091](plans/091-production-runtime-and-deployment.md), and the accepted P12-02 pre-mutation review is in [ExecPlan 092](plans/092-exact-infrastructure-pre-mutation-review.md).

P11-01, P12-01 and P12-02 are ACCEPTED / CLOSED; Phase 11 is CLOSED and Phase 12 remains IN PROGRESS. P12-03 is NEXT / NOT STARTED and, if separately authorized, is limited to one dedicated VM and base Ubuntu installation after fresh VMID/capacity/bridge checks and an authoritative Ubuntu ISO SHA-256 match. Temporary DHCP and key-only administrator SSH are permitted; the data disk remains unformatted and unused. Proxmox firewall is disabled, and a NIC flag is not protection. P12-03 creates no BrickVault, database, Python 3.13, uv, Caddy, restic/rclone, DNS, certificate, backup job, router or firewall change. P12-02 acceptance authorizes no mutation.

P12-02's configured-key Proxmox SSH check and bounded read-only inventory succeeded, but no home-server, Proxmox, storage, networking/router, DNS, Cloudflare, certificate, backup, service or production database mutation occurred. Brian selected encrypted PostgreSQL logical backups on both the existing Proxmox server and a new Google Drive `Brickvault_Apprisal_App_Backup` folder. Google Drive is the required off-host recovery copy; Proxmox is same-host supplemental recovery. No folder/job or unattended recovery path was created or verified. Brian approved `appraisal.abrianbaker.com` for later application planning; private DNS and platform-trusted certificate setup, backup account access and approved private access remain unresolved for P12-04/P12-05. Real Caddy/TLS/private-DNS and normal-certificate browser/PWA/Android behavior, physical Android acceptance and off-host restore remain unverified. Phase 9 localhost TEST transport/certificate is not production evidence. Never expose PostgreSQL publicly.

Production requires one exact HTTPS application Host and Origin, a derived exact same-site packaged Android Origin, Secure/HttpOnly/SameSite=Strict cookies, existing CSRF, and a loopback FastAPI listener behind the approved Caddy path. The proxy overwrites an internal secret header; Uvicorn does not trust forwarded headers. The production database URL must identify a dedicated loopback database/runtime role with a separate owner/migration role and verified ownership marker. Real secrets belong in admin-protected local service configuration outside the checkout and static build. This source contract is not live transport, certificate, backup or device evidence.

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
