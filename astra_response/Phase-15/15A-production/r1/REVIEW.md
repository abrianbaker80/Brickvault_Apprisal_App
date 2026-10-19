# 15A Share-only production deployment — 2026-10-19

**BLOCKED — preactivation health and backup-history failures.** Existing production
backend and phone APK remain installed and usable; no rollback was needed. 15A
Share is **not promoted to production**. 15B capture is excluded, partial/unqualified,
preserved and not resumed. 15C is not started.

The exact clean isolated source is `e3c04d90b1646b9b9dad73325bf1491fb8326943`.
Reuse the accepted [15A closeout](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f8291d5b3b32f4c068d4be3b8803783728057bbf/astra_response/Phase-15/15A/closeout/r1/REVIEW.md)
and [physical TEST evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/335b76098acc4c9130a3b8b8120b770b207781e8/astra_response/Phase-15/15A/r2/REVIEW.md).
No accepted test campaign was rerun. Accepted source inspection confirms Share
filters/plugin, INTERNET-only permission, zero services, and absence of capture
classes/bridge/UI. No new release, manifest or APK was built before the stop.

Current VM115 / `brickvault-appraisal` release is `phase13c-marketplace-intake-r1`,
schema `0017_listing_images`, manifest
`378bce4053dd9afb6d0d229536475353c727a80fecb25be2ca488a2740697d11`.
The preserved installed production APK hash is
`045210d00ecf200b4579aed1ab0bb869c5c9d09eee7328c64472902d7851ddd2`, signer
`e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72`.
Production API and packaged WebView origins, system-only TLS trust and version
code 1 match the retained pair. No installation, sign-in or private app-data access
occurred; only the installed APK and nonsecret package identity were read.

Preflight blockers are concrete:

- An overdue kernel reboot fails `REBOOT_PENDING`; currently booted kernel is
  6.8.0-142, with installed 146/147 kernels in the required-reboot marker.
- The existing Python maintenance monitor reports 3.13.15 installed and 3.13.16
  available. This is observed monitor evidence; no runtime upgrade was attempted.
- Deep health and the read-only retention planner refuse “Partial or unrecognized
  backup history.” Snapshot reconciliation finds four unexpected/unreceipted
  Proxmox snapshots and three Drive snapshots dated October 13, with zero missing
  expected snapshots. Repository identities pass. The reason that historical run
  failed is not established; no receipt was invented or backup data removed.

The latest protected dual schema-3 receipt is October 19 09:07:19 UTC, with all
four artifacts represented in both repositories. Metadata and snapshot presence
were checked; archive bytes were not newly read back. No new release recovery
point, backup, restore rehearsal or prune was performed. Recent receipt freshness
does not clear the separate history-reconciliation failure.

API/Caddy/PostgreSQL remain active. Backup, renewal, retention, health and Python
timers remain enabled/waiting. Root/health HTTPS return 200, while unauthenticated
session/listing routes return 401. Four existing operational oneshot services retain
their failures; no status was cleared to conceal them. No API maintenance pause,
restart, release transfer, schema change, APK replacement or production write occurred.

After separately authorized operational maintenance and protected backup-history
reconciliation, resume the established immutable build/manifest paths with retained
absolute signing/cache locations. Warn before the normal dual database/blob backup,
which pauses the API through readback; then activate the same-schema backend, verify
auth/privacy compatibility, install the matching same-signer/code-1 production APK,
and run one two-image synthetic Share workflow with explicit review/destination/Save.
The retained rollback pair is the current immutable release and preserved APK;
application rollback must preserve current user data and elevated privacy without
database restoration. Stop on health/recovery, contract/signer or ambiguous writes.

No synthetic listing/images were created. Set 10350's previously reported missing
market values remain separate and uninvestigated; no pricing provider calls occurred.
All 22 original dirty/untracked files and 359 private evidence files were hashed.
Only one additive deployment section was added to Plan 108; its previous bytes,
pending 15B work and protected files are preserved. Main remains unpushed and its
index empty. The publication contains no private pixels, credentials, cookies or
device serials.

Receipts: [identities](source-and-artifact-identities.json),
[deployment/final services](deployment-receipt.json),
[recovery admission](recovery-point-receipt.json), [phone](phone-receipt.json),
[smoke not run](production-smoke.json), [preservation](preservation-checks.json).
