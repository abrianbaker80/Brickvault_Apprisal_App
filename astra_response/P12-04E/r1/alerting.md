# Private Gmail operational alerts

Brian explicitly selected Gmail and entered a dedicated app password through
hidden local input. The single TEST received successful SMTP DATA acceptance.
TEST, API, HEALTH and PYTHON protected status records are ACCEPTED. Final
configuration and recipient remain private; no credentials enter this package.

The sender uses normal certificate validation on smtp.gmail.com:465 and bounded
20-second socket operations. Fixed messages contain only operational categories.
Root:root 0700 directories and 0600 configuration/state, symlink refusal,
duplicate-JSON-key refusal, exclusive state writes, fsync, persistent deduplication
(six hours after acceptance) and failed-attempt backoff (ten minutes) are enforced.
Ambiguous delivery does not prove receipt; PENDING records suppress rapid retry.
TEST is once-only. No app EnvironmentFile is loaded by alert units.

OnFailure covers backup, retention, API, Caddy, Certbot, light/deep health and
Python checks. Inactive Certbot timer/expiry trigger health; the deploy wrapper
also alerts directly while preserving failure. Actual failures during this slice
exercised the service path and were resolved. SMTP acceptance is transport proof,
not proof that the recipient opened the email. A guest-local monitor cannot
report a complete loss of the guest or its entire outbound network.

No ACME-contact permission was given. The account remains without contact email;
renewal/timer/deploy/expiry monitoring is provided through these external alerts.

[Exact sender](files/scripts/operational_alert.py),
[offline tests](files/scripts/test_operational_alert.py), [Plan](Plan-098.md).
