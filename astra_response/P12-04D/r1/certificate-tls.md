# Certificate and renewal

Stock Caddy 2.11.4 came from the official signed Caddy Cloudsmith stable repository.
Signing-key fingerprint: 65760C51EDEA2017CEA2CA15155B6D79CA56EA34.
Certbot 2.9.0-1, python3-certbot-dns-cloudflare 2.0.0-1 and python3-cloudflare
2.11.1-1ubuntu1 came from signed Ubuntu noble repositories; package audit passed.
Services were masked before installation to prevent the default port-80 startup.

Brian entered the Cloudflare token directly over a hidden local SSH TTY prompt.
Requested scope: Zone / DNS / Edit for only abrianbaker.com. No Global API Key or
additional Zone Read permission was requested. Root-only credential file mode
0600 and parent mode 0700 passed, as did functional DNS-01. Account-wide policy
was not enumerated. No token appears in this package or command arguments.

Let's Encrypt YE2 issued an ECDSA certificate with exactly one SAN:
appraisal.abrianbaker.com. Validity: 2026-09-30 02:45:59 UTC through
2026-12-29 02:45:58 UTC. Leaf DER SHA-256:
33e8fc2d09ee705d536c739aeebe439ebf24eb5ef33d78fc2710c533ecc50fb7.
Chain verification, exact SAN, key pairing, validity, Windows platform trust,
VM normal trust and served-leaf equality passed. No inbound HTTP or custom CA.
ACME registration has no contact email; external alerting remains deferred.

The guarded deploy hook accepts only this lineage, checks the normal trusted
chain/SAN/key/validity, writes a protected immutable certificate generation, and
atomically switches its current pointer. Certificate/key files are root:caddy
0640, directory root:caddy 0750 under /etc/caddy/brickvault-tls. It validates as
the caddy user and reloads the active service. Failure restores the prior disk
pointer; previous generations are retained. Focused tests cover these failure paths.

The existing /etc/brickvault parent remains restricted to root:brickvault; placing
Caddy's files beneath /etc/caddy avoids widening its access.

Certbot renew --dry-run --run-deploy-hooks passed. The hook used the active
production certificate and successfully reloaded Caddy. Both authoritative DNS
servers confirmed challenge TXT cleanup. certbot.timer is enabled/active, with
recorded next trigger 2026-09-30 15:42:51 UTC. Production renewal remains DNS-01.

Sources: [Caddy installation](https://caddyserver.com/docs/install),
[Cloudflare plugin](https://certbot-dns-cloudflare.readthedocs.io/en/stable/).
