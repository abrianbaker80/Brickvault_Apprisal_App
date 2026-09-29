# P12-04/P12-05 prerequisites carried forward

These remain open after P12-02 acceptance. None is a prerequisite to the
separately authorized P12-03 base-VM/Ubuntu slice, and none was satisfied by
this documentation closeout.

## P12-04 deployment

- Google Drive access, quota, dedicated unattended OAuth mechanism and the
  exact new folder `Brickvault_Apprisal_App_Backup`.
- Proxmox backup repository filesystem path, restricted account, quota,
  host free-space floor and deletion/retention isolation.
- Two independent encrypted repository keys with recovery custody outside
  the failed Proxmox host; encrypted logical database, role and configuration
  copies at both destinations. Proxmox is same-host supplemental recovery;
  Google Drive is required off-host recovery.
- Private DNS authority/control for `appraisal.abrianbaker.com`; approved
  reserved VM address and exact client/admin firewall ranges.
- Cloudflare/DNS-01 rights, trusted-certificate issuance and renewal strategy.
- Reviewed system Python 3.13 source, uv 0.12.10 production artifact/source,
  PostgreSQL 18 source/version and Caddy/DNS challenge tooling.
- Guarded production admin/migration/bootstrap command, production secret
  placement, and canonical provider-credential path with restrictive
  permissions before any provider use.
- Monitoring, backup-failure alert destination and real Caddy/TLS operation.

## P12-05 acceptance

- Independent restores from Proxmox and Google Drive; the Google-Drive-only
  recovery must work with the Proxmox copy unavailable.
- Private browser/PWA production acceptance and physical Android acceptance
  with an ordinary platform-trusted certificate.
- Off-host recovery, rollback and no-public-database acceptance evidence.

No backup repository, account, job, key, Drive folder, DNS record, certificate
or production service was created or tested in P12-02 or this closeout.
