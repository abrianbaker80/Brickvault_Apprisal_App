# Prompt 03 — Android capture feasibility spike

**Use in:** a new Codex chat in the same repository, after Phase 1 is committed  
**Model:** GPT-6 Astra  
**Reasoning:** High; use Extra High if platform/API conflicts appear  
**Mode:** Plan first, then Code after plan review  
**Expected result:** a deliberately small device-testable Android spike

---

Create and execute an ExecPlan for the Android capture feasibility spike described in `docs/ROADMAP.md`. Read all repository guidance and the completed Phase 1 API before planning.

The purpose is to prove the risky Android interaction, not to build the final polished client.

Implement only these capabilities:

1. A minimal Kotlin/Jetpack Compose Android app that can connect to the development API.
2. Android Share Target support for one or multiple images, allowing me to choose an existing listing or create a basic new listing and upload the images.
3. A clearly visible, user-triggered floating capture control implemented through the safest supported Android mechanism for the target device.
4. A capture path that, on Android 14/API 34 or newer, evaluates `AccessibilityService.takeScreenshotOfWindow` so the BrickVault overlay is not included in the target-window screenshot. Use only supported official Android APIs.
5. A narrowly scoped fallback strategy for older/special devices, such as standard display screenshot capture or MediaProjection, but do not build multiple elaborate implementations unless necessary for the spike.
6. Restriction to explicitly allowlisted application package names, including the normal Facebook package when configured.
7. Upload of the captured image to the existing listing/image API with clear success/failure feedback.
8. A settings/status screen explaining whether accessibility/capture permission is enabled and how to turn it off.

Hard boundaries:

- Every capture requires an explicit tap by Brian.
- No automatic swiping, clicking, Facebook navigation, background monitoring, OCR, carousel detection, or listing analysis.
- Do not intercept network traffic or access Facebook credentials.
- Do not claim Facebook compatibility from emulator/compile results alone.
- Keep experimental capture code isolated behind a feature flag/interface so the Share Target remains usable even if accessibility capture is disabled.

Testing and evidence:

- Add unit tests for package allowlisting, upload request construction, state handling, and duplicate submission prevention where practical.
- Build the debug APK and run available Android tests.
- Produce a precise physical-device test checklist for Brian, including Android version, Facebook package, permission steps, expected overlay behavior, expected screenshot contents, and logs/screenshots to collect on failure.
- Mark every behavior that still requires physical-device verification.

Stop after the spike. Update its ExecPlan with results and provide the path to the APK only if the build actually succeeds.
