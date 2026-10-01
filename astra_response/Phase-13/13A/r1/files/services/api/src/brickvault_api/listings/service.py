"""Short PostgreSQL receipt/link/order transactions follow completed blob publication."""

import hashlib
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from uuid import UUID, uuid4

from psycopg.types.json import Jsonb

from brickvault_api.auth import AuthService, Session
from brickvault_api.catalog.connection import CatalogConnection, CatalogDatabase
from brickvault_api.images.processing import RECIPE, process_image
from brickvault_api.images.storage import BlobStore, ImageError, StoredBlob
from brickvault_api.listings.models import ListingCreate, UploadArguments


class ListingService:
    def __init__(self, database: CatalogDatabase, store: BlobStore | None) -> None:
        self.database, self.store = database, store

    @contextmanager
    def transaction(
        self, token: str | None, csrf: str | None = None
    ) -> Iterator[tuple[CatalogConnection, Session]]:
        with self.database.connect() as c, c.transaction():
            session = AuthService(self.database).check_in_transaction(c, token, csrf)
            yield c, session

    @staticmethod
    def projection(row: dict[str, Any]) -> dict[str, Any]:
        return {
            k: (str(v) if k == "asking_price" and v is not None else v)
            for k, v in row.items()
            if k != "owner_id"
        }

    def create(self, token: str | None, csrf: str, body: ListingCreate) -> dict[str, Any]:
        with self.transaction(token, csrf) as (c, owner):
            row = c.execute(
                "INSERT INTO listing(id,owner_id,source_type,source_url,title,description,asking_price,currency) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                (
                    uuid4(),
                    owner.principal_id,
                    body.source_type,
                    body.source_url,
                    body.title,
                    body.description,
                    body.price(),
                    body.currency,
                ),
            ).fetchone()
            assert row is not None
            result = self.projection(row)
        return result

    def list(self, token: str | None, limit: int, offset: int) -> dict[str, Any]:
        with self.transaction(token) as (c, owner):
            rows = c.execute(
                "SELECT * FROM listing WHERE owner_id=%s ORDER BY created_at DESC,id DESC LIMIT %s OFFSET %s",
                (owner.principal_id, limit + 1, offset),
            ).fetchall()
            return {
                "items": [self.projection(r) for r in rows[:limit]],
                "next_offset": offset + limit if len(rows) > limit else None,
            }

    def detail(self, token: str | None, listing_id: UUID) -> dict[str, Any]:
        with self.transaction(token) as (c, owner):
            # One statement pins metadata, visible order and receipt high-water together.
            row = c.execute(
                "SELECT l.*, coalesce((SELECT max(display_order)::bigint+1 FROM upload_receipt WHERE listing_id=l.id),0) AS next_display_order, "
                "coalesce((SELECT jsonb_agg(jsonb_build_object('listing_image_id',li.id,'original_asset_id',li.original_asset_id,"
                "'thumbnail_asset_id',r.child_id,'display_order',li.display_order) ORDER BY li.display_order) "
                "FROM listing_image li JOIN image_relation r ON r.parent_id=li.original_asset_id AND r.transformation_version=%s "
                "WHERE li.listing_id=l.id),'[]'::jsonb) AS images FROM listing l WHERE l.id=%s AND l.owner_id=%s",
                (RECIPE, listing_id, owner.principal_id),
            ).fetchone()
            if row is None:
                raise ImageError("LISTING_NOT_FOUND", 404)
            return self.projection(row)

    @staticmethod
    def record_blob(c: CatalogConnection, blob: StoredBlob) -> UUID:
        c.execute(
            "INSERT INTO blob(id,sha256,storage_key,byte_count) VALUES(%s,%s,%s,%s) ON CONFLICT(sha256) DO NOTHING",
            (uuid4(), blob.sha256, blob.key, blob.byte_count),
        )
        row = c.execute("SELECT * FROM blob WHERE sha256=%s", (blob.sha256,)).fetchone()
        if row is None or row["storage_key"] != blob.key or row["byte_count"] != blob.byte_count:
            raise ImageError("BLOB_METADATA_CONFLICT", 503)
        return UUID(str(row["id"]))

    @staticmethod
    def record_asset(
        c: CatalogConnection,
        blob_id: UUID,
        format_name: str,
        width: int,
        height: int,
        kind: str,
        privacy: str,
    ) -> UUID:
        row = c.execute(
            "INSERT INTO image_asset(id,blob_id,format,width,height,kind,privacy) VALUES(%s,%s,%s,%s,%s,%s,%s) "
            "ON CONFLICT(blob_id,kind) DO UPDATE SET privacy=CASE WHEN image_asset.privacy='restricted' OR EXCLUDED.privacy='restricted' "
            "THEN 'restricted' ELSE 'private' END RETURNING *",
            (uuid4(), blob_id, format_name, width, height, kind, privacy),
        ).fetchone()
        assert row is not None
        if (row["format"], row["width"], row["height"]) != (format_name, width, height):
            raise ImageError("ASSET_METADATA_CONFLICT", 503)
        return UUID(str(row["id"]))

    def upload(
        self,
        token: str | None,
        csrf: str,
        listing_id: UUID,
        arguments: UploadArguments,
        filename: str,
        data: bytes,
    ) -> tuple[int, dict[str, Any]]:
        if self.store is None:
            raise ImageError("IMAGE_STORAGE_NOT_CONFIGURED", 503)
        # Reject nonexistent/other-owner targets before costly decode/storage. No row lock.
        self.detail(token, listing_id)
        # A committed UUID is bound to its bytes/position even if replacement
        # bytes are corrupt. Inspect this immutable receipt before decoding;
        # recheck under the row lock to handle a concurrently committed receipt.
        with self.transaction(token, csrf) as (c, _):
            admitted = c.execute(
                "SELECT content_hash,display_order FROM upload_receipt WHERE listing_id=%s AND client_upload_id=%s",
                (listing_id, arguments.client_upload_id),
            ).fetchone()
            if admitted is not None and (
                admitted["content_hash"] != hashlib.sha256(data).hexdigest()
                or admitted["display_order"] != arguments.display_order
            ):
                raise ImageError("UPLOAD_ID_CONFLICT", 409)
        processed = process_image(data)
        original = self.store.publish(data)
        thumbnail = self.store.publish(processed.thumbnail)
        with self.transaction(token, csrf) as (c, owner):
            listing = c.execute(
                "SELECT * FROM listing WHERE id=%s AND owner_id=%s FOR UPDATE",
                (listing_id, owner.principal_id),
            ).fetchone()
            if listing is None:
                raise ImageError("LISTING_NOT_FOUND", 404)
            receipt = c.execute(
                "SELECT * FROM upload_receipt WHERE listing_id=%s AND client_upload_id=%s",
                (listing_id, arguments.client_upload_id),
            ).fetchone()
            if receipt is not None:
                if (
                    receipt["content_hash"] != original.sha256
                    or receipt["display_order"] != arguments.display_order
                ):
                    raise ImageError("UPLOAD_ID_CONFLICT", 409)
                return 200, dict(receipt["stored_result"])
            if c.execute(
                "SELECT 1 FROM upload_receipt WHERE listing_id=%s AND display_order=%s",
                (listing_id, arguments.display_order),
            ).fetchone():
                raise ImageError("DISPLAY_ORDER_CONFLICT", 409)
            # Unknown inputs and screen captures are restricted. Explicit photo metadata
            # is private; sharing bytes can only escalate the canonical asset's privacy.
            privacy = (
                "private"
                if listing["source_type"] in ("seller_photo", "listing_photo")
                else "restricted"
            )
            original_id = self.record_asset(
                c,
                self.record_blob(c, original),
                processed.format,
                processed.width,
                processed.height,
                "original",
                privacy,
            )
            thumb_id = self.record_asset(
                c,
                self.record_blob(c, thumbnail),
                "JPEG",
                processed.thumbnail_width,
                processed.thumbnail_height,
                "thumbnail",
                privacy,
            )
            # A restricted canonical original cannot yield a less restricted thumbnail.
            c.execute(
                "UPDATE image_asset SET privacy='restricted' WHERE id=%s AND EXISTS(SELECT 1 FROM image_asset WHERE id=%s AND privacy='restricted')",
                (thumb_id, original_id),
            )
            c.execute(
                "INSERT INTO image_relation(id,parent_id,child_id,transformation_version,transformation_metadata) "
                "VALUES(%s,%s,%s,%s,%s) ON CONFLICT(parent_id,transformation_version) DO NOTHING",
                (uuid4(), original_id, thumb_id, RECIPE, Jsonb(processed.metadata)),
            )
            link = c.execute(
                "SELECT id,display_order FROM listing_image WHERE listing_id=%s AND original_asset_id=%s",
                (listing_id, original_id),
            ).fetchone()
            duplicate = link is not None
            identifier = link["id"] if link is not None else uuid4()
            if link is None:
                c.execute(
                    "INSERT INTO listing_image(id,listing_id,original_asset_id,display_order) VALUES(%s,%s,%s,%s)",
                    (identifier, listing_id, original_id, arguments.display_order),
                )
            elif arguments.display_order < link["display_order"]:
                c.execute(
                    "UPDATE listing_image SET display_order=%s WHERE id=%s",
                    (arguments.display_order, identifier),
                )
            result = {
                "client_upload_id": str(arguments.client_upload_id),
                "filename": filename,
                "status": "duplicate" if duplicate else "uploaded",
                "listing_image_id": str(identifier),
                "error": None,
            }
            c.execute(
                "INSERT INTO upload_receipt(id,listing_id,client_upload_id,filename,content_hash,display_order,listing_image_id,stored_result) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    uuid4(),
                    listing_id,
                    arguments.client_upload_id,
                    filename,
                    original.sha256,
                    arguments.display_order,
                    identifier,
                    Jsonb(result),
                ),
            )
        # This return runs only after the transaction context has committed.
        return (200 if duplicate else 201), result

    def content(self, token: str | None, asset_id: UUID) -> tuple[str, str]:
        with self.transaction(token) as (c, owner):
            row = c.execute(
                "SELECT b.sha256,a.format FROM image_asset a JOIN blob b ON b.id=a.blob_id "
                "WHERE a.id=%s AND EXISTS(SELECT 1 FROM listing_image li JOIN listing l ON l.id=li.listing_id "
                "LEFT JOIN image_relation r ON r.parent_id=li.original_asset_id "
                "WHERE l.owner_id=%s AND (li.original_asset_id=a.id OR r.child_id=a.id))",
                (asset_id, owner.principal_id),
            ).fetchone()
            if row is None:
                raise ImageError("IMAGE_NOT_FOUND", 404)
            return row["sha256"], {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}[
                row["format"]
            ]
