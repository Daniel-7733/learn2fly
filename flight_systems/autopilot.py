from typing import TYPE_CHECKING

from .flight_calculator import FlightCalculator
from .enums import FlightMode, ThreatType
from .missions.mission import Mission

if TYPE_CHECKING:
    from .plane import Plane
    from .flight_controller import FlightController
    from .decisions.decision import Decision


class AutoPilot:
    """
    Translates a Decision into control targets.

    It does not move the aircraft directly.
    It gives target values to FlightController.
    """

    def __init__(self, mission: Mission, speed_deadband: float = 5.0, 
                 altitude_deadband: float = 50.0, altitude_gain: float = 0.01, 
                 descent_vertical_speed_gain: float = 1.0, max_pitch_command: float = 5.0,
                 recovery_target_aoa: float = 4.0, minimum_recovery_pitch: float = -30.0, 
                 maximum_recovery_pitch: float = 10.0) -> None:

        # Mission goals are immutable and shared with DecisionMaker.
        self.mission = mission

        # Speed-control configuration
        self.speed_deadband = speed_deadband

        # Altitude-control configuration
        self.altitude_deadband = altitude_deadband
        self.altitude_gain = altitude_gain

        # Safety limits
        self.max_pitch_command = max_pitch_command
        self.max_safe_aoa: float = 12.0
        
        # Safety recovery
        self.recovery_target_aoa = recovery_target_aoa
        self.minimum_recovery_pitch = minimum_recovery_pitch
        self.maximum_recovery_pitch = maximum_recovery_pitch

        # Control value
        self.descent_vertical_speed_gain = 1.0
        self.descent_vertical_speed_gain = descent_vertical_speed_gain
        
        # Landing configuration
        self.landing_vertical_speed_mps = 1.5
        self.landing_vertical_speed_gain = 1.0

    def update(self, plane: "Plane", decision: "Decision", controller: "FlightController") -> None:
        """
        Translates the selected decision into pitch and throttle targets.
        """

        # ---------------------------------------------------------
        # 1. Emergency strategies
        # ---------------------------------------------------------

        if decision.mode is FlightMode.EMERGENCY:
            if decision.reason is ThreatType.STALL:
                recovery_pitch = (
                    plane.flight_path_angle()
                    + self.recovery_target_aoa
                )

                controller.target_pitch = FlightCalculator.clamp(
                    recovery_pitch,
                    self.minimum_recovery_pitch,
                    self.maximum_recovery_pitch,
                )

                controller.target_throttle = 1.0
                return

            if decision.reason is ThreatType.LOW_SPEED:
                controller.target_pitch = -5.0
                controller.target_throttle = 1.0
                return

            if decision.reason is ThreatType.IMPACT:
                controller.target_pitch = 5.0
                controller.target_throttle = 1.0
                return

            # Emergency is still active during the confirmation period.
            # Hold a gentle recovery configuration.
            controller.target_pitch = FlightCalculator.clamp(
                plane.flight_path_angle() + self.recovery_target_aoa,
                self.minimum_recovery_pitch,
                self.maximum_recovery_pitch,
            )
            controller.target_throttle = 0.7
            return

        # ---------------------------------------------------------
        # 2. Temporary fallback protection
        #
        # These checks can remain while the new DecisionMaker is
        # being integrated. Later, DecisionMaker should own them.
        # ---------------------------------------------------------

        if plane.horizontal_speed < (plane.min_safe_speed - self.speed_deadband):
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return

        if plane.aoa > self.max_safe_aoa:
            controller.target_pitch = -5.0
            controller.target_throttle = 1.0
            return
        
        # ---------------------------------------------------------
        # 3. Landing control
        # ---------------------------------------------------------

        if decision.mode is FlightMode.LANDING:
            target_vertical_speed = -self.landing_vertical_speed_mps

            vertical_speed_error = FlightCalculator.calculate_error(
                target_vertical_speed,
                plane.vertical_speed,
            )

            pitch_command = FlightCalculator.proportional_command(
                self.landing_vertical_speed_gain,
                vertical_speed_error,
            )

            controller.target_pitch = FlightCalculator.clamp(
                pitch_command,
                -self.max_pitch_command,
                self.max_pitch_command,
            )

            if plane.horizontal_speed < (
                self.mission.landing_speed - self.speed_deadband
            ):
                controller.target_throttle = 0.7

            elif plane.horizontal_speed > (
                self.mission.landing_speed + self.speed_deadband
            ):
                controller.target_throttle = 0.3

            else:
                controller.target_throttle = 0.5

            return
                        
        # ---------------------------------------------------------
        # 4. Descent control strategy
        # ---------------------------------------------------------

        if decision.mode is FlightMode.DESCENT:
            target_vertical_speed_mps = (-self.mission.planned_descent_speed_mps)

            vertical_speed_error = FlightCalculator.calculate_error(
                target_vertical_speed_mps,
                plane.vertical_speed,
            )

            pitch_command = FlightCalculator.proportional_command(
                self.descent_vertical_speed_gain,
                vertical_speed_error,
            )

            controller.target_pitch = FlightCalculator.clamp(
                pitch_command,
                -self.max_pitch_command,
                self.max_pitch_command,
            )

            # Maintain cruise speed during the initial descent.
            if plane.horizontal_speed < (self.mission.cruise_speed - self.speed_deadband):
                controller.target_throttle = 0.7

            elif plane.horizontal_speed > (self.mission.cruise_speed + self.speed_deadband):
                controller.target_throttle = 0.3

            else:
                controller.target_throttle = 0.5

            # Prevent normal altitude control from overwriting
            # the descent commands.
            return

        # ---------------------------------------------------------
        # 5. normal altitude-control strategy
        # ---------------------------------------------------------

        altitude_error = FlightCalculator.calculate_error(
            self.mission.target_altitude,
            plane.altitude,
        )

        # inside the acceptable altitude range, command level flight.
        if abs(altitude_error) <= self.altitude_deadband:
            controller.target_pitch = 0.0
            controller.target_throttle = 0.5
            return

        pitch_command = FlightCalculator.proportional_command(
            self.altitude_gain,
            altitude_error,
        )

        pitch_command = FlightCalculator.clamp(
            pitch_command,
            -self.max_pitch_command,
            self.max_pitch_command,
        )

        controller.target_pitch = pitch_command

        if pitch_command > 0:
            controller.target_throttle = 0.7
        else:
            controller.target_throttle = 0.3

