import os
import re

from bottle import run, get, abort, install, static_file, template
from pymongo import MongoClient
from bottle_errorsrest import ErrorsRestPlugin


install(ErrorsRestPlugin())

dbname = 'warframe_items'

cli = MongoClient(connect=False)
db = cli[dbname]


@get('/')
def index():
    items = db.items.count()
    places = db.places.count()
    drops = 0
    for item in db.items.find({}, {'drops': True}):
        drops += len(item.get('drops', []))
    return template(
        'templates/index.tpl',
        items=items, places=places, drops=drops)


@get('/all')
def all():
    info = ""
    for item in db.items.find({}, {'name': True}):
        info += '<a href="/item/%s">%s</a><br />' % (
            item['name'], item['name'])

    for place in db.places.find({}, {'name': True}):
        info += '<a href="/place/%s">%s</a><br />' % (
            place['name'], place['name'])

    return info


@get('/item/<name>')
def item(name):

    result = db.items.find_one({'name': name}, {'_id': False})
    if result:
        return template('templates/item.tpl', item=result)
    return abort(404, 'not found')


@get('/place/<name:path>')
def place(name):
    result = db.places.find_one({'name': name}, {'_id': False})
    if result:
        return template('templates/place.tpl', place=result)
    return abort(404, 'not found')


@get('/css/<filename>')
def css(filename):
    return static_file(filename, 'css')


@get('/img/<filename:path>')
def img(filename):
    return static_file(filename, 'img')


@get('/favicon.ico')
def favicon():
    return img('favicon.ico')


@get('/js/<filename>')
def js(filename):
    return static_file(filename, 'js')


@get('/robots.txt')
def robots():
    return static_file('robots.txt', 'txt')


@get('/sitemap.xml')
def sitemap():
    return static_file('sitemap.xml', 'xml')


if __name__ == "__main__":
    run(
        port=3322, host="0.0.0.0",
        server="gunicorn",
        worker_class='egg:meinheld#gunicorn_worker',
        workers=4,
        # reloader=True,
        quiet=False,
        debug=True
    )
