from flight_systems.decisions.decision import Decision
from flight_systems.enums import FlightMode, RiskLevel, ThreatType
from flight_systems.flight_report import FlightReport
from flight_systems.decisions.states.cruise_state import CruiseState
from flight_systems.decisions.states.flight_state import FlightState


class DecisionMaker:
    """
    Reads a FlightReport and manages flight-mode transitions.

    It remembers the current flight mode and returns a Decision.
    It does not move the aircraft or set controller targets.


    Important concept: state machine
    This design is the beginning of a finite-state machine.
                  HIGH / CRITICAL
           ┌─────────────────────────┐
           │                         ▼
       ┌────────┐                 ┌───────────┐
       │ CRUISE │                 │ EMERGENCY │
       └────────┘                 └───────────┘
           ▲                         │
           └─────────────────────────┘
                      LOW
    """

    def __init__(self) -> None:
        self.current_state: FlightState = CruiseState()

    def make_decision(self, report: FlightReport) -> Decision:
        """
        Selects a decision based on the current mode and flight report.
        """
        return self.current_state.handle(self, report)

    def change_state(self, new_state: FlightState) -> None:
        self.current_state = new_state

