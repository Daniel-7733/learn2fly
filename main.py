"""
            Measurement that I use in this program:
                Distance Measurement: m
                Mass Measurement: Kg
                Speed Measurement: m/s
                Acceleration Measurement: m/s^2
                Eneregy Measurement: J
                Force Measurement: N

            classes and there duties
                FlightCalculator:
                    Physics calculations & computes physics

                FlightReport:
                    Presentation

                MissionPlanner:
                    Goals

                FlightAnalyzer:
                    Interprets aircraft state and produces FlightReport

                DecisionMaker:
                    Selects flight mode and strategy

                AutoPilot:
                    Translates Decision into controller targets

                FlightController:
                    Smoothly moves controls toward targets

                Plane:
                    Stores aircraft state and updates physics
"""
from config import TIME_STEP

from flight_systems.missions.mission import Mission
from flight_systems.plane import Plane
from flight_systems.autopilot import AutoPilot
from flight_systems.flight_analyzer import FlightAnalyzer
from flight_systems.flight_controller import FlightController
from flight_systems.flight_system import FlightSystem
from flight_systems.decisions.decision_maker import DecisionMaker

from simulations.simulation import Simulation


def main() -> None:
    # ---------------------------------------------------------
    # 1. Create the aircraft
    # ---------------------------------------------------------

    plane = Plane(
        altitude=1200.0,
        horizontal_speed=85.0,
        pitch_angle=10.0,
        mass=20.0,
        max_thrust=100.0,
    )

    # ---------------------------------------------------------
    # 2. Create the aircraft specialists
    # ---------------------------------------------------------

    autopilot = AutoPilot()

    flight_controller = FlightController(
        target_pitch=plane.pitch_angle,
        target_throttle=plane.throttle,
        max_pitch_rate=2.0,
        max_throttle_rate=0.2,
    )

    flight_analyzer = FlightAnalyzer(
        plane,
        autopilot,
    )


    # ---------------------------------------------------------
    # 3. Create DecisionMaker
    # ---------------------------------------------------------
    mission = Mission(target_altitude=3000)
    decision_maker = DecisionMaker(mission)

    # ---------------------------------------------------------
    # 4. Connect them through FlightSystem
    # ---------------------------------------------------------

    flight_system = FlightSystem(
        plane=plane,
        autopilot=autopilot,
        flight_analyzer=flight_analyzer,
        flight_controller=flight_controller,
        decision_maker=decision_maker
    )

    # ---------------------------------------------------------
    # 4. Create and start the simulated world
    # ---------------------------------------------------------

    simulation = Simulation(
        flight_system=flight_system,
        time_step=TIME_STEP,
        max_simulation_time=300.0,
    )

    simulation.run()


if __name__ == "__main__":
    main()
