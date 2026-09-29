# Pinned backup tooling sources

| Tool | Version | Official source | Verification |
| --- | --- | --- | --- |
| restic | 0.19.1 | [Project release](https://github.com/restic/restic/releases/tag/v0.19.1) and [installation guidance](https://restic.readthedocs.io/en/stable/020_installation.html) | Published SHA-256 manifest signature verified against fingerprint `CF8F18F2844575973F79D4E191A6868BD3F7A907`; Linux and Windows archive digests matched. VM executable is root-owned `0755`. |
| rclone | 1.75.1 | [Official downloads](https://rclone.org/downloads/) and [release signing](https://rclone.org/release_signing/) | Published SHA-256 manifest signature verified against fingerprint `FBF737ECE9F8AB18604BD2AC93935E02FF3B54FA`; Linux archive digest matched. VM executable is root-owned `0755`. |

The Windows recovery context has restic 0.19.1 and rclone 1.75.1. The [rclone Drive documentation](https://rclone.org/drive/) describes the dedicated OAuth client requirement and `drive.file` access. Existing Google Drive API access and a production-published OAuth audience were checked in the user's Cloud project. The new client and token are held only in protected recovery locations; their identifiers and secrets are excluded here. No Proxmox package installation was needed.
