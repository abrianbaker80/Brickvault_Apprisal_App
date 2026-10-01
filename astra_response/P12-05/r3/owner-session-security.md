# Owner session and security evidence

Reuse accepted [P12-05 r2 evidence](../r2/owner-session-security.md) for Gates 1/2:
normal owner login/cookie restrictions, trusted origin, no-store, CSRF/Origin/Host
positive and negative checks, proxy-header handling and direct API inaccessibility.
These checks were not unnecessarily repeated. All passwords were entered locally.

New PWA and Android owner sessions authenticated through the ordinary production
application. After failure cleanup Android displayed Signed out; reloaded PWA
displayed sign-in. Read-only server metadata confirms zero valid owner sessions,
with one revoked and one expired. No cookie/token/session-hash values were exported.
The accepted earlier Windows old-token replay returned 401; replay of the new
continuation tokens was not exercised. Final Gate 10 replay qualification remains
pending and is not inferred from an unauthenticated request or session metadata.
