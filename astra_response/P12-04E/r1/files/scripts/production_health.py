"""Credential-free application probes and protected operational health checks."""

import argparse
import hashlib
import json
import os
import shutil
import socket
import ssl
import subprocess
import sys
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import complete_run_retention as retention
import operational_alert as protected

HOST = "appraisal.abrianbaker.com"
CONFIG = Path("/etc/brickvault/operations/health.json")
STATE = Path("/var/lib/brickvault-operations")


def command(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, timeout=30, check=False)
    if result.returncode:
        raise ValueError("Health command failed.")
    return result.stdout.decode("utf-8").strip()


def listeners_valid(output: str) -> bool:
    found: dict[int, set[str]] = {}
    for line in output.splitlines():
        fields = line.split()
        if len(fields) < 4:
            return False
        endpoint = fields[3]
        address, port_text = endpoint.rsplit(":", 1)
        port = int(port_text)
        # ss can include an interface suffix even on IPv4 loopback DNS stubs.
        address = address.strip("[]").split("%", 1)[0]
        found.setdefault(port, set()).add(address)
        if port not in {22, 443} and (address, port) not in {
            ("127.0.0.1", 18080),
            ("127.0.0.1", 5432),
            ("127.0.0.53", 53),
            ("127.0.0.54", 53),
        }:
            return False
    return (
        found.get(18080) == {"127.0.0.1"}
        and found.get(5432) == {"127.0.0.1"}
        and 443 in found
        and 80 not in found
    )


def recent_backup(records: list[dict[str, Any]], now: datetime) -> bool:
    if not records:
        return False
    times = [retention.stamp(r["verified_at_utc"], now) for r in records]
    return (now - max(times)).total_seconds() < 36 * 3600


def disk_ok(total: int, free: int, minimum: int) -> bool:
    return total > 0 and free >= minimum and free / total >= 0.10


def certificate_ok(certificate: dict[str, Any], now: float) -> bool:
    return (
        certificate.get("subjectAltName") == (("DNS", HOST),)
        and ssl.cert_time_to_seconds(certificate["notAfter"]) - now > 21 * 86400
    )


def checks(deep: bool) -> dict[str, bool]:
    config = protected.protected_json(CONFIG)
    result: dict[str, bool] = {}

    def probe(name: str, operation: Any) -> None:
        try:
            result[name] = bool(operation())
        except Exception:  # noqa: BLE001 - do not log command output or private configuration.
            result[name] = False

    def services() -> bool:
        units = [
            "brickvault-api.service",
            "caddy.service",
            "postgresql@18-main.service",
            "brickvault-backup.timer",
            "certbot.timer",
            "qemu-guest-agent.service",
            "brickvault-health.timer",
            "brickvault-health-deep.timer",
            "brickvault-python-version.timer",
            "brickvault-retention.timer",
            "apt-daily.timer",
            "apt-daily-upgrade.timer",
        ]
        return all(
            command("/usr/bin/systemctl", "is-active", name) == "active"
            for name in units
        )

    def https() -> bool:
        with urllib.request.urlopen(
            f"https://{HOST}/api/health", timeout=15
        ) as response:
            if response.status != 200 or response.url != f"https://{HOST}/api/health":
                return False
            json.loads(response.read(65536))
        with (
            socket.create_connection((HOST, 443), timeout=15) as raw,
            ssl.create_default_context().wrap_socket(
                raw, server_hostname=HOST
            ) as connection,
        ):
            return certificate_ok(dict(connection.getpeercert() or {}), time.time())

    def mount() -> bool:
        rows = json.loads(
            command(
                "/usr/bin/findmnt",
                "--json",
                "--target",
                "/var/lib/postgresql",
                "--output",
                "TARGET,FSTYPE,UUID",
            )
        )["filesystems"]
        return (
            len(rows) == 1
            and rows[0]
            == {
                "target": "/var/lib/postgresql",
                "fstype": "ext4",
                "uuid": config["data_uuid"],
            }
            and command(
                "/usr/lib/postgresql/18/bin/psql",
                "-X",
                "-A",
                "-t",
                "--no-password",
                "-h",
                "/var/run/postgresql",
                "-U",
                "postgres",
                "-d",
                "postgres",
                "-c",
                "SHOW data_directory",
            )
            == "/var/lib/postgresql/18/main"
        )

    def backups() -> bool:
        # Only protected receipt metadata is read in the frequent path; no remote restic work.
        from brickvault_api import production_admin as admin
        from brickvault_api import production_backup as backup

        identities, _ = backup._validated_identity(
            admin._parse_json(
                admin._protected_file(backup.BACKUP_DIR / "repositories.json")
            )
        )
        repositories = {
            d.name: {"uri": d.repository, "id": identities[d.name]}
            for d in backup.DESTINATIONS
        }
        marker = admin._load_config(admin.CONFIG_PATH).marker
        records = []
        for path in backup.RECEIPT_DIR.iterdir():
            record = protected.protected_json(path)
            retention.validate_receipt(
                path.stem, record, repositories, marker, datetime.now(UTC)
            )
            records.append(record)
        return (
            recent_backup(records, datetime.now(UTC))
            and retention.read_state(retention.STATE / "ledger.json")["status"]
            == "READY"
        )

    def release() -> bool:
        current = Path("/opt/brickvault/current")
        directory = current.resolve(strict=True)
        if (
            directory.parent != Path("/opt/brickvault/releases")
            or directory.name != config["release_id"]
        ):
            return False
        raw = (directory / "manifest.json").read_bytes()
        if hashlib.sha256(raw).hexdigest() != config["manifest_sha256"]:
            return False
        manifest = json.loads(raw)
        for row in manifest["files"]:
            path = directory / row["path"]
            if (
                path.is_symlink()
                or not path.resolve().is_relative_to(directory)
                or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]
            ):
                return False
        hook = Path("/etc/letsencrypt/renewal-hooks/deploy/brickvault-certificate")
        if hook.is_symlink() or hook.stat().st_uid != 0 or hook.stat().st_mode & 0o022:
            return False
        if (
            hook.read_bytes()
            != (
                directory / "deploy/certbot/renewal-hooks/deploy/brickvault-certificate"
            ).read_bytes()
        ):
            return False
        return list(sys.version_info[:3]) == config["python_version"] and Path(
            sys.executable
        ).resolve().is_relative_to(Path("/opt/python"))

    def security_updates() -> bool:
        values = command("/usr/bin/apt-config", "dump")
        return (
            'APT::Periodic::Update-Package-Lists "1";' in values
            and 'APT::Periodic::Unattended-Upgrade "1";' in values
            and 'Unattended-Upgrade::Automatic-Reboot "true";' not in values
            and 'Unattended-Upgrade::Automatic-Reboot "1";' not in values
            and "${distro_id}:${distro_codename}-security" in values
        )

    probe("SERVICES", services)
    probe("HTTPS_CERTIFICATE", https)
    probe("LISTENERS", lambda: listeners_valid(command("/usr/bin/ss", "-H", "-lnt")))
    probe(
        "DATABASE_READY",
        lambda: (
            "accepting connections"
            in command(
                "/usr/lib/postgresql/18/bin/pg_isready", "-h", "127.0.0.1", "-p", "5432"
            )
        ),
    )
    probe("DATA_MOUNT", mount)
    probe("BACKUP_FRESH_RETENTION_READY", backups)
    probe("RELEASE_RUNTIME_HOOK", release)
    probe(
        "UFW", lambda: command("/usr/sbin/ufw", "status").startswith("Status: active")
    )
    probe(
        "CLOCK",
        lambda: (
            command("/usr/bin/timedatectl", "show", "-p", "NTPSynchronized", "--value")
            == "yes"
        ),
    )
    for name, path, minimum in [
        ("ROOT_SPACE", "/", 2 * 1024**3),
        ("DATA_SPACE", "/var/lib/postgresql", 5 * 1024**3),
    ]:
        usage = shutil.disk_usage(path)
        result[name] = disk_ok(usage.total, usage.free, minimum)
    reboot = Path("/var/run/reboot-required")
    probe(
        "REBOOT_PENDING",
        lambda: not reboot.exists() or time.time() - reboot.stat().st_mtime < 48 * 3600,
    )
    probe("SECURITY_UPDATES", security_updates)
    if deep:

        def repositories() -> bool:
            from brickvault_api import production_backup as backup

            backup._verify_destination_identity()
            return retention.run("plan", None).startswith("RETENTION_PLAN ")

        probe("REPOSITORY_IDENTITIES", repositories)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deep", action="store_true")
    args = parser.parse_args()
    try:
        if os.geteuid() != 0:
            raise ValueError("Root required.")
        protected.directory(STATE, create=True)
        result = checks(args.deep)
        protected.write_state(
            STATE / ("health-deep.json" if args.deep else "health.json"),
            {"checked_at": time.time(), "checks": result},
        )
        failed = [name for name, passed in result.items() if not passed]
        if failed:
            print("HEALTH_FAILED " + ",".join(failed), file=sys.stderr)
            return 1
        return 0
    except Exception:  # noqa: BLE001 - private configuration and command errors stay local.
        print("HEALTH_FAILED INTERNAL", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
