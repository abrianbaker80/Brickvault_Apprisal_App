# Runtime and Ubuntu maintenance

The verified guest timezone is Etc/UTC. Enabled/active schedules:

| Timer | Cadence |
| --- | --- |
| brickvault-health | 10 minutes after boot and each invocation, up to 30 seconds jitter |
| brickvault-health-deep | Daily 08:15 UTC, up to 15 minutes jitter |
| brickvault-retention | Sunday 09:15 UTC, up to 15 minutes jitter |
| brickvault-python-version | Sunday 10:15 UTC, up to 15 minutes jitter |

Accepted backup and Certbot schedules remain enabled/active. Deep work follows
the established backup window. Calendar operations timers persist missed runs.

Python detection uses only https://www.python.org/downloads/source/ with normal
TLS, same-official-host redirects, bounded compressed and expanded HTTP response
sizes, identity/gzip decoding and final 3.13.x release links. Three bounded lookup
attempts precede failure. Newer patches or repeated lookup failure alert; nothing
is downloaded/installed automatically. Live installed=latest=3.13.15, CURRENT.
The official index and https://www.python.org/downloads/release/python-31315/
are the source authority; no third-party version service is consulted.

Future separately reviewed Python update procedure:

1. Fetch the official Python.org signed source release.
2. Verify its published SHA-256.
3. Verify the release-manager signature with the independently established key.
4. Install into a new versioned /opt/python/<version>, leaving /usr/bin/python3 alone.
5. Create a new immutable release venv from that interpreter and locked dependencies.
6. Run targeted application, installed-wheel, static-build and operational checks.
7. Atomically activate the reviewed release with the absolute immutable web path.
8. Retain the prior interpreter/release for a separately authorized rollback.
9. Remove old versions only after later review.

Ubuntu's existing unattended-upgrades is installed; apt-daily and
apt-daily-upgrade are enabled/active. Periodic package-list refresh and unattended
security upgrades are enabled. Automatic reboot is disabled by policy/default;
no third-party update manager was added. Reboot-required older than 48 hours
fails health and alerts. No reboot-required flag remained after the controlled
reboot. A package request alone does not authorize a reboot.
