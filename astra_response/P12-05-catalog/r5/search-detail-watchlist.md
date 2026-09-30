# Bounded installed-runtime application qualification

The real installed ProductService/PinnedCatalog/WatchlistService ran against the
production runtime role in repeatable-read, read-only transactions. All database
row counts and security stayed unchanged across qualification.

| Read | Actual result |
| --- | --- |
| Exact number 75331-1 | PASS; exactly one result: The Razor Crest |
| Actual name The Razor Crest | PASS; five results, includes exact set; repeated order/content deterministic |
| Appraisal/detail | PASS; correct canonical identity and accepted source/snapshot/provenance |
| Inventory | One version, native version 1, application-selected rather than provider-certified |
| Minifigures | Four direct lots: fig-010525, fig-013153, fig-013154, fig-013155; quantity one each; component inventories unavailable |
| Recorded rows | 802 part/color lots, 6,173 regular and 121 extra quantities; four minifigure lots/quantity four |
| Watchlist target resolver | PASS; exact set is valid, no catalog_unavailable; no owner session or Watchlist row created |
| Market | Zero observations; market_data_unavailable; all theoretical/liquid/fast-cash/dead-stock amounts null; zero-price substitution false; no provider dispatch |

Source metadata says structural valid and directly recorded figure membership
complete, while component/matching/partition/nested coverage remains unknown.
The official bulk source has no separate physical SourceContract. Whole-set
identity is COMPLETE_FOR_REPRESENTATION and admitted as one identified saleable
set. All three exploded strategies remain UNKNOWN/unadmitted. This is the accepted
representation contract and does not prove a seller's actual box is complete.
All four whole-set valuation views remain UNKNOWN with null amounts.

The accepted liquidity diagnostics include two unresolved_mapping references per
whole-set view. These are unavailable diagnostic references without a provider
identity/fetched time, not stored observations or priced evidence. Requiring zero
diagnostic references was an operational helper mistake, corrected to verify the
actual accepted projection without altering application source.

Appraisal is pinned to a snapshot ID, so its direct response has no captured
generation; the active database pointer independently proves generation 1. No
browser/PWA/Android acceptance or owner-login create/read/remove is claimed.
