import pytest

from config import GRAVITY
from flight_systems.autopilot import AutoPilot
from flight_systems.decisions.decision import Decision
from flight_systems.enums import (
    FlightMode,
    RiskLevel,
    ThreatType,
)
from flight_systems.flight_controller import FlightController
from flight_systems.missions.mission import Mission
from flight_systems.plane import Plane


def test_descent_control_reduces_altitude_and_tracks_descent_speed() -> None:
    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------
    mission = Mission(
        target_altitude=3000.0,
        cruise_speed=100.0,
        route_distance=100_000.0,
        landing_speed=55.0,
        planned_descent_speed_mps=5.0,
        landing_transition_altitude_m=300.0,
    )

    plane = Plane(
        altitude=3000.0,
        horizontal_speed=100.0,
        pitch_angle=0.0,
        mass=20.0,
        max_thrust=100.0,
    )

    autopilot = AutoPilot(
        mission=mission,
        descent_vertical_speed_gain=1.0,
    )

    controller = FlightController(
        target_pitch=plane.pitch_angle,
        target_throttle=plane.throttle,
        max_pitch_rate=2.0,
        max_throttle_rate=0.2,
    )

    # Keep the decision fixed in DESCENT.
    # This test focuses on control and physics, not state transitions.
    decision = Decision(
        mode=FlightMode.DESCENT,
        priority=RiskLevel.LOW,
        reason=ThreatType.NONE,
        message="Continue descent.",
        confidence=1.0,
    )

    initial_altitude = plane.altitude

    dt = 0.1
    number_of_steps = 300  # 30 simulated seconds

    # ---------------------------------------------------------
    # Act
    # ---------------------------------------------------------
    for _ in range(number_of_steps):
        # AutoPilot translates the DESCENT decision
        # into pitch and throttle targets.
        autopilot.update(
            plane,
            decision,
            controller,
        )

        # FlightController moves the physical controls smoothly.
        controller.update_pitch(plane, dt)
        controller.update_throttle(plane, dt)

        # Plane physics responds to the changed controls.
        plane.update_physics(GRAVITY, dt)

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------

    # The aircraft physically lost altitude.
    assert plane.altitude < initial_altitude

    # Negative vertical speed means descending.
    assert plane.vertical_speed < 0.0

    # The closed loop should settle near the mission target:
    # mission magnitude = +5 m/s
    # physical downward velocity = approximately -5 m/s
    assert plane.vertical_speed == pytest.approx(
        -mission.planned_descent_speed_mps,
        abs=1.0,
    )

    # Descent control must not allow the aircraft to become
    # slower than its minimum safe horizontal speed.
    assert plane.horizontal_speed > plane.min_safe_speed

    # The aircraft also progressed along the route.
    assert plane.distance_travelled_m > 0.0


