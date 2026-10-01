# Private Listings UI

Listings joins the existing navigation and online-only/authenticated shell.
Twelve newest-first rows per page; each reads the accepted detail projection for
count/first thumbnail. Create accepts optional title, description, URL and price;
currency defaults USD (existing core convention), zero differs from missing.
Source type offers manual/marketplace/listing photos/seller photos. No large editor.

Detail displays metadata and server-ordered thumbnail gallery, original image
viewing, next available position, multi-select JPEG/PNG/WebP, queue state/progress,
independent retry/removal and explicit gallery/position refresh. Privacy wording
states that listings/images stay private in BrickVault. There are no storage paths,
AI controls, retention/deletion controls or provider requests.

Generated contract aliases/openapi-fetch and existing session transport protect
metadata, multipart and binary content. Local image object URLs revoke on change/
unmount. No browser storage or private offline cache. Unfinished queues live only
in this open detail component; persisted images reopen after navigation/reload.
Two admitted shell routes support direct `/listings` and UUID detail opening;
no general fallback is introduced. Service-worker/PWA qualification is deferred.

Desktop 1440x900 and mobile 390x844 show wrapping navigation, usable gallery/touch
controls, readable upload states and no consequential horizontal overflow.
