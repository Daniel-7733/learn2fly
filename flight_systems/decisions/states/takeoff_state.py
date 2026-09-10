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
    """
    Handle decisions and transitions while the aircraft is taking off.

    Responsibility:
        - Remain in TAKEOFF until a safe altitude is reached.
        - Transition to EMERGENCY if safety becomes unacceptable.
        - Transition to CLIMB after successful takeoff.
    """

    def __init__(self, safe_altitude: float = 300.0) -> None:
        """
        safe_altitude:
            Minimum altitude required before takeoff is considered complete.
        """
        self.safe_altitude = safe_altitude

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:

        # ---------------------------------------------------------
        # Safety always has the highest priority.
        # ---------------------------------------------------------
        if self._should_enter_emergency(report):
            from flight_systems.decisions.states.emergency_state import (
                EmergencyState,
            )

            decision_maker.change_state(EmergencyState())

            return Decision(
                mode=FlightMode.EMERGENCY,
                priority=report.risk,
                reason=report.most_urgent_threat,
                message="Unsafe takeoff. Entering emergency mode.",
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # Takeoff completed successfully.
        # ---------------------------------------------------------
        if self._takeoff_complete(report):
            from flight_systems.decisions.states.climb_state import (
                ClimbState,
            )

            decision_maker.change_state(ClimbState())

            return Decision(
                mode=FlightMode.CLIMB,
                priority=report.risk,
                reason=ThreatType.NONE,
                message="Safe altitude reached. Transitioning to climb.",
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # Continue takeoff.
        # ---------------------------------------------------------
        return Decision(
            mode=FlightMode.TAKEOFF,
            priority=report.risk,
            reason=ThreatType.NONE,
            message="Continuing takeoff.",
            confidence=1.0,
        )

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        """Return True if takeoff is no longer safe."""
        return report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def _takeoff_complete(self, report: FlightReport) -> bool:
        """Return True when the aircraft reaches a safe takeoff altitude."""
        return report.altitude >= self.safe_altitude
