import pymysql.cursors
import RPi.GPIO as GPIO
import time
import subprocess

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
    sql = "select COUNT(*) from rooms"
    cursor.execute(sql)
    num_rooms = cursor.fetchall()[0][u'COUNT(*)']

with connection.cursor() as cursor:
    sql = "select * from rooms"
    cursor.execute(sql)
    rooms_info = cursor.fetchall()

GPIO.setmode(GPIO.BCM)
for i in range(num_rooms):
    GPIO.setup(rooms_info[i]['switch_port'], GPIO.IN)

while True:
    with connection.cursor() as cursor:
        sql = "select room_id from umbrellas where in_room = true"
        cursor.execute(sql)
        occupied_rooms = cursor.fetchall()

    would_occupied = [i in occupied_rooms for i in range(num_rooms)]

    for i in range(num_rooms):
        if (GPIO.input(rooms_info[i]['switch_port']) == GPIO.HIGH) == would_occupied[i]:
            pass
        else:
            if flag != i:
                subprocess.call("aplay alert.mp3", shell=True)

    time.sleep(0.1)
