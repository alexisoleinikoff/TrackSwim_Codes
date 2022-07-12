import pymysql

sql = pymysql.connect(host='localhost',
                port=3306,
                user='root',
                password='',
                database='trackswim_db')

with sql:
    with sql.cursor() as cursor:
        cursor.execute('SELECT ID_tag FROM tag WHERE EPC=%s', str(b'E2000001B7311003919000FE7'))
        if not cursor.rowcount:
            continue
        r = cursor.fetchone()[0]

        print(r)
        