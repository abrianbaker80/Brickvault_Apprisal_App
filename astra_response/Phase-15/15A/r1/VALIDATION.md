# Actual validation and limits — 2026-10-08

| Check | Actual evidence |
|---|---|
| Backend | 13 new parser/model/schema units passed; affected Ruff/format and strict mypy passed |
| PostgreSQL | 15 initial selected cases passed in 12.01s; added real multipart-limit case exposed a handler mismatch, passed in 0.60s after root fix; total 12 new cases + 4 relevant existing replay/conflict/shared-original regressions |
| Owned TEST cleanup | Every run, including the failed probe, removed its exact one recorded database; zero leftovers; prior TEST container state restored; volumes preserved |
| Frontend | 25 focused adapter/review/auth-boundary/queue cases passed; final high-water correction then passed the targeted 8-case review set; affected TypeScript/ESLint/Prettier passed |
| Native | 16 JUnit cases passed with zero errors/failures/skips; lint has 0 errors and 19 existing resource/layout/version warnings |
| Contract | OpenAPI/TypeScript regenerated; contracts:check passed; no migration |
| Build | Sanitized Vite android-qualification bundle and Capacitor sync passed; final build repeated only after the high-water source correction; offline Gradle assembleDebug passed |
| Artifact | APK package/min/target/compile/Share filters inspected; all 8 packaged web files match final build; backup/cleartext/native HTTP-cookie overrides disabled; only public TEST certificate, no key/env/keystore/pfx entry |
| Documentation | 475 local Markdown file links across changed docs resolve; task whitespace and reverse patch reconstruction pass |
| Review | One independent source-review cycle passed after lifecycle, provider-failure, failed-item removal and high-water corrections |

No complete legacy suite or accepted Phase 9/other physical qualification was rerun.
The existing Starlette/httpx/AnyIO warnings remain visible. Native lint warnings did not
cause accepted versions/resource modernization. The existing JUnit dependency was fetched
when absent from cache; declared versions and dependency files were unchanged.

The old localhost TEST certificate had expired. A fresh TEST-only certificate/key was
generated in ignored private-ACL storage and checked for localhost/validity. Only the public
certificate entered the APK. No device/system trust store changed, and the prior accepted
APK remains byte-preserved. APK/source receipt is [recorded here](apk-receipt.json).

Main HEAD remains the approved planning checkpoint, index empty; all 31 implementation/
documentation changes remain uncommitted. The three protected dirty files retain:

| Protected file | SHA-256 |
|---|---|
| AGENTS.md | f0a354ed80f631910f4cdcb64729209ef4758de441f3eaaf509da49395f969b4 |
| services/api/tests/integration/test_catalog_search.py | d06965d560361a06b7a33647efa5b9b34829f8c34d5d912226d9cd5b3645abf7 |
| services/api/tests/unit/test_catalog_parser.py | 0251b5c358cd37de9e07e2cbdfb44913752cade7050d9eb1b3a885f57d27a041 |

Only sanitized artifacts under this new r1 tree are published. Full unrelated historical
docs, private keys, raw TEST logs/credentials, device serials, image/listing bytes and local
secret paths are excluded. Code snapshots use LF UTF-8; inventory hashes name that normalization.
The patch includes complete changed hunks plus new source/tests/docs relative to the local
planning checkpoint, and is verified against that exact checkout. It does not apply itself
to remote main. Previous review trees and remote main are preserved.
