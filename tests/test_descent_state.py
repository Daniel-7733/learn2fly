import pytest
from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.descent_state import DescentState
from flight_systems.decisions.states.emergency_state import EmergencyState
from flight_systems.decisions.states.landing_state import LandingState
from flight_systems.enums import (
    EnergyState,
    FlightMode,
    Recoverability,
    RiskLevel,
    ThreatType,
)
from flight_systems.flight_report import FlightReport
from flight_systems.missions.mission import Mission


def make_mission() -> Mission:
    """Create a valid mission for DescentState tests."""
    return Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=300.0,
    )


def make_safe_report(altitude: float) -> FlightReport:
    """Create a safe flight report at the requested altitude."""
    return FlightReport(
        altitude=altitude,
        horizontal_speed=100.0,
        distance_travelled_m=30_000.0,
        speed_margin=50.0,
        aoa_margin=10.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )


def make_high_risk_stall_report(altitude: float) -> FlightReport:
    """Create an unsafe report representing a stall threat."""
    return FlightReport(
        altitude=altitude,
        horizontal_speed=100.0,
        distance_travelled_m=30_000.0,
        speed_margin=10.0,
        aoa_margin=1.0,
        time_to_stall=3.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.STALL,
        risk=RiskLevel.HIGH,
        recoverability=Recoverability.GOOD,
        energy_state=EnergyState.LOW,
    )


def test_safe_descent_continues_above_landing_transition_altitude() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = make_mission()
    decision_maker = DecisionMaker(mission)

    # DecisionMaker currently begins in CruiseState,
    # so explicitly place it into DescentState.
    decision_maker.change_state(DescentState())

    # Mission transition altitude is 300 m.
    # At 301 m, descent should continue.
    report = make_safe_report(altitude=301.0)

    # ---------------------------------------------------------
    # Act
    # ---------------------------------------------------------
    decision = decision_maker.make_decision(report)

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------
    assert decision.mode is FlightMode.DESCENT
    assert decision.reason is ThreatType.NONE
    assert decision.priority is RiskLevel.LOW
    assert isinstance(
        decision_maker.current_state,
        DescentState,
    )


def test_unsafe_descent_enters_emergency_even_below_landing_transition_altitude() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(DescentState())

    # The aircraft is below the 300 m landing boundary,
    # but safety must still have the highest priority.
    report = make_high_risk_stall_report(altitude=200.0)

    # ---------------------------------------------------------
    # Act
    # ---------------------------------------------------------
    decision = decision_maker.make_decision(report)

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------
    assert decision.mode is FlightMode.EMERGENCY
    assert decision.reason is ThreatType.STALL
    assert decision.priority is RiskLevel.HIGH
    assert isinstance(
        decision_maker.current_state,
        EmergencyState,
    )

@pytest.mark.parametrize(
    "altitude",
    [
        300.0,  # Exact landing-transition boundary
        299.0,  # Below the landing-transition boundary
    ],
)
def test_safe_descent_transitions_to_landing_at_or_below_boundary(altitude: float) -> None:
    # Arrange
    mission = make_mission()
    decision_maker = DecisionMaker(mission)

    # We are testing the transition FROM DescentState.
    decision_maker.change_state(DescentState())

    report = make_safe_report(altitude=altitude)

    # Act
    decision = decision_maker.make_decision(report)

    # Assert
    assert decision.mode is FlightMode.LANDING
    assert decision.reason is ThreatType.NONE
    assert decision.priority is RiskLevel.LOW
    assert isinstance(
        decision_maker.current_state,
        LandingState,
    )
