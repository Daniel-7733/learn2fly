from math import tan, radians, atan2, degrees
from flight_systems.flight_calculator import FlightCalculator


class Plane:
    def __init__(self, altitude: float, horizontal_speed: float, pitch_angle: float, mass: float,
                 min_safe_speed: float = 50, critical_aoa: float = 15, max_thrust: float = 100) -> None:
        # ===== altitude veriable ===== #
        self.altitude = altitude
        
        # ===== Speed veriables ===== #
        self.horizontal_speed = horizontal_speed
        self.vertical_speed: float = 0 
        self.min_safe_speed = min_safe_speed 
        self.distance_travelled_m = 0.0
        
        # ===== mass veriable ===== #
        self.mass = mass 
        
        # ===== angle & degree veriables ===== #
        self.pitch_angle = pitch_angle # pitch / aircraft nose angle
        self.aoa: float = 0 # -> formula -> (AoA = Pitch Angle − Flight Path Angle) && wing angle against airflow
        self.previous_aoa: float = 0.0
        self.aoa_rate: float = 0.0
        self.critical_aoa = critical_aoa # stall boundary

        # ===== Force veriables ==== #
        self.drag: float = 0
        self.throttle: float = 0.5  # 0.0 to 1.0 (0% engine power)
        self.max_thrust: float = max_thrust
        self.thrust: float = 0

        # ===== Energy veriables ==== #
        self.specific_energy = 0.0
        self.energy_rate = 0.0

    def update_physics(self, gravity: float, dt: float) -> None:
        if dt <= 0.0:
            raise ValueError("dt must be greater than zero.")

        # Save AoA from the previous completed physics step.
        self.previous_aoa = self.aoa

        # Refresh AoA before calculating forces that depend on it.
        self.aoa = self.calculate_aoa()

        # Update horizontal motion using the current AoA for drag.
        previous_horizontal_speed = self.horizontal_speed
        self.calculate_horizontal_speed(dt)

        # Horizontal speed changed, so refresh AoA before calculating lift.
        self.aoa = self.calculate_aoa()

        average_horizontal_speed = FlightCalculator.average_speed(previous_horizontal_speed, self.horizontal_speed)
        self.distance_travelled_m += average_horizontal_speed * dt

        lift_force: float = self.calculate_lift()
        vertical_drag: float = self.calculate_vertical_drag()

        lift_acceleration: float = (
            lift_force + vertical_drag
        ) / self.mass

        net_acceleration: float = gravity + lift_acceleration

        self.vertical_speed = self.calculate_next_vertical_speed(
            net_acceleration,
            dt,
        )

        self.altitude += self.vertical_speed * dt

        if self.altitude < 0.0:
            self.altitude = 0.0

        # Calculate the final AoA of this completed physics step.
        self.aoa = self.calculate_aoa()

        self.aoa_rate = (self.aoa - self.previous_aoa) / dt

    # ================ Speed functions =============== #
    def calculate_vertical_speed(self) -> float: # I won't use this one becsaue I use physic formula to solve the problem
        """In geometr: vyertical_speed = tan(Theta) x horizontal speed"""
        return tan(radians(self.pitch_angle)) * self.horizontal_speed
    
    def calculate_next_vertical_speed(self, acceleration: float, dt: float) -> float:
        """final_velocity = initial_velocity + (acceleration x time)"""
        return self.vertical_speed + (acceleration * dt)

    def calculate_horizontal_speed(self, dt: float) -> None:
        """
        f = ma -> a = f/m
        Vf = Vi + at
        """
        self.thrust = self.throttle * self.max_thrust
        self.drag = self.calculate_drag()

        net_force: float = self.thrust - self.drag
        acceleration: float = net_force / self.mass
        self.horizontal_speed += acceleration * dt

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
        """
        Calculate simplified horizontal aerodynamic drag. (Calculating the drag on x axel; The opposite forse of thrust)

        Drag increases with:
        - the square of horizontal speed;
        - the absolute angle of attack.
        """
        base_drag_factor: float = 0.003
        aoa_drag_factor: float = 0.0004

        speed_squared: float = self.horizontal_speed**2

        base_drag: float = (
            base_drag_factor * speed_squared
        )

        aoa_drag: float = (
            aoa_drag_factor
            * abs(self.aoa)
            * speed_squared
        )

        return base_drag + aoa_drag

    def calculate_vertical_drag(self) -> float:
        """calculating the resistance of drag on vertical axel"""
        drag_factor: float = 0.05
        return -self.vertical_speed * drag_factor

    def calculate_lift(self) -> float:
        """Calculate simplified aerodynamic lift. 
        The real formula is L=1/2pv^2SCL
        Where:

        ρ is air density;
        v is airspeed;
        S is wing area;
        CL is the lift coefficient.
        """

        lift_factor: float = 0.00543

        if self.aoa <= self.critical_aoa:
            effective_aoa = self.aoa
        else:
            stall_excess = self.aoa - self.critical_aoa
            effective_aoa = max(
                0.0,
                self.critical_aoa - stall_excess,
            )

        return lift_factor * (self.horizontal_speed**2) * effective_aoa
        
    def set_throttle(self, value: float) -> None:
        """Sets the engine throttle while keeping the value between 0.0 and 1.0."""
        self.throttle = max(0.0, min(1.0, value))

