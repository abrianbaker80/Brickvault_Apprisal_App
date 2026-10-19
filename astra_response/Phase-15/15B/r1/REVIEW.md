# Phase 15B capture spike — partial physical result

**PARTIAL / remaining physical qualification pending — Brian ended the experiment.**

The phone completed human-selected neutral-app capture → one PNG preview → explicit
Save through the accepted 15A intake/Phase 13 API. Production is restored. This is
review evidence, not production feature deployment or full capture qualification.

- **Actual scope:** Android readback recorded `RECORD_CONTENT_TASK` for the owned
  neutral helper, with `displayToRecord=-1`. Single-task scope was physically
  verified for that session. The app does not enforce or verify selected scope/package.
- **Original/Save:** 1440×3120 PNG, 108477 bytes, SHA-256
  `e60b7f4c3f58caf4e847991fc4c3d0e65778742d9ae82257380385298c7ab1dd`.
  Actual stored TEST blob bytes matched. Original and thumbnail were restricted.
  Preview wrote nothing; explicit Save added one image and one receipt.
- **Restoration:** preserved production APK restored in place and launched, SHA-256
  `045210d00ecf200b4579aed1ab0bb869c5c9d09eee7328c64472902d7851ddd2`.
  Same signer/UID/first-install identity; system-only trust, production destination,
  no TEST reverse dependency. Owned helper/API/database/blobs/credentials/ADB rules
  cleaned; prior unrelated state preserved.
- **Checks:** six native fixtures, 21 existing Share frontend regressions, affected
  lint/types/format/build/privacy/config/signature checks pass. Android lint has
  zero errors and 19 warnings. No backend, migration or dependency upgrades.

The initial APP-only chooser restriction failed: the phone also offered entire-screen
capture. Brian explicitly amended the boundary to Android's normal chooser, with him
selecting **Share one app**. The UI discloses reliance on that choice. The official
API configuration still requests APP only/audio off; this does not prove enforcement.
Both the failed gate and later amendment are retained in [design](DESIGN.md).

**Unqualified:** final notification-action/teardown hardening is source-tested only;
protected-content, rotation/visibility races, Stop/revocation/lock/process restart
and disabled-capture fallback were not physically completed. No Facebook content
was opened or captured, and no Facebook compatibility is claimed. See
[physical results](PHYSICAL.md) and [focused checks](focused-checks.json).

Brian confirmed production search found set **10350** after the first restoration,
but reported no market data/numbers for it. That unresolved observation was not
diagnosed here. The final restoration used the same exact artifact; automated
authenticated production testing was not repeated.

Main remains `e3c04d90b1646b9b9dad73325bf1491fb8326943`, source/docs uncommitted,
index empty and main unpushed. Three protected dirty files and prior uncommitted
Plan 108 restoration/mechanism notes are preserved. [Inventory](changed-inventory.json)
covers 19 changed paths; [patch](implementation.patch) replays to every resulting
file with line-ending normalization. Plan 108's patch starts from its preserved
uncommitted preimage; other tracked files start from main HEAD.

Recommended everyday path: normal phone screenshot → accepted 15A Share → review/Save.
Its production promotion is a separate task. No further experiment, deployment,
implementation commit, 15C or Phase 16 is authorized by this review.
