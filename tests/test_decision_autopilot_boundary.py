from dataclasses import dataclass

import pytest

from flight_systems.autopilot import AutoPilot
from flight_systems.decision_maker import DecisionMaker
from flight_systems.enums import (
    EnergyState,
    FlightMode,
    Recoverability,
    RiskLevel,
    ThreatType,
)
from flight_systems.flight_report import FlightReport

# ============================================
#     Initializing some fake classes
# ============================================

@dataclass
class FakePlane:
    """
    Provides only the Plane attributes AutoPilot needs.

    Physics is intentionally excluded from this test.
    """

    horizontal_speed: float
    min_safe_speed: float
    aoa: float
    altitude: float


@dataclass
class FakeController:
    """
    Receives the targets selected by AutoPilot.
    """

    target_pitch: float = 0.0
    target_throttle: float = 0.0


# ============================================
#           Test the functions
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
        # AutoPilot commands nose-down and full throttle.
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
            ),
            FlightMode.EMERGENCY,
            ThreatType.STALL,
            -5.0,
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
    # Arrange
    decision_maker = DecisionMaker()
    autopilot = AutoPilot()

    plane = FakePlane(
        horizontal_speed=100.0,
        min_safe_speed=50.0,
        aoa=5.0,
        altitude=3000.0,
    )

    controller = FakeController()

    # Act: FlightReport -> DecisionMaker -> Decision
    decision = decision_maker.make_decision(report)

    # Act: Decision -> AutoPilot -> Controller targets
    autopilot.update(
        plane,
        decision,
        controller,
    )

    # Assert the DecisionMaker output
    assert decision.mode is expected_mode
    assert decision.reason is expected_reason
    assert decision.priority is RiskLevel.CRITICAL

    # Assert the AutoPilot translation
    assert controller.target_pitch == pytest.approx(expected_pitch)
    assert controller.target_throttle == pytest.approx(
        expected_throttle
    )



def test_cruise_decision_uses_normal_altitude_control() -> None:
    # Arrange
    report = FlightReport(
        speed_margin=50.0,
        aoa_margin=10.0,
        altitude=2000.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )

    decision_maker = DecisionMaker()

    autopilot = AutoPilot(
        target_altitude=3000.0,
        altitude_gain=0.01,
        max_pitch_command=5.0,
    )

    plane = FakePlane(
        horizontal_speed=100.0,
        min_safe_speed=50.0,
        aoa=5.0,
        altitude=2000.0,
    )

    controller = FakeController()

    # Act
    decision = decision_maker.make_decision(report)

    autopilot.update(
        plane,
        decision,
        controller,
    )

    # Assert the selected strategy
    assert decision.mode is FlightMode.CRUISE
    assert decision.reason is ThreatType.NONE

    # altitude_error = 3000 - 2000 = 1000
    # raw command = 1000 * 0.01 = 10
    # clamped command = 5
    assert controller.target_pitch == pytest.approx(5.0)
    assert controller.target_throttle == pytest.approx(0.7)

