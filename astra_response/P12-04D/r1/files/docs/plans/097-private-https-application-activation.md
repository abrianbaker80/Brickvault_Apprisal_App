# ExecPlan 097 — P12-04D private HTTPS application activation

## Goal and user-visible outcome

Activate BrickVault Appraisal App on VM 115 at `https://appraisal.abrianbaker.com`
for the approved home LAN, using normal public-CA trust and private DNS. P12-04D
is authorized within P12-04. P12-04 remains IN PROGRESS; P12-05 is NOT STARTED.

## Why this work is being done now

[Plan 096](096-production-database-activation.md) is accepted/closed. Its immutable
`p12-04c-r4` release, production database, single owner and dual backup foundation
are the accepted baseline. This slice activates the private application transport.

## In scope

One stable DHCP reservation, one private DNS host override, signed official Caddy
and supported DNS-01 tooling, protected Cloudflare and proxy secrets, normal TLS
issuance/renewal, immutable deployment definitions, loopback API startup, guest
firewall, and bounded Windows/Android-Origin HTTP smoke checks.

## Explicit non-goals

No public application A/AAAA, WAN forwarding, HTTP-01, port 80 redirect listener,
self-signed application trust, provider credentials, APK/device/PWA acceptance,
restore/rollback rehearsal, backup deletion, retention, alert destination,
VM onboot change, unrelated backup rotation, main commit/push, or P12-05.

## Current repository state

Entry: `main` at `0d29d5f7f07f379ade834ee22cfaf4e7da9587c4`, empty index.
The pre-existing modified `AGENTS.md`, catalog-search integration test and
catalog-parser unit test match their accepted SHA-256 values and remain protected.
Live release manifest SHA-256 matches
`980b7d9894eeee745bd8c7e8222714790f8ac6a56e7812d1d0c6d9fd29ae96a8`.

## Decisions and assumptions

- Authenticated OPNsense 26.1.10 inspection proves Kea DHCPv4 serves the LAN.
  The VM lease matches the NIC independently reported by Proxmox's guest agent.
  Dnsmasq has no DHCP ranges and uses DNS port 53053. Unbound serves port 53.
  Windows and VM use the same private gateway as DHCP server and DNS resolver.
- The original VM address lay in a dynamic pool. Excluded only that address from
  dynamic allocation, retained every other pool address and existing reservation,
  then created one reservation. Renewal and Kea's assigned-static lease confirm it.
- Unbound initially had no host overrides. Added only the exact application A
  override, TTL 300, without PTR/aliases. No Android synthetic-origin DNS record.
- Stock Caddy consumes externally issued certificate files. Certbot with the
  Cloudflare plugin is the preferred issuer after package/source review.
- Source policy is deny inbound, allow outbound, SSH from the proven private
  admin subnet and HTTPS from the proven private client subnet; no public scope.
- Live private addresses, NIC identifiers and credentials stay out of this plan
  and all public review artifacts.
- TLS files and the proxy environment use `/etc/caddy/brickvault-tls` and
  `/etc/caddy/brickvault.env` so Caddy can read them without broadening access to
  the existing root:brickvault 0750 `/etc/brickvault` parent directory.
- The stock Caddy service used `--environ`. The reviewed drop-in removes it before
  secret installation, confines its admin API to a protected Unix socket, disables
  adapted-config persistence, and filters request/response-header log fields.
- Manifest schema 2 includes the literal deployment file inventory. Verification
  remains compatible with accepted schema-1 bundles; application/wheel/lock/frontend
  bytes are unchanged. This is a deployment identity change, not an API migration.

## Data model and API/interface changes

No migration, account or application API changes. The exact environment contract
is `BVA_MODE`, `BVA_BIND_HOST`, `BVA_API_PORT`, `BVA_RUNTIME_DATABASE_URL`,
`BVA_DATABASE_OWNERSHIP_MARKER`, `BVA_PRODUCTION_ORIGIN`,
`BVA_PROXY_SHARED_SECRET`, `BVA_STATIC_ENABLED`, and `BVA_WEB_BUILD_DIR`.
Production origin is `https://appraisal.abrianbaker.com`; the existing boundary
derives credentialed CORS for `https://android.appraisal.abrianbaker.com`.
Preserve Secure/HttpOnly/SameSite=Strict cookies and required mutation Origin.

## Implementation sequence

1. Verify preservation and the minimum live foundation. Inspect authoritative
   DHCP/DNS configuration read-only through Brian's authenticated OPNsense session.
2. Safely reserve the current VM address and add its one Unbound host override.
   Verify renewal, route/DNS and Windows normal-resolver results.
3. Review official package provenance; install Caddy without starting it and
   supported DNS-01 tooling. Stop for scoped Cloudflare token placement when needed.
4. Add reviewed Caddy/service/certificate helper definitions and focused tests.
   Bind changed deployment inputs into a fresh immutable release; never edit r4.
5. Issue the exact-host certificate through DNS-01; verify chain, key pairing,
   cleaned challenge, protected installation and automatic renewal/dry run.
6. Derive protected runtime configuration locally from the production descriptor;
   generate one fresh proxy secret locally for both API and Caddy. Preflight and
   start the API only on `127.0.0.1:18080`; stop on startup failure.
7. Apply reviewed guest firewall with a retained SSH session and rollback on
   failed fresh connection. Validate Caddy before enabling HTTPS on 443 only.
8. Run bounded real-hostname trust, Host/Origin/proxy/no-store and synthetic
   Android-Origin HTTP checks, plus public-exposure negatives and service checks.
9. Update actual evidence and publish sanitized `astra_response/P12-04D/r1/`
   on `astra-response`, leaving main uncommitted with an empty index.

## Validation and acceptance criteria

Use focused deployment/helper and manifest checks only when affected. Verify
exact release/source/lock/frontend/installed identities. Require normal Windows
TLS trust, private DNS, loopback PostgreSQL/API, exact proxy-header overwrite,
rejected wrong Host/Origin, no wildcard CORS, protected secrets, firewall source
restriction, API/Caddy enabled/active and backup timer enabled/active. Preserve
`onboot=0`. Transport smoke is not browser/PWA/physical Android acceptance.

## Security, privacy, and data-integrity considerations

Do not read credentials into chat. Cloudflare token must be zone-scoped DNS Edit,
with Zone Read only if required. Use hidden local installation, not command argv.
API config is root:brickvault 0640; Caddy secret is root:caddy 0640. TLS
directory is root:caddy 0750 and certificate/key files are root:caddy 0640. Never publish private
IPs/MACs, tokens, database marker/password, proxy secret, key, owner hash, recovery
credentials or browser session material. Do not trust client forwarding headers.

## Failure modes, rollback, and recovery

Stop on ambiguous network authority, unsafe reservation, missing login/token,
untrusted certificate, startup failure, SSH lockout risk, unexpected public exposure
or transport-boundary failure. Preserve accepted release and recovery material.
Do not retry migration/bootstrap/backups, weaken trust, or install a workaround.
Rollback only exact task-owned changes from recorded prior state when authorized;
retain failed evidence and keep application exposure disabled on failed gates.

## Progress log

- [x] 2026-09-29: Verified requested main HEAD, empty index and protected hashes.
- [x] VM running, Ubuntu 24.04.5, guest agent, accepted release manifest,
  production-admin verification (including exactly one owner), loopback PostgreSQL,
  inactive/disabled API, absent api.env/Caddy/API listener, and active backup timer.
  Both accepted protected backup receipts remain available. No backup was triggered.
- [x] 2026-09-29: Browser connection repaired through Brian's local extension
  reinstall; authenticated OPNsense DHCP/DNS inspection resumed.
- [x] Excluded only the VM's existing address from Kea's dynamic pools, preserving
  all other addresses and four existing reservations; added the one VM reservation.
  Renewal retained its address, gateway and resolver; Kea reports assigned static.
- [x] Added one Unbound A host override with TTL 300, no PTR or aliases. Windows
  normal-resolver and VM lookups both match the reserved private address. Both
  public authoritative nameservers returned no application A/AAAA. Destination
  NAT and one-to-one NAT have no configured forwarding entries; no WAN rule added.
- [x] Installed stock Caddy 2.11.4 from its signed official Cloudsmith stable
  repository (signing key fingerprint `65760C51EDEA2017CEA2CA15155B6D79CA56EA34`).
  Installed Certbot 2.9.0-1, python3-certbot-dns-cloudflare 2.0.0-1 and
  python3-cloudflare 2.11.1-1ubuntu1 from signed Ubuntu noble repositories.
  Package audit is clean. `caddy.service`, `caddy-api.service` and Certbot units were masked before
  installation and remain inactive; no web/API listener appeared.
- [x] Initially stopped because the Cloudflare credential was absent.
  Prepared an ignored, one-time hidden-input helper on Windows and root-owned
  VM helper; transferred bytes match SHA-256, Python compilation passes, and a
  noninteractive invocation refuses before writing credentials. It requires a
  terminal, refuses overwrites/symlinks, and writes root-only 0600 credentials in
  a root-owned 0700 directory. No token was requested through chat.
- [x] Brian confirmed local token placement. Directory root:root 0700 and file
  root:root 0600 passed. DNS-01 functional access passed using the requested
  Zone/DNS/Edit scope for the single parent zone; no Global API Key or extra
  Zone Read permission was requested. Broader account policy was not enumerated.
- [x] Let's Encrypt YE2 issued the exact-host ECDSA certificate, valid from
  2026-09-30 02:45:59 UTC to 2026-12-29 02:45:58 UTC. Chain, SAN, key pairing,
  validity, normal VM/Windows trust and served-leaf identity passed. Leaf DER
  SHA-256: `33e8fc2d09ee705d536c739aeebe439ebf24eb5ef33d78fc2710c533ecc50fb7`.
  ACME registered without a contact email; external alerting remains deferred.
- [x] Immutable `p12-04d-r1` installed. Source ID:
  `b704133a4754365ac96cb282902bcd14aa9a6a75bd572cb0df38816b968ce6bc`.
  Manifest SHA-256: `25cbb51ec895640f2ed27ab36afac8ebcd11590aa52f96015b15e460502b6f36`.
  Wheel SHA-256 remains `02dc2675632ffc72ffd11a797aab11b52fee5820b5966bc582864baf9ce8fc97`.
  CPython 3.13.15, uv 0.12.10, hashed dependency install/check, entrypoints,
  migration graph and installed deployment-byte comparisons passed. Accepted r4
  is preserved; no migration, account bootstrap or manual backup was repeated.
- [x] Production API configuration derived locally from the protected descriptor,
  with a new random 64-hex proxy secret shared through two protected files.
  Configuration and admin verification passed. API enabled/active on loopback
  18080 only; runtime DB readiness and nine local boundary cases passed.
- [x] UFW enabled with deny incoming/allow outgoing and exactly two source-scoped
  TCP rules: SSH 22 from the proven private admin /24 and HTTPS 443 from the proven
  private client /24 (the same LAN). Retained SSH session stayed open until fresh
  SSH passed. IPv6 has no inbound allow rule. Windows 22/443 reachable; 80/18080/5432
  denied. These are host-rule and approved-client checks, not a separate WAN probe.
- [x] Caddy enabled/active on TCP 443 only, HTTP/1.1 and HTTP/2. No TCP 80,
  UDP 443 or TCP admin listener. Protected Unix admin socket verified.
- [x] Windows normal DNS and normal .NET platform TLS trust passed. Health/app
  shell, private-route 401, unknown-API JSON 404/no-store, overwritten forged and
  duplicate proxy headers, wrong Host with real SNI (421), direct-IP TLS refusal,
  missing/wrong Origin (403), accepted browser Origin and exact native credentialed
  CORS preflight/auth-error behavior passed. No owner login or session was created.
- [x] Certbot renewal dry run with deploy hooks passed; the hook validated the
  production certificate and successfully reloaded Caddy. Certbot timer is
  enabled/active; the next recorded trigger was 2026-09-30 15:42:51 UTC. Both
  authoritative nameservers confirm challenge TXT cleanup and no application A/AAAA.
- [x] API/Caddy/Certbot journal and issuance-log checks found no token, DB password,
  ownership marker, proxy secret or private-key disclosure. Adapted Caddy autosave
  is absent. Backup timer remains enabled/active; Proxmox VM onboot remains 0.
- [x] The separate exposed identity is a legacy application's age identity, with
  no reference in this app's deployment/recovery scripts and no match in its
  restic/SSH access material. The appraisal OAuth client is also distinct. This
  identity is OUTSIDE this deployment, is not a blocker, and was not modified.
- [x] Seven release-manifest tests and five Linux certificate-deployment tests
  passed, including artifact tamper/omission refusal, schema-1 compatibility,
  protected permissions, idempotence and failed validation/reload restoration.
  Targeted Ruff/format and strict Linux-target mypy passed for four Python files.
- [x] Source and live evidence are complete for the sanitized review package at
  `astra_response/P12-04D/r1/` on `astra-response`. Protected hashes and the empty
  main index were rechecked; final publication verification accompanies the review link.

## Open questions or physical-device/manual checks

No outstanding activation blocker. Owner login/session-cookie issuance was not
exercised; the unchanged accepted source still specifies Secure/HttpOnly/SameSite
Strict cookies. The safe requests created no session and emitted no Set-Cookie.
Browser/PWA behavior and physical Android trust remain P12-05 acceptance work.
No real restore or release rollback rehearsal, retention deletion, alerting,
provider-credential setup, onboot change or CPython automation was performed.

## Outcome and follow-up

P12-04D IMPLEMENTED / READY FOR REVIEW. Private HTTPS is active; API, Caddy,
certificate renewal timer and backup timer are enabled/active. The review package
is `astra_response/P12-04D/r1/` on `astra-response`. Main stays uncommitted/unpushed with an empty index and
the three protected files unchanged. Independent acceptance review is pending.
P12-04 remains IN PROGRESS and P12-05 remains NOT STARTED. Retention, alerting,
VM onboot and CPython maintenance remain for the next P12-04 checkpoint.
