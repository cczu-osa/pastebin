from flask import send_file, render_template

from src.app import app
from src.settings import settings

baseurl = settings['baseurl'] or settings['rootdir']


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


@app.route('/')
def index():
    return render_template('index.html', baseurl=baseurl)


@app.route('/p/<string:dummy>')
def p(dummy):
    return render_template('p.html', baseurl=baseurl)


@app.route('/all')
@app.route('/all/<int:dummy>')
def all(dummy=1):
    return render_template('all.html', baseurl=baseurl)


@app.route('/about')
def about():
    return render_template('about.html', baseurl=baseurl)


@app.route('/404')
@app.errorhandler(404)
def error_404(dummy=None):
    return render_template('404.html', baseurl=baseurl), 404


@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /", 200, {'content-type': 'text/plain; charset=utf-8'}
