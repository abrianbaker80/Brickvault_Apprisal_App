"""Compact 13A proof on real owned PostgreSQL and disposable synthetic image bytes."""

import hashlib
import io
import secrets
import struct
import zlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from threading import Barrier
from typing import Any
from uuid import UUID, uuid4

import pytest
from alembic import command
from fastapi.testclient import TestClient
from PIL import Image
from psycopg.errors import CheckViolation
from sqlalchemy import text

from brickvault_api.auth import AuthService
from brickvault_api.catalog.connection import CatalogDatabase
from brickvault_api.images.consistency import inspect_storage
from brickvault_api.images.processing import MAX_FILE_BYTES
from brickvault_api.images.storage import FilesystemBlobStore, ImageError
from brickvault_api.listings.models import UploadArguments
from brickvault_api.listings.service import ListingService
from brickvault_api.main import create_app
from brickvault_api.persistence.database import create_database_engine, migration_config
from brickvault_api.settings import RuntimeSettings


def image_bytes(
    format_name: str = "JPEG", color: str = "red", size: tuple[int, int] = (640, 320)
) -> bytes:
    output = io.BytesIO()
    Image.new("RGBA" if format_name == "PNG" else "RGB", size, color).save(
        output, format=format_name
    )
    return output.getvalue()


@dataclass
class Harness:
    client: TestClient
    owner: CatalogDatabase
    runtime: CatalogDatabase
    store: FilesystemBlobStore
    token: str
    csrf: str

    def listing(self, **body: Any) -> str:
        response = self.client.post("/api/listings", json=body, headers=self.headers)
        assert response.status_code == 201
        return str(response.json()["id"])

    @property
    def headers(self) -> dict[str, str]:
        return {"Origin": "http://127.0.0.1:18000", "X-CSRF-Token": self.csrf}

    def upload(
        self,
        listing: str,
        data: bytes,
        position: int = 0,
        identifier: UUID | None = None,
        filename: str = "synthetic.jpg",
    ) -> Any:
        return self.client.post(
            f"/api/listings/{listing}/images",
            headers=self.headers,
            files={"file": (filename, data, "application/octet-stream")},
            data={"client_upload_id": str(identifier or uuid4()), "display_order": str(position)},
        )

    def rows(self, query: str, args: tuple[object, ...] = ()) -> list[dict[str, Any]]:
        with self.owner.connect() as c:
            return c.execute(query, args).fetchall()


@pytest.fixture
def h(
    test_settings: RuntimeSettings,
    owned_instance: Any,
    disposable_database: str,
    integration_run_id: str,
    tmp_path: Path,
) -> Any:
    from database import database_marker

    owner = CatalogDatabase(
        owned_instance.target(disposable_database, "owner"),
        "test",
        database_marker(owned_instance, integration_run_id),
    )
    runtime = CatalogDatabase(
        test_settings.database_url.get_secret_value(),
        "test",
        test_settings.database_ownership_marker.get_secret_value(),
        role="runtime",
    )
    password = secrets.token_urlsafe(32)
    # One disposable database is shared by this focused file; provision the sole owner once.
    with owner.connect() as c:
        provisioned = c.execute("SELECT 1 FROM auth_principal").fetchone() is not None
    if provisioned:
        # Replace only the owned TEST principal password, retaining its identity.
        from argon2 import PasswordHasher

        with owner.connect() as c:
            c.execute(
                "UPDATE auth_principal SET password_hash=%s", (PasswordHasher().hash(password),)
            )
    else:
        AuthService(owner).provision(password)
    settings = test_settings.model_copy(update={"image_blob_root": str(tmp_path / "blobs")})
    with TestClient(
        create_app(settings), base_url="http://127.0.0.1:18000", raise_server_exceptions=False
    ) as client:
        response = client.post(
            "/api/auth/login",
            json={"password": password},
            headers={"Origin": "http://127.0.0.1:18000", "X-BrickVault-Login": "1"},
        )
        assert response.status_code == 200
        yield Harness(
            client,
            owner,
            runtime,
            FilesystemBlobStore(tmp_path / "blobs"),
            client.cookies["bva_session"],
            response.json()["csrf_token"],
        )


def test_listing_metadata_decimal_missing_zero_and_pagination(h: Harness) -> None:
    missing, zero = (
        h.listing(),
        h.listing(asking_price="0", source_url="https://example.invalid/listing"),
    )
    assert h.client.get(f"/api/listings/{missing}").json()["asking_price"] is None
    assert h.client.get(f"/api/listings/{zero}").json()["asking_price"] == "0.00"
    assert h.client.get("/api/listings?limit=1").json()["next_offset"] == 1
    assert h.client.get("/api/listings?limit=101").status_code == 422
    assert (
        h.client.post(
            "/api/listings", json={"source_url": "file:///secret"}, headers=h.headers
        ).status_code
        == 422
    )


def test_valid_jpeg_original_thumbnail_and_exact_content(h: Harness) -> None:
    listing, data = h.listing(source_type="listing_photo"), image_bytes()
    uploaded = h.upload(listing, data)
    assert uploaded.status_code == 201 and uploaded.json()["status"] == "uploaded"
    entry = h.client.get(f"/api/listings/{listing}").json()["images"][0]
    original = h.client.get("/api/images/" + entry["original_asset_id"] + "/content")
    assert original.content == data and original.headers["cache-control"] == "no-store"
    assert original.headers["x-content-type-options"] == "nosniff"
    thumbnail = h.client.get("/api/images/" + entry["thumbnail_asset_id"] + "/content")
    with Image.open(io.BytesIO(thumbnail.content)) as image:
        assert image.size == (512, 256) and image.mode == "RGB" and not image.getexif()
    assert entry["original_asset_id"] != entry["thumbnail_asset_id"]
    relation = h.rows(
        "SELECT transformation_metadata FROM image_relation WHERE parent_id=%s",
        (UUID(entry["original_asset_id"]),),
    )[0]
    assert relation["transformation_metadata"]["decoder_version"] == "12.3.0"


def test_png_webp_transparency_no_enlargement_and_exif(h: Harness) -> None:
    listing = h.listing(source_type="raw_screenshot")
    for position, format_name in enumerate(("PNG", "WEBP")):
        data = image_bytes(format_name, "#00000000" if format_name == "PNG" else "blue", (20, 10))
        assert h.upload(listing, data, position).status_code == 201
    for entry in h.client.get(f"/api/listings/{listing}").json()["images"]:
        thumbnail = h.client.get("/api/images/" + entry["thumbnail_asset_id"] + "/content")
        with Image.open(io.BytesIO(thumbnail.content)) as image:
            assert image.size == (20, 10) and image.mode == "RGB"
            if entry["display_order"] == 0:
                assert image.getpixel((0, 0)) == (255, 255, 255)
    output = io.BytesIO()
    source = Image.new("RGB", (20, 10), "green")
    exif = Image.Exif()
    exif[274] = 6
    source.save(output, format="JPEG", exif=exif)
    assert h.upload(listing, output.getvalue(), 2).status_code == 201
    entry = h.client.get(f"/api/listings/{listing}").json()["images"][2]
    with Image.open(
        io.BytesIO(h.client.get("/api/images/" + entry["thumbnail_asset_id"] + "/content").content)
    ) as image:
        assert image.size == (10, 20) and not image.getexif()


def test_duplicate_receipt_and_exact_replay(h: Harness) -> None:
    listing, data, first_id, copy_id = h.listing(), image_bytes(color="purple"), uuid4(), uuid4()
    first = h.upload(listing, data, 0, first_id).json()
    duplicate = h.upload(listing, data, 2, copy_id)
    assert duplicate.status_code == 200 and duplicate.json()["status"] == "duplicate"
    assert duplicate.json()["listing_image_id"] == first["listing_image_id"]
    replay = h.upload(listing, data, 2, copy_id, filename="changed-name.jpg")
    assert replay.status_code == 200 and replay.json() == duplicate.json()
    assert h.upload(listing, data, 0, first_id).json() == first
    detail = h.client.get(f"/api/listings/{listing}").json()
    assert len(detail["images"]) == 1 and detail["next_display_order"] == 3
    assert len(h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),))) == 2


def test_upload_id_conflicts_do_not_mutate_receipt(h: Harness) -> None:
    listing, identifier, data = h.listing(), uuid4(), image_bytes(color="orange")
    assert h.upload(listing, data, 0, identifier).status_code == 201
    for bytes_value, position in (
        (image_bytes(color="white"), 0),
        (data, 1),
        (b"corrupt replacement", 0),
    ):
        response = h.upload(listing, bytes_value, position, identifier)
        assert (
            response.status_code == 409 and response.json()["error"]["code"] == "UPLOAD_ID_CONFLICT"
        )
    assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 1


def test_receipt_position_conflict_even_for_same_bytes(h: Harness) -> None:
    listing, data = h.listing(), image_bytes(color="yellow")
    assert h.upload(listing, data, 4).status_code == 201
    response = h.upload(listing, data, 4)
    assert (
        response.status_code == 409 and response.json()["error"]["code"] == "DISPLAY_ORDER_CONFLICT"
    )
    assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 5


def test_shared_identical_original_across_listings(h: Harness) -> None:
    left, right, data = (
        h.listing(source_type="seller_photo"),
        h.listing(source_type="raw_screenshot"),
        image_bytes(color="cyan"),
    )
    assert h.upload(left, data).status_code == 201 and h.upload(right, data).status_code == 201
    entries = [
        h.client.get(f"/api/listings/{listing}").json()["images"][0] for listing in (left, right)
    ]
    assert entries[0]["original_asset_id"] == entries[1]["original_asset_id"]
    assert entries[0]["listing_image_id"] != entries[1]["listing_image_id"]
    assert (
        len(h.rows("SELECT * FROM blob WHERE sha256=%s", (hashlib.sha256(data).hexdigest(),))) == 1
    )
    assert (
        h.rows(
            "SELECT privacy FROM image_asset WHERE id=%s", (UUID(entries[0]["original_asset_id"]),)
        )[0]["privacy"]
        == "restricted"
    )


def test_grouped_invalid_images_and_failed_upload_has_no_receipt(h: Harness) -> None:
    listing = h.listing()
    animated = io.BytesIO()
    Image.new("RGB", (10, 10), "red").save(
        animated,
        format="WEBP",
        save_all=True,
        append_images=[Image.new("RGB", (10, 10), "blue")],
        duration=100,
        loop=0,
    )

    def header_image(width: int, height: int) -> bytes:
        data = bytearray(image_bytes("PNG", size=(2, 2)))
        data[16:24] = struct.pack(">II", width, height)
        data[29:33] = struct.pack(">I", zlib.crc32(data[12:29]))
        return bytes(data)

    cases = [
        (b"corrupt", "INVALID_IMAGE"),
        (image_bytes()[:100], "INVALID_IMAGE"),
        (b"x" * (MAX_FILE_BYTES + 1), "IMAGE_FILE_TOO_LARGE"),
        (animated.getvalue(), "ANIMATED_IMAGE"),
        (header_image(16001, 1), "IMAGE_DIMENSIONS_EXCEEDED"),
        (header_image(10000, 5000), "IMAGE_DIMENSIONS_EXCEEDED"),
        (header_image(40000, 40000), "IMAGE_DECOMPRESSION_BOMB"),
        (image_bytes("GIF"), "UNSUPPORTED_IMAGE_FORMAT"),
    ]
    for data, code in cases:
        response = h.upload(listing, data)
        assert response.status_code in (413, 422) and response.json()["error"]["code"] == code
    assert h.client.get(f"/api/listings/{listing}").json()["images"] == []
    assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 0


def test_chunked_ceiling_multipart_and_private_access(
    h: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    listing = h.listing()

    def chunks() -> Any:
        for _ in range(27):
            yield b"x" * (1024 * 1024)

    response = h.client.post(
        f"/api/listings/{listing}/images",
        headers={**h.headers, "Content-Type": "multipart/form-data; boundary=x"},
        content=chunks(),
    )
    assert (
        response.status_code == 413
        and response.json()["error"]["code"] == "IMAGE_REQUEST_TOO_LARGE"
    )
    response = h.client.post(
        f"/api/listings/{listing}/images",
        headers=h.headers,
        files=[("file", ("a.jpg", image_bytes())), ("file", ("b.jpg", image_bytes()))],
        data={"client_upload_id": str(uuid4()), "display_order": "0"},
    )
    assert response.status_code == 400
    assert (
        h.client.post("/api/listings", json={}, headers={"Origin": h.headers["Origin"]}).status_code
        == 403
    )
    assert (
        h.client.post(
            "/api/listings", json={}, headers={**h.headers, "Origin": "https://invalid.example"}
        ).status_code
        == 403
    )
    assert h.client.get(f"/api/images/{uuid4()}/content").status_code == 404
    publish = FilesystemBlobStore.publish
    revoked = False

    def revoke_after_publish(store: FilesystemBlobStore, data: bytes) -> Any:
        nonlocal revoked
        result = publish(store, data)
        if not revoked:
            revoked = True
            with h.owner.connect() as c:
                from brickvault_api.auth import digest

                c.execute(
                    "UPDATE auth_session SET revoked_at=CURRENT_TIMESTAMP WHERE token_hash=%s",
                    (digest(h.token),),
                )
        return result

    monkeypatch.setattr(FilesystemBlobStore, "publish", revoke_after_publish)
    expired = h.upload(listing, image_bytes(color="gold"))
    assert expired.status_code == 401 and expired.json()["status"] == "failed"
    assert not h.rows("SELECT 1 FROM upload_receipt WHERE listing_id=%s", (UUID(listing),))
    h.client.cookies.clear()
    for path in ("/api/listings", f"/api/listings/{listing}", f"/api/images/{uuid4()}/content"):
        assert h.client.get(path).status_code == 401
    assert (
        h.client.post(
            f"/api/listings/{listing}/images", headers=h.headers, content=b"bad"
        ).status_code
        == 401
    )


def test_real_postgresql_ordering_with_late_lower_duplicate_and_restart(h: Harness) -> None:
    listing, a, b = UUID(h.listing()), image_bytes(color="pink"), image_bytes(color="brown")
    barrier = Barrier(2)
    base = h.store

    class Rendezvous(FilesystemBlobStore):
        def publish(self, data: bytes) -> Any:
            result = super().publish(data)
            if data in (a, b):
                barrier.wait(timeout=10)
            return result

    service = ListingService(h.runtime, Rendezvous(base.root))

    def upload(data: bytes, position: int) -> tuple[int, dict[str, Any]]:
        return service.upload(
            h.token,
            h.csrf,
            listing,
            UploadArguments(client_upload_id=uuid4(), display_order=position),
            "fixture.jpg",
            data,
        )

    # A-copy@2 and B@1 really overlap before their per-listing DB transactions.
    with ThreadPoolExecutor(max_workers=2) as pool:
        af, bf = pool.submit(upload, a, 2), pool.submit(upload, b, 1)
        assert af.result()[0] == 201 and bf.result()[0] == 201
    plain = ListingService(h.runtime, base)
    assert (
        plain.upload(
            h.token,
            h.csrf,
            listing,
            UploadArguments(client_upload_id=uuid4(), display_order=0),
            "a.jpg",
            a,
        )[0]
        == 200
    )
    restarted = ListingService(h.runtime, FilesystemBlobStore(base.root))
    detail = restarted.detail(h.token, listing)
    assert [entry["display_order"] for entry in detail["images"]] == [0, 1] and detail[
        "next_display_order"
    ] == 3
    assert [
        row["display_order"]
        for row in h.rows(
            "SELECT display_order FROM upload_receipt WHERE listing_id=%s ORDER BY display_order",
            (listing,),
        )
    ] == [0, 1, 2]


def test_failed_real_database_commit_leaves_no_false_success(h: Harness) -> None:
    listing = h.listing()
    with h.owner.connect() as c:
        c.execute(
            "CREATE FUNCTION public.test_13a_commit_failure() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'injected commit failure'; END $$"
        )
        c.execute(
            "CREATE CONSTRAINT TRIGGER test_13a_failure AFTER INSERT ON upload_receipt DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.test_13a_commit_failure()"
        )
    try:
        response = h.upload(listing, image_bytes(color="lime"))
        assert response.status_code == 503 and response.json()["status"] == "failed"
        assert h.client.get(f"/api/listings/{listing}").json()["images"] == []
        assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 0
        assert list(h.store.enumerate())
    finally:
        with h.owner.connect() as c:
            c.execute("DROP TRIGGER test_13a_failure ON upload_receipt")
            c.execute("DROP FUNCTION public.test_13a_commit_failure()")
    assert h.upload(listing, image_bytes(color="lime")).status_code == 201


def test_blob_immutable_reuse_corruption_and_report_only_consistency(h: Harness) -> None:
    with pytest.raises(ImageError, match="UNSAFE_BLOB_ROOT"):
        FilesystemBlobStore(h.store.root, forbidden_roots=(h.store.root.parent,))
    listing, data = h.listing(), image_bytes(color="black")
    assert h.upload(listing, data).status_code == 201
    original = h.store.publish(data)
    orphan = h.store.publish(b"synthetic orphan")
    missing_path = h.store.root / original.key
    missing_path.unlink()  # Explicit fault injection on disposable TEST bytes only.
    stage = h.store.root / ".stage-synthetic"
    stage.write_bytes(b"staging")
    report = inspect_storage(h.runtime, h.store)
    assert (
        original.key in report.missing
        and orphan.key in report.unreferenced
        and ".stage-synthetic" in report.staging
    )
    assert stage.exists() and (h.store.root / orphan.key).exists()
    h.store.publish(data)
    missing_path.write_bytes(b"corrupt")
    with pytest.raises(ImageError, match="BLOB_CORRUPT"):
        h.store.publish(data)
    assert missing_path.read_bytes() == b"corrupt"
    assert original.key in inspect_storage(h.runtime, h.store).corrupt


def test_postgresql_immutable_receipts_and_minimum_order_constraints(h: Harness) -> None:
    listing = h.listing()
    assert h.upload(listing, image_bytes(color="navy")).status_code == 201
    with h.owner.connect() as c:
        with pytest.raises(CheckViolation), c.transaction():
            c.execute(
                "INSERT INTO upload_receipt(id,listing_id,client_upload_id,filename,content_hash,display_order,listing_image_id,stored_result) "
                "SELECT %s,listing_id,%s,filename,content_hash,5,listing_image_id,jsonb_build_object('status',NULL,'client_upload_id',NULL,'listing_image_id',NULL,'filename',NULL,'error',NULL) "
                "FROM upload_receipt WHERE listing_id=%s",
                (uuid4(), uuid4(), UUID(listing)),
            )
        with pytest.raises(Exception, match="IMMUTABLE_IMAGE_RECORD"), c.transaction():
            c.execute(
                "UPDATE upload_receipt SET display_order=10 WHERE listing_id=%s", (UUID(listing),)
            )
        with pytest.raises(Exception, match="IMAGE_RECEIPT_ORDER_OR_HASH"), c.transaction():
            c.execute(
                "UPDATE listing_image SET display_order=10 WHERE listing_id=%s", (UUID(listing),)
            )
    assert h.client.get(f"/api/listings/{listing}").json()["images"][0]["display_order"] == 0


def test_disposable_0016_upgrade_preservation_and_downgrade_smoke(
    h: Harness, owned_instance: Any, disposable_database: str
) -> None:
    # A separate owned disposable DB is provisioned by the small runner for this gate.
    from database import cleanup_database, provision

    from brickvault_api.persistence.runtime_grants import grant_runtime

    name, run = "brickvault_test_" + uuid4().hex, uuid4().hex
    provision(owned_instance, name, run)
    engine = create_database_engine(owned_instance.target(name, "owner"), "test", "owner")
    try:
        with engine.begin() as c:
            cfg = migration_config()
            cfg.attributes["connection"] = c
            command.upgrade(cfg, "0016_hunt_cached_runs")
            before = c.execute(text("SELECT count(*) FROM public.auth_control")).scalar()
            command.upgrade(cfg, "head")
            assert (
                c.execute(text("SELECT version_num FROM public.alembic_version")).scalar()
                == "0017_listing_images"
            )
            assert c.execute(text("SELECT count(*) FROM public.auth_control")).scalar() == before
            grant_runtime(c, "brickvault_test_runtime")
            command.downgrade(cfg, "0016_hunt_cached_runs")
            command.upgrade(cfg, "head")
        assert (
            len(
                h.rows(
                    "SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename IN ('listing','blob','image_asset','image_relation','listing_image','upload_receipt')"
                )
            )
            == 6
        )
    finally:
        engine.dispose()
        cleanup_database(owned_instance, name, run, [name])
