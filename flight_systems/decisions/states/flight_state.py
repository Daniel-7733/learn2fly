from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from flight_systems.decisions.decision import Decision
from flight_systems.flight_report import FlightReport

if TYPE_CHECKING:
    from flight_systems.decisions.decision_maker import DecisionMaker


class FlightState(ABC):

    @abstractmethod
    def handle(self, decision_maker: "DecisionMaker", report: FlightReport) -> Decision:
        raise NotImplementedError
    
