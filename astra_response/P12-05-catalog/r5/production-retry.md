# Exactly one predecessor-linked production retry

One retry-import invocation used the original protected failed predecessor UUID.
Ordinary import mode was not used. The retry completed successfully: exact twelve
datasets, 1,898,466 staging/evidence rows, fingerprint continuity, atomic candidate
build and structural report passed; candidate validated, run succeeded/stage
validated. Before activation: exactly two audits, failed predecessor preserved,
zero activation receipts and NULL active pointer/generation 0.

Semantic fingerprint: `8f37571222fb078a2f75927ee1c58a7c3a90994bb24bee269270f784ebd48395`. Production timeouts stayed
300000 ms statement / 10000 ms lock. Zero statement/lock timeouts; 274 completed
named operations; no failed named operations/observer errors. Total observed
helper execution including native guards/parse/final verification:
1258.666 seconds.

Maximum production statement time **172.357442 seconds**, operation
`part_color_observations:inventory_parts`, phase `candidate_build`;
SQL identity `f7ff5498db8073df71458bf22696dd7f0fe8595a07c833bb2148f90563630589`. Margin: 127.642558 seconds below
the unchanged statement limit. [All sanitized named timings](statement-timings.json).
No raw SQL, production UUIDs or network/source paths are published.

Python 3.13 local monitoring observed the installed quiet_progress callback at
entry after a nonmutating admission probe. Existing event data was copied to
protected receipts; neither wrapper/importer function bindings nor code changed.
This captures the accepted statement event elapsed times, not a new server-side
profiling or PostgreSQL configuration scheme. Streaming digest operations also
emit named timings and are labeled as such in the dataset.

VM remained eight CPUs/16,384 MiB. No PostgreSQL setting, migration/index/schema,
manual ANALYZE, extra source repair, second retry or new-failure recovery. Native
accepted importer build statistics ran unchanged as part of normal construction.
Validation/audit/source/file ownership and noncatalog security/row counts passed
durable read-only checks before exact activation.
