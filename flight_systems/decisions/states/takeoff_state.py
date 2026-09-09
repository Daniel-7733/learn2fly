from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker

"""
Just a model to see how does we work
                handle(report)
                      |
            Is risk dangerous?
               /            \
             yes             no
             |               |
      enter EMERGENCY   safe altitude reached?
                            /       \
                          yes        no
                          |          |
                       CLIMB       TAKEOFF
"""
class TakeoffState(FlightState):
    """Handle decisions and transitions while the aircraft is taking off."""

    def __init__(self, safe_altitude: float = ...) -> None:
        self.safe_altitude = safe_altitude

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:

        # 1. Check whether safety requires EmergencyState.

        # 2. Check whether takeoff is complete.

        # 3. If complete, transition to ClimbState.

        # 4. Otherwise remain in TakeoffState.

        # 5. Return the appropriate Decision.

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        """Return whether safety requires EMERGENCY."""
        return NotImplementedError("_should_enter_emergency is Not Implemented")

    def _takeoff_complete(self, report: FlightReport) -> bool:
        """Return whether safe takeoff altitude has been reached."""
        return report.altitude >= self.safe_altitude

