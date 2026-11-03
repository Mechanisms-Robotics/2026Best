# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Mechanisms Robotics                                          #
#   Description:  2026 BEST robot (Byte to Bite) - VEX V5 Python               #
#                                                                              #
#   This is the program that gets downloaded to the brain.                     #
#                                                                              #
#   This is our tank drive program                                      #
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

# Drive motors. Each one goes through an MC55, so it's a Motor55.
# If one side drives backwards, flip its True/False.
left_motor = Motor55(Ports.PORT1, False)
right_motor = Motor55(Ports.PORT2, True)

# Deadband helps prevent the motors from moving when the controller is near its center position.
DEADBAND = 5

# Runs one motor at a power from -100 (full reverse) to 100 (full forward).
#
# A Motor55 is told how many volts to send, not a percent, so this converts
# for you. ALWAYS use set_power() instead of calling motor.spin() directly:
# motor.spin(FORWARD, 50) would ask for 50 volts, not 50 percent.
def set_power(motor, percent):
    
    if percent > 100:
        percent = 100
    if percent < -100:
        percent = -100

    # get_max_voltage() is the voltage that means 100%, in millivolts.
    max_volts = motor.get_max_voltage() / 1000
    motor.spin(FORWARD, max_volts * percent / 100, VOLT)

def tank_drive(left, right):
    set_power(left_motor, left)
    set_power(right_motor, right)

def apply_deadband(value):
    if abs(value) < DEADBAND:
        return 0
    return value

def driver_control():
    while True:
        left = apply_deadband(controller.axis3.position())
        right = apply_deadband(controller.axis2.position())
        tank_drive(left, right)
        wait(20, MSEC)


def autonomous():
    return

# This must stay the last line of the file. With no field control plugged in,
# running the program goes straight to driver_control().
competition = Competition(driver_control, autonomous)
