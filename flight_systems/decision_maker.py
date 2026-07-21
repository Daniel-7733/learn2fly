from .decision import Decision
from .enums import FlightMode, RiskLevel, ThreatType
from .flight_report import FlightReport


class DecisionMaker:
    """
    Reads a FlightReport and manages flight-mode transitions.

    It remembers the current flight mode and returns a Decision.
    It does not move the aircraft or set controller targets.


    Important concept: state machine
    This design is the beginning of a finite-state machine.
                  HIGH / CRITICAL
           ┌─────────────────────────┐
           │                         ▼
       ┌────────┐                 ┌───────────┐
       │ CRUISE │                 │ EMERGENCY │
       └────────┘                 └───────────┘
           ▲                         │
           └─────────────────────────┘
                      LOW
    """

    def __init__(self) -> None:
        self.current_mode = FlightMode.CRUISE

    def make_decision(self, report: FlightReport) -> Decision:
        """
        Selects a decision based on the current mode and flight report.
        """

        if self.current_mode is FlightMode.CRUISE:
            return self._decide_from_cruise(report)

        if self.current_mode is FlightMode.EMERGENCY:
            return self._decide_from_emergency(report)

        raise RuntimeError(
            f"Unsupported flight mode: {self.current_mode}"
        )

    def _decide_from_cruise(self, report: FlightReport) -> Decision:
        """
        Handles decisions while currently in cruise mode.
        """

        if report.risk in {
            RiskLevel.HIGH,
            RiskLevel.CRITICAL,
        }:
            self.current_mode = FlightMode.EMERGENCY

            return Decision(
                mode=self.current_mode,
                reason=report.most_urgent_threat,
                priority=report.risk,
                message="Danger detected. Entering emergency mode.",
                confidence=1.0,
            )

        return Decision(
            mode=self.current_mode,
            reason=ThreatType.NONE,
            priority=report.risk,
            message="Remaining in cruise mode.",
            confidence=1.0,
        )

    def _decide_from_emergency(self, report: FlightReport) -> Decision:
        """
        Handles decisions while currently in emergency mode.
        """

        if report.risk is RiskLevel.LOW:
            self.current_mode = FlightMode.CRUISE

            return Decision(
                mode=self.current_mode,
                reason=ThreatType.NONE,
                priority=report.risk,
                message="Threat resolved. Returning to cruise mode.",
                confidence=1.0,
            )

        return Decision(
            mode=self.current_mode,
            reason=report.most_urgent_threat,
            priority=report.risk,
            message="Emergency condition remains active.",
            confidence=1.0,
        )


