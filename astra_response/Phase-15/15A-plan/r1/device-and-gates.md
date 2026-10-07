# Device facts, capture gate and approvals

## Facts as of 2026-10-07

| Fact | Evidence status |
|---|---|
| Samsung Galaxy S26 Ultra; model spelling SM_S948U | Known from Brian; no repeat request |
| BrickVault package com.abrianbaker.brickvault.appraisal | Previously physically qualified |
| ADB availability | Installed local tool; sanitized devices -l returned zero devices |
| Android release / SDK/API | Unknown; record at implementation preflight |
| Installed Facebook-related package names | Unknown; no package assumed |
| Presently installed APK / API access mode | Unverified; no device available and no app-state inspection |
| Historical Phase 9 path | Plan 088: authenticated TEST TLS via localhost:18443 and USB reverse; cleanup removed the qualification path/app |
| Newer accepted Android path | Plan 099 Gate 7: production HTTPS/system-only trust, no reverse or native HTTP bypass |

No device serial, private listing content, credentials, device screenshot or local secret
is included. No Facebook launch, permissions/settings, app state, install or capture action ran.

## 15A review and implementation approvals

Approve the proposed Share-only slice, restricted-only privacy elevation and volatile
intake limits. Separately authorize the exact candidate APK build/install and physical
TEST backend/device checks. Missing release/API data does not block the plan; collect
it read-only when connected. Model/package/previous core qualification are already known.
Manual upload and direct lookup must still work with capture/recognition unavailable.

Use approved neutral images/source app for cold/warm one/multiple sharing; Facebook
is not required to establish generic Share reception. Label real phone evidence separately
from native/JS fixtures, real PostgreSQL tests and builds. Failed receipt/order/auth/privacy
or lifecycle rows keep 15A NOT QUALIFIED. Accepted 15A ends at review; no capture continuation.

## 15B capture mechanism selection — currently unresolved

API 34+ accessibility window screenshots are the technical target-window candidate.
Resolve documented accessibility-purpose suitability and explicit permission scope first.
Require current application window/root-package evidence against Brian's actual allowlist;
event filters alone do not enforce it. Bind request to the window and revalidate callback
identity/visibility; unknown, stale, ambiguous and in-flight target changes must refuse or
discard. The public API offers no atomic identity-plus-frame assurance; this remains an
explicit race/physical acceptance gate. No node text/OCR/content logging.

MediaProjection's single-app chooser is an alternate capability, but documented public
APIs do not expose or constrain the selected package. It cannot independently qualify
the requested allowlist. Do not weaken the gate to instructions to pick Facebook.
Overlay permission supplies optional visible controls; it supplies no package proof.
If controls are hidden/revoked, secure content is protected or no suitable supported
mechanism exists, report capture unavailable and keep Share/manual upload usable.

Before any 15B code/device work: accepted physical 15A review, Brian-approved confirmed
package names, chosen supported mechanism, suitability/permission scope, visibility/stop
behavior and exact device test authorization. Each capture is one explicit action, visible
and disableable. Default/restart disabled. No unattended collection, automatic navigation,
interception/scraping, seller automation or security bypass. Stop for 15B review afterward.
15C may proceed only after 15B physically passes and separate scope authorization.

## Privacy and networking

Phase 13C's 2026-10-01 policy remains approved: server retained originals/derivatives
are immutable while retained, owner-only/no-store, no scheduled deletion or orphan cleanup,
private encrypted backups, no AI/provider submission or dataset export. Raw screenshots
and unknown inputs are restricted; seller/profile names/photos, locations, messages,
notifications and unrelated content may be visible. Brian reviews/cancels before Save;
no new crop/redaction promise is made. No retention-policy rewrite.

Memory-only unsaved native/JS custody is proposed, consistent with accepted fresh-process
privacy. No persistent URI grants or phone spool. A requested durable crash-resume copy,
background upload or Android backup would create a new custody decision; obtain approval
before implementation. Clearing unsaved memory does not delete retained server images.

Prefer the historical approved localhost TEST TLS/ADB-reverse path with explicitly owned
TEST DB/blob storage for 15A qualification. Current source can also package production HTTPS;
history does not prove the phone's current route. This planning task made no API/backend
contact. Any testing beyond USB TEST or production data writes needs separate authenticated
network/data approval. Do not change exposure, bind addresses, firewall, DNS, Caddy/server
configuration or expose PostgreSQL/API ports to make the test work.
