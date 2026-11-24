from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class LandedState(FlightState):
    """
    Terminal state after a successful touchdown.

    Current responsibility:
        - Remain in LANDED mode.
        - Return a LANDED decision.
        - Never transition back to another flight state.
    """

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:
        return Decision(
            mode=FlightMode.LANDED,
            priority=RiskLevel.LOW,
            reason=ThreatType.NONE,
            message="Aircraft has landed successfully.",
            confidence=1.0,
        )

