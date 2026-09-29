# Open gates after P12-04B acceptance

## Backup/admin receipt integration

The accepted backup runner writes `schema`, `purpose`, `database`, `ownership_marker`, `run_id`, `verified_at_utc`, `repositories`, and artifacts with byte count, SHA-256, and per-destination snapshot IDs. `brickvault-production-admin` requires `purpose`, `database`, `ownership_marker`, `revisions_at_backup`, `proxmox_snapshot`, `drive_snapshot`, and `verified_at_utc` before `migrate`, `grant-runtime`, or `bootstrap-owner`. A successful backup run does not yet directly create that admin proof.

Before production migration, P12-04C must add one guarded conversion/finalization step that verifies the complete backup receipt and both repository readbacks; binds the exact production ownership marker and pre-migration Alembic revision tuple; derives stable recovery identifiers; and creates a new root-owned protected admin proof within the existing recency limit. Missing destination/readback must fail. Operator-entered arbitrary snapshot hashes and a weakened admin gate are prohibited. Test the integrated sequence end to end in P12-04C.

## Offline recovery custody

The current VM and protected Windows recovery sets permit restoration after loss of either one. They do not survive simultaneous VM and laptop loss. Before the first production migration, establish durable offline custody of the minimum credentials required to restore both repositories. P12-04C must resolve the mechanism. Do not create or publish secrets through this closeout, Git, ChatGPT, email, Downloads, or the repository.

## Remaining P12-04 and P12-05 gates

P12-04C is next and has not started. Still open: offline custody; backup/admin receipt integration; packaged backup runner installation on VM 115; production database provisioning; first real dual backup/readback; protected recovery proof; migration; runtime grants; owner bootstrap; complete-run retention deletion implementation and review; backup timer installation/activation; production API secrets/configuration; API startup; private DNS; trusted certificate; Caddy; firewall/client-source policy; monitoring/alerts; and VM production onboot behavior.

P12-05 has not started. Real database restore, browser, PWA, Android, and rollback acceptance remain open. Synthetic canary restores do not satisfy those gates.
