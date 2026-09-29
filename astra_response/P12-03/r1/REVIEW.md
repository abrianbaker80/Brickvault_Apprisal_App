# P12-03 r1 — prepared VM; manual Ubuntu installation required

## Verdict and requested review

**BLOCKED — installer/manual console required. MANUAL INSTALLER STEP REQUIRED.**
VM 115 and its fresh attachments are **PROVISIONED FOR REVIEW (partial)**.
Ubuntu is **NOT INSTALLED**, administrator SSH is **NOT ESTABLISHED**, and
P12-03 is **NOT CLOSED**. Review the gated creation, existing resource isolation,
untouched data disk, stopped handoff and manual installer instructions.

Brian authorized one dedicated VM/base OS slice on 2026-09-29. Main remains
`01db616d503b66c30b7fe95fc8e0259102ca2618`, with an empty index and the three
protected files byte-for-byte unchanged. P12-01/P12-02 remain CLOSED;
Phase 12 is IN PROGRESS; no P12-04 work occurred.

## Result

- Fresh checks passed: standalone pve, PVE 9.1.6/kernel 6.17.13-2-pve,
  approximately 148.6 GiB available RAM, healthy local-zfs with 380.4 GiB
  available, reviewed active untagged vmbr1, free VMID/nextid 115 and no name collision.
- Existing Ubuntu Server 24.04.2 ISO SHA-256 **MATCHED** the exact official
  Ubuntu archive filename. No replacement media was downloaded.
- Created exactly VM 115 brickvault-appraisal: q35/OVMF, one socket/four host
  vCPUs, fixed 8192 MiB, balloon 0, virtio-scsi-single, fresh EFI 1 MiB,
  OS 32 GiB and data 128 GiB on local-zfs, one untagged VirtIO NIC on vmbr1,
  verified ISO at ide2 and installation boot order ide2;scsi0.
- After each of seven mutations, read back qm config and compared existing
  guest inventory/configuration hashes. All 17 prior guests and prior local-zfs
  volumes remained unchanged. VM 107 stayed running; no guest was accessed.
- Read-only host probes show no data-disk partitions, filesystem/LVM signature
  or mount. Guest post-install checks remain NOT RUN; VM 115 never booted.
- Browser navigation failed with ERR_CERT_AUTHORITY_INVALID. No certificate
  exception, login, alternate installer framework or VM start occurred.
- Final state: **stopped**, **onboot=0**. No snapshot, backup or later software.

## Evidence and continuation

- [Final ExecPlan 093 and manual installer instructions](source/docs/plans/093-base-vm-provisioning.md)
- [Infrastructure before/after](infrastructure-before-after.md)
- [Authoritative ISO verification](iso-verification.md)
- [Sanitized executed commands](commands.txt)
- [Validation and preservation](validation.txt)
- [Complete five-document patch](changes.patch)
- [Workflow](source/CODEX_WORKFLOW.md), [roadmap](source/docs/ROADMAP.md),
  [Plan 091](source/docs/plans/091-production-runtime-and-deployment.md),
  [Plan 092](source/docs/plans/092-exact-infrastructure-pre-mutation-review.md)

Continue only the normal manual P12-03 installation on the 32-GiB OS disk,
using brickvault-admin and the approved laptop public key, then base-OS
validation and graceful shutdown of only 115. Leave the 128-GiB disk unused.
Destruction of any new VM/volume requires separate approval. No P12-04
approval is implied. This package is not complete P12-03 acceptance.

## Publication and redaction

Review-only package on astra-response, appending to
9497c5a6f5ac7a74396f32670d6eb5e7af5adf6c. Main is neither committed nor pushed.
The patch contains only task documentation, including new Plan 093.
Source snapshots keep repository-relative structure; their pre-existing
links to unrelated documents resolve in the main checkout. Those unrelated
documents are intentionally not duplicated into this minimal package.

No private addresses, MACs, keys, password hashes, device identifiers,
tokens, raw management configurations or unrelated guest details are published.
One historical private ZIP filename in source/CODEX_WORKFLOW.md is redacted,
outside the task patch. Other source snapshots match main byte-for-byte.
Raw evidence remains ignored locally. Automatic approval review rejected an
initial combined package-generation command as "blocked by policy", without
a specific reason; separate bounded file-writing/validation steps succeeded.
