from math import inf, nan

import pytest

from flight_systems.missions.mission import Mission

@pytest.mark.parametrize(
    "field_name",
    [
        "target_altitude",
        "cruise_speed",
        "route_distance",
        "landing_speed",
        "planned_descent_speed_mps",

    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        0.0,
        -1.0,
        inf,
        -inf,
        nan,
    ],
)
def test_mission_rejects_invalid_values(
    field_name: str,
    invalid_value: float,
) -> None:
    # Begin with a completely valid mission.
    mission_values: dict[str, float] = {
        "target_altitude": 3000.0,
        "cruise_speed": 100.0,
        "route_distance": 100_000.0,
        "landing_speed": 55.0,
        "planned_descent_speed_mps": 10.0,
        "landing_transition_altitude_m": 3000.0,
    }

    # Replace only the field currently being tested.
    mission_values[field_name] = invalid_value

    # The error message should identify the invalid field.
    with pytest.raises(ValueError, match=field_name):
        Mission(**mission_values)


def test_mission_accepts_valid_values() -> None:
    # Arrange and Act
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=2000.0,
    )

    # Assert
    assert mission.target_altitude == 3000.0
    assert mission.cruise_speed == 100.0
    assert mission.route_distance == 100_000.0
    assert mission.landing_speed == 55.0
    assert mission.planned_descent_speed_mps == 5.0
    assert mission.landing_transition_altitude_m == 2000.0

def test_mission_is_immutable() -> None:
    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            planned_descent_speed_mps=5.0,
            landing_transition_altitude_m=2000.0,
        )

    with pytest.raises(AttributeError):
        mission.target_altitude = 4000.0  # type: ignore[misc]

@pytest.mark.parametrize(
    "landing_transition_altitude_m",
    [
        3000.0,  # Equal to target altitude
        3500.0,  # Above target altitude
    ],
)
def test_mission_rejects_invalid_landing_transition_relationship(
    landing_transition_altitude_m: float,
) -> None:
    with pytest.raises(ValueError, match="landing_transition_altitude_m"):
        Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=55.0,
            planned_descent_speed_mps=5.0,
            landing_transition_altitude_m=(landing_transition_altitude_m),
        )

