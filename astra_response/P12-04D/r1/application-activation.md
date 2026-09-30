# Private application activation

Release: p12-04d-r1. Source ID: b704133a4754365ac96cb282902bcd14aa9a6a75bd572cb0df38816b968ce6bc.
Manifest SHA-256: 25cbb51ec895640f2ed27ab36afac8ebcd11590aa52f96015b15e460502b6f36. See [manifest](release-manifest.json).
Accepted p12-04c-r4 is preserved. The API wheel, dependency lock and frontend bytes
are unchanged; deployment definitions are included in manifest schema 2. Schema 1
verification remains supported. CPython 3.13.15, uv 0.12.10, hashed dependency
installation/check, installed entrypoints and migration head 0016_hunt_cached_runs
passed. Installed deployment files match the immutable manifest.

api.env is root:brickvault 0640. Runtime DB URL and ownership marker were derived
locally from the protected descriptor. A new random 64-lowercase-hex proxy secret
is shared with root:caddy 0640 /etc/caddy/brickvault.env. Neither value was printed.
Configuration/admin verification and runtime database readiness passed. API is
enabled/active only at 127.0.0.1:18080; PostgreSQL remains at 127.0.0.1:5432.

Caddy is enabled/active on TCP 443 only, preserves Host, replaces client proxy
headers, and removes forwarding headers. TLS SNI and HTTP Host must match. Its
admin API is a protected Unix socket, not TCP. The drop-in removes the stock
--environ flag; adapted config persistence and request/header logging are disabled.
Secret-value scans of API/Caddy/Certbot journals and issuance logs passed.

Windows used normal DNS and .NET platform TLS validation, with no certificate
bypass, hosts-file override, custom CA or proxy. Health and the app shell passed;
private/session/readiness routes return 401; unknown API is JSON 404. Private
responses carry no-store. Forged and duplicate client proxy headers are replaced.
Wrong Host with correct TLS SNI gives 421; direct-IP TLS is refused. Missing/wrong
mutation Origin gives 403; exact browser Origin reaches normal request validation.

Synthetic Android Origin https://android.appraisal.abrianbaker.com passes exact
credentialed preflight and receives the exact CORS headers on an unauthenticated
401. No wildcard CORS; the old TEST origin is rejected. This is HTTP transport
smoke only, not Android/browser/PWA acceptance. No owner login, session creation,
cookie issuance, APK installation or physical device test was performed. Secure,
HttpOnly and SameSite=Strict flags remain in unchanged accepted auth source; these
flags were not newly exercised by a login.

The legacy backup age identity is outside this application's recovery authority:
no deployment/recovery reference or matching restic/SSH material, and distinct
OAuth clients. No unrelated identity was rotated or modified. Backup timer remains
enabled/active and VM onboot remains 0. No migration/bootstrap/manual backup rerun.
