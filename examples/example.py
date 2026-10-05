# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       example.py                                                   #
#   Author:       Mechanisms Robotics                                          #
#   Description:  2026 BEST robot (Byte to Bite) - VEX V5 Python examples      #
#                                                                              #
#   This file is NOT downloaded to the brain. The robot runs src/main.py.      #
#   Copy the parts you need from here into src/main.py.                        #
#                                                                              #
#   This file is a starting framework, not a finished robot. Anything marked   #
#   CHANGE ME is a guess that has to be replaced once the robot is designed    #
#   and wired. The EXAMPLE functions show how each part works so you can       #
#   write your own.                                                            #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# ---------------------------------------------------------------------------- #
# Devices
# ---------------------------------------------------------------------------- #
brain = Brain()
controller = Controller()

# The kit has four 2-wire motors (two large, two small). Each one plugs into a
# Motor Controller 55 (MC55), and the MC55 plugs into a numbered Smart Port on
# the brain. In code an MC55 is a Motor55, NOT a Motor.
#
# CHANGE ME: the port numbers, which motor does which job, and the True/False.
# The True/False is "reversed": if a motor spins the wrong way, flip it.
left_motor = Motor55(Ports.PORT1, False)
right_motor = Motor55(Ports.PORT10, True)
motor_3 = Motor55(Ports.PORT2, False)   # not used for driving yet - rename it!
motor_4 = Motor55(Ports.PORT9, False)   # not used for driving yet - rename it!

# Every motor on the robot. stop_all() uses this list, so add new motors here.
ALL_MOTORS = [left_motor, right_motor, motor_3, motor_4]

# AI Vision Sensor (Smart Port). It can see the fiducials (AprilTags) on the
# Dining Room walls and tables. Byte to Bite uses the "Circle21h7" tag family.
# docs/fiducial-map.md shows which ID number is on which wall or table.
# CHANGE ME: the port number.
ai_vision = AiVision(Ports.PORT5, AiVision.ALL_TAGS)
ai_vision.set_tag_family(AiVision.TAG_CIRCLE21H7)
ai_vision.tag_detection(True)

# BEST IR Sensor Kit (3-wire port, the lettered ports A-H on the brain).
# CHANGE ME: the port letter. We have not tested this sensor yet, so we do not
# know what numbers it gives. Read it as a plain analog input (0 to 100
# percent) and watch the brain screen to learn what it does.
ir_sensor = AnalogIn(brain.three_wire_port.a)

# The kit also has servos, microswitches and potentiometers. They all use the
# 3-wire ports. One of each is set up here as an example.
# CHANGE ME: the port letters and the names. Delete the ones you don't use and
# copy a line to add more.
#
# Servo: turns to an angle you choose and holds it (good for a claw or latch).
example_servo = Servo(brain.three_wire_port.b)
# Microswitch: a small button the robot presses when a part reaches the end of
# its travel. It only knows "pressed" or "not pressed".
example_switch = Limit(brain.three_wire_port.c)
# Potentiometer: a knob that reports what angle it is turned to. Bolt it to an
# arm's pivot and the robot can tell where the arm is.
example_pot = Potentiometer(brain.three_wire_port.d)

# ---------------------------------------------------------------------------- #
# Settings you can tune
# ---------------------------------------------------------------------------- #
# Joystick values smaller than this (in percent) are treated as zero so the
# robot doesn't creep when the sticks are centered.
DEADBAND = 5

# Power (in percent) for the two extra motors when their buttons are held.
MOTOR_3_POWER = 50
MOTOR_4_POWER = 50

# Servo positions in degrees. The range is -50 to 50, with 0 in the middle.
# The BEST servos may not reach the full range - find the real limits by test.
SERVO_POSITION_1 = -40
SERVO_POSITION_2 = 40

# How close (in degrees) the potentiometer has to be to count as "there".
POT_TOLERANCE_DEGREES = 5

# The AI Vision Sensor's picture is 320 pixels wide, so 160 is straight ahead.
CAMERA_CENTER_X = 160
# How many pixels off-center still counts as "pointing at the tag".
TAG_CENTERED_PIXELS = 15


# ---------------------------------------------------------------------------- #
# Motor helpers
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


def drive(forward, turn):
    # Arcade drive: forward and turn are both -100 to 100.
    set_power(left_motor, forward + turn)
    set_power(right_motor, forward - turn)


def stop_all():
    for motor in ALL_MOTORS:
        motor.stop()


# ---------------------------------------------------------------------------- #
# Sensor helpers
#
# There are no encoders in the kit, so the robot can NOT measure how far its
# wheels have turned. These sensors are the only way it can know anything:
#   AI Vision Sensor  where a fiducial is (so where the robot is pointing)
#   IR sensor         not tested yet
#   microswitch       whether a part has reached the end of its travel
#   potentiometer     what angle an arm or joint is at
# ---------------------------------------------------------------------------- #
def read_ir():
    # Returns the IR sensor reading from 0 to 100 percent.
    return ir_sensor.value(PERCENT)


def find_tag(tag_id):
    # Looks for one fiducial (AprilTag) by its ID number.
    # Returns the tag if the camera can see it, or None if it can't.
    #
    # Useful things you can read from the tag that comes back:
    #   tag.id       the ID number printed on the fiducial sheet
    #   tag.centerX  where it is left/right in the picture (0 to 320)
    #   tag.centerY  where it is up/down in the picture (0 to 240)
    #   tag.width    how wide it looks in pixels - bigger means closer
    for tag in ai_vision.take_snapshot(AiVision.ALL_TAGS):
        if tag.id == tag_id:
            return tag
    return None


def visible_tag_ids():
    # Returns a list of the ID numbers of every tag the camera sees right now.
    ids = []
    for tag in ai_vision.take_snapshot(AiVision.ALL_TAGS):
        ids.append(tag.id)
    return ids


def show_sensors():
    # Prints live sensor readings on the brain screen. Point the camera at a
    # fiducial or put something in front of the IR sensor and watch the numbers
    # change - this is how you find out what values to use in your code.
    brain.screen.clear_row(3)
    brain.screen.set_cursor(3, 1)
    brain.screen.print("IR sensor:", read_ir())
    brain.screen.clear_row(4)
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Tags seen:", visible_tag_ids())
    brain.screen.clear_row(5)
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Switch:", example_switch.pressing(),
                       " Pot deg:", example_pot.angle(DEGREES))


# ---------------------------------------------------------------------------- #
# Autonomous building blocks
#
# In Byte to Bite, autonomous is NOT a period at the start of the match. The
# driver presses a button during the match, puts the controller down
# ("hands-free"), and the robot works on its own inside the Dining Room. The
# robot may only be in the Dining Room while it is driving itself.
#
# Every autonomous step below keeps checking the cancel button. Pressing it
# stops the robot at once and gives control back to the driver. The rules let
# the team abandon an autonomous run at any time and drive out by hand.
#
# Use auto_wait() instead of wait() inside autonomous code. A plain wait()
# cannot be cancelled, so the robot would keep moving with nobody in control.
# ---------------------------------------------------------------------------- #
class AutoCancelled(Exception):
    # Raised when the driver cancels. Like a Java exception, it jumps straight
    # out of whatever step was running, back to run_autonomous().
    pass


def check_cancel():
    # CHANGE ME: which button cancels autonomous.
    if controller.buttonB.pressing():
        raise AutoCancelled()


def auto_wait(time_ms):
    # Waits like wait(time_ms, MSEC), but stops early if the driver cancels.
    waited = 0
    while waited < time_ms:
        check_cancel()
        wait(20, MSEC)
        waited += 20


def auto_drive(forward, turn, time_ms):
    # Drives at the given powers for a set time, then stops.
    # Timed driving is not exact: the robot goes farther on a full battery and
    # on a smooth floor. Test on the real field and expect to re-tune.
    drive(forward, turn)
    auto_wait(time_ms)
    drive(0, 0)


def auto_turn_to_tag(tag_id, turn_power, timeout_ms):
    # EXAMPLE of using a sensor instead of a timer: turn until the camera is
    # pointing straight at a tag. Returns True if it got there, or False if it
    # ran out of time (so your routine can decide what to do next).
    waited = 0
    while waited < timeout_ms:
        check_cancel()
        tag = find_tag(tag_id)
        if tag is None:
            # Can't see it yet - keep turning to look for it.
            drive(0, turn_power)
        else:
            error = tag.centerX - CAMERA_CENTER_X
            if abs(error) <= TAG_CENTERED_PIXELS:
                drive(0, 0)
                return True
            # Tag is to the right of center -> turn right, and the other way
            # around. If the robot turns AWAY from the tag, swap these.
            if error > 0:
                drive(0, turn_power)
            else:
                drive(0, -turn_power)
        wait(20, MSEC)
        waited += 20
    drive(0, 0)
    return False


def auto_run_until_switch(motor, percent, timeout_ms):
    # EXAMPLE of using a microswitch: run a motor until the switch is pressed,
    # then stop it. Returns True if the switch was pressed, or False if it ran
    # out of time. The timeout matters - without it, a broken or unplugged
    # switch would leave the motor pushing forever.
    set_power(motor, percent)
    waited = 0
    while waited < timeout_ms:
        check_cancel()
        if example_switch.pressing():
            motor.stop()
            return True
        wait(20, MSEC)
        waited += 20
    motor.stop()
    return False


def auto_move_to_angle(motor, percent, target_degrees, timeout_ms):
    # EXAMPLE of using a potentiometer: run a motor until the potentiometer
    # reads the angle you asked for. Returns True if it got there, or False if
    # it ran out of time.
    #
    # This assumes positive power makes the angle go UP. If the arm runs away
    # from the target instead, swap the two set_power lines.
    waited = 0
    while waited < timeout_ms:
        check_cancel()
        error = target_degrees - example_pot.angle(DEGREES)
        if abs(error) <= POT_TOLERANCE_DEGREES:
            motor.stop()
            return True
        if error > 0:
            set_power(motor, percent)
        else:
            set_power(motor, -percent)
        wait(20, MSEC)
        waited += 20
    motor.stop()
    return False


def example_routine():
    # EXAMPLE ONLY - this does not score anything. It shows how steps go
    # together: one after another, top to bottom. Replace it with your own.
    auto_drive(40, 0, 1000)                  # forward for 1 second
    if auto_turn_to_tag(1, 20, 3000):        # look for tag 1 for up to 3 s
        brain.screen.print(" found tag 1")
    auto_drive(-40, 0, 1000)                 # back up for 1 second


def run_autonomous(routine):
    # Runs one autonomous routine safely. No matter how the routine ends -
    # finished, cancelled, or crashed - every motor is stopped afterwards.
    brain.screen.clear_row(2)
    brain.screen.set_cursor(2, 1)
    brain.screen.print("AUTO running (B = cancel)")
    try:
        routine()
        brain.screen.print(" done")
    except AutoCancelled:
        brain.screen.print(" CANCELLED")
    finally:
        stop_all()


# ---------------------------------------------------------------------------- #
# Driver control
#
# CHANGE ME: every control here is a starting guess. Keep the table of controls
# in AGENTS.md up to date when you change them.
#   Left stick up/down (axis 3)     drive forward/back
#   Right stick left/right (axis 1) turn
#   L1 / L2                         motor_3 forward / reverse
#   R1 / R2                         motor_4 forward / reverse
#   X / Y                           example servo to position 1 / position 2
#   A                               start the autonomous routine
#   B                               cancel the autonomous routine
# ---------------------------------------------------------------------------- #
def driver_control():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Driver control (A = auto)")

    loops = 0
    while True:
        # --- Driving ---
        forward = apply_deadband(controller.axis3.position())
        turn = apply_deadband(controller.axis1.position())
        drive(forward, turn)

        # --- Extra motors: run while a button is held, stop when let go ---
        if controller.buttonL1.pressing():
            set_power(motor_3, MOTOR_3_POWER)
        elif controller.buttonL2.pressing():
            set_power(motor_3, -MOTOR_3_POWER)
        else:
            motor_3.stop()

        if controller.buttonR1.pressing():
            set_power(motor_4, MOTOR_4_POWER)
        elif controller.buttonR2.pressing():
            set_power(motor_4, -MOTOR_4_POWER)
        else:
            motor_4.stop()

        # --- Servo: goes to a position and stays there ---
        if controller.buttonX.pressing():
            example_servo.set_position(SERVO_POSITION_1, DEGREES)
        elif controller.buttonY.pressing():
            example_servo.set_position(SERVO_POSITION_2, DEGREES)

        # --- Start autonomous ---
        if controller.buttonA.pressing():
            run_autonomous(example_routine)
            # Wait for A to be let go so the routine doesn't start again.
            while controller.buttonA.pressing():
                wait(20, MSEC)
            brain.screen.clear_row(2)

        # --- Show sensor readings about 4 times a second ---
        loops += 1
        if loops >= 12:
            loops = 0
            show_sensors()

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
