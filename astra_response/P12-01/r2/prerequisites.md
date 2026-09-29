# Unresolved prerequisites after P12-01

P12-02 is NEXT / NOT STARTED. It requires separate authorization and exact
pre-mutation review. No deployment or infrastructure mutation has occurred.

1. **Proxmox placement facts:** the configured target remains a placeholder.
   Node/version and actual CPU/RAM capacity/usage, VM/LXC inventory, storage
   pools/free space, bridge/VLAN/firewall and backup jobs/storage/retention
   remain unknown. The inspected Ubuntu guest's allocations do not prove spare
   host capacity. Its separate unmounted disk has unconfirmed ownership and
   must not be adopted.
2. **Exact private hostname and HTTPS path:** select the approved name, private
   DNS mechanism, Caddy route, certificate issuance/renewal and Android reach.
   Real Caddy/TLS/private-DNS behavior is unverified.
3. **Off-host backup and recovery:** select target and retention, protect
   recovery material and plan an actual restore rehearsal. Off-host backup and
   restore remain unverified.
4. **Database, data and bootstrap:** select the dedicated production database,
   owner/migration and runtime roles, initial data policy, principal bootstrap,
   rollback and real secret placement. No production database or real secret
   was created. When provider credentials are activated, verify their canonical
   secret directory and restrictive filesystem permissions.
5. **Live acceptance:** browser/PWA/Android under normal platform certificate
   validation, exact Host/Origin/CSRF/Secure-cookie behavior, private routing,
   monitoring and off-host restore must be checked in later authorized slices.
   The production Android evidence is source/config/build only: no APK or
   physical-device acceptance. Phase 9 localhost TEST transport/certificate is
   not production evidence.

PostgreSQL must never be publicly reachable. The dedicated VM and its sizing
remain conditional on actual host/storage/network/backup facts.
