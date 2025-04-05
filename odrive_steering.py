import odrive
import odrive.enums
from Joystick import Joystick

odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

odrv0.clear_errors()
print(odrv0.axis0)
odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL


joy = Joystick()

while True:
    try:
        j_vals = joy.get_joystick_values()
        if j_vals is None:
            print("No joystick values found")
            continue

        odrv0.axis0.controller.input_pos = j_vals["axes"][0]

        # odrv0.axis0.controller.input_pos = 0.01
        # print("Joystick Values: ", joy.get_joystick_values())
        # print("Current Position: ", odrv0.axis0.pos_estimate)
        print(odrv0.axis0.controller.input_pos, odrv0.axis0.pos_estimate)
        if odrv0.axis0.active_errors:
            odrv0.clear_errors()
            odrv0.axis0.requested_state = odrive.enums.AxisState.CLOSED_LOOP_CONTROL
    except KeyboardInterrupt:
        print("Exiting...")
        break

odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
