import uuid
from os import path
from bottle import Bottle, request

from datafly.core import FileUpload

from config import SITE_ROOT
from .models import Page

editor_app = Bottle()

@editor_app.post('/admin/upload/:filetype')
def upload_images(filetype):
    file = request.files.get('file')
    name, ext = path.splitext(file.filename)
    file = FileUpload(file.file, file.name, file.filename)
    # set unique name
    new_name = '%s%s' % (str(uuid.uuid4())[:8], ext)
    file.save(path.join(SITE_ROOT, 'static', 'upload', filetype, new_name),
             overwrite=True)
    link = '/static/upload/%s/%s' % (filetype, new_name)
    return { 'filelink': link }

@editor_app.post('/api/pages/<_id:path>')
def save_page(_id):
    data = { 'id': _id }
    data.update(request.forms)
    page = Page(data)
    page.save()
