class Plane:
    def __init__(self, altitude: float, speed: float, angle: float):
        self.altitude = altitude
        self.speed = speed
        self.angle = angle

    def apply_gravity(self, gravity: float, time_step: float):
        self.altitude -= gravity * time_step

        if self.altitude < 0:
            self.altitude = 0
