# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Mechanisms Robotics                                          #
#   Description:  2026 BEST robot (Byte to Bite) - VEX V5 Python               #
#                                                                              #
#   This is the program that gets downloaded to the brain.                     #
#                                                                              #
#   Right now it holds a TEMPORARY BENCH TEST: the left stick runs one motor  #
#   and the right stick moves one servo.                                       #
#   Everything marked TEMPORARY BENCH TEST is meant to be removed or replaced  #
#   once the real robot code is written.                                       #
#                                                                              #
#   examples/example.py has a working example of every building block (motors, #
#   sensors, driving, autonomous). Copy what you need from there into this     #
#   file. You can't import it: only this one file is downloaded to the brain.  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# ---------------------------------------------------------------------------- #
# Devices
#
# Declare every motor and sensor here, once you know which port it is plugged
# into. See the Devices section of examples/example.py for how each one is
# written.
# ---------------------------------------------------------------------------- #
brain = Brain()
controller = Controller()

# TEMPORARY BENCH TEST: one large motor on a Motor Controller 55 (MC55), which
# is plugged into Smart Port 1. In code an MC55 is a Motor55, NOT a Motor.
#
# The False is "reversed". The motor is not on the robot yet, so there is no
# right or wrong direction. Once it is, flip this to True if it spins the
# wrong way.
left_motor = Motor55(Ports.PORT1, False)

# TEMPORARY BENCH TEST: one servo on 3-wire port A (the lettered ports on the
# side of the brain). A servo turns to an angle you choose and holds it there.
test_servo = Servo(brain.three_wire_port.a)

# ---------------------------------------------------------------------------- #
# Settings you can tune
#
# Put speeds, timings and other numbers here with a name, instead of typing
# the number in the middle of the code. That way there is one place to change.
# ---------------------------------------------------------------------------- #
# Joystick values smaller than this (in percent) are treated as zero so the
# motor doesn't creep when the stick is centered.
DEADBAND = 5

# TEMPORARY BENCH TEST: the power (in percent) that a full push of the stick
# gives. 100 is full power; 50 would mean full stick runs it at half power.
TEST_MAX_POWER = 100

# TEMPORARY BENCH TEST: how far (in degrees) a full push of the stick turns
# the servo each way from its middle. 50 is the most the brain can ask for.
# The BEST servos may not reach that far: if the servo buzzes or strains at
# the end of its travel, make this number smaller.
SERVO_MAX_DEGREES = 50


# ---------------------------------------------------------------------------- #
# Helpers
#
# Functions that the rest of the code uses go here. These two are copied from
# examples/example.py.
# ---------------------------------------------------------------------------- #
def apply_deadband(value):
    if abs(value) < DEADBAND:
        return 0
    return value


def set_power(motor, percent):
    # Runs one motor at a power from -100 (full reverse) to 100 (full forward).
    #
    # A Motor55 is told how many volts to send, not a percent, so this converts
    # for you. ALWAYS use set_power() instead of calling motor.spin() directly:
    # motor.spin(FORWARD, 50) would ask for 50 volts, not 50 percent.
    if percent > 100:
        percent = 100
    if percent < -100:
        percent = -100

    # get_max_voltage() is the voltage that means 100%, in millivolts.
    max_volts = motor.get_max_voltage() / 1000
    motor.spin(FORWARD, max_volts * percent / 100, VOLT)


# ---------------------------------------------------------------------------- #
# Driver control
#
# TEMPORARY BENCH TEST controls:
#   Left stick up/down (axis 3)      run left_motor, up to TEST_MAX_POWER
#   Right stick left/right (axis 1)  turn test_servo, up to SERVO_MAX_DEGREES
# ---------------------------------------------------------------------------- #
def show_test_numbers(stick, percent, servo_degrees):
    # Prints what the program is doing on the brain screen, so you can tell a
    # wiring problem from a code problem.
    #   MC55 found  False means the brain can't see the MC55 on its port
    #   Max mV      the voltage that means 100%. If this is 0, set_power()
    #               can't work and the motor will not move.
    #   Stick       what the left stick reads, -100 to 100
    #   Power %     what the motor is being told to do
    #   Servo deg   the angle the servo is being told to go to
    brain.screen.clear_row(3)
    brain.screen.set_cursor(3, 1)
    brain.screen.print("MC55 found:", left_motor.installed())
    brain.screen.clear_row(4)
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Max mV:", left_motor.get_max_voltage())
    brain.screen.clear_row(5)
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Stick:", stick, " Power %:", percent)
    brain.screen.clear_row(6)
    brain.screen.set_cursor(6, 1)
    brain.screen.print("Servo deg:", servo_degrees)


def driver_control():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Bench test: L stick motor, R stick servo")

    loops = 0
    while True:
        # --- TEMPORARY BENCH TEST: left stick runs one motor ---
        # The stick reads -100 (pulled all the way back) to 100 (pushed all
        # the way forward). Scale it down so full stick is TEST_MAX_POWER.
        stick = apply_deadband(controller.axis3.position())
        percent = stick * TEST_MAX_POWER / 100
        if percent == 0:
            left_motor.stop()
        else:
            set_power(left_motor, percent)

        # --- TEMPORARY BENCH TEST: right stick left/right moves one servo ---
        # The servo follows the stick: centered stick is the middle (0
        # degrees), full right is SERVO_MAX_DEGREES, full left is the same
        # the other way. Let go and it returns to the middle.
        # If the servo turns the opposite way to the stick, put a minus sign
        # in front of servo_stick on the next line.
        servo_stick = apply_deadband(controller.axis1.position())
        servo_degrees = servo_stick * SERVO_MAX_DEGREES / 100
        test_servo.set_position(servo_degrees, DEGREES)

        # --- Show the numbers about 4 times a second ---
        loops += 1
        if loops >= 12:
            loops = 0
            show_test_numbers(stick, percent, servo_degrees)

        # Give the brain time for other tasks. Every loop should wait a little.
        wait(20, MSEC)


# ---------------------------------------------------------------------------- #
# Competition hookup
# ---------------------------------------------------------------------------- #
def autonomous():
    # Left empty on purpose. This is what field control would run in a game
    # with an autonomous period at the start of the match. Byte to Bite doesn't
    # have one: our autonomous starts from a button inside driver_control().
    pass


# This must stay the last line of the file. With no field control plugged in,
# running the program goes straight to driver_control().
competition = Competition(driver_control, autonomous)
