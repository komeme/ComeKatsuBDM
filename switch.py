import RPi.GPIO as GPIO
import time
import requests


base_url = "https://umbrella-stand-server.herokuapp.com"


def put():
    empty_rooms = requests.get(base_url + "rooms/empty")
    for i in range(200):
        for empty_room in empty_rooms:
            if GPIO.input(empty_room['switch_port']) == GPIO.HIGH:
                return empty_room
        time.sleep(0.1)
    return False


def take(room):
    for i in range(200):
        if GPIO.input(room['switch_port']) == GPIO.LOW:
            return True
        time.sleep(0.1)

    return False
