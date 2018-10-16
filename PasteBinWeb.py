from flask import Flask, render_template, request, send_file, redirect, send_from_directory
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import fnmatch
import string
import random
import time
import sys
import shutil

app = Flask(__name__)

# 获取工作目录路径
if (sys.path[0] == os.getcwd()):
    p = sys.path[0]
else:
    p = sys.path[1]
paste_path = os.path.join(p, 'pastefile')
try:
    os.mkdir(paste_path)
except BaseException as e:
    print("粘贴文件夹已创建")
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
        # print(os.path.join(paste_path, filename))
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
                # date = time.strftime("%Y-%m-%d %H:%M:%S", time_stamp)
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
            # print(file_path+time.ctime(os.stat(file_path).st_ctime))
            # path = os.path.splitext(file)[0][0:]
            file_name = os.path.basename(file_path).split('.')
            time_stamp = time.ctime(os.stat(file_path).st_ctime)
            # date = time_stamp
            code_source = ''
            f = open(file_path)
            for i in range(10):
                code_source = code_source + f.readline()
            lang = get_lexer_by_name(file_name[1])
            formatter = HtmlFormatter(encoding='utf-8', style='emacs', linenos=True)
            code = highlight(code_source, lang, formatter).decode("utf8").replace('highlighttable', 'pastetable', 1)
            posts.append(dict(url=file_name[0], dat=time_stamp, content=code))
            # print(os.path.splitext(file)[0][1:])
            # list.append()
            # list.append()
        return render_template('all.html', data=posts)
    except BaseException as e:
        print(str(e))
        return send_file(error_file_path)


@app.route('/clean')
def clean_all():
    shutil.rmtree(paste_path)
    os.mkdir(paste_path)
    return render_template('index.html', state='')


# err no such file
@app.errorhandler(404)
def page_not_found(error):
    return send_file(error_file_path), 404


# entry of programme
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # debug=True
    # host='0.0.0.0', port=81,
