"""Decode bounded single-frame images and derive metadata-free thumbnail-v1."""

import io
import warnings
from dataclasses import dataclass
from typing import Any

import PIL
from PIL import Image, ImageOps, UnidentifiedImageError

from brickvault_api.images.storage import ImageError

MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_REQUEST_BYTES = 26 * 1024 * 1024
RECIPE = "thumbnail-v1"


@dataclass(frozen=True)
class ProcessedImage:
    format: str
    width: int
    height: int
    thumbnail: bytes
    thumbnail_width: int
    thumbnail_height: int
    metadata: dict[str, Any]


def process_image(data: bytes) -> ProcessedImage:
    if len(data) > MAX_FILE_BYTES:
        raise ImageError("IMAGE_FILE_TOO_LARGE", 413)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as source:
                format_name = source.format
                if format_name not in ("JPEG", "PNG", "WEBP"):
                    raise ImageError("UNSUPPORTED_IMAGE_FORMAT")
                width, height = source.size
                if width > 16000 or height > 16000 or width * height > 40000000:
                    raise ImageError("IMAGE_DIMENSIONS_EXCEEDED")
                if getattr(source, "n_frames", 1) != 1 or getattr(source, "is_animated", False):
                    raise ImageError("ANIMATED_IMAGE")
                source.verify()
            with Image.open(io.BytesIO(data)) as decoded:
                decoded.load()
                oriented = ImageOps.exif_transpose(decoded)
                oriented.thumbnail((512, 512), Image.Resampling.LANCZOS)
                rgba = oriented.convert("RGBA")
                rgb = Image.new("RGB", rgba.size, "white")
                rgb.paste(rgba, mask=rgba.getchannel("A"))
                output = io.BytesIO()
                rgb.save(output, format="JPEG", quality=85)
                return ProcessedImage(
                    format_name,
                    width,
                    height,
                    output.getvalue(),
                    *rgb.size,
                    {
                        "recipe": RECIPE,
                        "decoder": "Pillow",
                        "decoder_version": PIL.__version__,
                        "exif_orientation": True,
                        "fit": [512, 512],
                        "enlarge": False,
                        "mode": "RGB",
                        "background": "white",
                        "format": "JPEG",
                        "quality": 85,
                        "source_metadata": False,
                    },
                )
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ImageError("IMAGE_DECOMPRESSION_BOMB") from None
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError) as error:
        if isinstance(error, ImageError):
            raise
        raise ImageError("INVALID_IMAGE") from None
