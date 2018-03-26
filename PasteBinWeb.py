from flask import Flask, render_template, request, send_file, redirect
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from jinja2 import Template
import json
import os
import fnmatch
import string
import random
import time

app = Flask(__name__)

@app.route('/')
def st():
    return send_file("index.html")


@app.route('/', methods=['POST'])
def index():
    language = request.form['syntax']
    content = request.form['content']
    print(content)
    if language and content :
        try:
            uuid = ''.join([random.choice(string.ascii_letters+string.digits) for ch in range(8)])
            filename = uuid + '.' + language
            file = open(filename, "w", newline='')
            file.write(content)
        finally:
            file.close()
            return redirect('p/'+uuid)
    else:
        return json.dumps({'请填写所有项'})
@app.route('/p/<stmp>')
def num(stmp):
    language = 'text'
    code_source = '0'
    date = '0'
    count = 0
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, stmp+"*"):
            filecontent = open(file)
            code_source = filecontent.read()
            language = os.path.splitext(file)[1][1:]
            timm = time.gmtime(os.path.getatime(file))
            date = time.strftime("%Y-%m-%d %H:%M:%S", timm)
            count = count + 1
    if(count != 0):
        lang = get_lexer_by_name(language)
        formatter = HtmlFormatter(encoding='utf-8', style = 'emacs', linenos = True)
        code = highlight(code_source, lang, formatter).decode("utf8").replace('highlighttable','pastetable',1)
        return render_template('head.html', name='Pasted in ' + date, content=code)
    else:
        return send_file('error.html')

#err no such file
@app.errorhandler(404)
def page_not_found(error):
    return send_file('error.html'), 404

if __name__ == '__main__':
    app.run()