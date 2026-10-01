"""Conditional filesystem publication of complete SHA-256 addressed objects."""

import hashlib
import os
import re
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Protocol


class ImageError(ValueError):
    def __init__(self, code: str, status: int = 422) -> None:
        self.code, self.status = code, status
        super().__init__(code)


def key_for(digest: str) -> str:
    if re.fullmatch(r"[a-f0-9]{64}", digest) is None:
        raise ImageError("INVALID_BLOB_HASH")
    return f"sha256/{digest[:2]}/{digest[2:4]}/{digest}"


@dataclass(frozen=True)
class StoredBlob:
    sha256: str
    key: str
    byte_count: int


class BlobStore(Protocol):
    def publish(self, data: bytes) -> StoredBlob: ...
    def read(self, digest: str) -> BinaryIO: ...
    def stat(self, digest: str) -> StoredBlob: ...
    def enumerate(self) -> Iterator[str]: ...


class FilesystemBlobStore:
    def __init__(self, root: Path, *, forbidden_roots: tuple[Path, ...] = ()) -> None:
        if not root.is_absolute():
            raise ImageError("UNSAFE_BLOB_ROOT", 503)
        self.root = root.resolve()
        if any(self.root.is_relative_to(p.resolve()) for p in forbidden_roots):
            raise ImageError("UNSAFE_BLOB_ROOT", 503)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)

    def _path(self, digest: str) -> Path:
        path = self.root / key_for(digest)
        if any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(self.root)):
            raise ImageError("UNSAFE_BLOB_OBJECT", 503)
        return path

    def publish(self, data: bytes) -> StoredBlob:
        if not data:
            raise ImageError("EMPTY_IMAGE")
        digest = hashlib.sha256(data).hexdigest()
        destination = self._path(digest)
        expected = StoredBlob(digest, key_for(digest), len(data))
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=destination.parent, prefix=".stage-", delete=False
            ) as f:
                temporary = f.name
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            try:
                # Hard-link publication is atomic and fails if the destination exists.
                # Windows NTFS and Linux local filesystems implement this primitive.
                os.link(temporary, destination)
            except FileExistsError:
                if self.stat(digest) != expected:
                    raise ImageError("BLOB_CORRUPT", 503) from None
            if os.name == "posix":
                descriptor = os.open(destination.parent, os.O_RDONLY)
                try:
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
            return expected
        except OSError:
            raise ImageError("BLOB_STORAGE_UNAVAILABLE", 503) from None
        finally:
            if temporary is not None:
                Path(temporary).unlink(missing_ok=True)

    def read(self, digest: str) -> BinaryIO:
        try:
            return self._path(digest).open("rb")
        except OSError:
            raise ImageError("BLOB_MISSING", 503) from None

    def stat(self, digest: str) -> StoredBlob:
        with self.read(digest) as f:
            size = 0
            hashed = hashlib.sha256()
            while block := f.read(1024 * 1024):
                size += len(block)
                hashed.update(block)
        if hashed.hexdigest() != digest:
            raise ImageError("BLOB_CORRUPT", 503)
        return StoredBlob(digest, key_for(digest), size)

    def enumerate(self) -> Iterator[str]:
        for directory, _, names in os.walk(self.root, followlinks=False):
            for name in names:
                yield (Path(directory) / name).relative_to(self.root).as_posix()
