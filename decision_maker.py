class DecisionMaker:
    """
    The brain of the autonomous pilot.

    Reads the FlightReport.

    Chooses the best strategy.

    Sends targets to the controllers.

    DecisionMaker
            │
            ├── Reads FlightReport
            ├── Chooses Strategy
            └── Returns Commands

    Ex: 
    decision = decision_maker.make_decision(report)
    autopilot.execute(decision)
    """

    def __init__(self) -> None:
        pass


