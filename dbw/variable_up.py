import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set PWM pin
pwm_pin = 12  # Adjust pin number according to your setup

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
        # Gradually increase voltage by 0.15 volts each second
        while desired_voltage < 3.0:
            desired_voltage += 0.15
            if desired_voltage > 3.0:
                desired_voltage = 3.0

            # Update duty cycle
            duty_cycle = (desired_voltage / max_voltage) * 100
            pwm.ChangeDutyCycle(duty_cycle)

            time.sleep(1)  # Wait for one second before increasing again

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
