from math import tan, radians


class Plane:
    def __init__(self, altitude: float, horizontal_speed: float, angle: float, mass: float) -> None:
        self.altitude = altitude
        self.horizontal_speed = horizontal_speed
        self.angle = angle
        self.mass = mass 
        self.vertical_speed: float = 0 
        self.thrust: float = 0 # for fall test I put 0 as value but then I'll change it to 3 or more 
        self.drag: float = 0 

    def update_physics(self, gravity: float, time_step: float) -> None:
        self.calculate_horizontal_speed(time_step)

        lift_force: float = self.calculate_lift()
        vertical_drag: float = self.calculate_vertical_drag()

        lift_acceleration: float = (lift_force + vertical_drag) / self.mass
        net_acceleration: float = gravity + lift_acceleration

        self.vertical_speed: float = self.calculate_next_vertical_speed(net_acceleration, time_step)
        self.altitude += self.vertical_speed * time_step 

        if self.altitude < 0:
            self.altitude = 0 

    def calculate_vertical_speed(self) -> float: # I won't use this one becsaue I use physic formula to solve the problem
        """In geometr: vyertical_speed = tan(Theta) x horizontal speed"""
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
        
    def calculate_vertical_drag(self) -> float:
        """calculating the resistance of drag on vertical axel"""
        drag_factor: float = 0.05
        return -self.vertical_speed * drag_factor

    def pitch_up(self, degree: float):
        """User can change the angle of plane to the up"""
        self.angle += degree

        if self.angle > 45:
            self.angle = 45

    def pitch_down(self, degree: float):
        """User can change the angle of plane to the down"""
        self.angle -= degree

        if self.angle < -45:
            self.angle = -45

    def calculate_horizontal_speed(self, time_step: float) -> None:
        """
        f = ma -> a = f/m
        Vf = Vi + at
        """
        self.drag = self.calculate_drag()

        net_force: float = self.thrust - self.drag
        acceleration: float = net_force / self.mass
        self.horizontal_speed += (acceleration * time_step)

    def calculate_drag(self) -> float:
        """Calculating the drag on x axel; The opposite forse of thrust"""
        drag_factor: float = 0.05
        return self.horizontal_speed * drag_factor
