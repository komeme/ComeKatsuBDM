import pymysql.cursors
import led
import tag
import switch
import RPi.GPIO as GPIO

connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )


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
        sql = "select * from umbrellas where nfc_id=%s"
        cursor.execute(sql, (nfc["id"],))
        umbrellas = cursor.fetchall()
    return umbrellas[0]


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
    led.locked(room)
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


def register(nfc):
    room = switch.put()
    if room is False:
        return
    with connection.cursor() as cursor:
        sql = "insert into umbrellas (room_id, nfc_id, in_room) values (%s, %s, %s)"
        cursor.execute(sql, (room["id"], nfc["id"], True))
    connection.commit()
    with connection.cursor() as cursor:
        sql = "select * from umbrellas where nfc_id=%s"
        cursor.execute(sql, (nfc["id"],))
        umbrella = cursor.fetchone()
    room = get_registered_room(umbrella)
    led.locked(room)
    print "umbrella is successfully registered"


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


try:
    prepare()
    reader = tag.TagReager()
    while True:
        tapped_tag_id = reader.read()
        registered_nfc = get_registered_nfc(tapped_tag_id)
        if registered_nfc is not False:
            unlock(registered_nfc)
        else:
            register_nfc(tapped_tag_id)
            registered_nfc = get_registered_nfc(tapped_tag_id)
            register(registered_nfc)
        print "--------------------"


except KeyboardInterrupt:
    print "\nexit"
