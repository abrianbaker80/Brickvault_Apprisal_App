# Production health

Light and deep installed systemd checks PASS before and after the single guest
reboot. Windows normal-trust private HTTPS health also returned 200 after reboot.

Light health checks credential-free exact-host trusted HTTPS, exact certificate
SAN and >21-day validity, services/timers, loopback API/DB and approved listeners,
pg readiness/data mount UUID, recent complete receipt (<36 hours), retention READY,
release/manifest/runtime/hook bytes, UFW, clock, guest agent, free space (>=10%,
root >=2 GiB and data >=5 GiB), reboot-required age (<48 hours), and apt policy.
The Linux ss interface suffix is normalized before checking the explicit allowed
endpoints; unexpected loopback and non-loopback ports still fail.
Daily deep health additionally reads both repository identities and validates
complete snapshot/receipt/pin history. Frequent checks do not run restic check.
All probes are owner-credential-free. Healthy health runs are quiet; failures
emit sanitized categories, exit nonzero and invoke external alerts. A stopped
VM cannot send its own alerts; independent whole-host availability monitoring
is not claimed by this guest-local implementation.


Light cadence: every ten minutes with up to 30 seconds jitter. Deep cadence:
daily 08:15 UTC with up to 15 minutes jitter. Health records are protected under
/var/lib/brickvault-operations. Units remain enabled/active; zero failed units.

Linux ss reported the DNS stub with an interface suffix, 127.0.0.53%lo. A
regression reproduced the original false failure and passed after normalization;
unexpected local or external listeners remain rejected. API and DB stay at
127.0.0.1:18080 and 127.0.0.1:5432; Caddy exposes only TCP 443.
