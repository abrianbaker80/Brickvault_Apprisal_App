# ExecPlan 091 — Production runtime and deployment

## P12-02 accepted closeout and P12-03 boundary — 2026-09-29

ChatGPT accepted P12-02 `r1` at review commit
`639b10dc483da27d85cd983b204d281e218b5b6c`. P12-02 is CLOSED, Phase 12
is IN PROGRESS, and P12-03 is NEXT / NOT STARTED. Accepted point-in-time
Proxmox facts and the conditional VM design remain in
[ExecPlan 092](092-exact-infrastructure-pre-mutation-review.md). Its corrected
P12-03 scope, if separately authorized, is only a new dedicated VM and base
Ubuntu Server installation. Recheck VMID 115, node CPU/RAM, `local-zfs`,
`vmbr1`, and the exact Ubuntu ISO hash against Ubuntu's published checksum
before any mutation. Temporary DHCP and key-only administrator SSH may be
used; the new data disk remains unformatted and unused. No BrickVault,
PostgreSQL, Python 3.13, uv, Caddy, restic/rclone, production secrets, DNS,
certificate, backup job, router or firewall change belongs to P12-03.
The two selected encrypted database copies, private DNS/certificate, runtime
package sources, guarded production administration and live acceptance remain
P12-04/P12-05 prerequisites. P12-02 acceptance authorizes no mutation.

## P12-02 review snapshot — 2026-09-29

Historical pre-acceptance status: P12-01 remained accepted as recorded below.
P12-02 was authorized for a bounded read-only Proxmox pass and exact
pre-mutation review, and remained in progress pending ChatGPT review. The SSH
check succeeded, replacing the placeholder-access unknown at the P12-01
closeout. Actual node facts,
conditional placement, unresolved backup/DNS/package gates and the full future
mutation order are in [ExecPlan 092](092-exact-infrastructure-pre-mutation-review.md).
No infrastructure mutation occurred. The P12-03 base provisioning, P12-04
deployment and P12-05 acceptance approvals below remain separate and are not
authorized by P12-02.

## P12-01 historical goal and authorization

Phase 10 and Phase 11 are closed. Brian authorized Phase 12 **P12-01 only**:
implement and locally prove a private production application runtime and Android
HTTPS transport, then make a minimum read-only attempt to resolve hosting facts.
P12-01 is ACCEPTED / CLOSED after review of the published r1 package. Phase 12
remains IN PROGRESS; P12-02 is NEXT / NOT STARTED. No production VM, database,
service, DNS, certificate, firewall, backup, provider or device change occurred
in this slice. P12-02 and later slices need separate review and authorization.

## Why now and accepted baseline

The accepted [Phase 11 discovery](090-home-infrastructure-discovery.md) found an
existing Ubuntu 24.04 KVM guest hosting a legacy BrickVault backend and
loopback PostgreSQL 16. Its 64 assigned vCPUs and 125 GiB RAM describe that
guest only, not spare Proxmox capacity. Its unmounted 200 GB disk has unknown
ownership and cannot be adopted. No active reverse proxy was observed on that
guest; a proxy elsewhere was not ruled out. Proxmox node/version/capacity,
storage, inventory, network and backup policy, plus off-host retention, remained
unknown. The dedicated Ubuntu VM and initial 4-vCPU, 8-GiB RAM, 32-GiB OS and
128-GiB data sizing are conditional proposals. PostgreSQL must never be public.
The Phase 9 localhost TEST certificate and transport do not qualify production.
The [Phase 10 packaged release](089-local-packaged-release-readiness.md) provides
accepted local build/static/API evidence; production configuration changes need
their own focused proof.

## Scope and non-goals

P12-01 adds explicit production settings, database-target validation, one exact
HTTPS Host/Origin contract, Secure cookies and existing CSRF enforcement across
one Caddy-to-loopback-FastAPI path. It adds an explicit Android production origin
configuration using normal platform TLS validation and the same web/backend
origin. It uses only an owned, disposable local PostgreSQL database for the
production-style HTTP proof, and checks the existing configured Proxmox target
read-only if usable. No schema migration or API contract change is expected.
Production provisioning, real secrets, DNS, certificates, backups, data migration,
Android build/device acceptance and deployment are outside this slice.

## Current application state and decisions

At the start of P12-01 the API accepted only development/TEST database targets and local
Host/Origin values; Uvicorn disables proxy-header trust. Auth uses HttpOnly,
host-only, SameSite=Strict cookies and CSRF. Normal web/PWA requests are
same-origin. Android's Phase 9 qualification uses a packaged localhost origin,
localhost TEST API and opt-in debug-only TEST certificate.

Production will require explicit loopback bind, API port, HTTPS application
origin, runtime database URL, ownership marker, proxy shared secret, static
serving and absolute build directory. The URL identifies a dedicated database
and runtime role; the matched owner/migration role is distinct. Both roles and
database must be provisioned by a later reviewed mutation slice. Local TEST
proof may use the existing owned TEST PostgreSQL service with run-specific
production-style database and roles; it does not make that service production.

The proxy will overwrite an internal identity header on every upstream request.
FastAPI accepts the exact configured Host and Origin and only that proxy identity.
Uvicorn remains bound to loopback with `proxy_headers=False`; no
`X-Forwarded-*` field controls application authorization, scheme or cookies.
Production auth emits Secure cookies by the reviewed HTTPS proxy contract.
Browser/PWA assets and API remain same-origin. Production Android packages the
same React build at an exact `https://android.<approved-host>` WebView origin
and calls `https://<approved-host>` over the normal WebView network stack.
These origins are same-site for Strict cookies; the API allows only this derived
native Origin for credentialed CORS. Capacitor's `server.url` live-reload
setting is not used. The APK must use system certificate trust only; physical
cookie/WebView behavior remains for P12-05 acceptance.

The application source now implements this contract. Production target
validation requires canonical `127.0.0.1` with an explicit port, dedicated
`brickvault_<name>` database, matched `_owner` and `_runtime` roles, 64-character
lowercase hex passwords and a marker matching the recorded database owner.
It rejects development/TEST names, remote/ambiguous targets and libpq PG*
overrides. The runtime role's enumerated grants remain the existing migration
policy; no schema migration was added. Production also requires an absolute
static build path, no loopback HTTP auth shortcut, no Android TEST qualification,
and an explicit proxy secret. Optional provider credentials remain server-side,
  from a separately approved protected absolute directory outside Git checkouts.

The proposed Caddy route has one HTTPS site name and one loopback FastAPI
upstream. Its upstream request must retain the exact original Host and
overwrite `X-BrickVault-Proxy` from a protected Caddy setting, even when a
client supplied that header. This is a configuration contract, not an applied
Caddyfile. Caddy's HTTP-to-HTTPS redirect, certificate challenge/renewal and
private DNS route depend on P12-02 facts. Uvicorn never interprets forwarded
headers, and the application derives Secure-cookie behavior only from the
validated production proxy path.

## P12-01 implementation sequence

1. Add strict production settings/target and proxy-origin validation without
   changing development/TEST acceptance.
2. Apply the production boundary to Host, Origin, auth transport, Secure cookies
   and database ownership checks. Keep static allowlist and private no-store.
3. Add explicit production Capacitor origin configuration and focused checks;
   retain the TEST localhost path only outside production mode.
4. Run focused settings/boundary/Android tests and one disposable local
   production-mode HTTP/database proof. Run targeted format, lint and type checks,
   and inspect the task diff. Reuse accepted packaging evidence unless changed
   source requires one build.
5. Make only the minimum read-only configured Proxmox check; record inaccessible
   access or newly observed facts without guessing targets.
6. Publish a sanitized P12-01 review package from an isolated checkout. Leave
   implementation uncommitted on main with an empty index.

## Validation and acceptance

Prove refusal of missing/HTTP production origin, missing database/ownership/proxy
inputs, wrong Host/Origin, duplicate headers, direct loopback requests without
proxy identity and arbitrary forwarded-header bypasses. Prove the exact origin
works, Secure/HttpOnly/Strict cookies and CSRF remain enforced, private responses
remain no-store, current migrations and the least-privilege runtime role work,
and secrets do not enter static bytes, responses or safe logs. Android checks
must reject HTTP, localhost/TEST and malformed production origins while ordinary
web/PWA and TEST behavior remain intact. No provider or physical-device calls.

### Actual P12-01 local results

- Focused Python settings, request-boundary and unchanged local/Android tests:
  **94 passed** initially; the **24** focused production tests passed after the
  final missing-Origin and credential-root hardening. Two already-known upstream
  test-client deprecations were reported.
- Focused web/Android configuration tests: **12 passed**. Targeted Ruff,
  mypy, Prettier, ESLint and TypeScript checks passed.
- The final run-owned PostgreSQL proof migrated the current graph under a
  separate owner role, authenticated browser and native-origin requests through
  the synthetic proxy path, preserved Secure/Strict cookies and CSRF, returned
  private no-store responses, denied runtime DDL and removed the exact database
  and roles with zero leftovers. Its private ledger stays ignored.
- A synthetic `android-production` Vite build, existing frontend byte/privacy
  verifier and Capacitor copy/config check passed. The first build exposed an
  unwanted TEST API literal in the production bundle; the build-time gate was
  corrected and the final bundle excludes it. No APK was built.
- The production copied hostname rejected opt-in TEST certificate trust during
  Gradle configuration. Ordinary offline `gradlew help` passed; neither command
  compiled or packaged Android. An initial offline configuration attempt lacked
  cached pinned Android plugins; they were retrieved for the subsequent guard
  check. No phone, certificate infrastructure or provider was used.
- `git diff --check` passed. Local Markdown targets in changed documentation
  resolved. Main HEAD/index and the three protected dirty-file hashes were
  preserved. No Proxmox connection or infrastructure mutation occurred.

## Deployment topology proposed for later review

Conditional on actual Proxmox capacity, storage, network and backup facts:
dedicated Ubuntu VM on a reviewed private bridge/VLAN; Caddy serving one exact
approved HTTPS name; Caddy proxies to FastAPI bound to `127.0.0.1` on an
explicit internal port; PostgreSQL bound only to a workload-local socket or
loopback with a dedicated database and separate owner/migration and runtime
roles. Browser/PWA load the trusted HTTPS site; bundled Android assets use the
derived same-site origin and call that trusted site for `/api`. Never expose
PostgreSQL publicly or reuse the legacy guest's unowned disk/database.

## Later mutation sequence and per-slice gates

1. **P12-02 — exact pre-mutation review:** verify Proxmox capacity, storage,
   inventory, bridge/VLAN/firewall and backup target; select VM placement,
   hostname, private DNS/HTTPS validation and renewal path, data/bootstrap
   policy, secrets placement and rollback. Present exact commands/targets and
   require Brian/ChatGPT review before any mutation.
2. **P12-03 — separately approved base provisioning:** create only the reviewed
   VM/disks/network placement; install reviewed pinned base software, create
   protected local service configuration and role separation. Check capacity,
   isolation and restore point before each irreversible step. No legacy guest
   changes.
3. **P12-04 — separately approved deployment:** create owned PostgreSQL
   database/roles, apply the current Alembic graph as owner, grant only the
   enumerated runtime privileges, bootstrap Brian's principal through an
   approved private input, install the reviewed artifact/systemd unit, configure
   Caddy/private DNS/certificate and monitoring, then configure off-host backup
   and retention. Verify database is workload-only before enabling the path.
4. **P12-05 — private acceptance and closeout:** verify browser/PWA/Android
   normal certificate validation, auth/CSRF/Host/Origin, private access,
   monitoring, an off-host restore rehearsal and rollback. Only actual evidence
   can close Phase 12.

## Secrets, backup, recovery and rollback

P12-02 must approve a root/admin-owned local environment or credential file
outside the checkout, with restrictive permissions and systemd `EnvironmentFile`
or equivalent simple local loading. Caddy's internal proxy secret and the API
must receive the same value through protected configuration. Database passwords,
provider credentials and bootstrap inputs remain server-side, outside static
assets and review packages. P12-01 provisions no real secret.
When real provider credentials are activated, verify their canonical secret
directory and restrictive filesystem permissions as part of production secret
placement. The source path check is not a live permissions check.
The initial proposal is a new empty dedicated database at the current Alembic
head with no copy from the legacy guest. P12-02 must decide whether any
pre-existing data is actually required, approve the database/role creation and
credential rotation policy, and specify a hidden-input owner bootstrap/reset
procedure. The current local `auth:bootstrap` helper is not a production
provisioner; P12-04 must implement or approve its production counterpart before
account creation.

Before any later data/schema change, capture and verify an off-host database
backup plus role/configuration recovery material under a selected retention
policy. A VM snapshot alone is insufficient. Preserve the prior release and
record migration compatibility; for incompatible schema/data changes, restore
the verified backup before rolling the application back. Reverse Caddy/private
DNS changes only against their exact reviewed prior state. Stop cutover if
backup, certificate, private routing, database isolation or rollback checks fail.

## Read-only preflight facts and remaining questions

The configured Proxmox SSH alias still resolves to a placeholder, so P12-01
made no remote Proxmox connection. Node version/capacity/usage, storage pools,
VM/LXC inventory, bridge/VLAN and firewall status, backup jobs/retention and
off-host target remain unknown. Proxy service elsewhere and private DNS
mechanism remain unknown. Brian must choose/approve the exact private hostname,
Android reachability, data/bootstrap policy and backup target before mutation.
Do not infer spare host capacity from the existing guest allocation.

| Prerequisite | P12-01 status | Next gate |
| --- | --- | --- |
| Proxmox node, capacity, pools, inventory, bridge/VLAN, firewall | Unknown; configured target is a placeholder | Read-only authenticated facts before VM placement |
| Exact private hostname, DNS and HTTPS challenge/renewal path | Unknown | Brian/P12-02 selection and certificate plan |
| Off-host backup target and retention | Unknown | P12-02 selection plus P12-05 restore proof |
| Production runtime and database target | Implemented and locally exercised with disposable PostgreSQL | Actual VM/database/role creation separately authorized |
| Exact Host/Origin/proxy/Secure-cookie contract | Implemented and locally exercised under a synthetic proxy request path | Real Caddy/TLS acceptance in P12-04/05 |
| Android production HTTPS source transport | Implemented and focused-tested with a synthetic origin and system trust config | Real hostname/cert/device acceptance in P12-05 |
| Initial database/data/bootstrap/secrets policy | Proposed only; no real secret or account provisioned | Exact P12-02 decision, later guarded execution |

## Progress log

- [x] 2026-09-28: Confirmed expected main HEAD, empty index and the three
  protected file hashes; reviewed Phase 11/10 history and current runtime.
- [x] 2026-09-28: Checked only the configured Proxmox SSH target; it remains a
  placeholder, so stopped that read-only subsection without remote commands.
- [x] 2026-09-28: Production settings, database/Host/Origin/proxy/cookie path,
  Android build/transport and current-grant proof implemented. Focused unit,
  HTTP and config checks passed using only synthetic/disposable local values.
- [x] 2026-09-28: Sanitized isolated P12-01 r1 review package published on
  `astra-response` without staging or committing main at that review boundary.
- [x] 2026-09-28: ChatGPT accepted published r1 source, tests, disposable proof
  and this plan. P12-01 closeout is limited to a local implementation checkpoint
  and isolated r2 review package; no tests, builds or discovery are repeated.

## Outcome

P12-01 is ACCEPTED / CLOSED as a local source checkpoint. Phase 12 is IN
PROGRESS; P12-02 is NEXT / NOT STARTED. No infrastructure deployment occurred.
The configured Proxmox target remains a placeholder. The exact hostname,
Proxmox placement, bridge/VLAN, storage pool, off-host backup, data/bootstrap
policy and actual secrets remain unresolved. Real Caddy/TLS/private-DNS
behavior, normal-certificate browser/PWA/Android acceptance and off-host
restore remain later gates. Production Android has source/config/build evidence
only, not an APK or physical-device acceptance; Phase 9 localhost TEST transport
is not production evidence. PostgreSQL must never be public. This plan is not
approval for P12-02 or infrastructure mutation.
