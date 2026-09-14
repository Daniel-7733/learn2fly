import pytest

from flight_systems.missions.mission import Mission
from flight_systems.missions.mission_planner import MissionPlanner


@pytest.mark.parametrize(
    ("distance_travelled_m", "expected_remaining_m"),
    [
        (0.0, 100_000.0),       # At the start
        (60_000.0, 40_000.0),  # Partway through
        (100_500.0, 0.0),      # Past the destination
    ],
)
def test_distance_remaining(distance_travelled_m: float, expected_remaining_m: float) -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
    )
    planner = MissionPlanner(mission)

    remaining_m = planner.distance_remaining(distance_travelled_m)

    assert remaining_m == pytest.approx(expected_remaining_m)
