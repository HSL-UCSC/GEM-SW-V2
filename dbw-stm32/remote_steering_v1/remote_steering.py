import time
from Joystick import Joystick
from serial import Serial

if __name__ == "__main__":
    j = Joystick()
    s = Serial("/dev/tty.usbmodem1203", 115200, timeout=0.1)
    while True:
        vals = j.get_joystick_values()
        if vals and vals["buttons"][0]:
            throttle = int(vals["axes"][2] * 255)
            print(throttle)
            s.write(throttle.to_bytes(1, "big"))
            print(s.read(30))
        # time.sleep(0.1)
