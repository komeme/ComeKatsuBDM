import RPi.GPIO as GPIO


class Room(object):
    def __init__(self, room_id, switch_PIN, locked_PIN, unlocked_PIN):
        self.room_id = room_id
        self.is_occupied = False
        self.tag_id = None
        self.switch_PIN = switch_PIN
        self.locked_PIN = locked_PIN
        self.unlocked_PIN = unlocked_PIN

    def register(self, tag_id):
        if not self.is_occupied:
            self.is_occupied = True
            self.tag_id = tag_id
        return

    def fetch(self):
        if self.is_occupied:
            self.is_occupied = False
            self.tag_id = None
        return

    def locked_led(self):
        GPIO.output(self.locked_PIN, GPIO.HIGH)
        GPIO.output(self.unlocked_PIN, GPIO.LOW)
        return

    def unlocked_led(self):
        GPIO.output(self.locked_PIN, GPIO.LOW)
        GPIO.output(self.unlocked_PIN, GPIO.HIGH)
        return

    def switch_state(self):
        return GPIO.input(self.switch_PIN) == GPIO.HIGH

