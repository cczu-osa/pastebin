# -*- coding: utf-8 -*-
import datetime
import os
import random
import string
import traceback

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

# 初始化db
SQL_URL = 'sqlite:////' + os.path.join(p, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URL
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
from Service import PasteDBService

# 静态量
endless = datetime.datetime(2099, 12, 31)


@app.route('/')
def st():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index():
    try:
        content = request.form['content']
        if not content:
            return render_template('index.html', content_empty=True)
        paste = PasteDBService.Paste()
        try:
            expire = request.form['expire']
        except:
            expire = 0
        try:
            language = str(request.form['syntax'])[:20]
        except:
            language = "Plains Text"
        try:
            paste.poster = str(request.form['poster'])[:30]
        except:
            paste.poster = ""
        try:
            secret = request.form['secret']
        except:
            secret = "False"
        expire = int(expire) if str(expire).isnumeric() and int(expire) > 0 else -1

        token = ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(8)])
        paste.token = token
        paste.ip = request.remote_addr

        paste.language = language
        paste.content = content
        paste.paste_time = datetime.datetime.now()
        if expire != -1:
            paste.expire_time = paste.paste_time + datetime.timedelta(minutes=expire)
        else:
            paste.expire_time = endless

        paste.secret = True if secret == "True" else False
        PasteDBService.paste_file(paste)
        return redirect('/p/' + token)
    except BaseException as e:
        return send_file(error_file_path), 500


# load pasted file
@app.route('/p/<stamp>')
def pasted_file(stamp):
    try:
        try:
            paste = PasteDBService.get_file(stamp)
        except:
            return send_file(error_file_path)

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
                               raw=paste_raw, show_expire=show_expire, expire_time=expire_time)
    except BaseException as e:
        exstr = traceback.format_exc()
        print(exstr)
        return send_file(error_file_path)


# raw file
@app.route('/r/<stamp>')
def raw(stamp):
    try:
        paste = PasteDBService.get_file(stamp)
        return Response(paste.content, mimetype='text/plain')
    except IOError:
        return send_file(error_file_path)


# download file
@app.route('/d/<stamp>')
def download_file(stamp):
    try:
        paste = PasteDBService.get_file(stamp)
        response = make_response(paste.content)
        response.headers["Content-Disposition"] = "attachment; filename=" + stamp + ".txt"
        return response
    except BaseException as e:
        return send_file(error_file_path)


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
        return render_template('all.html', list=list, pagination=all)
    except BaseException as e:
        return send_file(error_file_path), 500


@app.route('/delete/<stamp>')
def delete_one(stamp):
    try:
        if str(request.remote_addr).startswith("219.230.148.127"):
            PasteDBService.delete_one(stamp)
            return render_template('index.html')
        else:
            return "你没有权限执行此操作"
    except:
        return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# err no such file
@app.errorhandler(Exception)
def all_exception_handler(e):
    return send_file(error_file_path), 404


# entry of programme
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
