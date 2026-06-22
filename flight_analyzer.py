from enums import ThreatType, RiskLevel
from flight_calculator import FlightCalculator
from flight_report import FlightReport

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

    def calculate_risk_level(self, speed_margin: float, aoa_margin: float, time_to_stall: float, time_to_impact: float) -> RiskLevel:
        """So, this function answer to this question: How serious is the whole situation?"""

        # 1. Already crossed boundary
        if speed_margin <= 0 or aoa_margin <= 0:
            return RiskLevel.CRITICAL

        # 2. Very close to boundary, even if rate is slow
        if aoa_margin < 2 or speed_margin < 5:
            return RiskLevel.HIGH

        if aoa_margin < 5 or speed_margin < 10:
            return RiskLevel.MODERATE

        # 3. Future countdown danger
        shortest_time_to_danger: float = min(time_to_stall, time_to_impact)

        if shortest_time_to_danger < 2:
            return RiskLevel.CRITICAL

        if shortest_time_to_danger < 5:
            return RiskLevel.HIGH

        if shortest_time_to_danger < 15:
            return RiskLevel.MODERATE

        return RiskLevel.LOW

    def report(self) -> FlightReport:
        speed_margin = self.plane.horizontal_speed - self.plane.min_safe_speed
        aoa_margin = self.plane.critical_aoa - self.plane.aoa

        time_to_stall = FlightCalculator.time_to_stall(
            self.plane.aoa,
            self.plane.aoa_rate,
            self.plane.critical_aoa,
        )

        time_to_impact = FlightCalculator.time_to_impact(
            self.plane.altitude,
            self.plane.vertical_speed,
        )

        most_urgent_threat = self.urgency_variable(time_to_stall, time_to_impact)

        risk = self.calculate_risk_level(
            speed_margin,
            aoa_margin,
            time_to_stall,
            time_to_impact,
        )

        return FlightReport(
            speed_margin,
            aoa_margin,
            self.plane.altitude,
            time_to_stall,
            time_to_impact,
            most_urgent_threat,
            risk,
        )
