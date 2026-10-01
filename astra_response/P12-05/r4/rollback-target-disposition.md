# Accepted rollback target correction

Accepted blocker [r3](../r3/REVIEW.md), publication
`fb9c34ded36d0789d9676f20b00f95ae4ea054ff`, is preserved as dated evidence.
Brian explicitly rejects p12-04d-r1 for this gate: it predates P12-04E operational
hardening and cannot meet the installed current-pointer service/hook contract.
Its bytes remain immutable. The approved immediate operational predecessor is r6:

- Release: `p12-04e-r6`.
- Source ID: `00c719ac356f881c9929909a22f683831235f222939d28c8892747c8898558f5`.
- Manifest SHA-256: `9667d1f64f9a418647c0dc30a6d3a2525685d603ab3d930e8a3b854df0ba781d`.
- Forward remains `p12-05-catalog-repair-r1`, manifest SHA-256
  `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`.

Both exact 36-file manifests passed hashes/sizes. Both API interpreters/static
builds work and expect 0016; 49 migration artifact files are byte-identical.
Installed systemd service/timer/drop-in text was scanned for current-pointer paths.
Seven referencing files resolve every required r6 dependency: API directory,
Python/backup entry points, production health, complete-run retention, Python
maintenance and operational alerts. Operational script bytes match forward.
Both venv Python links resolve to the same root-owned, non-writable system
interpreter; their venv locations remain under their exact release. The installed
root-owned renewal hook matches both release hooks byte-for-byte.

Using the actual r6 interpreter and runtime role, PostgreSQL-enforced read-only
search/detail succeeded against current generation 1 and 28,278 sets. Exact
75331-1 resolved to The Razor Crest. Authoritative pointer generation was read
directly; the unchanged pinned appraisal response has null generation. No source
or admission contract was changed to manufacture another response. Security,
catalog, Watchlist, Settings and session metadata stayed unchanged during this
read-only proof; no importer/recovery/provider/user/session mutation occurred.

Final filesystem corroboration verified all 169 installed r6 package files against
its exact wheel and its interpreter/module locations. The repaired runtime's
170 installed package files likewise matched its exact wheel. Both releases
remained unchanged. [Static](r6-static.json) and [read proof](r6-read-only.json).
