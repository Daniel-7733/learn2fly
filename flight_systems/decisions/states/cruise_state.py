from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class CruiseState(FlightState):

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        """ The simple version is 'return report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}'"""
        if report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return True
        return False

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:

        if self._should_enter_emergency(report):
            from flight_systems.decisions.states.emergency_state import (
                EmergencyState,
            )

            decision_maker.change_state(EmergencyState())

            return Decision(
                mode=FlightMode.EMERGENCY,
                priority=report.risk,
                reason=report.most_urgent_threat,
                message=(f"Transitioning from Cruise to Emergency "
                         f"because of {report.most_urgent_threat.value}."),
                confidence=1.0
            )

        return Decision(
            mode=FlightMode.CRUISE,
            priority=report.risk,
            reason=ThreatType.NONE,
            message="Remaining in cruise mode.",
            confidence=1.0
        )

