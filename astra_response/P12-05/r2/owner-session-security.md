# Owner session and security

Fresh unsynced Chrome profile created by Brian; extension connected and owner
password entered locally. Brian reported ready; no password was collected by the
agent. Production used normal trusted HTTPS at https://appraisal.abrianbaker.com.
The authenticated session survived full reload and returned HTTP 200/no-store.
Settings and selling-profile reads returned HTTP 200/no-store.

Both bva_session and bva_csrf were Secure, HttpOnly, SameSite=Strict, host-only,
Path=/. Only metadata was emitted. Credentials were held in private process
memory for explicitly authorized probes and cleared afterward; no credential
values appear in files, chat or this package.

| Live control | Result |
| --- | --- |
| Unauthenticated Settings read | 401/no-store |
| Missing CSRF on Settings PUT | 403/no-store |
| Wrong CSRF on Settings PUT | 403/no-store |
| Wrong Origin with valid session/CSRF | 403/no-store |
| Wrong Host with normal production TLS SNI | 421 |
| Forged proxy/forwarded headers plus wrong Origin | 403/no-store |
| Correct browser Origin/session/CSRF Settings save | 200/no-store |
| Windows direct API TCP port | Inaccessible; bounded timeout |

The positive control saved identical defaults; only the normal settings revision
advanced. A subsequent temporary MANUAL default and restoration used the UI.
Negative mutation requests were rejected before reaching the settings mutation.
These are bounded live boundary checks, not a new broad security qualification.
Logout and old-session rejection are recorded in [cleanup](cleanup-logout.md).
