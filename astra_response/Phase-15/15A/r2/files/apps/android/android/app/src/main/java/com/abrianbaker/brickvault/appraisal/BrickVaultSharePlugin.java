package com.abrianbaker.brickvault.appraisal;

import android.content.ClipData;
import android.content.ContentResolver;
import android.content.Intent;
import android.net.Uri;
import android.os.BadParcelableException;
import android.util.Base64;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.json.JSONException;
import org.json.JSONObject;

/** Receive-only local bridge. Credentials, backend HTTP and persisted images never enter here. */
@CapacitorPlugin(name = "BrickVaultShare")
public final class BrickVaultSharePlugin extends Plugin {
    private static final ShareIntake INTAKE = new ShareIntake();
    // At most one active read and one replacement task after a lifecycle interruption.
    private static final ThreadPoolExecutor READER = new ThreadPoolExecutor(
            1, 1, 30, TimeUnit.SECONDS, new ArrayBlockingQueue<>(1),
            new ThreadPoolExecutor.DiscardOldestPolicy());
    static { READER.allowCoreThreadTimeOut(true); }

    @Override
    public void load() {
        INTAKE.attach(this, this::changed);
    }

    private void changed() {
        notifyListeners("shareAvailable", new JSObject());
        ShareIntake.Work work = INTAKE.begin();
        if (work != null) READER.execute(() -> INTAKE.read(work));
    }

    @Override
    protected void handleOnResume() { INTAKE.foreground(this, true); }

    @Override
    protected void handleOnPause() { INTAKE.foreground(this, false); }

    @Override
    protected void handleOnDestroy() { INTAKE.detach(this, getActivity().isFinishing()); }

    @Override
    protected void handleOnNewIntent(Intent intent) {
        if (!Intent.ACTION_SEND.equals(intent.getAction()) && !Intent.ACTION_SEND_MULTIPLE.equals(intent.getAction())) return;
        try {
            accept(intent);
        } catch (BadParcelableException | ClassCastException | IllegalArgumentException exception) {
            INTAKE.notice("AMBIGUOUS_STREAMS".equals(exception.getMessage()) ? "AMBIGUOUS_STREAMS" : "SHARE_INVALID");
        }
        changed();
    }

    @SuppressWarnings("deprecation")
    private void accept(Intent intent) {
        List<Object> raw = new ArrayList<>();
        int count;
        ClipData clip = intent.getClipData();
        if (intent.hasExtra(Intent.EXTRA_STREAM)) {
            if (Intent.ACTION_SEND.equals(intent.getAction())) {
                raw.add(intent.getParcelableExtra(Intent.EXTRA_STREAM));
                count = 1;
            } else {
                ArrayList<?> streams = intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM);
                if (streams == null) throw new IllegalArgumentException("invalid_streams");
                count = streams.size();
                for (int i = 0; i < Math.min(count, ShareIntake.MAX_ITEMS); i++) raw.add(streams.get(i));
            }
            if (clip != null) {
                if (clip.getItemCount() != count) throw new IllegalArgumentException("AMBIGUOUS_STREAMS");
                for (int i = 0; i < raw.size(); i++) {
                    if (!(raw.get(i) instanceof Uri) || !raw.get(i).equals(clip.getItemAt(i).getUri())) {
                        throw new IllegalArgumentException("AMBIGUOUS_STREAMS");
                    }
                }
            }
        } else {
            count = clip == null ? 0 : clip.getItemCount();
            for (int i = 0; i < Math.min(count, ShareIntake.MAX_ITEMS); i++) raw.add(clip.getItemAt(i).getUri());
        }
        if (Intent.ACTION_SEND.equals(intent.getAction()) && count != 1) throw new IllegalArgumentException("invalid_single_stream");
        ContentResolver resolver = getContext().getApplicationContext().getContentResolver();
        String declaredMime = intent.getType();
        List<ShareIntake.Source> sources = new ArrayList<>();
        for (Object value : raw) {
            if (!(value instanceof Uri) || !"content".equals(((Uri) value).getScheme())
                    || ((Uri) value).getAuthority() == null || ((Uri) value).getAuthority().isEmpty()) {
                sources.add(new ShareIntake.Source(null, "INVALID_CONTENT_URI", null));
                continue;
            }
            Uri uri = (Uri) value;
            sources.add(new ShareIntake.Source(() -> {
                String resolvedMime = resolver.getType(uri);
                return resolvedMime == null ? declaredMime : resolvedMime;
            }, () -> resolver.openInputStream(uri)));
        }
        INTAKE.receive(sources, count > ShareIntake.MAX_ITEMS);
    }

    @PluginMethod
    public void setSession(PluginCall call) {
        Boolean authenticated = call.getBoolean("authenticated");
        if (authenticated == null) { call.reject("INVALID_SESSION_STATE"); return; }
        INTAKE.session(authenticated);
        call.resolve();
    }

    @PluginMethod
    public void getPendingShare(PluginCall call) {
        ShareIntake.View view = INTAKE.view();
        JSObject response = new JSObject();
        response.put("notice", INTAKE.notice() == null ? JSObject.NULL : INTAKE.notice());
        if (view == null) {
            response.put("batch", JSObject.NULL);
        } else {
            JSObject batch = new JSObject();
            batch.put("id", view.id);
            batch.put("state", view.state);
            batch.put("handedOff", view.handedOff);
            JSArray items = new JSArray();
            for (ShareIntake.ItemView value : view.items) {
                JSObject item = new JSObject();
                item.put("id", value.id);
                item.put("index", value.index);
                item.put("filename", value.filename);
                item.put("mimeType", value.mimeType == null ? JSObject.NULL : value.mimeType);
                item.put("byteCount", value.byteCount);
                item.put("state", value.state);
                item.put("errorCode", value.errorCode == null ? JSObject.NULL : value.errorCode);
                items.put(item);
            }
            batch.put("items", items);
            if (view.reviewContext == null) {
                batch.put("reviewContext", JSObject.NULL);
            } else {
                JSObject review = new JSObject();
                JSArray selection = new JSArray();
                for (String selected : view.reviewContext.selectedItemIds) selection.put(selected);
                review.put("selectedItemIds", selection);
                review.put("creationUncertain", view.reviewContext.creationUncertain);
                batch.put("reviewContext", review);
            }
            if (view.queueContext == null) {
                batch.put("queueContext", JSObject.NULL);
            } else {
                JSObject context = new JSObject();
                context.put("listingId", view.queueContext.listingId);
                JSArray entries = new JSArray();
                for (ShareIntake.ContextItem value : view.queueContext.items) {
                    JSObject entry = new JSObject();
                    entry.put("itemId", value.itemId);
                    entry.put("clientUploadId", value.clientUploadId);
                    entry.put("displayOrder", value.displayOrder);
                    entries.put(entry);
                }
                context.put("items", entries);
                batch.put("queueContext", context);
            }
            response.put("batch", batch);
        }
        call.resolve(response);
    }

    @PluginMethod
    public void readChunk(PluginCall call) {
        String batch = call.getString("batchId");
        String item = call.getString("itemId");
        Integer offset = call.getInt("offset");
        Integer length = call.getInt("length");
        if (batch == null || item == null || offset == null || length == null) { call.reject("INVALID_CHUNK"); return; }
        try {
            byte[] bytes = INTAKE.chunk(batch, item, offset, length);
            int total = INTAKE.byteCount(batch, item);
            JSObject result = new JSObject();
            result.put("data", Base64.encodeToString(bytes, Base64.NO_WRAP));
            result.put("byteCount", bytes.length);
            result.put("eof", offset + bytes.length == total);
            call.resolve(result);
        } catch (IllegalArgumentException exception) { call.reject(exception.getMessage()); }
    }

    @PluginMethod
    public void acknowledgeShare(PluginCall call) {
        String batch = call.getString("batchId");
        if (batch == null) { call.reject("SHARE_UNAVAILABLE"); return; }
        try { INTAKE.clear(batch, true); call.resolve(); }
        catch (IllegalArgumentException exception) { call.reject(exception.getMessage()); }
    }

    @PluginMethod
    public void saveUploadContext(PluginCall call) {
        String batch = call.getString("batchId");
        String listing = call.getString("listingId");
        JSArray entries = call.getArray("items");
        if (batch == null || entries == null || entries.length() < 1 || entries.length() > ShareIntake.MAX_ITEMS) {
            call.reject("INVALID_SHARE_CONTEXT");
            return;
        }
        try {
            List<ShareIntake.ContextItem> items = new ArrayList<>();
            for (int i = 0; i < entries.length(); i++) {
                JSONObject entry = entries.getJSONObject(i);
                if (entry.length() != 3 || !entry.has("itemId") || !entry.has("clientUploadId") || !entry.has("displayOrder"))
                    throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
                Object rawOrder = entry.get("displayOrder");
                if (!(rawOrder instanceof Number)) throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
                Number order = (Number) rawOrder;
                if (order.longValue() < 0 || order.longValue() > 2147483646 || order.doubleValue() != order.longValue())
                    throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
                items.add(new ShareIntake.ContextItem(entry.getString("itemId"), entry.getString("clientUploadId"), order.intValue()));
            }
            INTAKE.saveContext(batch, new ShareIntake.UploadContext(listing, items));
            call.resolve();
        } catch (JSONException exception) { call.reject("INVALID_SHARE_CONTEXT"); }
        catch (IllegalArgumentException exception) { call.reject(exception.getMessage()); }
    }

    @PluginMethod
    public void saveReviewContext(PluginCall call) {
        String batch = call.getString("batchId");
        JSArray entries = call.getArray("selectedItemIds");
        Boolean uncertain = call.getBoolean("creationUncertain");
        if (batch == null || entries == null || uncertain == null || entries.length() > ShareIntake.MAX_ITEMS) {
            call.reject("INVALID_SHARE_CONTEXT");
            return;
        }
        try {
            List<String> selection = new ArrayList<>();
            for (int i = 0; i < entries.length(); i++) {
                Object value = entries.get(i);
                if (!(value instanceof String)) throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
                selection.add((String) value);
            }
            INTAKE.saveReview(batch, new ShareIntake.ReviewContext(selection, uncertain));
            call.resolve();
        } catch (JSONException exception) { call.reject("INVALID_SHARE_CONTEXT"); }
        catch (IllegalArgumentException exception) { call.reject(exception.getMessage()); }
    }

    @PluginMethod
    public void cancelShare(PluginCall call) {
        try { INTAKE.clear(call.getString("batchId"), false); call.resolve(); }
        catch (IllegalArgumentException exception) { call.reject(exception.getMessage()); }
    }
}
