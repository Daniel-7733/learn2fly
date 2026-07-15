from .flight_calculator import FlightCalculator
from .flight_controller import FlightController

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plane import Plane


class AutoPilot:
    """Makes flight-control decisions for the aircraft."""
    def __init__(self, target_speed: float = 100, speed_deadband: float = 5.0,
                 target_altitude: float = 3000, altitude_deadband: float = 50.0, altitude_gain: float = 0.01, 
                 max_pitch_command: float = 5.0) -> None:
        """Initializes the autopilot with targets, deadbands, and limits."""

        # Set speed control variables
        self.target_speed = target_speed 
        self.speed_deadband = speed_deadband

        # Set altitude control variables
        self.target_altitude = target_altitude
        self.altitude_deadband = altitude_deadband
        self.altitude_gain = altitude_gain

        # Set safety limit variables
        self.max_pitch_command = max_pitch_command
        self.max_safe_aoa: float = 12

    def update(self, plane: "Plane", controller: "FlightController") -> None:
        """Evaluates plane sensors and updates flight controls each frame."""

        # Priority 1: protect speed
        if plane.horizontal_speed < plane.min_safe_speed - self.speed_deadband:
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return
        
        # Priority 2: protect AoA & Stall protection
        if plane.aoa > self.max_safe_aoa:
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return

        # Priority 3: Altitude control
        altitude_error = FlightCalculator.calculate_error(self.target_altitude, plane.altitude)

        if abs(altitude_error) <= self.altitude_deadband:   # Do nothing if the plane is within the acceptable altitude range
            return

        pitch_command = altitude_error * self.altitude_gain # Calculate proportional pitch change based on altitude error
        pitch_command = FlightCalculator.clamp(                        # Limit the calculated pitch command to safe operational boundaries
            pitch_command,
            -self.max_pitch_command,
            self.max_pitch_command,
        )

        if pitch_command > 0:                               # Apply controls depending on whether the plane needs to climb or descend
            controller.target_pitch = pitch_command
            controller.target_throttle = 0.7
        else:
            controller.target_pitch = pitch_command # if the answer isn't negetive I may need to make it like this: abs(pitch_command)
            controller.target_throttle = 0.3


