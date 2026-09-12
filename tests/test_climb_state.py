from flight_systems.missions.mission import Mission
from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.cruise_state import CruiseState
from flight_systems.decisions.states.climb_state import ClimbState
from flight_systems.flight_report import FlightReport
from flight_systems.enums import FlightMode, RiskLevel, ThreatType, Recoverability, EnergyState


def make_safe_report(altitude: float) -> FlightReport:
    return FlightReport(
        altitude=altitude,
        speed_margin=50.0,
        aoa_margin=10.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )


def test_climb_continues_below_completion_altitude() -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
    )

    decision_maker = DecisionMaker(mission)

    # DecisionMaker currently begins in CruiseState,
    # so place it explicitly into ClimbState for this unit test.
    decision_maker.change_state(ClimbState(altitude_tolerance=50.0))

    report = make_safe_report(altitude=2949.9)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.CLIMB
    assert isinstance(decision_maker.current_state, ClimbState)


def test_climb_transitions_to_cruise_at_completion_boundary() -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
    )

    decision_maker = DecisionMaker(mission)

    # DecisionMaker currently begins in CruiseState,
    # so place it explicitly into ClimbState for this unit test.
    decision_maker.change_state(ClimbState(altitude_tolerance=50.0))

    report = make_safe_report(altitude=2950.0)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.CRUISE
    assert isinstance(decision_maker.current_state, CruiseState)

