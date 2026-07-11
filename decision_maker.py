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

    Just for example than we can use something like this to make decision.

    mode = decision_maker.current_code()

    match mode:
        case TAKEOFF:
            ... 
        case CLIMB:
            ...
        case CRUISE:
            ...
        case DESCENT:
            ...
        case LANDING:
            ...
        case EMERGENCY:
            ...

    So in another word, DecisionMaker "Given my current state, what behavior should I have?"

    """

    def __init__(self) -> None:
        pass


