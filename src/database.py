import datetime
import math
import random
import string

from flask_sqlalchemy import SQLAlchemy, Pagination
from werkzeug.exceptions import NotFound

from src.app import app

db = SQLAlchemy()

endless = datetime.datetime(9999, 12, 31)
page_limit = 10


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    token = db.Column(db.String(8), unique=True, index=True)
    ip = db.Column(db.String(20))  # 来源ip
    poster = db.Column(db.String(30))  # poster
    language = db.Column(db.String(50))  # 语言
    content = db.Column(db.Text)  # 内容
    paste_time = db.Column(db.DateTime)  # 发布时间
    expire_time = db.Column(db.DateTime)  # 过期时间
    secret = db.Column(db.Boolean)  # 是否加密

    def __init__(self, dic):
        self.ip = dic['ip']
        self.poster = dic.get('poster', '')
        self.language = dic.get('language', '')
        self.content: str = dic['content']
        if not self.content:
            raise RuntimeError('content empty')
        self.paste_time = datetime.datetime.now()
        expire = dic.get('expire', 604800)
        if expire < 0:
            self.expire_time = endless
        else:
            self.expire_time = self.paste_time + datetime.timedelta(seconds=expire)
        self.secret = dic.get('secret', False)

    def _toDict(self):
        dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dic['paste_time'] = self.paste_time.timestamp()
        dic['expire_time'] = self.expire_time.timestamp()
        return dic

    def __repr__(self):
        return self._toDict().__repr__()

    def outputDict(self):
        return {
            'token': self.token,
            'poster': self.poster,
            'language': self.language,
            'content': self.content,
            'paste_time': self.paste_time.timestamp(),
            'expire_time': self.expire_time.timestamp()
        }


def token_generate():
    return ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(8)])


class Service:
    _trim_count = 0

    def __init__(self, app):
        db.init_app(app)
        db.create_all(app=app)

    def add(self, paste):
        from sqlalchemy.exc import IntegrityError
        try:
            paste.token = token_generate()
            db.session.add(paste)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            paste.token = token_generate()
            db.session.add(paste)
            db.session.commit()
        finally:
            db.session.rollback()
        return paste.token

    def get(self, token):
        paste = Paste.query.filter(Paste.token == token, datetime.datetime.now() < Paste.expire_time).first()
        if paste is None:
            raise NotFound
        return paste.outputDict()

    def _get_obj(self, token):
        return Paste.query.filter(Paste.token == token).first()

    def page(self, num):
        paginate: Pagination = Paste.query.filter(datetime.datetime.now() < Paste.expire_time, Paste.secret == False) \
            .order_by(Paste.id.desc()).paginate(page=num, per_page=page_limit)
        return {
            'pagination': {
                'sum': math.ceil(paginate.total / page_limit),
                'current': paginate.page
            },
            'items': list(map(Paste.outputDict, paginate.items))
        }

    def trim(self):
        self._trim_count += 1
        Paste.query.filter(datetime.datetime.now() >= Paste.expire_time).delete()
        db.session.commit()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/paste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
service = Service(app)
