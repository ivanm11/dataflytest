from datetime import datetime

from datafly.odm import Document

from db import db

class Page(Document):
    __collection__ = 'pages'

    @classmethod
    def get_latest(cls, _id):
        pages = list(
            db.pages.find({'id': _id})
                    .sort('published', -1)
                    .limit(1)
        )
        if len(pages):
            return pages.pop()

    def pre_save(self):
        self['published'] = datetime.utcnow()
