import sys
import threading
import time
import tkinter as tk

import RPi.GPIO as GPIO  # type: ignore

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)


def go():
    GPIO.output(7, GPIO.HIGH)
    print("speeeeed")


def stop():
    GPIO.output(7, GPIO.LOW)
    print("stop")


# Dictionary to store key-command mappings
key_commands = {"w": lambda: go(), "s": lambda: stop()}


# Function to execute commands based on the pressed key
def execute_commands(key):
    global key_commands
    if key in key_commands:
        key_commands[key]()  # Call the command function for the pressed key


# Function to handle key press events
def on_key_press(event):
    key = event.char.lower()  # Convert to lowercase for case-insensitive detection
    threading.Thread(target=execute_commands, args=(key,)).start()


# Create the main window
window = tk.Tk()
window.title("W and S Key Detection")

# Label to display instructions
instructions_label = tk.Label(window, text="Hold 'w' or 's' to execute commands")
instructions_label.pack()

# Start listening for key events
window.bind("<KeyPress>", on_key_press)

# Keep the window open and running
window.mainloop()
GPIO.cleanup()
