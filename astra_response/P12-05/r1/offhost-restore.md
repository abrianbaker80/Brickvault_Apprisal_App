# Google Drive-only real restore — PASS

Windows independently unlocked its accepted protected recovery context and
matched the Drive repository identity. VM 115's Drive credentials were not used
for the restore. Windows restic streamed globals, database and configuration to
pinned SSH; each received artifact matched the selected receipt size and SHA-256.
There was no persistent plaintext Windows dump and no Proxmox repository fallback.

The disposable PostgreSQL 18 cluster used a 256 MiB tmpfs, separate data/socket
directories, port 55435 with empty listen_addresses, and no TCP listener. Available
RAM was approximately 7.1 GiB; the database artifact was under 1 MiB. A temporary
bootstrap superuser avoided collision while restoring postgres/owner/runtime roles.
Root-only recovered configuration recreated the exact database identity/owner/marker
inside this isolated cluster. Live `/var/lib/postgresql/18/main` was not stopped,
restored over, or used as a restore target.

All 76 per-table row counts matched source before and after the rehearsal. Schema
and object inventory/ownership, effective table ACLs, column grants, function
grants and default grants matched. Database PUBLIC privileges and owner/runtime
role attributes/memberships passed the accepted guard. Revision was
`0016_hunt_cached_runs`; exactly one owner principal existed. Recovered owner and
runtime passwords authenticated through SCRAM on the isolated socket, and runtime
least-privilege checks passed. No passwords, verifiers or marker were displayed.

Four disposable restore attempts used the selected existing fresh backup. The
first three stopped at an over-strict evidence-helper comparison of stored ACL
representation; diagnostic narrowing found only 12 catalog staging-table ACLs.
PostgreSQL can represent owner-only grants as an explicit ACL or as NULL/default.
The final helper expanded defaults using PostgreSQL acldefault and sorted grant
entries on both clusters. Every effective grant, object owner and object identity
then matched. No production/source/grant modification was made to obtain PASS.
A Windows closed-pipe reader warning in the first relay was also corrected only
in the ignored helper. Later relays completed without that warning.

Every attempt stopped the disposable cluster, unmounted its tmpfs and removed
the mount directory, restored configuration, database plaintext, source inventory,
guest relay and temporary receipt copy. Sanitized evidence only was retained for
the rehearsal. After final cleanup, live admin verification, exact manifest,
all 13 light checks and zero failed units passed.


See [all 76 table counts](restore-table-counts.json) and
[sanitized verification](sanitized-evidence.json). The selected fresh backup
recovered the actual provisioned database, which has one owner and no catalog or
saved application data. This is not evidence of nonempty saved-work recovery.
