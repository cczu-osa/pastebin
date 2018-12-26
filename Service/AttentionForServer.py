# -*- coding: utf-8 -*-
import requests

db_path = BaseService.get_db_path()

token = ""


def send_alart(content):
    title = u"来自PasteBin的通知"
    data = {
        "text": title,
        "desp": content
    }
    if token != "":
        api = "https://sc.ftqq.com/" + token + ".send"
        requests.get(api, params=data)
