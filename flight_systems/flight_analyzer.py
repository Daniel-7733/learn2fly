from .enums import ThreatType, RiskLevel, Recoverability, EnergyState
from .flight_calculator import FlightCalculator
from .flight_report import FlightReport

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plane import Plane
    from .autopilot import AutoPilot


class FlightAnalyzer:
    """
    FlightAnalyzer = interpretation

    1. Danger: Is the plane in danger?
    2. Urgency: How urgent is the danger?
    3. Recoverability: How many recovery options remain?
    """
    def __init__(self, plane: "Plane", autopilot: "AutoPilot") -> None:
        self.plane = plane
        self.autopilot = autopilot


    # ============ Analyzing the score ============== #

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

    def calculate_recoverability_score(self) -> int: # I might not use this one
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

    def calculate_specific_energy_score(self, specific_energy: float) -> int:
        if specific_energy < 100:
            return 0

        if specific_energy < 500:
            return 1

        if specific_energy < 1000:
            return 2

        if specific_energy < 10000:
            return 3

        return 4

    def calculate_risk(self) -> int:
        """
        A simple model for calculating the risk:
        risk = danger + urgency - recoverability
        """
        return self.calculate_danger() + self.calculate_urgency() - self.calculate_recoverability_score()


    # ============ Analyzing the Level ============== #

    def urgency_variable(self, time_to_stall: float, time_to_impact: float) -> ThreatType:
        """This function will say which variable is urgency and need to take care of it"""
        if time_to_stall < time_to_impact:
            return ThreatType.STALL

        if time_to_impact < time_to_stall:
            return ThreatType.IMPACT

        return ThreatType.NONE

    def determine_most_urgent_threat(self, altitude: float, speed_margin: float, aoa_margin: float, time_to_stall: float, time_to_impact: float) -> ThreatType:
        """
        Determines the aircraft's most urgent current threat.

        Crossed boundaries are checked before future countdowns.
        """

        # The aircraft has reached or crossed the ground.
        if altitude <= 0:
            return ThreatType.IMPACT

        # Immediate terrain collision is now the dominant danger.
        if time_to_impact <= 2.0:
            return ThreatType.IMPACT

        # The aircraft is already beyond the critical AoA.
        if aoa_margin <= 0:
            return ThreatType.STALL

        # Later, after adding LOW_SPEED to ThreatType:
        # if speed_margin <= 0:
        #     return ThreatType.LOW_SPEED

        # Compare future dangers only when boundaries are not crossed.
        if time_to_stall < time_to_impact:
            return ThreatType.STALL

        if time_to_impact < time_to_stall:
            return ThreatType.IMPACT

        return ThreatType.NONE

    def calculate_risk_level(self, speed_margin: float, aoa_margin: float, time_to_stall: float, time_to_impact: float) -> RiskLevel:
        """So, this function answer to this question: How serious is the whole situation?"""

        # 1. Immediate Crash / Crossed Boundary
        if speed_margin <= 0 or aoa_margin <= 0:
            return RiskLevel.CRITICAL

        shortest_time_to_danger: float = min(time_to_stall, time_to_impact)

        # 2. All Time-Based Countdown Dangers (Highest priority to lowest)
        if shortest_time_to_danger < 2:
            return RiskLevel.CRITICAL
        if shortest_time_to_danger < 5:
            return RiskLevel.HIGH
        if shortest_time_to_danger < 15:
            return RiskLevel.MODERATE

        # 3. Static Margin Dangers (Checked only if time is safe)
        if aoa_margin < 2 or speed_margin < 5:
            return RiskLevel.HIGH
        if aoa_margin < 5 or speed_margin < 10:
            return RiskLevel.MODERATE

        return RiskLevel.LOW

    def classify_recoverability(self, recovery_margin: float) -> Recoverability:
        if recovery_margin < 0:
            return Recoverability.IMPOSSIBLE

        if recovery_margin < 5:
            return Recoverability.POOR

        if recovery_margin < 15:
            return Recoverability.GOOD

        return Recoverability.EXCELLENT

    def calculate_specific_energy_level(self, specific_energy: float) -> EnergyState:
        if specific_energy < 500:
            return EnergyState.LOW

        if specific_energy < 2000:
            return EnergyState.MODERATE

        if specific_energy < 15000:
            return EnergyState.HIGH

        return EnergyState.EXCESSIVE


    # ============ Analyzing the lefted time  ============== #

    def estimate_required_recovery_time(self, aoa_margin: float, speed_margin: float, vertical_speed: float, throttle: float) -> float:
        required_time: float = 5.0

        if abs(vertical_speed) > 20:
            required_time += 3.0

        if aoa_margin < 3:
            required_time += 3.0

        if speed_margin < 10:
            required_time += 2.0

        if throttle < 0.5:
            required_time += 2.0

        return required_time

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

        most_urgent_threat = self.determine_most_urgent_threat(
            altitude=self.plane.altitude,
            speed_margin=speed_margin,
            aoa_margin=aoa_margin,
            time_to_stall=time_to_stall,
            time_to_impact=time_to_impact,
        )

        risk = self.calculate_risk_level(
            speed_margin,
            aoa_margin,
            time_to_stall,
            time_to_impact,
        )

        required_time = self.estimate_required_recovery_time(
                aoa_margin,
                speed_margin,
                self.plane.vertical_speed,
                self.plane.throttle,
                )

        recovery_margin = FlightCalculator.recovery_margin(
                FlightCalculator.time_to_impact(self.plane.altitude, self.plane.vertical_speed),
                required_time,
                )

        recoverability = self.classify_recoverability(recovery_margin)


        specific_energy_score = self.calculate_specific_energy_score(self.plane.specific_energy)
        energy_state = self.calculate_specific_energy_level(self.plane.specific_energy)

        return FlightReport(
            speed_margin,
            aoa_margin,
            self.plane.altitude,
            time_to_stall,
            time_to_impact,
            most_urgent_threat,
            risk,
            recoverability,
            energy_state,
        )
