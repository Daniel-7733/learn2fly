from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import ThreatType, RiskLevel

class FlightReport:
    def __init__(self, speed_margin: float, aoa_margin: float, altitude: float, time_to_stall: float, time_to_impact: float, 
                 most_urgent_threat: "ThreatType", risk: "RiskLevel") -> None:

        self.speed_margin = speed_margin
        self.aoa_margin = aoa_margin
        self.altitude = altitude
        self.time_to_stall = time_to_stall
        self.time_to_impact = time_to_impact
        self.most_urgent_threat = most_urgent_threat
        self.risk = risk

    def to_dict(self) -> dict[str, str]:
        return {
            "Speed Margin": f"{self.speed_margin} m/s",
            "AoA Margin": f"{self.aoa_margin}°",
            "Altitude": f"{self.altitude} m",
            "Time To Stall": f"{self.time_to_stall} s",
            "Time To Impact": f"{self.time_to_impact} s",
            "Most Urgent Threat": self.most_urgent_threat.value,
            "Risk": self.risk.value,
        }

