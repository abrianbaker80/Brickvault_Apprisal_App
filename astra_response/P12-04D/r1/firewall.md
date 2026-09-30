# Private guest firewall

UFW 0.36.2-6 was already installed and inactive with no user rules. Configured deny
incoming, allow outgoing, and exactly two TCP allow rules: port 22 from the proven
private admin /24; port 443 from the proven private client /24. Both roles use the
same verified LAN. No IPv6 inbound allow rule. Exact private ranges are omitted.

A retained SSH session stayed open through rule review and enablement. A fresh
strict-host-key SSH connection succeeded immediately afterward; no rollback was
needed. Windows can reach 22/443 and cannot reach 80/18080/5432. API/DB bind only
to loopback. Caddy has no TCP 80/2019 or UDP 443 listener. No Proxmox firewall
dependency, WAN rule, broad LAN scan or unapproved source allowance was introduced.

Evidence establishes the installed host policy and approved-client behavior.
No separate untrusted-network/WAN-origin penetration test is claimed.
