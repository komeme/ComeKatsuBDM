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
    #
    # with connection.cursor() as cursor:
    #     sql = "select * from rooms"
    #     cursor.execute(sql)
    #     rooms_info = cursor.fetchall()
    #
    # with connection.cursor() as cursor:
    #     sql = "select room_id from umbrellas where in_room = true"
    #     cursor.execute(sql)
    #     occupied_rooms = [room["room_id"] for room in cursor.fetchall()]
    #
    # would_occupied = [i in occupied_rooms for i in range(len(rooms_info))]
    #
    # for i in range(200):
    #     for room_info in rooms_info:
    #         if (GPIO.input(room_info['switch_port']) == GPIO.HIGH) != would_occupied[room_info["id"]]:
    #             with connection.cursor() as cursor:
    #                 sql = "select * from rooms where id = %s"
    #                 cursor.execute(sql, (room_info["id"],))
    #                 return cursor.fetchone()
    #     time.sleep(0.1)
    #
    # return False

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
    # connection = pymysql.connect(
    #     user='root',
    #     passwd='root',
    #     host='localhost',
    #     db='bdm_umbrella_stand',
    #     charset='utf8mb4',
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    #
    # with connection.cursor() as cursor:
    #     sql = "select * from rooms"
    #     cursor.execute(sql)
    #     rooms_info = cursor.fetchall()
    #
    # with connection.cursor() as cursor:
    #     sql = "select room_id from umbrellas where in_room = true"
    #     cursor.execute(sql)
    #     occupied_rooms = [occupied_room["room_id"] for occupied_room in cursor.fetchall()]
    #
    # would_occupied = [i in occupied_rooms for i in range(len(rooms_info))]
    #
    # for i in range(200):
    #     for room_info in rooms_info:
    #         if (GPIO.input(room_info['switch_port']) == GPIO.HIGH) != would_occupied[room_info["id"]]:
    #             if room_info["id"] == room["id"]:
    #                 return True
    #     time.sleep(0.1)
    # return False

    for i in range(200):
        if GPIO.input(room['switch_port']) == GPIO.LOW:
            return True
        time.sleep(0.1)

    return False
