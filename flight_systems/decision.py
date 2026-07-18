from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .enums import FlightMode, ThreatType, RiskLevel


class Decision:
    """
    Represents the behavior selected by the DecisionMaker. In another word, Represents the result produced by the DecisionMaker.
    It communicates what the aircraft should do, why it should do it,
    and how urgent the decision is.

    Responsibility of Decision is to stores meaning.

    Stores the result produced by DecisionMaker.

    It communicates:
    - what mode the aircraft should use,
    - why the mode was selected,
    - how urgent the situation is,
    - and a readable explanation.

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

    def __str__(self) -> str:
        return (
            "============ Decision Details ============\n"
            f"Mode: {self.mode.value} | \n"
            f"Reason: {self.reason.value} | \n"
            f"Priority: {self.priority.value} | \n"
            f"Message: {self.message} | \n"
            f"Confidence: {self.confidence} | \n"
            "==========================================\n"
        )

