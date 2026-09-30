# P12-04E - production operational hardening

**READY FOR P12-04E REVIEW. P12-04E IMPLEMENTED / READY FOR REVIEW.
P12-04 IN PROGRESS. P12-05 NOT STARTED.**

Production operations are active on immutable p12-04e-r6. Complete-run retention
permanently pins accepted recovery points; its first live plan kept all three
production runs and apply returned NOOP. No live history was deleted or pruned.
Gmail accepted the one synthetic TEST. Light/deep health and official Python
maintenance checks pass. VM 115 now autostarts at the proven application order,
and the single controlled guest reboot recovered all required services and timers,
the reserved address and normally trusted private HTTPS. Failed units: zero.

## Identity and preservation

- Main HEAD: `389a30e0ba4cdf6902d48e06277cc6ef1bc2fc6c`; implementation uncommitted,
  no main push, index empty, three protected dirty files unchanged/unstaged.
- Final release: `p12-04e-r6`; accepted D and earlier E releases preserved.
- Source ID: `00c719ac356f881c9929909a22f683831235f222939d28c8892747c8898558f5`.
- Manifest SHA-256: `9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d`.
- Runtime: versioned CPython 3.13.15; official latest 3.13.15; uv 0.12.10.
- Schema 3 includes operations/deployment bytes and retains schema 1/2 verification.

## Review focus

Retention treats all six artifacts plus the protected receipt as one policy item;
30 daily / 8 weekly / 12 monthly selection is deterministic and digest-bound.
Full readback precedes explicit-ID forget. Cross-repository failures durably
mark DEGRADED before mutation and prevent automatic retry/prune. Real destructive
proof used only disposable local restic repositories. A separate prune interface
has no timer and was not used live.

Generic Gmail alerts use root-only configuration, normal TLS, bounded timeouts
and durable dedup/backoff. Service failures, stale backups, certificate expiry,
reboot-required age and runtime updates are monitored without owner credentials.
Ubuntu's standard security automation remains active; no automatic reboot or
Python replacement is enabled. ACME remains without contact email; independent
renewal/deploy/expiry operational alerts provide notification.

Activation initially hit the existing static loader's symlink refusal. Work
stopped; Brian explicitly approved the absolute immutable path repair and resume.
The outage is resolved. Linux ss suffix and official gzip response regressions
were corrected; final review also corrected the size bound for retention evidence.
The final release and post-reboot checks pass without weakening accepted guards.

## Evidence

- [Plan 098](Plan-098.md)
- [Retention design and failure recovery](retention-design.md)
- [Alerting and ACME decision](alerting.md)
- [Health checks](health-monitoring.md)
- [Python / Ubuntu maintenance and update runbook](runtime-maintenance.md)
- [VM autostart and controlled reboot](vm-autostart.md)
- [Actual focused validation](validation.txt) and [sanitized commands](commands.txt)
- [Release manifest](release-manifest.json), [source input hashes](source-input-sha256.json)
- [28 changed files](changed-files.txt), [exact byte hashes](changed-file-sha256.json),
  [source copies](files/) and [cumulative patch](cumulative%20changes.patch)
- [Minimal accepted D context](context/accepted-p12-04d.md)

The exact files tree preserves repository-relative paths and original bytes;
its relative documentation links target the complete repository after applying
the patch. Plan-098.md has its baseline link redirected to the included context.
A package-local .gitattributes disables newline conversion for exact-copy fidelity.
One unchanged database helper is included under context/source-inputs solely to
reproduce its existing mixed Windows newline bytes in the source fingerprint.
No private addresses, email, credentials or live backup identifiers are published.

## Remaining gates

Independent review is pending. P12-05 remains NOT STARTED: owner login/session/
cookies and auth/CSRF/Host/Origin acceptance; full private browser acceptance;
PWA install/offline/reconnect; physical Android production TLS; real off-host
production restore; release rollback rehearsal; end-to-end disaster recovery.
This guest reboot does not establish Proxmox host-boot or disaster-recovery proof.
