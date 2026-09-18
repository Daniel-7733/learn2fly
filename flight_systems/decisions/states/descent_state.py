from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class DescentState(FlightState):
    """
    Handle decisions while the aircraft is descending.

    Current responsibilities:
        - Enter EMERGENCY when flight conditions become unsafe.
        - Remain in DESCENT while conditions are safe.

    The transition to LandingState will be added after LandingState exists.
    """

    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:
        """
        Decision order:

            Check safety
                ↓
            Unsafe?
                ├── Yes → EMERGENCY
                └── No  → continue DESCENT
        """

        # ---------------------------------------------------------
        # Safety always has the highest priority.
        # ---------------------------------------------------------
        if self._should_enter_emergency(report):
            # Local import prevents circular imports between states.
            from flight_systems.decisions.states.emergency_state import (
                EmergencyState,
            )

            decision_maker.change_state(EmergencyState())

            return Decision(
                mode=FlightMode.EMERGENCY,
                priority=report.risk,
                reason=report.most_urgent_threat,
                message="Unsafe descent. Entering emergency mode.",
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # Landing transition will be added in the next step. (Descent completed successfully.)
        # ---------------------------------------------------------
        # if self._landing_phase_reached(report, mission.landing_transition_altitude_m):
        #     from flight_systems.decisions.states.emergency_state import (
        #             Landing_State,
        #             )
        #
        #     decision_maker.change_state(Landing_State())
        #
        #     return Decision(
        #         mode=FlightMode.LANDING,
        #         priority=report.risk,
        #         reason=ThreatType.NONE,
        #         message="Safe Landing reached. Transitioning to Landing.",
        #         confidence=1.0,
        #     )
        # ---------------------------------------------------------
        # Continue descending.
        # ---------------------------------------------------------
        return Decision(
            mode=FlightMode.DESCENT,
            priority=report.risk,
            reason=ThreatType.NONE,
            message="Continuing descent.",
            confidence=1.0,
        )

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        """Return True when descent conditions are unsafe."""
        return report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def _landing_phase_reached(report: FlightReport, landing_transition_altitude_m: Mission) -> bool:
        return report.altitude <= landing_transition_altitude_m
