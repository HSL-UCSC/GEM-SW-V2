import time

import odrive
import odrive.enums
from Joystick import Joystick, JoystickConstants
from serial import Serial

# must not be zero - zero value doesn't work?
# TODO: double check this
DEFAULT_STEERING_POS = 1e-3
MAX_STEERING_POS = 5.0
MIN_STEERING_POS = -5.0
MAX_DELTA_STEERING = 0.5

MAX_THROTTLE = 255  # fit in one byte

# initialize odrive
print("Finding ODrive...")
odrv0 = odrive.find_any(timeout=10)
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

j = Joystick()
pos = DEFAULT_STEERING_POS

s = Serial("/dev/tty.usbmodem1203", 115200)

# configure the joystick lx axis for steering
j.REVERSED[JoystickConstants.AXIS_LX] = False
j.SCALE[JoystickConstants.AXIS_LX] = MAX_DELTA_STEERING
j.BIAS[JoystickConstants.AXIS_LX] = 0.0

# configure the joystick ly axis for throttle
j.REVERSED[JoystickConstants.AXIS_LY] = True
j.SCALE[JoystickConstants.AXIS_LY] = MAX_THROTTLE
j.BIAS[JoystickConstants.AXIS_LY] = 0.0

while True:
    try:
        if odrv0.axis0.active_errors:
            odrv0.clear_errors()
            odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

        j_vals = j.get_joystick_values()
        if j_vals is None:
            print("No joystick values found")
            continue

        # get the commanded steering position
        pos += j_vals["axes"][JoystickConstants.AXIS_LX]
        pos = max(MIN_STEERING_POS, min(MAX_STEERING_POS, pos))

        if j_vals["buttons"][JoystickConstants.BTN_A]:
            pos = DEFAULT_STEERING_POS
        elif j_vals["buttons"][JoystickConstants.BTN_B]:
            DEFAULT_STEERING_POS = pos

        # get the commanded throttle
        throttle = int(j_vals["axes"][JoystickConstants.AXIS_LY])
        throttle = max(0, min(MAX_THROTTLE, throttle))

        # send the steering & throttle commands
        odrv0.axis0.controller.input_pos = pos
        s.write(throttle.to_bytes(1, "big"))

        print(
            f"Joystick: {round(j_vals['axes'][JoystickConstants.AXIS_LX], 3)}, Pos: {round(pos, 3)}, Default Pos: {round(DEFAULT_STEERING_POS, 3)}, Throttle: {throttle}"
        )

        # wait for a short time to avoid flooding the serial port
        time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
        break

# stop the odrive & throttle, and close the serial port
odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
s.write(b"\x00")
s.close()
