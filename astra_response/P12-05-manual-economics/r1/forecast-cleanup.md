# Normal unsaved-preview expiry cleanup

Prior P12-05 r2 reports one ordinary UNSAVED/PENDING capture at creation. It was not
saved or manually deleted. This slice has no production interaction; its current
state and expiry cleanup are not freshly observed or claimed.

The saved-forecast guard refuses deletion when saved_at is set or the normal
save_eligible_until deadline has not passed. Pending deadlines are at most
15 minutes from creation. A later normal ForecastService._preview invokes
forecast_cleanup(owner) within its transaction. Cleanup selects only that owner's
expired unsaved rows, ordered by deadline/identity, at most 100, with SKIP LOCKED.
Saved history is excluded; passive status/historical/index reads do not perform it.

Fresh isolated real PostgreSQL tests passed:

- test_forecasts_expired_status_cleanup_and_saved_protection creates two ordinary
  previews, saves one, verifies the other's normal 15-minute deadline, advances
  only the disposable TEST clock, rejects the expired save, invokes a normal
  preview, verifies pending-row removal and saved-row preservation.
- test_forecasts_bounded_cleanup_and_payload_limit confirms payload size guards,
  100 then 1 expired unsaved rows removed, and saved-row protection.

Both tests passed (2 tests, 17.84s), using the owned TEST runner with API smoke
disabled. The ledger reports passed, pytest exit 0, every run-recorded database
removed and no leftovers; preexisting service/resource state is preserved by the
runner. Only TEST clocks were controlled. No production/development clock, guard,
schema or records were touched. Later separately authorized production acceptance
may use the existing normal expiry/preview cleanup path.
