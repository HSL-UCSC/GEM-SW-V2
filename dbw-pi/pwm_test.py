import time

import RPi.GPIO as GPIO  # type: ignore

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set PWM pin
pwm_pin = 12  # Adjust pin number according to your setup

# Set PWM frequency (Hz)
frequency = 1000

# Initialize PWM
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, frequency)

try:
    # Start PWM at 0.15 volts
    desired_voltage = 0.15
    max_voltage = 3.3
    duty_cycle = (desired_voltage / max_voltage) * 100
    pwm.start(duty_cycle)

    while True:
        # Wait for user input
        input("Press Enter to set voltage to 3 volts: ")

        # Set voltage to 3 volts
        desired_voltage = 3.0
        duty_cycle = (desired_voltage / max_voltage) * 100
        pwm.ChangeDutyCycle(duty_cycle)

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
