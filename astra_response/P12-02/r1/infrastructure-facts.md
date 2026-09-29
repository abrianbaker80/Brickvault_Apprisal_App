# P12-02 sanitized infrastructure facts

Observed 2026-09-29 through the existing `proxmox` alias and direct read-only
Proxmox/Linux commands. The one configured-key BatchMode authentication check
succeeded as root on `pve`; there was no alternate credential attempt. This is
a point-in-time inventory, not a resource reservation or deployment result.

| Category | Finding |
| --- | --- |
| Node | Standalone `pve`, PVE 9.1.6, kernel 6.17.13-2-pve; no Corosync configuration. |
| Capacity | 36 physical/72 logical CPUs, 188.8 GiB RAM; about 148.6 GiB memory available and load averages below 1 during observation. Running guests assign about 77 vCPUs and 144.5 GiB maximum RAM. |
| Existing workloads | VMIDs 100–114 and 201–202 present. Running legacy BrickVault VM 107, firewall VM 112 and LXCs 113/114. No reuse of VM 107 or its disks/database. Next VMID reported 115. |
| Storage | `local-zfs` supports VM images, ~381 GiB available; `rpool` online with one observed leaf device. `sas_raid0_lvmthin` supports images, ~6.93 TiB available, but is a RAID0 pool. `local` supports backups/ISO and shares the same host storage. Parent `sas_raid0` has no allocatable space. |
| Media | Ubuntu 24.04.2 Server ISO present in `local`. Provenance/hash not yet checked. |
| Network | `vmbr1` active with a private address, physical uplink and current untagged workloads; no VLAN-aware setting/tag on that path. The workstation uses its gateway as DNS; this does not identify the private-DNS management system. |
| Firewall | `pve-firewall status` returned `disabled/running`; node firewall enable=0. Existing per-NIC firewall flags are not proof of enforcement. |
| Backup | No Proxmox backup jobs and no PBS storage. `local` is backup-capable but shares the same `rpool` as the selected VM disks. Brian selected encrypted PostgreSQL logical copies on existing Proxmox and a new Google Drive folder. No safe host repository path/quota, folder, job, account right, unattended remote, encryption or restore was verified. Google Drive is the only selected off-host destination. |
| Proxy/name | LXC 110 named `proxy-ddns` is stopped; no active proxy was previously observed on legacy VM 107. Brian approved `appraisal.abrianbaker.com` for planning, but private DNS and DNS-01/certificate rights are unverified. |

Raw management addresses, MACs, device identifiers, firewall files and private
network dumps are excluded. No guest files, legacy database or Cloudflare
account were opened. The [runbook](mutation-plan.md) records the proposed
topology, remaining gates and rollback.
