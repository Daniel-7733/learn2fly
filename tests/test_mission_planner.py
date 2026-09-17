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
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=2000.0,
    )
    planner = MissionPlanner(mission)
    remaining_m = planner.distance_remaining(distance_travelled_m)

    assert remaining_m == pytest.approx(expected_remaining_m)



@pytest.mark.parametrize(
    ("planned_descent_speed", "expected_horizontal_distance"),
    [
        (5.0, 60_000.0),       # Normal planned descent
        (10.0, 30_000.0),      # Twice the descent speed, half the distance
        (2.5, 120_000.0),      # Half the descent speed, twice the distance
        (3.3333, 90_000.9),    # Fractional descent speed
        (100.0, 3_000.0),      # Very fast descent: 30 seconds
    ],
)
def test_required_descent_distance(planned_descent_speed: float, expected_horizontal_distance: float) -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=planned_descent_speed,
        landing_transition_altitude_m=2000.0,
    )

    planner = MissionPlanner(mission)
    horizontal_distance = planner.required_descent_distance(3000.0, 100.0)
    # Using pytest.approx is highly recommended for floating-point math to prevent rounding failures
    assert horizontal_distance == pytest.approx(expected_horizontal_distance, rel=1e-6)



@pytest.mark.parametrize(
    ("distance_travelled_m", "expected_result"),
    [
        (30_000.0, False),   # continue cruise
        (40_000.0, True),    # exact descent boundary
        (60_000.0, True),    # descent is already required
    ],
)
def test_should_begin_descent(distance_travelled_m: float, expected_result: bool) -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=2000.0,
    )
    
    planner = MissionPlanner(mission)
    is_descent = planner.should_begin_descent(distance_travelled_m, 3000.0, 100.0)

    assert is_descent is expected_result

