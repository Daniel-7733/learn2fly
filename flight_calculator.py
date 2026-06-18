class FlightCalculator:
    """
    FlightCalculator = formulas
    shared calculations

    Measurement that I use in this program:
        Distance Measurement: m
        Mass Measurement: Kg
        Speed Measurement: m/s
        Acceleration Measurement: m/s^2
        Eneregy Measurement: J
        Force Measurement: N

    """

    @staticmethod
    def kinetic_energy(mass: float, speed: float) -> float:
        """This function calulate kinetic energy: KE = 1/2 mv^2"""
        return 0.5 * mass * speed ** 2

    @staticmethod
    def potential_energy(mass: float, gravity: float, altitude: float) -> float:
        """This function calculate potential energy: PE = mgh"""
        return mass * abs(gravity) * altitude

    @staticmethod
    def total_energy(mass: float, gravity: float, altitude: float, speed: float) -> float:
        """This function calculate the total energy: E = mgh + 1/2 mv^2"""
        return (
            FlightCalculator.kinetic_energy(mass, speed)
            + FlightCalculator.potential_energy(mass, gravity, altitude)
        )

    @staticmethod
    def specific_energy(gravity: float, altitude: float, speed: float) -> float:
        """
        This function will calculate the specific energy by removing the mass from right side of formula.
        E = mgh + 1/2 mv^2 -> at the end we receive Energy (Like 1000 J)
        E/m = gh + v^2 / 2 -> at the end we receive Energy per kilogram (Like 500 J/KG)
        """
        return abs(gravity) * altitude + 0.5 * speed ** 2

    @staticmethod
    def estimated_glide_distance(altitude: float, lift: float, drag: float) -> float:
        """
        With this formula we will get the gliding distance that we can travel.
        formula: distance = altitude * (lift / drag)
        Note: Right now, it is estimated answer because our formula for drag, lift is not complete yet
        """
        if drag <= 0:
            return 0.0
        return altitude * (lift / drag)
    
    @staticmethod
    def total_speed(horizontal_speed: float, vertical_speed: float) -> float:
        """
        This function calculate the both speeds and return total speed. How did I find this formula:

        1. c^2 = a^2 + b^2        ---OR--- (Vx^2 + Vy^2 = V^2)
        2.   c = root(a^2 + b^2)
        3.   c = (a^2 + b^2)^1/2  ---OR--- c = (a^2 + b^2)^0.5

        So, this is the formula -> (Vx^2 + Vy^2)^0.5
        """
        return (horizontal_speed**2 + vertical_speed**2) ** 0.5

    @staticmethod
    def energy_rate(previous_energy: float, current_energy: float, time_step: float) -> float:
        """Energy rate is Energy rate = de/dt"""
        return (current_energy - previous_energy) / time_step
