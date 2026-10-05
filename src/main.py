# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Mechanisms Robotics                                          #
#   Description:  2026 BEST robot (Byte to Bite) - VEX V5 Python               #
#                                                                              #
#   This is the program that gets downloaded to the brain. It starts out       #
#   empty on purpose: it does not move anything yet.                           #
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

# ---------------------------------------------------------------------------- #
# Settings you can tune
#
# Put speeds, timings and other numbers here with a name, instead of typing
# the number in the middle of the code. That way there is one place to change.
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
# Helpers
#
# Functions that the rest of the code uses go here.
#
# Before you run a motor, copy set_power() from examples/example.py and use
# it. Calling motor.spin(FORWARD, 50) directly asks for 50 VOLTS, not 50
# percent.
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Driver control
# ---------------------------------------------------------------------------- #
def driver_control():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Driver control")

    while True:
        # Read the controller and run the motors here.

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
