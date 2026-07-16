from typing import TYPE_CHECKING

from .flight_calculator import FlightCalculator
from .enums import FlightMode, ThreatType

if TYPE_CHECKING:
    from .plane import Plane
    from .decision import Decision
    from .flight_controller import FlightController


class AutoPilot:
    """
    Translates a Decision into control targets.

    It does not move the aircraft directly.
    It gives target values to FlightController.
    """

    def __init__(self, target_speed: float = 100.0, speed_deadband: float = 5.0, target_altitude: float = 3000.0, altitude_deadband: float = 50.0, altitude_gain: float = 0.01, max_pitch_command: float = 5.0) -> None:
        # Speed-control configuration
        self.target_speed = target_speed
        self.speed_deadband = speed_deadband

        # Altitude-control configuration
        self.target_altitude = target_altitude
        self.altitude_deadband = altitude_deadband
        self.altitude_gain = altitude_gain

        # Safety limits
        self.max_pitch_command = max_pitch_command
        self.max_safe_aoa: float = 12.0

    def update(self, plane: "Plane", decision: "Decision", controller: "FlightController") -> None:
        """
        Translates the selected decision into pitch and throttle targets.
        """

        # ---------------------------------------------------------
        # 1. Emergency strategies
        # ---------------------------------------------------------

        if decision.mode is FlightMode.EMERGENCY:

            if decision.reason is ThreatType.STALL:
                controller.target_pitch = -5.0
                controller.target_throttle = 1.0
                return

            if decision.reason is ThreatType.IMPACT:
                controller.target_pitch = 5.0
                controller.target_throttle = 1.0
                return

        # ---------------------------------------------------------
        # 2. Temporary fallback protection
        #
        # These checks can remain while the new DecisionMaker is
        # being integrated. Later, DecisionMaker should own them.
        # ---------------------------------------------------------

        if plane.horizontal_speed < (
            plane.min_safe_speed - self.speed_deadband
        ):
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return

        if plane.aoa > self.max_safe_aoa:
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return

        # ---------------------------------------------------------
        # 3. Normal altitude-control strategy
        # ---------------------------------------------------------

        altitude_error = FlightCalculator.calculate_error(
            self.target_altitude,
            plane.altitude,
        )

        # Inside the acceptable altitude range, command level flight.
        if abs(altitude_error) <= self.altitude_deadband:
            controller.target_pitch = 0.0
            controller.target_throttle = 0.5
            return

        pitch_command = FlightCalculator.proportional_command(
            self.altitude_gain,
            altitude_error,
        )

        pitch_command = FlightCalculator.clamp(
            pitch_command,
            -self.max_pitch_command,
            self.max_pitch_command,
        )

        controller.target_pitch = pitch_command

        if pitch_command > 0:
            controller.target_throttle = 0.7
        else:
            controller.target_throttle = 0.3

