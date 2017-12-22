import pymysql.cursors
import led
import tag

connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )


def get_room():
    switch_port = get_input()
    with connection.cursor() as cursor:
        sql = "select * from rooms where switch_port=%s"
        cursor.execute(sql, (switch_port,))
        rooms = cursor.fetchall()
    if len(rooms) == 0:
        print "room not found!!"
        return False
    return rooms[0]


def get_registered_room(umbrella):
    with connection.cursor() as cursor:
        sql = "select * from rooms where id=%s"
        cursor.execute(sql, (umbrella["room_id"],))
        rooms = cursor.fetchall()
    if len(rooms) == 0:
        print "room not found!!"
        return False
    return rooms[0]


# TODO: connect with devise
def get_input():
    return input()


def register_nfc(tag):
    with connection.cursor() as cursor:
        insert_sql = "insert into nfcs (`tag_id`) values (%s)"
        cursor.execute(insert_sql, (tag["id"],))
    connection.commit()


def get_tag():
    tag_id = tag.read()
    return {'id': tag_id}


def get_registered_umbrella(nfc):
    with connection.cursor() as cursor:
        sql = "select * from umbrellas where nfc_id=%s"
        cursor.execute(sql, (nfc["id"],))
        umbrellas = cursor.fetchall()
    return umbrellas[0]


def get_registered_nfc(tag):
    with connection.cursor() as cursor:
        sql = "select * from nfcs where tag_id=%s"
        cursor.execute(sql, (tag["id"],))
        nfcs = cursor.fetchall()
    if len(nfcs) == 0:
        return False
    return nfcs[0]


def wait_for_umbrella_fetched(umbrella):
    print "fetched!"
    return True


def unlock(nfc):
    umbrella = get_registered_umbrella(nfc)
    room = get_registered_room(umbrella)
    led.locked(room)
    if wait_for_umbrella_fetched(umbrella):
        with connection.cursor() as cursor:
            sql = "update umbrellas set in_room=%s where id=%s"
            cursor.execute(sql, (False, umbrella["id"]))
        connection.commit()
        led.turn_off()
        print "umbrella is successfully fetched"
    else:
        led.locked()
        print "umbrella is not fetched"


def register(nfc):
    room = get_room()
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


try:
    while True:
        tapped_tag = get_tag()
        registered_nfc = get_registered_nfc(tapped_tag)
        if registered_nfc:
            unlock(registered_nfc)
        else:
            register_nfc(tapped_tag)
            registered_nfc = get_registered_nfc(tapped_tag)
            register(registered_nfc)
        print "--------------------"


except KeyboardInterrupt:
    print "\nexit"
