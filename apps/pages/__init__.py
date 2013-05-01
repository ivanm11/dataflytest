import uuid
from os import path
from datetime import datetime

from bottle import Bottle, request
from bson.objectid import ObjectId

from config import _root_dir, Config
from datafly.bottle.utils import template, FileUpload
from datafly.admin import before_request

from db import db

app = Bottle()

app.hooks.add('before_request', before_request)

class MongoBackend(object):
    def load(self, id, version=None):
        if version:
            return db.pages.find_one({'_id': ObjectId(version)})
        try:
            return db.pages.find({'id': id}).sort('published', -1)[0]
        except IndexError:
            return {
                'title': '',
                'html': ''
            }

    def load_all(self, id):
        return db.pages.find({'id': id}).sort('published', -1)[1:]

    # save html to file
    def save(self, id, data):
        page = {
            'id': id,
            'html': data.html,
            'title': data.title,
            'published': datetime.now()
        }
        return db.pages.insert(page)

class FileBackend(object):
    # load html from file
    def load(self, id, published=None):
        source = path.join(_root_dir, 'html', id+'.html')
        try:
            f = open(source)
            html = f.read().decode('utf-8')
            f.close()
        except IOError:
            f = open(source, 'w')
            html = u''
            f.close()
        return {
            'title': '',
            'html': html
        }

    def load_all(self, id):
        return None

    # save html to file
    def save(self, id, data):
        f = open(path.join(_root_dir, 'html', id+'.html'), 'w')
        f.write(data.html.encode('utf-8'))
        f.close()

if Config.PAGES_BACKEND == 'mongo':
    backend = MongoBackend()
else:
    backend = FileBackend()

def load_html(id):
    return backend.load(id)['html']

@app.get('/')
@app.get('/:page')
@app.get('/:section/:page')
def pages(page=None, section=None):
    c = template_context = {}
    c['id'] = id = '%s/%s' % (section, page) if section else page
    version = request.query.get('v', False)
    if version:
        c['current'] = version
        page = backend.load(id, version)
    else:
        page = backend.load(id)
    # page is a dict, keys: title, html
    c.update(page)
    c['versions'] = backend.load_all(id)
    return template('pages/layout.html', **template_context)

@app.post('/:page')
@app.post('/:section/:page')
def save_page(page=None, section=None):
    id = '%s/%s' % (section, page) if section else page
    data = request.forms
    backend.save(id, data)
    prev = db.pages.find({'id': id}).sort('published', -1)[1]
    return {
        'id': str(prev['_id']),
        'datetime': prev['published'].strftime('%m-%d-%Y %I:%M %p')
    }

@app.post('/upload')
def upload_images():
    file = request.files.get('file')
    name, ext = path.splitext(file.filename)
    file = FileUpload(file.file, file.name, file.filename)
    # set unique name
    new_name = '%s%s' % (str(uuid.uuid4())[:8], ext)
    file.save(path.join(_root_dir, 'static', 'img', 'upload', new_name),
             overwrite=True)
    link = '/static/img/upload/%s' % new_name
    return { 'filelink': link }

