import type { MouseEvent, ReactNode } from 'react';

export function AppShell({
  scout,
  listings = false,
  navigateListings,
  deals = false,
  watchlist = false,
  hunt = false,
  settings = false,
  navigateSettings,
  navigate,
  navigateDeals,
  navigateWatchlist,
  navigateHunt,
  search,
  sessionAction,
  children,
}: {
  scout: boolean;
  listings?: boolean;
  navigateListings?: (event: MouseEvent<HTMLAnchorElement>) => void;
  deals?: boolean;
  watchlist?: boolean;
  hunt?: boolean;
  settings?: boolean;
  navigateSettings?: (event: MouseEvent<HTMLAnchorElement>) => void;
  navigate: (event: MouseEvent<HTMLAnchorElement>, number: string | null) => void;
  navigateDeals?: (event: MouseEvent<HTMLAnchorElement>) => void;
  navigateWatchlist?: (event: MouseEvent<HTMLAnchorElement>) => void;
  navigateHunt?: (event: MouseEvent<HTMLAnchorElement>) => void;
  search: ReactNode;
  sessionAction?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="masthead">
        <div className="shell-header-inner">
          <a className="wordmark" href="/" onClick={(event) => navigate(event, null)}>
            BrickVault<span>APPRAISAL</span>
          </a>
          <nav aria-label="Primary navigation" className="primary-nav">
            <a
              href="/"
              aria-current={scout ? 'page' : undefined}
              onClick={(e) => navigate(e, null)}
            >
              Scout
            </a>
            {navigateDeals && (
              <a href="/deals" aria-current={deals ? 'page' : undefined} onClick={navigateDeals}>
                Deals
              </a>
            )}
            {navigateWatchlist && (
              <a
                href="/watchlist"
                aria-current={watchlist ? 'page' : undefined}
                onClick={navigateWatchlist}
              >
                Watchlist
              </a>
            )}
            {navigateHunt && (
              <a href="/hunt" aria-current={hunt ? 'page' : undefined} onClick={navigateHunt}>
                Hunt
              </a>
            )}
            {navigateListings && (
              <a
                href="/listings"
                aria-current={listings ? 'page' : undefined}
                onClick={navigateListings}
              >
                Marketplace Listings
              </a>
            )}
            {navigateSettings && (
              <a
                href="/settings"
                aria-current={settings ? 'page' : undefined}
                onClick={navigateSettings}
              >
                Settings
              </a>
            )}
          </nav>
          {search}
          <span className="environment">{sessionAction ?? 'Private workspace'}</span>
        </div>
      </header>
      <main id="main" className="shell-main" tabIndex={-1}>
        {children}
      </main>
      <footer className="shell-footer">
        <span>BrickVault Appraisal App</span>
        <span>Cached evidence. Transparent assumptions.</span>
      </footer>
    </div>
  );
}
