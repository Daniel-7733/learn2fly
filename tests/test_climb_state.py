from flight_systems.missions.mission import Mission
from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.cruise_state import CruiseState
from flight_systems.decisions.states.climb_state import ClimbState
from flight_systems.decisions.states.emergency_state import EmergencyState
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
        horizontal_speed = 100.0,
        distance_travelled_m = 30_000.0,
    )


def make_high_risk_stall_report(altitude: float) -> FlightReport:
    return FlightReport(
            altitude=altitude,
            speed_margin=10.0,
            aoa_margin=1.0,
            time_to_stall=3.0,
            time_to_impact=99.0,
            most_urgent_threat=ThreatType.STALL,
            risk=RiskLevel.HIGH,
            recoverability=Recoverability.GOOD,
            energy_state=EnergyState.LOW,
            horizontal_speed = 100.0,
            distance_travelled_m = 30_000.0,
            )


def test_climb_continues_below_completion_altitude() -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=0.5,
        landing_transition_altitude_m=2000.0,
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
        planned_descent_speed_mps=0.5,
        landing_transition_altitude_m=2000.0,
    )

    decision_maker = DecisionMaker(mission)

    # DecisionMaker currently begins in CruiseState,
    # so place it explicitly into ClimbState for this unit test.
    decision_maker.change_state(ClimbState(altitude_tolerance=50.0))

    report = make_safe_report(altitude=2950.0)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.CRUISE
    assert isinstance(decision_maker.current_state, CruiseState)


def test_unsafe_climb_enters_emergency_despite_reaching_mission_altitude() -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=0.5,
        landing_transition_altitude_m=2000.0,
    )

    decision_maker = DecisionMaker(mission)
    decision_maker.change_state(ClimbState(altitude_tolerance=50.0))
    report = make_high_risk_stall_report(3000.0)
    decision = decision_maker.make_decision(report)

    assert decision.mode is FlightMode.EMERGENCY
    assert decision.reason is ThreatType.STALL
    assert decision.priority is RiskLevel.HIGH
    assert isinstance(decision_maker.current_state, EmergencyState)


def test_climb_decision_depends_on_mission_target() -> None:
    higher_mission = Mission(
        target_altitude=3500.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=0.5,
        landing_transition_altitude_m=2000.0,
    )

    higher_decision_maker = DecisionMaker(higher_mission)
    higher_decision_maker.change_state(ClimbState(altitude_tolerance=50.0))

    # Reuse the SAME safe report: aircraft altitude is still 3000.0 m.
    report = make_safe_report(altitude=3000.0)
    higher_decision = higher_decision_maker.make_decision(report)

    assert higher_decision.mode is FlightMode.CLIMB
    assert isinstance(higher_decision_maker.current_state, ClimbState)

