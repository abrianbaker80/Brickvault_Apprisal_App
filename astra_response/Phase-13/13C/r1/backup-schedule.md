# Daily backup schedule operational addendum

Brian authorized this narrow change on October 1, 2026 (Central).
The [matching timer drop-in](files/deploy/systemd/brickvault-backup.timer.d/schedule.conf)
and [repository schedule note](files/docs/BACKUP_SCHEDULE.md) are the only two
additional repository files. The [current inventory](changed-files.txt) has the
original twenty Phase 13C files plus these two; all original candidate/protected
bytes remain unchanged, main HEAD remains the accepted 13B checkpoint, and the
main index is empty. The immutable application release and base timer were untouched.

Effective schedule: `*-*-* 04:00:00 America/Chicago`; randomized delay zero.
Timer enabled and active/waiting. `Persistent=true`, `AccuracySec=1min` and the
server timezone `Etc/UTC` are preserved. Next scheduled trigger:
**October 2, 2026, 04:00:00 CDT / 09:00:00 UTC**.

The old schedule had started a normal backup at 03:29:04 UTC before inspection.
It completed successfully at 03:35:28 UTC and resumed the API naturally. Its
protected receipt records the four required image-inclusive artifacts. This
run was not invoked by this task. Only after it was idle and the API active
was the timer stopped, its drop-in installed, systemd reloaded and the already
enabled timer started. LastTrigger remains 03:29:04 UTC, later than the latest
elapsed new-calendar occurrence (October 1, 09:00 UTC); no scheduler-state reset
or catch-up backup was required. Receipt hashes and scheduler stamp are unchanged.

[Sanitized readback](backup-schedule-validation.json) records one effective
calendar, zero random delay, future next trigger, inactive backup service and
active API. Backup invocation/start timestamp and API invocation/PID stayed
unchanged through the change and subsequent readback. Validation was limited
to calendar parsing, effective timer/next-run and service-state readback. No
tests, builds, backup invocation, restore, browser/device, migration, application
deployment or additional health campaign ran. Main was not pushed.

The original cumulative application patch and validation remain historical
Phase 13C evidence. The operational drop-in is managed separately under
`/etc/systemd/system/brickvault-backup.timer.d/`; this addendum does not rebuild
or revise the existing immutable release or its source identity.
