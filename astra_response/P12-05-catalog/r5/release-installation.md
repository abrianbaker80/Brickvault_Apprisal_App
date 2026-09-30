# Exact retained repair installation and switch

Release `p12-05-catalog-repair-r1`; reviewed source ID `33d1cd5d78e2069b6c61a864cd3ba4c6fa66cc094142f57db14cc9530aa1f344`; manifest SHA-256
`02c0cc06a49efe1718ffa2392c5cb88fe22e093328de22bdf4a53c3041333b36`; wheel SHA-256 `a7e61ce8bacb5e8e308b40ad852c46f654d6355fa5e51d423ddc43a8f3274ed6`. Retained manifest and
every listed file matched exact bytes. No rebuild or substitute artifact.

Install ran once beside r6 while r6 stayed current. Existing Python 3.13.15 and
uv 0.12.10 installed the accepted locked requirements with hashes, no dependencies
outside the lock and no source builds. Verification passed 26 Linux-applicable
locked dependencies; tzdata was excluded by its accepted Windows marker. All
170 installed wheel package files match the wheel byte-for-byte. Migration graph
remains 0016_hunt_cached_runs, no pending migration.

| Module | Installed raw SHA-256 |
| --- | --- |
| builder | `d25d67ff8c4762c1a2a591b442c21f57a9db175823d8766dadf0d1433fc82a8c` |
| importer | `7d0c71e7ce314b56c5db5035960e846e27393a84fedf3e5e8afb94a5af5000cb` |
| recovery | `c6b08a5968a70c83690a7b7c1c519b48c4291632012c389d83f901c4459d6d6f` |

The source-bound root-protected operational wrapper remains byte-identical to
the accepted r2 file (`812f505508774bd6d6a040795d8076207ebe79f7ea5c041548e45f75a56fb339`); it is verified separately
from the immutable bundle, which does not package that operational entrypoint.
Native bridge admission passed using the repair interpreter while r6 remained
current. Guarded retirement then ran once before switching.

Accepted atomic pointer/web-path switching changed only the exact absolute
immutable build path in the protected API environment. Other environment bytes
and permissions remained unchanged; health identity changed only release/manifest.
API restart, admin, HTTPS and all 13 health checks passed; Caddy, PostgreSQL and
listener inventory remained unchanged. Startup rollback was not needed or rehearsed.
Final verification again matched manifest, wheel, all 170 module files and wrapper.
An ignored platform-marker verifier correction did not repeat installation.
