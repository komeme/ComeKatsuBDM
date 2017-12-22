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
        sql = "select * from rooms"
        cursor.execute(sql)
        rooms_info = cursor.fetchall()

    with connection.cursor() as cursor:
        sql = "select room_id from umbrellas where in_room = true"
        cursor.execute(sql)
        occupied_rooms = cursor.fetchall()

    would_occupied = [i in occupied_rooms for i in range(len(rooms_info))]

    for i in range(200):
        for j in range(len(rooms_info)):
            if (GPIO.input(rooms_info[j]['switch_port']) == GPIO.HIGH) != would_occupied[j]:
                with connection.cursor() as cursor:
                    sql = "select room from rooms where id = %s"
                    cursor.execute(sql, (j,))
                    return cursor.fetchone()
        time.sleep(0.1)

    return False


def take(room):
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
        rooms_info = cursor.fetchall()

    with connection.cursor() as cursor:
        sql = "select room_id from umbrellas where in_room = true"
        cursor.execute(sql)
        occupied_rooms = cursor.fetchall()

    would_occupied = [i in occupied_rooms for i in range(len(rooms_info))]

    for i in range(200):
        for j in range(len(rooms_info)):
            if (GPIO.input(rooms_info[j]['switch_port']) == GPIO.HIGH) != would_occupied[j]:
                if j == room["id"]:
                    return True
        time.sleep(0.1)
    return False
