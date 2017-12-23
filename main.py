import pymysql.cursors
import led
import tag
import switch
import RPi.GPIO as GPIO
import sound
import threading
import time


connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )

flag = -1

class AlertThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        with connection.cursor() as cursor:
            sql = "select * from rooms"
            cursor.execute(sql)
            rooms = cursor.fetchall()

        GPIO.setmode(GPIO.BCM)
        for room in rooms:
            GPIO.setup(room['switch_port'], GPIO.IN)

        while True:
            with connection.cursor() as cursor:
                sql = "select * from rooms join umbrellas on rooms.id = umbrellas.room_id where umbrellas.in_room = true"
                cursor.execute(sql)
                occupied_rooms = cursor.fetchall()

            empty_rooms = []
            for room in rooms:
                if all([room["id"] != occupied_room["id"] for occupied_room in occupied_rooms]):
                    empty_rooms.append(room)

            for empty_room in empty_rooms:
                if GPIO.input(empty_room['switch_port']) == GPIO.LOW and flag != empty_room["id"]:
                    sound.alert()

            time.sleep(0.5)


def get_registered_room(umbrella):
    with connection.cursor() as cursor:
        sql = "select * from rooms where id=%s"
        cursor.execute(sql, (umbrella["room_id"],))
        rooms = cursor.fetchall()
    if len(rooms) == 0:
        print "room not found!!"
        return False
    return rooms[0]


def register_nfc(tag_id):
    with connection.cursor() as cursor:
        insert_sql = "insert into nfcs (`tag_id`) values (%s)"
        cursor.execute(insert_sql, (tag_id,))
    connection.commit()


def get_registered_umbrella(nfc):
    with connection.cursor() as cursor:
        sql = "select * from umbrellas where nfc_id=%s and in_room = True"
        cursor.execute(sql, (nfc["id"],))
        return cursor.fetchone()


def get_registered_nfc(tag_id):
    with connection.cursor() as cursor:
        sql = "select * from nfcs where tag_id=%s"
        cursor.execute(sql, (tag_id,))
        nfcs = cursor.fetchall()
    if len(nfcs) == 0:
        return False
    return nfcs[0]


def unlock(nfc):
    umbrella = get_registered_umbrella(nfc)
    room = get_registered_room(umbrella)
    led.unlocked(room)
    flag = room['id']
    if switch.take(room):
        with connection.cursor() as cursor:
            sql = "update umbrellas set in_room=%s where id=%s"
            cursor.execute(sql, (False, umbrella["id"]))
        connection.commit()
        led.turn_off(room)
        print "umbrella is successfully fetched"
    else:
        led.locked(room)
        print "umbrella is not fetched"
    flag = -1

def register(nfc):
    room = switch.put()
    if room is False:
        return
    with connection.cursor() as cursor:
        sql = "insert into umbrellas (room_id, nfc_id, in_room) values (%s, %s, %s)"
        cursor.execute(sql, (room["id"], nfc["id"], True))
    connection.commit()
    led.locked(room)
    print "umbrella is successfully registered"


def umbrella_in_room_exists(nfc):
    if get_registered_umbrella(nfc):
        return True
    else:
        return False


def prepare():
    # gpio
    GPIO.setmode(GPIO.BCM)
    with connection.cursor() as cursor:
        sql = "select * from rooms"
        cursor.execute(sql)
        rooms = cursor.fetchall()
    for room in rooms:
        GPIO.setup(room["locked_led_port"], GPIO.OUT)
        GPIO.setup(room["unlocked_led_port"], GPIO.OUT)
        GPIO.setup(room["switch_port"], GPIO.IN)
        led.turn_off(room)


try:
    at = AlertThread()
    at.start()
    prepare()
    reader = tag.TagReader()
    print "start!"
    while True:
        tapped_tag_id = reader.read()
        sound.touch_sound()
        registered_nfc = get_registered_nfc(tapped_tag_id)
        if registered_nfc is not False and umbrella_in_room_exists(registered_nfc):
            unlock(registered_nfc)
        else:
            if registered_nfc is False:
                register_nfc(tapped_tag_id)
            registered_nfc = get_registered_nfc(tapped_tag_id)
            register(registered_nfc)
        print "--------------------"


except KeyboardInterrupt:
    print "\nexit"
