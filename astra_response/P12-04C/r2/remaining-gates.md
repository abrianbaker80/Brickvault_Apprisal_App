# Remaining gates

P12-04 remains IN PROGRESS. P12-04C is ready for review, not accepted/closed by this publication. P12-04D and P12-05 have not started.

Still open:

- Complete-run destructive retention implementation/review; no forget/prune ran.
- Production API secrets/configuration and startup.
- Private DNS, trusted certificate, Caddy and HTTPS exposure.
- Firewall/client-source policy.
- Monitoring and alerts.
- Deliberate VM production onboot behavior.
- P12-05 real restore, browser/PWA/Android and rollback acceptance.

The separate rotation review for the unrelated protected backup identity noted in r1 remains open. P12-04C did not modify that unrelated backup system.

The completed P12-04C gates are offline custody, source receipt/proof integration, packaged runner installation, production DB/roles/descriptor, both real backup/readback runs, protected proof, migration, runtime grants, one owner and admin verification, and reviewed timer activation. No production application traffic was enabled.
