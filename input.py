import pymysql.cursors

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


# TODO: connect with devise
def get_input():
    return input()


def get_nfc():
    tag = get_tag()
    with connection.cursor() as cursor:
        sql = "select * from nfcs where tag_id=%s"
        cursor.execute(sql, (tag["id"],))
        if len(cursor.fetchall()) == 0:
            insert_sql = "insert into nfcs (`tag_id`) values (%s)"
            cursor.execute(insert_sql, (tag["id"],))
            connection.commit()
        cursor.execute(sql, (tag["id"],))
        return cursor.fetchone()


# TODO: connect with devise
def get_tag():
    tag_id = raw_input()
    return {'id': tag_id}


def register_umbrella(room, nfc):
    with connection.cursor() as cursor:
        sql = "insert into umbrellas (room_id, nfc_id, in_room) values (%s, %s, %s)"
        cursor.execute(sql, (room["id"], nfc["id"], True))
    connection.commit()
    with connection.cursor() as cursor:
        sql = "select * from umbrellas where nfc_id=%s"
        cursor.execute(sql, (nfc["id"],))
        umbrellas = cursor.fetchall()
    print umbrellas[0]


try:
    while True:
        room = get_room()
        if not room:
            print "-------------------------------"
            continue
        nfc = get_nfc()
        register_umbrella(room, nfc)
        print "success!"


except KeyboardInterrupt:
    print "\nexit"

