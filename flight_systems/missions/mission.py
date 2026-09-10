from dataclasses import dataclass

"""
Our model

    Mission
       │
       ▼
    DecisionMaker
       │
       ├── owns current_state
       └── owns mission
                │
                ▼
           ClimbState
                │
                ▼
             Decision
                │
                ▼
             AutoPilot
                │
                ▼
         FlightController
"""
@dataclass(frozen=True)
class Mission:
    target_altitude: float

