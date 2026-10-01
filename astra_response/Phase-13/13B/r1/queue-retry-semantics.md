# Queue and recovery semantics

Selection assigns each File a fresh crypto UUID and consecutive positions from
max(server next_display_order, local next). The local counter increases before
dispatch, never decreases, and never reuses failed/removed positions. At most two
requests are active. States: queued, uploading, uploaded, duplicate, failed.
Progress is indeterminate while uploading, followed by the exact per-file result.

Success/duplicate triggers authoritative gallery refresh. Stale/aborted reads are
ignored. Gallery order comes from the server. Failed requests preserve their File,
UUID and position; only explicit retry resends that same item. Removing a failed
queue item is local-only; no saved image/receipt/blob is deleted. Successes stay
successful and are never resent due to another file failing.

Early API errors and network exceptions normalize using known identity/filename
into the generated UploadResult shape. DISPLAY_ORDER_CONFLICT explains refresh,
remove and reselection. UPLOAD_ID_CONFLICT explains new submission identity. These
conflicts do not offer an ordinary retry or silently move the attempt; explicit
reselection creates a new UUID and new high-water position. Network/unconfirmed
results offer same-attempt retry, including recovery of an already committed receipt.

Offline gating pauses queued dispatch. Unmount/logout abort outstanding requests
and disposes the queue. No unattended resume, persistent queue or batch restart.
