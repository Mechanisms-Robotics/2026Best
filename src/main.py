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

def driver_control():
    return

def autonomous():
    return

# This must stay the last line of the file. With no field control plugged in,
# running the program goes straight to driver_control().
competition = Competition(driver_control, autonomous)