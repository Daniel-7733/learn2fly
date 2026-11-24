from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class LandingState(FlightState):
    def __init__(self, max_touchdown_sink_rate_mps: float = 2.0,
                 landing_speed_tolerance_mps: float = 5.0) -> None:
        self.max_touchdown_sink_rate_mps = max_touchdown_sink_rate_mps
        self.landing_speed_tolerance_mps = landing_speed_tolerance_mps


    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:
        """
        1. Ground reached?
           ├── Yes, safe speeds   → LANDED
           └── Yes, unsafe speeds → EMERGENCY / IMPACT

        2. Unsafe while still airborne?
           └── EMERGENCY

        3. Otherwise
           └── Continue LANDING
        """
        # ---------------------------------------------------------
        # 1. Evaluate touchdown before ordinary airborne threats.
        # ---------------------------------------------------------

        if self._ground_reached(report):
            if self._touchdown_is_safe(report, decision_maker.mission.landing_speed):
                from flight_systems.decisions.states.landed_state import (
                    LandedState,
                )

                decision_maker.change_state(LandedState())

                return Decision(
                    mode=FlightMode.LANDED,
                    priority=RiskLevel.LOW,
                    reason=ThreatType.NONE,
                    message="Safe touchdown. Entering landed mode.",
                    confidence=1.0,
                )

            from flight_systems.decisions.states.emergency_state import (
                EmergencyState,
            )

            decision_maker.change_state(EmergencyState())

            return Decision(
                mode=FlightMode.EMERGENCY,
                priority=report.risk,
                reason=ThreatType.IMPACT,
                message="Unsafe touchdown. Entering emergency mode.",
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # 2. Handle airborne emergencies.
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
                message="Unsafe landing. Entering emergency mode.",
                confidence=1.0
            )
        
        
        # ---------------------------------------------------------
        # 3. Continue landing.
        # ---------------------------------------------------------

        return Decision(
            mode=FlightMode.LANDING,
            priority=report.risk,
            reason=ThreatType.NONE,
            message="continuing landing.",
            confidence=1.0
        )

    def _should_enter_emergency(self, report: FlightReport) -> bool:
        """Return True when landing conditions are unsafe."""
        return report.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def _ground_reached(self, report: FlightReport) -> bool:
        """Return True if altitude is 0 or under 0"""
        return report.altitude <= 0.0

    def _touchdown_is_safe(self, report: FlightReport, landing_speed_mps: float) -> bool:
        """
        Return true if vertical & horizontal speed is safe.
        
        Example:
        -1.5 >= -2.0 → safe
        -6.0 >= -2.0 → false, unsafe
        """
        maximum_horizontal_speed = (
            landing_speed_mps
            + self.landing_speed_tolerance_mps
        )

        safe_vertical_speed = (
            report.vertical_speed
            >= -self.max_touchdown_sink_rate_mps
        )

        safe_horizontal_speed = (
            report.horizontal_speed
            <= maximum_horizontal_speed
        )

        # safe touchdown 
        return safe_vertical_speed and safe_horizontal_speed           
