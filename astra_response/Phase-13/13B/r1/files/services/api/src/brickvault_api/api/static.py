"""An immutable, bounded snapshot of an explicitly selected frontend build.

Only the entry, exact PWA files and flat Vite JS/CSS assets are public. Reading once
at startup keeps requests independent of subsequent file replacement or links.
"""

import os
import re
import stat
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response

from brickvault_api.settings import ConfigurationError

router = APIRouter(include_in_schema=False)
BUILD_ERROR = (
    "Static build unavailable or unsafe; run pnpm build and select a dedicated build directory."
)
MAX_BUILD_BYTES = 32 * 1024 * 1024
PWA_FILES = {
    "manifest.webmanifest": "application/manifest+json",
    "sw.js": "text/javascript",
    "icon-192.png": "image/png",
    "icon-512.png": "image/png",
}


def ordinary(path: Path) -> None:
    if any(p.is_symlink() or p.is_junction() for p in (path, *path.parents)):
        raise ConfigurationError(BUILD_ERROR)


def load_build(directory: str | None) -> dict[str, tuple[bytes, str]]:
    try:
        if directory is None or not Path(directory).is_absolute():
            raise ConfigurationError(BUILD_ERROR)
        root = Path(directory)
        ordinary(root)
        root = root.resolve(strict=True)
        entries = {p.name for p in root.iterdir()}
        base = {"index.html", "assets"}
        if entries not in (base, base | PWA_FILES.keys()):
            raise ConfigurationError(BUILD_ERROR)
        assets = root / "assets"
        ordinary(assets)
        files = [root / "index.html", *assets.iterdir()]
        files.extend(root / name for name in PWA_FILES if name in entries)
        if len(files) < 2 or len(files) > 100:
            raise ConfigurationError(BUILD_ERROR)
        result: dict[str, tuple[bytes, str]] = {}
        total = 0
        for path in files:
            ordinary(path)
            before = path.lstat()
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                raise ConfigurationError(BUILD_ERROR)
            if (
                path.parent == assets
                and re.fullmatch(r"[A-Za-z0-9_-]+\.(js|css)", path.name) is None
            ):
                raise ConfigurationError(BUILD_ERROR)
            total += before.st_size
            if total > MAX_BUILD_BYTES:
                raise ConfigurationError(BUILD_ERROR)
            with path.open("rb") as stream:
                opened = os.fstat(stream.fileno())
                if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                    raise ConfigurationError(BUILD_ERROR)
                content = stream.read(MAX_BUILD_BYTES + 1)
                after = os.fstat(stream.fileno())
            ordinary(path)
            if len(content) != before.st_size or after.st_mtime_ns != before.st_mtime_ns:
                raise ConfigurationError(BUILD_ERROR)
            media = PWA_FILES.get(path.name) or (
                "text/html"
                if path.name == "index.html"
                else "text/css"
                if path.suffix == ".css"
                else "text/javascript"
            )
            key = (
                "/"
                if path.name == "index.html"
                else ("/" + path.name if path.parent == root else "/assets/" + path.name)
            )
            result[key] = (content, media)
        return result
    except (OSError, ValueError):
        raise ConfigurationError(BUILD_ERROR) from None


def build_response(request: Request, key: str) -> Response:
    build = request.app.state.build
    if build is None or key not in build:
        raise HTTPException(404)
    content, media = build[key]
    # Only successful exact build lookups can opt into public caching. The
    # boundary ignores arbitrary Cache-Control headers on all other responses.
    request.state.public_static_cache = (
        "public, max-age=31536000, immutable"
        if re.fullmatch(r"/assets/[A-Za-z0-9_-]+-[A-Za-z0-9_-]{8,}\.(js|css)", key)
        else "no-cache"
    )
    return Response(content, media_type=media, headers={"X-Content-Type-Options": "nosniff"})


@router.get("/manifest.webmanifest")
def manifest(request: Request) -> Response:
    return build_response(request, "/manifest.webmanifest")


@router.get("/sw.js")
def service_worker(request: Request) -> Response:
    return build_response(request, "/sw.js")


@router.get("/icon-192.png")
def icon_small(request: Request) -> Response:
    return build_response(request, "/icon-192.png")


@router.get("/icon-512.png")
def icon_large(request: Request) -> Response:
    return build_response(request, "/icon-512.png")


@router.get("/")
def index(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/sets/{set_number}", include_in_schema=False)
def set_page(request: Request, set_number: str) -> Response:
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+\-]{0,255}", set_number) is None:
        raise HTTPException(404)
    return build_response(request, "/")


@router.get("/assets/{asset_path:path}")
def asset(request: Request, asset_path: str) -> Response:
    # Exact lookup: no filesystem joining, unquoting, traversal, or SPA fallback.
    return build_response(request, "/assets/" + asset_path)


@router.get("/deals/{forecast_id}", include_in_schema=False)
def forecast_page(request: Request, forecast_id: str) -> Response:
    if (
        re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", forecast_id)
        is None
    ):
        raise HTTPException(404)
    return build_response(request, "/")


@router.get("/deals", include_in_schema=False)
def forecast_index_page(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/watchlist", include_in_schema=False)
def watchlist_page(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/listings", include_in_schema=False)
def listings_page(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/listings/{listing_id}", include_in_schema=False)
def listing_page(request: Request, listing_id: str) -> Response:
    if (
        re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", listing_id)
        is None
    ):
        raise HTTPException(404)
    return build_response(request, "/")


@router.get("/settings", include_in_schema=False)
def settings_page(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/hunt", include_in_schema=False)
def hunt_page(request: Request) -> Response:
    return build_response(request, "/")


@router.get("/hunt/{run_id}", include_in_schema=False)
def hunt_run_page(request: Request, run_id: str) -> Response:
    if (
        re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", run_id)
        is None
    ):
        raise HTTPException(404)
    return build_response(request, "/")
