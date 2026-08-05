from flight_systems.plane import Plane
import pytest


def test_drag_at_cruise_condition() -> None:
    plane = Plane(
        altitude=3000.0,
        horizontal_speed=100.0,
        pitch_angle=5.0,
        mass=20.0,
        max_thrust=100.0,
    )
    plane.aoa = 5.0

    assert plane.calculate_drag() == pytest.approx(50.0)


def test_half_throttle_maintains_cruise_speed() -> None:
    plane = Plane(
        altitude=3000.0,
        horizontal_speed=100.0,
        pitch_angle=5.0,
        mass=20.0,
        max_thrust=100.0,
    )
    plane.aoa = 5.0
    plane.throttle = 0.5

    plane.calculate_horizontal_speed(dt=1.0)

    assert plane.thrust == pytest.approx(50.0)
    assert plane.drag == pytest.approx(50.0)
    assert plane.horizontal_speed == pytest.approx(100.0)

