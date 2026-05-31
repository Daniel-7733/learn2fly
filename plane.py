from math import tan, radians


class Plane:
    def __init__(self, altitude: float, horizontal_speed: float, angle: float) -> None:
        self.altitude = altitude
        self.horizontal_speed = horizontal_speed
        self.angle = angle
        self.vertical_speed: float = 0 

    def apply_gravity(self, gravity: float, time_step: float) -> None:
        self.vertical_speed = self.calculate_next_vertical_speed(gravity, time_step)
        self.altitude += self.vertical_speed * time_step 

        if self.altitude < 0:
            self.altitude = 0 

    def calculate_vertical_speed(self) -> float:
        """vertical_speed = tan(Theta) x horizontal speed"""
        return tan(radians(self.angle)) * self.horizontal_speed
    
    def calculate_next_vertical_speed(self, gravity: float, time_step: float) -> float:
        """final_velocity = initial_velocity + (acceleration x time)"""
        return self.vertical_speed + (gravity * time_step)
        
