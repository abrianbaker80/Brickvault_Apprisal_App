# P12-01 r1 — production runtime and deployment preflight

**Requested verdict:** READY FOR P12-01 REVIEW. This package describes the
uncommitted working-tree change against main
`5a0b94a190ab3aabc52f5ea17afdf5e96cf6cc51` (`Close Phase 11 home
infrastructure discovery`). Main remains at that commit with an empty index.
No application or documentation commit is requested yet. Phase 10 and Phase 11
are closed; Phase 12 is in progress at this bounded slice only.

## Review material

- [Complete task patch](changes.patch): 27 changed files against the stated
  baseline, excluding three protected pre-existing dirty files.
- [Final ExecPlan 091](docs/plans/091-production-runtime-and-deployment.md):
  accepted Phase 11 facts, implemented source contract, conditional topology,
  exact later slice gates, rollback, backup/restore, DNS/HTTPS, Android,
  secrets/bootstrap and unresolved prerequisites.
- [Final changed source and focused tests](source/): exact file contents under
  their repository paths. The deleted old Capacitor JSON is represented in the
  complete patch; its TypeScript replacement is in `source/`.
- [Validation](validation.txt), [deployment preflight](deployment-preflight.md)
  and [sanitized local command record](commands.txt).

Links inside the copied ExecPlan use their original repository-relative paths;
the accepted Phase 10/11 plans remain in the main checkout and are not
duplicated here.

## Implemented boundary

Production is an explicit runtime purpose. It requires a specified loopback
listener, HTTPS application origin, dedicated loopback PostgreSQL database and
runtime role, distinct owner/migration role, ownership marker, protected proxy
identity, static build directory and Secure host-only SameSite=Strict cookies.
Production Host and state-changing Origin are exact; CSRF and private no-store
remain. The approved Caddy-to-loopback path overwrites an internal identity
header, while Uvicorn ignores arbitrary forwarded headers. The current
migration graph grants the runtime role only enumerated application access; no
schema migration or API contract change was made.

Production Android packages the same React UI at the derived same-site WebView
origin and calls the exact configured HTTPS API origin with cookies and CSRF.
The source uses system certificate trust, no production TEST CA, no localhost
TEST API, no `server.url`, no cleartext, no adb reverse and no native bearer
replacement. Browser/PWA same-origin and Phase 9 TEST behavior remain intact.
The build used only the synthetic `https://app.example.test` origin. No APK or
physical Android test was performed.

## Evidence and limits

Focused tests, local production-mode HTTP/database proof, targeted checks and
one Android web/config build passed; see [validation](validation.txt). The
proof used a run-owned disposable database and roles on the existing owned
local TEST PostgreSQL service, migrated the current graph, denied runtime DDL
and cleaned all recorded resources. It did not contact providers or a real
production database.

The configured Proxmox SSH target is still a placeholder. Only local SSH
configuration expansion was performed; no remote command or infrastructure
mutation occurred. No new Proxmox capacity/storage/inventory/network/firewall,
backup, proxy-elsewhere or private DNS fact was established. The accepted
Phase 11 guest allocations are not host spare capacity. The guest's unowned
disk remains excluded. No VM, DNS, certificate, firewall, service, real
database, backup, or legacy guest was changed.

## Review decision requested

Review the production Host/Origin/proxy/cookie/database and Android transport
contract, the local evidence, and the unresolved prerequisites. P12-02 may
prepare an exact pre-mutation proposal only after separate authorization;
P12-03 through P12-05 and every infrastructure/production mutation remain
unauthorized by this package. PostgreSQL must never be publicly reachable.
