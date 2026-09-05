# Security, Privacy, and Data Integrity

## Scope

This is a private single-user application, but it processes screen captures, external API credentials, seller-provided photos, and potentially seller-identifying information. Private does not mean careless.

## Secrets

- All provider credentials live on the server.
- Client builds receive only the BrickVault server URL and a replaceable client-auth mechanism.
- `.env` files are gitignored; `.env.example` contains placeholders only.
- Authorization headers and provider request bodies must not be logged wholesale.

## Server access

- Development may bind to localhost or a private LAN interface.
- Production remote access must use TLS and authentication, preferably through Brian's existing private-network/reverse-proxy strategy after an explicit deployment plan.
- Never expose the API publicly without authentication.

## Android capture

- The service must visibly indicate when capture capability is enabled.
- Capture happens only after Brian's explicit action.
- Restrict behavior to allowlisted target applications/package names where technically practical.
- Do not monitor keystrokes, messages, or unrelated apps.
- Do not implement automatic swipes/clicks as part of the initial system.
- Keep manual screenshot/share upload available.

## Image classes

1. **Raw screen capture:** may include Facebook UI and unrelated personal details. Most restricted.
2. **Listing-photo crop:** seller's LEGO photo without surrounding UI. Preferred long-term recognition asset.
3. **Object crop:** a LEGO object/minifigure region. Preferred training asset after confirmation.
4. **Training derivative:** normalized/sanitized copy tied to a versioned dataset.

## Redaction and retention

- Strip seller names, profile images, messages, notifications, exact addresses, and unrelated UI from training-ready exports.
- Preserve listing-photo and object crops needed for training.
- Make full-screen raw-capture retention configurable. A reasonable initial policy is to retain raw captures until extraction/cropping is verified, then allow deletion after a configurable period while keeping useful crops and metadata.
- Deletion must respect lineage and never silently remove the only training/source asset.

## Data integrity

- Original files are immutable.
- Hash every stored file.
- Validate MIME type and decode images server-side.
- Enforce upload-size and pixel-dimension limits.
- Use database transactions when linking stored blobs to records.
- Reconcile orphaned files through a maintenance command; do not delete automatically without a dry run.
- Backups must include both the database and blob storage at a consistent point.

## External AI providers

- Send only the image crops and context needed for the requested analysis.
- Record provider/model/version and cost metadata.
- Do not assume provider outputs are factual.
- Review current provider data-use and retention settings before production use.
