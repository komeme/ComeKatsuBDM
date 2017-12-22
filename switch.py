import RPi.GPIO as GPIO
import pymysql.cursors
import time


def put():
    connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        sql = "select * from rooms inner join umbrellas on rooms.id = umbrellas.room_id where umbrellas.in_room = true"
        cursor.execute(sql)
        occupied_rooms = cursor.fetchall()

    with connection.cursor() as cursor:
        sql = "select * from rooms"
        cursor.execute(sql)
        rooms = cursor.fetchall()

    empty_rooms = []
    for room in rooms:
        if all([room != occupied_room for occupied_room in occupied_rooms]):
            empty_rooms.append(room)

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
