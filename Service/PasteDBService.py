# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import PasteBinWeb

# init variables
app = PasteBinWeb.app
db = PasteBinWeb.db
SQL_URL = PasteBinWeb.SQL_URL
engine = create_engine(SQL_URL)
DBSession = sessionmaker(bind=engine)
# 每页10条数据
limit = 10


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    token = db.Column(db.String(8), unique=True, index=True)
    ip = db.Column(db.String(20))  # 来源ip
    poster = db.Column(db.String(30))  # poster
    language = db.Column(db.String(20))  # 语言
    content = db.Column(db.Text)  # 内容
    paste_time = db.Column(db.DateTime)  # 发布时间
    expire_time = db.Column(db.DateTime)  # 过期时间
    secret = db.Column(db.Boolean)  # 是否加密


# paste one
def paste_file(paste):
    session = DBSession()
    session.add(paste)
    session.commit()
    session.close()


# get one
def get_file(token):
    session = DBSession()
    try:
        paste = session.query(Paste).filter(Paste.token == token, Paste.expire_time > datetime.now()).one()
        return paste
    finally:
        session.close()


# all pasted files
def get_all(page):
    session = DBSession()
    try:
        paste_list = Paste.query.filter(Paste.expire_time > datetime.now(), Paste.secret == False).order_by(
            Paste.id.desc()).paginate(page=page, per_page=limit)
        return paste_list
    except BaseException as e:
        print(e)
    finally:
        session.close()


def delete_one(token):
    session = DBSession()
    try:
        paste = session.query(Paste).filter(Paste.token == token).one()
        paste.expire_time = datetime.now()
        session.commit()
    finally:
        session.close()
