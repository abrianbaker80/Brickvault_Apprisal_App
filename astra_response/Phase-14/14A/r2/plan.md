# Phase 14A bounded execution

Implement the amended USD 10.00 lifetime cap for exact `gpt-6-luna`, retain ten
inference attempts and the exact seven groups/13 approved photos/texts, and run once.
Use a whole-model input ceiling for conservative reservations without token counting.
Report exact raw recognition separately from canonical catalog coverage.

Delivered: cap/schema/CLI changes, durable accounting and sanitized HTTP diagnostics,
independent raw scoring, canonical coverage counters, workload and cost averages.
Reuse three retained accepted-catalog references; fourteen confirmed figure labels
remain canonically unresolved. No mapping, import, migration, database startup or
production operation was needed. The ledger was initialized once from previously
absent state, and the failed G06 reservation remains retained.

The one run sent six requests and stopped on G06 incomplete output. Five groups
completed; G07 was not sent. Stop for review. A manual retry needs explicit revised
output/reasoning and retry approval; the failed attempt remains counted. The broader
Phase 14 comparison and Phase 15/16 are outside this delivery.

[Current source plan](source/docs/plans/104-recognition-quality-pilot.md)
