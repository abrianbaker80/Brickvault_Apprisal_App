# Accepted private HTTPS state

These results reuse accepted r1 evidence; they are not new live observations.
Production hostname: https://appraisal.abrianbaker.com.

One stable Kea reservation and one private Unbound host override serve VM 115.
No public application A/AAAA, WAN forwarding, static-address workaround, new NIC,
VLAN or bridge. Exact private IP/MAC and all secret values are omitted.

Caddy 2.11.4 came from its official signed repository. Certbot 2.9.0 with the
Cloudflare plugin 2.0.0 issued the normally trusted exact-SAN Let's Encrypt
certificate via DNS-01 only. No HTTP-01, private CA or Android TEST CA. Challenge
TXT cleanup passed. The zone-scoped credential is protected locally. Renewal dry
run, deploy hook and Caddy reload passed; certbot.timer was enabled/active.
The ACME account has no contact email: an operational note, not a P12-04D defect.

Immutable release: `p12-04d-r1`.
Source ID: `b704133a4754365ac96cb282902bcd14aa9a6a75bd572cb0df38816b968ce6bc`.
Manifest SHA-256: `25cbb51ec895640f2ed27ab36afac8ebcd11590aa52f96015b15e460502b6f36`.
API wheel SHA-256: `02dc2675632ffc72ffd11a797aab11b52fee5820b5966bc582864baf9ce8fc97`.
These installed identities are preserved; closeout does not rebuild or redeploy.

API was enabled/active at 127.0.0.1:18080; PostgreSQL at 127.0.0.1:5432.
Caddy was enabled/active on TCP 443 only, with a protected Unix admin socket,
no TCP 80/admin listener and no UDP 443. Exact HTTPS host proxies only to loopback;
X-BrickVault-Proxy is overwritten from the protected secret; client Forwarded,
X-Forwarded-* and X-Real-IP are removed. No client forwarding header is authoritative.

UFW was enabled, deny incoming/allow outgoing: TCP 22 only from the approved
private admin subnet and 443 only from the approved private client subnet.
No inbound allowance for 80, 18080 or 5432. Fresh SSH after enablement passed.

Windows normal DNS/platform trust, app shell, health, unauthenticated private-route
refusal, unknown API JSON/no-store, wrong Host rejection, direct-IP TLS refusal,
missing/wrong Origin refusal and forged/duplicate proxy replacement passed.
Android production Origin https://android.appraisal.abrianbaker.com had exact
credentialed CORS, no wildcard and rejection of the old TEST origin. This is
transport smoke only, not physical Android acceptance. No owner login/session
or new Set-Cookie evidence exists; cookie issuance remains P12-05.

API, Caddy, brickvault-backup.timer and certbot.timer were enabled/active.
VM onboot=0 is unchanged. The unrelated legacy backup identity is separate from
BrickVault Appraisal recovery authority, unchanged and not a deployment blocker.

[Accepted r1 review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/REVIEW.md), [network](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/network-dns.md), [TLS](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/certificate-tls.md), [application](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/application-activation.md), [firewall](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/firewall.md), [validation](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/aff388fd89fd935c5d9ab61f7a3cf4490196b58f/astra_response/P12-04D/r1/validation.txt).
