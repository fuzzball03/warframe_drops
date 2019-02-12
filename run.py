import os
import re

from bottle import run, get, abort, install, static_file, template
from pymongo import MongoClient
from bottle_errorsrest import ErrorsRestPlugin


install(ErrorsRestPlugin())

dbname = 'warframe_drops'

cli = MongoClient(connect=False)
db = cli[dbname]


@get('/search/<text>')
def search(text):
    return {'mods': list(db.mods.find({'name': re.compile(text, re.IGNORECASE)}, {'name': True, '_id': False}))}


@get('/all')
def all_mods():
    return {'mods': [v['name'] for v in db.mods.find({}, {'name': True})]}


@get('/')
def index():
    return template('templates/index.tpl')


@get('/mod/<name>')
def info(name):

    result = db.mods.find_one({'name': name}, {'_id': False})
    if result:
        print(result.keys())
        return template('templates/mod.tpl', mod=result)
    return abort(404, 'not found')


@get('/css/<filename>')
def css(filename):
    return static_file(filename, 'css')


@get('/img/<filename>')
def img(filename):
    return static_file(filename, 'img')


@get('/js/<filename>')
def js(filename):
    return static_file(filename, 'js')


@get('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /"


if __name__ == "__main__":
    run(
        port=3322, host="0.0.0.0",
        #server="gunicorn",
        #worker_class='egg:meinheld#gunicorn_worker',
        #workers=4,
        quiet=False,
        debug=True
    )
