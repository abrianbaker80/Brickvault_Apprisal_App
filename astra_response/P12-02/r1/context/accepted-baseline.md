# Minimal accepted baseline

P12-01 is accepted/closed at main HEAD
`c91f0bb2f76497dcf69a5f9887c885871871ddb9`. Its local production
runtime and Android HTTPS source proof is preserved in
[ExecPlan 091](../source/docs/plans/091-production-runtime-and-deployment.md).
It was not retested in P12-02.

The accepted source requires exact HTTPS Host/Origin, an overwritten protected
`X-BrickVault-Proxy` header, Secure/HttpOnly/SameSite=Strict cookies, CSRF,
FastAPI loopback with `proxy_headers=False`, and dedicated PostgreSQL
owner/runtime roles with a verified ownership marker. Android derives its
same-site production Origin and uses normal platform certificate trust. The
current packaged migration head is `0016_hunt_cached_runs`.

The existing database migration and owner-bootstrap helpers are restricted to
development/disposable TEST. The future production command described in
ExecPlan 092 must be implemented and reviewed before production data changes.
