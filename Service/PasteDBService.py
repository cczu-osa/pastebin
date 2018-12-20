import sqlite3

from Service import BaseService

db_path = BaseService.get_db_path()


def add_paste():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('insert into config(KEY_ID,VALUE_OF_KEY) values("push_token","' + token + '");')
        if conn.total_changes > 0:
            conn.commit()
    except BaseException as e:
        c.execute('update config set VALUE_OF_KEY ="' + token + '" where KEY_ID = "push_token";')
        conn.commit()
