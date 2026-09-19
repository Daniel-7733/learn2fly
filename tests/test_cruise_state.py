from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.cruise_state import CruiseState
from flight_systems.decisions.states.descent_state import DescentState
from flight_systems.decisions.states.emergency_state import EmergencyState
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
    """Create a valid mission for CruiseState tests."""
    return Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=300.0,
    )


def make_safe_report(
    distance_travelled_m: float,
) -> FlightReport:
    """Create a safe cruise report at the requested route position."""
    return FlightReport(
        altitude=3000.0,
        horizontal_speed=100.0,
        distance_travelled_m=distance_travelled_m,
        speed_margin=50.0,
        aoa_margin=10.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )


def make_high_risk_stall_report(
    distance_travelled_m: float,
) -> FlightReport:
    """Create an unsafe cruise report at the requested route position."""
    return FlightReport(
        altitude=3000.0,
        horizontal_speed=100.0,
        distance_travelled_m=distance_travelled_m,
        speed_margin=10.0,
        aoa_margin=1.0,
        time_to_stall=3.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.STALL,
        risk=RiskLevel.HIGH,
        recoverability=Recoverability.GOOD,
        energy_state=EnergyState.LOW,
    )


def test_safe_cruise_remains_cruise_before_descent_boundary() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(CruiseState())

    # Remaining distance:
    # 100,000 - 30,000 = 70,000 m
    #
    # Required descent distance:
    # 3,000 / 5 × 100 = 60,000 m
    #
    # 70,000 > 60,000, so it is too early to descend.
    report = make_safe_report(
        distance_travelled_m=30_000.0,
    )

    # ---------------------------------------------------------
    # Act
    # ---------------------------------------------------------
    decision = decision_maker.make_decision(report)

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------
    assert decision.mode is FlightMode.CRUISE
    assert decision.reason is ThreatType.NONE
    assert decision.priority is RiskLevel.LOW
    assert isinstance(
        decision_maker.current_state,
        CruiseState,
    )


def test_safe_cruise_transitions_to_descent_at_descent_boundary() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(CruiseState())

    # Remaining distance:
    # 100,000 - 40,000 = 60,000 m
    #
    # Required descent distance:
    # 3,000 / 5 × 100 = 60,000 m
    #
    # The exact descent boundary has been reached.
    report = make_safe_report(
        distance_travelled_m=40_000.0,
    )

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


def test_unsafe_cruise_enters_emergency_at_descent_boundary() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(CruiseState())

    # The descent boundary has been reached, but safety has
    # higher priority than mission progress.
    report = make_high_risk_stall_report(
        distance_travelled_m=40_000.0,
    )

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
