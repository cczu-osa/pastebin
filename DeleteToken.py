import sqlite3

import BaseService

db_path = BaseService.get_db_path()

def init():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS config
           (KEY_ID VARCHAR(50) PRIMARY KEY  NOT NULL,
           VALUE_OF_KEY  VARCHAR(50)  NOT NULL);''')
    conn.commit()
    conn.close()


def check_delete_token_status():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute('''select * from config where KEY_ID = \'delete_token\';''')
    if not cursor.fetchall():
        return True
    return False


def set_delete_token(token):
    if check_delete_token_status():
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('insert into config(KEY_ID,VALUE_OF_KEY) values("delete_token","' + token + '");')
        if conn.total_changes > 0:
            conn.commit()
            return True
    return False


def check_delete_token(token):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute('select * from config where KEY_ID = "delete_token";')
    result = cursor.fetchall()
    for rows in result:
        if rows[1] == token:
            return True
    return False
