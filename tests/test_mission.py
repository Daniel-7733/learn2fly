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
    )

    # Assert
    assert mission.target_altitude == 3000.0
    assert mission.cruise_speed == 100.0
    assert mission.route_distance == 100_000.0
    assert mission.landing_speed == 55.0

def test_mission_is_immutable() -> None:
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
    )

    with pytest.raises(AttributeError):
        mission.target_altitude = 4000.0  # type: ignore[misc]
