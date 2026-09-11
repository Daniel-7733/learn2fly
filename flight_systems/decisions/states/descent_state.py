from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.decisions.states.flight_state import FlightState
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class DescentState(FlightState):
    def __init__(self) -> None:
        print("DescentState class isn't made yet")
