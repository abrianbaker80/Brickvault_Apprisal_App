# Focused validation and evidence boundaries

Accepted [13A r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/f59328e7bbe05dce9316940fc41f046a5a55b142/astra_response/Phase-13/13A/r1/REVIEW.md) and [13B r1](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/ed32c83b9b73a4bf987c3246c5fe5f301a32d108/astra_response/Phase-13/13B/r1/REVIEW.md) are reused. The 13B closeout reran only Git inventory/diff/whitespace/protected checks.

Eight unique focused Python seam cases passed; the final affected run was 8 passed in 0.47s. A prior passing run preceded the added ownership/context inventory and its affected corrections; it was repeated only after those meaningful changes. One existing UI metadata case passed with terminology/navigation assertions; six unrelated cases were skipped.

| Case | What it proves | Boundary |
| --- | --- | --- |
| Legacy proof | Exact schema 2/0016, three artifacts, supported grant transition; incompatible revision refused | Synthetic receipt and mocked protected/readback inputs; actual proof/admission code |
| Combined proof | Schema 3/0017 requires all four artifacts | Same synthetic proof boundary |
| Malformed copies | Unknown/extra fields, missing destination, malformed hash and reused snapshot IDs refused | Pure real validator |
| Blob archive | Exact archive/extraction round trip; corrupt/missing source refused | Real disposable filesystem/tar; arbitrary fixture bytes, no image decoder |
| Unsafe archive | Traversal, symlink, missing, duplicate and corrupt members refused | Real disposable archives/filesystem |
| Mixed retention | Legacy/new admission and complete-run planning; two permanent pins and canaries preserved | Synthetic repository inventory; no live deletion or DEGRADED transaction |
| Pause recovery | Finally restores original active units after capture and stop failures | Real temporary journal; mocked systemd/root and Windows POSIX adaptation |
| Failed second sink | Actual producer/two-child stream fails closed | Real subprocesses and disposable file; no encrypted repositories |

Affected Ruff formatting/lint passed. Seven affected Python sources passed mypy with the Linux target and silent followed imports. Affected frontend ESLint, typecheck and Prettier passed. One final normal build succeeded, including locked wheel installation, migration graph/resources/entrypoints and frontend assets. Earlier pipeline attempts stopped in API packaging: an obsolete 0016 packaging assertion was corrected, then the already locked Pillow dependency was populated into the disposable packaging cache. No dependency version changed; no extra successful release or Android build was made.

Live evidence is recorded separately: one actual Linux publication/reuse/hash proof; guarded 0017 upgrade and runtime grants; one browser intake with three decoded images; normal encrypted combined service capture/readback; independent Drive-only restore and cleanup. The focused fixtures do not substitute for these gates.

No broad 13A backend, 13B browser, catalog/performance, API/frontend, Phase 12, PWA offline or Android campaign ran. No recognition, provider/model calls, source-URL fetch, native capture, dataset/export, delete/orphan repair, retention forget/prune, rollback/downgrade or newer-data restore occurred. The installed Android APK was not rebuilt or claimed updated. Phase 14 is not started.

A separate bounded read-only source review found no blocking defect. It ran no tests/builds and contacted neither production nor the browser.
