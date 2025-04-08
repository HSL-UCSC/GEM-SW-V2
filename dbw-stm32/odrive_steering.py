import time
import odrive
import odrive.enums
from Joystick import Joystick, JoystickConstants

# must not be zero - zero value doesn't work?
# TODO: double check this
DEFAULT_POS = 0
JOY_SCALE = 0.01
MAX_POS = 0.8
MIN_POS = -2.65

# initialize odrive
print("Finding ODrive...")
odrv0 = odrive.find_any(timeout=10)
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

joy = Joystick()
pos = odrv0.axis0.pos_estimate

while True:
    try:
        if odrv0.axis0.active_errors:
            odrv0.clear_errors()
            odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

        j_vals = joy.get_joystick_values()
        if j_vals is None:
            print("No joystick values found")
            continue
        
        if j_vals["buttons"][JoystickConstants.BTN_R_BUMPER]:
            pos += j_vals["axes"][JoystickConstants.AXIS_LX] * JOY_SCALE
            pos = max(MIN_POS, min(MAX_POS, pos))

            if j_vals["buttons"][JoystickConstants.BTN_A]:
                pos = DEFAULT_POS
            elif j_vals["buttons"][JoystickConstants.BTN_B]:
                DEFAULT_POS = pos

            odrv0.axis0.controller.input_pos = pos

        print(
            f"Joystick: {round(j_vals['axes'][JoystickConstants.AXIS_LX], 3)}, Command Pos: {round(pos, 3)}, Actual Pos: {round(odrv0.axis0.pos_estimate, 3)}, Default Pos: {round(DEFAULT_POS, 3)}"
        )
        
        time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
        break


odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
