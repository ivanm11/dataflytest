import uuid
import json
from bson.json_util import dumps
from os import path
from bottle import Bottle, request

from datafly.core import FileUpload
from datafly.utils import slugify

from config import db, SITE_ROOT
from .models import Page

editor_app = Bottle()

@editor_app.post('/admin/upload/:filetype')
def upload(filetype):
    file = request.files.get('file')
    name, ext = path.splitext(file.filename)
    file = FileUpload(file.file, file.name, file.filename)
    # set unique name
    new_name = '%s%s' % (str(uuid.uuid4())[:8], ext)
    file.save(path.join(SITE_ROOT, 'static', 'upload', filetype, new_name),
             overwrite=True)
    link = '/static/upload/%s/%s' % (filetype, new_name)
    return { 'filelink': link }

@editor_app.get('/admin/api/pages/<_id>/version')
def get_page(_id):
    p = Page.get_by_id(_id)
    return json.loads(dumps(p))

@editor_app.post('/admin/api/pages/id/<page_id:path>')
def save_page(page_id):    
    if 'new' in page_id.split('/'):
        page_id = page_id.replace('new', slugify(page_content['meta']['title']))
    new_version = Page(request.json['page'])
    new_version.save()