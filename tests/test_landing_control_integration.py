import pytest
from flight_systems.plane import Plane
from flight_systems.missions.mission import Mission
from flight_systems.autopilot import AutoPilot
from flight_systems.flight_controller import FlightController
from flight_systems.decisions.decision import Decision
from flight_systems.enums import FlightMode, RiskLevel, ThreatType


# @pytest.mark.parametrize(
#     "landing_speed",
#     [55.0, 60.0, 65.0, 70.0],
# )
def test_successful_landing():

    """
    LANDING Decision
          ↓
    AutoPilot chooses pitch and throttle targets
          ↓
    FlightController gradually applies those targets
          ↓
    Plane physics updates altitude and speed
          ↓
    Repeat
    """
    dt = 0.1
    steps = 300


    mission = Mission(
            target_altitude=3000.0,
            cruise_speed=100.0,
            route_distance=100_000.0,
            landing_speed=70.0,
            planned_descent_speed_mps=5.0,
            landing_transition_altitude_m=300.0,
            )

    plane = Plane(
        altitude=300.0,
        horizontal_speed=75.0,
        pitch_angle=0.0,
        mass=20.0,
    )

    initial_altitude = plane.altitude
    initial_horizontal_speed = plane.horizontal_speed

    autopilot = AutoPilot(mission)

    decision = Decision(
        mode=FlightMode.LANDING,
        priority=RiskLevel.LOW,
        reason=ThreatType.NONE,
        message="Landing integration test.",
        confidence=1.0,
    )
    controller = FlightController()

    for _ in range(steps):
        autopilot.update(plane, decision, controller)
        controller.update_pitch(plane, dt)
        controller.update_throttle(plane, dt)
        plane.update_physics(-9.81, dt)

    print(
        "\nFinal landing state:"
        f"\n  altitude:          {plane.altitude:.2f} m"
        f"\n  horizontal speed:  {plane.horizontal_speed:.2f} m/s"
        f"\n  vertical speed:    {plane.vertical_speed:.2f} m/s"
        f"\n  pitch angle:       {plane.pitch_angle:.2f} deg"
        f"\n  target pitch:      {controller.target_pitch:.2f} deg"
        f"\n  AoA:               {plane.aoa:.2f} deg"
        f"\n  throttle:          {plane.throttle:.2f}"
        f"\n  target throttle:   {controller.target_throttle:.2f}"
    )

    assert plane.altitude < initial_altitude
    assert plane.vertical_speed < 0.0
    assert plane.altitude > 0.0
    assert plane.horizontal_speed < initial_horizontal_speed

    assert plane.horizontal_speed == pytest.approx(
        mission.landing_speed,
        abs=5.0,
    )

    assert plane.vertical_speed == pytest.approx(
        -autopilot.landing_vertical_speed_mps,
        abs=0.5,
    )

    assert plane.aoa <= autopilot.max_safe_aoa

