from .flight_calculator import FlightCalculator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plane import Plane


class FlightController:
    """
    Mission goal isn't the job of this class; This class meant to know the targets and smooth the movement.
    In another word, this class ask: How do I smoothly move toward that target?
    """
    def __init__(self, target_pitch: float = 0.0, target_throttle: float = 0.0, max_pitch_rate: float = 2.0, max_throttle_rate: float = 0.2) -> None:
        self.target_pitch = target_pitch
        self.target_throttle = target_throttle
        self.max_pitch_rate = max_pitch_rate
        self.max_throttle_rate = max_throttle_rate

    def update_pitch(self, plane: "Plane", dt: float) -> None:
        """
        Updating the pitch. 
        Plane is the Object and dt is delta time
        """
        pitch_error: float = FlightCalculator.calculate_error(self.target_pitch, plane.pitch_angle)
        max_change: float = self.max_pitch_rate * dt
        pitch_change: float = FlightCalculator.clamp(pitch_error, -max_change, max_change)
        plane.pitch_angle += pitch_change

    def update_throttle(self, plane: "Plane", dt: float) -> None:
        """
        Updating the throttle. 
        Plane is the Object and dt is delta time
        """
        throttle_error: float = FlightCalculator.calculate_error(self.target_throttle, plane.throttle)
        max_change: float = self.max_throttle_rate * dt
        throttle_change: float = FlightCalculator.clamp(throttle_error, -max_change, max_change)
        plane.throttle += throttle_change

    def update_bank(self, plane: "Plane", dt: float):
        pass


