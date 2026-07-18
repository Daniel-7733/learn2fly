from enum import Enum


class RiskLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatType(Enum):
    NONE = "NONE"
    STALL = "STALL"
    LOW_SPEED = "LOW_SPEED"
    IMPACT = "IMPACT"
    OVERSPEED = "OVERSPEED"
    ENERGY_LOSS = "ENERGY_LOSS"


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


class FlightMode(Enum):
    TAKEOFF = "TAKEOFF"
    CLIMB = "CLIMB"
    CRUISE = "CRUISE"
    DESCENT = "DESCENT"
    LANDING = "LANDING"
    EMERGENCY = "EMERGENCY"


