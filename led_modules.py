import RPi.GPIO as GPIO
import time


def unlocked_led(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.HIGH)
    GPIO.output(room_dict['locked_led_port'], GPIO.LOW)


def locked_led(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.LOW)
    GPIO.output(room_dict['locked_led_port'], GPIO.HIGH)

def turn_off_led(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.LOW)
    GPIO.output(room_dict['locked_led_port'], GPIO.LOW)


def turn_on_led(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.HIGH)
    GPIO.output(room_dict['locked_led_port'], GPIO.HIGH)