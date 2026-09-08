from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class EmergencyState(FlightState):
    """
    Keeps the aircraft in emergency mode until the risk has remained
    low for several consecutive updates.
    """

    def __init__(self, safe_updates_required: int = 3) -> None:
        self.safe_updates_required = safe_updates_required
        self.safe_update_count: int = 0

    def _recovery_confirmed(self) -> bool:
        return self.safe_update_count >= self.safe_updates_required

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:

        if report.risk is RiskLevel.LOW:
            self.safe_update_count += 1
        else:
            # Recovery was interrupted.
            self.safe_update_count = 0

        if self._recovery_confirmed():
            from flight_systems.decisions.states.cruise_state import (
                CruiseState,
            )

            decision_maker.change_state(CruiseState())

            return Decision(
                mode=FlightMode.CRUISE,
                priority=report.risk,
                reason=ThreatType.NONE,
                message=(
                    "Emergency resolved after "
                    f"{self.safe_update_count} safe updates. "
                    "Returning to cruise."
                ),
                confidence=1.0,
            )

        return Decision(
            mode=FlightMode.EMERGENCY,
            priority=report.risk,
            reason=report.most_urgent_threat,
            message=(
                "Remaining in emergency mode. "
                f"Safe updates: {self.safe_update_count}/"
                f"{self.safe_updates_required}."
            ),
            confidence=1.0,
        )


