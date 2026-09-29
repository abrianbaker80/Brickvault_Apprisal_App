# P12-02 — exact infrastructure pre-mutation review

**Verdict: BLOCKED — dual-backup access/restore and private
DNS/certificate/access facts remain missing.** P12-02 is in review, not closed.
No P12-03/04/05 mutation is authorized or performed.

The main baseline is `c91f0bb2f76497dcf69a5f9887c885871871ddb9` on
`main`. The first noninteractive configured-key SSH check succeeded as root on
Proxmox node `pve`. Subsequent direct commands were read-only. The node has
72 logical CPUs, 188.8 GiB RAM and about 381 GiB available on `local-zfs`;
VMID 115 was free at the snapshot. `vmbr1` is the existing untagged private
bridge. Proxmox firewall is disabled and no backup job or PBS target was
configured. See [infrastructure facts](infrastructure-facts.md) for the bounded
observations and [commands](commands.txt) for sanitized command names.

The [full mutation plan](mutation-plan.md) selects one dedicated Ubuntu VM on
`pve`: proposed VMID 115, 4 vCPU, 8 GiB RAM, 32 GiB OS and 128 GiB data disks
on `local-zfs`, and untagged `vmbr1`. Brian approved
`appraisal.abrianbaker.com` for planning. Caddy would proxy `:443` to loopback
FastAPI `127.0.0.1:18080`, with PostgreSQL loopback-only on the new VM.
Production begins with a new empty database; the legacy database is untouched.
Brian selected encrypted PostgreSQL logical backup copies on both the existing
Proxmox server and a future Google Drive folder named
`Brickvault_Apprisal_App_Backup`. Google Drive is the off-host recovery copy;
Proxmox remains on the same physical host as the VM. The plan uses two
independently encrypted restic repositories and requires separate restores.

Before mutation authorization, verify both backup destinations' access,
encryption, host storage capacity and restore paths; identify the private DNS
manager and trusted-certificate DNS-01 rights; confirm the reserved VM address
and permitted client/admin
ranges; and select supportable Python 3.13, PostgreSQL 18 and certificate
tooling. The current repository has no production migration/bootstrap command;
that guarded tool is a later implementation gate. The runbook keeps the
accepted P12-03 base provisioning, P12-04 deployment and P12-05 acceptance
boundaries separate.

## Review contents

- [Infrastructure facts](infrastructure-facts.md): sanitized node findings.
- [Mutation plan](mutation-plan.md): topology, data policy, ordered future
  changes, verification and rollback. It is also the final
  [ExecPlan 092](source/docs/plans/092-exact-infrastructure-pre-mutation-review.md).
- [Commands](commands.txt): sanitized read-only discovery receipt.
- [Changes patch](changes.patch): exact six-document diff against main HEAD,
  generated through a separate temporary index.
- [Validation](validation.txt): documentation-only checks and protected hashes.
- [Accepted baseline](context/accepted-baseline.md): minimal P12-01 context.
- `source/`: all six final changed planning/status documents.

Public sanitization: one unchanged historical private local ZIP filename in
`source/CODEX_WORKFLOW.md` is redacted. The local workflow document and
`changes.patch` retain the exact task diff; no P12-02 changed line was altered
in the review copy.

The package publishes documentation only from an isolated review worktree.
Main was not staged, committed or pushed. No VM, disk, bridge, VLAN, firewall,
DNS, certificate, backup job, database, service, package or production secret
was created or modified. ChatGPT review is required before P12-02 can close.
