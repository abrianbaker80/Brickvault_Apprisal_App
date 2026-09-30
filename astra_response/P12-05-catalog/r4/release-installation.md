# Release identity and installation scope

Local retained artifact verification **PASS**; no build or rebuild.

| Identity | Exact accepted value |
| --- | --- |
| Release | `p12-05-catalog-repair-r1` |
| Source ID | `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344` |
| Manifest SHA-256 | `02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36` |
| Wheel SHA-256 | `a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6` |
| Accepted wrapper raw SHA-256 | `812f505508774bd6d6a040795d8076207ebe79f7ea5c041548e45f75a56fb339` |

The normal release verifier checked the reviewed manifest and every listed
artifact's byte size/SHA-256. The wrapper's raw bytes remain the accepted bytes.
Installed repair dependency/module hashes, wrapper presence, migration graph and
no-pending-migration verification are **UNRUN**: installation never began. Current
production remains r6; its installed migration/admin/health admission passed.

## Required approval contract discrepancy

Step 4 requires the detached root-owned repair approval to bind the exact failed
predecessor run and candidate. The accepted
[approve_repair_release validator](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/files/scripts/production_catalog.py#L231-L260), lines 231–260, permits only:

- `database`
- `migration_head`
- `predecessor_release_id`
- `predecessor_release_manifest_sha256`
- `purpose`
- `release_id`
- `release_manifest_sha256`
- `source_manifest_sha256`
- `source_provenance_sha256`
- `source_version`

Its exact-field comparison rejects any extra field. Neither failed-run nor
candidate identity is represented. The accepted `recover-failed` command has
explicit identity arguments, but that is separate from the required detached
approval binding. No approval was created, no identity values are published, and
no additional field or companion approval was introduced to bypass the contract.

The requested continuation forbids a new source/deployment repair and requires
stopping on such a discrepancy. The conflict was found during preparation before
Step 3. The exact accepted artifact remains retained and unchanged. This stop is
not an artifact-unavailability determination.
