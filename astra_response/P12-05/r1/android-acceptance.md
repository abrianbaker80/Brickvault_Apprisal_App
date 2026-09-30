# Physical Android production acceptance — UNRUN

The accepted build entry point was inspected: package.json build:android-production
invokes scripts/android_production.mjs with the approved production API origin.
No production Android build or APK installation ran after the catalog blocker.
There is no P12-05 APK hash/build identity or physical-device evidence to report.
No adb reverse, TEST CA, localhost transport or device network change was used.
TLS/auth/Settings/Watchlist/offline/reconnect/logout all remain unqualified.
