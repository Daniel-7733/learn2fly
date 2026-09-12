import pytest
from flight_systems.decisions.decision_maker import DecisionMaker
from flight_systems.decisions.states.cruise_state import CruiseState
from flight_systems.decisions.states.emergency_state import EmergencyState
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import (
    EnergyState,
    FlightMode,
    Recoverability,
    RiskLevel,
    ThreatType,
)
from flight_systems.flight_report import FlightReport
from flight_systems.missions.mission import Mission

# ==================================================================
#                 How to use pytest
# inside the neovime: (4 ways) 
#  1. This will likely work immediately:
#                :!python3 -m pytest %
#  2. Run the current test file:
#                :!python3 -m pytest -v %
#  3. Run the entire test suite:
#                :!python3 -m pytest -v
#  4. Run only the test under a specific name:
#                :!python3 -m pytest -v % -k test_make_decision
#
# in the terminal (2 ways):       
#                1. python3 -m pytest tests/test_decision_maker.py
#                2. PYTHONPATH=. pytest tests/test_decision_maker.py
# ==================================================================

@pytest.mark.parametrize(
    (
        "report",
        "expected_state_type",
        "expected_mode",
        "expected_reason",
        "expected_priority",
    ),
    [
        # ==================================
        #     Critical predicted stall
        # ==================================

        (
            FlightReport(
                speed_margin=10.0,
                aoa_margin=3.0,
                altitude=5000.0,
                time_to_stall=1.5,
                time_to_impact=30.0,
                most_urgent_threat=ThreatType.STALL,
                risk=RiskLevel.CRITICAL,
                recoverability=Recoverability.POOR,
                energy_state=EnergyState.LOW,
            ),
            EmergencyState,
            FlightMode.EMERGENCY,
            ThreatType.STALL,
            RiskLevel.CRITICAL,
        ),

        # ==================================
        #     Critical predicted impact
        # ==================================

        (
            FlightReport(
                speed_margin=15.0,
                aoa_margin=8.0,
                altitude=200.0,
                time_to_stall=99.0,
                time_to_impact=1.5,
                most_urgent_threat=ThreatType.IMPACT,
                risk=RiskLevel.CRITICAL,
                recoverability=Recoverability.IMPOSSIBLE,
                energy_state=EnergyState.MODERATE,
            ),
            EmergencyState,
            FlightMode.EMERGENCY,
            ThreatType.IMPACT,
            RiskLevel.CRITICAL,
        ),

        # ==================================
        #      Normal low-risk flight
        # ==================================

        (
            FlightReport(
                speed_margin=50.0,
                aoa_margin=10.0,
                altitude=3000.0,
                time_to_stall=99.0,
                time_to_impact=99.0,
                most_urgent_threat=ThreatType.NONE,
                risk=RiskLevel.LOW,
                recoverability=Recoverability.EXCELLENT,
                energy_state=EnergyState.HIGH,
            ),
            CruiseState,
            FlightMode.CRUISE,
            ThreatType.NONE,
            RiskLevel.LOW,
        ),
    ],
)
def test_make_decision(report: FlightReport, expected_state_type: type[FlightState], expected_mode: FlightMode, 
                       expected_reason: ThreatType, expected_priority: RiskLevel) -> None:
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            )
    decision_maker = DecisionMaker(mission)

    decision = decision_maker.make_decision(report)

    assert isinstance(
        decision_maker.current_state,
        expected_state_type,
    )
    assert decision.mode is expected_mode
    assert decision.reason is expected_reason
    assert decision.priority is expected_priority

def test_cruise_to_emergency_and_back_to_cruise() -> None:
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            )
    decision_maker = DecisionMaker(mission)

    critical_report = FlightReport(
        speed_margin=10.0,
        aoa_margin=3.0,
        altitude=5000.0,
        time_to_stall=1.5,
        time_to_impact=30.0,
        most_urgent_threat=ThreatType.STALL,
        risk=RiskLevel.CRITICAL,
        recoverability=Recoverability.POOR,
        energy_state=EnergyState.LOW,
    )

    safe_report = FlightReport(
        speed_margin=50.0,
        aoa_margin=10.0,
        altitude=3000.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )

    # The DecisionMaker begins in cruise.
    assert isinstance(decision_maker.current_state, CruiseState)

    # Critical danger changes CruiseState into EmergencyState.
    emergency_decision = decision_maker.make_decision(critical_report)

    assert isinstance(decision_maker.current_state, EmergencyState)
    assert emergency_decision.mode is FlightMode.EMERGENCY


# First safe update: remain in EmergencyState.
    first_safe_decision = decision_maker.make_decision(safe_report)

    assert isinstance(decision_maker.current_state, EmergencyState)
    assert first_safe_decision.mode is FlightMode.EMERGENCY


# Second safe update: still remain in EmergencyState.
    second_safe_decision = decision_maker.make_decision(safe_report)

    assert isinstance(decision_maker.current_state, EmergencyState)
    assert second_safe_decision.mode is FlightMode.EMERGENCY


# Third consecutive safe update: recovery is confirmed.
    third_safe_decision = decision_maker.make_decision(safe_report)

    assert isinstance(decision_maker.current_state, CruiseState)
    assert third_safe_decision.mode is FlightMode.CRUISE

def test_emergency_requires_consecutive_safe_updates() -> None:
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            )
    decision_maker = DecisionMaker(mission)

    critical_report = FlightReport(
        speed_margin=10.0,
        aoa_margin=3.0,
        altitude=5000.0,
        time_to_stall=1.5,
        time_to_impact=30.0,
        most_urgent_threat=ThreatType.STALL,
        risk=RiskLevel.CRITICAL,
        recoverability=Recoverability.POOR,
        energy_state=EnergyState.LOW,
    )

    safe_report = FlightReport(
        speed_margin=50.0,
        aoa_margin=10.0,
        altitude=3000.0,
        time_to_stall=99.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.LOW,
        recoverability=Recoverability.EXCELLENT,
        energy_state=EnergyState.HIGH,
    )

    moderate_report = FlightReport(
        speed_margin=30.0,
        aoa_margin=8.0,
        altitude=3000.0,
        time_to_stall=20.0,
        time_to_impact=99.0,
        most_urgent_threat=ThreatType.NONE,
        risk=RiskLevel.MODERATE,
        recoverability=Recoverability.GOOD,
        energy_state=EnergyState.MODERATE,
    )

    # Enter EmergencyState.
    decision_maker.make_decision(critical_report)

    assert isinstance(decision_maker.current_state, EmergencyState)

    # LOW #1
    decision = decision_maker.make_decision(safe_report)
    assert decision.mode is FlightMode.EMERGENCY

    # LOW #2
    decision = decision_maker.make_decision(safe_report)
    assert decision.mode is FlightMode.EMERGENCY

    # MODERATE interrupts recovery and resets the counter.
    decision = decision_maker.make_decision(moderate_report)
    assert decision.mode is FlightMode.EMERGENCY

    # LOW #1 again
    decision = decision_maker.make_decision(safe_report)
    assert decision.mode is FlightMode.EMERGENCY

    # LOW #2
    decision = decision_maker.make_decision(safe_report)
    assert decision.mode is FlightMode.EMERGENCY

    # LOW #3 → recovery confirmed.
    decision = decision_maker.make_decision(safe_report)

    assert decision.mode is FlightMode.CRUISE
    assert isinstance(decision_maker.current_state, CruiseState)
