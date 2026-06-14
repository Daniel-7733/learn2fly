"""
            Meaurement that I use in this program:
                Distance meaurement: m
                Mass measurement: Kg
                Speed meaurement: m/s
                Acceleration meaurement: m/s^2
                Eneregy meaurement: J
                Force meaurement: N

            classes and there duties
                Plane:
                    State of aircraft

                AutoPilot:
                    Decisions

                FlightCalculator:
                    Physics calculations. Ex -> distance = calculator.max_glide_distance(plane)

                MissionPlanner:
                    Goals
"""

from plane import Plane
from autopilot import AutoPilot
from config import GRAVITY, TIME_STEP


def main():
    time_elapsed: float = 0

    plane: Plane = Plane(altitude=1200, horizontal_speed=85, pitch_angle=10, mass=20.0)
    autopilot: AutoPilot = AutoPilot()

    while plane.altitude > 0:

        plane.aoa = plane.calculate_aoa()
        autopilot.update(plane)

        plane.update_physics(GRAVITY, TIME_STEP)
        time_elapsed += TIME_STEP
        
        #if time_elapsed == 2:
            #plane.pitch_up(30)

        #print(
            #f"Time: {time_elapsed:.1f}s | "
            #f"Altitude: {plane.altitude:.2f}m | "
            #f"horizontal Speed: {plane.horizontal_speed:.2f}m/s | "
            #f"Angle: {plane.angle:.2f}° | "
            #f"Vertical speed is: {plane.vertical_speed:.2f}m/s"
        #)

        KE: float = 1/2 * plane.mass * plane.vertical_speed**2
        PE: float = plane.mass * abs(GRAVITY) * plane.altitude
        E: float = KE + PE
        distance: float = plane.altitude * (plane.calculate_lift() / plane.drag)

        print(
            f"Time: {time_elapsed:.1f}s | "
            f"Pitch Angle: {plane.pitch_angle:.2f}° | "
            #f"Initial Pitch: {plane.pitch_angle} | "
            f"Flight Path Angle: {plane.flight_path_angle():.2f}° | "
            f"AoA: {plane.aoa:.2f}° | "
            f"Altitude: {plane.altitude:.2f}m | "
            f"horizontal Speed: {plane.horizontal_speed:.2f}m/s | "
            f"Vertical Speed: {plane.vertical_speed:.2f}m/s | "
            f"Lift: {plane.calculate_lift():.2f}N | "
            f"Drag: {plane.drag:.2f}N | "
            f"KE: {KE:,.2f}J | "
            f"PE: {PE:,.2f}J | "
            f"E: {E:,.2f}J | "
            f"estimated_distance: {distance:,.2f}m | " # for now My lift and drag are simplified simulator values and that's why I said estimated until i use correct form of drag, lift,... formula
            )

        
    print("The plane has reached the ground.")


if __name__ == "__main__":
    main()
