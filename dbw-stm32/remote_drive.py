import time

import odrive
import odrive.enums
import threading
from Joystick import Joystick, JoystickConstants
from serial import Serial

MAX_POS = None
CENTER_POS = None
MIN_POS = None
MAX_DELTA_POS = 0.05

# what portion of the total steering wheel turn ability to use (ex. 0.5 would mean limiting to -50% to 50%)
BOUND = 0.7

# maximum throttle value (255 is the maximum for a byte, lower values to limit the throttle)
MAX_THROTTLE = 255

# initialize odrive
print("Finding ODrive...")
odrv0 = odrive.find_any(timeout=10)
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE

# calibrate the odrive (get the min and max positions)
print("Please turn the steering wheel all the way to the left and right to calibrate.")
print("Press Enter when done...")

finish_calibration = False
pos_vals = []


# wait for the user to press Enter to finish calibration
def wait_for_calibration():
    global finish_calibration
    input()
    finish_calibration = True


t = threading.Thread(target=wait_for_calibration).start()
while not finish_calibration:
    pos_vals.append(odrv0.axis0.pos_estimate)

# calculate the min and max positions
MIN_POS = min(pos_vals)
MAX_POS = max(pos_vals)
print(f"Min pos: {MIN_POS}, Max pos: {MAX_POS}")

# get the center position
print("Please turn the steering wheel to the center position.")
print("Press Enter when done...")
input()  # wait for Enter
CENTER_POS = odrv0.axis0.pos_estimate
print(f"Center pos: {CENTER_POS}")

# initialize the joystick
j = Joystick()
if not j.active:
    print("No joystick found, exiting...")
    exit(1)

pos = 0.0
last_pos = odrv0.axis0.pos_estimate
throttle = 0
active = False

# open the serial port for the throttle
try:
    s = Serial("/dev/tty.usbmodem1103", 115200)
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# configure the joystick rx axis for steering
j.REVERSED[JoystickConstants.AXIS_RX] = False
j.SCALE[JoystickConstants.AXIS_RX] = BOUND
j.BIAS[JoystickConstants.AXIS_RX] = 0.0

# configure the joystick ly axis for throttle
j.REVERSED[JoystickConstants.AXIS_LY] = True
j.SCALE[JoystickConstants.AXIS_LY] = MAX_THROTTLE
j.BIAS[JoystickConstants.AXIS_LY] = 0.0

try:
    while True:
        try:
            # if there are any odrive errors, clear them and set the requested state depending on active/inactive state
            if odrv0.axis0.active_errors:
                print("ODrive errors detected, clearing...")
                odrv0.clear_errors()
                odrv0.axis0.requested_state = (
                    odrive.enums.AxisState.CLOSED_LOOP_CONTROL
                    if active
                    else odrive.enums.AxisState.IDLE
                )

            # get the joystick values, skip if not available
            j_vals = j.get_joystick_values()
            if j_vals is None:
                print("No joystick values found")
                continue

            # get the commanded steering position
            if j_vals["buttons"][JoystickConstants.BTN_R_BUMPER]:
                # if bumper was just pressed (previously inactive), activate steering
                if not active:
                    print("Joystick activated")
                    odrv0.axis0.requested_state = (
                        odrive.enums.AxisState.CLOSED_LOOP_CONTROL
                    )
                    active = True

                # get joystick steering axis
                pos = j_vals["axes"][JoystickConstants.AXIS_RX]

                # scale the joystick value to the steering range (different for right and left of center)
                if pos > 0:
                    pos *= MAX_POS - CENTER_POS
                elif pos < 0:
                    pos *= CENTER_POS - MIN_POS

                pos += CENTER_POS

                # limit the change in steering position to avoid sudden jumps
                if abs(pos - last_pos) > MAX_DELTA_POS:
                    pos = last_pos + (
                        MAX_DELTA_POS if pos > last_pos else -MAX_DELTA_POS
                    )
                last_pos = pos

                # limit the steering position to the range (just in case)
                pos = max(MIN_POS, min(MAX_POS, pos))

                # send steering command
                odrv0.axis0.controller.input_pos = pos

                # get the joystick throttle axis
                throttle = int(j_vals["axes"][JoystickConstants.AXIS_LY])

                # bound the throttle to the range
                throttle = max(0, min(MAX_THROTTLE, throttle))

                # send throttle command
                s.write(throttle.to_bytes(1, "big"))

            else:
                # if the bumper is not pressed but the system was active (bumper was just released) deactivate steering
                if active:
                    print("Joystick deactivated")
                    odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
                    active = False

                # stop the throttle
                s.write(b"\x00")

            print(
                f"Active: {'yes' if active else ' no'}, Steering: {round(pos, 3)}, Throttle: {throttle}, Actual Pos: {round(odrv0.axis0.pos_estimate, 3)}"
            )

            # wait for a short time to avoid flooding the serial port
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Exiting...")
            break
except Exception as e:
    print(f"Exception occurred: {e}")

# stop the odrive & throttle, and close the serial port
odrv0.axis0.requested_state = odrive.enums.AxisState.IDLE
s.write(b"\x00")
s.close()
