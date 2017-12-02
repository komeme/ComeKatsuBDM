import pymysql.cursors

connection = pymysql.connect(
        user='root',
        passwd='root',
        host='localhost',
        db='bdm_umbrella_stand',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )


def get_registered_umbrella(nfc):
    with connection.cursor() as cursor:
        sql = "select * from umbrellas where nfc_id=%s"
        cursor.execute(sql, (nfc["id"],))
        umbrellas = cursor.fetchall()
    return umbrellas[0]


def get_registered_nfc():
    tag_id = get_tapped_tag()
    with connection.cursor() as cursor:
        sql = "select * from nfcs where tag_id=%s"
        cursor.execute(sql, (tag_id,))
        nfcs = cursor.fetchall()
    if len(nfcs) == 0:
        print "nfcs not found!!"
        return False
    return nfcs[0]


# TODO: connect with devise
def get_tapped_tag():
    return raw_input()


def release_umbrella(umbrella):
    with connection.cursor() as cursor:
        sql = "update umbrellas set in_room=%s where id=%s"
        cursor.execute(sql, (False, umbrella["id"]))
    connection.commit()


def send_signal(umbrella):
    print umbrella


try:
    while True:
        nfc = get_registered_nfc()
        if not nfc:
            print "-------------------------------"
            continue
        umbrella = get_registered_umbrella(nfc)
        send_signal(umbrella)
        release_umbrella(umbrella)
        print "success!"

except KeyboardInterrupt:
    print "\nexit"
