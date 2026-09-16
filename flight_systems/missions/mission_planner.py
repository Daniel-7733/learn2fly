from math import isfinite

from flight_systems.missions.mission import Mission
from flight_systems.flight_calculator import FlightCalculator


class MissionPlanner:
    """Based on the current conditions, how much horizontal distance does the aircraft require to descend to the ground?"""

    def __init__(self, mission: Mission) -> None:
        self.mission = mission

    def distance_remaining(self, distance_travelled_m: float) -> float:
        if not isfinite(distance_travelled_m) or distance_travelled_m < 0.0:
            raise ValueError("distance_travelled_m must be finite and non-negative")

        return max(0.0, self.mission.route_distance - distance_travelled_m)

    def required_descent_distance(self, current_altitude_m: float, horizontal_speed_mps: float) -> float:

        descent_t = FlightCalculator.descent_time(current_altitude_m, self.mission.planned_descent_speed_mps)
        horizontal_d = FlightCalculator.horizontal_distance(horizontal_speed_mps, descent_t)
                                 
        return horizontal_d


    def should_begin_descent(self, distance_travelled_m: float, current_altitude_m: float,
                             current_horizontal_speed_mps: float) -> bool:
        """
        Responsibility:
            True  → descent should begin
            False → continue cruising
        """
        remaining_distance_m = self.distance_remaining(distance_travelled_m)
        required_distance_m = self.required_descent_distance(current_altitude_m,
                                                                     current_horizontal_speed_mps)

        if remaining_distance_m <= required_distance_m:
            return True
        return False

