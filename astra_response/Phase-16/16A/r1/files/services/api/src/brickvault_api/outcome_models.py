"""Strict, versioned actual outcomes; no client-supplied calculations or owner IDs."""

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from brickvault_api.economics_v1 import DealModel, MoneyInput, signed_money

MONEY_FIELDS = (
    "purchase_price",
    "acquisition_extra_costs",
    "replacement_costs",
    "labor_costs",
    "item_sale_proceeds",
    "shipping_charged",
    "selling_fees",
    "shipping_paid",
    "other_selling_costs",
)


class OutcomeActuals(DealModel):
    purchase_decision: Literal["BOUGHT", "NOT_BOUGHT"]
    currency: Literal["USD"] = "USD"
    acquired_on: date | None = None
    purchase_price: MoneyInput | None = None
    acquisition_extra_costs: MoneyInput | None = None
    contents_state: Literal["NOT_CHECKED", "CONFIRMED_MATCH", "CONFIRMED_DIFFERENT"] = "NOT_CHECKED"
    contents_checked_on: date | None = None
    contents_note: Annotated[str, Field(max_length=1000)] | None = None
    forecast_preceded_purchase: Annotated[bool, Field(strict=True)] | None = None
    replacement_costs: MoneyInput | None = None
    labor_minutes: Annotated[int, Field(strict=True, ge=0, le=2_147_483_647)] | None = None
    labor_costs: MoneyInput | None = None
    sale_status: Literal["NOT_SOLD", "PARTIALLY_SOLD", "COMPLETE"] | None = None
    sale_strategy: Literal["COMPLETE_SET", "OTHER"] | None = None
    sale_condition: Literal["N", "U", "UNKNOWN"] | None = None
    sale_channel: Annotated[str, Field(max_length=80)] | None = None
    sold_on: date | None = None
    item_sale_proceeds: MoneyInput | None = None
    shipping_charged: MoneyInput | None = None
    selling_fees: MoneyInput | None = None
    shipping_paid: MoneyInput | None = None
    other_selling_costs: MoneyInput | None = None

    @field_validator(*MONEY_FIELDS)
    @classmethod
    def canonical_money(cls, value: str | None) -> str | None:
        return signed_money(Decimal(value)) if value is not None else None

    @field_validator("contents_note", "sale_channel")
    @classmethod
    def optional_text(cls, value: str | None) -> str | None:
        return value.strip() or None if value is not None else None

    @field_validator("acquired_on", "contents_checked_on", "sold_on", mode="before")
    @classmethod
    def calendar_date(cls, value: object) -> object:
        if value is None or (isinstance(value, date) and not isinstance(value, datetime)):
            return value
        if not isinstance(value, str):
            raise ValueError("calendar_date_required")
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            raise ValueError("calendar_date_required") from None
        if parsed.isoformat() != value:
            raise ValueError("calendar_date_required")
        return parsed

    @model_validator(mode="after")
    def coherent(self) -> "OutcomeActuals":
        if self.purchase_decision == "NOT_BOUGHT":
            allowed = {"purchase_decision", "currency", "contents_state"}
            if self.contents_state != "NOT_CHECKED" or any(
                value is not None for key, value in self.model_dump().items() if key not in allowed
            ):
                raise ValueError("not_bought_requires_null_transaction_fields")
            return self
        if self.sale_status is None:
            raise ValueError("bought_requires_sale_status")
        if self.contents_state != "NOT_CHECKED" and self.contents_checked_on is None:
            raise ValueError("confirmed_contents_require_date")
        if self.contents_state == "CONFIRMED_DIFFERENT" and not self.contents_note:
            raise ValueError("different_contents_require_note")
        if self.sale_status == "NOT_SOLD" and (
            self.item_sale_proceeds is not None or self.shipping_charged is not None
        ):
            raise ValueError("not_sold_cannot_have_sale_receipts")
        if self.sold_on is not None and self.sale_status != "COMPLETE":
            raise ValueError("final_sale_date_requires_complete_sale")
        if self.acquired_on is not None and self.sold_on is not None:
            if self.sold_on < self.acquired_on:
                raise ValueError("sale_precedes_acquisition")
        return self


class OutcomeAppend(DealModel):
    id: UUID
    expected_revision: Annotated[int, Field(strict=True, ge=0, le=2_147_483_646)]
    actuals: OutcomeActuals
    correction_reason: Annotated[str, Field(max_length=500)] | None = None

    @field_validator("correction_reason")
    @classmethod
    def reason(cls, value: str | None) -> str | None:
        return value.strip() or None if value is not None else None

    @model_validator(mode="after")
    def correction(self) -> "OutcomeAppend":
        if self.expected_revision > 0 and self.correction_reason is None:
            raise ValueError("correction_reason_required")
        return self


class OutcomeAmount(DealModel):
    amount: str | None = None
    reasons: tuple[str, ...] = ()


class OutcomeComparisonMetric(DealModel):
    state: Literal["COMPARABLE", "NONCOMPARABLE", "UNAVAILABLE"]
    actual_amount: str | None
    expected_amount: str | None
    error_amount: str | None = None
    error_exact: str | None = None
    reasons: tuple[str, ...] = ()


class OutcomeComparison(DealModel):
    original_id: UUID
    original_digest: str | None = None
    original_created_at: datetime
    set_number: str | None = None
    basis: Literal["sold", "stock"] | None = None
    sale_basis: Literal["SELECTED_MARKET", "MANUAL"] | None = None
    meaning: Literal["FORECAST_COMPARISON", "ASSUMPTION_COMPARISON", "UNAVAILABLE"]
    original_acquisition: str | None = None
    actual_acquisition: str | None = None
    sale: OutcomeComparisonMetric
    net: OutcomeComparisonMetric
    profit: OutcomeComparisonMetric


class OutcomeResults(DealModel):
    calculation_version: Literal["outcome-calculation-v1"] = "outcome-calculation-v1"
    rounding_version: Literal["whole-set-usd-rounding-v1"] = "whole-set-usd-rounding-v1"
    currency: Literal["USD"] = "USD"
    state: Literal["NOT_BOUGHT", "NOT_SOLD", "PARTIALLY_SOLD", "INCOMPLETE", "COMPLETE"]
    missing_fields: tuple[str, ...] = ()
    gross: OutcomeAmount
    selling_costs: OutcomeAmount
    net: OutcomeAmount
    acquisition: OutcomeAmount
    profit: OutcomeAmount
    days_to_sell: int | None
    duration_reasons: tuple[str, ...] = ()
    unpaid_own_labor_excluded: Literal[True] = True
    comparison: OutcomeComparison


class OutcomeEntry(DealModel):
    id: UUID
    root_forecast_id: UUID
    revision: int
    recorded_at: datetime
    correction_reason: str | None
    actuals: OutcomeActuals
    results: OutcomeResults


class OutcomeHistoryItem(DealModel):
    id: UUID
    revision: int
    recorded_at: datetime
    correction_reason: str | None
    purchase_decision: Literal["BOUGHT", "NOT_BOUGHT"]
    sale_status: Literal["NOT_SOLD", "PARTIALLY_SOLD", "COMPLETE"] | None


class OutcomeResponse(DealModel):
    root_forecast_id: UUID
    state: Literal["NOT_RECORDED", "RECORDED"]
    latest: OutcomeEntry | None
    history: tuple[OutcomeHistoryItem, ...]
    next_before_revision: int | None


OutcomeErrorCode = Literal[
    "OUTCOME_NOT_FOUND",
    "OUTCOME_CONFLICT",
    "OUTCOME_ID_REUSED",
    "OUTCOME_UNAVAILABLE",
    "OUTCOME_INVALID_CHRONOLOGY",
]


class OutcomeProblemDetail(DealModel):
    code: OutcomeErrorCode
    message: str
    request_id: UUID


class OutcomeProblem(DealModel):
    error: OutcomeProblemDetail
