
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import ThreatType, RiskLevel

 # ====================== Update Class ====================== #
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

    def __str__(self) -> str:
        """Returns a human-readable telemetry dashboard for printing."""
        return (
            f"\n=== FLIGHT SAFETY REPORT ===\n"
            f"Risk Level:         {self.risk.value}\n"
            f"Most Urgent Threat: {self.most_urgent_threat.value}\n"
            f"----------------------------\n"
            f"Altitude:           {self.altitude:,.2f} m\n"
            f"Speed Margin:       {self.speed_margin:,.2f} m/s\n"
            f"AoA Margin:         {self.aoa_margin:,.2f}°\n"
            f"Time to Stall:      {self.time_to_stall:,.2f}s\n"
            f"Time to Impact:     {self.time_to_impact:,.2f}s\n"
            f"============================"
        )

    def __repr__(self) -> str:
        """Returns a standard developer-focused string representation."""
        return (
            f"FlightReport(speed_margin={self.speed_margin}, aoa_margin={self.aoa_margin}, "
            f"altitude={self.altitude}, time_to_stall={self.time_to_stall}, "
            f"time_to_impact={self.time_to_impact}, most_urgent_threat={self.most_urgent_threat}, "
            f"risk={self.risk})"
        )
 # ====================== Update Class ====================== #


