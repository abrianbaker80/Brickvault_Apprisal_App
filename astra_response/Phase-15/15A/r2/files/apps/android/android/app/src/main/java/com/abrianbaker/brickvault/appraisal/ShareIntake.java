package com.abrianbaker.brickvault.appraisal;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Volatile, bounded custody of explicitly shared bytes. No Android storage or network. */
final class ShareIntake {
    static final int MAX_ITEMS = 8;
    static final int MAX_FILE_BYTES = 25 * 1024 * 1024;
    static final int MAX_TOTAL_BYTES = 50 * 1024 * 1024;
    static final int MAX_CHUNK_BYTES = 256 * 1024;

    interface Opener { InputStream open() throws IOException; }
    interface MimeResolver { String resolve(); }

    static final class Source {
        final String mimeType;
        final String errorCode;
        final Opener opener;
        final MimeResolver mimeResolver;

        Source(String mimeType, String errorCode, Opener opener) {
            this.mimeType = mimeType;
            this.errorCode = errorCode;
            this.opener = opener;
            this.mimeResolver = null;
        }

        Source(MimeResolver mimeResolver, Opener opener) {
            this.mimeType = null;
            this.errorCode = null;
            this.opener = opener;
            this.mimeResolver = mimeResolver;
        }
    }

    static final class Item {
        final String id = UUID.randomUUID().toString();
        final int index;
        String filename;
        String mimeType;
        String errorCode;
        byte[] bytes;
        boolean finished;

        Item(int index, String mimeType, String errorCode) {
            this.index = index;
            this.mimeType = mimeType;
            this.errorCode = errorCode;
            filename = neutralFilename(index, mimeType);
            finished = errorCode != null;
        }

    }

    static final class ItemView {
        final String id, filename, mimeType, state, errorCode;
        final int index, byteCount;

        ItemView(Item item) {
            id = item.id;
            index = item.index;
            filename = item.filename;
            mimeType = item.mimeType;
            state = !item.finished ? "pending" : item.errorCode == null ? "ready" : "failed";
            errorCode = item.errorCode;
            byteCount = item.bytes == null ? 0 : item.bytes.length;
        }
    }

    static final class View {
        final String id, state;
        final List<ItemView> items;
        final UploadContext queueContext;
        final ReviewContext reviewContext;
        final boolean handedOff;

        View(String id, List<Item> originals, UploadContext queueContext, ReviewContext reviewContext, boolean handedOff) {
            this.id = id;
            this.queueContext = queueContext;
            this.reviewContext = reviewContext;
            this.handedOff = handedOff;
            items = new ArrayList<>();
            boolean ready = true;
            for (Item item : originals) {
                items.add(new ItemView(item));
                ready &= item.finished;
            }
            state = ready ? "ready" : "reading";
        }
    }

    static final class ContextItem {
        final String itemId, clientUploadId;
        final int displayOrder;
        ContextItem(String itemId, String clientUploadId, int displayOrder) {
            if (!canonicalUuid(itemId) || !canonicalUuid(clientUploadId) || displayOrder < 0 || displayOrder > 2147483646)
                throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
            this.itemId = itemId;
            this.clientUploadId = clientUploadId;
            this.displayOrder = displayOrder;
        }
        @Override public boolean equals(Object other) {
            if (!(other instanceof ContextItem)) return false;
            ContextItem value = (ContextItem) other;
            return itemId.equals(value.itemId) && clientUploadId.equals(value.clientUploadId) && displayOrder == value.displayOrder;
        }
        @Override public int hashCode() { return Objects.hash(itemId, clientUploadId, displayOrder); }
    }

    static final class UploadContext {
        final String listingId;
        final List<ContextItem> items;
        UploadContext(String listingId, List<ContextItem> entries) {
            if (!canonicalUuid(listingId) || entries.isEmpty() || entries.size() > MAX_ITEMS)
                throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
            this.listingId = listingId;
            this.items = Collections.unmodifiableList(new ArrayList<>(entries));
        }
        @Override public boolean equals(Object other) {
            if (!(other instanceof UploadContext)) return false;
            UploadContext value = (UploadContext) other;
            return listingId.equals(value.listingId) && items.equals(value.items);
        }
        @Override public int hashCode() { return Objects.hash(listingId, items); }
    }

    static final class ReviewContext {
        final List<String> selectedItemIds;
        final boolean creationUncertain;
        ReviewContext(List<String> selectedItemIds, boolean creationUncertain) {
            if (selectedItemIds.size() > MAX_ITEMS || selectedItemIds.stream().anyMatch(id -> !canonicalUuid(id))
                    || new HashSet<>(selectedItemIds).size() != selectedItemIds.size())
                throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
            this.selectedItemIds = Collections.unmodifiableList(new ArrayList<>(selectedItemIds));
            this.creationUncertain = creationUncertain;
        }
    }

    static final class Work {
        final long revision;
        final String batchId;
        Work(long revision, String batchId) { this.revision = revision; this.batchId = batchId; }
    }

    private String batchId, notice;
    private final List<Source> sources = new ArrayList<>();
    private final List<Item> items = new ArrayList<>();
    private boolean sessionKnown, authenticated, foreground, reading;
    private long revision;
    private InputStream activeStream;
    private Runnable listener = () -> {};
    private Object owner;
    private UploadContext queueContext;
    private ReviewContext reviewContext;
    private boolean handedOff;

    void attach(Object nextOwner, Runnable nextListener) {
        InputStream close;
        synchronized (this) {
            owner = nextOwner;
            listener = nextListener;
            sessionKnown = false;
            authenticated = false;
            foreground = false;
            revision++;
            reading = false;
            close = activeStream;
            activeStream = null;
        }
        close(close);
    }

    void foreground(Object currentOwner, boolean value) {
        InputStream close = null;
        synchronized (this) {
            if (owner != currentOwner) return;
            foreground = value;
            if (!value) {
                sessionKnown = false;
                authenticated = false;
                revision++;
                reading = false;
                close = activeStream;
                activeStream = null;
            }
        }
        close(close);
        changed();
    }

    void detach(Object currentOwner, boolean discard) {
        InputStream close;
        synchronized (this) {
            if (owner != currentOwner) return;
            owner = null;
            listener = () -> {};
            foreground = false;
            sessionKnown = false;
            authenticated = false;
            revision++;
            reading = false;
            close = discard ? clearLocked() : activeStream;
            activeStream = null;
        }
        close(close);
    }

    void session(boolean value) {
        InputStream close = null;
        synchronized (this) {
            if (value && !foreground) return; // A delayed background reply cannot authorize resume.
            sessionKnown = true;
            authenticated = value;
            if (!value) {
                boolean hadIntake = batchId != null;
                close = clearLocked();
                if (hadIntake) notice = "SIGN_IN_AND_RESHARE";
            }
        }
        close(close);
        changed();
    }

    boolean receive(List<Source> incoming, boolean overflow) {
        synchronized (this) {
            if (sessionKnown && !authenticated) {
                notice = "SIGN_IN_AND_RESHARE";
                return false;
            }
            if (batchId != null) {
                notice = "SHARE_BUSY";
                return false;
            }
            if (incoming.isEmpty()) {
                notice = "SHARE_INVALID";
                return false;
            }
            batchId = UUID.randomUUID().toString();
            notice = overflow ? "ITEM_COUNT_LIMIT" : null;
            for (int i = 0; i < Math.min(incoming.size(), MAX_ITEMS); i++) {
                Source source = incoming.get(i);
                sources.add(source);
                items.add(new Item(i, source.mimeType, source.errorCode));
            }
            if (overflow) items.add(new Item(MAX_ITEMS, null, "ITEM_COUNT_LIMIT"));
        }
        changed();
        return true;
    }

    synchronized void notice(String code) { notice = code; }
    synchronized String notice() { return notice; }
    synchronized View view() {
        return sessionKnown && authenticated && batchId != null ? new View(batchId, items, queueContext, reviewContext, handedOff) : null;
    }

    synchronized Work begin() {
        if (!sessionKnown || !authenticated || !foreground || reading || batchId == null
                || items.stream().allMatch(item -> item.finished)) return null;
        reading = true;
        return new Work(++revision, batchId);
    }

    void read(Work work) {
        try {
            for (int i = 0; i < sourcesCount(work); i++) {
                Source source;
                int ceiling;
                synchronized (this) {
                    if (!permitted(work)) return;
                    if (items.get(i).finished) continue;
                    source = sources.get(i);
                    int total = items.stream().mapToInt(item -> item.bytes == null ? 0 : item.bytes.length).sum();
                    ceiling = Math.min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total);
                }
                byte[] result = null;
                String error = null;
                String mime = source.mimeType;
                try {
                    if (source.mimeResolver != null) mime = source.mimeResolver.resolve();
                    synchronized (this) { if (!permitted(work)) return; }
                    if (!supportedMime(mime)) {
                        error = "UNSUPPORTED_MIME";
                        mime = null;
                    } else {
                        try (InputStream stream = source.opener.open()) {
                            if (stream == null) throw new IOException("missing_stream");
                            synchronized (this) {
                                if (!permitted(work)) return;
                                activeStream = stream;
                            }
                            ByteArrayOutputStream output = new ByteArrayOutputStream();
                            byte[] buffer = new byte[64 * 1024];
                            while (true) {
                                synchronized (this) { if (!permitted(work)) return; }
                                int read = stream.read(buffer, 0, Math.min(buffer.length, ceiling - output.size() + 1));
                                if (read == -1) break;
                                if (read == 0) throw new IOException("empty_stream_read");
                                if (output.size() + read > ceiling) {
                                    error = ceiling < MAX_FILE_BYTES ? "SHARE_TOTAL_TOO_LARGE" : "IMAGE_FILE_TOO_LARGE";
                                    break;
                                }
                                output.write(buffer, 0, read);
                            }
                            if (error == null) result = output.toByteArray();
                        }
                    }
                } catch (IOException | RuntimeException exception) {
                    error = "URI_UNREADABLE";
                } finally {
                    synchronized (this) { if (revision == work.revision) activeStream = null; }
                }
                synchronized (this) {
                    if (!permitted(work)) return;
                    Item item = items.get(i);
                    item.mimeType = mime;
                    item.filename = neutralFilename(i, mime);
                    item.bytes = error == null ? result : null;
                    item.errorCode = error;
                    item.finished = true;
                    // Once snapshotted (or failed), discard the content URI closure.
                    sources.set(i, null);
                }
                changed();
            }
        } finally {
            synchronized (this) { if (revision == work.revision) reading = false; }
            changed();
        }
    }

    private synchronized int sourcesCount(Work work) { return permitted(work) ? sources.size() : 0; }
    private boolean permitted(Work work) {
        return revision == work.revision && authenticated && sessionKnown && foreground && work.batchId.equals(batchId);
    }

    synchronized byte[] chunk(String requestedBatch, String itemId, int offset, int length) {
        if (!authenticated || !sessionKnown || !foreground || batchId == null || !batchId.equals(requestedBatch))
            throw new IllegalArgumentException("SHARE_UNAVAILABLE");
        Item item = items.stream().filter(value -> value.id.equals(itemId)).findFirst()
                .orElseThrow(() -> new IllegalArgumentException("SHARE_UNAVAILABLE"));
        if (!item.finished || item.errorCode != null || item.bytes == null)
            throw new IllegalArgumentException("SHARE_UNAVAILABLE");
        if (offset < 0 || offset > item.bytes.length || length < 1 || length > MAX_CHUNK_BYTES)
            throw new IllegalArgumentException("INVALID_CHUNK");
        return Arrays.copyOfRange(item.bytes, offset, offset + Math.min(length, item.bytes.length - offset));
    }

    synchronized int byteCount(String requestedBatch, String itemId) {
        if (!authenticated || !sessionKnown || !foreground || batchId == null || !batchId.equals(requestedBatch))
            throw new IllegalArgumentException("SHARE_UNAVAILABLE");
        return items.stream().filter(item -> item.id.equals(itemId) && item.bytes != null)
                .findFirst().orElseThrow(() -> new IllegalArgumentException("SHARE_UNAVAILABLE")).bytes.length;
    }

    void clear(String requestedBatch, boolean acknowledge) {
        InputStream close;
        synchronized (this) {
            if (requestedBatch != null && !requestedBatch.equals(batchId)) throw new IllegalArgumentException("SHARE_UNAVAILABLE");
            if (acknowledge && (batchId == null || !authenticated || !sessionKnown || !foreground
                    || items.stream().anyMatch(item -> !item.finished))) throw new IllegalArgumentException("SHARE_UNAVAILABLE");
            if (acknowledge) {
                // Retain bounded originals in this process so a recreated WebView can
                // recover the same bytes/UUID/order. No disk or upload replay lives here.
                handedOff = true;
                close = null;
            } else close = clearLocked();
            notice = null;
        }
        close(close);
        changed();
    }

    synchronized void saveContext(String requestedBatch, UploadContext context) {
        if (!authenticated || !sessionKnown || !foreground || batchId == null || !batchId.equals(requestedBatch)
                || !handedOff || items.stream().anyMatch(item -> !item.finished))
            throw new IllegalArgumentException("SHARE_UNAVAILABLE");
        if (queueContext != null) {
            if (!queueContext.equals(context)) throw new IllegalArgumentException("SHARE_CONTEXT_CONFLICT");
            return; // A context replay never revives an intentionally retired file.
        }
        Set<String> identities = new HashSet<>(), uploads = new HashSet<>();
        Set<Integer> positions = new HashSet<>();
        for (ContextItem entry : context.items) {
            if (items.stream().noneMatch(item -> item.id.equals(entry.itemId) && item.finished && item.errorCode == null && item.bytes != null)
                    || !identities.add(entry.itemId) || !uploads.add(entry.clientUploadId) || !positions.add(entry.displayOrder))
                throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
        }
        if (reviewContext != null && !new HashSet<>(reviewContext.selectedItemIds).equals(identities))
            throw new IllegalArgumentException("SHARE_CONTEXT_CONFLICT");
        queueContext = context;
        List<String> selected = new ArrayList<>();
        for (ContextItem entry : context.items) selected.add(entry.itemId);
        reviewContext = new ReviewContext(selected, false);
    }

    synchronized void saveReview(String requestedBatch, ReviewContext context) {
        if (!authenticated || !sessionKnown || !foreground || batchId == null || !batchId.equals(requestedBatch)
                || !handedOff || items.stream().anyMatch(item -> !item.finished))
            throw new IllegalArgumentException("SHARE_UNAVAILABLE");
        for (String selected : context.selectedItemIds) {
            if (items.stream().noneMatch(item -> item.id.equals(selected) && item.finished && item.errorCode == null && item.bytes != null))
                throw new IllegalArgumentException("INVALID_SHARE_CONTEXT");
        }
        if (queueContext != null) {
            Set<String> previouslySelected = new HashSet<>(reviewContext.selectedItemIds);
            if (context.creationUncertain || !previouslySelected.containsAll(context.selectedItemIds))
                throw new IllegalArgumentException("SHARE_CONTEXT_CONFLICT");
            previouslySelected.removeAll(context.selectedItemIds);
            for (Item item : items) {
                if (previouslySelected.contains(item.id)) {
                    item.bytes = null;
                    item.errorCode = "SHARE_REMOVED";
                }
            }
        }
        if (reviewContext != null && reviewContext.creationUncertain && !new HashSet<>(reviewContext.selectedItemIds)
                .equals(new HashSet<>(context.selectedItemIds))) throw new IllegalArgumentException("SHARE_CONTEXT_CONFLICT");
        reviewContext = context;
    }

    private InputStream clearLocked() {
        revision++;
        reading = false;
        batchId = null;
        sources.clear();
        items.clear();
        queueContext = null;
        reviewContext = null;
        handedOff = false;
        InputStream close = activeStream;
        activeStream = null;
        return close;
    }

    private void changed() { Runnable current; synchronized (this) { current = listener; } current.run(); }
    private static boolean supportedMime(String mime) {
        return "image/jpeg".equals(mime) || "image/png".equals(mime) || "image/webp".equals(mime);
    }
    private static boolean canonicalUuid(String value) {
        if (value == null || value.length() != 36) return false;
        try { return UUID.fromString(value).toString().equals(value); }
        catch (IllegalArgumentException exception) { return false; }
    }
    private static String neutralFilename(int index, String mime) {
        String extension = "image/jpeg".equals(mime) ? "jpg" : "image/png".equals(mime) ? "png"
                : "image/webp".equals(mime) ? "webp" : "bin";
        return index < MAX_ITEMS ? "shared-image-" + (index + 1) + "." + extension : "additional-shared-images";
    }
    private static void close(InputStream stream) {
        if (stream != null) try { stream.close(); } catch (IOException ignored) { /* No private exception text. */ }
    }
}
