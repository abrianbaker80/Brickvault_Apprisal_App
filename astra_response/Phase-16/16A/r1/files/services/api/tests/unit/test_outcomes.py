"""Focused actual-outcome arithmetic and strict comparison, using existing frozen fixtures."""

from dataclasses import replace
from datetime import UTC, datetime
from decimal import ROUND_DOWN, Inexact, localcontext
from typing import Any
from uuid import uuid4

import pytest
from pydantic import ValidationError

from brickvault_api.economics_snapshot import encode, replay
from brickvault_api.outcome_calculation import (
    OutcomeBaseline,
    OutcomeChronologyError,
    calculate_outcome,
)
from brickvault_api.outcome_models import OutcomeActuals, OutcomeAppend
from brickvault_api.providers.bricklink.requests import Basis

from .test_economics_snapshot import original


def actual(**changes: Any) -> OutcomeActuals:
    return OutcomeActuals.model_validate(
        {
            "purchase_decision": "BOUGHT",
            "acquired_on": "2026-10-01",
            "purchase_price": "80",
            "acquisition_extra_costs": "0",
            "contents_state": "CONFIRMED_MATCH",
            "contents_checked_on": "2026-10-01",
            "forecast_preceded_purchase": True,
            "replacement_costs": "0",
            "labor_minutes": 90,
            "labor_costs": "0",
            "sale_status": "COMPLETE",
            "sale_strategy": "COMPLETE_SET",
            "sale_condition": "N",
            "sale_channel": "Synthetic channel",
            "sold_on": "2026-10-11",
            "item_sale_proceeds": "180.05",
            "shipping_charged": "10",
            "selling_fees": "18",
            "shipping_paid": "8",
            "other_selling_costs": "2",
            **changes,
        }
    )


def baseline(**changes: Any) -> OutcomeBaseline:
    snapshot = original(
        limits=False,
        purchase_price="80",
        acquisition_costs="0",
        shipping_charged="10",
        shipping_paid="8",
        other_selling_costs="2",
        selling_fees="18",
        **changes,
    )
    return OutcomeBaseline(uuid4(), snapshot.accepted_at, snapshot, replay(snapshot))


def test_exact_cash_and_forecast_errors_without_changing_original() -> None:
    b = baseline()
    assert b.snapshot is not None
    before = encode(b.snapshot)
    result = calculate_outcome(actual(), b)
    assert result.state == "COMPLETE"
    assert (
        result.gross.amount,
        result.selling_costs.amount,
        result.net.amount,
        result.acquisition.amount,
        result.profit.amount,
        result.days_to_sell,
    ) == (
        "190.05",
        "28.00",
        "162.05",
        "80.00",
        "82.05",
        10,
    )
    assert result.unpaid_own_labor_excluded is True
    for metric in (result.comparison.sale, result.comparison.net, result.comparison.profit):
        assert metric.state == "COMPARABLE"
        assert metric.error_exact == "0.001" and metric.error_amount == "0.00"
    assert result.comparison.original_id == b.original_id
    assert encode(b.snapshot) == before


def test_unknown_zero_labor_and_partial_sale_are_distinct() -> None:
    b = baseline()
    unknown = calculate_outcome(actual(shipping_paid=None), b)
    assert unknown.gross.amount == "190.05"
    assert unknown.net.amount is unknown.profit.amount is None
    assert unknown.state == "INCOMPLETE" and "shipping_paid" in unknown.net.reasons
    zero = calculate_outcome(actual(shipping_paid="0", labor_costs="5", replacement_costs="7"), b)
    assert zero.net.amount == "158.05"  # 190.05 - (18+0+2+5+7), no time-to-money conversion.
    partial = calculate_outcome(actual(sale_status="PARTIALLY_SOLD", sold_on=None), b)
    assert partial.state == "PARTIALLY_SOLD" and partial.net.amount == "162.05"
    assert partial.profit.amount is partial.days_to_sell is None
    assert partial.comparison.sale.state == "NONCOMPARABLE"
    assert "SALE_NOT_COMPLETE" in partial.comparison.sale.reasons


def test_negative_profit_zero_acquisition_and_missing_dates() -> None:
    b = baseline()
    negative = calculate_outcome(actual(item_sale_proceeds="0", shipping_charged="0"), b)
    assert negative.net.amount == "-28.00" and negative.profit.amount == "-108.00"
    free = calculate_outcome(actual(purchase_price="0"), b)
    assert free.profit.amount == "162.05"
    dates = calculate_outcome(actual(acquired_on=None, sold_on=None, sale_channel=None), b)
    assert dates.profit.amount == "82.05" and dates.days_to_sell is None
    assert dates.state == "INCOMPLETE"


@pytest.mark.parametrize(
    "changes,reason",
    [
        ({"sale_strategy": "OTHER"}, "STRATEGY_UNVERIFIED_OR_CHANGED"),
        ({"sale_condition": "U"}, "CONDITION_UNVERIFIED_OR_CHANGED"),
        (
            {"contents_state": "CONFIRMED_DIFFERENT", "contents_note": "Missing piece"},
            "CONTENTS_UNVERIFIED_OR_CHANGED",
        ),
        ({"forecast_preceded_purchase": None}, "FORECAST_NOT_CONFIRMED_BEFORE_PURCHASE"),
    ],
)
def test_comparison_scope_mismatch_does_not_suppress_actuals(
    changes: dict[str, Any], reason: str
) -> None:
    result = calculate_outcome(actual(**changes), baseline())
    assert result.profit.amount == "82.05"
    assert result.comparison.sale.state == "NONCOMPARABLE"
    assert reason in result.comparison.sale.reasons
    assert result.comparison.sale.error_amount is None


def test_acquisition_change_manual_assumption_and_stock_baseline() -> None:
    changed = calculate_outcome(actual(purchase_price="81"), baseline())
    assert changed.comparison.sale.state == changed.comparison.net.state == "COMPARABLE"
    assert changed.comparison.profit.state == "NONCOMPARABLE"
    assert changed.comparison.profit.reasons == ("ACQUISITION_BASIS_CHANGED",)
    assert changed.comparison.original_acquisition == "80"
    assert changed.comparison.actual_acquisition == "81.00"
    manual = calculate_outcome(actual(), baseline(sale_basis="MANUAL", manual_sale_price="180.05"))
    assert manual.comparison.meaning == "ASSUMPTION_COMPARISON"
    stock = calculate_outcome(actual(), baseline(basis=Basis.STOCK))
    assert stock.comparison.sale.state == "NONCOMPARABLE"
    assert "ACTIVE_LISTING_WHAT_IF" in stock.comparison.sale.reasons


def test_unknown_or_unreplayable_forecast_does_not_invent_expected_prices() -> None:
    b = baseline(evidence_state="missing")
    result = calculate_outcome(actual(), b)
    assert result.profit.amount == "82.05"
    assert result.comparison.sale.state == "UNAVAILABLE"
    assert result.comparison.sale.expected_amount is None
    damaged = replace(
        b, snapshot=None, calculation=None, unavailable_reason="SNAPSHOT_INTEGRITY_FAILURE"
    )
    result = calculate_outcome(actual(), damaged)
    assert result.net.amount == "162.05"
    assert "SNAPSHOT_INTEGRITY_FAILURE" in result.comparison.net.reasons


def test_minimum_decisions_strict_inputs_and_idempotency_normalization() -> None:
    b = baseline()
    not_bought = calculate_outcome(OutcomeActuals(purchase_decision="NOT_BOUGHT"), b)
    assert not_bought.state == "NOT_BOUGHT" and not_bought.acquisition.amount is None
    minimal = calculate_outcome(
        OutcomeActuals(purchase_decision="BOUGHT", sale_status="NOT_SOLD"), b
    )
    assert minimal.state == "NOT_SOLD" and minimal.profit.amount is None
    body = {"id": str(uuid4()), "expected_revision": 0, "actuals": actual().model_dump(mode="json")}
    normalized = OutcomeAppend.model_validate(body)
    body["actuals"]["purchase_price"] = "80.0"
    assert OutcomeAppend.model_validate(body) == normalized
    for changes in (
        {"purchase_price": 80.1},
        {"purchase_price": "-1"},
        {"purchase_price": "1.001"},
        {"labor_minutes": True},
        {"sale_status": "NOT_SOLD"},
        {"sold_on": "2026-09-30"},
        {"purchase_decision": "NOT_BOUGHT"},
        {"acquired_on": 1},
        {"result": {}},
    ):
        with pytest.raises(ValidationError):
            actual(**changes)
    with pytest.raises(ValidationError):
        OutcomeAppend.model_validate({**body, "expected_revision": 1})


def test_chronology_and_hostile_decimal_context() -> None:
    b = baseline()
    with pytest.raises(OutcomeChronologyError):
        calculate_outcome(actual(), replace(b, created_at=datetime(2026, 10, 2, tzinfo=UTC)))
    expected = calculate_outcome(actual(), b)
    with localcontext() as ctx:
        ctx.prec = 2
        ctx.rounding = ROUND_DOWN
        ctx.Emax = 2
        ctx.Emin = -2
        ctx.traps[Inexact] = True
        assert calculate_outcome(actual(), b) == expected
