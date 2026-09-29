# P12-04A repository changes

This slice adds production administration and release tooling plus an inactive
API service definition. It does not add a schema migration, change API routes,
create production data or authorize the next deployment checkpoint.

## Exact task inventory

### Application and packaging

| File | Change |
| --- | --- |
| `services/api/src/brickvault_api/production_admin.py` | New guarded CLI with preflight, database provisioning, packaged migration, runtime grants, owner bootstrap and verification; protected input, ownership checks and credential logging controls. |
| `services/api/src/brickvault_api/persistence/runtime_grants.py` | New shared module containing the existing enumerated runtime grants and role-name validation. |
| `scripts/database.py` | Calls the shared grant module instead of carrying a separate copy of its SQL policy. |
| `services/api/pyproject.toml` | Registers the `brickvault-production-admin` console entrypoint. |
| `scripts/package_api.py` | Requires admin/grant modules in the wheel and verifies imports, console entrypoint resolution and help from an independent installed environment. |

### Release, tests and deployment definition

| File | Change |
| --- | --- |
| `scripts/release_manifest.py` | New source digest, release staging and manifest verification commands; exact source inventory, wheel/source comparison, accepted frontend verification, locked requirements export and artifact hashes. |
| `scripts/test_release_manifest.py` | Focused tests for artifact mutation, external digest/identity checks, unexpected frontend files, source inventory boundaries and stale or incomplete wheel contents. |
| `services/api/tests/unit/test_production_admin.py` | Thirty synthetic cases covering the admin contract, refusal paths, recovery receipt and credential handling. |
| `scripts/production_admin_secret_proof.py` | Explicit integration proof using one disposable local PostgreSQL 18.6 container; tests real SCRAM authentication and credential-free success/error logs, then removes only its owned container. |
| `deploy/systemd/brickvault-api.service` | API unit running as `brickvault`, bound to loopback port 18080, dependent on PostgreSQL and required mounts. Its environment file is mandatory; filesystem and privilege restrictions are declared. The unit is prepared for later authorized startup. |

### Documentation

| File | Change |
| --- | --- |
| `docs/plans/094-production-foundation.md` | New P12-04A plan and execution record: foundation scope, package provenance, data storage, admin design, validation, deviations and remaining gates. |
| `CODEX_WORKFLOW.md` | Current P12-04A checkpoint and later authorization boundary. |
| `docs/ROADMAP.md` | Current Phase 12/P12-04 status and checkpoint boundary. |
| `docs/plans/091-production-runtime-and-deployment.md` | Status reference to the current foundation checkpoint. |
| `docs/plans/092-exact-infrastructure-pre-mutation-review.md` | Status reference preserving the accepted infrastructure review. |
| `docs/plans/093-base-vm-provisioning.md` | Status reference preserving accepted P12-03 evidence and its historical records. |

These are **16 task files**. The pre-existing dirty `AGENTS.md`,
`services/api/tests/integration/test_catalog_search.py` and
`services/api/tests/unit/test_catalog_parser.py` are protected, excluded from
the task patch and preserved separately. No dependency lockfile change is part
of this inventory.

## Source ID and artifact identity

The release manifest records two different source identifiers:

- `source.commit` is the baseline Git HEAD. It identifies the committed base;
  it does not claim that the uncommitted P12-04A implementation is committed.
- `source.reviewed_id` is the SHA-256 emitted by `release_manifest.py source-id`.
  It binds that HEAD and the exact current bytes of a literal 14-file input
  list. It is not an arbitrary release label or a hash of the whole worktree.

The input list contains the ten application/build/test/deployment files above,
plus unchanged `package.json`, `apps/web/package.json`, `pnpm-lock.yaml` and
`services/api/uv.lock`. The digest includes a format/version prefix, HEAD, then
each sorted path, byte size and file SHA-256. Source changes outside this list
are refused, except for the six specified status documents and three protected
dirty files. Those nine files do not enter the source digest. Unsupported Git
states, including staged changes, deletion, rename and unresolved conflicts,
are refused. Status documents are excluded because they record the resulting
release identity; protected-file preservation is checked independently.

Release creation compares the supplied source ID before and after staging.
The wheel's package-file inventory and bytes must match the checkout package
source; the accepted frontend verifier must pass. Production dependencies are
exported offline from the unchanged lockfile with pinned repository-local
uv 0.12.10. The bundle contains the API wheel, sdist, hashed requirements and
the supported web files.

`manifest.json` records the release ID, baseline commit, reviewed source ID,
uv version and each artifact's path, size and SHA-256. Verification requires a
separately supplied reviewed manifest SHA-256 and exact release/source IDs,
checks every artifact and rejects unlisted files. File/directory checks reject
symlinks, junctions and nonordinary files; artifact files must have one link.
The source digest binds the reviewed inputs; the manifest digest binds the
actual staged bytes. Neither alone substitutes for build or runtime testing.

## Production boundary

The CLI implementation and disposable proofs do not create anything in the
VM's production database cluster. No BrickVault production database, owner or
runtime database role, ownership marker, account principal, production
credential descriptor or recovery receipt has been provisioned on VM 115.
The API environment file remains absent and the service remains inactive.
Backup destinations, recovery qualification, production secrets, first
migration/bootstrap, Caddy, DNS/TLS and later application acceptance retain
their separate approval gates.
