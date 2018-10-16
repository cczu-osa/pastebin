from flask import Flask, render_template, request, send_file, redirect, send_from_directory
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
import DeleteToken
import AttentionForServer
import BaseService
app = Flask(__name__)

# 获取工作目录路径
p = BaseService.get_root_path()
paste_path = os.path.join(p, 'pastefile')
error_file_path = os.path.join(p, 'static', 'error.html')


# templates does not need absolute path.
# index_file_path = os.path.join(p, 'templates', 'index.html')
# pasted_file_path = os.path.join(p, 'templates', 'pasted.html')


@app.route('/')
def st():
    return render_template('index.html', state='')


@app.route('/', methods=['POST'])
def index():
    language = request.form['syntax']
    content = request.form['content']
    # print(content)
    if language and content:
        uuid = ''.join([random.choice(string.ascii_letters + string.digits) for ch in range(8)])
        filename = uuid + '.' + language
        code_file = open(os.path.join(paste_path, filename), "w", newline='')
        code_file.write(content)
        code_file.close()
        return redirect('p/' + uuid)
    else:
        return render_template('index.html', state='<script>alert("Please fill all the content!")</script>')


# load pasted file
@app.route('/p/<stamp>')
def pasted_file(stamp):
    try:
        # not to show file extension
        if str(stamp).find('.') >= 0:
            return send_file(error_file_path)
        for file in os.listdir(paste_path):
            if fnmatch.fnmatch(file, stamp + "*"):
                file_path = os.path.join(paste_path, file)
                code_source = open(file_path).read()
                language = os.path.splitext(file)[1][1:]
                time_stamp = time.ctime(os.stat(file_path).st_ctime)
                date = time_stamp
                lang = get_lexer_by_name(language)
                formatter = HtmlFormatter(encoding='utf-8', style='emacs', linenos=True)
                code = highlight(code_source, lang, formatter).decode("utf8").replace('highlighttable', 'pastetable', 1)
                paste_download = '/d/' + str(os.path.basename(file_path))
                return render_template('pasted.html', name='Pasted in ' + date, content=code, pasted=paste_download)
        return send_file(error_file_path)
    except IOError:
        return send_file(error_file_path)


@app.route('/d/<stamp>')
def download_file(stamp):
    try:
        if str(stamp).find('.'):
            return send_file(error_file_path)
        for file in os.listdir(paste_path):
            if fnmatch.fnmatch(file, stamp + "*"):
                file_path = os.path.join(paste_path, file)
                return send_from_directory(paste_path, os.path.basename(file_path), as_attachment=True)
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
        token = request.values.get("token")
        app.logger.info("ip:" + request.remote_addr + "use token:" + token + " request to clean all files")
        if DeleteToken.check_delete_token(token):
            AttentionForServer.send_alart("ip:" + request.remote_addr + "</br>request to clean all files")
            rmtree(paste_path)
            os.mkdir(paste_path)
            return render_template('index.html', state='')
        raise Exception('Auth not passed!')
    except BaseException as e:
        app.logger.error("ip:" + request.remote_addr + "use token:" + token + "auth fail! " + e)
        return "Auth Fail"


# err no such file
@app.errorhandler(404)
def page_not_found(error):
    return send_file(error_file_path), 404


@app.route('/settoken')
def setToken():
    token = request.values.get("token")
    push = request.values.get("pushapi")
    push_set = False
    if push is not None:
        AttentionForServer.set_token(push)
        push_set = True
    if DeleteToken.set_delete_token(token):
        if push_set:
            return '''Set Success! Please Remember it Firmly!</br>
            And you can use push Service now!
            '''
        return 'Set Success! Please Remember it Firmly!'
    if push_set:
        return "You can use push Service now!"
    return 'Fail!'


# entry of programme
if __name__ == '__main__':
    DeleteToken.init()
    app.run(host='0.0.0.0', port=80, debug=True)
    # debug=True
    # host='0.0.0.0', port=81,
