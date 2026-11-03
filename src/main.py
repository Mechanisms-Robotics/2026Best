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

def set_power(motor, percent):
    if percent > 100:
        percent = 100
    if percent < -100:
        percent = -100

    max_volts = motor.get_max_voltage() / 1000
    motor.spin(FORWARD, max_volts * percent / 100, VOLT)

def tank_drive(left, right):
    set_power(left_motor, left)
    set_power(right_motor, right)

def apply_deadband(value):
    if abs(value) < DEADBAND:
        return 0
    return value
# Drive motors. Each one goes through an MC55, so it's a Motor55.
# If one side drives backwards, flip its True/False.
left_motor = Motor55(Ports.PORT1, False)
right_motor = Motor55(Ports.PORT2, True)

DEADBAND = 5

# copy apply_deadband(), set_power() and tank_drive() from examples/example.py

def driver_control():
    while True:
        left = apply_deadband(controller.axis3.position())
        right = apply_deadband(controller.axis2.position())
        tank_drive(left, right)
        wait(20, MSEC)
#brain = Brain()
#controller = Controller()
#controller = Controller(PRIMARY)
#LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
#RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
#def deadband(value, threshold=DEADBAND):
#    if abs(value) < threshold:
#        return 0
#    return value
#def driver_control():

#    while True:
#        left_speed = deadband(controller.axis3.position())
#        right_speed = deadband(controller.axis2.position())
        
#       wait(20, MSEC)
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
