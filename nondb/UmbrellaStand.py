import RPi.GPIO as GPIO
from TagReader import TagReader

class UmbrellaStand(object):
    def __init__(self):
        self.rooms = []
        self.reader = TagReader()

    def add_room(self, room):
        self.rooms.append(room)
        return

    def remove_room(self, room):
        self.rooms.remove(room)
        return

    def num_rooms(self):
        return len(self.rooms)

    def init_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        for room in self.rooms:
            GPIO.setup(room.switch_PIN, GPIO.IN)
            GPIO.setup(room.locked_PIN, GPIO.OUT)
            GPIO.setup(room.unlocked_PIN, GPIO.OUT)

    def is_registered(self, tag_id):
        for room in self.rooms:
            if room.tag_id == tag_id:
                return room
        else:
            return None

    def wait_switch(self,time):
        for i in range(time):
            


    def read_tag(self):
        tag_id = self.reader.read()
        room = self.is_registered(tag_id)
        if room:
            room.fetch()
        else:
            room.fetch()



