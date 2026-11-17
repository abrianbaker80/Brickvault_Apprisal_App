# Recovery admission failure

The one authorized backup failed in the existing dual-stream implementation before
a complete receipt or recovery proof existed. A new database artifact is retained on
Proxmox; none was observed on Drive. Neither is a qualifying complete dual recovery
point. The latest complete receipt is still 2026-11-17 10:08:38 UTC, before the two
mapping inserts at 14:17:23 UTC. No migration, grants or activation followed.

The current wrapper suppresses producer/sink output and collapses stream failures into
one BackupError. The underlying cause cannot be attributed to Drive, the network,
the producer, timeout or storage from the retained evidence. Repository snapshot
enumeration succeeded for both destinations. No broad repair was attempted.

Read-only retention planning now returns `Partial or unrecognized backup history.`
The new partial artifact was preserved; no ledger amendment or deletion ran. The
14 direct ordinary health checks passing does not make recovery admission pass.
The health unit still records HTTPS_CERTIFICATE/LISTENERS failure at 14:43:19 UTC;
later direct checks of both pass. API is active and the pause journal is absent.

Next authorization should cover bounded backup failure diagnosis and its production
root-cause correction, a reviewed disposition of the evidenced partial run, and one
recovery retry. Preserving diagnostic failure details may be needed because the
current implementation discards them. Do not treat a ledger entry alone as repair.
No new migration, mapping or broader maintenance campaign is required by this report.

Private originals and task-owned protected exact copies were retained. Admission
receipt SHA-256: `781063b2b981996ab47f8a1033016bf92458d486729328370c7ed24a8bf31a35`.
Lineage SHA-256: `0b01449dd5e95b79f85e46035f95e8fde364508c5bf4c4075c655b602afb591b`.
An earlier task copy normalized line endings; it was retained and supplemented with
the exact-byte protected copy. The original evidence was never changed.

Initial Windows materialization had CRLF bytes. It was retained and excluded; a clean
isolated canonical-LF clone supplied the final candidate. No immutable release was
patched or identity reused for different bytes. The sole finalized candidate remains
staged for future reviewed use. No accepted-source modifications were made.
