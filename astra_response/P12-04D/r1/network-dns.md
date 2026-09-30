# Private addressing and DNS

Authenticated OPNsense 26.1.10 inspection established Kea DHCPv4 as the LAN DHCP
authority and Unbound as the normal port-53 resolver. Windows and VM 115 use that
gateway/resolver. Proxmox guest-agent NIC identity matched the actual VM lease.
Dnsmasq uses port 53053 and has no DHCP ranges.

One reservation retains the existing VM address. Only that address was removed
from dynamic allocation; every other pool address and the four prior reservations
were preserved. Renewing the lease retained address, route and resolver. Kea now
reports assigned static. No static Ubuntu address, new NIC, bridge or VLAN change.

One Unbound A override maps appraisal.abrianbaker.com to the reserved private
address, TTL 300, no PTR/aliases. Windows normal-resolver and VM checks passed.
The Android synthetic origin received no DNS record.

Both Cloudflare authoritative nameservers returned no application A/AAAA, and no
remaining ACME TXT record after issuance/renewal. OPNsense destination NAT and
one-to-one NAT tables had no configured forwarding entries. No WAN rule was added.
Exact private addresses and NIC identifiers are intentionally excluded.
