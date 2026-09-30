# VM 115 startup and reboot

Proxmox discovery confirmed firewall VM 112 (opensense) onboot=1 with
startup order=1,up=15 and the existing application VM 107 at order=2.
After unattended readiness passed, only VM 115 was changed to onboot=1,
startup order=2. Configuration readback passed. Proxmox was never rebooted.

Before the single reboot: recent production backup, alerts, light/deep health,
maintenance state, retention READY and no failed units passed. Backup,
retention, certificate and apt jobs were idle; schedulers were drained without
interrupting jobs. A protected once-only intent and boot ID were recorded.

After reboot: boot ID changed, VM returned, the same reserved IP and interface
MAC were observed through guest-agent readback, and key-only pinned SSH worked.
Data mount, PostgreSQL, API, Caddy, trusted HTTPS health/app 200, UFW, clock,
all eight backup/cert/operations/apt timers, guest agent and listener checks passed.
Light/deep health and official Python check passed again; failed units=0.
This is one guest reboot test, not a Proxmox host boot or disaster-recovery test.
