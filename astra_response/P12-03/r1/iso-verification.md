# Authoritative ISO verification — MATCH

- Filename: `ubuntu-24.04.2-live-server-amd64.iso`.
- Proxmox reference: `local:iso/ubuntu-24.04.2-live-server-amd64.iso`.
- Resolved path: `/var/lib/vz/template/iso/ubuntu-24.04.2-live-server-amd64.iso`.
- Local SHA-256: `d6dab0c3a657988501b4bd76f1297c053df710e06e0c3aece60dead24f270b4d`.
- Expected SHA-256: `d6dab0c3a657988501b4bd76f1297c053df710e06e0c3aece60dead24f270b4d`.
- Source: [Ubuntu-operated archive SHA256SUMS](https://old-releases.ubuntu.com/releases/24.04.2/SHA256SUMS).
- Result on 2026-09-29: **MATCH**, before VM creation or media boot.

The exact filename entry came directly from the official HTTPS checksum file,
not a snippet, mirror, forum or third-party hash database. The local digest was
calculated over the existing ISO. No replacement media was downloaded. No
detached-signature verification is claimed; the authorized gate required an
authoritative Ubuntu-published SHA-256. The ISO was attached but never booted.
