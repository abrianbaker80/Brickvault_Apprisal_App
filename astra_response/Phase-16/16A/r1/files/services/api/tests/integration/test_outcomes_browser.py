"""One outcomes UI/API flow with owned PostgreSQL and an isolated browser build."""

import json
import os
import socket
import subprocess
from pathlib import Path
from threading import Event, Thread

import pytest
import uvicorn
from pydantic import SecretStr

from brickvault_api.api.forecasts import forecast_service
from brickvault_api.auth import AuthService
from brickvault_api.main import create_app
from brickvault_api.settings import RuntimeSettings

from .test_forecasts import ForecastHarness
from .test_forecasts import forecasts as forecasts
from .test_forecasts import market as market
from .test_forecasts import no_provider_network as no_provider_network
from .test_forecasts import owner_engine as owner_engine
from .test_forecasts import synthetic as synthetic
from .test_product import forbid_market_actions


def test_outcomes_one_real_browser_flow(
    forecasts: ForecastHarness,
    monkeypatch: pytest.MonkeyPatch,
    no_provider_network: None,
) -> None:
    h = forecasts
    root = Path(__file__).resolve().parents[4]
    output = root / ".local/phase16a-chatgpt"
    h.market.lookup()
    h.market.fetch()
    original = h.save(h.preview().status.id)
    child = h.save(h.service.preview_revision(h.token, h.csrf, original.id, h.request()).status.id)
    before = (h.row(original.id), h.row(child.id))
    forbid_market_actions(monkeypatch)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    settings = RuntimeSettings(
        purpose="test",
        port=port,
        auth_allow_loopback_http=True,
        static_enabled=True,
        web_build_dir=str(output / "web-dist"),
        database_url=SecretStr(h.market.app.database.url),
        database_ownership_marker=SecretStr(h.market.app.database.ownership_marker),
    )
    app = create_app(settings)
    app.dependency_overrides[forecast_service] = lambda: h.service
    ready = Event()
    server = uvicorn.Server(uvicorn.Config(app, access_log=False, log_config=None))
    startup = server.startup

    async def start(sockets: list[socket.socket] | None = None) -> None:
        await startup(sockets)
        app.state.auth = AuthService(h.market.app.database, clock=h.market.clock)
        ready.set()

    monkeypatch.setattr(server, "startup", start)
    thread = Thread(target=lambda: server.run(sockets=[listener]), daemon=True)
    thread.start()
    try:
        assert ready.wait(20), "Owned TEST API did not start"
        allow = {
            "PATH",
            "SYSTEMROOT",
            "WINDIR",
            "TEMP",
            "TMP",
            "USERPROFILE",
            "LOCALAPPDATA",
            "APPDATA",
        }
        env = {name: value for name, value in os.environ.items() if name.upper() in allow}
        env.update(
            {
                "BVA_E2E_API_URL": f"http://127.0.0.1:{port}",
                "BVA_E2E_PASSWORD": h.password,
                "BVA_TEST_TIME": h.market.clock().isoformat(),
                "BVA_OUTCOME_ROOT": str(original.id),
                "BVA_OUTCOME_CHILD": str(child.id),
            }
        )
        result = subprocess.run(
            ["node", str(root / "apps/web/e2e/outcomes-real.mjs")],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=150,
        )
        assert result.returncode == 0, result.stderr
        report = json.loads(result.stdout)
        assert report["outcome_revisions"] == 2
        assert report["desktop_and_320px"] and report["history_preserved"]
        assert before == (h.row(original.id), h.row(child.id))
        with h.market.owner.database.connect() as c:
            rows = c.execute(
                "SELECT revision,results FROM deal_outcome_revision WHERE root_forecast_id=%s ORDER BY revision",
                (original.id,),
            ).fetchall()
        assert [(row["revision"], row["results"]["profit"]["amount"]) for row in rows] == [
            (1, "47.00"),
            (2, "57.00"),
        ]
        report["frozen_original_and_revision_rows_unchanged"] = True
        report["real_database_history_verified"] = True
    finally:
        server.should_exit = True
        thread.join(timeout=15)
        listener.close()
        assert not thread.is_alive(), "Owned TEST API did not stop"
    report["owned_api_stopped"] = True
    (output / "browser-result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
