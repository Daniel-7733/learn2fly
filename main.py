"""
            Measurement that I use in this program:
                Distance Measurement: m
                Mass Measurement: Kg
                Speed Measurement: m/s
                Acceleration Measurement: m/s^2
                Eneregy Measurement: J
                Force Measurement: N

            classes and there duties
                Plane:
                    State of aircraft & stores state

                FlightCalculator:
                    Physics calculations & computes physics

                AutoPilot:
                    makes decisions

                FlightAnalyzer
                    interprets state

                FlightReport:
                    Presentation

                MissionPlanner:
                    Goals
"""

from plane import Plane
from autopilot import AutoPilot
from flight_calculator import FlightCalculator
from flight_analyzer import FlightAnalyzer
from config import GRAVITY, TIME_STEP


def main():
    time_elapsed: float = 0

    plane: Plane = Plane(altitude=1200, horizontal_speed=85, pitch_angle=10, mass=20.0)
    autopilot: AutoPilot = AutoPilot()
    flight_analyzer: FlightAnalyzer = FlightAnalyzer(plane, autopilot) 


    current_energy: float = FlightCalculator.total_energy(
        plane.mass, GRAVITY, plane.altitude,
        FlightCalculator.total_speed(plane.horizontal_speed, plane.vertical_speed)
    )

    while plane.altitude > 0:
        plane.previous_aoa = plane.aoa
        plane.aoa = plane.calculate_aoa()
        plane.aoa_rate = FlightCalculator.rate_of_change(plane.previous_aoa, plane.aoa, TIME_STEP)

        previous_energy: float = current_energy

        plane.update_physics(GRAVITY, TIME_STEP)

        total_speed: float = FlightCalculator.total_speed(plane.horizontal_speed, plane.vertical_speed)
        current_energy: float = FlightCalculator.total_energy(plane.mass, GRAVITY, plane.altitude, total_speed)
        energy_rate: float = FlightCalculator.rate_of_change(previous_energy, current_energy, TIME_STEP)

        time_elapsed += TIME_STEP

        
        #if time_elapsed == 2:
            #plane.pitch_up(30)
        
        ke: float = FlightCalculator.kinetic_energy(plane.mass, total_speed)
        pe: float = FlightCalculator.potential_energy(plane.mass, GRAVITY, plane.altitude)
        energy: float = FlightCalculator.total_energy(plane.mass, GRAVITY, plane.altitude, total_speed)
        specific_energy: float = FlightCalculator.specific_energy(GRAVITY, plane.altitude, total_speed)
        estimated_distance: float = FlightCalculator.estimated_glide_distance(plane.altitude, plane.calculate_lift(), plane.drag)

        print(
            f"Time: {time_elapsed:.1f}s | "

            f"Pitch Angle: {plane.pitch_angle:.2f}° | "
            #f"Initial Pitch: {plane.pitch_angle} | "
            f"Flight Path Angle: {plane.flight_path_angle():.2f}° | "
            f"AoA: {plane.aoa:.2f}° | "

            f"Altitude: {plane.altitude:.2f}m | "
            f"estimated_distance: {estimated_distance:,.2f}m | "

            f"horizontal Speed: {plane.horizontal_speed:.2f}m/s | "
            f"Vertical Speed: {plane.vertical_speed:.2f}m/s | "
            f"Total Speed: {total_speed:.2f} m/s | "

            f"Lift: {plane.calculate_lift():.2f}N | "
            f"Drag: {plane.drag:.2f}N | "

            f"KE: {ke:,.2f}J | "
            f"PE: {pe:,.2f}J | "
            f"E: {energy:,.2f}J | "
            f"Specific Energy: {specific_energy:,.2f}J/KG | "
            f"Energy Rate: {energy_rate:,.2f}J | "
            )

        print(flight_analyzer.report())
        
    print("The plane has reached the ground.")

    

if __name__ == "__main__":
    main()
