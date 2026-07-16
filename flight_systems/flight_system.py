from typing import TYPE_CHECKING

from config import GRAVITY
from .flight_calculator import FlightCalculator

if TYPE_CHECKING:
    from .plane import Plane
    from .autopilot import AutoPilot
    from .flight_report import FlightReport
    from .decision_maker import DecisionMaker
    from .flight_analyzer import FlightAnalyzer
    from .flight_controller import FlightController


class FlightSystem:
    """
    Coordinates the aircraft's internal systems.

    One call to update(dt) advances the aircraft by one time step.
    """

    def __init__(self, plane: "Plane", autopilot: "AutoPilot", flight_analyzer: "FlightAnalyzer", flight_controller: "FlightController", decision_maker: "DecisionMaker") -> None:
        self.plane = plane
        self.autopilot = autopilot
        self.flight_analyzer = flight_analyzer
        self.flight_controller = flight_controller
        self.decision_maker = decision_maker

        initial_total_speed = FlightCalculator.total_speed(
            self.plane.horizontal_speed,
            self.plane.vertical_speed,
        )

        self.current_energy = FlightCalculator.total_energy(
            self.plane.mass,
            GRAVITY,
            self.plane.altitude,
            initial_total_speed,
        )

        self.energy_rate: float = 0.0

    def update(self, dt: float) -> None:
        """
        Advances the complete flight system by one time step.

        Order:
        1. Save previous values.
        2. Analyze and choose control targets.
        3. Apply controller movement.
        4. Update aircraft physics.
        5. Recalculate derived flight values.
        """

        if dt <= 0:
            raise ValueError("dt must be greater than zero.")
        # ---------------------------------------------------------
        # 1. Create the report before the autopilot acts
        # ---------------------------------------------------------

        report = self.flight_analyzer.report()
        decision = self.decision_maker.make_decision(report)

        # ---------------------------------------------------------
        # 2. Preserve values from the previous frame
        # ---------------------------------------------------------

        previous_aoa = self.plane.aoa
        previous_specific_energy = self.plane.specific_energy
        previous_total_energy = self.current_energy

        # ---------------------------------------------------------
        # 3. Autopilot chooses control targets
        # ---------------------------------------------------------
        #
        # The autopilot should not directly change pitch or throttle.
        # It should set:
        #
        # controller.target_pitch
        # controller.target_throttle
        #
        self.autopilot.update(
            self.plane,
            decision,
            self.flight_controller,
        )

        # ---------------------------------------------------------
        # 4. Controller moves toward those targets smoothly
        # ---------------------------------------------------------

        self.flight_controller.update_pitch(self.plane, dt)
        self.flight_controller.update_throttle(self.plane, dt)

        # Later:
        # self.flight_controller.update_bank(self.plane, dt)

        # ---------------------------------------------------------
        # 5. Physics responds to the control changes
        # ---------------------------------------------------------

        self.plane.update_physics(GRAVITY, dt)

        # ---------------------------------------------------------
        # 6. Update derived flight values
        # ---------------------------------------------------------

        self.plane.aoa_rate = FlightCalculator.rate_of_change(
            previous_aoa,
            self.plane.aoa,
            dt,
        )

        total_speed = FlightCalculator.total_speed(
            self.plane.horizontal_speed,
            self.plane.vertical_speed,
        )

        self.plane.specific_energy = FlightCalculator.specific_energy(
            GRAVITY,
            self.plane.altitude,
            total_speed,
        )

        self.plane.energy_rate = FlightCalculator.rate_of_change(
            previous_specific_energy,
            self.plane.specific_energy,
            dt,
        )

        self.current_energy = FlightCalculator.total_energy(
            self.plane.mass,
            GRAVITY,
            self.plane.altitude,
            total_speed,
        )

        self.energy_rate = FlightCalculator.rate_of_change(
            previous_total_energy,
            self.current_energy,
            dt,
        )

    def report(self) -> "FlightReport":
        """Returns the current flight analysis report."""
        return self.flight_analyzer.report()

    def telemetry(self) -> str:
        """Creates a readable snapshot of the current aircraft state."""

        total_speed = FlightCalculator.total_speed(
            self.plane.horizontal_speed,
            self.plane.vertical_speed,
        )

        kinetic_energy = FlightCalculator.kinetic_energy(
            self.plane.mass,
            total_speed,
        )

        potential_energy = FlightCalculator.potential_energy(
            self.plane.mass,
            GRAVITY,
            self.plane.altitude,
        )

        specific_energy = FlightCalculator.specific_energy(
            GRAVITY,
            self.plane.altitude,
            total_speed,
        )

        estimated_distance = FlightCalculator.estimated_glide_distance(
            self.plane.altitude,
            self.plane.calculate_lift(),
            self.plane.drag,
        )

        return (
            f"Pitch Angle: {self.plane.pitch_angle:.2f}° | "
            f"Flight Path Angle: {self.plane.flight_path_angle():.2f}° | "
            f"AoA: {self.plane.aoa:.2f}° | "
            f"AoA Rate: {self.plane.aoa_rate:.2f}°/s | "
            f"Altitude: {self.plane.altitude:.2f} m | "
            f"Estimated Glide Distance: {estimated_distance:,.2f} m | "
            f"Horizontal Speed: {self.plane.horizontal_speed:.2f} m/s | "
            f"Vertical Speed: {self.plane.vertical_speed:.2f} m/s | "
            f"Total Speed: {total_speed:.2f} m/s | "
            f"Lift: {self.plane.calculate_lift():.2f} N | "
            f"Drag: {self.plane.drag:.2f} N | "
            f"KE: {kinetic_energy:,.2f} J | "
            f"PE: {potential_energy:,.2f} J | "
            f"Total Energy: {self.current_energy:,.2f} J | "
            f"Specific Energy: {specific_energy:,.2f} J/kg | "
            f"Specific Energy Rate: {self.plane.energy_rate:,.2f} J/kg/s | "
            f"Total Energy Rate: {self.energy_rate:,.2f} J/s"
        )


