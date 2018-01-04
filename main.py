import subprocess

import led
import tag
import switch
import RPi.GPIO as GPIO
import sound
import threading
import time
import requests
import json


flag = -1
base_url = "https://umbrella-stand-server.herokuapp.com"


class AlertThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        rooms = requests.get(base_url + "/rooms")

        GPIO.setmode(GPIO.BCM)
        for room in rooms:
            GPIO.setup(room['switch_port'], GPIO.IN)

        while True:
            occupied_rooms = requests.get(base_url + "/rooms/occupied")
            for occupied_room in occupied_rooms:
                if GPIO.input(occupied_room['switch_port']) == GPIO.LOW and flag != occupied_room["id"]:
                    sound.alert()
            time.sleep(0.5)

    def stop(self):
        self.stop_event.set()
        self.thread.join()


def unlock(room):
    led.unlocked(room)
    flag = room['id']
    if switch.take(room):
        requests.get(base_url + "/rooms/" + str(room["id"]) + "/umbrella/take")
        led.turn_off(room)
        print "umbrella is successfully fetched"
    else:
        led.locked(room)
        print "umbrella is not fetched"
    flag = -1

def register(tag_id):
    room = switch.put()
    if room is False:
        return
    requests.post(base_url + "/rooms/" + str(room["id"]) + "/umbrella", data=json.dumps({"tag_id": tag_id}))
    led.locked(room)
    print "umbrella is successfully registered"


def prepare():
    # gpio
    GPIO.setmode(GPIO.BCM)
    rooms = requests.get(base_url + "/rooms").json()
    for room in rooms:
        GPIO.setup(room["locked_led_port"], GPIO.OUT)
        GPIO.setup(room["unlocked_led_port"], GPIO.OUT)
        GPIO.setup(room["switch_port"], GPIO.IN)
        led.turn_off(room)
    # sound
    subprocess.call("sudo amixer cset numid=3 1", shell=True)


try:
    prepare()
    reader = tag.TagReader()
    at = AlertThread()
    at.start()
    print "start!"
    while True:
        tapped_tag_id = reader.read()
        is_in_room = requests.get(base_url + "/is_in_room", params={"tag_id": tapped_tag_id}).json()
        if is_in_room["in_room"]:
            unlock(is_in_room["room"])
        else:
            register(tapped_tag_id)
        print "--------------------"


except KeyboardInterrupt:
    at.stop()
    print "\nexit"
