from enum import Enum


class RiskLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatType(Enum):
    NONE = "NONE"
    STALL = "STALL"
    IMPACT = "IMPACT"
    OVERSPEED = "OVERSPEED"


class Recoverability(Enum):
    IMPOSSIBLE = "IMPOSSIBLE"
    POOR = "POOR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


class EnergyState(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXCESSIVE = "EXCESSIVE"


