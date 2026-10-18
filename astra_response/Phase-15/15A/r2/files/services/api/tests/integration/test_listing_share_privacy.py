"""15A restricted Share admission on real owned PostgreSQL and immutable blobs."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Event
from typing import Any
from uuid import UUID, uuid4

import pytest

from brickvault_api.catalog.connection import CatalogConnection
from brickvault_api.images.storage import FilesystemBlobStore, StoredBlob
from brickvault_api.listings.models import UploadArguments
from brickvault_api.listings.service import ListingService

from .test_listing_images import Harness, image_bytes
from .test_listing_images import h as h


def fixture_bytes() -> bytes:
    # Every test gets independent pixels/bytes in the shared disposable database.
    return image_bytes("PNG", "#" + uuid4().hex[:6], (37, 19))


def upload(
    h: Harness,
    listing: str,
    data: bytes,
    position: int = 0,
    identifier: UUID | None = None,
    *,
    elevation: str | None = "restricted",
) -> Any:
    fields = {"client_upload_id": str(identifier or uuid4()), "display_order": str(position)}
    if elevation is not None:
        fields["privacy_elevation"] = elevation
    return h.client.post(
        f"/api/listings/{listing}/images",
        headers=h.headers,
        files={"file": ("neutral-share.png", data, "image/png")},
        data=fields,
    )


def asset_privacy(h: Harness, listing: str) -> dict[str, str]:
    original = h.client.get(f"/api/listings/{listing}").json()["images"][0]["original_asset_id"]
    rows = h.rows(
        "SELECT id,privacy FROM image_asset WHERE id=%s OR id IN "
        "(SELECT child_id FROM image_relation WHERE parent_id=%s)",
        (UUID(original), UUID(original)),
    )
    assert len(rows) == 2  # 0017 admits one canonical original and thumbnail-v1.
    return {str(row["id"]): row["privacy"] for row in rows}


def test_first_share_restricts_photo_source_without_changing_listing_metadata(h: Harness) -> None:
    listing, data = h.listing(source_type="seller_photo"), fixture_bytes()
    response = upload(h, listing, data)
    assert response.status_code == 201
    assert set(asset_privacy(h, listing).values()) == {"restricted"}
    detail = h.client.get(f"/api/listings/{listing}").json()
    assert detail["source_type"] == "seller_photo" and detail["next_display_order"] == 1
    original = detail["images"][0]["original_asset_id"]
    assert h.client.get(f"/api/images/{original}/content").content == data


def test_restricted_replay_escalates_existing_assets_without_new_receipt_or_result(
    h: Harness,
) -> None:
    listing, data, identifier = h.listing(source_type="listing_photo"), fixture_bytes(), uuid4()
    first = upload(h, listing, data, identifier=identifier, elevation=None)
    assert first.status_code == 201 and set(asset_privacy(h, listing).values()) == {"private"}
    receipts = h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),))
    replay = upload(h, listing, data, identifier=identifier)
    assert replay.status_code == 200 and replay.json() == first.json()
    assert set(asset_privacy(h, listing).values()) == {"restricted"}
    assert h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),)) == receipts
    assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 1
    # Omitting elevation later cannot downgrade any shared/retained asset.
    assert upload(h, listing, data, identifier=identifier, elevation=None).json() == first.json()
    assert set(asset_privacy(h, listing).values()) == {"restricted"}


def test_new_uuid_duplicate_elevates_and_keeps_receipt_order_contract(h: Harness) -> None:
    listing, data = h.listing(source_type="seller_photo"), fixture_bytes()
    first = upload(h, listing, data, position=3, elevation=None)
    assert first.status_code == 201 and set(asset_privacy(h, listing).values()) == {"private"}
    duplicate = upload(h, listing, data, position=1)
    assert duplicate.status_code == 200 and duplicate.json()["status"] == "duplicate"
    assert duplicate.json()["listing_image_id"] == first.json()["listing_image_id"]
    assert set(asset_privacy(h, listing).values()) == {"restricted"}
    detail = h.client.get(f"/api/listings/{listing}").json()
    assert len(detail["images"]) == 1 and detail["images"][0]["display_order"] == 1
    assert detail["next_display_order"] == 4
    assert len(h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),))) == 2


def test_cross_listing_original_and_thumbnail_escalation_is_monotone(h: Harness) -> None:
    left, right, data = (
        h.listing(source_type="seller_photo"),
        h.listing(source_type="listing_photo"),
        fixture_bytes(),
    )
    assert upload(h, left, data, elevation=None).status_code == 201
    assert set(asset_privacy(h, left).values()) == {"private"}
    assert upload(h, right, data).status_code == 201
    assert asset_privacy(h, left) == asset_privacy(h, right)
    assert set(asset_privacy(h, left).values()) == {"restricted"}
    assert upload(h, left, data, position=1, elevation=None).status_code == 200
    assert set(asset_privacy(h, left).values()) == {"restricted"}


def test_conflicting_elevated_requests_mutate_no_privacy_receipt_or_order(h: Harness) -> None:
    listing, data, identifier = h.listing(source_type="seller_photo"), fixture_bytes(), uuid4()
    assert upload(h, listing, data, identifier=identifier, elevation=None).status_code == 201
    before = asset_privacy(h, listing)
    receipts = h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),))
    for body, position, identity, code in (
        (fixture_bytes(), 0, identifier, "UPLOAD_ID_CONFLICT"),
        (data, 1, identifier, "UPLOAD_ID_CONFLICT"),
        (data, 0, uuid4(), "DISPLAY_ORDER_CONFLICT"),
    ):
        response = upload(h, listing, body, position, identity)
        assert response.status_code == 409 and response.json()["error"]["code"] == code
        assert asset_privacy(h, listing) == before
        assert (
            h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),)) == receipts
        )
    assert h.client.get(f"/api/listings/{listing}").json()["next_display_order"] == 1


@pytest.mark.parametrize("value", ["private", "", "null", "Restricted"])
def test_invalid_elevation_refuses_before_storage_or_metadata(h: Harness, value: str) -> None:
    listing, data = h.listing(source_type="seller_photo"), fixture_bytes()
    response = upload(h, listing, data, elevation=value)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_PRIVACY_ELEVATION"
    assert h.client.get(f"/api/listings/{listing}").json()["images"] == []
    assert h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),)) == []
    assert list(h.store.enumerate()) == []


def test_duplicate_extra_and_file_valued_multipart_fields_fail_before_upload(h: Harness) -> None:
    listing, data = h.listing(source_type="seller_photo"), fixture_bytes()
    base = [
        ("file", ("neutral-share.png", data, "image/png")),
        ("client_upload_id", (None, str(uuid4()))),
        ("display_order", (None, "0")),
    ]
    for additions in (
        [("privacy_elevation", (None, "restricted")), ("privacy_elevation", (None, "restricted"))],
        [("unknown", (None, "restricted"))],
        [("privacy_elevation", ("private-file.png", data, "image/png"))],
        [("client_upload_id", base[1][1])],
    ):
        response = h.client.post(
            f"/api/listings/{listing}/images", headers=h.headers, files=[*base, *additions]
        )
        assert response.status_code in (400, 422)
        assert response.json()["error"]["code"] == "INVALID_MULTIPART"
    assert h.client.get(f"/api/listings/{listing}").json()["images"] == []
    assert h.rows("SELECT * FROM upload_receipt WHERE listing_id=%s", (UUID(listing),)) == []
    assert list(h.store.enumerate()) == []


@pytest.mark.parametrize("restricted_first", [False, True])
def test_ordered_overlapping_cross_listing_uploads_never_downgrade(
    h: Harness, restricted_first: bool
) -> None:
    first_listing, second_listing, data = (
        UUID(h.listing(source_type="seller_photo")),
        UUID(h.listing(source_type="listing_photo")),
        fixture_bytes(),
    )
    published = Barrier(2)
    first_inside, second_published = Event(), Event()

    class FirstStore(FilesystemBlobStore):
        def publish(self, value: bytes) -> StoredBlob:
            result = super().publish(value)
            if value == data:
                published.wait(timeout=10)
            return result

    class SecondStore(FilesystemBlobStore):
        def publish(self, value: bytes) -> StoredBlob:
            result = super().publish(value)
            if value == data:
                published.wait(timeout=10)
                assert first_inside.wait(timeout=10)
            else:
                second_published.set()
            return result

    class HoldingService(ListingService):
        @staticmethod
        def inherit_privacy(
            c: CatalogConnection, original_id: UUID, *, restricted: bool = False
        ) -> None:
            first_inside.set()
            assert second_published.wait(timeout=10)
            ListingService.inherit_privacy(c, original_id, restricted=restricted)

    first = HoldingService(h.runtime, FirstStore(h.store.root))
    second = ListingService(h.runtime, SecondStore(h.store.root))

    def submit(
        service: ListingService, listing: UUID, restricted: bool
    ) -> tuple[int, dict[str, Any]]:
        return service.upload(
            h.token,
            h.csrf,
            listing,
            UploadArguments(
                client_upload_id=uuid4(),
                display_order=0,
                privacy_elevation="restricted" if restricted else None,
            ),
            "neutral-share.png",
            data,
        )

    # Both requests finish real admission before rendezvousing in blob publication.
    # The first metadata transaction holds the production auth/listing/asset locks
    # while the second finishes publication, then the second commits afterward.
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(submit, first, first_listing, restricted_first)
        b = pool.submit(submit, second, second_listing, not restricted_first)
        assert a.result(timeout=20)[0] == 201 and b.result(timeout=20)[0] == 201
    assert asset_privacy(h, str(first_listing)) == asset_privacy(h, str(second_listing))
    assert set(asset_privacy(h, str(first_listing)).values()) == {"restricted"}
    assert (
        len(
            h.rows(
                "SELECT * FROM upload_receipt WHERE listing_id IN (%s,%s)",
                (first_listing, second_listing),
            )
        )
        == 2
    )
