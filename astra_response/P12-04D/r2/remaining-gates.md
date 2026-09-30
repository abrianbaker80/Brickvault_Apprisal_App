# Remaining gates

P12-04D ACCEPTED / CLOSED. P12-04 IN PROGRESS.
Next P12-04 operational-hardening checkpoint NEXT / NOT STARTED.
P12-05 NOT STARTED. No next checkpoint was begun.

Remaining P12-04 gates stay OPEN:

- Complete-run destructive backup retention implementation/review.
- External operational alerting.
- Deliberate production VM onboot behavior.
- CPython 3.13 security-release/update maintenance.
- ACME contact/renewal operational notification decision. The account currently
  has no contact email; this is an operational note, not a P12-04D defect.
- Remaining production service health/maintenance automation.

Keep for P12-05:

- Owner login/session/cookie issuance; no new Set-Cookie evidence exists.
- Full browser acceptance.
- Full PWA install/offline/reconnect acceptance.
- Physical Android production-TLS acceptance; accepted CORS checks are transport only.
- Real production restore rehearsal.
- Release rollback rehearsal.
- End-to-end disaster-recovery acceptance.

The legacy protected backup identity is separate from this application's recovery
authority, was not changed, and is not a BrickVault deployment blocker.
