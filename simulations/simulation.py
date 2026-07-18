from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flight_systems.flight_system import FlightSystem


class Simulation:
    """
    Manages simulated time and repeatedly updates the flight system.
    """

    def __init__(self, flight_system: "FlightSystem", time_step: float) -> None:
        if time_step <= 0:
            raise ValueError("time_step must be greater than zero.")

        self.flight_system = flight_system
        self.time_step = time_step
        self.time_elapsed: float = 0.0
        self.is_running: bool = False

    def run(self) -> None:
        """Runs the simulation until the aircraft reaches the ground."""

        self.is_running = True

        while self.is_running:
            # Stop before performing another update when already grounded.
            if self.flight_system.plane.altitude <= 0:
                self.stop()
                break

            # One aircraft heartbeat.
            self.flight_system.update(self.time_step)

            # Total simulation time.
            self.time_elapsed += self.time_step

            self.display_status()

        print("The plane has reached the ground.")

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

        print(self.flight_system.report())
        print("-" * 100)


