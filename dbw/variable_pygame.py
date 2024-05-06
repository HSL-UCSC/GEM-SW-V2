import RPi.GPIO as GPIO
import pygame
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

# Initialize pygame
pygame.init()

# Set screen size (required for pygame)
pygame.display.set_mode((100, 100))

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
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # Increase voltage while 'w' key is held
                    while pygame.key.get_pressed()[pygame.K_w]:
                        increase_voltage()
                        duty_cycle = (desired_voltage / max_voltage) * 100
                        pwm.ChangeDutyCycle(duty_cycle)
                        time.sleep(0.1)  # Adjust as needed for responsiveness
                elif event.key == pygame.K_s:
                    # Decrease voltage while 's' key is held
                    while pygame.key.get_pressed()[pygame.K_s]:
                        decrease_voltage()
                        duty_cycle = (desired_voltage / max_voltage) * 100
                        pwm.ChangeDutyCycle(duty_cycle)
                        time.sleep(0.1)  # Adjust as needed for responsiveness

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
