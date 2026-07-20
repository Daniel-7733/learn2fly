import pytest
from flight_systems.decision_maker import DecisionMaker
from flight_systems.flight_report import FlightReport
from flight_systems.enums import RiskLevel, ThreatType, FlightMode, Recoverability, EnergyState


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
    "report, expected_mode, expected_reason, expected_priority",
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
            FlightMode.CRUISE,
            ThreatType.NONE,
            RiskLevel.LOW,
        ),
    ],
)
def test_make_decision(report: FlightReport, expected_mode: FlightMode, expected_reason: ThreatType, expected_priority: RiskLevel) -> None:
    decision_maker = DecisionMaker()
    decision = decision_maker.make_decision(report)

    assert decision.mode is expected_mode
    assert decision.reason is expected_reason
    assert decision.priority is expected_priority

