from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta


@dataclass
class DeadlineResult:
    deadline_type: str
    calculation_status: str
    anchor_date: date | None
    calculated_date: date | None
    assumptions: dict
    explanation: str


def calculate_one_month_deadline(anchor_date: date | None, deadline_type: str = "rechtsbehelf") -> DeadlineResult:
    if not anchor_date:
        return DeadlineResult(deadline_type, "missing_anchor", None, None, {}, "Keine Berechnung möglich, weil kein Bekanntgabe- oder Zustelldatum erkannt wurde.")
    calculated = anchor_date + relativedelta(months=1)
    return DeadlineResult(deadline_type, "uncertain", anchor_date, calculated, {"rule": "one_month_from_anchor_date"}, "Vorläufige Monatsfrist ab Ankerdatum. Keine verbindliche Rechtsberatung.")
