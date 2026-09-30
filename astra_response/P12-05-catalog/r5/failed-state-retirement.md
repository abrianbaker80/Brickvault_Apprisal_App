# One native guarded retirement

One recover-failed invocation returned recovered_for_fresh_retry and normal
acknowledgement. Current production remained r6; the exact repair interpreter ran
the native command with the freshly admitted private run/candidate UUIDs.
Elapsed: 70.713 seconds.

The original failed run keeps status failed, stage failed, database_failure,
original timestamps, source/provenance and dataset counts. Only accepted additive
catalog-failed-retirement-v1 / retire-and-fresh-retry metadata was added. Exact
candidate metadata/fingerprint remains in that recovery audit.

The candidate and exactly 1,898,466 predecessor staging rows were removed;
provider/source/all twelve file receipts remain. Canonical/validation/activation
rows stayed zero, pointer NULL/generation 0, no new retry yet. Durable exact-state
inspection passed. The retirement command was never repeated; no ambiguous
acknowledgement occurred. Later retry/activation preserve this failed audit.
