from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker

class EmergencyState(FlightState):

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:

        if report.risk is RiskLevel.LOW:
            from flight_systems.decisions.states.cruise_state import CruiseState

            decision_maker.change_state(CruiseState())

            return Decision(
                mode=FlightMode.CRUISE,
                priority=report.risk,
                reason=ThreatType.NONE,
                message="Emergency resolved. Returning to cruise.",
                confidence=1.0
            )

        return Decision(
            mode=FlightMode.EMERGENCY,
            priority=report.risk,
            reason=report.threat,
            message="Remaining in emergency mode.",
            confidence=1.0
        )


