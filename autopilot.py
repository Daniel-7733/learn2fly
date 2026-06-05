from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plane import Plane


class AutoPilot:
    """Makes flight-control decisions for the aircraft."""

    def __init__(self, safe_speed: float, target_altitude: float, altitude_deadband: float = 50.0, 
                 speed_deadband: float = 5.0, altitude_gain: float = 0.01, max_pitch_command: float = 5.0) -> None:
        self.safe_speed = safe_speed
        self.target_altitude = target_altitude
        self.altitude_deadband = altitude_deadband
        self.speed_deadband = speed_deadband
        self.altitude_gain = altitude_gain
        self.max_pitch_command = max_pitch_command

    def update(self, plane: "Plane") -> None:
        # Priority 1: protect speed
        if plane.horizontal_speed < self.safe_speed - self.speed_deadband:
            plane.pitch_down(1.0)
            return

        # Priority 2: correct altitude
        altitude_error = self.target_altitude - plane.altitude

        if abs(altitude_error) <= self.altitude_deadband:
            return

        pitch_command = altitude_error * self.altitude_gain
        pitch_command = self._clamp(
            pitch_command,
            -self.max_pitch_command,
            self.max_pitch_command,
        )

        if pitch_command > 0:
            plane.pitch_up(pitch_command)
        else:
            plane.pitch_down(abs(pitch_command))

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))

