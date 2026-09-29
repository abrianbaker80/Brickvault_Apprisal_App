# P12-01 sanitized deployment preflight

## Read-only access result

The configured Proxmox SSH alias still resolves to a placeholder. The local
configuration check stopped there. No remote SSH session or home-host query
was attempted, and no network scan was used. Therefore P12-01 resolved **no
new infrastructure facts**. Private DNS, an off-host backup target and any
reverse proxy elsewhere in the known environment remain unverified.

## Accepted Phase 11 facts retained

The inspected target was an existing Ubuntu 24.04 KVM guest with a legacy
BrickVault backend and loopback PostgreSQL 16. Its 64 assigned vCPUs and
125 GiB RAM describe that guest only; they do not establish spare Proxmox
capacity. Its separate unmounted 200 GB virtual disk has unconfirmed
ownership and is excluded from the plan. No active reverse proxy was observed
on that guest; one elsewhere was not ruled out. Off-host backup and retention
remain unverified. A dedicated Ubuntu VM with 4 vCPU, 8 GiB RAM, 32 GiB OS
and 128 GiB data remains a conditional proposal. PostgreSQL is never public.

## Proposed path subject to P12-02 review

One approved private HTTPS hostname reaches Caddy, which proxies to FastAPI
bound to loopback. Caddy retains exact Host and overwrites a protected internal
identity header. The app trusts no general forwarded headers. A dedicated
database has distinct owner/migration and runtime roles with local-only
PostgreSQL access. Browser/PWA use that HTTPS origin; Android's bundled same
React UI calls it with normal platform TLS validation, cookies and CSRF.
No production hostname, certificate challenge, VM placement, DNS or backup
target has been selected or provisioned.

## Unresolved prerequisites

1. Authenticated Proxmox node/version, CPU/RAM totals and usage, VM/LXC
   inventory, storage types/free space, bridge/VLAN/firewall, backup jobs,
   storage and retention, and any off-host target.
2. Exact approved private hostname, DNS mechanism, reachable HTTPS route and
   certificate issuance/renewal path, including Android network reachability.
3. Off-host backup target, retention, restore procedure and recovery material.
4. Exact production VM, database name, role creation, data/bootstrap inputs,
   admin-protected secret placement and rollback plan. Source/local runtime
   behavior is proven; no real resource exists yet.
5. Actual Caddy/TLS/Host/Origin/Secure-cookie verification after a separately
   approved deployment, plus normal-certificate browser/PWA/Android and
   off-host restore acceptance. Phase 9 localhost TEST transport is not this
   evidence.

P12-02 is an exact pre-mutation plan for review. Subsequent VM, service,
database, DNS/certificate and backup operations require distinct approval.
