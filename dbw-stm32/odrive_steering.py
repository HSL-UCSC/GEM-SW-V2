import time
import odrive
import odrive.enums
from Joystick import Joystick, JoystickConstants

DEFAULT_POS = 0
JOY_SCALE = 0.01
MAX_POS = -0.0
MIN_POS = -1.6

# what portion of the total steering wheel turn ability to use (ex. 0.5 would mean limiting to -50% to 50%)
BOUND = 0.3

# initialize odrive
print("Finding ODrive...")
odrv0 = odrive.find_any(timeout=10)
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

joy = Joystick()
pos = odrv0.axis0.pos_estimate
active = False

while True:
    try:
        if odrv0.axis0.active_errors:
            odrv0.clear_errors()
            # odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL

        j_vals = joy.get_joystick_values()
        if j_vals is None:
            print("No joystick values found")
            continue
        
        if j_vals["buttons"][JoystickConstants.BTN_R_BUMPER]:
            if not active:
                print("Joystick activated")
                odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL
                active = True
            # pos += j_vals["axes"][JoystickConstants.AXIS_LX] * JOY_SCALE
            # pos = max(MIN_POS, min(MAX_POS, pos))

            # if j_vals["buttons"][JoystickConstants.BTN_A]:
            #     pos = DEFAULT_POS
            # elif j_vals["buttons"][JoystickConstants.BTN_B]:
            #     DEFAULT_POS = pos

            pos = (j_vals["axes"][JoystickConstants.AXIS_LX]) * 0.5 * BOUND * (MAX_POS - MIN_POS) + (MAX_POS + MIN_POS) / 2

            odrv0.axis0.controller.input_pos = pos
        else:
            if active:
                print("Joystick deactivated")
                odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
                active = False

        print(
            f"Joystick: {round(j_vals['axes'][JoystickConstants.AXIS_LX], 3)}, Command Pos: {round(pos, 3)}, Actual Pos: {round(odrv0.axis0.pos_estimate, 3)}, Default Pos: {round(DEFAULT_POS, 3)}"
        )
        
        time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
        break


odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
