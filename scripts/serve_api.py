"""API-only launcher. Only runtime credentials cross into the serving process."""

import os
import sys

from brickvault_api.main import serve
from database import load_config, require_free_port


def main() -> None:
    configured = load_config()
    require_free_port(8000)
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("BVA_")
    }
    environment.update(
        {
            "BVA_MODE": "development",
            "BVA_BIND_HOST": "127.0.0.1",
            "BVA_API_PORT": "8000",
            "BVA_RUNTIME_DATABASE_URL": configured["BVA_DEV_RUNTIME_DATABASE_URL"],
            "BVA_LOG_LEVEL": configured["BVA_LOG_LEVEL"],
        }
    )
    # Keep the serving PID owned by this launcher on Windows as well as POSIX.
    # Windows execve emulation would detach a new process from the parent's handle.
    del configured
    os.environ.clear()
    os.environ.update(environment)
    serve()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(
            "API startup failed; check the private local configuration and port availability.",
            file=sys.stderr,
        )
        sys.exit(1)
