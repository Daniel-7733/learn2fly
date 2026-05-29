from plane import Plane
from config import GRAVITY, TIME_STEP


def main():
    plane: Plane = Plane(altitude=100.0, speed=20.0, angle=0.0)

    time_elapsed: int = 0

    while plane.altitude > 0:
        plane.apply_gravity(GRAVITY, TIME_STEP)
        time_elapsed += TIME_STEP

        print(
            f"Time: {time_elapsed:.1f}s | "
            f"Altitude: {plane.altitude:.2f} | "
            f"Speed: {plane.speed:.2f} | "
            f"Angle: {plane.angle:.2f}"
        )

    print("The plane has reached the ground.")


if __name__ == "__main__":
    main()
