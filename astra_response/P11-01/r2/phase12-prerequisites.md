# Unresolved Phase 12 prerequisites

Phase 12 is **NEXT / NOT STARTED**. This list records work requiring a
reviewed plan and separate explicit authorization; it authorizes no action.

1. Obtain authorized Proxmox node facts: identity/version, actual spare CPU
   and RAM, VM/LXC inventory, storage pools/free space, relevant bridge/VLAN,
   and backup policy. The inspected Ubuntu 24.04 KVM guest's 64 assigned
   vCPUs and 125 GiB RAM cannot establish host capacity.
2. Confirm ownership and intended use of the separate unmounted guest disk.
   Treat it as unavailable until then. The dedicated Ubuntu VM and initial
   4-vCPU/8-GiB/32-GiB-OS/128-GiB-data design remain conditional proposals.
3. Identify whether a proxy exists elsewhere; none was active on the
   inspected guest. Approve the exact private network attachment, hostname,
   internal DNS and HTTPS/certificate path. Do not infer router, firewall,
   public DNS or Cloudflare configuration from the guest observation.
4. Confirm an off-host backup target, capacity, retention, encryption and
   restore procedure for PostgreSQL plus required roles/configuration. The
   guest's `pg_dump` binary and unknown Proxmox policy do not prove recovery.
5. Implement and review a production application runtime. Current source
   permits only development/TEST database targets and loopback Host/Origin;
   production database, exact host/origin, trusted proxy and Secure-cookie
   behavior need explicit, tested design before any non-loopback exposure.
6. Implement and review production Android HTTPS transport to the approved
   name with normal certificate validation. Phase 9 localhost TEST
   certificate/transport mechanics are not deployment evidence.
7. Review the exact initial database/data policy, owner bootstrap, service
   and secrets configuration, release/rollback steps and private validation.
   PostgreSQL must remain reachable only within the approved workload
   boundary and must never be publicly exposed.
8. Obtain Brian's separate explicit Phase 12 authorization before VM/disk
   creation, installs, service starts/restarts, migrations, data copy,
   network/firewall/DNS/Cloudflare/certificate changes, credential placement,
   backups, monitoring, cutover or production/device checks.
