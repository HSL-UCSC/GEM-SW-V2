import time
from Joystick import Joystick
from serial import Serial

if __name__ == "__main__":
    j = Joystick()
    s = Serial("/dev/tty.usbmodem1203", 115200)
    while True:
        vals = j.get_joystick_values()
        if vals and vals["buttons"][0] and vals["axes"][1] >= 0.0:
            throttle = int(vals["axes"][1] * 255)
        else:
            throttle = 0
        print(throttle)
        s.write(throttle.to_bytes(1, "big"))
        time.sleep(0.1)
