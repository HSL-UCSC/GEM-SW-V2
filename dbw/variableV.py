# code to send a variable voltage between 0.15 and 3.3V to accelerater pins on GEM DBW
# done via Jetson Nano GPIO pins
# results in plot of variable voltage vs. time
import Jetson.GPIO as GPIO
import tkinter as tk
import threading
import sys
import time
# import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT, initial=GPIO.HIGH)

pwm_pin = 33
pwm_freq = 1000
# set up GPIO
pwm = GPIO.PWM(pwm_pin, pwm_freq)
pwm.start(0)

def set_duty_cycle(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)

def set_voltage(voltage):
    duty_cycle = (voltage - 0.15) / (3.3 - 0.15) * 100
    set_duty_cycle(duty_cycle)
    print(f"Set voltage to {voltage}V\n")

def go():
    # start pwm
    set_voltage(3)
    print("Going\n")

def stop():
    set_voltage(0.15)
    print("Stopping\n")

def key_press(event):
    key = event.char
    if key in key_commands:
        key_commands[key]()

key_commands = {
    "w": lambda: go(),
    "s": lambda: stop()
}

window = tk.Tk()
window.title("Discrete Voltage Control")

instructions_label = tk.Label(window, text="Hold 'w' or 's' to execute commands")
instructions_label.pack()

window.bind("<KeyPress>", key_press)


# set up plot
# plt.ion()
# fig, ax = plt.subplots()
# line, = ax.plot([], [])
# ax.set_xlim(0, 10)
# ax.set_ylim(0, 3.3)
# ax.set_xlabel('Time (s)')
# ax.set_ylabel('Voltage (V)')
# ax.set_title('Variable Voltage vs. Time')

# def update_plot(voltage):
#     line.set_xdata(list(range(len(voltage))))
#     line.set_ydata(voltage)
#     ax.relim()
#     ax.autoscale_view()
#     plt.draw()
#     plt.pause(0.01)

# def plot_update_loop():
#     voltage_data = []
#     while True:
#         voltage = (3.3 - 0.15) * pwm._dc / 100 + 0.15
#         voltage_data.append(voltage)
#         update_plot(voltage_data)
#         time.sleep(0.01)

# plot_thread = threading.Thread(target=plot_update_loop)
# plot_thread.daemon = True
# plot_thread.start()

# start gui
window.mainloop()

# clean up
GPIO.cleanup()
