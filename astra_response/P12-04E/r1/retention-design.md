# Complete-run retention

One policy item comprises a structurally valid protected schema-2 production
receipt and all three artifacts (database.dump, globals.sql, configuration.tar)
in both independently identified repositories. The planner rejects missing,
extra, malformed, overlapping or ambiguous snapshot identities and changed
receipt/pin metadata. Snapshot paths and tags must match the complete run.

Sort by verified UTC time and then run ID. Keep the newest run in each of the
latest 30 distinct UTC days, 8 ISO weeks and 12 calendar months; take their union
and add permanent pins. The two accepted production recovery points and both
synthetic canaries are permanently pinned. Sparse history retains available
buckets; overlapping policies do not produce artifact-level decisions.

The plan digest binds policy, UTC date, exact keep/delete sets, repository
identities, all receipt digests, complete snapshot metadata, pins and ledger.
Apply gathers again and requires the exact digest. Before deleting anything it
reads back every selected artifact from both destinations and rechecks the plan.
Only the three explicit snapshot IDs for a selected complete run are forgotten
at each destination. Exact surviving snapshot inventories and restic check follow
each destination. Backup, retention and deep planning share a protected flock.

Before any destructive call, persist a DEGRADED ledger and exact transaction
intent. After each successful destination, persist progress. Only complete
success returns READY. First-destination failure, partial cross-repository failure,
interruption or failed post-check leaves durable DEGRADED state and stops all
further deletion. No destructive retry is automatic. Normal configuration reads
remain capped at 64 KiB; retention evidence/ledger reads have a bounded 16 MiB
limit so full snapshot evidence remains readable as history grows.

Pins: /etc/brickvault/backup/retention-pins.json, root:root 0600.
Ledger/transactions: /etc/brickvault/backup/retention/, root:root 0700, files 0600.
Receipts remain available after logical deletion and their digests stay in the
ledger. Protected records use exclusive temporary creation, fsync and atomic
replacement. Raw IDs remain only in protected local evidence.

Operator repair after DEGRADED: stop the retention timer; preserve ledger,
transaction and both repository inventories; establish which operations really
completed, verify pinned history and repository integrity, and review a concrete
recovery/reconciliation plan with Brian. Never clear DEGRADED or replay deletion
blindly. Prune requires READY, unchanged current plan, zero pending candidates,
and prior completed deletion/readback/check evidence; it also persists failure
state before mutation. There is no prune timer.

Six initial retention tests passed (313.085 seconds), including actual forget
against disposable LOCAL Linux restic repositories, complete-run/pin preservation,
changed plan, incomplete/ambiguous history, first-destination and partial
cross-repository failures, and degraded refusal. A later focused Linux root-file
regression proved large protected-state roundtrip, size bounds and permission
refusal; the two policy tests also passed again. No production deletion occurred.

First live invocation: PLAN keep=3, delete=0, digest
`65c14383b67e90edf7e59b8a6b4ff43ec3b7c3b3c156a36e904ab8bb4be5ff7b`.
Digest-bound apply returned NOOP. Ledger remains READY with no deleted runs.
Weekly retention was enabled only after all required disposable and live gates.
Future scheduled runs may apply the reviewed complete-run policy under the
explicit P12-04E authorization; that is distinct from this checkpoint's NOOP.
