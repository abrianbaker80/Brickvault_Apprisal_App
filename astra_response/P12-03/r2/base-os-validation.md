# P12-03 base OS validation

| Gate | Observed result |
| --- | --- |
| Source and installed OS | Verified 24.04.2 installer ISO; installed Ubuntu 24.04.5 LTS after official updates, kernel `6.8.0-142-generic` |
| Platform | KVM, host CPU model, four vCPUs, 7.7 GiB usable RAM from fixed 8192 MiB VM allocation |
| Administrator | `brickvault-admin` in sudo group; approved laptop key login, noninteractive sudo; temporary password locked |
| SSH | `sshd -t` passed before reload; post-reload key-only connection passed; effective root, password and keyboard-interactive login all `no` |
| Packages | 89 standard upgrades plus one dependency-requiring `fwupd` upgrade; four new Ubuntu packages: `libdrm-amdgpu1`, `libfwupd3`, `liburing2`, `qemu-guest-agent`; no pending upgrades or dpkg audit issue |
| Guest agent | Service active; Proxmox ping and network interface query succeeded after channel-enabled stop/start |
| Network and clock | Private DHCP, default route, Ubuntu DNS resolution, synchronized time; no static IP, DNS, router or firewall change |
| Listeners | TCP 22 for OpenSSH; local DNS stub; DHCP client UDP; no application or database listener |
| Root storage | 32-GiB `scsi0` has EFI and ext4 root; 31-GiB root filesystem with about 22 GiB free |
| Swap and discard | Standard 4-GiB swap file with zero use; guest discard capability and active `fstrim.timer` |
| Data storage | 128-GiB `scsi1` has zero child partitions; guest `wipefs`, `blkid`, LVM, mount and fstab checks empty; stopped-host `wipefs`/`lsblk` empty; fresh-volume ZFS allocation unchanged |
| Final VM | Stopped by guest poweroff, `onboot=0`, `scsi0` boot, EFI/OS/data/NIC intact, agent configured, no installer media attached |

No P12-04 software or configuration was added: no BrickVault checkout or
service, PostgreSQL server, Python 3.13 runtime, uv, Caddy, restic/rclone
repository, production secrets, provider credentials, certificate or DNS
configuration. No application tests, device checks, snapshot or backup were
run in P12-03. The private DHCP address and hardware identifiers are retained
only in ignored local evidence.
