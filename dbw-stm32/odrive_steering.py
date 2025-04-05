import odrive
import odrive.enums
from Joystick import Joystick, JoystickConstants

# must not be zero - zero value doesn't work?
# TODO: double check this
DEFAULT_POS = 1e-3
JOY_SCALE = 1
MAX_POS = 5.0
MIN_POS = -5.0

# initialize odrive
print("Finding ODrive...")
odrv0 = odrive.find_any(timeout=10)
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

joy = Joystick()
pos = DEFAULT_POS

while True:
    try:
        if odrv0.axis0.active_errors:
            odrv0.clear_errors()
            odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

        j_vals = joy.get_joystick_values()
        if j_vals is None:
            print("No joystick values found")
            continue

        pos += j_vals["axes"][JoystickConstants.AXIS_LX] * JOY_SCALE
        pos = max(MIN_POS, min(MAX_POS, pos))

        if j_vals["buttons"][JoystickConstants.BTN_A]:
            pos = DEFAULT_POS
        elif j_vals["buttons"][JoystickConstants.BTN_B]:
            DEFAULT_POS = pos

        odrv0.axis0.controller.input_pos = pos

        print(
            f"Joystick: {round(j_vals['axes'][JoystickConstants.AXIS_LX], 3)}, Pos: {round(pos, 3)}, Default Pos: {round(DEFAULT_POS, 3)}"
        )

    except KeyboardInterrupt:
        print("Exiting...")
        break

odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
