# Automated installation of VM 115

The OS source was the existing Ubuntu Server 24.04.2 ISO. Its SHA-256 matched
the [official Ubuntu archive checksum](https://old-releases.ubuntu.com/releases/24.04.2/SHA256SUMS)
before boot. OVMF Secure Boot remained enabled throughout.

One task-owned NoCloud `cidata` ISO held private cloud-config with an
`autoinstall` document. It specified hostname `brickvault-appraisal`, user
`brickvault-admin`, the approved laptop **public** SSH key, OpenSSH, a
temporary high-entropy password hash, security updates and installer
poweroff. No plaintext password was written to disk or logs; the laptop
private key was never read or transferred. An early command refused storage
configuration unless exactly one 32-GiB OS disk and one 128-GiB data disk
with the expected VM-specific serials were present. The storage layout
selected the exact `scsi0` udev `ID_SERIAL` and did not mention `scsi1` as
an installation target. The seed's raw contents are private.

The signed ISO was booted through its normal GRUB menu. The selected
`Try or Install Ubuntu Server` entry was edited through VM 115's QEMU
console to place `autoinstall ds=nocloud` before the kernel line's `---`.
This uses Ubuntu's documented
[NoCloud autoinstall delivery](https://canonical-subiquity.readthedocs-hosted.com/en/latest/howto/autoinstall-quickstart.html)
and [zero-touch boot parameter](https://canonical-subiquity.readthedocs-hosted.com/en/latest/explanation/zero-touch-autoinstall.html).
No shared ISO, LAN PXE/DHCP/TFTP service or other guest was changed.

Two diagnostics preceded the successful run. A direct QEMU kernel/shim
boot displayed a Secure Boot verification error before any disk write; the
normal signed ISO reached GRUB, ruling out a general ISO boot failure.
The first NoCloud seed then failed at storage selection before disk writes:
Subiquity's `match.serial` compares udev `ID_SERIAL`, while the custom
serial seen by `lsblk` was `ID_SCSI_SERIAL`. The live-installer udev output
confirmed both fields. The seed was regenerated with the exact `scsi0`
`ID_SERIAL`; the early serial-and-size guard remained. This matches
[Canonical's storage matcher definition](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html).
Fresh stopped-VM gates again verified both blank disks, ISO hash, task-owned
seed and VM configuration before the corrected run.

The successful installer partitioned only the 32-GiB OS disk, extracted the
base image, installed OpenSSH and security updates, and powered off. Host
readback showed an EFI partition and ext4 root on the OS disk and no data-disk
signatures. After that, the seed and Ubuntu ISO were detached, boot order
was set to `scsi0`, and the installed OS was started for validation. The
task-owned seed/media extraction files were removed after installation;
the shared verified Ubuntu ISO was preserved.
