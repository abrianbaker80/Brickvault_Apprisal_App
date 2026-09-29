# P12-04A server foundation

## VM and storage

VM 115 `brickvault-appraisal` began as the accepted, stopped Ubuntu 24.04.5 base VM. Its OS root remained `/dev/sda2` on the 32-GiB `scsi0`. Preflight identified the separate, blank 128-GiB `scsi1` by its stable guest attributes and exact 137,438,953,472-byte size. Only `scsi1` received a GPT table, one partition, and ext4. Its `/dev/sdb1` partition is mounted at `/var/lib/postgresql` by a private filesystem UUID in `/etc/fstab` with `defaults 0 2`; `nofail` is absent.

The requested example label `brickvault-pgdata` exceeded ext4's 16-byte label limit. Provisioning stopped after the partition/filesystem step, before mounting or changing fstab. The partition and ext4 signature were inspected, then the existing filesystem was relabeled `brickvault-db`. No second format or OS-disk mutation occurred. An unmount/remount from fstab and a controlled VM reboot both returned `/var/lib/postgresql` to `/dev/sdb1`.

## PostgreSQL and access

PGDG PostgreSQL 18.6 created its `18/main` cluster only after the data mount existed. Its data directory is `/var/lib/postgresql/18/main` on `/dev/sdb1`; the instance is enabled and active after reboot and has an explicit mount dependency. The only database TCP listener is `127.0.0.1:5432`. Local socket maintenance uses a narrow peer map for OS `root` and `postgres`; ordinary local users use peer authentication. IPv4 loopback requires SCRAM, and IPv6 loopback is rejected. Statement, error-statement, and parameter logging controls avoid routine credential disclosure. A workstation TCP attempt to the VM's private address on 5432 was refused or unreachable.

No BrickVault production database, owner/runtime role, migration, bootstrap principal, ownership marker, or database secret was created. No legacy VM 107 database was accessed.

## Release and inactive service

The future `brickvault` account is a locked system account with its own private group, `/usr/sbin/nologin`, and no sudo rights. `/opt/brickvault`, `/opt/brickvault/releases`, and `/etc/brickvault` are `root:brickvault` mode `0750`; `/var/lib/brickvault` is `brickvault:brickvault` mode `0700` and empty.

The verified artifact bundle `p12-04a-r1` lives under `/opt/brickvault/releases/p12-04a-r1`; `/opt/brickvault/current` points there. It contains the reviewed API wheel/sdist, locked requirements, regular web build files, manifest, and a Python 3.13 venv. The installed wheel imports from the venv as `brickvault`, and its `brickvault-production-admin` entry point is present. Source checkout files are not served. Source ID: `c65188e2f3bfeecc140175e52f5ecab9a64c850710513c7a2c5aaf3ce9c7bc4c`. Manifest SHA-256: `bfc6608efa56d1625f4493fe5e491b587ef95accacacf399fd44de38c6998ce9`.

`brickvault-api.service` is installed and passed `systemd-analyze verify`; it runs as `brickvault` from the release venv and is configured for `127.0.0.1:18080`. It is **disabled and inactive**. Its mandatory `/etc/brickvault/api.env` is absent, so production configuration and secrets have not been created. There is no API or Caddy listener. No Caddy, backup repository/job, DNS record, certificate, proxy secret, firewall/router change, or provider call occurred.

## Reboot and final state

One guest-only reboot changed VM 115's boot ID. The VM remains **RUNNING**, with `onboot=0` and `scsi0` boot order. After reboot, mount/data location, PostgreSQL readiness and listener, approved-key SSH and hardened settings, QEMU guest agent, synchronized time, release import, account permissions, empty config/state directories, and absence of new external listeners passed. Proxmox itself was not rebooted.
