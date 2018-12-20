# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_file, redirect, send_from_directory, Response
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import fnmatch
import string
import random
import time
import datetime
from shutil import rmtree
from Service import AttentionForServer
from Service import BaseService, DeleteToken

app = Flask(__name__)

# 获取工作目录路径
p = app.root_path
paste_path = os.path.join(p, 'pastefile')
error_file_path = os.path.join(p, 'static', 'error.html')

test = '''import random, time
import numpy as np, sys

def wait(second):
    for i in range(second):
        time.sleep(1)
        sys.stdout.write("\\r倒数{}".format(second - i))
        sys.stdout.flush()
    print('')


def next(str):
    # time.sleep(5)
    while True:
        next = input(str)
        if next == "y" or next == "Y":
            return True
        elif next == "n" or next == "N":
            return  False
        else:
            print("输入有误!请重新输入")


def showlist(namelist):
    for i in range(len(namelist)):
        print(namelist[i],end='\\t\\t\\t')
        # print("{3}".format())
        if (i+1)%10 == 0:
            print('')

res = []
notcome = []
def game():
    file = open('namelist.txt', "r", encoding='utf-8')
    str = file.read()
    file.close()
    str.replace(' ', '')
    name_list = str.split('\n')
    while True:
        n = len(name_list)
        showlist(name_list)     # 打印剩余人员
        print("有{}个人还没交换礼物".format(n))
        giver_list  = []
        while True:
            giver = random.sample(name_list, 1)[0]
            print("送礼物的人是{}!".format(giver))
            judge = next(giver+"来了吗?")
            name_list.pop(name_list.index(giver))
            if judge:
                giver_list.append(giver)
                print("有请{}上台!".format(giver))
                wait(3)
            else:
                print("很遗憾ta没来")
                notcometxt = open("notcome.txt", 'a', encoding='utf-8')
                notcome.append(giver)
                notcometxt.write(giver)
                notcometxt.close()
                time.sleep(2)
            if len(giver_list) == 2:
                res.append(giver_list)
                print("有请<--{}--> 和 <--{}--> 交换礼物并发表'换礼物感言'!".format(giver_list[0], giver_list[1]))
                continue_ = next("继续?")
                if continue_ == "y":
                    pass

                break

        n = len(name_list)
        if n == 1:
            print("还剩{}一个人没有交换哦!".format(n))
            break
        elif n==0:
            print("礼物交换到此结束了哦!")
            break


if __name__ == '__main__':
    game()


for xiaokeai in res:
    print("{}和{}".format(xiaokeai[0],xiaokeai[1]))'''

@app.route('/')
def st():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index():
    content = request.form['content']
    if not content:
        return render_template('index.html', content_empty=True)

    poster = str(request.form['poster'])
    language = str(request.form['syntax'])
    secret = 1 if request.form['secret'] == "True" else 0

    expire = request.form['expire']
    expire = expire if str(expire).isnumeric() else 0

    uuid = ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(8)])
    # filename = uuid + '.' + language
    # code_file = open(os.path.join(paste_path, filename), "w", newline='')
    # code_file.write(content)
    # code_file.close()
    # return redirect('p/' + uuid)

    return render_template('index.html')


# load pasted file
@app.route('/p/<stamp>')
def pasted_file(stamp):
    try:
        code_source = test
        language = "python"
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lang = get_lexer_by_name(language)
        formatter = HtmlFormatter(encoding='utf-8', style='emacs', linenos=True, full=True)
        paste_download = '/d/' + stamp
        paste_raw = '/r/' + stamp
        code = highlight(code_source, lang, formatter).decode("utf8").replace('highlighttable', 'pastetable', 1)

        return render_template('pasted.html', name='Pasted in ' + date, content=code, pasted=paste_download,
                               raw=paste_raw)

    except IOError:
        return send_file(error_file_path)


# raw file
@app.route('/r/<stamp>')
def raw(stamp):
    return Response(test, mimetype='text/plain')

@app.route('/d/<stamp>')
def download_file(stamp):
    try:
        if '.' in stamp:
            return send_file(error_file_path)
        for file in os.listdir(paste_path):
            if fnmatch.fnmatch(file, stamp + "*"):
                return send_from_directory(paste_path, file, as_attachment=True)
        return send_file(error_file_path)
    except IOError:
        return send_file(error_file_path)


@app.route('/all')
def show_all():
    try:
        posts = []
        os.chdir(paste_path)
        files = filter(os.path.isfile, os.listdir(paste_path))
        files = [os.path.join(paste_path, f) for f in files]
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for file in files:
            file_path = os.path.join(paste_path, file)
            file_name = os.path.basename(file_path).split('.')
            time_stamp = time.ctime(os.stat(file_path).st_ctime + datetime.timedelta(hours=8))
            code_source = ''
            f = open(file_path)
            for i in range(10):
                code_source = code_source + f.readline()
            lang = get_lexer_by_name(file_name[1])
            formatter = HtmlFormatter(encoding='utf-8', style='emacs', linenos=True)
            code = highlight(code_source, lang, formatter).decode("utf8").replace('highlighttable', 'pastetable', 1)
            posts.append(dict(url=file_name[0], dat=time_stamp, content=code))
        return render_template('all.html', data=posts)
    except BaseException as e:
        print(str(e))
        return send_file(error_file_path)


@app.route('/clean')
def clean_all():
    try:
        if str(request.remote_addr).startswith("219.230.148.127"):
            return render_template('index.html', state='')
            pass
        else:
            return "你没有权限执行此操作"
    except BaseException:
        return render_template('index.html', state='')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# err no such file
@app.errorhandler(Exception)
def all_exception_handler(e):
    print("error" + e)
    return send_file(error_file_path), 404


# entry of programme
if __name__ == '__main__':
    DeleteToken.init()
    app.run(host='0.0.0.0', port=81)
    # debug=True
    # host='0.0.0.0', port=81,
