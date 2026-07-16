from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .enums import FlightMode, ThreatType, RiskLevel


class Decision:
    """
    Represents the behavior selected by the DecisionMaker. In another word, Represents the result produced by the DecisionMaker.
    It communicates what the aircraft should do, why it should do it,
    and how urgent the decision is.

    responsibility of Decision is to stores meaning.

    example usage: 
        Decision(
            mode=FlightMode.EMERGENCY,
            reason=ThreatType.STALL,
            priority=RiskLevel.CRITICAL,
            message="Entering emergency mode because time to stall is below 2 seconds.",
            confidence=0.98,
        )
    """

    def __init__(self, mode: "FlightMode", reason: "ThreatType", priority: "RiskLevel", message: str, confidence: float) -> None:
        self.mode = mode
        self.reason = reason
        self.priority = priority
        self.message = message
        self.confidence = confidence


