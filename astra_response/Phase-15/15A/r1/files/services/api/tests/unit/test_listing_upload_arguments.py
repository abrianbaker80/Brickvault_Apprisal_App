"""Strict multipart admission keeps privacy elevation separate from upload identity."""

import io
import json
from uuid import uuid4

import pytest
from pydantic import ValidationError
from starlette.datastructures import FormData, UploadFile

from brickvault_api.api.listings import upload_arguments
from brickvault_api.contracts import export
from brickvault_api.images.storage import ImageError
from brickvault_api.listings.models import UploadArguments


def parts() -> list[tuple[str, str | UploadFile]]:
    return [
        ("file", UploadFile(io.BytesIO(b"synthetic"), filename="image.png")),
        ("client_upload_id", str(uuid4())),
        ("display_order", "0"),
    ]


@pytest.mark.parametrize("elevation", [None, "restricted"])
def test_optional_restricted_elevation_preserves_existing_arguments(elevation: str | None) -> None:
    fields = parts()
    if elevation is not None:
        fields.append(("privacy_elevation", elevation))
    file, arguments = upload_arguments(FormData(fields))
    assert file is fields[0][1]
    assert str(arguments.client_upload_id) == fields[1][1]
    assert arguments.display_order == 0
    assert arguments.privacy_elevation == elevation


@pytest.mark.parametrize("value", ["private", "", "null", "Restricted", " restricted"])
def test_privacy_elevation_never_accepts_downgrade_or_unknown_values(value: str) -> None:
    with pytest.raises(ImageError, match="INVALID_PRIVACY_ELEVATION"):
        upload_arguments(FormData([*parts(), ("privacy_elevation", value)]))


@pytest.mark.parametrize("name", ["file", "client_upload_id", "display_order", "privacy_elevation"])
def test_duplicate_fields_are_rejected_even_when_identical(name: str) -> None:
    fields = [*parts(), ("privacy_elevation", "restricted")]
    duplicate = next(part for part in fields if part[0] == name)
    with pytest.raises(ImageError, match="INVALID_MULTIPART"):
        upload_arguments(FormData([*fields, duplicate]))


def test_extra_missing_and_file_valued_elevation_are_rejected() -> None:
    fields = parts()
    for malformed in ([*fields, ("unknown", "restricted")], fields[:-1]):
        with pytest.raises(ImageError, match="INVALID_MULTIPART"):
            upload_arguments(FormData(malformed))
    with pytest.raises(ImageError, match="INVALID_PRIVACY_ELEVATION"):
        upload_arguments(FormData([*fields, ("privacy_elevation", fields[0][1])]))


def test_model_and_export_admit_only_optional_restricted_value() -> None:
    with pytest.raises(ValidationError):
        UploadArguments.model_validate(
            {"client_upload_id": uuid4(), "display_order": 0, "privacy_elevation": "private"}
        )
    schema = json.loads(export())["paths"]["/api/listings/{listing_id}/images"]["post"][
        "requestBody"
    ]["content"]["multipart/form-data"]["schema"]
    assert "privacy_elevation" not in schema["required"]
    assert schema["properties"]["privacy_elevation"]["anyOf"] == [
        {"const": "restricted", "type": "string"},
        {"type": "null"},
    ]
    assert schema["additionalProperties"] is False
