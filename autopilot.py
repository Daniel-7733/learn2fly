from plane import Plane


class AutoPilot:
    """This class is for making decisions: (Then we might have other class like Human Pilot, Military Pilot, Civil Pilot, Autopilot, AI Pilot)"""
    def __init__(self, safe_speed: float, target_altitude: float):
        self.safe_speed = safe_speed 
        self.target_altitude = target_altitude

    def update(self, plane: Plane):
        if plane.horizontal_speed < self.safe_speed:
            plane.pitch_down(1)

        elif plane.altitude < self.target_altitude:
            plane.pitch_up(1)

        elif plane.altitude > self.target_altitude:
            plane.pitch_down(1)


