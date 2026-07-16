from .decision import Decision
from .enums import FlightMode, RiskLevel, ThreatType
from .flight_report import FlightReport


class DecisionMaker:
    """
    Interprets the FlightReport and chooses the aircraft's behavior. In another words, Reads a FlightReport and returns a Decision.
    responsibility of DecisionMaker is to creates meaning
    """
    def __init__(self) -> None:
        pass

    def make_decision(self, report: FlightReport) -> Decision:
        if report.risk is RiskLevel.CRITICAL:
            return Decision(
                mode=FlightMode.EMERGENCY,
                reason=report.most_urgent_threat,
                priority=report.risk,
                message="Critical flight condition detected.",
                confidence=1.0,
            )

        return Decision(
            mode=FlightMode.CRUISE,
            reason=ThreatType.NONE,
            priority=report.risk,
            message="The aircraft is operating normally.",
            confidence=1.0,
        )


