# Gate 7 physical Android production acceptance

PASS on one non-emulator, non-network ADB target physically connected by USB as
confirmed by Brian. Windows ADB did not expose independent USB bus-path metadata;
no device serial/IP/MAC is published. The phone stayed unlocked and the owner
password was entered locally. No emulator or transport-only result substitutes
for the observed app behavior.

Package `com.abrianbaker.brickvault.appraisal`, versionName 1.0/versionCode 1.
Signed debug acceptance APK SHA-256:
`045210d00ecf200b4579aed1ab0bb869c5c9d09eee7328c64472902d7851ddd2`.
This is a physical acceptance artifact, not a release-store signing qualification.

Existing approved toolchain/build path succeeded once: production web/config build
and Gradle offline assembleDebug. APK signature verified. Packaged API origin is
`https://appraisal.abrianbaker.com`; WebView origin is
`https://android.appraisal.abrianbaker.com`. Compiled security config trusts system
certificates only, cleartext/mixed content disabled, no test CA/private files,
no localhost/server override, no native HTTP/cookie bypass. Eight public assets
matched the production build. ADB reverse list was empty; no reverse rule added.

Real local owner login succeeded. Set 75331-1 detail retained honest UNKNOWN
market evidence. Settings changed sale mode to MANUAL, saved through UI, then
restored choose-in-each-draft, saved and freshly read. Original default profile
was absent and all three option flags remained off. The initially empty Watchlist
received exactly one temporary set with target 123.45; authoritative reload retained it.

Alive-process offline: temporary Wi-Fi/mobile-data disable, native Home/resume
with same PID, eventual Offline dated read-only Watchlist, retained target, disabled
input/search/save. Reconnect through Check connection restored authenticated reads.
Cold offline: force-stop verified no app process, offline restart showed Connection
unavailable with no private Watchlist/workspace. Exact original phone network
settings were restored; online restart and Check connection recovered authoritative
target once without duplicate. UI accessibility observations were read in the real
app, with password text suppressed; no session storage/token extraction occurred.

Failure cleanup removed that item through UI, displayed No watched sets yet, then
Signed out. Server readback confirms zero items, original Settings defaults and
zero valid sessions. No saved acceptance deal or forecast was created.
