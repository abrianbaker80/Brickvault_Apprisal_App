# Accepted P12-04 production state

This document reuses [accepted r1 evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/6f06662b394471aaef2a136c59d7ed4f3becd676/astra_response/P12-04E/r1/REVIEW.md).
Nothing below was re-probed during closeout.

P12-04A runtime/storage/release foundation CLOSED; B dual encrypted recovery
CLOSED; C production database/migration/owner and real recovery points CLOSED;
D private trusted HTTPS CLOSED; E operational hardening CLOSED.
**P12-04 ACCEPTED / CLOSED. Phase 12 IN PROGRESS.**

- Retention: 30 daily / 8 weekly / 12 monthly complete-run selection, one valid
  receipt and all three artifacts in BOTH independently encrypted repositories.
  Permanent synthetic/pre-migration/post-bootstrap pins never age out automatically.
  Deterministic digest-bound plan/apply, full dual readback, explicit snapshot IDs,
  repository checks, durable DEGRADED before mutation and progress after each
  destination; no artifact-level selection or automatic destructive retry. Partial
  cross-repository failure remains DEGRADED. Prune is separate; no prune timer.
  Disposable destructive tests PASS. First live PLAN keep=3/delete=0, APPLY NOOP;
  no production snapshot deletion/prune. Retention timer enabled/active.
- Alerts: private Gmail, dedicated locally entered protected app credential,
  synthetic TEST SMTP acceptance PASS. Normal TLS, bounded timeout, root-only
  configuration/state, generic categories, persistent dedup/backoff, no application
  EnvironmentFile or owner-secret disclosure. Failure integration covers backup,
  retention, API, Caddy, Certbot, light/deep health and Python maintenance.
- Health: light/deep PASS. Exact trusted HTTPS/SAN/expiry, loopback API/DB, services,
  allowed listeners, DB readiness/data mount, backup freshness, retention READY,
  release/manifest/runtime, UFW/clock/guest agent, disk/reboot/update policy. Deep
  checks cover repository identities, receipt completeness and pinned history;
  frequent checks do not run expensive restic check.
- Python: installed 3.13.15; official current 3.13.x was 3.13.15 at accepted evidence
  time, CURRENT. Official python.org only, normal TLS, bounded response/decompression
  and retries; alerts on update/failure. No automatic replacement. Preserve signed
  source/hash/signature verification, new versioned interpreter/release/venv,
  targeted qualification, atomic activation and prior runtime retention. Never
  replace /usr/bin/python3.
- Ubuntu: unattended-upgrades and apt timers active, standard security updates
  enabled; automatic reboot disabled. Reboot-required older than 48 hours alerts.
- ACME: contact email intentionally absent. Certbot failure, renewal timer,
  deploy-hook failure and served-certificate expiry monitoring provide coverage.
- VM 115: onboot=1, startup order=2 after the proven firewall order=1 and reviewed
  delay. Only VM 115 startup changed. One guest reboot PASS: reserved address,
  data mount, PostgreSQL/API/Caddy/trusted HTTPS/UFW, backup/Certbot/health/Python/
  retention/apt timers, key-only SSH, guest agent, expected listeners, zero failed
  units. No Proxmox host reboot; host boot/disaster proof remains open.

Accepted immutable release: p12-04e-r6. Prior releases preserved.
Source ID: 00c719ac356f881c9929909a22f683831235f222939d28c8892747c8898558f5.
Manifest SHA-256: 9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d.
Accepted repairs: absolute immutable web path, Linux ss interface suffix,
official HTTP gzip handling and bounded 16 MiB retention-state reader. No
accepted security guard was weakened; closeout changes no executable bytes.

Guest-local alerts cannot report loss of VM 115 or the entire Proxmox host.
The guest reboot does not prove Proxmox host-boot recovery. Both limitations
carry into [P12-05 disaster/recovery acceptance](p12-05-gates.md); no new host
monitor or destructive host-boot test is introduced by closeout.
