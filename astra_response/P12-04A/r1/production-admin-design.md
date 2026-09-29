# Production administration design — P12-04A

## Boundary

`brickvault-production-admin` is a packaged administration entrypoint for a
later authorized production-data checkpoint. Its six commands are implemented;
none was executed against VM 115 in P12-04A. The production database, database
roles, ownership marker, protected descriptor, recovery receipt and application
owner principal have not been created there. Installing the CLI does not satisfy
the later backup, migration, bootstrap or exposure gates.

## Exact target and protected input

| Contract | Required value or check |
| --- | --- |
| Purpose | `production` |
| Database | `brickvault_appraisal_prod` |
| Schema owner role | `brickvault_appraisal_prod_owner` |
| Runtime role | `brickvault_appraisal_prod_runtime` |
| Credential connections | Exactly `127.0.0.1:5432`; canonical production URLs only |
| Maintenance connection | Local `/var/run/postgresql` socket, port 5432, OS root mapped to PostgreSQL `postgres` through peer authentication |
| Cluster identity | PostgreSQL 18, primary rather than recovery mode, `listen_addresses=127.0.0.1`, expected database and session/current role |
| Ownership marker | `brickvault-appraisal:<32 lowercase hex>:<32 lowercase hex>`; exact database comment, with the corresponding `:role` comments on both roles |
| Default descriptor | `/etc/brickvault/production-admin.json`, root-owned regular file, mode 0400 or 0600 |

Descriptor parsing rejects duplicate or additional keys, development/test
targets, alternate names or ports, identical owner/runtime passwords and
malformed markers. Each password must satisfy the existing canonical
64-character lowercase hexadecimal URL contract. Input directories must be
root-owned and not writable by group or others; symlinked directories and a
symlinked final file are refused. Files are size-limited. Inherited PostgreSQL
settings and application environment overrides are rejected.

Existing state must have the exact database owner and marker. Both roles must
be ordinary login roles with no superuser, database/role creation, replication
or RLS-bypass privilege, and no role memberships in either direction. PUBLIC
database access is revoked. Runtime has database CONNECT and schema USAGE,
without database/schema CREATE or TEMPORARY rights.

## Commands and sequencing

| Command | Behavior and gate |
| --- | --- |
| `preflight` | Read-only; recognizes either wholly unused names or an existing database with verified ownership, schema and runtime identity. Partial state is refused. |
| `provision-db` | Creates only the unused exact database and two roles; refuses existing or partial state. Creates no application schema or principal. Partial failure is retained for review rather than automatically deleted. |
| `migrate --recovery-proof <protected-file>` | Requires established ownership, schema/runtime identity and a current recovery receipt matching the pre-migration revision. Uses only the installed package's Alembic graph, advances to its head and checks the resulting revision in the transaction. An already-current database is refused as a no-op. |
| `grant-runtime --recovery-proof <protected-file>` | Requires the packaged migration head and recovery receipt, then applies the shared, enumerated runtime grant policy. |
| `bootstrap-owner --recovery-proof <protected-file>` | Requires the packaged head, empty principal table, runtime privilege checks and recovery receipt. Reads and confirms a password through hidden local TTY input and uses the existing account provisioning service. Existing principals are refused. |
| `verify` | Read-only and repeatable; checks ownership, packaged revision, one private owner principal and the defined core runtime privilege checks. |

The recovery receipt is a protected root-owned JSON file, bound to the exact
database and ownership marker. It contains two distinct snapshot digests and a
UTC verification time no older than 24 hours. Migration additionally matches
the receipt's saved revision list to the current pre-migration state. Grants
and bootstrap allow the same pre-migration receipt after the schema advances.
The receipt records an operator's verification of both recovery copies; it
does not create backups, establish encryption or prove restoration itself.

Runtime grants use explicit known tables, columns and functions. The shared
policy is extracted from the existing local database helper, avoiding separate
production and local grant implementations. It grants no default privileges
on future tables. The `verify` command's core privilege checks are not a
comprehensive database security audit.

## Credential and log protection

The CLI has no plaintext password argument. Database credentials come from the
protected descriptor; the application owner's password comes from hidden TTY
input. Descriptor representations and CLI errors omit secret values, hashes,
full credential URLs and underlying driver messages.

Before credential-bearing SQL, a privileged peer session refuses unreviewed
preload libraries, sets PostgreSQL's standard statement/error/parameter/debug
logging and activity controls, and verifies their effective values. It also
requires SCRAM-SHA-256 with a bounded iteration count. Role provisioning creates
salted SCRAM verifiers client-side, so plaintext database passwords never enter
SQL. Verifiers remain sensitive and receive the same logging protection.

Application owner bootstrap opens a guarded peer session, checks database
ownership, applies logging controls, switches the effective role to the schema
owner, then rechecks identity, logging controls and migration head. The existing
authentication service hashes the password with Argon2 and serializes account
creation through its established transaction. No password reset command is
added by this slice.

## Verification and its limits

- **30 focused unit tests passed.** Coverage includes canonical target and
  ownership checks, partial-state refusal, recovery receipts, CLI redaction,
  SCRAM formatting, logging readback refusal, preload refusal, guarded owner
  role switching and bootstrap sequencing. These use synthetic inputs.
- **A separate real PostgreSQL 18.6 proof passed** in a uniquely owned local
  Docker container using the repository-pinned image. Correct-password SCRAM
  login succeeded and incorrect-password login failed. Role creation and a
  duplicate-role error were exercised; after an effective owner-role switch,
  account-hash insertion and a duplicate-row error were exercised.
- The proof began with deliberately verbose logging and confirmed harmless
  success/error control markers. All five sensitive test values were absent
  from 104,226 bytes of captured server logs. Only a sanitized receipt was
  retained. The proof container was removed and its loopback port released.
- The real proof calls the credential helpers against disposable PostgreSQL;
  it is not execution of the full production CLI sequence on VM 115. No
  production migration, account bootstrap, backup restore or application
  acceptance is claimed.

The package builder checks that the wheel contains the admin and grant modules,
imports them from an independent installed environment and resolves the console
entrypoint. The release's actual build and installation results are recorded
separately in this review package.
