from enums import ThreatType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plane import Plane
    from autopilot import AutoPilot


class FlightAnalyzer:
    """
    FlightAnalyzer = interpretation

    1. Is the plane in danger?
    2. How urgent is the danger?
    3. How many recovery options remain?
    """
    def __init__(self, plane: "Plane", autopilot: "AutoPilot") -> None:
        self.plane = plane
        self.autopilot = autopilot

    def calculate_danger(self) -> int:
        danger: int = 0

        if self.plane.horizontal_speed < self.plane.min_safe_speed:
            danger += 3

        if self.plane.aoa > self.plane.critical_aoa:
            danger += 5
        elif self.plane.aoa > self.autopilot.max_safe_aoa:
            danger += 2

        if self.plane.altitude < 100:
            danger += 2

        return danger

    def calculate_recoverability(self) -> int:
        recoverability: int = 0

        if self.plane.altitude > 1000:
            recoverability += 3

        if self.plane.horizontal_speed > self.plane.min_safe_speed:
            recoverability += 2

        if self.plane.aoa < self.autopilot.max_safe_aoa:
            recoverability += 2

        if self.plane.throttle > 0:
            recoverability += 2

        return recoverability

    def calculate_urgency(self) -> int:
        urgency: int = 0

        if self.plane.vertical_speed < 0:
            time_to_ground: float = self.plane.altitude / abs(self.plane.vertical_speed)
        else:
            time_to_ground = float("inf")

        if time_to_ground < 5:
            urgency = 5
        elif time_to_ground < 20:
            urgency = 3
        else:
            urgency = 1

        return urgency

    def calculate_risk(self) -> int:
        """
        A simple model for calculating the risk:
        risk = danger + urgency - recoverability
        """
        return self.calculate_danger() + self.calculate_urgency() - self.calculate_recoverability()

    def urgency_variable(self, time_to_stall: float, time_to_impact: float) -> ThreatType:
        """This function will say which variable is urgency and need to take care of it"""
        if time_to_stall < time_to_impact:
            return ThreatType.STALL

        if time_to_impact < time_to_stall:
            return ThreatType.IMPACT

        return ThreatType.NONE

    def report(self) -> dict[str, int]:
        return {
            "danger": self.calculate_danger(),
            "urgency": self.calculate_urgency(),
            "recoverability": self.calculate_recoverability(),
            "risk": self.calculate_risk(),
        }
