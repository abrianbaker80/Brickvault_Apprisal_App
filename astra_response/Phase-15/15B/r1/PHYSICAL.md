# Physical TEST evidence and limits

Samsung SM-S948U, Android 17/API 37. No serial, credentials, private pixels or signing
material is included. Only owned neutral-helper content was selected. Consent and
source selection were performed by Brian, never automated.

| Check | Actual evidence |
|---|---|
| Initial restricted chooser | Failed: both Share one app and Share entire screen enabled despite compiled APP-only configuration; no capture; restoration/cleanup completed |
| Owner-amended chooser | Brian explicitly approved choosing Share one app himself in the normal chooser |
| Actual selected task | Android projection readback: RECORD_CONTENT_TASK, owned helper task, displayToRecord=-1; no whole-display recording in that observed session |
| Visible controls | Brian found Capture by expanding the capture notification; explicit Capture completed |
| Preview | Brian confirmed preview; one complete 1440×3120 PNG image loaded; native original 108477 bytes |
| Projection release | No BrickVault projection or capture service after snapshot/review |
| Before Save | 1 seeded listing, 2 seeded images and 2 seeded receipts remained unchanged at preview |
| Explicit Save | Brian selected the existing TEST listing and explicitly uploaded; totals became 1 listing, 3 images, 3 receipts |
| Exact bytes/privacy | Native original hash/length matched PostgreSQL evidence and actual stored blob bytes; new original and thumbnail restricted |
| Responsive UI | Portrait 384×777, scrollWidth 384; preview loaded at full native dimensions |
| Visibility | While the selected helper was obscured, native status reported unavailable; no preview then. This is an observation, not race qualification |
| Cancel | Initial no-source/no-projection attempt was dismissed; no capture/storage result. Exhaustive cancellation timing not tested |
| Protected content, rotation/races, Stop/revocation/lock/process restart | NOT COMPLETED: Brian chose to end the optional experiment after successful Save |
| Disabled-capture Share/manual fallback | Existing 15A physical acceptance and 21 frontend regressions reused; no new physical fallback campaign |
| Final source hardening | Six fixtures/compilation/lint passed; not installed or physically tested after final teardown correction |

The successful phone APK was
`76abdc59b92f607fed5c5b6acdc300c974030b4b2d892f5f6d1ddcd12649f73b`.
An intermediate hardened APK
`a65c952833d550fe7d8522452f2cbdb4619087f4b10d1d7b75c465470b979dd5`
was built and verified but never installed. A final ownership check in teardown was
then source-compiled/tested/linted only. Source and phone evidence are not conflated.

Both disposable TEST runs were cleaned. Final production bytes were restored and
launched, with no helper, capture service, projection or owned ADB rules left.
See [restoration](production-restoration.json), [device cleanup](device-cleanup.json)
and [backend cleanup](backend-cleanup.json). Earlier immutable 15A evidence is reused
from its existing [physical review](../../15A/r2/REVIEW.md).
