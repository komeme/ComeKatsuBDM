import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

try:
    while True:
        if GPIO.input(24) == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
        else:
            GPIO.output(25, GPIO.LOW)
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()