"""Root-only, category-limited Gmail alerts; credentials and server replies stay private."""

import argparse
import json
import os
import re
import smtplib
import ssl
import stat
import sys
import time
from email.message import EmailMessage
from pathlib import Path
from typing import Any

CONFIG = Path("/etc/brickvault/operations/gmail.json")
STATE = Path("/var/lib/brickvault-operations/alerts")
CATEGORIES = frozenset(
    {
        "TEST",
        "BACKUP",
        "RETENTION",
        "API",
        "CADDY",
        "CERTIFICATE",
        "HEALTH",
        "PYTHON",
        "REBOOT",
    }
)
UNITS = {
    "brickvault-backup.service": "BACKUP",
    "brickvault-retention.service": "RETENTION",
    "brickvault-api.service": "API",
    "caddy.service": "CADDY",
    "certbot.service": "CERTIFICATE",
    "brickvault-health.service": "HEALTH",
    "brickvault-health-deep.service": "HEALTH",
    "brickvault-python-version.service": "PYTHON",
}


class AlertError(RuntimeError):
    """Sanitized operational failure."""


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise AlertError("Ambiguous operations record.")
        value[key] = item
    return value


def directory(path: Path, *, create: bool = False) -> None:
    if create:
        path.mkdir(mode=0o700, parents=False, exist_ok=True)
    for item in (path, *path.parents):
        info = item.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise AlertError("Unsafe operations directory.")
    if stat.S_IMODE(path.stat().st_mode) != 0o700 or path.stat().st_gid != 0:
        raise AlertError("Unsafe operations directory permissions.")


def protected_json(path: Path, *, max_bytes: int = 65536) -> dict[str, Any]:
    directory(path.parent)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != 0
            or info.st_gid != 0
            or stat.S_IMODE(info.st_mode) != 0o600
            or info.st_nlink != 1
            or info.st_size > max_bytes
        ):
            raise AlertError("Unsafe operations file.")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            value = json.load(stream, object_pairs_hook=unique_object)
    finally:
        os.close(descriptor)
    if not isinstance(value, dict):
        raise AlertError("Invalid operations record.")
    return value


def write_state(path: Path, value: dict[str, Any]) -> None:
    directory(path.parent)
    temporary = path.with_suffix(".pending")
    descriptor = os.open(
        temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
    )
    with os.fdopen(descriptor, "w", encoding="ascii") as stream:
        json.dump(value, stream, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def validate_config(value: dict[str, Any]) -> None:
    if (
        set(value)
        != {
            "schema",
            "purpose",
            "transport",
            "host",
            "port",
            "username",
            "sender",
            "recipient",
            "password",
        }
        or type(value["schema"]) is not int
        or value["schema"] != 1
        or value["purpose"] != "brickvault-operational-alerts"
        or value["transport"] != "smtp-ssl"
        or value["host"] != "smtp.gmail.com"
        or type(value["port"]) is not int
        or value["port"] != 465
        or not isinstance(value["username"], str)
        or re.fullmatch(r"[a-z0-9][a-z0-9._+\-]{0,63}@gmail\.com", value["username"])
        is None
        or value["sender"] != value["username"]
        or value["recipient"] != value["username"]
        or not isinstance(value["password"], str)
        or re.fullmatch(r"[a-z]{16}", value["password"]) is None
    ):
        raise AlertError("Invalid Gmail alert configuration.")


def deliver(config: dict[str, Any], category: str) -> None:
    validate_config(config)
    if category not in CATEGORIES:
        raise AlertError("Unknown alert category.")
    message = EmailMessage()
    message["From"] = config["sender"]
    message["To"] = config["recipient"]
    message["Subject"] = f"BrickVault operations: {category}"
    message.set_content(
        "BrickVault operational notification.\n"
        + (
            "This is the authorized synthetic alert test.\n"
            if category == "TEST"
            else f"Attention is required for category {category}. Inspect the protected local operations status.\n"
        )
        + "No application records, account identifiers, infrastructure addresses or credentials are included.\n"
    )
    client = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        local_hostname="brickvault-operations",
        timeout=20,
        context=ssl.create_default_context(),
    )
    try:
        client.login(config["username"], config["password"])
        refused = client.send_message(message)
        if refused:
            raise AlertError("Alert recipient was refused.")
        # send_message returning without refusal proves the final SMTP DATA acceptance.
        # A failure during QUIT must not turn that accepted send into an automatic retry.
    finally:
        client.close()


def due(record: dict[str, Any], now: float) -> bool:
    if not record:
        return True
    if (
        set(record) != {"attempt", "status"}
        or type(record["attempt"]) not in (int, float)
        or record["status"] not in {"PENDING", "ACCEPTED", "FAILED"}
        or not 0 <= record["attempt"] <= now
    ):
        raise AlertError("Invalid alert state or clock rollback.")
    return now - float(record["attempt"]) >= (
        21600 if record["status"] == "ACCEPTED" else 600
    )


def send(category: str) -> str:
    import fcntl

    if os.geteuid() != 0 or category not in CATEGORIES:
        raise AlertError("Root and an approved category are required.")
    os.umask(0o077)
    directory(STATE.parent, create=True)
    directory(STATE, create=True)
    descriptor = os.open(STATE / "lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if (
            info.st_uid != 0
            or info.st_nlink != 1
            or stat.S_IMODE(info.st_mode) != 0o600
        ):
            raise AlertError("Unsafe alert lock.")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        path = STATE / f"{category}.json"
        record = protected_json(path) if path.exists() or path.is_symlink() else {}
        now = time.time()
        if category == "TEST" and record:
            raise AlertError("Test alert already attempted; operator review required.")
        if not due(record, now):
            return (
                "SUPPRESSED"
                if record["status"] == "ACCEPTED"
                else "FAILED_RATE_LIMITED"
            )
        config = protected_json(CONFIG)
        validate_config(config)
        write_state(path, {"attempt": now, "status": "PENDING"})
        try:
            deliver(config, category)
        except Exception:  # noqa: BLE001 - SMTP/configuration details must never escape.
            write_state(path, {"attempt": now, "status": "FAILED"})
            raise AlertError(
                "Alert delivery failed; private details withheld."
            ) from None
        write_state(path, {"attempt": now, "status": "ACCEPTED"})
        return "ACCEPTED"
    finally:
        os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", choices=sorted(CATEGORIES | UNITS.keys()))
    args = parser.parse_args()
    try:
        result = send(UNITS.get(args.category, args.category))
        print("ALERT_" + result)
        return 0 if result in {"ACCEPTED", "SUPPRESSED"} else 1
    except Exception:  # noqa: BLE001 - SMTP/configuration details must never escape.
        print("ALERT_FAILED: private details withheld", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
