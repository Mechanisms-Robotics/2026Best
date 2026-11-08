from vex import *

brain = Brain()

# Servo plugged into 3-Wire port B
servo_b = Servo(brain.three_wire_port.b)

# Move to the center positio

# Move to one side
servo_b.set_position(35, DEGREES)
wait(1, SECONDS)

# Move to the other side
servo_b.set_position(-35, DEGREES)
wait(1, SECONDS)


