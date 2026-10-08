package com.abrianbaker.brickvault.appraisal;

import static org.junit.Assert.*;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.Test;

public class ShareIntakeTest {
    private final Object owner = new Object();

    private ShareIntake intake() {
        ShareIntake value = new ShareIntake();
        value.attach(owner, () -> {});
        return value;
    }

    private ShareIntake.Source source(byte[] bytes) {
        return new ShareIntake.Source("image/png", null, () -> new ByteArrayInputStream(bytes));
    }

    private void start(ShareIntake value) {
        value.foreground(owner, true);
        value.session(true);
        ShareIntake.Work work = value.begin();
        assertNotNull(work);
        value.read(work);
    }

    @Test
    public void coldShareWaitsForVerifiedForegroundAndSignedOutDiscards() {
        ShareIntake value = intake();
        AtomicInteger opened = new AtomicInteger();
        value.receive(List.of(new ShareIntake.Source("image/png", null, () -> {
            opened.incrementAndGet();
            return new ByteArrayInputStream(new byte[] { 1 });
        })), false);
        assertNull(value.view());
        assertNull(value.begin());
        value.foreground(owner, true);
        assertNull(value.begin());
        value.session(false);
        value.session(true);
        assertNull(value.view());
        assertEquals(0, opened.get());
        assertEquals("SIGN_IN_AND_RESHARE", value.notice());
    }

    @Test
    public void providerMimeResolutionWaitsForSessionAndUnsupportedMimeNeverOpensBytes() {
        ShareIntake value = intake();
        AtomicInteger resolved = new AtomicInteger(), opened = new AtomicInteger();
        ShareIntake.Source unsupported = new ShareIntake.Source(() -> {
            resolved.incrementAndGet();
            return "image/gif";
        }, () -> { opened.incrementAndGet(); return new ByteArrayInputStream(new byte[] { 1 }); });
        value.receive(List.of(unsupported), false);
        value.foreground(owner, true);
        assertNull(value.begin());
        assertEquals(0, resolved.get());
        value.session(false);
        assertEquals(0, resolved.get());
        value.session(true);
        ShareIntake.Source throwingProvider = new ShareIntake.Source(() -> {
            throw new IllegalStateException("private provider detail");
        }, () -> { opened.incrementAndGet(); return new ByteArrayInputStream(new byte[] { 9 }); });
        value.receive(List.of(unsupported, source(new byte[] { 7 }), throwingProvider), false);
        value.read(value.begin());
        assertEquals(1, resolved.get());
        assertEquals(0, opened.get());
        assertEquals("UNSUPPORTED_MIME", value.view().items.get(0).errorCode);
        assertEquals("shared-image-1.bin", value.view().items.get(0).filename);
        assertEquals("ready", value.view().items.get(1).state);
        assertEquals("URI_UNREADABLE", value.view().items.get(2).errorCode);
    }

    @Test
    public void pauseResumeRequiresFreshSessionVerificationAndKeepsExactIdentity() {
        ShareIntake value = intake();
        byte[] original = { 0, 1, 2, -1, 10 };
        value.receive(List.of(source(original)), false);
        start(value);
        ShareIntake.View before = value.view();
        value.foreground(owner, false);
        value.session(true); // A late verification reply while paused must not authorize resume.
        value.foreground(owner, true);
        assertNull(value.view());
        assertNull(value.begin());
        assertThrows(IllegalArgumentException.class, () -> value.chunk(before.id, before.items.get(0).id, 0, 3));
        value.session(true);
        ShareIntake.View after = value.view();
        assertEquals(before.id, after.id);
        assertEquals(before.items.get(0).id, after.items.get(0).id);
        assertArrayEquals(original, value.chunk(after.id, after.items.get(0).id, 0, 100));
    }

    @Test
    public void independentFailureAndDuplicateEntriesKeepOriginalOrderAndBytes() {
        ShareIntake value = intake();
        byte[] original = { 12, 3, -1 };
        AtomicInteger closed = new AtomicInteger();
        value.receive(List.of(source(original), new ShareIntake.Source("image/png", null, () -> new InputStream() {
            @Override public int read() throws IOException { throw new IOException("private provider text"); }
            @Override public void close() { closed.incrementAndGet(); }
        }), source(original)), false);
        start(value);
        ShareIntake.View view = value.view();
        assertEquals("ready", view.state);
        assertEquals("ready", view.items.get(0).state);
        assertEquals("URI_UNREADABLE", view.items.get(1).errorCode);
        assertEquals("ready", view.items.get(2).state);
        assertEquals(1, closed.get());
        assertNotEquals(view.items.get(0).id, view.items.get(2).id);
        assertEquals("shared-image-3.png", view.items.get(2).filename);
        assertArrayEquals(original, value.chunk(view.id, view.items.get(0).id, 0, 100));
        assertArrayEquals(original, value.chunk(view.id, view.items.get(2).id, 0, 100));
    }

    private static InputStream sized(int length, AtomicInteger readCount, AtomicInteger closes) {
        return new InputStream() {
            private int remaining = length;
            @Override public int read() {
                if (remaining == 0) return -1;
                remaining--;
                readCount.incrementAndGet();
                return 7;
            }
            @Override public int read(byte[] target, int offset, int count) {
                if (remaining == 0) return -1;
                int delivered = Math.min(remaining, count);
                java.util.Arrays.fill(target, offset, offset + delivered, (byte) 7);
                remaining -= delivered;
                readCount.addAndGet(delivered);
                return delivered;
            }
            @Override public void close() { closes.incrementAndGet(); }
        };
    }

    @Test
    public void unreportedOversizeStopsAtLimitPlusOneAndDoesNotBlockNextFile() {
        ShareIntake value = intake();
        AtomicInteger count = new AtomicInteger(), closes = new AtomicInteger();
        value.receive(List.of(new ShareIntake.Source("image/png", null,
                () -> sized(ShareIntake.MAX_FILE_BYTES + 1024, count, closes)), source(new byte[] { 9 })), false);
        start(value);
        assertEquals(ShareIntake.MAX_FILE_BYTES + 1, count.get());
        assertEquals(1, closes.get());
        assertEquals("IMAGE_FILE_TOO_LARGE", value.view().items.get(0).errorCode);
        assertEquals("ready", value.view().items.get(1).state);
    }

    @Test
    public void aggregateLimitKeepsEarlierReadableImagesAndMetadataIsBounded() {
        ShareIntake value = intake();
        List<ShareIntake.Source> sources = new ArrayList<>();
        for (int i = 0; i < ShareIntake.MAX_ITEMS; i++) {
            int bytes = i < 2 ? ShareIntake.MAX_FILE_BYTES : 1;
            sources.add(new ShareIntake.Source("image/png", null,
                    () -> sized(bytes, new AtomicInteger(), new AtomicInteger())));
        }
        value.receive(sources, true);
        start(value);
        ShareIntake.View view = value.view();
        assertEquals(9, view.items.size());
        assertEquals(ShareIntake.MAX_FILE_BYTES, view.items.get(0).byteCount);
        assertEquals(ShareIntake.MAX_FILE_BYTES, view.items.get(1).byteCount);
        for (int i = 2; i < 8; i++) assertEquals("SHARE_TOTAL_TOO_LARGE", view.items.get(i).errorCode);
        assertEquals("ITEM_COUNT_LIMIT", view.items.get(8).errorCode);
        assertEquals("additional-shared-images", view.items.get(8).filename);
    }

    @Test
    public void tokensChunkBoundsAndAcknowledgementCannotReadAnotherBatch() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 2, 4, 6 })), false);
        value.foreground(owner, true);
        value.session(true);
        ShareIntake.View pending = value.view();
        assertThrows(IllegalArgumentException.class, () -> value.clear(pending.id, true));
        value.read(value.begin());
        ShareIntake.View view = value.view();
        String item = view.items.get(0).id;
        assertThrows(IllegalArgumentException.class, () -> value.chunk("wrong", item, 0, 3));
        assertThrows(IllegalArgumentException.class, () -> value.chunk(view.id, "wrong", 0, 3));
        assertThrows(IllegalArgumentException.class, () -> value.chunk(view.id, item, -1, 3));
        assertThrows(IllegalArgumentException.class, () -> value.chunk(view.id, item, 4, 3));
        assertThrows(IllegalArgumentException.class, () -> value.chunk(view.id, item, 0, ShareIntake.MAX_CHUNK_BYTES + 1));
        assertThrows(IllegalArgumentException.class, () -> value.clear("wrong", false));
        assertArrayEquals(new byte[] { 4, 6 }, value.chunk(view.id, item, 1, 2));
        assertArrayEquals(new byte[0], value.chunk(view.id, item, 3, 1));
        value.clear(view.id, true);
        assertTrue(value.view().handedOff);
        assertArrayEquals(new byte[] { 2, 4, 6 }, value.chunk(view.id, item, 0, 3));
        value.clear(view.id, false);
        assertNull(value.view());
        assertThrows(IllegalArgumentException.class, () -> value.chunk(view.id, item, 0, 3));
    }

    @Test
    public void cancellationClosesActiveStreamAndLateReadNeverPublishes() throws Exception {
        ShareIntake value = intake();
        CountDownLatch entered = new CountDownLatch(1), release = new CountDownLatch(1);
        AtomicInteger closed = new AtomicInteger();
        value.receive(List.of(new ShareIntake.Source("image/png", null, () -> new InputStream() {
            @Override public int read() throws IOException {
                entered.countDown();
                try { if (!release.await(5, TimeUnit.SECONDS)) throw new IOException("test_timeout"); }
                catch (InterruptedException exception) { throw new IOException("interrupted"); }
                return -1;
            }
            @Override public void close() { closed.incrementAndGet(); }
        })), false);
        value.foreground(owner, true);
        value.session(true);
        ShareIntake.Work work = value.begin();
        Thread reader = new Thread(() -> value.read(work));
        reader.start();
        assertTrue(entered.await(5, TimeUnit.SECONDS));
        value.session(false);
        assertTrue(closed.get() >= 1);
        release.countDown();
        reader.join(5000);
        assertFalse(reader.isAlive());
        value.session(true);
        assertNull(value.view());
        assertEquals("SIGN_IN_AND_RESHARE", value.notice());
    }

    @Test
    public void pausedLateReadIsDiscardedAndResumedItemStartsFromOriginalStream() throws Exception {
        ShareIntake value = intake();
        CountDownLatch entered = new CountDownLatch(1), release = new CountDownLatch(1);
        AtomicInteger opened = new AtomicInteger(), closed = new AtomicInteger();
        value.receive(List.of(new ShareIntake.Source("image/png", null, () -> {
            if (opened.incrementAndGet() > 1) return new ByteArrayInputStream(new byte[] { 5, 6 });
            return new InputStream() {
                @Override public int read() throws IOException {
                    entered.countDown();
                    try { if (!release.await(5, TimeUnit.SECONDS)) throw new IOException("test_timeout"); }
                    catch (InterruptedException exception) { throw new IOException("interrupted"); }
                    return -1;
                }
                @Override public void close() { closed.incrementAndGet(); }
            };
        })), false);
        value.foreground(owner, true);
        value.session(true);
        ShareIntake.View before = value.view();
        ShareIntake.Work work = value.begin();
        Thread reader = new Thread(() -> value.read(work));
        reader.start();
        assertTrue(entered.await(5, TimeUnit.SECONDS));
        value.foreground(owner, false);
        assertTrue(closed.get() >= 1);
        value.foreground(owner, true);
        assertNull(value.begin());
        release.countDown();
        reader.join(5000);
        assertFalse(reader.isAlive());
        value.session(true);
        assertEquals("pending", value.view().items.get(0).state);
        value.read(value.begin());
        assertEquals(before.id, value.view().id);
        assertEquals(before.items.get(0).id, value.view().items.get(0).id);
        assertArrayEquals(new byte[] { 5, 6 }, value.chunk(before.id, before.items.get(0).id, 0, 2));
        assertEquals(2, opened.get());
    }

    @Test
    public void inProcessRecreationKeepsSnapshotsButFreshInstanceHasNoDraft() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 99 })), false);
        start(value);
        ShareIntake.View before = value.view();
        Object replacement = new Object();
        value.attach(replacement, () -> {});
        value.foreground(owner, false); // The old activity cannot pause its replacement.
        value.detach(owner, true); // Nor can its late destruction discard the new owner.
        value.foreground(replacement, true);
        assertNull(value.view());
        value.session(true);
        assertEquals(before.id, value.view().id);
        assertArrayEquals(new byte[] { 99 }, value.chunk(before.id, before.items.get(0).id, 0, 1));
        assertNull(intake().view());
    }

    @Test
    public void secondShareCannotReplaceAnUnconsumedBatch() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 1 })), false);
        start(value);
        ShareIntake.View first = value.view();
        assertFalse(value.receive(List.of(source(new byte[] { 2 })), false));
        assertEquals("SHARE_BUSY", value.notice());
        assertEquals(first.id, value.view().id);
        assertArrayEquals(new byte[] { 1 }, value.chunk(first.id, first.items.get(0).id, 0, 1));
    }

    private ShareIntake.UploadContext context(ShareIntake.View view, int position) {
        return new ShareIntake.UploadContext("12345678-1234-1234-1234-123456789abc", List.of(
                new ShareIntake.ContextItem(view.items.get(0).id, "aaaaaaaa-1234-1234-1234-123456789abc", position)));
    }

    @Test
    public void acknowledgedBytesAndImmutableQueueIdentitySurviveWebViewRecreationUntilLogout() {
        ShareIntake value = intake();
        byte[] original = { 5, 4, 3, 2, 1 };
        value.receive(List.of(source(original)), false);
        start(value);
        ShareIntake.View before = value.view();
        ShareIntake.UploadContext context = context(before, 17);
        assertThrows(IllegalArgumentException.class, () -> value.saveContext(before.id, context));
        value.clear(before.id, true);
        value.saveContext(before.id, context);
        value.saveContext(before.id, context(before, 17)); // Exact context replay is harmless.
        assertThrows(IllegalArgumentException.class, () -> value.saveContext(before.id, context(before, 18)));
        Object replacement = new Object();
        value.detach(owner, false);
        value.attach(replacement, () -> {});
        value.foreground(replacement, true);
        assertNull(value.view());
        value.session(true);
        ShareIntake.View recovered = value.view();
        assertEquals(before.id, recovered.id);
        assertEquals(context, recovered.queueContext);
        assertEquals(17, recovered.queueContext.items.get(0).displayOrder);
        assertEquals("aaaaaaaa-1234-1234-1234-123456789abc", recovered.queueContext.items.get(0).clientUploadId);
        assertArrayEquals(original, value.chunk(before.id, before.items.get(0).id, 0, 5));
        assertFalse(value.receive(List.of(source(new byte[] { 8 })), false));
        value.session(false);
        value.session(true);
        assertNull(value.view());
        assertTrue(value.receive(List.of(source(new byte[] { 8 })), false));
    }

    @Test
    public void queueContextCannotBindUnknownFailedOrRepeatedItems() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 1 }), new ShareIntake.Source(null, "URI_UNREADABLE", null)), false);
        start(value);
        ShareIntake.View view = value.view();
        value.clear(view.id, true);
        ShareIntake.ContextItem valid = context(view, 2).items.get(0);
        assertThrows(IllegalArgumentException.class, () -> new ShareIntake.ContextItem("0-0-0-0-0", valid.clientUploadId, 2));
        assertThrows(IllegalArgumentException.class, () -> new ShareIntake.ContextItem(valid.itemId, valid.clientUploadId, -1));
        assertThrows(IllegalArgumentException.class, () -> new ShareIntake.ContextItem(valid.itemId, valid.clientUploadId, Integer.MAX_VALUE));
        assertThrows(IllegalArgumentException.class, () -> value.saveContext(view.id, new ShareIntake.UploadContext(
                "12345678-1234-1234-1234-123456789abc", List.of(valid, valid))));
        ShareIntake.ContextItem failed = new ShareIntake.ContextItem(view.items.get(1).id,
                "bbbbbbbb-1234-1234-1234-123456789abc", 3);
        assertThrows(IllegalArgumentException.class, () -> value.saveContext(view.id, new ShareIntake.UploadContext(
                "12345678-1234-1234-1234-123456789abc", List.of(failed))));
        ShareIntake.ContextItem unknown = new ShareIntake.ContextItem("cccccccc-1234-1234-1234-123456789abc",
                "bbbbbbbb-1234-1234-1234-123456789abc", 3);
        assertThrows(IllegalArgumentException.class, () -> value.saveContext(view.id, new ShareIntake.UploadContext(
                "12345678-1234-1234-1234-123456789abc", List.of(unknown))));
        assertNull(value.view().queueContext);
    }

    @Test
    public void streamCloseFailureDoesNotRetainFailedBytesOrBlockTheNextItem() {
        ShareIntake value = intake();
        value.receive(List.of(new ShareIntake.Source("image/png", null, () -> new ByteArrayInputStream(new byte[] { 7 }) {
            @Override public void close() throws IOException { throw new IOException("provider_close_failure"); }
        }), source(new byte[] { 8 })), false);
        start(value);
        assertEquals("URI_UNREADABLE", value.view().items.get(0).errorCode);
        assertEquals(0, value.view().items.get(0).byteCount);
        assertEquals("ready", value.view().items.get(1).state);
    }

    @Test
    public void selectedPhotosAndUncertainCreationSurviveRecreationWithoutIncludingDeselectedFiles() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 1 }), source(new byte[] { 2 })), false);
        start(value);
        ShareIntake.View before = value.view();
        value.clear(before.id, true);
        String selected = before.items.get(0).id;
        value.saveReview(before.id, new ShareIntake.ReviewContext(List.of(selected), false));
        value.saveReview(before.id, new ShareIntake.ReviewContext(List.of(selected), true));
        assertThrows(IllegalArgumentException.class, () -> value.saveReview(before.id,
                new ShareIntake.ReviewContext(List.of(selected, before.items.get(1).id), false)));
        Object replacement = new Object();
        value.detach(owner, false);
        value.attach(replacement, () -> {});
        value.foreground(replacement, true);
        value.session(true);
        assertTrue(value.view().reviewContext.creationUncertain);
        assertEquals(List.of(selected), value.view().reviewContext.selectedItemIds);
        value.saveContext(before.id, context(before, 15));
        assertFalse(value.view().reviewContext.creationUncertain);
        assertEquals(List.of(selected), value.view().reviewContext.selectedItemIds);
        value.saveReview(before.id, new ShareIntake.ReviewContext(List.of(), false));
        assertEquals("SHARE_REMOVED", value.view().items.get(0).errorCode);
        assertEquals(0, value.view().items.get(0).byteCount);
        assertThrows(IllegalArgumentException.class, () -> value.saveReview(before.id,
                new ShareIntake.ReviewContext(List.of(selected), false)));
    }

    @Test
    public void removingOneBoundFailureRetiresOnlyItsBytesAndCannotReviveAfterRecreation() {
        ShareIntake value = intake();
        value.receive(List.of(source(new byte[] { 3 }), source(new byte[] { 4 })), false);
        start(value);
        ShareIntake.View before = value.view();
        value.clear(before.id, true);
        ShareIntake.UploadContext context = new ShareIntake.UploadContext("12345678-1234-1234-1234-123456789abc", List.of(
                new ShareIntake.ContextItem(before.items.get(0).id, "aaaaaaaa-1234-1234-1234-123456789abc", 7),
                new ShareIntake.ContextItem(before.items.get(1).id, "bbbbbbbb-1234-1234-1234-123456789abc", 8)));
        value.saveContext(before.id, context);
        value.saveReview(before.id, new ShareIntake.ReviewContext(List.of(before.items.get(1).id), false));
        value.saveContext(before.id, context); // Idempotent replay does not restore removed files.
        Object replacement = new Object();
        value.detach(owner, false);
        value.attach(replacement, () -> {});
        value.foreground(replacement, true);
        value.session(true);
        assertEquals(context, value.view().queueContext);
        assertEquals(7, value.view().queueContext.items.get(0).displayOrder);
        assertEquals(8, value.view().queueContext.items.get(1).displayOrder);
        assertEquals(List.of(before.items.get(1).id), value.view().reviewContext.selectedItemIds);
        assertEquals("SHARE_REMOVED", value.view().items.get(0).errorCode);
        assertEquals(0, value.view().items.get(0).byteCount);
        assertThrows(IllegalArgumentException.class, () -> value.chunk(before.id, before.items.get(0).id, 0, 1));
        assertArrayEquals(new byte[] { 4 }, value.chunk(before.id, before.items.get(1).id, 0, 1));
        assertThrows(IllegalArgumentException.class, () -> value.saveReview(before.id,
                new ShareIntake.ReviewContext(List.of(before.items.get(0).id, before.items.get(1).id), false)));
    }
}
