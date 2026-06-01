from plane import Plane
from config import GRAVITY, TIME_STEP


def main():
    time_elapsed: int = 0

    plane: Plane = Plane(altitude=100.0, horizontal_speed=20.0, angle=3.0)

    while plane.altitude > 0:
        plane.apply_vertical_forces(GRAVITY, TIME_STEP)
        time_elapsed += TIME_STEP

        if time_elapsed == 2:
            plane.pitch_up(100)

        print(
            f"Time: {time_elapsed:.1f}s | "
            f"Altitude: {plane.altitude:.2f}m | "
            f"horizontal Speed: {plane.horizontal_speed:.2f}m/s | "
            f"Angle: {plane.angle:.2f}° | "
            f"Vertical speed is: {plane.vertical_speed:.2f}m/s"
        )
        
    print("The plane has reached the ground.")


if __name__ == "__main__":
    main()
