"""
All values remain in SI units: 
use base units internally. Learn2Fly should continue using SI units.
    
    =====================================
            Inside the program:
    =====================================
    Measurement    |    Internal unit
    -------------------------------------
    Distance       |    metres
    Altitude       |    metres
    Speed          |    metres per second
    Time           |    seconds
    Mass           |    kilograms
    Force          |    newtons
    Angle          |    degrees currently
    -------------------------------------

    Example:
        mission = Mission(
            target_altitude=3000.0,   # metres              | Climb to 3,000 m
            cruise_speed=100.0,       # metres per second   | Cruise at 100 m/s
            route_distance=100_000.0, # metres              | Travel a total route of 100 km
            landing_speed=55.0,       # metres per second   | Approach landing at 55 m/s
        )
        
        OR

        Mission(
            target_altitude=3000.0,
            cruise_speed=float("inf"),
            route_distance=100_000.0,
            landing_speed=55.0,
        )
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Mission:
    target_altitude: float    # → Climb/Cruise goal
    cruise_speed: float       # → Cruise goal
    route_distance: float     # → Determines mission progress
    landing_speed: float      # → Landing goal
    planned_descent_speed_mps: float

    def __post_init__(self) -> None:
        if not isfinite(self.target_altitude) or self.target_altitude <= 0:
            raise ValueError("target_altitude must be finite and greater than zero")

        if not isfinite(self.cruise_speed) or self.cruise_speed <= 0:
            raise ValueError("cruise_speed must be finite and greater than zero")

        if not isfinite(self.route_distance) or self.route_distance <= 0:
            raise ValueError("route_distance must be finite and greater than zero")

        if not isfinite(self.landing_speed) or self.landing_speed <= 0:
            raise ValueError("landing_speed must be finite and greater than zero")
        
        if not isfinite(self.planned_descent_speed_mps) or self.planned_descent_speed_mps <= 0:
            raise ValueError("planned_descent_speed_mps must be finite and greater than zero")

