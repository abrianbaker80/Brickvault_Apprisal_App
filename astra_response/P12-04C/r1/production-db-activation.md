# Production database activation state

VM 115 was verified against its pinned target identity before mutation. Ubuntu 24.04.5, PostgreSQL 18.6 on the reviewed data mount and loopback-only port 5432, guest agent, clock, SSH, inactive API/no listener, absent Caddy, and both accepted backup repository identities passed the relevant checks.

Hash-pinned release `p12-04c-r3` was installed under `/opt/brickvault/releases/p12-04c-r3` and selected through `/opt/brickvault/current`. Source ID: `abb75b857c38212837b2f559aa58adebb5832295e4aab17acad6fac4947ccb0e`; manifest SHA-256: `aef807e362b162700d9df46573a7bd519034c5c73f9c876181061df98ae2d54f`; API wheel SHA-256: `06aba11e7004b3f2ab8d79848c60ef2d3e4690f4b5f2509a8d2ce9a779bef521`. Hash-pinned transfer, installed-wheel import, admin/backup CLI and migration graph passed. The API remained disabled/inactive.

The root-owned protected production descriptor was generated on VM 115 with distinct owner/runtime database credentials and an ownership marker; none was printed or transferred. Guarded preflight passed before `provision-db`. The exact `brickvault_appraisal_prod` database and owner/runtime roles exist with the reviewed role attributes, marker, no memberships, PUBLIC revocation and runtime database CONNECT. There is no migration revision and no application principal.

The backup service and timer definitions were installed and passed `systemd-analyze verify`. The timer stayed disabled/inactive. The first backup service start failed; see [real backup evidence](real-backup-evidence.md). No subsequent production activation step ran. The corrected local unit has **not** been installed. No database object was deleted or reset.
