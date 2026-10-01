# Sanitized commands and scope

Commands were scoped to the named production VM and the connected physical phone.
Configured SSH target, device serial and local toolchain paths are withheld.

| Operation | Result |
|---|---|
| node scripts/android_production.mjs with approved HTTPS production origin | PASS |
| gradlew.bat --no-daemon --console=plain --offline assembleDebug | PASS |
| APK inspection/signature/system trust/origin/asset checks | PASS |
| adb devices/device properties/reverse list | One physical non-network target; reverse empty |
| adb install -r production-configured APK | PASS; no data clear/uninstall |
| Actual app accessibility/UI controls and locally entered login | PASS; password field suppressed |
| Offline phone network controls | Exact original settings restored |
| am force-stop approved package, process-absence check, ordinary launch | Fresh offline no private records |
| Supported browser DOM/CDP network/public CacheStorage inspection | PASS within accepted browser skill |
| Existing backup six encrypted readbacks/repositories/proof | PASS, no new backup |
| Pinned immutable manifest/static build checks | PASS for both releases |
| systemctl show known service ExecStart + immutable missing-script check | BLOCKED compatibility confirmed |
| Protected read-only database/session/settings/cleanup queries | PASS; no business SQL mutation |
| Additive docs/original-body/Markdown-link/source/protected/index checks | PASS; 313 local links |

No broad tests, dependency installation, provider calls, backend deployment,
rollback switch, operational timer pause, VM stop/start or final backup.
Existing accepted V1/diagnostic tests were reused. Build results and physical
behavior are separately recorded. Worker-version transition and new-token replay
remain unexercised. Agent-local helper invocation errors were corrected without
changing application code or production configuration.
