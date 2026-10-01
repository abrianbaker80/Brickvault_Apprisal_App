import { OnlineOnly, PrivateView, useConnection } from './Connectivity';
import { useEffect, useRef, useState } from 'react';
import type { FormEvent, MouseEvent } from 'react';
import { ProductRequestError, searchSets } from './product-api';
import type { Search } from './product-api';
import { SetDetailPage } from './SetDetailPage';
import { DraftMemoryProvider, useDraftMemory, useLogout } from './Authentication';
import type { DraftMemory } from './Authentication';
import { AppShell } from './AppShell';
import { SetSearch, SearchResults } from './SetSearch';
import {
  navigateDealsIndex,
  navigateWatchlist,
  navigateSet,
  selectedDealsIndex,
  selectedSet,
  selectedForecast,
  selectedWatchlist,
  selectedHunt,
  selectedHuntRun,
  navigateHunt,
  watchNavigation,
} from './navigation';
import { HistoricalForecastPage } from './HistoricalForecastPage';
import { ForecastWorkspace } from './ForecastSave';
import { DealsPage } from './DealsPage';
import { SettingsPage } from './SettingsPage';
import { WatchlistPage } from './WatchlistPage';
import { HuntWorkspace } from './HuntWorkspace';
import { HuntPage } from './HuntPage';
import { ListingDetailPage, ListingsPage, openListings } from './ListingsPage';

export default function App() {
  const inherited = useDraftMemory();
  const local = useRef<DraftMemory>({
    value: null,
    forecastId: null,
    ownerId: null,
    huntAttempt: null,
    huntRecoveryReady: false,
  });
  return (
    <DraftMemoryProvider value={inherited ?? local.current}>
      <Workspace />
    </DraftMemoryProvider>
  );
}

function Workspace() {
  const connection = useConnection();
  const online = connection.state === 'ONLINE_VERIFIED';
  const logout = useLogout();
  const draftMemory = useDraftMemory();
  const [query, setQuery] = useState('');
  const [search, setSearch] = useState<Search | null>(null);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState('');
  const [submittedQuery, setSubmittedQuery] = useState('');
  const [searchOpen, setSearchOpen] = useState(false);
  const [selected, setSelected] = useState(selectedSet);
  const [forecast, setForecast] = useState(selectedForecast);
  const [deals, setDeals] = useState(selectedDealsIndex);
  const [settings, setSettings] = useState(() => window.location.pathname === '/settings');
  const [watchlist, setWatchlist] = useState(selectedWatchlist);
  const [hunt, setHunt] = useState(selectedHunt);
  const [huntRun, setHuntRun] = useState(selectedHuntRun);
  const [listings, setListings] = useState(() =>
    /^\/listings(?:\/|$)/.test(window.location.pathname),
  );
  const [listingId, setListingId] = useState(() => window.location.pathname.split('/')[2] ?? null);
  const searchController = useRef<AbortController | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    const unwatch = watchNavigation((number) => {
      searchController.current?.abort();
      searchController.current = null;
      setSearching(false);
      setSearchOpen(false);
      setSelected(number);
      setForecast(selectedForecast());
      setDeals(selectedDealsIndex());
      setWatchlist(selectedWatchlist());
      setHunt(selectedHunt());
      setHuntRun(selectedHuntRun());
      setSettings(window.location.pathname === '/settings');
      setListings(/^\/listings(?:\/|$)/.test(window.location.pathname));
      setListingId(window.location.pathname.split('/')[2] ?? null);
    });
    return () => {
      unwatch();
      searchController.current?.abort();
      searchController.current = null;
    };
  }, []);
  useEffect(() => {
    if (!selected && !forecast && !settings && draftMemory) {
      draftMemory.value = null;
      draftMemory.forecastId = null;
    }
    if (!selected && !forecast && !deals && !watchlist && !settings && !hunt && !listings) {
      document.title = 'Scout | BrickVault';
      heading.current?.focus();
    }
  }, [selected, forecast, deals, watchlist, settings, hunt, listings, draftMemory]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    searchController.current?.abort();
    const controller = new AbortController();
    searchController.current = controller;
    const timer = window.setTimeout(() => controller.abort(), 15_000);
    setSearching(true);
    setSearchError('');
    setSearch(null);
    setSubmittedQuery(query.trim());
    setSearchOpen(true);
    try {
      const value = await searchSets(query.trim(), controller.signal);
      if (searchController.current === controller) setSearch(value);
    } catch (error: unknown) {
      if (searchController.current === controller)
        setSearchError(
          error instanceof ProductRequestError
            ? error.message
            : 'Search could not be completed. Check local services and try again.',
        );
    } finally {
      window.clearTimeout(timer);
      if (searchController.current === controller) setSearching(false);
    }
  }
  function navigate(event: MouseEvent<HTMLAnchorElement>, number: string | null) {
    if (!navigateSet(event, number)) return;
    searchController.current?.abort();
    searchController.current = null;
    setSearching(false);
    setSearchOpen(false);
    setForecast(null);
    setDeals(false);
    setWatchlist(false);
    setSettings(false);
    setHunt(false);
    setHuntRun(null);
    setListings(false);
    if (number === selected && !forecast) {
      document.getElementById('set-title')?.focus();
      return;
    }
    setSelected(number);
  }
  function openDeals(event: MouseEvent<HTMLAnchorElement>) {
    if (!navigateDealsIndex(event)) return;
    searchController.current?.abort();
    searchController.current = null;
    setSearching(false);
    setSearchOpen(false);
    setSelected(null);
    setForecast(null);
    setDeals(true);
    setWatchlist(false);
    setSettings(false);
    setHunt(false);
    setHuntRun(null);
    setListings(false);
  }
  function openWatchlist(event: MouseEvent<HTMLAnchorElement>) {
    if (!navigateWatchlist(event)) return;
    searchController.current?.abort();
    searchController.current = null;
    setSearching(false);
    setSearchOpen(false);
    setSelected(null);
    setForecast(null);
    setDeals(false);
    setWatchlist(true);
    setSettings(false);
    setHunt(false);
    setHuntRun(null);
    setListings(false);
  }
  function openHunt(event: MouseEvent<HTMLAnchorElement>) {
    if (!navigateHunt(event)) return;
    searchController.current?.abort();
    searchController.current = null;
    setSearching(false);
    setSearchOpen(false);
    setSelected(null);
    setForecast(null);
    setDeals(false);
    setWatchlist(false);
    setSettings(false);
    setHunt(true);
    setHuntRun(null);
    setListings(false);
  }
  return (
    <AppShell
      listings={listings}
      navigateListings={(event) => openListings(event)}
      settings={settings}
      navigateSettings={(event) => {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
          return;
        event.preventDefault();
        window.history.pushState({}, '', '/settings');
        window.dispatchEvent(new PopStateEvent('popstate'));
      }}
      scout={!selected && !forecast && !deals && !watchlist && !settings && !hunt && !listings}
      deals={deals || forecast !== null}
      watchlist={watchlist}
      hunt={hunt}
      navigate={navigate}
      navigateDeals={openDeals}
      navigateWatchlist={openWatchlist}
      navigateHunt={openHunt}
      search={
        <fieldset className="connectivity-fields" disabled={!online}>
          <SetSearch query={query} change={setQuery} submit={(event) => void submit(event)} />
        </fieldset>
      }
      sessionAction={
        logout ? (
          <button className="session-signout" onClick={logout}>
            Sign out
          </button>
        ) : undefined
      }
    >
      <ForecastWorkspace>
        {listings && (
          <OnlineOnly>
            {listingId ? <ListingDetailPage key={listingId} id={listingId} /> : <ListingsPage />}
          </OnlineOnly>
        )}
        {!selected && !forecast && !deals && !watchlist && !settings && !hunt && !listings && (
          <section className="scout-heading" aria-labelledby="scout-title">
            <p className="eyebrow">Scout · Set lookup</p>
            <h1 id="scout-title" ref={heading} tabIndex={-1}>
              Start with the set.
            </h1>
            <p>Find a LEGO set. Understand the evidence behind its value.</p>
          </section>
        )}
        {((!selected && !forecast && !deals && !watchlist && !settings && !listings) ||
          searchOpen) &&
          online &&
          (searching || search || searchError) && (
            <SearchResults
              search={search}
              searching={searching}
              error={searchError}
              query={submittedQuery}
              selected={selected}
              navigate={navigate}
              close={
                selected || forecast
                  ? () => {
                      setSearchOpen(false);
                      document.getElementById('set-search')?.focus();
                    }
                  : undefined
              }
            />
          )}
        {selected && (
          <PrivateView path={`/api/sets/${encodeURIComponent(selected)}/appraisal`}>
            <SetDetailPage key={selected} number={selected} />
          </PrivateView>
        )}
        {forecast && (
          <PrivateView path={`/api/deal-forecasts/${forecast}`} historical>
            <HistoricalForecastPage key={forecast} id={forecast} />
          </PrivateView>
        )}
        {deals && (
          <OnlineOnly>
            <DealsPage />
          </OnlineOnly>
        )}
        {watchlist && (
          <PrivateView path="/api/watchlist">
            <WatchlistPage />
          </PrivateView>
        )}
        {hunt &&
          (huntRun ? (
            <PrivateView path={`/api/hunt/runs/${huntRun}`} historical>
              <HuntPage key={huntRun} id={huntRun} />
            </PrivateView>
          ) : (
            <OnlineOnly>
              <HuntWorkspace />
            </OnlineOnly>
          ))}
        {settings && (
          <OnlineOnly>
            <SettingsPage />
          </OnlineOnly>
        )}
        {!selected &&
          !forecast &&
          !deals &&
          !watchlist &&
          !settings &&
          !hunt &&
          !listings &&
          !search &&
          !searching &&
          !searchError && (
            <section className="welcome">
              <div className="welcome-intro">
                <h2>
                  A number finds the variant.
                  <br />A name opens the search.
                </h2>
                <p>
                  Use the search above to explore whole-set evidence and eligible contents
                  strategies.
                </p>
              </div>
              <dl className="lookup-guide">
                <div>
                  <dt>Whole-set market</dt>
                  <dd>New and used. Sold and stock. Four separate views.</dd>
                </div>
                <div>
                  <dt>Contents &amp; part-out</dt>
                  <dd>Quantity-aware appraisals where physical evidence supports them.</dd>
                </div>
                <div>
                  <dt>Evidence first</dt>
                  <dd>See what is supported, partial or still unknown.</dd>
                </div>
              </dl>
            </section>
          )}
      </ForecastWorkspace>
    </AppShell>
  );
}
