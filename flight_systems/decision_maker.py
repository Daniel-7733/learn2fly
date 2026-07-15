class DecisionMaker:
    """
    Interprets the FlightReport and chooses the aircraft's behavior.

    Reads:
        FlightReport

    Returns:
        Decision

    It does not directly control the plane or FlightController.   

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


