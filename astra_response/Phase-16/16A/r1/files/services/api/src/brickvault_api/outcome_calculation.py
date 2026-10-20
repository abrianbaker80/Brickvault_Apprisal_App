"""Outcome-calculation-v1: recorded cash facts and frozen, per-metric comparison.

No IO, current prices, provider access or changes to the original forecast engine.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, localcontext
from typing import Literal
from uuid import UUID

from brickvault_api.economics_snapshot import SnapshotV1
from brickvault_api.economics_v1 import CalculationV1, arithmetic_context, signed_money
from brickvault_api.outcome_models import (
    MONEY_FIELDS,
    OutcomeActuals,
    OutcomeAmount,
    OutcomeComparison,
    OutcomeComparisonMetric,
    OutcomeResults,
)


class OutcomeChronologyError(ValueError):
    pass


@dataclass(frozen=True)
class OutcomeBaseline:
    original_id: UUID
    created_at: datetime
    snapshot: SnapshotV1 | None = None
    calculation: CalculationV1 | None = None
    unavailable_reason: str = "ORIGINAL_UNAVAILABLE"


def _sum(actuals: OutcomeActuals, fields: tuple[str, ...]) -> OutcomeAmount:
    missing = tuple(field for field in fields if getattr(actuals, field) is None)
    if missing:
        return OutcomeAmount(reasons=missing)
    total = sum((Decimal(getattr(actuals, field)) for field in fields), Decimal(0))
    return OutcomeAmount(amount=signed_money(total))


def _subtract(left: OutcomeAmount, right: OutcomeAmount) -> OutcomeAmount:
    if left.amount is None or right.amount is None:
        return OutcomeAmount(reasons=tuple(dict.fromkeys((*left.reasons, *right.reasons))))
    return OutcomeAmount(amount=signed_money(Decimal(left.amount) - Decimal(right.amount)))


def _comparison(
    actuals: OutcomeActuals,
    baseline: OutcomeBaseline,
    net: OutcomeAmount,
    profit: OutcomeAmount,
    acquisition: OutcomeAmount,
) -> OutcomeComparison:
    snapshot, calculated = baseline.snapshot, baseline.calculation
    expected_sale = expected_net = expected_profit = expected_acquisition = None
    unavailable: tuple[str, ...] = ()
    reasons: list[str] = []
    if actuals.purchase_decision != "BOUGHT":
        reasons.append("NOT_BOUGHT")
    if actuals.sale_status != "COMPLETE":
        reasons.append("SALE_NOT_COMPLETE")
    if actuals.sale_strategy != "COMPLETE_SET":
        reasons.append("STRATEGY_UNVERIFIED_OR_CHANGED")
    if actuals.contents_state != "CONFIRMED_MATCH":
        reasons.append("CONTENTS_UNVERIFIED_OR_CHANGED")
    if actuals.forecast_preceded_purchase is not True:
        reasons.append("FORECAST_NOT_CONFIRMED_BEFORE_PURCHASE")
    if actuals.acquired_on is None:
        reasons.append("ACQUISITION_DATE_UNKNOWN")
    if snapshot is None or calculated is None:
        unavailable = (baseline.unavailable_reason,)
    else:
        inputs = snapshot.inputs
        original = calculated.exact
        expected_sale, expected_net = original.expected_sale, original.estimated_net
        expected_profit, expected_acquisition = (
            original.estimated_profit,
            original.total_acquisition,
        )
        if inputs.basis.basis.value != "sold" or (
            calculated.presentation.interpretation != "SALE_ESTIMATE"
        ):
            reasons.append("ACTIVE_LISTING_WHAT_IF")
        if actuals.sale_condition != inputs.basis.condition.value:
            reasons.append("CONDITION_UNVERIFIED_OR_CHANGED")
        if (
            inputs.basis.representation != "COMPLETE_SET"
            or not inputs.historical.physical_admitted
            or inputs.historical.saleable_quantity != 1
            or inputs.historical.set_id is None
        ):
            reasons.append("ORIGINAL_SCOPE_UNVERIFIED")
        if inputs.basis.status.value != "SUPPORTED":
            unavailable = ("ORIGINAL_NOT_SUPPORTED",)

    def metric(
        actual: str | None,
        expected: str | None,
        *,
        extra: tuple[str, ...] = (),
        missing: tuple[str, ...] = (),
    ) -> OutcomeComparisonMetric:
        absent = (*unavailable, *(("ORIGINAL_VALUE_UNAVAILABLE",) if expected is None else ()))
        if actual is None:
            absent = (*absent, "ACTUAL_VALUE_UNAVAILABLE", *missing)
        # Unsupported/missing values must remain unavailable even with scope issues.
        if absent:
            return OutcomeComparisonMetric(
                state="UNAVAILABLE",
                actual_amount=actual,
                expected_amount=expected,
                reasons=tuple(dict.fromkeys(absent)),
            )
        blocked = tuple(dict.fromkeys((*reasons, *extra)))
        if blocked:
            return OutcomeComparisonMetric(
                state="NONCOMPARABLE",
                actual_amount=actual,
                expected_amount=expected,
                reasons=blocked,
            )
        assert actual is not None and expected is not None
        difference = Decimal(actual) - Decimal(expected)
        return OutcomeComparisonMetric(
            state="COMPARABLE",
            actual_amount=actual,
            expected_amount=expected,
            error_amount=signed_money(difference),
            error_exact=str(difference),
        )

    acquisition_reasons: tuple[str, ...] = ()
    if expected_acquisition is None or acquisition.amount is None:
        acquisition_reasons = ("ACQUISITION_BASIS_UNAVAILABLE",)
    elif Decimal(expected_acquisition) != Decimal(acquisition.amount):
        acquisition_reasons = ("ACQUISITION_BASIS_CHANGED",)
    sale_basis = snapshot.inputs.assumptions.sale_basis if snapshot else None
    return OutcomeComparison(
        original_id=baseline.original_id,
        original_digest=snapshot.digest if snapshot else None,
        original_created_at=baseline.created_at,
        set_number=snapshot.inputs.basis.set_number if snapshot else None,
        basis=snapshot.inputs.basis.basis.value if snapshot else None,
        sale_basis=sale_basis,
        meaning="UNAVAILABLE"
        if unavailable
        else ("ASSUMPTION_COMPARISON" if sale_basis == "MANUAL" else "FORECAST_COMPARISON"),
        original_acquisition=expected_acquisition,
        actual_acquisition=acquisition.amount,
        sale=metric(actuals.item_sale_proceeds, expected_sale),
        net=metric(net.amount, expected_net, missing=net.reasons),
        profit=metric(
            profit.amount, expected_profit, extra=acquisition_reasons, missing=profit.reasons
        ),
    )


def calculate_outcome(actuals: OutcomeActuals, baseline: OutcomeBaseline) -> OutcomeResults:
    # Dates are calendar dates. The recorded UTC date is the explicit baseline
    # convention; same-day ordering is attested by the operator, not invented.
    if baseline.created_at.utcoffset() is None:
        raise ValueError("aware_original_time_required")
    if (
        actuals.forecast_preceded_purchase is True
        and actuals.acquired_on is not None
        and actuals.acquired_on < baseline.created_at.astimezone(UTC).date()
    ):
        raise OutcomeChronologyError("OUTCOME_INVALID_CHRONOLOGY")
    # Original exact values permit up to 512-digit coefficients/exponents.
    # Keep subtraction exact even when the ambient Decimal context is hostile.
    with localcontext(arithmetic_context(2200)):
        if actuals.purchase_decision == "NOT_BOUGHT":
            unavailable = OutcomeAmount(reasons=("NOT_BOUGHT",))
            return OutcomeResults(
                state="NOT_BOUGHT",
                gross=unavailable,
                selling_costs=unavailable,
                net=unavailable,
                acquisition=unavailable,
                profit=unavailable,
                days_to_sell=None,
                duration_reasons=("NOT_BOUGHT",),
                comparison=_comparison(actuals, baseline, unavailable, unavailable, unavailable),
            )
        gross = _sum(actuals, ("item_sale_proceeds", "shipping_charged"))
        selling = _sum(
            actuals,
            (
                "selling_fees",
                "shipping_paid",
                "other_selling_costs",
                "replacement_costs",
                "labor_costs",
            ),
        )
        net = _subtract(gross, selling)
        acquisition = _sum(actuals, ("purchase_price", "acquisition_extra_costs"))
        profit = (
            _subtract(net, acquisition)
            if actuals.sale_status == "COMPLETE"
            else OutcomeAmount(reasons=("SALE_NOT_COMPLETE",))
        )
        duration_reasons: tuple[str, ...] = ()
        days = None
        if actuals.sale_status != "COMPLETE":
            duration_reasons = ("SALE_NOT_COMPLETE",)
        elif actuals.acquired_on is None or actuals.sold_on is None:
            duration_reasons = tuple(
                name for name in ("acquired_on", "sold_on") if getattr(actuals, name) is None
            )
        else:
            days = (actuals.sold_on - actuals.acquired_on).days
        missing = tuple(
            name
            for name in (
                *MONEY_FIELDS,
                "acquired_on",
                "sold_on",
                "sale_channel",
                "sale_strategy",
                "sale_condition",
            )
            if getattr(actuals, name) is None
            or (name == "sale_condition" and actuals.sale_condition == "UNKNOWN")
        )
        state: Literal["NOT_SOLD", "PARTIALLY_SOLD", "INCOMPLETE", "COMPLETE"] = (
            "NOT_SOLD"
            if actuals.sale_status == "NOT_SOLD"
            else "PARTIALLY_SOLD"
            if actuals.sale_status == "PARTIALLY_SOLD"
            else "INCOMPLETE"
            if missing
            else "COMPLETE"
        )
        return OutcomeResults(
            state=state,
            missing_fields=missing,
            gross=gross,
            selling_costs=selling,
            net=net,
            acquisition=acquisition,
            profit=profit,
            days_to_sell=days,
            duration_reasons=duration_reasons,
            comparison=_comparison(actuals, baseline, net, profit, acquisition),
        )
