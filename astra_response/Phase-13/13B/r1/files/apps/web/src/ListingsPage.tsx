import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react';
import type { FormEvent, MouseEvent } from 'react';
import { useConnection } from './Connectivity';
import { createListing, imageContent, listingDetail, listingList } from './listings-api';
import type { Listing, ListingCreate, ListingDetail } from './listings-api';
import { UploadQueue } from './upload-queue';

export function openListings(event: MouseEvent<HTMLAnchorElement>, id?: string) {
  if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
    return;
  event.preventDefault();
  window.history.pushState({}, '', id ? `/listings/${encodeURIComponent(id)}` : '/listings');
  window.dispatchEvent(new PopStateEvent('popstate'));
}
const label = (listing: Listing) => listing.title || 'Untitled listing';
const price = (listing: Listing) =>
  listing.asking_price === null || listing.asking_price === undefined
    ? 'Asking price not entered'
    : `${listing.currency} ${listing.asking_price}`;
const message = (error: unknown) =>
  error instanceof Error ? error.message : 'Request could not be completed.';

function PrivateImage({
  id,
  alt,
  original = false,
}: {
  id: string;
  alt: string;
  original?: boolean;
}) {
  const [url, setUrl] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    let objectUrl: string | null = null;
    setUrl(null);
    setFailed(false);
    void imageContent(id, controller.signal)
      .then((blob) => {
        if (controller.signal.aborted) return;
        objectUrl = URL.createObjectURL(blob);
        setUrl(objectUrl);
      })
      .catch(() => {
        if (!controller.signal.aborted) setFailed(true);
      });
    return () => {
      controller.abort();
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [id]);
  return url ? (
    <img className={original ? 'listing-original' : 'listing-thumbnail'} src={url} alt={alt} />
  ) : (
    <span className="image-placeholder">{failed ? 'Image unavailable' : 'Loading image…'}</span>
  );
}

function ListingCard({ listing }: { listing: Listing }) {
  const [detail, setDetail] = useState<ListingDetail | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    void listingDetail(listing.id, controller.signal)
      .then(setDetail)
      .catch(() => {
        if (!controller.signal.aborted) setFailed(true);
      });
    return () => controller.abort();
  }, [listing.id]);
  return (
    <li className="listing-card">
      {detail?.images[0] && (
        <PrivateImage
          id={detail.images[0].thumbnail_asset_id}
          alt={`Preview of ${label(listing)}`}
        />
      )}
      <div>
        <p className="eyebrow">{listing.source_type || 'Unspecified source'}</p>
        <h2>
          <a href={`/listings/${listing.id}`} onClick={(e) => openListings(e, listing.id)}>
            {label(listing)}
          </a>
        </h2>
        <p>{price(listing)}</p>
        <p>
          {detail
            ? `${detail.images.length} images`
            : failed
              ? 'Image count unavailable'
              : 'Loading image count…'}
        </p>
      </div>
    </li>
  );
}

export function ListingsPage() {
  const [page, setPage] = useState<Awaited<ReturnType<typeof listingList>> | null>(null);
  const [offset, setOffset] = useState(0);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    document.title = 'Listings | BrickVault';
    const controller = new AbortController();
    setPage(null);
    setError('');
    void listingList(offset, controller.signal)
      .then(setPage)
      .catch((e: unknown) => {
        if (!controller.signal.aborted) setError(message(e));
      });
    return () => controller.abort();
  }, [offset]);
  return (
    <section className="listings-workspace" aria-labelledby="listings-title">
      <p className="eyebrow">Private workspace</p>
      <h1 id="listings-title" tabIndex={-1}>
        Listings
      </h1>
      <p>Keep marketplace details and photos in your private BrickVault workspace.</p>
      <button onClick={() => setCreating(!creating)}>
        {creating ? 'Cancel creation' : 'Create listing'}
      </button>
      {creating && <CreateListing />}
      {error && <p role="alert">{error}</p>}
      {!page && !error && <p role="status">Loading listings…</p>}
      {page && (
        <>
          <ul className="listing-cards">
            {page.items.map((v) => (
              <ListingCard key={v.id} listing={v} />
            ))}
          </ul>
          {!page.items.length && <p>No listings yet. Create one to add photos.</p>}
          <div className="listing-actions">
            {offset > 0 && (
              <button onClick={() => setOffset(Math.max(0, offset - 12))}>Previous listings</button>
            )}
            {page.next_offset !== null && (
              <button onClick={() => setOffset(page.next_offset!)}>Next listings</button>
            )}
          </div>
        </>
      )}
    </section>
  );
}

function CreateListing() {
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const controller = useRef<AbortController | null>(null);
  useEffect(() => () => controller.current?.abort(), []);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy) return;
    const values = new FormData(event.currentTarget);
    const text = (key: string) => {
      const value = values.get(key);
      return typeof value === 'string' ? value : '';
    };
    const optional = (key: string) => text(key).trim() || null;
    const body: ListingCreate = {
      title: optional('title'),
      description: optional('description'),
      source_url: optional('source_url'),
      source_type: text('source_type'),
      asking_price: optional('asking_price'),
      currency: text('currency').trim().toUpperCase(),
    };
    controller.current = new AbortController();
    const signal = controller.current.signal;
    setBusy(true);
    setError('');
    try {
      const listing = await createListing(body, signal);
      if (signal.aborted) return;
      window.history.pushState({}, '', `/listings/${listing.id}`);
      window.dispatchEvent(new PopStateEvent('popstate'));
    } catch (e: unknown) {
      if (!signal.aborted) setError(message(e));
    } finally {
      if (!signal.aborted) setBusy(false);
    }
  }
  return (
    <form className="listing-create" onSubmit={(e) => void submit(e)}>
      <h2>Create a private listing</h2>
      <fieldset disabled={busy}>
        <label>
          Source type
          <select name="source_type" defaultValue="manual">
            <option value="manual">Manual entry</option>
            <option value="marketplace">Marketplace listing</option>
            <option value="listing_photo">Listing photos</option>
            <option value="seller_photo">Seller photos</option>
          </select>
        </label>
        <label>
          Title (optional)
          <input name="title" maxLength={512} />
        </label>
        <label>
          Description (optional)
          <textarea name="description" maxLength={10000} rows={3} />
        </label>
        <label>
          Source URL (optional)
          <input name="source_url" type="url" maxLength={2048} />
        </label>
        <label>
          Asking price (optional)
          <input
            name="asking_price"
            inputMode="decimal"
            pattern="(0|[1-9][0-9]{0,15})(\.[0-9]{1,2})?"
          />
        </label>
        <label>
          Currency
          <input name="currency" defaultValue="USD" pattern="[A-Za-z]{3}" maxLength={3} required />
        </label>
        <button type="submit">{busy ? 'Creating…' : 'Save listing'}</button>
      </fieldset>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}

function QueueView({ queue }: { queue: UploadQueue }) {
  const items = useSyncExternalStore(queue.subscribe, queue.snapshot);
  return (
    <>
      <p>Next available upload position: {queue.nextPosition()}</p>
      <p>
        At most two images upload at once. Upload progress stays in this open listing; queued files
        are not retained after leaving or reloading.
      </p>
      <ul className="upload-queue" aria-label="Upload queue" aria-live="polite">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.file.name}</strong>
            <span>
              Position {item.order} · {item.state}
            </span>
            {item.state === 'uploading' && <progress aria-label={`Uploading ${item.file.name}`} />}
            {item.result?.error && (
              <p>
                {item.result.error.message} <small>({item.result.error.code})</small>
              </p>
            )}
            {item.state === 'failed' && (
              <div className="listing-actions">
                {!['DISPLAY_ORDER_CONFLICT', 'UPLOAD_ID_CONFLICT'].includes(
                  item.result?.error?.code ?? '',
                ) && <button onClick={() => queue.retry(item.id)}>Retry {item.file.name}</button>}
                <button onClick={() => queue.remove(item.id)}>
                  Remove failed {item.file.name}
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </>
  );
}

export function ListingDetailPage({ id }: { id: string }) {
  const [detail, setDetail] = useState<ListingDetail | null>(null);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<string | null>(null);
  const [queue, setQueue] = useState<UploadQueue | null>(null);
  const readController = useRef<AbortController | null>(null);
  const readVersion = useRef(0);
  const online = useConnection().state === 'ONLINE_VERIFIED';
  const load = useCallback(async () => {
    const version = ++readVersion.current;
    readController.current?.abort();
    const controller = new AbortController();
    readController.current = controller;
    try {
      const value = await listingDetail(id, controller.signal);
      if (controller.signal.aborted || version !== readVersion.current) return;
      setDetail(value);
      setError('');
    } catch (e: unknown) {
      if (!controller.signal.aborted) setError(message(e));
    }
  }, [id]);
  useEffect(() => {
    document.title = 'Private listing | BrickVault';
    const created = new UploadQueue(id, () => {
      void load();
    });
    setQueue(created);
    void load();
    return () => {
      created.dispose();
      readController.current?.abort();
      readVersion.current++;
    };
  }, [id, load]);
  useEffect(() => {
    queue?.setEnabled(online);
  }, [queue, online]);
  useEffect(() => {
    if (detail) queue?.refreshPositions(detail.next_display_order);
  }, [detail, queue]);
  return (
    <section className="listings-workspace" aria-labelledby="listing-title">
      <a href="/listings" onClick={(e) => openListings(e)}>
        All listings
      </a>
      <p className="eyebrow">Private listing</p>
      <h1 id="listing-title">{detail ? label(detail) : 'Listing'}</h1>
      {error && <p role="alert">{error}</p>}
      {!detail && !error && <p role="status">Loading listing…</p>}
      {detail && (
        <>
          <p>
            {detail.source_type || 'Unspecified source'} · {price(detail)}
          </p>
          {detail.description && <p className="listing-description">{detail.description}</p>}
          {detail.source_url && (
            <p>
              Source:{' '}
              <a href={detail.source_url} target="_blank" rel="noopener noreferrer">
                {detail.source_url}
              </a>
            </p>
          )}
          <h2>Photos · {detail.images.length}</h2>
          <p>These images stay private in BrickVault.</p>
          <ul className="listing-gallery">
            {detail.images.map((image, index) => (
              <li key={image.listing_image_id}>
                <button
                  aria-label={`View original image ${index + 1}`}
                  onClick={() => setSelected(image.original_asset_id)}
                >
                  <PrivateImage id={image.thumbnail_asset_id} alt={`Listing image ${index + 1}`} />
                </button>
                <span>
                  Image {index + 1} · Position {image.display_order}
                </span>
              </li>
            ))}
          </ul>
          {selected && (
            <section className="original-view" aria-label="Selected original image">
              <button onClick={() => setSelected(null)}>Close original</button>
              <PrivateImage id={selected} alt="Selected original image" original />
            </section>
          )}
          <h2>Add photos</h2>
          <label className="file-picker">
            Choose photos
            <input
              type="file"
              accept="image/jpeg,image/png,image/webp,.jpg,.jpeg,.png,.webp"
              multiple
              disabled={!queue || !online}
              onChange={(e) => {
                const files = Array.from(e.target.files ?? []);
                e.target.value = '';
                try {
                  queue?.select(files, detail.next_display_order);
                } catch (error: unknown) {
                  setError(message(error));
                }
              }}
            />
          </label>
          <p>Single-frame JPEG, PNG or WebP. Up to 25 MiB and 40 megapixels per image.</p>
          <button onClick={() => void load()}>Refresh gallery and positions</button>
          {queue && <QueueView queue={queue} />}
        </>
      )}
    </section>
  );
}
