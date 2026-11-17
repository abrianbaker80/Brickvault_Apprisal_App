# Backup correction and recovery admission

The original failed stage is established as the database artifact's dual stream.
The retained Proxmox database snapshot ended at 14:42:46.936 UTC; the wrapper
reported failure at 14:43:17.625 UTC. Producer/destination stderr and exit statuses
were discarded by that version. The original cause and any relationship to earlier
incomplete runs remain unestablished. Absence of a Drive snapshot is not evidence
of a Drive outage, authentication failure or network fault.

A concrete orchestration defect was reproduced with real synthetic subprocesses:
a destination taking 31 seconds after EOF was terminated at 30.07 seconds although
the configured stream deadline was 60 seconds. The old code separately limited
worker joins and child waits to 30 seconds. The amended implementation applies the
existing single stream deadline to transfer, drain and finalization. It does not
increase the configured four-hour maximum or change backup policy.

Diagnostic improvement is separate from that correction: fixed artifact/stage/role,
exit statuses before and after cleanup, deadline, byte counts and allowlisted stderr
categories are emitted through existing Python logging. Raw stdout/stderr, commands,
URLs, configuration and environment values are never logged. Owned process groups
are terminated/reaped on failure; cancellation exits are distinguished from observed
natural exits. Small synthetic tests prove failure, timeout, spawn cleanup, redaction,
no complete receipt on failed capture, and existing API-pause restoration behavior.
Installed Linux checks additionally verify POSIX descendant-pipe cleanup.

Read-only preflight found no repository locks or overlapping backup children, no
new unexplained snapshots and adequate checked local space. The exact partial database
artifact was streamed through schema/revision verification and SHA-256/size readback
without writing a plaintext dump. Its ownership marker and schema 0019 were verified.
The supported ledger recorded exactly one FAILED_INCOMPLETE run, preserving its
snapshot, original receipts, permanent pins and all three prior partial-run entries.
It remains ineligible for recovery or retention deletion. Read-only PLAN passed.
No forget/prune/APPLY, forced unlock, deletion or broad ignore-unknown rule ran.

Only production_backup.py changed in each new wheel (plus its required RECORD).
The source/test amendment remains uncommitted. Schema-0019 maintenance release
phase16c-backup-maintenance-r2 was activated with the retained compatible 0019 release
and exact configuration available for in-place rollback; no database mutation or
restore was used for maintenance. Both the maintenance and final contents backend
carry amendment 51dff96c361d812b28927c59f809d5c267791e037e645f3723b09ff1ad5b6d2e.
The earlier unfinished maintenance-r1 build materialization was retained after its
strict source-byte check found the old accepted sdist's CRLF encoding. A distinct r2
identity was used; no finalized immutable artifact was patched. Original installed
backup bytes were 3d0662a8663ea4e069aa5ddf5e564e14b1aef479a94c7e9ea933165b7737b949;
canonical Git LF bytes were 24bdc7533a1a18b0f7dcba39557db4ff4c4a75e6ff6a285c9d18e5bce8ad8832.
Their normalized source matched exactly. The new module is identified in the amendment.

ONE additional normal full dual backup ran, 15:28:19–15:36:11 UTC on 2026-11-17
(9:28–9:36 a.m. Central). It captured the current database, globals, configuration
including the existing market credential recovery input, and image blobs. Both
admitted mappings predate its consistent database snapshot. Both destinations passed
artifact SHA-256/size readbacks and repository checks. The API resumed, with no pause
journal left behind. Recovery-proof verification passed at 15:41 UTC. The guarded
migration independently performed its required fresh readback of this SAME recovery
set; no second additional backup or restore rehearsal ran.

Complete recovery receipt SHA-256:
13a5e9fd2f7471d0dbd4ead912eeece5b17bcf921f0507cd5e809dde939a989d.

The successful retry proves current recovery admission, not the historical cause.
After migration, retain the compatible 0020 runtime and use forward correction when
history makes guarded downgrade ineligible. Never restore over newer user records.
The original failure evidence, protected exact admission/lineage receipts, partial
snapshots, old releases and original APK remain retained. The 04:00 America/Chicago
backup schedule is unchanged.
