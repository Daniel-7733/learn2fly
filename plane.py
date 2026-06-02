from math import tan, radians


class Plane:
    def __init__(self, altitude: float, horizontal_speed: float, angle: float, mass: float) -> None:
        self.altitude = altitude
        self.horizontal_speed = horizontal_speed
        self.angle = angle
        self.vertical_speed: float = 0 
        self.thrust: float = 3 
        self.drag: float = 1 
        self.mass: float = mass 

    def update_physics(self, gravity: float, time_step: float) -> None:
        lift: float = self.calculate_lift()
        net_acceleration: float = gravity + lift

        self.calculate_horizontal_speed(time_step)
        self.vertical_speed: float = self.calculate_next_vertical_speed(net_acceleration, time_step)
        self.altitude += self.vertical_speed * time_step 

        if self.altitude < 0:
            self.altitude = 0 

    def calculate_vertical_speed(self) -> float:
        """vertical_speed = tan(Theta) x horizontal speed"""
        return tan(radians(self.angle)) * self.horizontal_speed
    
    def calculate_next_vertical_speed(self, gravity: float, time_step: float) -> float:
        """final_velocity = initial_velocity + (acceleration x time)"""
        return self.vertical_speed + (gravity * time_step)

    def calculate_lift(self) -> float:
        """This is a very simple calculation about lifting. More complex one will be added next time."""
        lift_factor: float = 0.01
        stall_angle: float = 15

        if self.angle <= stall_angle:
            effective_angle: float = self.angle
        else: # if angle is more then stall angle the plane loss its effective angle and enter at stall angle
            effective_angle = max(0, stall_angle - (self.angle - stall_angle))

        return effective_angle * self.horizontal_speed * lift_factor
        
    def pitch_up(self, degree: float):
        self.angle += degree

        if self.angle > 45:
            self.angle = 45

    def pitch_down(self, degree: float):
        self.angle -= degree

        if self.angle < -45:
            self.angle = -45

    def calculate_horizontal_speed(self, time_step: float) -> None:
        """
        f = ma -> a = f/m
        Vf = Vi + at
        """
        net_force: float = self.thrust - self.drag
        acceleration: float = net_force / self.mass
        self.horizontal_speed += (acceleration * time_step)
