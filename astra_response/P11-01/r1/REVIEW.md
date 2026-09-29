# P11-01 r1 — read-only home infrastructure discovery

**Verdict: READY FOR PHASE 11 CLOSEOUT REVIEW.** Phase 11 remains **IN
PROGRESS / DISCOVERY COMPLETE FOR REVIEW** until ChatGPT reviews the evidence.
Phase 12 is **NOT STARTED** and no deployment is authorized.

## What was observed

The configured, authenticated home target reached an existing Ubuntu 24.04 KVM
guest with a private `/24` network path. The guest has 64 assigned vCPUs,
125 GiB assigned RAM, 199 GB free on its root filesystem, and a separate
unmounted 200 GB virtual disk whose ownership is unknown. It already runs a
legacy BrickVault backend and loopback PostgreSQL 16. No reverse proxy was
active on that guest. Public DNS delegation is with Cloudflare.

The workstation's Proxmox alias has a placeholder hostname and the known
`proxmox` name did not resolve, so node identity/version, physical capacity,
VM inventory, bridge/VLAN, storage pools and backup jobs were not inspected.
No proxy or backup service elsewhere is ruled out. These are Phase 12
prerequisites, not inferred facts.

The checked-out API has only development/TEST database targets and loopback
Host/Origin policy. Android's special HTTPS destination is a TEST localhost
path. A private production hostname needs reviewed runtime and transport
implementation before any exposure.

## Recommended design for review

Use a dedicated Ubuntu VM on the existing Proxmox estate, conditional on
node and backup-pool confirmation: initial proposal 4 vCPU, 8 GiB RAM,
32 GiB OS plus 128 GiB database volume. Keep FastAPI, the React build and a
dedicated PostgreSQL cluster on that VM; bind API/database to loopback or
socket. A private DNS override points the approved subdomain to a Caddy HTTPS
entry point on the VM, with a DNS-01 certificate and no WAN forwarding.
Back up PostgreSQL and roles/configuration to a verified off-host target and
prove a restore before cutover. [Discovery](discovery.md) gives the evidence,
unknowns, change plan, approvals and rollback conditions.

## Review scope and artifacts

- [discovery.md](discovery.md): the full environment-specific ExecPlan.
- [commands.txt](commands.txt): sanitized read-only command/result record.
- [changes.patch](changes.patch): complete six-file documentation patch,
  including the new ExecPlan.
- [validation.txt](validation.txt): diff, link, privacy and preservation checks.

The documentation changes are uncommitted in the local implementation
checkout at `03ab154a7dbbf9b6aaee3c877c3a400732c6fd96`. Only this
report package is committed/pushed on `astra-response`. The three pre-existing
dirty protected files remain byte-for-byte and unstaged. No application code,
test, build, production database, Proxmox configuration, DNS, certificate,
service or network setting was changed.

## Requested review

Assess whether the bounded discovery and explicit unknowns are sufficient to
close Phase 11. Do not treat this package as Phase 12 approval. The Proxmox
node/backup facts, exact hostname/private DNS path, off-host backup target
and production runtime changes must be resolved before a deployment decision.
