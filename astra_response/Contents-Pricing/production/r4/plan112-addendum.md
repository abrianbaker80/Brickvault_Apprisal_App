## 24. Sample-count projection corrected and deployed — 2026-11-17

Brian accepted the r3 live pricing check and authorized only this metadata correction,
focused source/TEST verification and a compatible backend-only update. Contents now
projects sample_count from normalized market_observation.occurrence_count. Sold and
Stock remain tied to their exact request; total_quantity and selected quantity are
not substituted. Null, recorded zero and normal eligibility suppression are preserved.
No contract, frontend, price, normalization, mapping or accounting change was made.

Six focused synthetic PostgreSQL cases passed (Sold/Stock × positive/null/zero),
including stored-row projection, other-view isolation and display-expiry suppression.
Affected Python lint/format and production-module typing passed. A supplemental
test-module typing check found the same five pre-existing diagnostics as HEAD,
confirmed with a shadow-file baseline; no unrelated typing cleanup was included.
No broad Python/UI suite or web/APK build ran. Existing UI rendering was reused
and verified on the physical phone with the retained cached evidence.

Immutable backend contents-sample-metadata-production-r1 was staged and activated
on schema 0020; health passed and 25 data-table fingerprints were preserved. Manifest
SHA256 ca6533b25b409c3154383449faba890a1d6a15200d533294cfd49f6a604131ee.
It contains accepted feature f79e94092d272a050ced989eb1761b34320bdd28, the exact
accepted backup-stream amendment and this projection correction. Only contents.py
and wheel RECORD differ from the previous wheel; web assets/dependencies and the
installed APK remain unchanged. Prior immutable releases remain available for
same-schema rollback. Current recovery/deep-health checks reused qualifying prior
recovery evidence; no new backup, restore, schema operation or runtime upgrade ran.
Brian was warned before the controlled backend switch/restart.

The existing authenticated phone UI displayed Used/Sold sample 5 for idea106 and
sample 1387 for PART 3001 White 1, matching the corresponding stored occurrences.
The cached evidence remained fresh at readback: USD 26.78 and USD 0.10, with original
fetch times and expiry unchanged. Provider attempts 7→7, observations 6→6, refresh
operations 3→3 and targets 2→2; zero new provider calls or refresh operations. No
Confirm, Resume, discovery or credential probe occurred. Response color remains
unconfirmed by the part response; exact rolling-window boundaries remain unspecified.

Phone left signed in on Contents; owned inspection forward removed. All 22 original
pending paths, protected files, stopped capture work, prior publications/private
evidence and accepted backup source/tests are preserved. Prior Plan 112 bytes are
preserved as a prefix. Correction/tests, backup amendment/tests and this plan remain
uncommitted; main remains at accepted f79e940, index empty and unpushed. The backup
deadline correction still does not establish the historical failure cause.
Sanitized correction diff, exact hashes, focused results and backend/readback evidence
are published only under astra_response/Contents-Pricing/production/r4/. Stop for review.
