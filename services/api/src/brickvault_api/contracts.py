"""Credential-free schema export; never enters the application's lifespan."""

import sys

from brickvault_api.main import create_app, schema_bytes


def export() -> bytes:
    return schema_bytes(create_app())


if __name__ == "__main__":
    sys.stdout.buffer.write(export())
