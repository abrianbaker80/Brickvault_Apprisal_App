# P12-02 r2 — accepted infrastructure review closeout

**P12-02 is ACCEPTED / CLOSED. Phase 12 is IN PROGRESS. P12-03 is NEXT /
NOT STARTED.** ChatGPT accepted the published
[`r1` infrastructure review](https://github.com/abrianbaker80/Brickvault_Apprisal_App/blob/639b10dc483da27d85cd983b204d281e218b5b6c/astra_response/P12-02/r1/REVIEW.md)
and clarified that its unresolved deployment requirements do not prevent a
separately authorized base-VM slice. Acceptance and this closeout authorize no
infrastructure mutation.

The [final ExecPlan 092](ExecPlan-092.md) retains the accepted 2026-09-29
point-in-time Proxmox facts and the conditional `brickvault-appraisal` VM on
`pve`: VMID 115 only if still free, 4 host vCPU, fixed 8 GiB RAM, OVMF/q35,
fresh EFI/32-GiB OS/128-GiB data disks on `local-zfs`, and one untagged
VirtIO NIC on `vmbr1`. The legacy VM 107, its database/disks and the unowned
disk remain excluded.

P12-03, **if separately authorized**, now covers only creating that VM and
installing base Ubuntu. Before mutation it must recheck VMID, node capacity,
pool space and bridge state, then match the existing ISO's SHA-256 against an
authoritative Ubuntu checksum for the exact image. Temporary DHCP and key-only
administrator SSH are allowed; the new data disk stays unformatted and the VM
is left stopped for review. No BrickVault, PostgreSQL, Python 3.13, uv,
Caddy, restic/rclone, secrets, DNS, certificate, firewall/router rule or
backup job belongs to P12-03.

Brian's selected encrypted PostgreSQL recovery copies on existing Proxmox
(same-host supplemental) and Google Drive folder
`Brickvault_Apprisal_App_Backup` (required off-host) remain future work.
Private DNS, trusted certificates, package sources, guarded production
administration, live clients and independent restores also remain open.
See [carried-forward gates](carried-forward-gates.md) for the P12-04/P12-05
prerequisites.

The local documentation commit is
`01db616d503b66c30b7fe95fc8e0259102ca2618`; its exact six-file
inventory is in [local-commit.txt](local-commit.txt). Main was not pushed.
P12-02 closeout used no Proxmox connection, discovery rerun, tests, builds,
database, Android, provider, Google Drive or infrastructure mutation.

## Review contents

- [Cumulative six-document patch](changes.patch): baseline `c91f0bb2` to
  local closeout commit `01db616d`.
- [Final ExecPlan 092](ExecPlan-092.md): accepted facts, narrowed P12-03
  boundary, later gates and future mutation order.
- [Carried-forward gates](carried-forward-gates.md): P12-04/P12-05
  prerequisites that remain unresolved.
- [Validation](validation.txt): staged diff, links, protected hashes and
  publication checks.
- [Accepted r1 context](context/accepted-r1.md): the review authority and
  retained evidence.
- `source/`: final versions of the six local documentation files.

Public sanitization: one unchanged historical private local ZIP filename is
redacted in `source/CODEX_WORKFLOW.md`. The local committed workflow file and
`changes.patch` remain exact; no closeout line was changed in the review copy.
The package-local copy of ExecPlan 092 changes only its relative ExecPlan 091
link so it resolves here. The exact committed plan is in `source/`.

Preserve `r1`. P12-03 has not begun.
