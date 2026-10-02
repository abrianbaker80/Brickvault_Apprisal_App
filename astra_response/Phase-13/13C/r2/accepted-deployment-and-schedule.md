# Accepted deployment and backup schedule

These identities and results come from the accepted r1 evidence; no production
connection or new qualification was performed for closeout.

| Accepted deployment identity | Value |
| --- | --- |
| Release | `phase13c-marketplace-intake-r1` |
| Migration | `0017_listing_images` |
| Catalog | Generation 1; 28,278 sets; one active accepted nonsynthetic snapshot |
| Deployed build source ID | `791f09c12fbc7d8642e6578fc2e2428296dc63b7cb3a5af46aac90795bdffd08` |
| Manifest SHA-256 | `378bce4053dd9afb6d0d229536475353c727a80fecb25be2ca488a2740697d11` |
| Wheel SHA-256 | `c9d4c9841d9c54067a7e314e3dfe57dbde89de993bf9c5f69cc83a4861bd8e9d` |

[Deployment/capture evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/0d010531c122165ec8ec45a58e740c7e4c6853dd/astra_response/Phase-13/13C/r1/deployment-and-backup-format.md).
The local closeout changes status documentation and commits the operational overlay;
it does not rebuild, recalculate or change this immutable release identity.

| Accepted backup timer setting | Value |
| --- | --- |
| Calendar | `*-*-* 04:00:00 America/Chicago` |
| Calendar replacement | Empty `OnCalendar=` before the one daily calendar |
| Randomized delay | `0` |
| Persistent | `true`, unchanged |
| Server timezone | `Etc/UTC`, unchanged |
| Accuracy | Existing one-minute systemd window, unchanged |
| Separate drop-in | `deploy/systemd/brickvault-backup.timer.d/schedule.conf` |
| Schedule note | `docs/BACKUP_SCHEDULE.md` |

[Schedule evidence](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/30392cfb7f60edd4a6e0f3360ddda66903b37abc/astra_response/Phase-13/13C/r1/backup-schedule.md)
and [readback](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/30392cfb7f60edd4a6e0f3360ddda66903b37abc/astra_response/Phase-13/13C/r1/backup-schedule-validation.json).
A normal backup was already running at that inspection and finished before the
change. No extra backup or API interruption was caused by the change; no scheduler
state reset was needed. Image-inclusive backups still temporarily pause the API
through their accepted capture/readback mechanism. The existing Android APK was
not rebuilt. No timer or application operation ran during closeout.

Phase 14: NEXT / NOT STARTED; separate authorization is required.
