from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.landing_state import LandingState
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
    """Create a valid mission for LandingState tests."""
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

def test_safe_landing() -> None:
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(LandingState())
    report = make_safe_report(altitude=300.0)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.LANDING
    assert decision.reason is ThreatType.NONE
    assert decision.priority is RiskLevel.LOW
    assert isinstance(
        decision_maker.current_state,
        LandingState,
    )


def test_unsafe_landing() -> None:
    mission = make_mission()
    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(LandingState())
    report = make_high_risk_stall_report(altitude=200.0)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.EMERGENCY
    assert decision.reason is ThreatType.STALL
    assert decision.priority is RiskLevel.HIGH
    assert isinstance(decision_maker.current_state, EmergencyState)

