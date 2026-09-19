from dataclasses import dataclass

import pytest

from flight_systems.autopilot import AutoPilot
from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.enums import (
    EnergyState,
    FlightMode,
    Recoverability,
    RiskLevel,
    ThreatType,
)
from flight_systems.flight_report import FlightReport
from flight_systems.missions.mission import Mission


# ============================================
# Initializing some fake classes
# ============================================


@dataclass
class FakePlane:
    """
    Provides only the Plane attributes and methods AutoPilot needs.

    Physics is intentionally excluded from this test.

    This fake exists because this test is checking the boundary between:
        DecisionMaker -> Decision -> AutoPilot -> Controller

    We do not need the full Plane physics engine here.
    """

    horizontal_speed: float
    min_safe_speed: float
    aoa: float
    altitude: float

    # Used by AutoPilot during stall recovery.
    # The real Plane calculates this from its motion.
    # Here we provide a fixed value so the test stays deterministic.
    flight_path_angle_value: float = 0.0

    def flight_path_angle(self) -> float:
        """Return the fake flight-path angle used by AutoPilot."""
        return self.flight_path_angle_value


@dataclass
class FakeController:
    """
    Receives the targets selected by AutoPilot.

    We only need the outputs that this boundary test cares about:
        - target_pitch
        - target_throttle
    """

    target_pitch: float = 0.0
    target_throttle: float = 0.0

# ============================================
#   Helper function for consistance altitude
# ============================================
def make_cruise_scenario(altitude: float) -> tuple[FlightReport, FakePlane]:
    report = FlightReport(
        speed_margin=50.0,
        aoa_margin=10.0,
        altitude=altitude,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
        horizontal_speed = 100.0,
        distance_travelled_m = 30_000.0,
    )

    plane = FakePlane(
        horizontal_speed=100.0,
        min_safe_speed=50.0,
        aoa=5.0,
        altitude=altitude,
        flight_path_angle_value=-10.0,
    )

    return report, plane

# ============================================
# Test the emergency decision -> AutoPilot path
# ============================================


@pytest.mark.parametrize(
    (
        "report",
        "expected_mode",
        "expected_reason",
        "expected_pitch",
        "expected_throttle",
    ),
    [
        # Critical stall:
        # DecisionMaker chooses EMERGENCY.
        #
        # AutoPilot calculates stall-recovery pitch from:
        #
        #     flight_path_angle + recovery_target_aoa
        #
        # Fake flight path angle = -10 degrees
        # Default recovery target AoA = 4 degrees
        #
        # Therefore:
        #
        #     -10 + 4 = -6 degrees
        #
        # AutoPilot also commands full throttle.
        (
            FlightReport(
                speed_margin=20.0,
                aoa_margin=2.0,
                altitude=3000.0,
                time_to_stall=1.0,
                time_to_impact=60.0,
                most_urgent_threat=ThreatType.STALL,
                risk=RiskLevel.CRITICAL,
                recoverability=Recoverability.POOR,
                energy_state=EnergyState.LOW,
                horizontal_speed = 100.0,
                distance_travelled_m = 30_000.0,
            ),
            FlightMode.EMERGENCY,
            ThreatType.STALL,
            -6.0,
            1.0,
        ),

        # Critical impact:
        # DecisionMaker chooses EMERGENCY.
        # AutoPilot commands pitch-up and full throttle.
        (
            FlightReport(
                speed_margin=40.0,
                aoa_margin=10.0,
                altitude=100.0,
                time_to_stall=60.0,
                time_to_impact=1.0,
                most_urgent_threat=ThreatType.IMPACT,
                risk=RiskLevel.CRITICAL,
                recoverability=Recoverability.IMPOSSIBLE,
                energy_state=EnergyState.MODERATE,
                horizontal_speed = 100.0,
                distance_travelled_m = 30_000.0,
            ),
            FlightMode.EMERGENCY,
            ThreatType.IMPACT,
            5.0,
            1.0,
        ),
    ],
)
def test_emergency_decision_produces_correct_control_targets(
    report: FlightReport,
    expected_mode: FlightMode,
    expected_reason: ThreatType,
    expected_pitch: float,
    expected_throttle: float,
) -> None:
    # ============================================
    # Arrange
    # ============================================

    # DecisionMaker now requires a Mission.
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            planned_descent_speed_mps=5.0,
            landing_transition_altitude_m=300.0,
            )

    decision_maker = DecisionMaker(mission)

    autopilot = AutoPilot(mission=mission)

    # The fake plane gives AutoPilot only the information
    # required for this boundary test.
    plane = FakePlane(
        horizontal_speed=100.0,
        min_safe_speed=50.0,
        aoa=5.0,
        altitude=report.altitude,
        flight_path_angle_value=-10.0,
    )

    controller = FakeController()

    # ============================================
    # Act
    # ============================================

    # FlightReport -> DecisionMaker -> Decision
    decision = decision_maker.make_decision(report)

    # Decision -> AutoPilot -> Controller targets
    autopilot.update(
        plane,
        decision,
        controller,
    )

    # ============================================
    # Assert
    # ============================================

    # Assert the DecisionMaker output.
    assert decision.mode is expected_mode
    assert decision.reason is expected_reason
    assert decision.priority is RiskLevel.CRITICAL

    # Assert the AutoPilot translation.
    assert controller.target_pitch == pytest.approx(expected_pitch)

    assert controller.target_throttle == pytest.approx(
        expected_throttle
    )


# ============================================
# Test normal cruise altitude control
# ============================================


def test_cruise_decision_uses_normal_altitude_control() -> None:
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            planned_descent_speed_mps=5.0,
            landing_transition_altitude_m=300.0,
            )
    decision_maker = DecisionMaker(mission)

    # ============================================
    # Arrange
    # ============================================

    autopilot = AutoPilot(mission=mission, altitude_gain=0.01, max_pitch_command=5.0)
    report, plane = make_cruise_scenario(altitude=2000.0)
    controller = FakeController()

    # ============================================
    # Act
    # ============================================

    # FlightReport -> DecisionMaker -> Decision
    decision = decision_maker.make_decision(report)

    # Decision -> AutoPilot -> Controller targets
    autopilot.update(plane, decision, controller)

    # ============================================
    # Assert
    # ============================================

    # Assert the selected strategy.
    assert decision.mode is FlightMode.CRUISE
    assert decision.reason is ThreatType.NONE

    # altitude_error = 3000 - 2000 = 1000
    # raw command = 1000 * 0.01 = 10
    # clamped command = 5
    assert controller.target_pitch == pytest.approx(5.0)
    assert controller.target_throttle == pytest.approx(0.7)

