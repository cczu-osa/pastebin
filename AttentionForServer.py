import sqlite3
import requests

import BaseService

db_path = BaseService.get_db_path()


def send_alart(content):
    title = u"来自PasteBin的通知"
    data = {
        "text": title,
        "desp": content
    }
    token = query_token()
    if token != "":
        api = "https://sc.ftqq.com/" + token + ".send"
        requests.get(api, params=data)


def set_token(token):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('insert into config(KEY_ID,VALUE_OF_KEY) values("push_token","' + token + '");')
        if conn.total_changes > 0:
            conn.commit()
    except BaseException as e:
        c.execute('update config set VALUE_OF_KEY ="' + token + '" where KEY_ID = "push_token";')
        conn.commit()


def query_token():
    conn = sqlite3.connect('pastebin.db')
    c = conn.cursor()
    cursor = c.execute('select * from config where KEY_ID = "push_token";')
    result = cursor.fetchall()
    for rows in result:
        return rows[1]
    return ""
