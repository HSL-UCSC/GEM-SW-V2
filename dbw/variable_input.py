import RPi.GPIO as GPIO
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

# Start PWM at 0.15 volts
desired_voltage = 0.15
max_voltage = 3.3
duty_cycle = (desired_voltage / max_voltage) * 100
pwm.start(duty_cycle)

try:
    while True:
        # Check for keyboard input
        key_input = input("Press 'w' to increase voltage, 's' to decrease, or 'q' to quit: ")

        if key_input == 'w':
            # Increase voltage
            desired_voltage += 0.1
            if desired_voltage > 3.0:
                desired_voltage = 3.0
            duty_cycle = (desired_voltage / max_voltage) * 100
            pwm.ChangeDutyCycle(duty_cycle)
        elif key_input == 's':
            # Decrease voltage
            desired_voltage -= 0.1
            if desired_voltage < 0.15:
                desired_voltage = 0.15
            duty_cycle = (desired_voltage / max_voltage) * 100
            pwm.ChangeDutyCycle(duty_cycle)
        elif key_input == 'q':
            # Quit the program
            break
        else:
            print("Invalid input. Press 'w' to increase voltage, 's' to decrease, or 'q' to quit.")

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
