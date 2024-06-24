import RPi.GPIO as GPIO
import keyboard
import time
#change this depending on what adc we end up using
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn
import busio
from board import SCL, SDA

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set PWM pin
pwm_pin = 12  # Adjust pin number according to your setup

# Set PWM frequency (Hz)
frequency = 1000

# Initialize PWM
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, frequency)

# ADC setup
i2c = busio.I2C(SCL, SDA)
ads = ADS1015(i2c)
adc_channel = AnalogIn(ads, ADS1015.P0)  # Use channel 0

# Start PWM at 0.15 volts
desired_voltage = 0.15
max_voltage = 3.3
duty_cycle = (desired_voltage / max_voltage) * 100
pwm.start(duty_cycle)

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

try:
    while True:
        # Read ADC value
        adc_value = adc_channel.voltage

        # Check if ADC value is above 0.15V
        if adc_value > 0.15:
            desired_voltage = adc_value
            print(f"ADC voltage: {adc_value:.2f}V")

        # Calculate duty cycle based on desired voltage
        duty_cycle = (desired_voltage / max_voltage) * 100
        pwm.ChangeDutyCycle(duty_cycle)

        # Manual control
        if adc_value <= 0.15:
            if keyboard.is_pressed('w'):
                increase_voltage()
                duty_cycle = (desired_voltage / max_voltage) * 100
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.1)  # Adjust as needed for responsiveness
            elif keyboard.is_pressed('s'):
                decrease_voltage()
                duty_cycle = (desired_voltage / max_voltage) * 100
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(0.1)  # Adjust as needed for responsiveness

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
