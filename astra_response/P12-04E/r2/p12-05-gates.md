# P12-05 - NEXT / NOT STARTED

P12-04E independent ChatGPT review is complete: Brian accepted the
[published r1 package](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/6f06662b394471aaef2a136c59d7ed4f3becd676/astra_response/P12-04E/r1/REVIEW.md). All gates below remain
open for P12-05, NEXT / NOT STARTED. This closeout does not authorize them.

- Auth/session: real owner login and session creation; cookie issuance with
  Secure, HttpOnly and SameSite=Strict; CSRF, Host and Origin enforcement;
  logout/session invalidation.
- Browser: full private browser workflow acceptance.
- PWA: installability at the normally trusted production origin; offline saved
  views, reconnect/session and update behavior; no durable private-response leakage.
- Android: production APK/build identity as required; physical Android device;
  normal public-CA TLS, production API hostname and Android production Origin/CORS;
  authenticated session, saved work and offline/reconnect behavior. No TEST CA,
  localhost or adb reverse may substitute for production evidence.
- Recovery: REAL production restore rehearsal from off-host Google Drive;
  restored database ownership/marker/revision/account verification and recovery
  from protected configuration material.
- Rollback: immutable application release rollback, forward return to the current
  release, database compatibility and no-data-loss verification.
- Disaster/boot: end-to-end disaster recovery including host/VM startup reasoning.
  The accepted guest reboot is NOT Proxmox host-reboot evidence. Verify autostart
  dependency/order as appropriate without inventing a destructive test.
- Monitoring limitation: guest-local alerts cannot report complete loss of VM 115
  or the entire Proxmox host. Carry this into disaster-recovery acceptance; do not
  add host-level monitoring during this closeout.
- Final Phase 12: security/listener/DNS/TLS checks, backup/restore and rollback
  acceptance, operational state and independent review before Phase 12 closeout.
