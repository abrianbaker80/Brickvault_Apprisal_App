# Gate 8 immutable rollback operational incompatibility

**BLOCKED before any release switch.** Required target: `p12-04d-r1`.
Required exact forward release: `p12-05-catalog-repair-r1`.

All manifest file hashes/sizes verified for old (15 files) and forward (36 files);
static build loading passed for each with its accepted virtual environment.
Old manifest SHA-256:
`25cbb51ec895640f2ed27ab36afac8ebcd11590aa52f96015b15e460502b6f36`.
Forward manifest SHA-256:
`02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`.

Installed ExecStart paths under `/opt/brickvault/current/deploy/` reference scripts
absent from the required old release:

| Installed service | Missing rollback script |
|---|---|
| brickvault-health.service | production_health.py |
| brickvault-health-deep.service | production_health.py |
| brickvault-retention.service | complete_run_retention.py |
| brickvault-python-version.service | python_maintenance.py |
| brickvault-alert@RELEASE.service | operational_alert.py |

The root-owned installed certificate renewal hook matches the forward release,
but differs from the rollback hook. The current health release contract requires
installed hook bytes equal the hook under the selected current release. The old
hook lacks the forward operational-alert failure branch. Both certificate deploy
implementations and all eight web files are otherwise identical.

These facts establish an operational compatibility defect before switching, not
an observed rollback failure. No pointer/environment/health-config change, service
restart, timer pause, migration, old-hook replacement or source repair occurred.
Draft mutation helpers were removed; the diagnostic dispatcher rejects rollback
and forward modes. No substitute release or check-disable workaround was attempted.

Next required action is a separately reviewed compatibility disposition for this
exact target/current operational contract. The current repaired release remains
installed and unchanged. Authenticated rollback/forward workflow is unexercised.
See [live sanitized readback](compatibility.json).
