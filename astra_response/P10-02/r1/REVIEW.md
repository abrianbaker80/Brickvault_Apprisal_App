# P10-02 — bounded local database backup/restore proof

**Verdict: PASS for this bounded TEST-only proof; awaiting ChatGPT review.** Phase 10
remains IN PROGRESS. One real PostgreSQL custom dump restored representative private
records from one run-owned disposable TEST database into another. The focused test
authenticated and read the restored records through normal runtime service paths.
This is not production disaster-recovery or release qualification.

## Scope and implementation state

- Baseline and final implementation HEAD: `0621ee095eec60fa4a4551d54ce10d58cdee9ce4`
  on `main`; no implementation commit or push. Remote `main` was
  `5c57731c7e15abdae5d6d1e5a35e46e602bc3618` at publication preparation, so
  the implementation baseline was unavailable there.
- Initial index: empty. Final implementation index: empty. Initial working tree had
  only the three protected modified files listed below. Final working tree retains
  those three plus the seven uncommitted P10-02 files in this package.
- Protected and unstaged, byte-for-byte SHA-256 verified before and after:
  `AGENTS.md` (`f0a354ed80f631910f4cdcb64729209ef4758de441f3eaaf509da49395f969b4`),
  `services/api/tests/integration/test_catalog_search.py`
  (`d06965d560361a06b7a33647efa5b9b34829f8c34d5d912226d9cd5b3645abf7`),
  `services/api/tests/unit/test_catalog_parser.py`
  (`0251b5c358cd37de9e07e2cbdfb44913752cade7050d9eb1b3a885f57d27a041`).

## Exact task file inventory

| Repository path | Change and rationale |
| --- | --- |
| `scripts/recovery_runner.py` | New TEST-only runner. Reuses the existing local instance, exclusive lock, ownership markers, provisioning, migrations and guarded cleanup. Records two exact databases before operations, refuses populated restore targets, uses installed `pg_dump`/`pg_restore`, supplies the local bootstrap password through process stdin, reasserts runtime grants, and restores the prior TEST container state. Dump stays under ignored `.local/database/backups` and is removed. |
| `services/api/tests/integration/recovery_proof.py` | New explicitly selected integration proof using the existing synthetic market/forecast fixtures. Verifies restored principal identity, Watchlist target/note/revision, immutable saved forecast and idempotent replay, readiness, runtime SELECT grants, and unchanged selected source rows. Its filename keeps it out of the ordinary integration directory collection, which lacks this runner's two-database fixture. |
| `scripts/test_recovery_runner.py` | New seven focused refusal cases for TEST-only selection, distinct recorded names, owner/run identity and dump-path identity. |
| `scripts/tasks.mjs` | Adds the root-only `test:recovery` dispatch through the installed Python environment. |
| `package.json` | Exposes `pnpm test:recovery`; no dependency or lockfile change. |
| `docs/LOCAL_DEVELOPMENT.md` | Adds the repeatable local procedure, cleanup behavior, 32 MiB fixture bound and backup limits. |
| `CODEX_WORKFLOW.md` | Adds only the current P10-02 implemented-for-review note; standing rules and history remain in the checkout. |

`changes.patch` is the cumulative, task-scoped unified diff against the stated
baseline, including all three new files. `source/` contains complete final versions
of changed implementation/test/entrypoint files. `base/` holds exact baseline blobs
for the three changed tracked files needed to reconstruct their patch remotely.
The baseline `CODEX_WORKFLOW.md` is intentionally omitted because it contains
private history; its narrow documentation hunk remains in `changes.patch`. This
is the only reconstruction gap for a reviewer without the local baseline.
`context/` contains the unchanged owned-database helpers and selected, labeled
synthetic fixture source excerpts needed to evaluate the proof. No dump, verifier,
credential, actual private
record, dataset or `.local` artifact is included.

## Evidence and limits

- **New local evidence:** One final Windows rehearsal passed (`1` focused integration
  test). It used the verified existing local TEST container and PostgreSQL 18.6
  image. The runner reported two databases removed, dump removed, no leftovers and
  TEST service returned to its initially stopped state. Seven focused guard tests,
  targeted Python/JavaScript format, lint and type checks, and `git diff --check`
  passed. Exact commands and the initial corrected failure are in `validation.txt`.
- **Reused evidence:** Existing accepted ownership guards, fixture/service paths,
  migration/grant logic and P10-01 acceptance were read and reused; no historical
  suites or release checks were rerun.
- The proof covers one small synthetic database and selected private records. It
  does not cover production data volume, retention, encryption, off-host storage,
  role/configuration backup, crash recovery, full static-loader behavior, Android,
  providers or a complete Phase 10 release. The dump contains password verifiers
  while it exists. A forced runner or machine termination can leave a recorded
  resource requiring exact ownership review before manual cleanup.

**Decision requested:** ChatGPT should accept or reject this bounded TEST-only
backup/restore proof and its review package. Keep Phase 10 open either way.
