# P12-04D — private HTTPS application activation

**READY FOR P12-04D REVIEW. P12-04 IN PROGRESS. P12-05 NOT STARTED.**

BrickVault Appraisal App is active privately at https://appraisal.abrianbaker.com.
The VM retains its address through one Kea reservation and one Unbound host
override. A normally trusted Let's Encrypt certificate was issued through
Cloudflare DNS-01. Caddy exposes TCP 443 to the approved LAN, with the API and
PostgreSQL on loopback. No public application A/AAAA or WAN forwarding was added.

## Deployment identity

- Source checkout: main at `0d29d5f7f07f379ade834ee22cfaf4e7da9587c4`; uncommitted, unpushed, index empty.
- New immutable release: `p12-04d-r1`; accepted r4 preserved.
- Source ID: `b704133a4754365ac96cb282902bcd14aa9a6a75bd572cb0df38816b968ce6bc`.
- Manifest SHA-256: `25cbb51ec895640f2ed27ab36afac8ebcd11590aa52f96015b15e460502b6f36`.
- API wheel SHA-256: `02dc2675632ffc72ffd11a797aab11b52fee5820b5966bc582864baf9ce8fc97` (unchanged).

## Review focus

The exact-host Caddy configuration overwrites the proxy identity header and uses
a protected Unix admin socket. The service override removes stock environment
printing; no secret or adapted secret-bearing config is logged/persisted. The
certificate hook verifies trust, hostname and key pairing, installs a protected
pair atomically, validates/reloads Caddy and restores the previous pointer on
failure. Manifest schema 2 binds deployment bytes while retaining schema-1 support.

Seven manifest tests and five Linux deployment tests passed, together with
targeted Ruff/format/strict mypy. Live startup, DB readiness, normal Windows TLS,
Host/Origin/proxy/no-store boundaries, synthetic Android credentialed CORS,
private firewall, renewal dry run/deploy hook and public-DNS negatives passed.
API/Caddy and both timers are enabled/active. VM onboot remains 0.

## Evidence and exact changes

- [Plan 097](Plan-097.md)
- [Private network/DNS](network-dns.md)
- [Certificate, tooling and renewal](certificate-tls.md)
- [Application activation and transport](application-activation.md)
- [Firewall](firewall.md)
- [Sanitized commands](commands.txt) and [validation](validation.txt)
- [Release manifest](release-manifest.json)
- [Ten changed files](changed-files.txt), [exact copies](files/) and [cumulative patch](cumulative%20changes.patch)
- [Minimal accepted P12-04C context](context/accepted-p12-04c.md)

The three pre-existing protected files are unchanged, unstaged and excluded.
No credentials, private addresses/MACs, private keys, owner data or recovery-media
identifiers are included. The unrelated legacy backup age identity is outside
this deployment and was not changed.

## Explicit remaining gates

Independent acceptance review is pending. No owner login/cookie issuance, full
browser/PWA acceptance, physical Android, APK work, real restore or release rollback
rehearsal occurred. Cookie flags remain source-qualified only. Retention/pruning,
external alerting, onboot and CPython maintenance remain the next P12-04 checkpoint.
ACME has no contact email; renewal timer is active, while alerting remains deferred.
This package does not close P12-04 or start P12-05.
