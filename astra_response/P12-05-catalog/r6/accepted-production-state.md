# Accepted production state reused from r5

This is the accepted r5 state, **not refreshed during r6 closeout**. The current
release and artifact hashes are in [accepted activation](accepted-catalog-activation.md).
Importer repair and catalog activation prerequisite are ACCEPTED / CLOSED;
P12-05 is IN PROGRESS / RESUMABLE and Phase 12 remains IN PROGRESS.

One pre-recovery dual backup and one post-activation dual backup passed.
Each passed Proxmox and Google Drive, `database.dump`, `globals.sql`,
`configuration.tar`, six encrypted readbacks, hashes/sizes, both repository
checks and a protected schema-2 receipt. The final post-activation backup contains
the repaired current release configuration, nonempty accepted generation-1
catalog and migration 0016. These backups are accepted prerequisite evidence;
the final P12-05 dual backup remains a separate, unstarted gate.

| Accepted receipt | SHA-256 |
| --- | --- |
| Pre-recovery | `40a0018c30ef9e7deb59a6793b587e1d9bf80d3747a506f4bc8a58c840cf6b78` |
| Post-activation | `2548a2a4a64974406d8f25ed5c0329dcca815d9d267819aa44463d73f87ee358` |

[Accepted pre-backup](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/09035359864d021518341c37f32a6ce453ceb3ca/astra_response/P12-05-catalog/r5/pre-recovery-backup.md) and
[post-backup](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/09035359864d021518341c37f32a6ce453ceb3ca/astra_response/P12-05-catalog/r5/post-activation-backup.md).

Accepted production admin passed with exactly one owner and migration
`0016_hunt_cached_runs`. All 13 health checks passed; retention was READY,
required timers active/enabled and failed units zero. API/PostgreSQL were
loopback-only, trusted private HTTPS passed, public application A/AAAA were
absent and no BrickVault WAN forwarding existed. No credential leakage was
found; source archives remained outside static roots. Caddy/PostgreSQL/listeners,
timeouts, schema/indexes and VM resources were unchanged. No market-provider
activation or Phase 13 work occurred.
[Accepted final operations/security/network](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/09035359864d021518341c37f32a6ce453ceb3ca/astra_response/P12-05-catalog/r5/final-production-state.md).

All substantive r5 evidence is linked and hash-bound in [the reuse manifest](r5-evidence.json).
[Remaining P12-05 gates](remaining-p12-05-gates.md) are recorded only.
