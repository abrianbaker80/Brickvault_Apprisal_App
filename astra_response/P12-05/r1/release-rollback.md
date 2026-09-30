# Immutable release rollback — UNRUN

Target remains the previously accepted p12-04d-r1; no superseded E intermediate
was selected. The production current pointer and absolute immutable web directory
were not changed. r6 remains healthy with the expected manifest. Rollback/forward
requires the temporary authenticated Watchlist persistence probe, which could
not be created without a production catalog. No API restart or timer pause ran.
