from bottle import Bottle, request, response
from bson.objectid import ObjectId
from bson.json_util import dumps

from config import db

admin_api_app = Bottle()

@admin_api_app.post('/admin/api/<collection>')
@admin_api_app.post('/admin/api/<collection>/<_id>')
def update_resource(collection, _id=None):
    data = dict(request.forms.items())
    for key, value in data.items():
        if value in ('true', 'false'):
            data[key] = (value == 'true')
    collection = db[collection]
    query = { '_id': ObjectId(_id) } if _id else { 'id': 'new' }
    response.content_type = 'application/json'
    return dumps(collection.find_and_modify(
        query,
        { '$set': data },
        upsert=True,
        new=True
    ))

@admin_api_app.post('/admin/api/<collection>/<_id>/delete')
def delete_resource(collection, _id):
    collection = db[collection]
    collection.remove(
        { '_id': ObjectId(_id) }
    )