# Focused validation

2026-10-02, local source only. Existing Python 3.13 environment; no new dependencies.

- Six fixture tests: **6 passed in 2.96s**.
- After report-input integrity and test import typing corrections, two affected
  tests: **2 passed in 1.04s**. No broad suite rerun.
- Ruff check: passed on the five new package files and one new test file.
- Ruff format check: six files already formatted.
- Mypy strict, follow-imports=silent: success on six changed Python files.
- CLI help and real protected-directory initialization passed. Live `run` refused
  with `sealed_approval_required` before any provider connection.
- All local Markdown links in seven changed documents resolve in the application tree.
- Literal 13-file diff passes whitespace validation; patch application checked
  against a temporary index at the application base, without staging main.

Tests cover strict schema/malformed/refusal/truncation handling, exact namespace and
suffix resolution, ambiguous/invalid IDs, production-target refusal, unknown/mixed
results, preliminary metric denominators, completed-run replay, budget/call caps,
pre-dispatch reservation and interruption, lock exclusion, fixed-host HTTP failure
without retries, bounded timeout, redacted errors, real Windows private ACLs,
metadata stripping, selected-file preparation and approval/content integrity.
Network connections are prohibited in the fixture test file. Real catalog export,
provider entitlement/schema acceptance and recognition accuracy are not claimed.

A Windows ACL setup defect was corrected: isolate Windows PowerShell's module path
and write only the directory DACL, avoiding an unnecessary audit privilege request.
The actual ACL preparation/check test now passes; permissions were not bypassed.

No catalog/image-upload/migration/backup/PWA/browser/Phase 12/13 campaign, frontend
or Android build, production access/deployment, marketplace provider activation,
native capture or later-phase work was performed.

Main HEAD stays d839e51b65f9156e5829740c08d52b59be4c4ec4. Main index is empty.
Protected SHA-256 values remain:

- AGENTS.md: F0A354ED80F631910F4CDCB64729209EF4758DE441F3EAAF509DA49395F969B4
- test_catalog_search.py: D06965D560361A06B7A33647EFA5B9B34829F8C34D5D912226D9CD5B3645ABF7
- test_catalog_parser.py: 0251B5C358CD37DE9E07E2CBDFB44913752CADE7050D9EB1B3A885F57D27A041
