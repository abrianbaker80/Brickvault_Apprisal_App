# P12-03 infrastructure before and after

| Item | Before | After |
| --- | --- | --- |
| Node | Standalone pve, PVE 9.1.6, kernel 6.17.13-2-pve | Unchanged; no host upgrade |
| RAM | 188.8 GiB total; 148.6 GiB available | 8 GiB assigned to stopped VM; no guest boot |
| local-zfs | Active; 398,886,824 KiB available; rpool ONLINE, zero errors | 398,887,708 KiB available; thin allocation, full 160-GiB growth budget retained |
| Pool caveat | Some supported/requested features not enabled; last scrub zero errors | No pool upgrade or policy change |
| VMID/name | 115 absent; nextid 115; no name collision | Exactly one VM 115 brickvault-appraisal |
| Existing guests | 17 QEMU/LXC guests | Inventory and host-side config hashes unchanged after every mutation |
| Legacy 107 | Running | Running; unchanged; never accessed or mutated |
| Bridge | Reviewed active private untagged vmbr1 | Unchanged; one new VirtIO NIC attached |
| EFI | Absent | local-zfs:vm-115-disk-0, normal 1-MiB OVMF variables disk; pre-enrolled keys; automatic ms-cert=2023w |
| OS | Absent | local-zfs:vm-115-disk-1, scsi0, 32 GiB, discard/iothread/ssd enabled; no installed OS |
| Data | Absent | local-zfs:vm-115-disk-2, scsi1, 128 GiB, discard/iothread/ssd enabled; untouched |
| Media | Existing Ubuntu Server 24.04.2 ISO | Same authenticated ISO at ide2; no download/modification |
| VM compute | Absent | q35/OVMF, host CPU, 1 socket/4 vCPU, fixed 8192 MiB, balloon 0, virtio-scsi-single, l26 |
| Boot/onboot | Absent | ide2;scsi0; onboot 0 |
| VM runtime | Absent | Stopped; no start/shutdown command needed |
| OS/admin/DHCP | None | None; manual installation required |
| P12-04 | Out of scope | None performed |

Data checks: 137,438,953,472 bytes; lsblk one disk, no child partitions,
null filesystem, empty mountpoints; wipefs --no-act empty signatures;
blkid -p status 2; findmnt no source mount. No filesystem/LVM/partition signature.
These are host-side pre-install checks, not guest OS acceptance.

New OS/data volumes each reported 57,344 bytes used/referenced from ZFS
allocation metadata; EFI reported 94,208 bytes. Thin provisioning does not
reserve full physical growth space; preflight allowed full disk growth.

Rollback: retain stopped VM, all three volumes, NIC and media. No automatic
destruction/deletion. Separate destructive approval is required.
