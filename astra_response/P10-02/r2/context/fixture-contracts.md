# Unchanged fixture excerpts

These verbatim excerpts show the setup paths reused by `recovery_proof.py`.
Line numbers refer to the implementation baseline and final unchanged source.

## `scripts/integration_runner.py:34-88`

```python
class IntegrationFixtures:
    def __init__(self, instance: Instance, database: str, run_id: str) -> None:
        self.instance = instance
        self.database = database
        self.run_id = run_id

    @pytest.fixture
    def owned_instance(self) -> Instance:
        return self.instance

    @pytest.fixture
    def disposable_database(self) -> str:
        return self.database

    @pytest.fixture
    def integration_run_id(self) -> str:
        return self.run_id

    @pytest.fixture
    def test_settings(self) -> RuntimeSettings:
        return RuntimeSettings(
            purpose="test",
            database_url=SecretStr(self.instance.target(self.database, "runtime")),
            port=18000,
            auth_allow_loopback_http=True,
            database_ownership_marker=SecretStr(
                database_marker(self.instance, self.run_id)
            ),
        )

    @pytest.fixture
    def owner_engine(self) -> Iterator[Engine]:
        engine = create_database_engine(
            self.instance.target(self.database, "owner"), "test", "owner"
        )
        try:
            yield engine
        finally:
            engine.dispose()

    @pytest.fixture
    def runtime_engine(self) -> Iterator[Engine]:
        engine = create_database_engine(
            self.instance.target(self.database, "runtime"), "test"
        )
        try:
            yield engine
        finally:
            engine.dispose()


def smoke_api(
    instance: Instance, database: str, record: dict[str, Any], journal: Path
) -> None:
    settings = RuntimeSettings(
```

## `services/api/tests/integration/test_catalog_schema.py:122-139`

```python
def synthetic(owner_engine: Engine, request: pytest.FixtureRequest) -> Iterator[Synthetic]:
    data = json.loads(
        (Path(__file__).parents[1] / "fixtures/catalog/synthetic/relational.json").read_text()
    )
    assert data["synthetic"] is True
    hunt_capacity = request.node.get_closest_marker("hunt_capacity") is not None
    capacity_numbers = [f"90000-{index}-1" for index in range(1, 17)] if hunt_capacity else []
    data["sets"].extend(capacity_numbers)
    now = datetime(2026, 9, 7, tzinfo=UTC)
    with owner_engine.connect() as connection:
        transaction = connection.begin()
        fixture = Synthetic(connection)
        add = fixture.insert
        add(
            "catalog_provider",
            id=key("provider"),
            code="synthetic",
            name="Synthetic only",
```

## `services/api/tests/integration/test_catalog_schema.py:457-465`

```python
            source_relation_code="P",
            normalized_meaning="print",
        )
        try:
            yield fixture
        finally:
            if transaction.is_active:
                transaction.rollback()
            else:
```

## `services/api/tests/integration/test_catalog_queries.py:75-85`

```python
def accept(data: Synthetic) -> None:
    # This fixture is explicitly authored physical evidence, distinct from the
    # LIVE-UNVERIFIED bulk profile. Freeze it before testing read-only queries.
    data.connection.execute(
        text("UPDATE catalog_snapshot SET state='validated',validation_digest=:digest"),
        {"digest": "2" * 64},
    )
    data.connection.execute(text("UPDATE catalog_snapshot SET state='accepted'"))
    data.connection.commit()


```

## `services/api/tests/integration/test_market.py:92-129`

```python
def market(
    synthetic: Synthetic, catalog_db: CatalogDatabase, owned_instance: Instance
) -> Iterator[Harness]:
    accept(synthetic)
    clock = Clock()
    owner = MarketRepository(catalog_db, clock=clock)
    app = MarketRepository(runtime(catalog_db, owned_instance), clock=clock)
    policy = MarketPolicy(created_at=clock(), effective_at=clock())
    scope = uuid4()
    owner.install_policy(policy, uuid4(), scope)
    mapping = MappingRevision(
        item_type="SET",
        item_no="80000-1",
        set_id=key("set"),
        snapshot_id=key("snapshot"),
        source_version_id=key("source"),
        evidence_id=key("evidence"),
        method="exact_item",
        evidence_reference="synthetic-review-1",
        reviewer="fixture",
        created_at=clock(),
        reviewed_at=clock(),
    )
    owner.review_mapping(mapping)
    yield Harness(
        owner,
        app,
        clock,
        mapping,
        policy,
        scope,
        Request(Operation.PRICE, uuid4(), ItemType.SET, "80000-1"),
    )


def test_schema_and_policy_immutable(market: Harness) -> None:
    with market.owner.database.connect() as c:
        tables = {
```

## `services/api/tests/integration/test_forecasts.py:65-99`

```python
    def login(self) -> None:
        self.token, self.csrf, _ = AuthService(
            self.market.app.database, clock=self.market.clock
        ).login(self.password, None)

    def request(self) -> DealRequest:
        appraisal = ProductService(
            self.market.app.database, clock=self.market.clock, snapshot_id=key("snapshot")
        ).appraisal("80000-1")
        view = next(v for v in appraisal.views if v.condition == "N" and v.basis == "sold")
        whole = next(s for s in view.strategies if s.strategy == "COMPLETE_SET")
        return DealRequest.model_validate(
            {
                "condition": "N",
                "basis": "sold",
                "basis_revision": whole.deal_basis_revision,
                "sale_basis": "MANUAL",
                "manual_sale_price": "180.05",
                "purchase_price": "100",
                "shipping_charged": "10",
                "selling_fees": "10",
                "shipping_paid": "0",
                "other_selling_costs": "0",
                "acquisition_costs": "0",
            }
        )

    def preview(self) -> Any:
        return self.service.preview(self.token, self.csrf, "80000-1", self.request())

    def save(self, handle: UUID) -> Any:
        return self.service.save(self.token, self.csrf, handle)

    def row(self, handle: UUID) -> Any:
        with self.market.owner.database.connect() as c:
```

## `services/api/tests/integration/test_forecasts.py:103-119`

```python
@pytest.fixture
def forecasts(market: Harness) -> ForecastHarness:
    password = secrets.token_urlsafe(32)
    owner = AuthService(market.owner.database, clock=market.clock).provision(password)
    harness = ForecastHarness(
        market,
        ForecastService(market.app.database, snapshot_id=key("snapshot")),
        password,
        "",
        "",
        owner,
    )
    harness.advance()
    harness.login()
    return harness


```
