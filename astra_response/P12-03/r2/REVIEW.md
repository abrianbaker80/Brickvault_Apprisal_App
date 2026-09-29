# P12-03 r2 — automated Ubuntu base VM

## Review verdict

**READY FOR P12-03 REVIEW.** VM 115 has a verified Ubuntu Server base installation,
key-only administrator access, base updates, SSH hardening and working QEMU
guest integration. The 128-GiB data disk remains blank. VM 115 is gracefully
stopped with `onboot=0` and `scsi0` boot order. P12-03 is **not CLOSED** until
ChatGPT review, and no P12-04 work was performed.

Brian's continuation superseded the manual-installer boundary of the
[r1 partial review](../r1/REVIEW.md). Main remains at
`01db616d503b66c30b7fe95fc8e0259102ca2618`, with its index empty and
three protected files unchanged. This r2 package preserves r1 and contains
only P12-03 documentation and sanitized evidence.

## Result

- The checksum-verified Ubuntu Server **24.04.2 ISO** booted normally under
  OVMF Secure Boot. A private NoCloud seed attached only to VM 115 supplied
  autoinstall data; the ISO's GRUB entry received `autoinstall ds=nocloud`.
  The target was the exact `scsi0` udev identity, with pre-partition checks
  for the 32-GiB OS and 128-GiB data disks. The installer powered off on
  completion. Official Ubuntu updates advanced the installed release string
  to **24.04.5 LTS**.
- Post-install apt completed **90 package upgrades and four new packages**:
  `libdrm-amdgpu1`, `libfwupd3`, `liburing2`, and `qemu-guest-agent`.
  OpenSSH, CA certificates, curl, gnupg, jq and unattended-upgrades were
  already present. Apt has no pending candidates; `dpkg --audit` is empty.
- `brickvault-admin` authenticated with the approved laptop public key and
  has sudo. After `sshd -t` and reload, a fresh key-only SSH session passed.
  Effective SSH settings disable root, password and keyboard-interactive
  logins. The temporary installer password is locked. Sudo is
  `NOPASSWD:ALL` for this sole administrator, so the approved key grants
  full VM administration.
- The guest agent is active. Proxmox `qm agent 115 ping` and
  `network-get-interfaces` succeeded after a graceful stop/start added its
  channel. DHCP, route, DNS, synchronized time, TRIM and standard update
  timers passed. The observed listeners were SSH, local DNS and DHCP client.
- Guest and stopped-host probes found **zero partitions, filesystem/LVM
  signatures, mounts and fstab entries** on the 128-GiB disk. Its host
  allocation stayed at the fresh-volume baseline. All 17 pre-existing guest
  configuration hashes and the r1 storage inventory matched their baseline.
- The task-owned seed ISO and extracted installer files were removed after
  detachment and ownership/reference checks. The shared verified Ubuntu ISO
  remains intact. No snapshot, backup or application service was created.

## Evidence

- [Final ExecPlan 093](source/docs/plans/093-base-vm-provisioning.md)
- [Automated-install method and diagnosed retries](automated-install.md)
- [Base OS and data-disk validation](base-os-validation.md)
- [Sanitized executed command sequence](commands.txt)
- [Validation and preservation summary](validation.txt)
- [Cumulative five-document P12-03 patch against main](changes.patch)

The patch contains the workflow, roadmap and Plans 091/092 updates. The
ExecPlan snapshot retains its repository-relative links; those links resolve
in the main checkout rather than this minimal public package.

## Deviations and limits

The direct-kernel diagnostic boot hit Secure Boot verification before disk
writes; normal signed-ISO boot passed. A first seed used the SCSI serial in
Subiquity's `match.serial`, which actually compares udev `ID_SERIAL`; the
installer stopped before writing either disk. The seed was corrected to the
exact `scsi0` udev identity before the successful run. Proxmox-host Debian
`ripgrep` and `sbsigntool` were installed for this diagnosis; there were no
other host package upgrades. Enabling the agent required a graceful VM
stop/start because the channel was absent from the already-running process.
An initial cleanup command failed locally due to PowerShell substitution;
file presence was rechecked and guarded host-side cleanup then succeeded.

This is base-server qualification only. No BrickVault application build/test,
database, production runtime, proxy, certificate, DNS, backup or physical
Android acceptance is claimed. Private DHCP, MAC, VM UUID/serial, SSH key
contents and installer password/hash remain outside the public package.
