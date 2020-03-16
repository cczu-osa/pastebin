# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import string
import traceback
import json
import sqlite3

import markdown2
from flask import Flask, render_template, request, send_file, redirect, send_from_directory, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from Service.language_select import get_language

app = Flask(__name__)

# 获取工作目录路径
p = app.root_path
error_file_path = os.path.join(p, 'static', 'error.html')

# 检查data文件夹
if not os.path.isdir('data'):
    os.mkdir('data')

# 初始化db
if not os.path.isfile('data/paste.db'):
    conn = sqlite3.connect('data/paste.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE paste (
            id INTEGER NOT NULL,
            token VARCHAR(8),
            ip VARCHAR(20),
            poster VARCHAR(30),
            language VARCHAR(20),
            content TEXT,
            paste_time DATETIME,
            expire_time DATETIME,
            secret BOOLEAN,
            PRIMARY KEY (id),
            CHECK (secret IN (0, 1))
        )
    ''')
    cursor.execute('CREATE UNIQUE INDEX ix_paste_token ON paste (token)')
    cursor.close()
    conn.commit()
    conn.close()

SQL_URL = 'sqlite:////' + os.path.join(p, 'data/paste.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URL
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
from Service import PasteDBService

# settings
try:
    with open('data/settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
        baseurl = settings.get('baseurl', settings.get('rootdir', ''))
except FileNotFoundError:
    # default
    baseurl = ''

endless = datetime.datetime(2099, 12, 31)

# PostBin的MarkDown加载器
# 自动格式化连接
link_patterns = [(re.compile(
    r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),
                  r'\1')]
markdown = markdown2.Markdown(extras=["link-patterns", "fenced-code-blocks", "cuddled-lists", "tables", "footnotes"],
                              link_patterns=link_patterns)


@app.route('/')
def st():
    return render_template('index.html', baseurl=baseurl)


@app.route('/about')
def about_page():
    return render_template('about.html', baseurl=baseurl)


@app.route('/', methods=['POST'])
def index():
    try:
        content = request.form['content']
        if not content:
            return render_template('index.html', content_empty=True, baseurl=baseurl)

        paste = PasteDBService.Paste()
        expire = request.form.get('expire', type=int, default=129600)
        language = request.form.get('syntax', type=str, default="Plains Text")[:20]
        paste.poster = request.form.get('poster', type=str, default="")[:30]
        secret = request.form.get('secret', type=str, default="False")
        secret = True if secret == "True" else False

        paste.token = token = get_token()
        paste.ip = request.remote_addr
        paste.language = language
        paste.content = content
        paste.paste_time = datetime.datetime.now()
        paste.expire_time = paste.paste_time + datetime.timedelta(minutes=expire) if expire > 0 else endless
        paste.secret = secret
        PasteDBService.paste_file(paste)
        return redirect(baseurl + '/p/' + token)
    except:
        return render_template('error.html', baseurl=baseurl), 500


# load pasted file
@app.route('/p/<stamp>')
def pasted_file(stamp):
    try:
        try:
            paste = PasteDBService.get_file(stamp)
        except:
            return render_template('error.html', baseurl=baseurl)

        date = paste.paste_time.strftime("%Y-%m-%d %H:%M:%S")

        lang = get_lexer_by_name(get_language(paste.language))

        if len(paste.poster) > 0:
            title = 'Pasted by ' + paste.poster + ' in ' + date
        else:
            title = 'Pasted in ' + date
        if paste.expire_time == endless:
            show_expire = False
            expire_time = endless
        else:
            show_expire = True
            expire_time = paste.expire_time.strftime("%Y-%m-%d %H:%M:%S")
        formatter = HtmlFormatter(encoding='utf-8', style='native', linenos=True)
        paste_download = '/d/' + stamp
        paste_raw = '/r/' + stamp
        code = highlight(paste.content, lang, formatter).decode("utf8").replace('highlighttable', 'pastetable', 1)
        return render_template('pasted.html', name=title, content=code, pasted=paste_download,
                               raw=paste_raw, show_expire=show_expire, expire_time=expire_time, baseurl=baseurl)
    except:
        exstr = traceback.format_exc()
        print(exstr)
        return render_template('error.html', baseurl=baseurl)


# raw file
@app.route('/r/<stamp>')
def raw(stamp):
    try:
        paste = PasteDBService.get_file(stamp)
        return Response(paste.content, mimetype='text/plain')
    except IOError:
        return render_template('error.html', baseurl=baseurl)


# download file
@app.route('/d/<stamp>')
def download_file(stamp):
    try:
        paste = PasteDBService.get_file(stamp)
        response = make_response(paste.content)
        response.headers["Content-Disposition"] = "attachment; filename=" + stamp + ".txt"
        return response
    except:
        return render_template('error.html', baseurl=baseurl)


@app.route('/all')
@app.route('/all/<int:page>')
def show_all(page=1):
    try:
        all = PasteDBService.get_all(page)
        list = all.items
        for paste in list:
            lang = get_lexer_by_name(get_language(paste.language))
            formatter = HtmlFormatter(encoding='utf-8', style='native', linenos=True)
            paste.content = highlight(paste.content[:140], lang, formatter).decode("utf8").replace('highlighttable',
                                                                                                   'pastetable', 1)
        return render_template('all.html', list=list, pagination=all, baseurl=baseurl)
    except BaseException as e:
        return render_template('error.html', baseurl=baseurl), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# 2019-02-26
# 更新postbin功能
@app.route('/post')
def posts_main():
    return render_template('post.html', baseurl=baseurl)


@app.route('/post', methods=['POST'])
def posts():
    try:
        content = request.form['content']
        if not content:
            return render_template('post.html', content_empty=True, baseurl=baseurl)

        paste = PasteDBService.Paste()
        paste.token = token = get_token()
        paste.ip = request.remote_addr
        paste.poster = request.form.get('poster', type=str, default="")[:30]
        paste.language = request.form.get('title', type=str, default="")[:50]
        paste.content = content
        paste.paste_time = datetime.datetime.now()
        paste.expire_time = endless
        paste.secret = True
        PasteDBService.paste_file(paste)
        return redirect('/post/v/' + token)
    except:
        msg = traceback.format_exc()
        print(msg)
        return render_template('error.html', baseurl=baseurl), 500


@app.route('/post/v/<stamp>')
def posted_file(stamp):
    try:
        try:
            paste = PasteDBService.get_file(stamp)
        except:
            return render_template('error.html', baseurl=baseurl)

        date = paste.paste_time.strftime("%Y-%m-%d %H:%M:%S")

        if len(paste.language) <= 0:
            title = 'No Title'
        else:
            title = paste.language

        if len(paste.poster) > 0:
            name = 'Posted by ' + paste.poster + ' in ' + date
        else:
            name = 'Posted in ' + date

        paste_raw = '/r/' + stamp
        code = markdown.convert(paste.content)
        return render_template('posted.html', post_title=title, name=name, content=code,
                               raw=paste_raw, baseurl=baseurl)
    except:
        return render_template('error.html', baseurl=baseurl)


@app.route('/post/r/<stamp>')
def posted_raw_file(stamp):
    return redirect('/p/' + stamp)


# err no such file
@app.errorhandler(Exception)
def all_exception_handler(e):
    return render_template('error.html', baseurl=baseurl), 404


def get_token():
    return ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(8)])


# entry of programme
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
