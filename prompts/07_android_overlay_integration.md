# Prompt 07 — Polished Android listing capture

**Use in:** a new Codex chat only after the device spike has succeeded and API contracts are stable  
**Model:** GPT-6 Astra  
**Reasoning:** High/Extra High  
**Mode:** Plan first  
**Expected result:** practical multi-photo capture integrated with the real appraisal workflow

---

Using the physical-device findings from the Android spike, plan and implement the production-quality private Android capture flow.

Target experience:

- Open a Facebook Marketplace listing.
- Tap a visible BrickVault bubble/control.
- Capture the current Facebook window/photo without including the BrickVault overlay where supported.
- Swipe the Marketplace carousel manually and capture additional photos.
- Show a captured/unique-photo count.
- Detect exact and near-duplicate captures.
- Review/remove/reorder photos before upload.
- Optionally select/crop/circle a LEGO object.
- Capture or manually enter the visible title, description, asking price, and URL when available.
- Upload as one listing/capture session.
- Start analysis and show a compact result handoff without automating Facebook.

Requirements:

- Explicit user action for capture.
- Package allowlist and clear enabled/disabled state.
- Share Target remains fully functional as a fallback.
- No automatic Facebook clicking/swiping, credentials, traffic interception, or unattended collection.
- Keep raw capture, listing-photo crop, and object crop lineage.
- Apply privacy redaction/exclusion rules before anything becomes training-ready.
- Avoid counting zoomed or repeated versions as independent training examples; link them to the source listing.
- Include robust upload retry/resume behavior suitable for phone connectivity.
- Update the physical-device regression checklist.

Test every behavior available in automation, build the APK, and state exactly which items were verified only by compilation versus on Brian's device.
