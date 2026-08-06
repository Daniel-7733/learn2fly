from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flight_systems.flight_system import FlightSystem


class Simulation:
    """
    Manages simulated time and repeatedly updates the flight system.
    """

    def __init__(self, flight_system: "FlightSystem", time_step: float, max_simulation_time: float = 120.0,) -> None:
        if time_step <= 0:
            raise ValueError("time_step must be greater than zero.")

        if max_simulation_time <= 0:
            raise ValueError("max_simulation_time must be greater than zero.")

        self.flight_system = flight_system
        self.time_step = time_step
        self.max_simulation_time = max_simulation_time
        self.time_elapsed: float = 0.0
        self.is_running: bool = False

    def run(self) -> None:
        """Runs the simulation until the aircraft reaches the ground."""

        self.is_running = True

        while (self.is_running) and (self.time_elapsed < self.max_simulation_time):
            # Stop before performing another update when already grounded.
            if self.flight_system.plane.altitude <= 0:
                self.stop()
                break

            # One aircraft heartbeat.
            self.flight_system.update(self.time_step)

            # Total simulation time.
            self.time_elapsed += self.time_step

            self.display_status()

        if self.flight_system.plane.altitude <= 0:
            print("The plane has reached the ground.")
        else:
            print(
                "Simulation finished after "
                f"{self.time_elapsed:.1f} seconds."
            )

    def stop(self) -> None:
        """Stops the simulation."""
        self.is_running = False

    def display_status(self) -> None:
        """Displays telemetry and the analyzer's report."""
        print(self.flight_system.report())
        print(self.flight_system.decision())
        print(
            f"Time: {self.time_elapsed:.1f} s | "
            f"{self.flight_system.telemetry()}"
        )

        print("-" * 100)


