from datetime import datetime
from decimal import Decimal
from typing import Literal
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ListingModel(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)


class ListingCreate(ListingModel):
    source_type: str | None = Field(default=None, max_length=80)
    source_url: str | None = Field(default=None, max_length=2048)
    title: str | None = Field(default=None, max_length=512)
    description: str | None = Field(default=None, max_length=10000)
    asking_price: str | None = Field(default=None, pattern=r"^(0|[1-9][0-9]{0,15})(\.[0-9]{1,2})?$")
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")

    @field_validator("source_type", "source_url", "title", "description")
    @classmethod
    def no_nulls(cls, value: str | None) -> str | None:
        if value is not None and "\x00" in value:
            raise ValueError("invalid_text")
        return value

    @field_validator("source_url")
    @classmethod
    def inert_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if any(c.isspace() or c == "\\" or ord(c) < 32 or ord(c) == 127 for c in value):
            raise ValueError("invalid_source_url")
        parsed = urlsplit(value)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            raise ValueError("invalid_source_url")
        return value

    def price(self) -> Decimal | None:
        return Decimal(self.asking_price) if self.asking_price is not None else None


class ListingResponse(ListingCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class ListingPage(ListingModel):
    items: list[ListingResponse]
    next_offset: int | None


class ListingImage(ListingModel):
    listing_image_id: UUID
    original_asset_id: UUID
    thumbnail_asset_id: UUID
    display_order: int


class ListingDetail(ListingResponse):
    images: list[ListingImage]
    next_display_order: int


class UploadArguments(ListingModel):
    client_upload_id: UUID
    display_order: int = Field(ge=0, le=2147483646)
    privacy_elevation: Literal["restricted"] | None = None


class UploadBody(UploadArguments):
    file: bytes = Field(json_schema_extra={"format": "binary"})


class UploadProblem(ListingModel):
    code: str
    message: str


class ListingProblem(ListingModel):
    error: UploadProblem


class UploadResult(ListingModel):
    client_upload_id: UUID
    filename: str
    status: Literal["uploaded", "duplicate", "failed"]
    listing_image_id: UUID | None
    error: UploadProblem | None
