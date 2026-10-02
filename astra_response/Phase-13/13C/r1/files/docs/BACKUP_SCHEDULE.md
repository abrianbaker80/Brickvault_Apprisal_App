# Daily production backup schedule

Brian approved this operational change on October 1, 2026 (Central).
The existing VM115 image-inclusive backup timer now has one daily calendar:
`*-*-* 04:00:00 America/Chicago`, with `RandomizedDelaySec=0`.
The server timezone remains `Etc/UTC`; `Persistent=true` and the existing
one-minute systemd accuracy window are preserved.

Install the tracked [schedule drop-in](../deploy/systemd/brickvault-backup.timer.d/schedule.conf)
as `/etc/systemd/system/brickvault-backup.timer.d/schedule.conf`, root-owned,
mode 0644. Its empty `OnCalendar=` replaces the base calendar. The immutable
release and base timer remain unchanged. Backup, encryption, retention,
pinning and verification behavior are unchanged.

The old schedule had already triggered at October 2, 03:29:04 UTC before
inspection. That normal backup finished successfully at 03:35:28 UTC and
resumed the API before the timer was changed. Its completed protected receipt
includes all four artifacts, including `image-blobs.tar`.

The retained last trigger follows the latest elapsed occurrence of the new
calendar (October 1, 09:00:00 UTC), so no persistent-state reset was needed.
Only the timer was stopped, its drop-in installed, systemd reloaded and the
already-enabled timer started. No backup service invocation or API restart
occurred during this change; receipt history and scheduler timestamp stayed
unchanged.

Calendar parsing and effective service/timer readback passed. At validation,
the timer was enabled and active/waiting, with exactly one calendar and zero
randomized delay. Its next scheduled trigger was **October 2, 2026, 04:00:00
CDT (America/Chicago), equivalent to 09:00:00 UTC**. The backup service was
inactive and the API active; both invocation identities and the API PID were
unchanged across the timer change.

This operational addendum preserves the Phase 13C candidate and protected
files. No application deployment, tests, builds, backup invocation, restore,
browser/device work, migration or health campaign was performed. Main remains
uncommitted and unpushed.
