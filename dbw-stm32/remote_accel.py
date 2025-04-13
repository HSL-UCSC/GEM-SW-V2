import time
from Joystick import Joystick, JoystickConstants
from serial import Serial

if __name__ == "__main__":
    j = Joystick()
    s = Serial("/dev/tty.usbmodem1103", 115200)
    j.REVERSED[JoystickConstants.AXIS_LY] = True
    j.SCALE[JoystickConstants.AXIS_LY] = 255
    while True:
        vals = j.get_joystick_values()
        print(vals)
        if vals and vals["buttons"][JoystickConstants.BTN_R_BUMPER] and vals["axes"][JoystickConstants.AXIS_LY] >= 0.0:
            throttle = int(vals["axes"][JoystickConstants.AXIS_LY])
        else:
            throttle = 0
        print(throttle)
        s.write(throttle.to_bytes(1, "big"))
        time.sleep(0.1)
