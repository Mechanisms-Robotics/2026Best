from vex import *
import math

# ---------------------------------------------------------------------------- #
# Devices
#
# Declare every motor and sensor here, once you know which port it is plugged
# into. See the Devices section of examples/example.py for how each one is
# written.
# ---------------------------------------------------------------------------- #
brain = Brain()
controller = Controller()
controller_1 = Controller(PRIMARY)
LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

def driver_control():

    while True:
        left_speed = controller_1.axis3.position()
        right_speed = controller_1.axis2.position()

        LeftMotor.set_velocity(left_speed, PERCENT)
        RightMotor.set_velocity(right_speed, PERCENT)

        LeftMotor.spin(FORWARD)
        RightMotor.spin(FORWARD)

        wait(20, MSEC)
    # global myVariable
    # while True:
    #     LeftMotor.set_velocity(controller_1.axis3.position(), PERCENT)
    #     RightMotor.set_velocity(controller_1.axis2.position(), PERCENT)
    #     LeftMotor.spin(REVERSE)
    #     RightMotor.spin(REVERSE)
    #     wait(5, MSEC)



        

def autonomous():
    return

# This must stay the last line of the file. With no field control plugged in,
# running the program goes straight to driver_control().
competition = Competition(driver_control, autonomous)
