from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker

"""
Model of flight order:
    Runway
    ↓

    TAKEOFF

    Mission:
    Become airborne.

    ↓

    CLIMB

    Mission:
    Reach cruise altitude.

    ↓

    CRUISE

    Mission:
    Maintain stable flight.

    ↓

    DESCENT

    Mission:
    Lose altitude safely.

    ↓

    LANDING

    Mission:
    Return safely to the ground.


In Climb State we will add (or consider) mission and that's why we need two 
kind of information;
1. Fllight report
2. Mission

State = What operating phase am I in?
Mission = What objective am I trying to achieve?

             Mission
                │
                ▼
Plane → FlightReport → DecisionMaker → ClimbState
                                     │
                                     ▼
                                  Decision

"""
class ClimbState(FlightState):
    """
    Handle decision and transition rules while the aircraft is climbing.

    Responsibility:
        - Remain in CLIMB while approaching the mission altitude.
        - Transition to EMERGENCY if flight conditions become unsafe.
        - Transition to CRUISE when the mission altitude is sufficiently close.

    Handle decision and transition rules while the aircraft is climbing.
                  ClimbState
                      │
          ┌───────────┼───────────┐
          │           │           │
      dangerous   target met   still below
          │           │           │
          ▼           ▼           ▼
     EMERGENCY      CRUISE       CLIMB
    """

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:
        """
        Check safety
            ↓
        Danger?
            → EMERGENCY

        Otherwise
            ↓
        Read mission target
            ↓
        Climb complete?
            → CRUISE

        Otherwise
            → CLIMB
        """
        # Safety has the highest priority.
        if self._should_enter_emergency(report):
            from flight_systems.decisions.states.emergency_state import (
                EmergencyState,
            )

            decision_maker.change_state(EmergencyState())

            return Decision(
                mode=FlightMode.EMERGENCY,
                priority=report.risk,
                reason=report.most_urgent_threat,
                message="Unsafe climb. Entering emergency mode.",
                confidence=1.0,
            )

        target_altitude = decision_maker.mission.target_altitude

        # Mission objective has been reached closely enough.
        if self._climb_complete(report=report, target_altitude=target_altitude):
            from flight_systems.decisions.states.cruise_state import (
                CruiseState,
            )

            decision_maker.change_state(CruiseState())

            return Decision(
                mode=FlightMode.CRUISE,
                priority=report.risk,
                reason=ThreatType.NONE,
                message=(
                    "Climb complete. "
                    f"Target altitude: {target_altitude:.0f} m. "
                    "Transitioning to cruise."
                ),
                confidence=1.0,
            )

        return Decision(
            mode=FlightMode.CLIMB,
            priority=report.risk,
            reason=ThreatType.NONE,
            message=(
                "Continuing climb toward "
                f"{target_altitude:.0f} m."
            ),
            confidence=1.0,
        )

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        return report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def _climb_complete(self, report: FlightReport, target_altitude: float) -> bool:
        """Compare the current plane condition with mission object (target altitude)"""
        minimum_completion_altitude = (target_altitude - self.altitude_tolerance)
        return report.altitude >= minimum_completion_altitude
