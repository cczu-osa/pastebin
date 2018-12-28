# -*- coding: utf-8 -*-
from datetime import datetime

import requests


def send_alart(content, token):
    title = u"来自PasteBin的通知 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "text": title,
        "desp": content
    }
    if token != "":
        api = "https://sc.ftqq.com/" + token + ".send"
        requests.get(api, params=data)
