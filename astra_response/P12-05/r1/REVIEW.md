# P12-05 — blocked production acceptance

**BLOCKED — production catalog unavailable. P12-05 is not READY or CLOSED.
Phase 12 remains IN PROGRESS.**

The independent Windows Google Drive-only real restore passed, including all 76
table counts, ownership/marker, migration, one owner, effective grants and recovered
database credential authentication. All disposable plaintext was removed and live
production remains healthy on the accepted r6 release.

That restore and a read-only live comparison exposed the blocking prerequisite:
production has zero catalog sets/providers/snapshots and no active snapshot.
Installed number/name search returns catalog_unavailable. The required Set Detail
and temporary Watchlist workflow cannot run. No production catalog import, provider
onboarding, source fix or synthetic substitute was performed.

## Review decision needed

Authorize a separate bounded production catalog activation using an accepted
nonsynthetic source with confirmed data/provider rights, and the evidence needed
for the selected economics workflow. Resume remaining P12-05 acceptance only after
that prerequisite is accepted. No Phase 13 work is included.

## Evidence

- [Plan 099](Plan-099.md)
- [Browser/auth blocker](auth-browser.md)
- [PWA gates unrun](pwa-acceptance.md)
- [Android gates unrun](android-acceptance.md)
- [Real off-host restore and cleanup](offhost-restore.md)
- [Rollback gates unrun](release-rollback.md)
- [Startup configuration and cold-start gate](disaster-boot.md)
- [Healthy blocked-run state](final-security-operations.md)
- [Validation](validation.txt) and [sanitized operation record](commands.txt)
- [Exact table counts](restore-table-counts.json), [sanitized evidence](sanitized-evidence.json)
- [Cumulative documentation patch](cumulative-documentation.patch)
- [Changed files](changed-files.txt), [hashes](changed-file-sha256.json), [exact copies](files/)
- [Minimal accepted context](context/accepted-p12-04.md)

## Scope and preservation

Main remains uncommitted at 5c673e81a4f1caa13a0909a746d6ba0fffca075e, index empty,
with the three protected dirty files unchanged and unstaged. Only Plan 099 and
minimal CODEX_WORKFLOW/ROADMAP status additions changed. No application/deployment
source changed. The isolated review branch adds only this r1 package.

Exactly one new normal dual backup ran because the prior configuration was stale;
the final acceptance backup did not run. Four disposable restore attempts narrowed
an evidence-helper ACL representation mismatch; expanding PostgreSQL default ACLs
proved all effective privileges equal. No production change was used to make it pass.
Browser/auth, PWA, Android, rollback/forward, guest cold start and final backup
remain UNRUN. This package is a blocker review, not final production acceptance.

Exact documentation copies keep repository-relative links; resolve those against
the complete accepted main tree plus this cumulative patch. The standalone plan
uses commit-pinned source links. No secret/private identifier/plaintext recovery
artifact is included.
