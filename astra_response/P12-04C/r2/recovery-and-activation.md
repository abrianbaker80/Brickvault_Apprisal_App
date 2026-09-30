# Real backup, proof and database activation

The accepted r1 failure remains recorded: the original production backup attempt failed before creating a snapshot or receipt. No rollback or deletion of the provisioned production database/roles occurred.

After r4 installation and unit verification, the admission gate confirmed an unmigrated database, no principal, one accepted canary in each repository, and empty protected receipt/proof directories. Exactly one authorized first-backup retry then succeeded through the installed service.

The pre-migration backup streamed database.dump, globals.sql and configuration.tar to both independently encrypted repositories. All six encrypted readbacks matched the streamed sizes and SHA-256 values, both repository checks passed, and the runner created a root-protected schema-2 receipt. No persistent plaintext dump was used. The run ID was kept in private local custody.

Guarded proof finalization reread that receipt and all six artifact copies, checked both repositories, matched the exact production marker and empty revision tuple, bound the receipt digest and created a fresh root-owned 0600 proof with exclusive creation. No proof was fabricated or edited.

Production-admin migration validated the same proof and reached packaged head `0016_hunt_cached_runs`. Runtime grants validated that proof again and applied the enumerated policy. The runtime guard, production role/membership/marker checks, schema ownership, no runtime CREATE/database TEMP privileges and protected principal privileges passed. No application principal existed before local owner bootstrap.

Brian created the single private owner through the approved command in a local interactive SSH TTY with hidden password prompts. The password never entered chat, logs or review files. Independent production-admin verification then passed exact production ownership, marker, migration head, one owner principal and runtime privileges.

The one post-bootstrap service run then passed the same three-artifact, dual-repository pipeline, including six encrypted readbacks and both repository checks. Its protected receipt records revision `0016_hunt_cached_runs`. The pre-migration receipt records the empty revision tuple. Both receipt files and the generated pre-migration proof are root-owned 0600 under protected directories.

Final snapshot checks found seven snapshots per destination: the original canary plus three artifacts from each of the two real runs. The daily timer was enabled only after the second backup succeeded. It is active with a next trigger of `2026-09-30 03:22:03 UTC`; the backup service is inactive after successful completion. No extra manual scheduled backup was invoked.

Final checks retained the API disabled/inactive, no API listener/api.env/Caddy, loopback-only PostgreSQL, no unexpected externally bound TCP service, key-only SSH/root login disabled, reviewed data mount, synchronized clock and healthy guest agent.
