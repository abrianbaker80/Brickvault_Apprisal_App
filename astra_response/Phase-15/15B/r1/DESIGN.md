# Amendment and implementation

Brian first authorized replacing strict Facebook-package allowlisting with
OS-selected single-app capture, requiring API 37 APP-only chooser configuration.
The compiled candidate enabled APP and disabled DISPLAY, APP_CONTENT and audio.
The phone nevertheless offered both “Share one app” and “Share entire screen”.
No projection/frame/save occurred in that first attempt; production and owned TEST
resources were restored/cleaned. The exact system reason is unresolved. This is
not corrected by claiming that preselection enforces scope.

Brian then explicitly approved Android's normal chooser and relying on his own
**Share one app** selection. That supersedes the requirement that the actual chooser
must disable whole-screen selection, while preserving human consent and every
other privacy/TEST/production boundary. Source code continues requesting APP only
and audio off. No title guessing, package polling, hidden API, reflection,
AccessibilityService, overlay, microphone or broad storage is introduced.

The optional TEST bridge is default-disabled in ordinary builds. Build opt-in
requires the existing owned TEST certificate configuration. Compile SDK is 37.0;
minimum 24, target 36, AGP/Gradle/Capacitor and all dependencies stay unchanged.
API availability is a capability gate, not a selected-scope attestation. This spike
does not qualify arbitrary API 37 devices or Facebook compatibility.

`Start` opens Android consent. Brian alone selects the source. A nonexported
mediaProjection foreground service presents a visible notification with Capture/Stop
actions and requests notification permission explicitly. It may remain active while
BrickVault's Activity is backgrounded; the accepted Share/background-upload policy
is unchanged. Each projection requires fresh consent and admits at most one original.

Two ImageReader buffers, at most 12 million pixels each, are transient OS/native
projection buffers. Pre-action frames are immediately closed without image analysis
or history. Explicit Capture arms admission for a frame timestamp newer than the
action. A five-second frame deadline and two-minute session/pending deadline bound
custody. Resize replaces the reader/surface without creating a second projection
display; resize/visibility loss disarms the request. Stop, revocation, screen-off,
timeout, stale generation callbacks and process death cannot automatically restart.
Final generation-bound notification actions and teardown prevent an old action or
callback from interfering with a new session; these final changes lack phone proof.

Pixels are packed without enhancement and PNG-encoded once; output is bounded to
the accepted 25 MiB/file limit. Projection/display/reader resources are released
before preview. One process-only original can transfer to the existing Share intake
after verified foreground-session checks. No URI opener, disk spool, gallery export,
native HTTP credential or second protocol is added. Existing review/destination,
UUID/order/queue and restricted Save semantics are reused. Logout/observed session
expiry/discard clears unsaved custody; clearing does not delete a saved server image.

Protected output is never bypassed. A blanked region may remain blank; darkness is
not interpreted as a reliable secure-window detector. Controlled protected-content
and remaining lifecycle/race tests were stopped by Brian before qualification.

Official API references used:

- [MediaProjectionConfig.Builder](https://developer.android.com/reference/android/media/projection/MediaProjectionConfig.Builder)
- [MediaProjectionConfig](https://developer.android.com/reference/android/media/projection/MediaProjectionConfig)
- [MediaProjectionManager](https://developer.android.com/reference/android/media/projection/MediaProjectionManager)
- [Media projection lifecycle and callbacks](https://developer.android.com/media/grow/media-projection)
