# Bounded Phase 13B validation

## Results

Seven unique cases: create/list/detail and zero price; selection identity/high-water;
max concurrency 2; partial success/duplicate/same-file retry; conflict refresh/remove/
reselection; multipart session transport and generic/network normalization;
readable UI conflict/local failed removal. Initial run six PASS/one fixture failure.
After client construction and jsdom/native Request fixture correction, the affected
two-case subset PASS (five deselected). Other scoped lint typing corrections followed.
No repeated broad campaign; binary bytes qualified in real Chromium, not jsdom.

Commands actually used (existing Node runtime; sanitized frontend environment):

```text
node node_modules/vitest/vitest.mjs run src/Listings.test.tsx                 # cwd apps/web
node node_modules/vitest/vitest.mjs run src/Listings.test.tsx -t 'normalizes|shows a readable'
node node_modules/typescript/bin/tsc --project apps/web/tsconfig.json          # PASS
node node_modules/eslint/bin/eslint.js --max-warnings 0 <six affected TS/TSX files>
node node_modules/prettier/bin/prettier.cjs --check <seven affected web files> # PASS
node node_modules/vite/bin/vite.js build                                     # cwd apps/web; PASS once
python -m ruff check --config services/api/pyproject.toml services/api/src/brickvault_api/api/static.py
python -m ruff format --check --config services/api/pyproject.toml services/api/src/brickvault_api/api/static.py
python -m mypy --config-file services/api/pyproject.toml services/api/src/brickvault_api/api/static.py
```

Final affected ESLint PASS; formatter PASS; frontend types PASS; Vite 60 modules,
normal frontend build PASS. One changed Python module Ruff/format/mypy PASS.
No dependency installation/change, contracts regeneration, backend pytest, migration
test campaign, release packaging or broad frontend suite. Backend shell routes were
added after an actual initial `/listings` 404; disposable API restarted once before
flows began. Normal fresh TEST schema provisioning is browser setup only.

## Real browser flows and stop condition

Codex in-app Chromium, existing owned TEST PostgreSQL 18 harness, separate disposable
DB and synthetic filesystem blobs. Desktop 1440x900; mobile 390x844. No production.

1. Sign in with generated disposable owner; create listing (USD zero); choose three
   valid synthetic PNGs; observe two uploading/one queued. All succeed at positions
   0,1,2. Original decodes 640x480; thumbnails 512x384. Reload same detail and reopen
   from listing card: metadata, three-image count/preview and persisted order survive.
2. Select two more files at positions 3,4. A TEST-only response fault replaces the
   fourth upload's real committed 201 with one synthetic 503 TRANSPORT_ERROR. The
   other file stays uploaded. Explicit retry sends only the failed same attempt and
   recovers its stored uploaded result. Six requests total; peak active two; no
   remaining active uploads. Read-only counts: one listing, five listing_images,
   exactly five upload_receipts. The retry adds no sixth saved image/receipt.
3. Cheap mobile smoke at 390x844: gallery wraps with ~163px-wide/174px-high touch
   buttons, readable queue/failure/actions and no consequential overflow. Desktop
   likewise fits. Screenshots inspected privately; no extra browser permutation.

Stop condition met. No PWA/Android/native, recognition/provider, production or
shipping qualification. Proposed privacy policy remains unapproved.

## Cleanup and Git boundary

Browser signed out/closed; viewport reset. Owned API process/listener stopped,
disposable DB dropped, synthetic blob store and temporary credential file removed.
Ledger status passed, leftovers [], prior TEST instance stopped state restored.
Original persistent TEST volume retained. Earlier pre-flow startup cleanup likewise
left no resources. Synthetic fixtures/screenshots remain ignored local evidence.

Main HEAD `d14002e244434123dc68b57aefda004a00aa8e89`, unpushed; 13B edits uncommitted, index empty. Three protected
files hash-identical and unstaged. Exact 11-file source inventory and complete
zero-context patch reverse-apply PASS; Markdown links main: 244. Separate
astra-response publication changes only this r1 prefix, preserving all earlier reviews.

Source raw SHA-256 values frozen for publication:

| File | SHA-256 |
|---|---|
| CODEX_WORKFLOW.md | 44238b61b4681dacc2b0f7b2a1d52e6413a73d6ad49f7dbb30cc8e63608a2f6a |
| apps/web/src/App.tsx | 49e30a863e6d6746db81389b75221d5bd751cea7c040679cf2064f034317a303 |
| apps/web/src/AppShell.tsx | a75d07a29322263f0ce12fb4a5f57ef15ccc783d598c60470b75b6af05ace783 |
| apps/web/src/Listings.test.tsx | f2727103fe88b4499a18234dc8035fcf1ee644a5d4ff396488a90a66c8d3fbcc |
| apps/web/src/ListingsPage.tsx | 1402b6d4e990c308d603d4d564f470b1f460dc05876c1c664bd0dd80cd436a5a |
| apps/web/src/listings-api.ts | 2839310412f0cda0e72ea1eded1690e12242ec5159d4b7dc0be45ce7878dd45a |
| apps/web/src/styles.css | ab4882b716d2465e4d43bda1803bdb456e4e35909e11698c12d6647e8cbf856e |
| apps/web/src/upload-queue.ts | c773a21cb86bf240bd3ee117213df4e0e7e10ffee53719557b97da76b8e7fc70 |
| docs/ROADMAP.md | 456716044b96b76800ab79dadc90d5046c100286c2ffada759e8dddcdd9ed18c |
| docs/plans/103-phase-13-image-ingestion.md | b1b2b779f1e65cdd466a86904613a29de8f087632ff49a9b3dccb61d44c59404 |
| services/api/src/brickvault_api/api/static.py | 2a46afa14b0df2a8ca6bcf8f46bc89c59aeab524927444aaed1a126aef594ee9 |
