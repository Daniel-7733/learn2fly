from math import tan, radians, atan2, degrees


class Plane:
    def __init__(self, altitude: float, horizontal_speed: float, pitch_angle: float, mass: float,
                 min_safe_speed: float = 50, critical_aoa: float = 15) -> None:
        # ===== altitude veriable ===== #
        self.altitude = altitude
        
        # ===== Speed veriables ===== #
        self.horizontal_speed = horizontal_speed
        self.vertical_speed: float = 0 
        self.min_safe_speed = min_safe_speed 
        
        # ===== mass veriable ===== #
        self.mass = mass 
        
        # ===== angle & degree veriables ===== #
        self.pitch_angle = pitch_angle # pitch / aircraft nose angle
        self.aoa: float = 0 # -> formula -> (AoA = Pitch Angle − Flight Path Angle) && wing angle against airflow
        self.critical_aoa = critical_aoa # stall boundary

        # ===== Force veriables ==== #
        self.drag: float = 0
        self.throttle: float = 0.5  # 0.0 to 1.0 (0% engine power)
        self.max_thrust: float = 100
        self.thrust: float = 0

    def update_physics(self, gravity: float, time_step: float) -> None:
        self.calculate_horizontal_speed(time_step)
        self.aoa = self.calculate_aoa()

        lift_force: float = self.calculate_lift()
        vertical_drag: float = self.calculate_vertical_drag()

        lift_acceleration: float = (lift_force + vertical_drag) / self.mass
        net_acceleration: float = gravity + lift_acceleration

        self.vertical_speed: float = self.calculate_next_vertical_speed(net_acceleration, time_step)
        self.altitude += self.vertical_speed * time_step 

        if self.altitude < 0:
            self.altitude = 0 


    # ================ Speed functions =============== #
    def calculate_vertical_speed(self) -> float: # I won't use this one becsaue I use physic formula to solve the problem
        """In geometr: vyertical_speed = tan(Theta) x horizontal speed"""
        return tan(radians(self.pitch_angle)) * self.horizontal_speed
    
    def calculate_next_vertical_speed(self, gravity: float, time_step: float) -> float:
        """final_velocity = initial_velocity + (acceleration x time)"""
        return self.vertical_speed + (gravity * time_step)

    def calculate_horizontal_speed(self, time_step: float) -> None:
        """
        f = ma -> a = f/m
        Vf = Vi + at
        """
        self.thrust = self.throttle * self.max_thrust
        self.drag = self.calculate_drag()

        net_force: float = self.thrust - self.drag
        acceleration: float = net_force / self.mass
        self.horizontal_speed += acceleration * time_step

        if self.horizontal_speed < 0:
            self.horizontal_speed = 0


    # ================ angle, degrees & pitch functions =============== #
    def flight_path_angle(self) -> float:
        """
        In math terms:
            Let y = Vertical Speed, x = Horizontal Speed
            1. tan(Theta) = y / x (The ratio of speeds)
            2. Flight Path Angle (radians) = tan^-1(y / x)
            3. Flight Path Angle (degrees) = tan^-1(y / x) * (180 / pi)
        
        In python terms:
            flight_path_angle = degrees(atan2(vertical_speed, horizontal_speed))
        
        Mathematical Identities:
            atan2(y, x) == tan^-1(y / x)                 -> Returns Radians
            degrees(atan2(y, x)) == tan^-1(y / x) * (180/pi) -> Returns Degrees
        """
        return degrees(atan2(self.vertical_speed, self.horizontal_speed))
    
    def calculate_aoa(self) -> float:
        """
        In math terms:
            AoA (degrees) = Pitch Angle (degrees) - Flight Path Angle (degrees)

        In python terms:
            2. AoA = pitch_angle - flight_path_angle
        
        """
        return self.pitch_angle - self.flight_path_angle()

    def pitch_up(self, degree: float):
        """User can change the angle of plane to the up"""
        self.pitch_angle += degree

        if self.pitch_angle > 45:
            self.pitch_angle = 45

    def pitch_down(self, degree: float):
        """User can change the angle of plane to the down"""
        self.pitch_angle -= degree

        if self.pitch_angle < -45:
            self.pitch_angle = -45


    # ================ force functions =============== #
    def calculate_drag(self) -> float:
        """Calculating the drag on x axel; The opposite forse of thrust"""
        base_drag_factor: float = 0.05
        aoa_drag_factor: float = 0.02 # High AoA should create huge drag

        base_drag: float = self.horizontal_speed * base_drag_factor
        aoa_drag: float = abs(self.aoa) * aoa_drag_factor * self.horizontal_speed

        return base_drag + aoa_drag

    def calculate_vertical_drag(self) -> float:
        """calculating the resistance of drag on vertical axel"""
        drag_factor: float = 0.05
        return -self.vertical_speed * drag_factor

    def calculate_lift(self) -> float:
        """This is a very simple calculation about lifting. More complex one will be added next time."""
        lift_factor: float = 0.01

        if self.aoa <= self.critical_aoa:
            effective_aoa = self.aoa
        else: # if angle is more then stall angle the plane loss its effective angle and enter at stall angle
            effective_aoa = max(0, self.critical_aoa - (self.aoa - self.critical_aoa))

        return effective_aoa * self.horizontal_speed * lift_factor
        
    def set_throttle(self, value: float) -> None:
        """Sets the engine throttle while keeping the value between 0.0 and 1.0."""
        self.throttle = max(0.0, min(1.0, value))

