# Bounded operational helper corrections

The immutable accepted application, wrapper, wheel and importer were not changed.
Ignored operational verification helpers needed these same-scope corrections:

- The installer verifier initially treated every lock entry as Linux-applicable;
  it was corrected to evaluate accepted platform markers and skip Windows-only
  tzdata. Verification continued read-only; installation was not repeated.
  Its small embedded command-escaping/stderr-handling errors were also corrected.
- The runtime helper initially passed positional arguments to the Pydantic Owner;
  it was corrected to use the documented keyword fields.
- Its zero-observation check initially assumed zero diagnostic references. The
  accepted projection includes unavailable unresolved_mapping references; those
  have no provider identity/fetched time and all amounts remain null. The helper
  now checks that meaning and the actual zero database observation count.
- Before reaching its physical-state assertion, source inspection identified an
  incorrect helper expectation for whole-set identity. The accepted COMPLETE_SET
  representation does not inspect exploded contents; it admits the known set
  identity while retaining the seller-box limitation. Exploded representations
  remain UNKNOWN/unadmitted. The helper was aligned with that accepted contract.

Final installed-runtime checks passed without application source mutation,
provider dispatch, owner-state writes or any extra production recovery/import/
activation/backup. Read-only qualification was rerun only to correct these helper
invocation/assertion errors. They were not importer/retry failures. The one
authorized production retry and activation each passed on their sole invocation.
