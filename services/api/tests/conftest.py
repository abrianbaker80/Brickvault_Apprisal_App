import sys
from pathlib import Path

import pytest
from brickvault_api.settings import RuntimeSettings
from pydantic import SecretStr

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))


@pytest.fixture
def runtime_settings() -> RuntimeSettings:
    return RuntimeSettings(
        purpose="development",
        database_url=SecretStr(
            "postgresql+psycopg://brickvault_dev_runtime:"
            + "a" * 64
            + "@127.0.0.1:55432/brickvault_dev"
        ),
    )
