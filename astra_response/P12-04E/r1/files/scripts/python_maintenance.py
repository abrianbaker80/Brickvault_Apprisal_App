"""Detect official 3.13 patch releases; never download or install an interpreter."""

import gzip
import io
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import operational_alert as protected

SOURCE = "https://www.python.org/downloads/source/"
STATE = Path("/var/lib/brickvault-operations/python-version.json")
MAX_RESPONSE = 2 * 1024 * 1024


class ReleaseLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.patches: set[int] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href") or ""
        match = re.fullmatch(r"/downloads/release/python-313([0-9]+)/", href)
        if match:
            self.patches.add(int(match[1]))


def latest_from_html(html: str) -> tuple[int, int, int]:
    parser = ReleaseLinks()
    parser.feed(html)
    if "Stable Releases" not in html or not parser.patches:
        raise ValueError("Official source release index is unrecognized.")
    return 3, 13, max(parser.patches)


def lookup() -> tuple[int, int, int]:
    request = urllib.request.Request(
        SOURCE,
        headers={
            "User-Agent": "BrickVault-operations-version-check/1",
            "Accept-Encoding": "gzip, identity",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        location = urlparse(response.url)
        if location.scheme != "https" or location.hostname != "www.python.org":
            raise ValueError("Official source redirect refused.")
        raw = response.read(MAX_RESPONSE + 1)
        encoding = response.headers.get("Content-Encoding", "identity").lower().strip()
    if len(raw) > MAX_RESPONSE:
        raise ValueError("Official source response too large.")
    if encoding == "gzip":
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as compressed:
            raw = compressed.read(MAX_RESPONSE + 1)
    elif encoding != "identity":
        raise ValueError("Official source response encoding is unsupported.")
    if len(raw) > MAX_RESPONSE:
        raise ValueError("Official source expanded response too large.")
    return latest_from_html(raw.decode("utf-8"))


def main() -> int:
    installed = tuple(sys.version_info[:3])
    try:
        protected.directory(STATE.parent, create=True)
        if installed[:2] != (3, 13):
            raise ValueError("Unexpected installed runtime family.")
        latest = None
        for attempt in range(3):
            try:
                latest = lookup()
                break
            except (OSError, ValueError, EOFError):
                if attempt < 2:
                    time.sleep(2)
        if latest is None or latest < installed:
            protected.write_state(
                STATE,
                {
                    "checked_at": time.time(),
                    "status": "LOOKUP_FAILED",
                    "installed": installed,
                },
            )
            print("PYTHON_LOOKUP_FAILED_AFTER_THREE_ATTEMPTS", file=sys.stderr)
            return 1
        status = "UPDATE_AVAILABLE" if latest > installed else "CURRENT"
        protected.write_state(
            STATE,
            {
                "checked_at": time.time(),
                "status": status,
                "installed": installed,
                "latest": latest,
            },
        )
        print(
            f"PYTHON_{status} installed={'.'.join(map(str, installed))} latest={'.'.join(map(str, latest))}"
        )
        return int(latest > installed)
    except Exception:  # noqa: BLE001 - only sanitized maintenance categories may be logged.
        print("PYTHON_MAINTENANCE_FAILED", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
