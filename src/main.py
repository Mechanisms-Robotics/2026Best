# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Mechanisms Robotics                                          #
#   Description:  2026 BEST robot - VEX V5 Python starter                      #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# ---------------------------------------------------------------------------- #
# Devices
# Change the port numbers to match how your robot is wired. If a side of the
# drivetrain drives backward, flip the True/False (reversed) on those motors.
# ---------------------------------------------------------------------------- #
brain = Brain()
controller = Controller()

left_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_back = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_front = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_back = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

left_drive = MotorGroup(left_front, left_back)
right_drive = MotorGroup(right_front, right_back)

# Joystick values smaller than this (in percent) are treated as zero so the
# robot doesn't creep when the sticks are centered.
DEADBAND = 5


def apply_deadband(value):
    if abs(value) < DEADBAND:
        return 0
    return value


# ---------------------------------------------------------------------------- #
# Autonomous - runs once when the field starts the autonomous period.
# ---------------------------------------------------------------------------- #
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Autonomous")

    # Example: drive forward for one second, then stop.
    left_drive.spin(FORWARD, 50, PERCENT)
    right_drive.spin(FORWARD, 50, PERCENT)
    wait(1, SECONDS)
    left_drive.stop()
    right_drive.stop()


# ---------------------------------------------------------------------------- #
# Driver control - arcade drive.
# Left stick up/down (axis 3) = forward/back, right stick left/right (axis 1) = turn.
# ---------------------------------------------------------------------------- #
def driver_control():
    brain.screen.clear_screen()
    brain.screen.print("Driver control")

    while True:
        forward = apply_deadband(controller.axis3.position())
        turn = apply_deadband(controller.axis1.position())

        left_drive.spin(FORWARD, forward + turn, PERCENT)
        right_drive.spin(FORWARD, forward - turn, PERCENT)

        # Give the brain time for other tasks. Every loop should wait a little.
        wait(20, MSEC)


# The Competition object calls autonomous() and driver_control() when the field
# control system says to. With no field control plugged in, running the program
# goes straight to driver_control().
competition = Competition(driver_control, autonomous)
