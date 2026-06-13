from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plane import Plane


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

    def update(self, plane: "Plane") -> None:
        """Evaluates plane sensors and updates flight controls each frame."""

        # Priority 1: protect speed
        if plane.horizontal_speed < plane.min_safe_speed - self.speed_deadband:
            plane.thrust = plane.max_thrust
            plane.pitch_down(1.0)
            return
        
        # Priority 2: protect AoA & Stall protection
        if plane.aoa > self.max_safe_aoa:
            plane.set_throttle(1.0)
            plane.pitch_down(5.0)
            return

        # Priority 3: Altitude control
        altitude_error = self.target_altitude - plane.altitude

        if abs(altitude_error) <= self.altitude_deadband:   # Do nothing if the plane is within the acceptable altitude range
            return

        pitch_command = altitude_error * self.altitude_gain # Calculate proportional pitch change based on altitude error
        pitch_command = self._clamp(                        # Limit the calculated pitch command to safe operational boundaries
            pitch_command,
            -self.max_pitch_command,
            self.max_pitch_command,
        )

        if pitch_command > 0:                               # Apply controls depending on whether the plane needs to climb or descend
            plane.set_throttle(0.7)
            plane.pitch_up(pitch_command)
        else:
            plane.set_throttle(0.3)
            plane.pitch_down(abs(pitch_command))

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        """Restricts a numerical value between a minimum and maximum limit."""
        return max(minimum, min(maximum, value))

