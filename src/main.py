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

servo_a = Servo(brain.three_wire_port.a)
servo_b = Servo(brain.three_wire_port.b)
servo_c = Servo(brain.three_wire_port.c)
left_motor = Motor55(Ports.PORT1, False)
right_motor = Motor55(Ports.PORT2, True)
fork_motor = Motor55(Ports.PORT3, True)
fork_motor.set_stopping(HOLD)
elapsed_time = Timer()

# Deadband helps prevent the motors from moving when the controller is near its center position.
DEADBAND = 5
SERVO_A_DEPLOYED_POSITION = 70
SERVO_A_INITIAL_POSITION = 0
SERVO_B_DEPLOYED_POSITION = 70
SERVO_B_INITIAL_POSITION = 0
FORKLIFT_UP_POWER = 100
FORKLIFT_DOWN_POWER = -100
FORKLIFT_UP_POWER_SLOW = 30
FORKLIFT_DOWN_POWER_SLOW = -20
FORKLIFT_HOLD_POWER = 0
JITTER_SPEED_UP = 30
JITTER_SPEED_DOWN = 45

def set_power(motor, percent):
    if percent > 100:
        percent = 100
    if percent < -100:
        percent = -100
    max_volts = motor.get_max_voltage() / 1000
    motor.spin(FORWARD, max_volts * percent / 100, VOLT)

def deploy_servo(servo_motor, position):
    servo_motor.set_position(position, DEGREES)

def tank_drive(left, right):
    set_power(left_motor, left)
    set_power(right_motor, right)

def apply_deadband(value):
    if abs(value) < DEADBAND:
        return 0
    return value
def jitter_fork_forward(jitter_speed):
    fork_motor.spin(FORWARD, jitter_speed, VOLT)
    wait(20, MSEC)
    fork_motor.stop()

def jitter_fork_reverse(jitter_speed):
    fork_motor.spin(REVERSE, jitter_speed, VOLT)
    wait(20, MSEC)
    fork_motor.stop()
    
def driver_control():
    while True:
        #drive
        left = apply_deadband(controller.axis3.position())
        right = apply_deadband(controller.axis2.position())
        tank_drive(left, right)

        # forklift
        if controller.buttonR1.pressing():
            set_power(fork_motor, FORKLIFT_UP_POWER)
        elif controller.buttonR2.pressing():
            set_power(fork_motor, FORKLIFT_DOWN_POWER)
        elif controller.buttonL1.pressing():
            set_power(fork_motor, FORKLIFT_UP_POWER_SLOW)
        elif controller.buttonL2.pressing():
            set_power(fork_motor, FORKLIFT_DOWN_POWER_SLOW)
        else:
            set_power(fork_motor, FORKLIFT_HOLD_POWER)

        if controller.buttonB.pressing():
                jitter_fork_forward(JITTER_SPEED_UP)
                jitter_fork_reverse(JITTER_SPEED_DOWN)
        
        wait(20, MSEC)

def autonomous():
    return

controller.buttonA.pressed(deploy_servo, (servo_a, SERVO_A_DEPLOYED_POSITION))
controller.buttonX.pressed(deploy_servo, (servo_a, -SERVO_A_DEPLOYED_POSITION))
controller.buttonY.pressed(deploy_servo, (servo_a, SERVO_A_INITIAL_POSITION))
controller.buttonRight.pressed(deploy_servo, (servo_b, SERVO_B_DEPLOYED_POSITION))
controller.buttonLeft.pressed(deploy_servo, (servo_b, -SERVO_B_DEPLOYED_POSITION))
controller.buttonUp.pressed(deploy_servo, (servo_b, SERVO_B_INITIAL_POSITION))

competition = Competition(driver_control, autonomous)