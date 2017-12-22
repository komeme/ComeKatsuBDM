import RPi.GPIO as GPIO


def unlocked(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.HIGH)
    GPIO.output(room_dict['locked_led_port'], GPIO.LOW)


def locked(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.LOW)
    GPIO.output(room_dict['locked_led_port'], GPIO.HIGH)


def turn_off(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.LOW)
    GPIO.output(room_dict['locked_led_port'], GPIO.LOW)


def turn_on(room_dict):
    GPIO.output(room_dict['unlocked_led_port'], GPIO.HIGH)
    GPIO.output(room_dict['locked_led_port'], GPIO.HIGH)
