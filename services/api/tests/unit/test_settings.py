import os

import pytest
from brickvault_api.persistence import database
from brickvault_api.settings import ConfigurationError, RuntimeSettings, validate_target

GOOD = "postgresql+psycopg://brickvault_dev_runtime:" + "a" * 64 + "@127.0.0.1:55432/brickvault_dev"


@pytest.mark.parametrize(
    "value",
    [
        GOOD.replace("55432", "5432"),
        GOOD.replace("55432", "55433"),
        GOOD.replace("127.0.0.1", "localhost"),
        GOOD.replace("127.0.0.1", "remote.invalid"),
        GOOD.replace("127.0.0.1", "127.0.0.\t1"),
        GOOD + " ",
        GOOD + "?host=remote.invalid",
        GOOD + "?options=-c%20search_path=x",
        GOOD + "#fragment",
        GOOD.replace("/brickvault_dev", "/postgres"),
        GOOD.replace("/brickvault_dev", "/brickvault_test_" + "a" * 32),
        GOOD.replace("runtime", "owner"),
        GOOD.replace("127.0.0.1", "[::1]"),
        GOOD.replace("127.0.0.1", "2130706433"),
        GOOD.replace("55432", "055432"),
        GOOD.replace("postgresql+psycopg", "postgresql"),
        GOOD.replace("127.0.0.1", "%31%32%37.0.0.1"),
        "\n" + GOOD,
    ],
)
def test_target_rejected_before_engine_or_connection(
    value: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("Forbidden target reached engine construction")

    monkeypatch.setattr(database, "create_engine", forbidden)
    with pytest.raises(ConfigurationError) as caught:
        database.create_database_engine(value, "development")
    assert value not in str(caught.value)


@pytest.mark.parametrize(
    "key",
    [
        "PGHOST",
        "PGHOSTADDR",
        "PGPORT",
        "PGDATABASE",
        "PGSERVICE",
        "PGSERVICEFILE",
        "PGOPTIONS",
        "PGPASSFILE",
    ],
)
def test_inherited_libpq_overrides_rejected(key: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(key, "secret-sentinel")
    with pytest.raises(ConfigurationError):
        validate_target(GOOD, "development", "runtime")


def test_runtime_startup_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in list(os.environ):
        if key.startswith(("BVA_", "PG")):
            monkeypatch.delenv(key)
    with pytest.raises(ConfigurationError):
        RuntimeSettings.from_environment()
    monkeypatch.setenv("BVA_RUNTIME_DATABASE_URL", GOOD)
    assert RuntimeSettings.from_environment().target().port == 55432
    for key, value in [
        ("BVA_BIND_HOST", "0.0.0.0"),
        ("BVA_API_PORT", "08000"),
        ("BVA_UNKNOWN", "secret-sentinel"),
    ]:
        monkeypatch.setenv(key, value)
        with pytest.raises(ConfigurationError) as caught:
            RuntimeSettings.from_environment()
        assert "secret-sentinel" not in str(caught.value)
        monkeypatch.delenv(key)


def test_test_template_is_never_a_connection_target() -> None:
    template = (
        GOOD.replace("dev_", "test_")
        .replace("55432", "55433")
        .replace("/brickvault_dev", "/brickvault_test")
    )
    assert (
        validate_target(template, "test", "runtime", config_template=True).database
        == "brickvault_test"
    )
    with pytest.raises(ConfigurationError):
        validate_target(template, "test", "runtime")
    with pytest.raises(ConfigurationError):
        validate_target(GOOD, "test", "runtime")
