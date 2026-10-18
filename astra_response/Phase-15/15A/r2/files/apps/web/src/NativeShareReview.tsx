import { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { useConnection } from './Connectivity';
import { CreateListing, QueueView, openListings } from './ListingsPage';
import { listingDetail, listingList } from './listings-api';
import type { Listing } from './listings-api';
import { UploadQueue } from './upload-queue';
import {
  cancelNativeShare,
  nativeShareSnapshot,
  subscribeNativeShare,
  saveNativeShareUploadContext,
  saveNativeShareReviewContext,
} from './native-share';
import type { SharedImage, NativeShareQueueContext } from './native-share';
import { connectionSnapshot, privateSessionValid, sessionManaged } from './private-views';

const notices: Record<string, string> = {
  SIGN_IN_AND_RESHARE:
    'Sign in, then share the images again. No images are retained through sign-in.',
  SHARE_BUSY: 'Finish or cancel the current Share review before sharing more images.',
  SHARE_INVALID: 'This Share could not be received. Share granted JPEG, PNG or WebP images again.',
  SHARE_RESTARTED: 'The app restarted. Check the saved listing, then share unsaved images again.',
  ITEM_COUNT_LIMIT:
    'Only the first eight shared entries can be received. Additional entries were refused.',
  SHARE_BACKGROUNDED: 'Return to BrickVault, verify the session, then share the images again.',
  SHARE_UNAVAILABLE:
    'Share intake is unavailable. Cancel and share again, or use manual photo upload.',
  SHARE_ACK_UNCONFIRMED:
    'Images reached this live review, but transfer cleanup was not confirmed. Clear this review when finished to release any remaining intake.',
};
const errors: Record<string, string> = {
  UNSUPPORTED_MIME: 'Unsupported image type. Use JPEG, PNG or WebP.',
  INVALID_CONTENT_URI: 'A temporary granted content URI is required.',
  URI_UNREADABLE: 'Image access was unavailable or revoked. Share this image again.',
  IMAGE_FILE_TOO_LARGE: 'This image exceeds 25 MiB.',
  SHARE_TOTAL_TOO_LARGE: 'This image exceeds the remaining 50 MiB Share limit.',
  ITEM_COUNT_LIMIT: 'Additional images exceed the eight-entry limit.',
  AMBIGUOUS_STREAMS: 'The Share contained conflicting image references. Share again.',
  SHARE_TRANSFER_FAILED: 'Image transfer could not be completed. Share this image again.',
  SHARE_REMOVED: 'This failed image was removed from the live queue.',
};
export function NativeShareNotice() {
  const state = useSyncExternalStore(subscribeNativeShare, nativeShareSnapshot);
  return state.notice ? (
    <p role="status">{notices[state.notice] ?? notices.SHARE_UNAVAILABLE}</p>
  ) : null;
}
function SharePreview({ item }: { item: SharedImage }) {
  const [url, setUrl] = useState<string | null>(null);
  useEffect(() => {
    if (!item.file) return;
    const created = URL.createObjectURL(item.file);
    setUrl(created);
    return () => {
      URL.revokeObjectURL(created);
    };
  }, [item.file]);
  return url ? (
    <img className="listing-thumbnail" src={url} alt={`Shared image ${item.index + 1}`} />
  ) : null;
}

/** Shared core review; native code has no listing model, credentials or upload client. */
export function NativeShareReview() {
  const state = useSyncExternalStore(subscribeNativeShare, nativeShareSnapshot);
  const online = useConnection().state === 'ONLINE_VERIFIED';
  const enabled = online && state.foreground && state.verified;
  const [chosen, setChosen] = useState<string[]>([]);
  const [mode, setMode] = useState<'existing' | 'new'>('existing');
  const [page, setPage] = useState<Awaited<ReturnType<typeof listingList>> | null>(null);
  const [offset, setOffset] = useState(0);
  const [refresh, setRefresh] = useState(0);
  const [listingId, setListingId] = useState('');
  const [destination, setDestination] = useState<Listing | null>(null);
  const [busy, setBusy] = useState(false);
  const [createBusy, setCreateBusy] = useState(false);
  const [uncertainCreate, setUncertainCreate] = useState(false);
  const [error, setError] = useState('');
  const [queue, setQueue] = useState<UploadQueue | null>(null);
  const [contextReady, setContextReady] = useState(false);
  const [recoveredCount, setRecoveredCount] = useState<number | null>(null);
  const request = useRef<AbortController | null>(null);
  const queueRef = useRef<UploadQueue | null>(null);
  const batch = useRef<string | null>(null);
  const initializedBatch = useRef<string | null>(null);
  const contextRef = useRef<NativeShareQueueContext | null>(null);
  const contextReadyRef = useRef(false);
  const uploading = useRef(false);
  const canDispatch = () => {
    const current = nativeShareSnapshot();
    return (
      current.batchId === state.batchId &&
      current.foreground &&
      current.verified &&
      connectionSnapshot().state === 'ONLINE_VERIFIED' &&
      (!sessionManaged() || privateSessionValid())
    );
  };
  useEffect(() => {
    if (batch.current === state.batchId) return;
    batch.current = state.batchId;
    queueRef.current?.dispose();
    queueRef.current = null;
    contextRef.current = null;
    contextReadyRef.current = false;
    initializedBatch.current = null;
    setContextReady(false);
    setRecoveredCount(null);
    setQueue(null);
    setChosen([]);
    setDestination(null);
    setListingId('');
    setMode('existing');
    setOffset(0);
    setPage(null);
    setError('');
    setUncertainCreate(false);
  }, [state.batchId]);
  useEffect(() => {
    if (state.state === 'ready' && initializedBatch.current !== state.batchId) {
      initializedBatch.current = state.batchId;
      setChosen(
        state.reviewContext?.selectedItemIds ??
          state.items.filter((item) => item.file).map((item) => item.id),
      );
      setUncertainCreate(state.reviewContext?.creationUncertain ?? false);
    }
  }, [state.state, state.items, state.batchId, state.reviewContext]);
  useEffect(() => {
    if (state.state !== 'ready' || !enabled || queue || state.queueContext) return;
    const controller = new AbortController();
    setPage(null);
    setListingId('');
    void listingList(offset, controller.signal)
      .then((value) => {
        if (!controller.signal.aborted) setPage(value);
      })
      .catch(() => {
        if (!controller.signal.aborted)
          setError('Listings could not be read. Check connectivity and refresh.');
      });
    return () => controller.abort();
  }, [state.state, enabled, queue, offset, refresh, state.queueContext]);
  useEffect(() => {
    const context = state.queueContext;
    if (state.state !== 'ready' || !context || !enabled || queueRef.current) return;
    const controller = new AbortController();
    setBusy(true);
    setError('');
    void listingDetail(context.listingId, controller.signal)
      .then((detail) => {
        if (controller.signal.aborted) return;
        const retained = new Set(
          state.reviewContext?.selectedItemIds ?? context.items.map((item) => item.itemId),
        );
        const files = context.items
          .filter((entry) => retained.has(entry.itemId))
          .map((entry) => {
            const item = state.items.find((candidate) => candidate.id === entry.itemId);
            if (!item?.file)
              throw new Error('The original bytes needed for queue recovery are unavailable.');
            return { id: entry.clientUploadId, order: entry.displayOrder, file: item.file };
          });
        const restored = new UploadQueue(
          context.listingId,
          () => {},
          undefined,
          () => {
            const current = nativeShareSnapshot();
            return (
              contextReadyRef.current &&
              current.batchId === state.batchId &&
              current.foreground &&
              current.verified &&
              connectionSnapshot().state === 'ONLINE_VERIFIED' &&
              (!sessionManaged() || privateSessionValid())
            );
          },
        );
        restored.setEnabled(false);
        restored.restore(
          files,
          Math.max(
            detail.next_display_order,
            ...context.items.map((item) => item.displayOrder + 1),
          ),
          'restricted',
        );
        contextRef.current = context;
        contextReadyRef.current = true;
        queueRef.current = restored;
        setContextReady(true);
        setQueue(restored);
        setDestination(detail);
        setRecoveredCount(detail.images.length);
      })
      .catch(() => {
        if (!controller.signal.aborted)
          setError(
            'The recovered queue requires an authenticated listing readback and all original bytes. Refresh the saved listing state before retrying.',
          );
      })
      .finally(() => {
        if (!controller.signal.aborted) setBusy(false);
      });
    return () => controller.abort();
  }, [
    state.state,
    state.queueContext,
    state.reviewContext,
    state.items,
    state.batchId,
    enabled,
    refresh,
  ]);
  useEffect(() => {
    queue?.setEnabled(enabled && contextReady);
  }, [queue, enabled, contextReady]);
  useEffect(
    () => () => {
      request.current?.abort();
      queueRef.current?.dispose();
    },
    [],
  );
  async function uploadTo(id: string) {
    if (!canDispatch() || uploading.current || queueRef.current) return;
    const selected = state.items.filter((item) => chosen.includes(item.id) && item.file);
    if (!selected.length) return;
    uploading.current = true;
    const controller = new AbortController();
    request.current = controller;
    setBusy(true);
    setError('');
    try {
      const detail = await listingDetail(id, controller.signal);
      if (controller.signal.aborted) return;
      if (!canDispatch()) {
        setDestination(detail);
        setListingId(detail.id);
        setMode('existing');
        setError(
          'Session verification is required before upload. Confirm this saved destination again when ready.',
        );
        return;
      }
      const created = new UploadQueue(
        detail.id,
        () => {},
        undefined,
        () => contextReadyRef.current && canDispatch(),
      );
      created.setEnabled(false);
      created.select(
        selected.map((item) => item.file!),
        detail.next_display_order,
        'restricted',
      );
      queueRef.current = created;
      setQueue(created);
      setDestination(detail);
      contextRef.current = {
        listingId: detail.id,
        items: created.snapshot().map((item, index) => ({
          itemId: selected[index]!.id,
          clientUploadId: item.id,
          displayOrder: item.order,
        })),
      };
      await confirmContext(created);
    } catch {
      if (!controller.signal.aborted)
        setError(
          queueRef.current
            ? 'The live queue context was not confirmed. No upload dispatch is allowed until its same identities are confirmed.'
            : 'The destination could not be verified. No image upload was started. Refresh listings and choose again.',
        );
    } finally {
      if (!controller.signal.aborted) setBusy(false);
      uploading.current = false;
    }
  }
  async function confirmContext(created = queueRef.current) {
    if (!created || !contextRef.current || !canDispatch()) return;
    setBusy(true);
    try {
      await saveNativeShareUploadContext(contextRef.current);
      if (queueRef.current !== created) return;
      contextReadyRef.current = true;
      setContextReady(true);
      setUncertainCreate(false);
      setError('');
      created.setEnabled(canDispatch());
    } catch {
      setError(
        'The live queue context was not confirmed. Confirm these same identities before uploading; do not allocate new ones.',
      );
    } finally {
      setBusy(false);
    }
  }
  async function changeSelection(ids: string[]) {
    if (!canDispatch() || busy || createBusy || queueRef.current) return;
    setBusy(true);
    try {
      await saveNativeShareReviewContext({
        selectedItemIds: ids,
        creationUncertain: uncertainCreate,
      });
      setChosen(ids);
      setError('');
    } catch {
      setError('Selection could not be saved in live memory. The previous selection is retained.');
    } finally {
      setBusy(false);
    }
  }
  async function retire(id: string) {
    const created = queueRef.current;
    const context = contextRef.current;
    const entry = context?.items.find((item) => item.clientUploadId === id);
    if (
      !created ||
      !context ||
      !entry ||
      !canDispatch() ||
      busy ||
      created.snapshot().find((item) => item.id === id)?.state !== 'failed'
    )
      return;
    const selected =
      nativeShareSnapshot().reviewContext?.selectedItemIds ??
      context.items.map((item) => item.itemId);
    setBusy(true);
    try {
      await saveNativeShareReviewContext({
        selectedItemIds: selected.filter((itemId) => itemId !== entry.itemId),
        creationUncertain: false,
      });
      if (queueRef.current === created) created.remove(id);
      setError('');
    } catch {
      setError(
        'Removal could not be confirmed. This failed item remains in the live queue with its original identity.',
      );
    } finally {
      setBusy(false);
    }
  }
  async function beforeCreate() {
    if (!canDispatch() || !chosen.length) throw new Error('Verify the session before saving.');
    await saveNativeShareReviewContext({ selectedItemIds: chosen, creationUncertain: true });
    if (!canDispatch()) throw new Error('Session verification is required before saving.');
  }
  async function clearKnownCreationFailure() {
    try {
      await saveNativeShareReviewContext({ selectedItemIds: chosen, creationUncertain: false });
    } catch {
      setUncertainCreate(true);
      setMode('existing');
    }
  }
  function discard() {
    request.current?.abort();
    queueRef.current?.dispose();
    queueRef.current = null;
    contextReadyRef.current = false;
    contextRef.current = null;
    setQueue(null);
    void cancelNativeShare();
  }
  if (!state.batchId) return <NativeShareNotice />;
  return (
    <section
      className="listings-workspace native-share-review"
      aria-labelledby="share-review-title"
    >
      <h2 id="share-review-title">Review shared images</h2>
      <NativeShareNotice />
      <p>
        Source identity is unknown. Shared images are stored as restricted and are never submitted
        to recognition or training.
      </p>
      <p>
        Check for names, faces, messages, locations and notifications. Cancel and share a safer
        image if needed. Saved originals remain immutable under the existing retention policy.
      </p>
      {state.state === 'reading' && <p role="status">Receiving images in this open app…</p>}
      {!enabled && (
        <p role="status">
          Intake and new uploads are paused until the app is visible and the session is verified.
        </p>
      )}
      {state.state === 'ready' && (
        <>
          {!queue && (
            <ul className="upload-queue" aria-label="Shared image review">
              {state.items.map((item) => (
                <li key={item.id}>
                  <SharePreview item={item} />
                  {item.file ? (
                    <label>
                      <input
                        type="checkbox"
                        disabled={
                          !enabled || busy || createBusy || uncertainCreate || !!state.queueContext
                        }
                        checked={chosen.includes(item.id)}
                        onChange={(event) =>
                          void changeSelection(
                            event.target.checked
                              ? [...chosen, item.id]
                              : chosen.filter((id) => id !== item.id),
                          )
                        }
                      />{' '}
                      Include image {item.index + 1}
                    </label>
                  ) : (
                    <strong>Image {item.index + 1} unavailable</strong>
                  )}
                  {item.errorCode && (
                    <p>{errors[item.errorCode] ?? errors.SHARE_TRANSFER_FAILED}</p>
                  )}
                </li>
              ))}
            </ul>
          )}
          {!queue && state.queueContext && (
            <>
              <p role="status">
                Recovering the live Share queue. Prior upload results remain uncertain until
                explicit retry; no upload starts during recovery.
              </p>
              <button disabled={!enabled || busy} onClick={() => setRefresh((value) => value + 1)}>
                Refresh saved listing state
              </button>
            </>
          )}
          {!queue && !state.queueContext && (
            <fieldset
              disabled={!enabled || busy || createBusy || !chosen.length}
              className="listing-create"
            >
              <legend>Choose where to save the reviewed images</legend>
              <label>
                Destination
                <select
                  aria-label="Share destination"
                  value={mode}
                  onChange={(event) => setMode(event.target.value as 'existing' | 'new')}
                >
                  <option value="existing">Existing Marketplace Listing</option>
                  {!uncertainCreate && (
                    <option value="new">Create a new Marketplace Listing</option>
                  )}
                </select>
              </label>
              {uncertainCreate && (
                <p role="alert">
                  Listing creation was not confirmed. Refresh the saved listings and resolve the
                  destination before uploading. Creation will not be retried automatically.
                </p>
              )}
              {mode === 'existing' ? (
                <>
                  <label>
                    Saved listing
                    <select
                      aria-label="Saved listing for shared images"
                      value={listingId}
                      onChange={(event) => {
                        setListingId(event.target.value);
                        setDestination(null);
                      }}
                    >
                      <option value="">Choose a listing</option>
                      {destination && !page?.items.some((item) => item.id === destination.id) && (
                        <option value={destination.id}>
                          {destination.title || 'Untitled listing'}
                        </option>
                      )}
                      {page?.items.map((listing) => (
                        <option key={listing.id} value={listing.id}>
                          {listing.title || 'Untitled listing'} · {listing.currency}{' '}
                          {listing.asking_price ?? 'price unknown'}
                        </option>
                      ))}
                    </select>
                  </label>
                  {offset > 0 && (
                    <button onClick={() => setOffset(Math.max(0, offset - 12))}>
                      Previous saved listings
                    </button>
                  )}
                  {page?.next_offset != null && (
                    <button onClick={() => setOffset(page.next_offset!)}>
                      Next saved listings
                    </button>
                  )}
                  <button onClick={() => setRefresh((value) => value + 1)}>
                    Refresh saved listings
                  </button>
                  <button disabled={!listingId || busy} onClick={() => void uploadTo(listingId)}>
                    Upload reviewed images to selected listing
                  </button>
                </>
              ) : (
                <CreateListing
                  submitLabel="Save new listing and upload reviewed images"
                  beforeCreate={beforeCreate}
                  onKnownFailure={clearKnownCreationFailure}
                  onBusyChange={setCreateBusy}
                  onUncertain={() => {
                    setUncertainCreate(true);
                    setMode('existing');
                    setRefresh((value) => value + 1);
                  }}
                  onCreated={(listing) => {
                    setDestination(listing);
                    setListingId(listing.id);
                    setMode('existing');
                    void uploadTo(listing.id);
                  }}
                />
              )}
            </fieldset>
          )}
          {queue && (
            <>
              <h3>Uploads to {destination?.title || 'Untitled listing'}</h3>
              {recoveredCount !== null && (
                <p role="status">
                  Recovered this live process queue after checking the saved gallery (
                  {recoveredCount} images). Every prior upload result is uncertain. Retry each
                  needed item explicitly to recover its same receipt.
                </p>
              )}
              {!contextReady && (
                <button disabled={!enabled || busy} onClick={() => void confirmContext()}>
                  Confirm this live queue before uploading
                </button>
              )}
              <QueueView
                queue={queue}
                enabled={enabled && contextReady && !busy && !createBusy}
                recoverable
                onRemove={(id) => void retire(id)}
              />
              <p>
                Already dispatched requests may have saved images even if interrupted. Open the
                saved listing to check the gallery; retry only an uncertain item with this same
                queue identity.
              </p>
              {destination && (
                <a
                  href={`/listings/${destination.id}`}
                  onClick={(event) => openListings(event, destination.id)}
                >
                  Open saved listing
                </a>
              )}
            </>
          )}
        </>
      )}
      {error && <p role="alert">{error}</p>}
      <button onClick={discard}>
        {queue ? 'Clear this live Share queue' : 'Cancel Share review'}
      </button>
    </section>
  );
}
