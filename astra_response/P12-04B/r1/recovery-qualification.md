# Synthetic recovery qualification

| Check | Proxmox supplemental copy | Google Drive off-host copy |
| --- | --- | --- |
| Repository | Restricted SFTP chroot `/repository` on Proxmox | `Brickvault_Apprisal_App_Backup/restic-production` |
| Encryption | Separate restic password; repo ID prefix `db58f878c2` | Different restic password; repo ID prefix `a82ca12e8252` |
| VM operation | Canary backup and `restic check` passed | Folder creation, initialization, canary backup and `restic check` passed |
| Independent context | Windows recovery transport key and restic password | Windows encrypted rclone config, DPAPI unlock and restic password |
| Windows restore | **PASS** | **PASS** |
| Exact verification | Pre-recorded run ID, manifest, file size, bytes and SHA-256 matched | Same manifest, file size, bytes and SHA-256 matched |

The canary contains only synthetic bytes, a random run ID and a timestamp. Windows used a fresh private temporary restore directory for each destination and removed each directory after successful comparison. The Drive restore contacted the off-host repository without VM 115. The Proxmox copy shares the physical host and is supplemental only. No production database or customer data was involved.

Credentials and full repository identifiers are held in protected local state, not this review. The Windows recovery set can open both repositories if VM 115 is lost. Simultaneous VM/laptop loss still needs an offline custody decision before production migration.
