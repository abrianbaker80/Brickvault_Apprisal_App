# ExecPlan 096 — P12-04C production database activation

## Goal and user-visible outcome

Activate the private BrickVault production database on VM 115 with two verified real recovery points: one before migration and one after owner bootstrap. Leave the API disabled and inactive. P12-04 remains IN PROGRESS; P12-05 has not started.

## Why this work is being done now

[P12-04A](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/22f80286b1b82d7862b922fe2d66fd06fa84cf9b/astra_response/P12-04A/r1/REVIEW.md) established the private VM, PostgreSQL and inactive packaged API. [P12-04B](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/32614857222de30bf978675f08da8ac4b0b2711f/astra_response/P12-04B/r2/REVIEW.md) qualified two independently encrypted synthetic recovery paths but left offline credential custody and the mismatch between backup receipts and admin recovery proofs open. Those gates must close before the first production migration.

## In scope

- Put the minimum two-repository recovery material on Brian's selected removable SD card in an authenticated encrypted bundle; locally verify decryption, manifest hashes and access to both repositories.
- Derive a protected migration proof only from a fresh, complete, dual-readback production backup receipt and the exact Alembic revision state.
- Build and install one new immutable release, provision the exact production database/roles/descriptor, run the guarded pre-migration backup, migrate, grant runtime access, bootstrap one owner through hidden local input, verify, then run the post-bootstrap backup.
- Install the reviewed backup units; enable the daily timer only after the second backup succeeds.
- Publish sanitized P12-04C review evidence to `astra-response` without committing or pushing `main`.

## Explicit non-goals

No Caddy, DNS, TLS, API secret or startup, public listener, firewall/router change, destructive restic retention, VM onboot change, real restore drill, browser/PWA/Android acceptance, or P12-04D/P12-05 work. Do not copy production DB passwords directly into the offline recovery bundle.

## Current repository state

At entry, `main` is `5b0fc9919d6755d1414527c27592b7df1068c96d` with an empty index. The pre-existing modified `AGENTS.md`, `services/api/tests/integration/test_catalog_search.py` and `services/api/tests/unit/test_catalog_parser.py` have their accepted SHA-256 values and remain outside this slice. P12-04A and P12-04B are accepted. The corrected P12-04C r4 release is installed on VM 115, with the API inactive. The r1 blocked package is accepted as a correct fail-closed checkpoint and remains intact.

The first two local bundles were superseded before any VM transfer: r1 preceded the focused grant/bootstrap integration test, and r2 preceded backup state-directory isolation. The previous `p12-04c-r3` release remains intact; its source ID was `abb75b857c38212837b2f559aa58adebb5832295e4aab17acad6fac4947ccb0e`, manifest SHA-256 `aef807e362b162700d9df46573a7bd519034c5c73f9c876181061df98ae2d54f` and API wheel SHA-256 `06aba11e7004b3f2ab8d79848c60ef2d3e4690f4b5f2509a8d2ce9a779bef521`.

The current immutable release is `p12-04c-r4`, source ID `6c0ca52d142b2018c2a4b7a72342705196e1cb72e883cb352e91a3f167cb6536`, manifest SHA-256 `980b7d9894eeee745bd8c7e8222714790f8ac6a56e7812d1d0c6d9fd29ae96a8`, API wheel SHA-256 `02dc2675632ffc72ffd11a797aab11b52fee5820b5966bc582864baf9ce8fc97`. Local manifest/wheel/source/frontend/lock verification, hash-pinned transfer, VM dependency installation, installed-wheel import, CLI entrypoints and migration graph passed. The corrected unit retains `NoNewPrivileges=true`; its SHA-256 is `69f868c85113ea3ea340c4fcd204374863148d3060c5d2a6dec4e9ff5bbb33e4`.

## Decisions and assumptions

Brian identified an attached removable SD card for offline custody. A local-only helper under ignored `.local/p12-04c/` prepared and verified the encrypted bundle. The first attempt failed because temporary Windows OpenSSH key permissions were too broad; the helper's temporary extraction ACL was corrected. The first attempt's unlock phrase appeared in chat, so its bundle was disqualified. Brian confirmed that card was destroyed or permanently retired. A different clean removable card and fresh private phrase passed on-media decryption, manifest hashes and independent access to both accepted repositories. Brian confirmed physical custody of the new phrase away from VM/laptop; the replacement card was removed. **Offline custody PASS**, manifest digest `7b0257c774c5a88c4bbe56f2946d103f957dc06a75ad9568346a9ed9673822e0`. No phrase, media identity or secret material is included here.

The backup receipt becomes schema 2. It records the production marker, run ID, exact revision tuple, repository URIs/IDs and each artifact's bytes, digest and separate destination snapshot IDs. Protected receipts and proofs reside under `/etc/brickvault/backup`, whose root-owned parents satisfy the production admin reader; `/var/lib/brickvault` belongs to the API account and cannot safely hold these root-only proofs. The backup unit uses its own root-owned `/var/lib/brickvault-backup-runner` state rather than systemd creating a nested state directory under the API account's tree. `brickvault-production-backup finalize-proof <run-id>` rereads all six encrypted artifacts, checks both repositories and the protected receipt, confirms the current revisions and recency, then creates a root-owned proof with exclusive creation. The admin commands revalidate the proof against the detailed receipt and both repositories. Operators supply only a run ID or generated proof path, never arbitrary snapshot hashes.

## Data model and API/interface changes

### r2 continuation: preserve the service sandbox

Brian accepted r1 as a correct blocked checkpoint and authorized one corrected first-backup retry. The r1 proposal to set `NoNewPrivileges=false` was not installed and is superseded. The accepted PostgreSQL `brickvault_maintenance` peer map already lets OS root authenticate as database `postgres` on the local Unix socket. A transient service with `NoNewPrivileges=true`, `RestrictSUIDSGID=true` and the other accepted protections successfully ran direct `pg_dump` and `pg_dumpall` without passwords or inherited credential environment. Its read-only checks confirmed the exact peer identity, empty revision state, no principal, no new snapshots and no receipt/proof.

The corrected runner removes `runuser` from producers, tool preflight and constants. It invokes the absolute PostgreSQL executables directly with the exact socket/user/database, `--no-password`, closed standard input, an isolated environment and `/dev/null` as the password-file location. Both producer streams remain memory-only. The service retains `NoNewPrivileges=true` and every other accepted sandbox setting. Fifty-four focused tests, targeted Ruff, format and mypy passed before building the new immutable `p12-04c-r4` release. The single production retry may run only after the new release and unit pass their gates; a retry failure requires another stop.

No application schema or HTTP API change is planned. The production backup CLI adds `finalize-proof <run-id>` and upgrades future detailed receipts to schema 2. The production admin proof uses schema 2 with a SHA-256 binding to the exact protected backup receipt, six snapshot identities, both repository identities, the ownership marker, run ID, revision tuple and verification time. Existing legacy proof-shaped files are refused.

## Implementation sequence

1. Confirm the selected SD card, produce the encrypted recovery bundle through a visible local terminal, and verify it from the removable media. Record only the safe PASS/FAIL summary and digest. Stop before database provisioning if this gate fails.
2. Complete backup/admin source integration and focused tests for missing destination, tampering, readback failure, digest/revision/staleness binding, CLI redaction and refusal of operator-provided hashes. Run targeted pytest, Ruff, format and mypy.
3. Read-only verify VM 115, loopback PostgreSQL, absence of production names/API listener, inactive API, reviewed storage and repository identities. Stop on target drift.
4. Build a new immutable P12-04C release using the accepted manifest/package pipeline. The current release is `p12-04c-r4`; r1/r2 were superseded locally before transfer, and r3 remains intact after the accepted blocked checkpoint. Check the source ID, wheel/lock/frontend, manifest digest and entrypoints. Transfer only reviewed artifacts; install under `/opt/brickvault/releases/` and atomically select `/opt/brickvault/current` while the API stays inactive.
5. Install and verify the backup service/timer definitions without enabling the timer. Generate the root-only production descriptor and distinct credentials locally on VM 115 without printing them. Pass `brickvault-production-admin preflight` before provisioning.
6. Provision only `brickvault_appraisal_prod`, its owner role and runtime role. Verify exact marker, privileges, no memberships or migration, and stop on partial state.
7. Run one real pre-migration dual backup and validate all artifacts/readbacks/checks. Finalize one protected proof from its run ID; verify the proof is recent and bound to the empty pre-migration revision tuple.
8. Use that proof for guarded migration to the packaged head, runtime grants and one owner bootstrap through a local hidden-input TTY. Run `brickvault-production-admin verify`. If no secure local TTY is available, stop at `OWNER PASSWORD INPUT REQUIRED` and resume after Brian completes the one local command.
9. Run one real post-bootstrap dual backup and verify both destinations. Preserve both runs and all synthetic canaries. Enable and inspect the reviewed daily timer. Recheck API inactivity, loopback database, SSH, guest agent, clock and data mount.
10. Update this plan and minimum status references with actual results. Publish sanitized r1 review artifacts from the exact P12-04C diff, leaving `main` uncommitted and its index empty.

## Validation and acceptance criteria

The offline bundle must decrypt from the SD card and independently open both accepted repository identities. Focused source tests and static checks must pass before live mutation. The new release must have verified source, wheel, frontend and manifest identities on both machines. The production DB must be owned by the exact guarded role/marker, migrated to the packaged head, have least-privilege runtime grants and exactly one owner principal. Both real backups must have protected detailed receipts after six matching encrypted readbacks and repository checks. The first must produce the only proof used for migration/grants/bootstrap. The timer may be active only after the post-bootstrap backup passes. The API must remain disabled/inactive, with no API/Caddy listener.

## Security, privacy and data integrity

Keep raw credentials, ownership marker, private addresses, SD media identity, OAuth tokens, repository IDs and production configuration out of terminal capture and review artifacts. The offline unlock phrase stays outside VM/laptop/chat. The release is immutable; do not modify the installed P12-04A tree. The production backup streams the DB dump directly to independently encrypted repositories; no persistent plaintext dump. The proof gate requires a current, fully read-back receipt and fails closed on any mismatch. Do not delete any snapshot in P12-04C.

During local recovery inventory, the contents of an unrelated protected backup identity appeared in one Codex tool result. It is not part of this offline package or review artifact. Its separate rotation review remains open; P12-04C does not alter that unrelated backup system.

## Failure modes, rollback and recovery

Stop if offline custody or either repository check fails, release identity drifts, descriptor protection is uncertain, provisioning is partial, backup/readback fails, proof cannot be derived, migration/grants/account checks differ, the owner TTY is unavailable, the second backup fails, the timer cannot be safely enabled, or the API starts unexpectedly. Preserve exact state and diagnose; do not auto-delete production objects, fabricate a proof, weaken the admin gate, or run destructive retention. The pre-migration real backup is the recovery boundary for later production changes.

## Progress log

- [x] 2026-09-29: Confirmed the expected `main` HEAD, empty index and accepted hashes of the three protected dirty files.
- [x] 2026-09-29: Identified Brian's selected removable SD card and prepared a local encrypted-bundle helper without putting secrets in Git. The local custody proof is pending.
- [x] 2026-09-29: Implemented the schema 2 receipt/proof integration source and passed 45 focused backup/admin unit tests plus targeted Ruff. Found and corrected the protected receipt/proof parent ownership mismatch before any real backup; post-correction checks remain pending.
- [x] 2026-09-29: After the protected-path and state-directory corrections, 46 focused backup/admin tests, five release-manifest tests, targeted Ruff, format and mypy passed. The pnpm build verified the independent installed wheel, migration graph and frontend; the current `p12-04c-r3` local release manifest verified.
- [x] 2026-09-29: Proxmox guest-agent identity matched VM 115 to the pinned P12 target after an unrelated SSH alias was found to point elsewhere. Read-only VM checks passed Ubuntu, guest agent, time, mount, PostgreSQL/version/loopback, absent production names, inactive API/no listener and absent Caddy. Both accepted recovery repository IDs matched protected VM records. No production mutation occurred.
- [x] 2026-09-29: Read-only release preinstall checks confirmed the accepted P12-04A current symlink, expected root/service-account directory ownership, protected backup configuration parent, Python 3.13.15, uv 0.12.10, no r3 release path and inactive API. P12-04C artifacts have not been transferred.
- [x] 2026-09-29: The first SD-card bundle was created but its readback verification failed. A safe local diagnostic traced this to inherited Windows OpenSSH permissions on the temporary copied recovery key. The helper was corrected to restrict extraction directory and file ACLs; diagnostic access to both repositories then passed. The first bundle's unlock phrase appeared in chat, so that bundle is disqualified and a clean replacement removable device is pending.
- [x] 2026-09-29: Brian attached a replacement removable card. Windows read-only checks found a healthy, ready exFAT volume with no v1 bundle and only the normal system metadata directory. The v2 helper uses a fresh bundle/status name and clears the visible console after Brian confirms separate physical phrase storage. On-media decryption, manifest verification and both repository access checks passed. The no-secret manifest digest is `7b0257c774c5a88c4bbe56f2946d103f957dc06a75ad9568346a9ed9673822e0`; the replacement card was removed from the laptop afterward.
- [x] Offline custody PASS, including Brian's separate physical unlock-secret custody confirmation and first-card retirement.
- [x] Final source validation and read-only live foundation gate.
- [x] New r3 release built, hash-pinned, installed and verified; API remains inactive.
- [x] Protected descriptor, preflight and exact DB/role provisioning. The descriptor was generated locally on VM 115, root-owned and mode 0600. Distinct owner/runtime credentials and the marker were not printed. The DB is unmigrated with no application principal.
- [x] Backup service/timer definitions installed and verified; timer remains disabled/inactive.
- [x] 2026-09-29: The one authorized first real backup service start failed with exit code 1 before creating a protected receipt or either destination snapshot. Read-only snapshot counts remained at one synthetic canary per repository. The service stays failed; the API and timer stay inactive. No second backup attempt, proof finalization, migration, grant or bootstrap ran.
- [x] 2026-09-29, historical r1: Read-only transient service probes passed descriptor, revision and configuration checks, then isolated failure to `runuser -u postgres` (`cannot set user id: Operation not permitted`). With the otherwise matching sandbox, disabling `NoNewPrivileges` alone let `runuser`, `pg_dump`, `pg_dumpall` and configuration tar streams complete. `RestrictSUIDSGID=true` and the other unit protections remained enabled. The r1 local proposal set `NoNewPrivileges=false`; it was **never installed** and was superseded by the direct peer correction below.
- [x] r2 continuation: direct root peer `pg_dump` and `pg_dumpall` passed under the complete intended sandbox with `NoNewPrivileges=true`. Removed the unnecessary `runuser` dependency and retained the accepted hardening. Fifty-four focused tests, targeted Ruff, format and mypy passed.
- [x] r2 continuation: new immutable r4 release installed and selected atomically; installed-wheel bytes and corrected unit verified. Only the failed oneshot state was reset. The pre-retry gate confirmed unchanged canary-only repositories, empty receipt/proof directories and an unmigrated database with no principal.
- [x] The single authorized first-backup retry passed all three artifacts, both destinations, six encrypted readbacks, size/digest equality, repository checks and protected schema-2 receipt creation. The run ID is recorded privately.
- [x] Guarded proof finalization reread all six encrypted copies and both repositories, bound the exact marker/receipt digest/empty revision tuple, and exclusively created a root-owned 0600 proof with a fresh timestamp.
- [x] Guarded migration with the generated proof reached `0016_hunt_cached_runs`. Runtime grants using the same proof passed the minimum privilege guard, production identity/role checks, schema ownership and no-principal checks.
- [x] Brian bootstrapped exactly one owner using the local interactive SSH TTY and hidden password prompts. The password was not requested or received in chat. Independent `brickvault-production-admin verify` passed production ownership, migration, one principal and runtime core privileges.
- [x] The one post-bootstrap dual backup passed all three artifacts and six encrypted readbacks, matching sizes/hashes and both repository checks. Its separate protected receipt binds `0016_hunt_cached_runs`; its run ID is stored privately. Both real runs and each prior canary remain, with seven snapshots per destination.
- [x] After the post-bootstrap backup passed, the reviewed daily timer was enabled and started. At accepted evidence time it was active with next trigger `2026-09-30 03:22:03 UTC`, within the accepted 03:15 plus up-to-30-minute randomized schedule. The backup service is inactive after successful completion. No extra manual scheduled backup was run.
- [x] Final checks passed API disabled/inactive, no api.env/Caddy/API listener, PostgreSQL only `127.0.0.1:5432`, no unexpected externally bound TCP service, key-only SSH with root login disabled, guest agent, synchronized clock and reviewed PostgreSQL data mount.
- [x] The sanitized r1 blocked package was published and accepted. Its evidence remains intact; the successful continuation is prepared as a separate r2 package. Main remains uncommitted, with an empty index and the protected files excluded.

## Open questions and manual checks

Brian identified a different, clean removable device and completed its private v2 verification. He confirmed that the first card with the exposed-phrase bundle is destroyed or permanently retired under his control. He also completed owner account creation through local hidden-input SSH TTY prompts. Neither new secret entered chat or review evidence.

- [x] Closeout: Brian accepted the [r2 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/18e87d889f5203d1da30fb3d356178f2ce2919b8/astra_response/P12-04C/r2/REVIEW.md). Only the nine-file local checkpoint and r3 review publication are authorized. Accepted r2 evidence is reused; no live, test, build or recovery work is rerun.

## Outcome and follow-up

**P12-04C is ACCEPTED / CLOSED.** The accepted r1 blocked checkpoint is preserved. Direct root peer authentication removed the unnecessary privilege transition; `NoNewPrivileges=true` remains installed. Offline custody, corrected r4 release, the one authorized pre-migration backup retry, guarded proof, migration to `0016_hunt_cached_runs`, runtime grants, exactly one owner through hidden local input, independent admin verification, the post-bootstrap dual backup and timer activation passed. Both protected receipts and the pre-migration proof remain; both real runs and synthetic canaries are retained. The API remains disabled/inactive and unexposed. No production restore drill has been claimed. P12-04 remains IN PROGRESS; P12-04D is NEXT / NOT STARTED; P12-05 is NOT STARTED.

Remaining gates stay OPEN:

- Complete-run destructive retention implementation/review.
- Production API configuration/secrets and API startup.
- Private DNS, trusted production certificate, Caddy and private HTTPS path.
- Firewall/client-source policy.
- Monitoring and alert destination.
- Deliberate production VM onboot behavior.
- CPython 3.13 maintenance/update monitoring.
- Unrelated protected-backup identity rotation review noted above.
- P12-05 real production restore, browser/PWA acceptance, physical Android normal-TLS acceptance and rollback rehearsal.
