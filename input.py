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
    input_id = get_input()
    with connection.cursor() as cursor:
        sql = "select * from `rooms` where `input_id`=%s"
        cursor.execute(sql, (input_id,))
        rooms = cursor.fetchall()
        if len(rooms) == 0:
            return False
        return rooms[0]["id"]


# TODO: connect with devise
def get_input():
    return input()


def get_nfc():
    tag_id = get_tag()
    with connection.cursor() as cursor:
        sql = "select * from nfcs where tag_id=%s"
        cursor.execute(sql, (tag_id,))
        if len(cursor.fetchall()) == 0:
            insert_sql = "insert into nfcs (`tag_id`) values (%s)"
            cursor.execute(insert_sql, (tag_id,))
            connection.commit()
        cursor.execute(sql, (tag_id,))
        return cursor.fetchone()["id"]


# TODO: connect with devise
def get_tag():
    return raw_input()


while True:
    room_id = get_room()
    if not room_id:
        continue
    nfc_id = get_nfc()
    with connection.cursor() as cursor:
        sql = "insert into umbrellas (`room_id`, `nfc_id`, `in_room`) values (%s, %s, %s)"
        cursor.execute(sql, (room_id, nfc_id, True))
    connection.commit()
    print("success!")
