import RPi.GPIO as GPIO
import keyboard
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set PWM pin
pwm_pin = 18  # Adjust pin number according to your setup

# Set PWM frequency (Hz)
frequency = 1000

# Initialize PWM
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, frequency)

# Function to increase voltage
def increase_voltage():
    global desired_voltage
    desired_voltage += 0.1
    if desired_voltage > 3.0:
        desired_voltage = 3.0

# Function to decrease voltage
def decrease_voltage():
    global desired_voltage
    desired_voltage -= 0.1
    if desired_voltage < 0.15:
        desired_voltage = 0.15

# Start PWM at 0.15 volts
desired_voltage = 0.15
max_voltage = 3.3
duty_cycle = (desired_voltage / max_voltage) * 100
pwm.start(duty_cycle)

try:
    while True:
        if keyboard.is_pressed('w'):
            # Increase voltage while 'w' key is held
            increase_voltage()
            duty_cycle = (desired_voltage / max_voltage) * 100
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)  # Adjust as needed for responsiveness
        elif keyboard.is_pressed('s'):
            # Decrease voltage while 's' key is held
            decrease_voltage()
            duty_cycle = (desired_voltage / max_voltage) * 100
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)  # Adjust as needed for responsiveness

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
