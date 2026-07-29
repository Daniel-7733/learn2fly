from dataclasses import dataclass
from flight_systems.enums import RiskLevel, ThreatType, FlightMode

@dataclass(frozen=True)
class FlightSample:
    time: float
    altitude: float
    horizontal_speed: float
    vertical_speed: float
    pitch_angle: float
    aoa: float
    throttle: float
    risk: RiskLevel
    threat: ThreatType
    mode: FlightMode

