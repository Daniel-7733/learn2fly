from .decision import Decision
from .enums import FlightMode, RiskLevel, ThreatType
from .flight_report import FlightReport


class DecisionMaker:
    """
    Reads a FlightReport and chooses the aircraft's current behavior.

    It does not move the aircraft.
    It does not set controller targets.
    It only returns a Decision.
    """

    def make_decision(self, report: FlightReport) -> Decision:
        # ---------------------------------------------------------
        # 1. Critical emergencies
        # ---------------------------------------------------------

        if report.risk is RiskLevel.CRITICAL:
            return Decision(
                mode=FlightMode.EMERGENCY,
                reason=report.most_urgent_threat,
                priority=report.risk,
                message=(
                    "Critical flight condition detected. "
                    f"Most urgent threat: "
                    f"{report.most_urgent_threat.value}."
                ),
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # 2. High-risk situations
        # ---------------------------------------------------------

        if report.risk is RiskLevel.HIGH:
            return Decision(
                mode=FlightMode.EMERGENCY,
                reason=report.most_urgent_threat,
                priority=report.risk,
                message=(
                    "High-risk condition detected. "
                    "Preventive recovery is required."
                ),
                confidence=1.0,
            )

        # ---------------------------------------------------------
        # 3. Normal operation
        # ---------------------------------------------------------

        return Decision(
            mode=FlightMode.CRUISE,
            reason=ThreatType.NONE,
            priority=report.risk,
            message="No immediate emergency detected.",
            confidence=1.0,
        )

