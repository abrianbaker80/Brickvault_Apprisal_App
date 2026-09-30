# VM cold stop/start

NOT RUN after Gate 5 blocker. No Proxmox/VM mutation, shutdown, start or reboot
occurred. The remaining gate still requires startup order firewall VM 112 before
VM 115, graceful stop/start only VM 115, stopped-state proof and complete guest
service/network/mount/timer recovery. Historical ordering is not a fresh check.
