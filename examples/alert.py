import pymysql.cursors
import RPi.GPIO as GPIO
import time
import sound

flag = None

connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )

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
