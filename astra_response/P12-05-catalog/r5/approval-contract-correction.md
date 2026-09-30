# Accepted procedural correction

r4's stop was correct under its preceding prompt. That prompt incorrectly required
the live failed-run UUID and failed-candidate UUID inside a detached STATIC repair
approval. ChatGPT removed ONLY that requirement; all existing production
authorization and exact-once boundaries remain valid.

The [accepted validator](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/3d17ff6da2b0ec7748ea5a886a1341fbf583aaea/astra_response/P12-05-catalog/r2/files/scripts/production_catalog.py#L231-L260) requires exactly these ten keys:
purpose, database, release_id, predecessor_release_id,
predecessor_release_manifest_sha256, release_manifest_sha256, source_version,
source_manifest_sha256, source_provenance_sha256 and migration_head. Native
admission accepted a protected ten-field approval with SHA-256
`47fbe031080b49abe0738acdd91de3a3d357ebe89bc5086b9f3c90f7fc42fec6`. No extra keys or live IDs were added.

Typed root-only recover-failed UUID arguments, protected admin/source/release/
migration contracts, operations lock, conflict checks, admin verification and
native recover_failed exact-state validation bind the actual run and candidate
at execution. Admission proved the only failed source/candidate, exact fingerprint,
12 files and 1,898,466 owned staging rows, zero canonical/validation/activation,
NULL pointer/generation 0 and no competing attempt before mutation.

The exact wrapper raw SHA-256 remains `812f505508774bd6d6a040795d8076207ebe79f7ea5c041548e45f75a56fb339`. No wrapper
patch, approve_repair_release change, schema change or rebuild was needed.
Earlier [r4 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/4aca962f789d6d242d503d7d5892e7e9e772f74b/astra_response/P12-05-catalog/r4/REVIEW.md)
and [accepted r3 closeout](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/9f24d1e541da3b173cfe3ea7304e269f37d5c17c/astra_response/P12-05-catalog/r3/REVIEW.md)
are preserved as historical evidence. Protected UUIDs/configuration are withheld.
