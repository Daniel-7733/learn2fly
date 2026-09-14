from math import isfinite

from flight_systems.missions.mission import Mission


class MissionPlanner:
    def __init__(self, mission: Mission) -> None:
        self.mission = mission

    def distance_remaining(self, distance_travelled_m: float) -> float:
        if not isfinite(distance_travelled_m) or distance_travelled_m < 0.0:
            raise ValueError("distance_travelled_m must be finite and non-negative")

        return max(0.0, self.mission.route_distance - distance_travelled_m)

