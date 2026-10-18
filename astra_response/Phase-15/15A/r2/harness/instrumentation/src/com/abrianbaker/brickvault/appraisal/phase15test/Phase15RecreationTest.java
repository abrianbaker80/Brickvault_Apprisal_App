package com.abrianbaker.brickvault.appraisal.phase15test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;

import android.app.Activity;
import android.app.Application;
import android.app.Instrumentation;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ApplicationInfo;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.content.res.Configuration;
import android.os.Build;
import android.os.Bundle;
import android.os.Process;
import android.os.SystemClock;
import android.util.Log;

import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry;
import androidx.test.runner.lifecycle.Stage;

import com.abrianbaker.brickvault.appraisal.MainActivity;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Collection;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

import org.json.JSONObject;
import org.junit.Test;
import org.junit.runner.RunWith;

/** Ignored androidTest-only control. It does not ship in or alter the target APK. */
@RunWith(AndroidJUnit4.class)
public final class Phase15RecreationTest {
    private static final String TARGET = "com.abrianbaker.brickvault.appraisal";
    private static final String HARNESS = TARGET + ".phase15harness";
    private static final String TAG = "BV15Recreate";
    private static final String EXPECTED_APK = "fcc37bfe0acaabe2fcc1f5c9c3d9faae6c00227e4dc3cac2c857ff518fb22c9c";
    private static final String EXPECTED_SIGNER = "e4d375e7f1611cb1113620379ea171a176f32bb11cc7528b6c176a1a08dffe72";
    private static final long MAX_LIFETIME_MS = 30L * 60L * 1000L;
    private static final int MAX_RECREATIONS = 12;
    private static final int MAX_ORIENTATION_REQUESTS = 24;
    private static final long LIFECYCLE_GUARD_MS = 45000L;

    private static final class Snapshot {
        final int pid, activity, webView, orientation, requestedOrientation, width, height;
        Snapshot(MainActivity owner) {
            pid = Process.myPid();
            activity = System.identityHashCode(owner);
            webView = System.identityHashCode(owner.getBridge().getWebView());
            orientation = owner.getResources().getConfiguration().orientation;
            requestedOrientation = owner.getRequestedOrientation();
            width = owner.getBridge().getWebView().getWidth();
            height = owner.getBridge().getWebView().getHeight();
        }
    }

    private static final class Recreation {
        final Snapshot before;
        final CountDownLatch destroyed = new CountDownLatch(1);
        final CountDownLatch created = new CountDownLatch(1);
        final CountDownLatch resumed = new CountDownLatch(1);
        final AtomicReference<Snapshot> after = new AtomicReference<>();
        final AtomicReference<Throwable> observationFailure = new AtomicReference<>();
        volatile int createdActivity;
        volatile boolean savedState;
        Recreation(Snapshot before) { this.before = before; }
    }

    private interface MainAction<T> { T run() throws Exception; }

    @Test
    public void controlledSameProcessRecreation() throws Exception {
        Instrumentation instrumentation = InstrumentationRegistry.getInstrumentation();
        Context target = instrumentation.getTargetContext();
        assertReviewedTestArtifact(target);
        String runId = InstrumentationRegistry.getArguments().getString("run_id", "phase15a_20261018");
        assertTrue("Invalid bounded harness run identifier", runId.matches("[A-Za-z0-9_]{1,48}"));
        String prefix = HARNESS + ".RUN_" + runId;
        String recreateAction = prefix + ".RECREATE";
        String finishAction = prefix + ".FINISH";
        String landscapeAction = prefix + ".LANDSCAPE";
        String portraitAction = prefix + ".PORTRAIT";
        ArrayBlockingQueue<String> commands = new ArrayBlockingQueue<>(4);
        AtomicReference<WeakReference<MainActivity>> latest = new AtomicReference<>(new WeakReference<>(null));
        AtomicReference<Recreation> pending = new AtomicReference<>();
        AtomicReference<Integer> originalRequestedOrientation = new AtomicReference<>();
        Application app = (Application) target.getApplicationContext();
        Application.ActivityLifecycleCallbacks lifecycle = new Application.ActivityLifecycleCallbacks() {
            @Override public void onActivityCreated(Activity activity, Bundle state) {
                if (activity instanceof MainActivity) {
                    latest.set(new WeakReference<>((MainActivity) activity));
                    Recreation ticket = pending.get();
                    if (ticket != null && System.identityHashCode(activity) != ticket.before.activity) {
                        ticket.createdActivity = System.identityHashCode(activity);
                        ticket.savedState = state != null;
                        ticket.created.countDown();
                    }
                    event("ACTIVITY_CREATED", runId, Process.myPid(), System.identityHashCode(activity), 0, 0);
                }
            }
            @Override public void onActivityDestroyed(Activity activity) {
                if (activity instanceof MainActivity) {
                    MainActivity previous = latest.get().get();
                    if (previous == activity) latest.set(new WeakReference<>(null));
                    Recreation ticket = pending.get();
                    if (ticket != null && System.identityHashCode(activity) == ticket.before.activity) ticket.destroyed.countDown();
                    event("ACTIVITY_DESTROYED", runId, Process.myPid(), System.identityHashCode(activity), 0, 0);
                }
            }
            @Override public void onActivityStarted(Activity activity) {}
            @Override public void onActivityResumed(Activity activity) {
                if (!(activity instanceof MainActivity)) return;
                latest.set(new WeakReference<>((MainActivity) activity));
                event("ACTIVITY_RESUMED", runId, Process.myPid(), System.identityHashCode(activity), 0, 0);
                Recreation ticket = pending.get();
                if (ticket != null && ticket.createdActivity == System.identityHashCode(activity)
                        && ticket.createdActivity != ticket.before.activity) {
                    try { ticket.after.set(new Snapshot((MainActivity) activity)); }
                    catch (Throwable failure) { ticket.observationFailure.set(failure); }
                    ticket.resumed.countDown();
                }
            }
            @Override public void onActivityPaused(Activity activity) {}
            @Override public void onActivityStopped(Activity activity) {}
            @Override public void onActivitySaveInstanceState(Activity activity, Bundle state) {}
        };
        BroadcastReceiver control = new BroadcastReceiver() {
            @Override public void onReceive(Context context, Intent intent) {
                if (!TARGET.equals(intent.getPackage())) return;
                String action = intent.getAction();
                if (recreateAction.equals(action) || finishAction.equals(action)
                        || landscapeAction.equals(action) || portraitAction.equals(action)) {
                    if (!commands.offer(action)) event("CONTROL_QUEUE_FULL", runId, Process.myPid(), 0, 0, 0);
                }
            }
        };
        IntentFilter filter = new IntentFilter();
        filter.addAction(recreateAction);
        filter.addAction(finishAction);
        filter.addAction(landscapeAction);
        filter.addAction(portraitAction);
        app.registerActivityLifecycleCallbacks(lifecycle);
        if (Build.VERSION.SDK_INT >= 33) target.registerReceiver(control, filter, Context.RECEIVER_EXPORTED);
        else target.registerReceiver(control, filter);
        int recreations = 0;
        int orientationRequests = 0;
        long deadline = SystemClock.elapsedRealtime() + MAX_LIFETIME_MS;
        try {
            // Use the framework launch and lifecycle monitor, which identify actual
            // instances independently of the consumed Share Intent's filter fields.
            Intent launch = new Intent(target, MainActivity.class).setAction(Intent.ACTION_MAIN)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            instrumentation.startActivitySync(launch);
            instrumentation.waitForIdleSync();
            Snapshot initial = snapshot(instrumentation);
            originalRequestedOrientation.set(initial.requestedOrientation);
            event("READY", runId, initial.pid, initial.activity, initial.webView, recreations);
            boolean finish = false;
            while (!finish) {
                long remaining = deadline - SystemClock.elapsedRealtime();
                assertTrue("Harness control exceeded its 30-minute limit", remaining > 0);
                String command = commands.poll(Math.min(remaining, 30000L), TimeUnit.MILLISECONDS);
                if (command == null) continue;
                if (finishAction.equals(command)) {
                    finish = true;
                    continue;
                }
                if (landscapeAction.equals(command) || portraitAction.equals(command)) {
                    assertTrue("Harness orientation request limit reached", orientationRequests < MAX_ORIENTATION_REQUESTS);
                    boolean landscape = landscapeAction.equals(command);
                    int requested = landscape ? ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE : ActivityInfo.SCREEN_ORIENTATION_PORTRAIT;
                    int expectedConfiguration = landscape ? Configuration.ORIENTATION_LANDSCAPE : Configuration.ORIENTATION_PORTRAIT;
                    Snapshot beforeOrientation = snapshot(instrumentation);
                    orientationEvent("BEFORE_ORIENTATION", runId, beforeOrientation, orientationRequests);
                    onMain(instrumentation, () -> {
                        resumedActivity().setRequestedOrientation(requested);
                        return null;
                    });
                    Snapshot oriented = awaitOrientation(instrumentation, beforeOrientation, expectedConfiguration, requested,
                            Math.min(deadline, SystemClock.elapsedRealtime() + LIFECYCLE_GUARD_MS));
                    assertEquals("The process must survive per-Activity orientation", beforeOrientation.pid, oriented.pid);
                    orientationRequests++;
                    orientationEvent(beforeOrientation.orientation == expectedConfiguration
                            ? "ORIENTATION_ALREADY_CURRENT" : "ORIENTATION_CHANGED", runId, oriented, orientationRequests);
                    continue;
                }
                assertTrue("Harness recreation limit reached", recreations < MAX_RECREATIONS);
                Snapshot before = snapshot(instrumentation);
                Recreation ticket = new Recreation(before);
                assertTrue("A prior recreation remains pending", pending.compareAndSet(null, ticket));
                event("BEFORE_RECREATE", runId, before.pid, before.activity, before.webView, recreations);
                onMain(instrumentation, () -> {
                    MainActivity current = resumedActivity();
                    assertEquals("Visible Activity changed before the framework request", before.activity, System.identityHashCode(current));
                    assertTrue("A finishing Activity cannot be recreated", !current.isFinishing() && !current.isDestroyed());
                    current.recreate();
                    return null;
                });
                long lifecycleDeadline = Math.min(deadline, SystemClock.elapsedRealtime() + LIFECYCLE_GUARD_MS);
                await(ticket.destroyed, lifecycleDeadline, "Old Activity destruction was not observed");
                await(ticket.created, lifecycleDeadline, "New Activity creation was not observed");
                await(ticket.resumed, lifecycleDeadline, "New Activity resume was not observed");
                assertTrue("Lifecycle observation failed", ticket.observationFailure.get() == null);
                instrumentation.waitForIdleSync();
                Snapshot after = snapshot(instrumentation);
                assertEquals("The target process must survive recreation", before.pid, after.pid);
                assertNotEquals("A new Activity instance is required", before.activity, after.activity);
                assertNotEquals("A new WebView instance is required", before.webView, after.webView);
                assertEquals("The resumed Activity must be the newly created instance", ticket.createdActivity, after.activity);
                assertEquals("The observed WebView must belong to that new instance", ticket.after.get().webView, after.webView);
                assertTrue("The recreated Activity did not receive saved instance state", ticket.savedState);
                pending.compareAndSet(ticket, null);
                recreations++;
                event("RECREATED", runId, after.pid, after.activity, after.webView, recreations);
            }
            assertTrue("At least one actual recreation is required", recreations > 0);
            event("FINISHED", runId, Process.myPid(), 0, 0, recreations);
        } finally {
            target.unregisterReceiver(control);
            app.unregisterActivityLifecycleCallbacks(lifecycle);
            onMain(instrumentation, () -> {
                MainActivity current = latest.get().get();
                if (current != null && !current.isFinishing() && !current.isDestroyed()) {
                    Integer original = originalRequestedOrientation.get();
                    if (original != null) {
                        current.setRequestedOrientation(original);
                        assertEquals("Original per-Activity orientation was not restored", original.intValue(), current.getRequestedOrientation());
                        orientationEvent("ORIENTATION_REQUEST_RESTORED", runId, new Snapshot(current), 0);
                    }
                    current.finish();
                }
                return null;
            });
        }
    }

    private static Snapshot snapshot(Instrumentation instrumentation) throws Exception {
        return onMain(instrumentation, () -> new Snapshot(resumedActivity()));
    }

    private static MainActivity resumedActivity() {
        MainActivity current = findResumedActivity();
        assertTrue("The real MainActivity must be resumed before control", current != null);
        return current;
    }

    private static MainActivity findResumedActivity() {
        Collection<Activity> resumed = ActivityLifecycleMonitorRegistry.getInstance().getActivitiesInStage(Stage.RESUMED);
        MainActivity current = null;
        for (Activity activity : resumed) {
            if (activity instanceof MainActivity) {
                assertTrue("Multiple MainActivity instances are resumed", current == null);
                current = (MainActivity) activity;
            }
        }
        return current;
    }

    private static Snapshot awaitOrientation(Instrumentation instrumentation, Snapshot before, int expected, int requested,
            long deadline) throws Exception {
        while (SystemClock.elapsedRealtime() < deadline) {
            Snapshot value = onMain(instrumentation, () -> {
                MainActivity current = findResumedActivity();
                return current == null ? null : new Snapshot(current);
            });
            if (value != null && value.orientation == expected && value.requestedOrientation == requested
                    && value.width > 0 && value.height > 0
                    && (before.orientation == expected || value.width != before.width || value.height != before.height)) return value;
            // Observe an asynchronous resource/layout change, never assume success after a sleep.
            Thread.sleep(50L);
        }
        throw new AssertionError("Per-Activity orientation/configuration/viewport transition was not observed within the harness guard");
    }

    private static void await(CountDownLatch latch, long deadline, String message) throws InterruptedException {
        long remaining = deadline - SystemClock.elapsedRealtime();
        assertTrue(message, remaining > 0 && latch.await(remaining, TimeUnit.MILLISECONDS));
    }

    private static <T> T onMain(Instrumentation instrumentation, MainAction<T> action) throws Exception {
        AtomicReference<T> value = new AtomicReference<>();
        AtomicReference<Throwable> failure = new AtomicReference<>();
        instrumentation.runOnMainSync(() -> {
            try { value.set(action.run()); }
            catch (Throwable error) { failure.set(error); }
        });
        Throwable error = failure.get();
        if (error instanceof Exception) throw (Exception) error;
        if (error instanceof Error) throw (Error) error;
        if (error != null) throw new AssertionError("Unexpected harness main-thread failure", error);
        return value.get();
    }

    @SuppressWarnings("deprecation")
    private static void assertReviewedTestArtifact(Context target) throws Exception {
        assertEquals("Unexpected target package", TARGET, target.getPackageName());
        PackageManager manager = target.getPackageManager();
        ApplicationInfo info = manager.getApplicationInfo(TARGET, 0);
        assertTrue("Only a debuggable TEST target is allowed", (info.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0);
        try (InputStream apk = new FileInputStream(info.sourceDir)) {
            assertEquals("The installed target is not the exact reviewed retained-signer TEST APK", EXPECTED_APK, digest(apk));
        }
        PackageInfo packageInfo = manager.getPackageInfo(TARGET,
                Build.VERSION.SDK_INT >= 28 ? PackageManager.GET_SIGNING_CERTIFICATES : PackageManager.GET_SIGNATURES);
        Signature[] signatures = Build.VERSION.SDK_INT >= 28
                ? packageInfo.signingInfo.getApkContentsSigners() : packageInfo.signatures;
        assertEquals("Unexpected signer count", 1, signatures.length);
        assertEquals("The retained debug signer is required", EXPECTED_SIGNER, hex(MessageDigest.getInstance("SHA-256").digest(signatures[0].toByteArray())));
        try (InputStream config = target.getAssets().open("capacitor.config.json")) {
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];
            int count;
            while ((count = config.read(buffer)) != -1) {
                assertTrue("Unexpected oversized Capacitor configuration", output.size() + count <= 65536);
                output.write(buffer, 0, count);
            }
            JSONObject parsed = new JSONObject(new String(output.toByteArray(), StandardCharsets.UTF_8));
            JSONObject server = parsed.getJSONObject("server");
            assertEquals("Only localhost TEST WebView is allowed", "localhost", server.getString("hostname"));
            assertEquals("TEST HTTPS is required", "https", server.getString("androidScheme"));
            assertTrue("Live-reload/remote WebView is prohibited", !server.has("url"));
            assertTrue("Cleartext TEST origin is prohibited", !server.optBoolean("cleartext", false));
        }
    }

    private static String digest(InputStream input) throws Exception {
        MessageDigest hash = MessageDigest.getInstance("SHA-256");
        byte[] buffer = new byte[65536];
        int count;
        while ((count = input.read(buffer)) != -1) hash.update(buffer, 0, count);
        return hex(hash.digest());
    }

    private static String hex(byte[] bytes) {
        StringBuilder output = new StringBuilder(bytes.length * 2);
        for (byte value : bytes) output.append(String.format(java.util.Locale.ROOT, "%02x", value & 255));
        return output.toString();
    }

    private static void event(String stage, String runId, int pid, int activity, int webView, int recreations) {
        Log.i(TAG, "{\"stage\":\"" + stage + "\",\"runId\":\"" + runId + "\",\"pid\":" + pid
                + ",\"activity\":" + activity + ",\"webView\":" + webView + ",\"recreations\":" + recreations + "}");
    }

    private static void orientationEvent(String stage, String runId, Snapshot value, int requests) {
        Log.i(TAG, "{\"stage\":\"" + stage + "\",\"runId\":\"" + runId + "\",\"pid\":" + value.pid
                + ",\"activity\":" + value.activity + ",\"webView\":" + value.webView + ",\"orientation\":" + value.orientation
                + ",\"requestedOrientation\":" + value.requestedOrientation + ",\"widthPx\":" + value.width
                + ",\"heightPx\":" + value.height + ",\"requests\":" + requests + "}");
    }
}
